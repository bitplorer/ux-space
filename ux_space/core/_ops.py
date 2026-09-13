"""What a graph becomes on the wire.

apply(graph, host=..., cap=...) → one Cap-gated ``bridge.call`` (method ``apply``).
pick(hit, host=..., cap=...) → one Cap-gated ``bridge.call`` (method ``pick``).
orbit/pan/zoom(..., host=..., cap=...) → Cap-gated ``bridge.call`` methods
``orbit`` / ``pan`` / ``zoom``.

Ops speak the Channel bridge plane only:
``bridge.mount`` / ``bridge.update`` / ``bridge.call``.
This module does not import ``ux_channel``.
"""

from __future__ import annotations

import html
import json
from typing import Any, Mapping, Sequence

from ux_space.core._cap import require_cap
from ux_space.core._ir import validate_plan
from ux_space.core._peer import PACKAGE

OP_MOUNT = "bridge.mount"
OP_UPDATE = "bridge.update"
OP_CALL = "bridge.call"
OP_APPLY = OP_CALL
APPLY_METHOD = "apply"
PICK_METHOD = "pick"
ORBIT_METHOD = "orbit"
PAN_METHOD = "pan"
ZOOM_METHOD = "zoom"


def _op(op_type: str, **fields: Any) -> dict[str, Any]:
    body: dict[str, Any] = {"op": op_type}
    for key, value in fields.items():
        if value is not None:
            body[key] = value
    return body


def _as_plan(graph: Any) -> dict[str, Any]:
    plan_fn = getattr(graph, "plan", None)
    if callable(plan_fn):
        return validate_plan(plan_fn())
    if isinstance(graph, Mapping):
        return validate_plan(graph)
    raise TypeError("apply() expects a Graph or a plan mapping")


def mount(host: str, *, props: Any = None, package: str = PACKAGE) -> list[dict[str, Any]]:
    """Channel-compatible ``bridge.mount``. Not the Cap-gated verb."""
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host must be a non-empty string")
    return [
        _op(
            OP_MOUNT,
            id=host,
            package=package,
            props=props,
            target=f'[data-channel-bridge-id="{host}"]',
        )
    ]


def update(host: str, props: Any, *, replace: bool = False) -> list[dict[str, Any]]:
    """Channel-compatible ``bridge.update``. Not the Cap-gated verb."""
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host must be a non-empty string")
    return [_op(OP_UPDATE, id=host, props=props, replace=True if replace else None)]


def _as_hit(hit: Any) -> dict[str, Any]:
    if not isinstance(hit, Mapping):
        raise ValueError("pick() expects a hit mapping with node_id")
    nid = hit.get("node_id")
    if not isinstance(nid, str) or not nid.strip():
        raise ValueError("hit.node_id must be a non-empty string")
    out: dict[str, Any] = {"node_id": nid.strip()}
    if "point" in hit:
        val = hit["point"]
        if (
            not isinstance(val, (list, tuple))
            or len(val) != 3
            or any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in val)
        ):
            raise ValueError("hit.point must be [x, y, z] numbers")
        out["point"] = [float(val[0]), float(val[1]), float(val[2])]
    for key, val in hit.items():
        if key in out or key == "cap":
            continue
        out[key] = val
    return out


def _keep_unknown_payload(src: Mapping[str, Any], out: dict[str, Any]) -> dict[str, Any]:
    for key, val in src.items():
        if key in out or key == "cap":
            continue
        out[key] = val
    return out


