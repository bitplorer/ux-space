"""What a graph becomes on the wire.

apply(graph, host=..., cap=...) → one Cap-gated ``bridge.call`` (method ``apply``).

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
