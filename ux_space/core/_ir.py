"""Plan IR v1 — one space graph as additive JSON.

Receivers MUST ignore unknown fields.
A new ``v`` is the only legal breaking change.
Keys are never reused.
"""

from __future__ import annotations

from typing import Any, Mapping

from ux_space.core._version import IR_VERSION

KIND_PLAN = "plan"
KIND_GRAPH = "graph"
KIND_NODE = "node"
KIND_CAMERA = "camera"
KIND_LIGHT = "light"

KINDS = frozenset({KIND_PLAN, KIND_GRAPH, KIND_NODE})
# Soft 2 leftover: locked set. HOLD the full three.js catalog.
SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
# Soft 3 leftover: locked node kinds. HOLD materials + Soft 4 transform.
NODE_KINDS = frozenset({KIND_NODE, KIND_CAMERA, KIND_LIGHT})
CAMERAS = frozenset({"perspective"})
LIGHTS = frozenset({"ambient", "directional"})


class PlanError(ValueError):
    """Invalid plan IR."""


def _req_str(obj: Mapping[str, Any], key: str, ctx: str) -> str:
    val = obj.get(key)
    if not isinstance(val, str) or not val.strip():
        raise PlanError(f"{ctx}: {key} must be a non-empty string")
    return val


def _opt_str(obj: Mapping[str, Any], key: str, ctx: str) -> str | None:
    val = obj.get(key)
    if val is None:
        return None
    if not isinstance(val, str) or not val.strip():
        raise PlanError(f"{ctx}: {key} must be a non-empty string when present")
    return val


def _opt_position(node: Mapping[str, Any], ctx: str) -> list[float] | None:
    if "position" not in node:
        return None
    pos = node["position"]
    if (
        not isinstance(pos, (list, tuple))
        or len(pos) != 3
        or any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in pos)
    ):
        raise PlanError(f"{ctx}: position must be [x, y, z] numbers")
    return [float(pos[0]), float(pos[1]), float(pos[2])]


def _keep_unknown(node: Mapping[str, Any], out: dict[str, Any]) -> dict[str, Any]:
    # Additive: unknown fields are kept so receivers can ignore them.
    for key, val in node.items():
        if key not in out:
            out[key] = val
    return out


def _validate_mesh_node(node: Mapping[str, Any], nid: str, ctx: str) -> dict[str, Any]:
    shape = node.get("shape", "box")
    if not isinstance(shape, str) or shape not in SHAPES:
        raise PlanError(f"{ctx}: shape must be one of {sorted(SHAPES)}")
    out: dict[str, Any] = {"kind": KIND_NODE, "id": nid, "shape": shape}
    color = _opt_str(node, "color", ctx)
    if color is not None:
        out["color"] = color
    pos = _opt_position(node, ctx)
    if pos is not None:
        out["position"] = pos
    return _keep_unknown(node, out)


def _validate_camera_node(node: Mapping[str, Any], nid: str, ctx: str) -> dict[str, Any]:
    camera = node.get("camera", "perspective")
    if not isinstance(camera, str) or camera not in CAMERAS:
        raise PlanError(f"{ctx}: camera must be one of {sorted(CAMERAS)}")
    out: dict[str, Any] = {"kind": KIND_CAMERA, "id": nid, "camera": camera}
    pos = _opt_position(node, ctx)
    if pos is not None:
        out["position"] = pos
    return _keep_unknown(node, out)


def _validate_light_node(node: Mapping[str, Any], nid: str, ctx: str) -> dict[str, Any]:
    light = node.get("light", "ambient")
    if not isinstance(light, str) or light not in LIGHTS:
        raise PlanError(f"{ctx}: light must be one of {sorted(LIGHTS)}")
    out: dict[str, Any] = {"kind": KIND_LIGHT, "id": nid, "light": light}
    color = _opt_str(node, "color", ctx)
    if color is not None:
        out["color"] = color
    pos = _opt_position(node, ctx)
    if pos is not None:
        out["position"] = pos
    return _keep_unknown(node, out)


def _validate_node(node: Mapping[str, Any], ctx: str) -> dict[str, Any]:
    if not isinstance(node, Mapping):
        raise PlanError(f"{ctx} must be an object")
    kind = node.get("kind", KIND_NODE)
    if kind not in NODE_KINDS:
        raise PlanError(f"{ctx}: kind must be one of {sorted(NODE_KINDS)}")
    nid = _req_str(node, "id", ctx)
    if kind == KIND_CAMERA:
        return _validate_camera_node(node, nid, ctx)
    if kind == KIND_LIGHT:
        return _validate_light_node(node, nid, ctx)
    return _validate_mesh_node(node, nid, ctx)


def _validate_graph(graph: Mapping[str, Any], ctx: str) -> dict[str, Any]:
    if not isinstance(graph, Mapping):
        raise PlanError(f"{ctx} must be an object")
    kind = graph.get("kind", KIND_GRAPH)
    if kind != KIND_GRAPH:
        raise PlanError(f"{ctx}: kind must be {KIND_GRAPH!r}")
    nodes = graph.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise PlanError(f"{ctx}: nodes must be a non-empty list")
    out: dict[str, Any] = {
        "kind": KIND_GRAPH,
        "nodes": [_validate_node(n, f"{ctx}.nodes[{i}]") for i, n in enumerate(nodes)],
    }
    host = _opt_str(graph, "host", ctx)
    if host is not None:
        out["host"] = host
    for key, val in graph.items():
        if key not in out:
            out[key] = val
    return out


def validate_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return a JSON-ready plan. Unknown fields are kept."""
    if not isinstance(plan, Mapping):
        raise PlanError("plan must be an object")
    v = plan.get("v", IR_VERSION)
    if str(v) != IR_VERSION:
        raise PlanError(f"plan.v must be {IR_VERSION!r}")
    kind = plan.get("kind", KIND_PLAN)
    if kind != KIND_PLAN:
        raise PlanError(f"plan.kind must be {KIND_PLAN!r}")
    pid = _req_str(plan, "id", "plan")
    graph = plan.get("graph")
    if not isinstance(graph, Mapping):
        raise PlanError("plan.graph is required")
    out: dict[str, Any] = {
        "v": IR_VERSION,
        "kind": KIND_PLAN,
        "id": pid,
        "graph": _validate_graph(graph, "plan.graph"),
    }
    for key, val in plan.items():
        if key not in out:
            out[key] = val
    return out