def _as_orbit(orbit: Any) -> dict[str, Any]:
    if not isinstance(orbit, Mapping):
        raise ValueError("orbit() expects an orbit mapping with azimuth and/or polar")
    out: dict[str, Any] = {}
    if "azimuth" in orbit:
        val = orbit["azimuth"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ValueError("orbit.azimuth must be a number")
        out["azimuth"] = float(val)
    if "polar" in orbit:
        val = orbit["polar"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ValueError("orbit.polar must be a number")
        out["polar"] = float(val)
    if "azimuth" not in out and "polar" not in out:
        raise ValueError("orbit requires azimuth and/or polar")
    return _keep_unknown_payload(orbit, out)


def _as_pan(pan: Any) -> dict[str, Any]:
    if not isinstance(pan, Mapping):
        raise ValueError("pan() expects a pan mapping with x and/or y")
    out: dict[str, Any] = {}
    if "x" in pan:
        val = pan["x"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ValueError("pan.x must be a number")
        out["x"] = float(val)
    if "y" in pan:
        val = pan["y"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            raise ValueError("pan.y must be a number")
        out["y"] = float(val)
    if "x" not in out and "y" not in out:
        raise ValueError("pan requires x and/or y")
    return _keep_unknown_payload(pan, out)


def _as_zoom(zoom: Any) -> dict[str, Any]:
    if not isinstance(zoom, Mapping):
        raise ValueError("zoom() expects a zoom mapping with distance")
    val = zoom.get("distance")
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ValueError("zoom.distance must be a positive number")
    distance = float(val)
    if distance <= 0:
        raise ValueError("zoom.distance must be a positive number")
    out: dict[str, Any] = {"distance": distance}
    return _keep_unknown_payload(zoom, out)


def _call_payload(
    method: str,
    payload: Mapping[str, Any],
    *,
    host: str | None,
    cap: Any,
    package: str,
) -> list[dict[str, Any]]:
    require_cap(cap)
    hid = host
    if not isinstance(hid, str) or not hid.strip():
        raise ValueError(f"{method} requires host=")
    return [
        _op(
            OP_CALL,
            id=hid,
            method=method,
            args=[dict(payload)],
            package=package,
        )
    ]


def orbit(
    orbit: Any,
    *,
    host: str | None = None,
    cap: Any,
    package: str = PACKAGE,
) -> list[dict[str, Any]]:
    """Cap-gated Soft 7 verb. Orbit becomes Intent args → ``bridge.call`` method ``orbit``.

    ``cap`` must be a Channel-minted token. This Soft does not mint or verify.
    The token stays server-side — it is not copied onto the Result ops.
    """
    return _call_payload(ORBIT_METHOD, _as_orbit(orbit), host=host, cap=cap, package=package)


def pan(
    pan: Any,
    *,
    host: str | None = None,
    cap: Any,
    package: str = PACKAGE,
) -> list[dict[str, Any]]:
    """Cap-gated Soft 7 verb. Pan becomes Intent args → ``bridge.call`` method ``pan``.

    ``cap`` must be a Channel-minted token. This Soft does not mint or verify.
    The token stays server-side — it is not copied onto the Result ops.
    """
    return _call_payload(PAN_METHOD, _as_pan(pan), host=host, cap=cap, package=package)


def zoom(
    zoom: Any,
    *,
    host: str | None = None,
    cap: Any,
    package: str = PACKAGE,
) -> list[dict[str, Any]]:
    """Cap-gated Soft 7 verb. Zoom becomes Intent args → ``bridge.call`` method ``zoom``.

    ``cap`` must be a Channel-minted token. This Soft does not mint or verify.
    The token stays server-side — it is not copied onto the Result ops.
    """
    return _call_payload(ZOOM_METHOD, _as_zoom(zoom), host=host, cap=cap, package=package)


def pick(
    hit: Any,
    *,
    host: str | None = None,
    cap: Any,
    package: str = PACKAGE,
) -> list[dict[str, Any]]:
    """Cap-gated Soft 6 verb. Hit becomes Intent args → ``bridge.call`` method ``pick``.

    ``cap`` must be a Channel-minted token. This Soft does not mint or verify.
    The token stays server-side — it is not copied onto the Result ops.
    """
    require_cap(cap)
    payload = _as_hit(hit)
    hid = host
    if not isinstance(hid, str) or not hid.strip():
        raise ValueError("pick requires host=")
    return [
        _op(
            OP_CALL,
            id=hid,
            method=PICK_METHOD,
            args=[payload],
            package=package,
        )
    ]


def apply(
    graph: Any,
    *,
    host: str | None = None,
    cap: Any,
    package: str = PACKAGE,
) -> list[dict[str, Any]]:
    """The day-1 Cap-gated verb. Returns one ``bridge.call`` (method ``apply``).

    ``cap`` must be a Channel-minted token. This Soft does not mint or verify.
    The token stays server-side — it is not copied onto the Result ops.
    Soft 9 leftover: glTF / texture nodes travel on this same Plan — no
    ``load()`` verb.
    """
    require_cap(cap)
    plan = _as_plan(graph)
    hid = host or plan.get("graph", {}).get("host")
    if not isinstance(hid, str) or not hid.strip():
        raise ValueError("apply requires host= or plan.graph.host")
    return [
        _op(
            OP_CALL,
            id=hid,
            method=APPLY_METHOD,
            args=[plan],
            package=package,
        )
    ]


def to_result(
    ops: Sequence[Mapping[str, Any]],
    *,
    ok: bool = True,
    action: str | None = None,
) -> dict[str, Any]:
    """Channel-shaped Result dict. Does not import ux_channel."""
    result: dict[str, Any] = {"ok": ok, "ops": [dict(o) for o in ops]}
    if action:
        result["meta"] = {"action": action}
    return result


def host_html(
    host: str,
    *,
    plan: Mapping[str, Any] | None = None,
    class_name: str = "",
    tag: str = "div",
    inner: str = "",
) -> str:
    """SSR host element using Channel bridge attributes.

    Same ``data-channel-bridge-*`` contract as Channel ``mount_html``.
    Package is always ``ux-space`` so the product surface is not the demo name ``three``.
    Does not import ``ux_channel``.
    """
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host must be a non-empty string")
    cls = f' class="{html.escape(class_name, quote=True)}"' if class_name else ""
    props_s = ""
    if plan is not None:
        raw = json.dumps({"plan": dict(plan)}, default=str, separators=(",", ":"))
        props_s = f' data-channel-bridge-props="{html.escape(raw, quote=True)}"'
    hid = html.escape(host, quote=True)
    pkg = html.escape(PACKAGE, quote=True)
    return (
        f'<{tag} data-channel-bridge-id="{hid}"'
        f' data-channel-bridge-package="{pkg}"'
        f"{props_s}{cls}>{inner}</{tag}>"
    )


def dumps(plan: Mapping[str, Any]) -> str:
    return json.dumps(validate_plan(plan), separators=(",", ":"), sort_keys=True)


def loads(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if not isinstance(data, Mapping):
        raise ValueError("loads() expected a plan object")
    return validate_plan(data)
