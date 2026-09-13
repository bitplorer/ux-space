"""Graph / space() — one scene graph. Not motion's scene()."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from ux_space.core._ir import KIND_GRAPH, KIND_NODE, KIND_PLAN, validate_plan
from ux_space.core._ops import apply as apply_ops
from ux_space.core._ops import to_result
from ux_space.core._version import IR_VERSION


class Graph:
    """One space graph. Method names are frozen. Not a motion Scene."""

    def __init__(self, gid: str | None = None) -> None:
        self._id = gid or f"space-{uuid4().hex[:10]}"
        self._host: str | None = None
        self._nodes: list[dict[str, Any]] = []

    def host(self, host_id: str) -> "Graph":
        if not isinstance(host_id, str) or not host_id.strip():
            raise ValueError("host must be a non-empty string")
        self._host = host_id.strip()
        return self

    def node(
        self,
        nid: str,
        *,
        shape: str = "box",
        color: str | None = None,
        position: list[float] | tuple[float, float, float] | None = None,
        **extra: Any,
    ) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {"kind": KIND_NODE, "id": nid.strip(), "shape": shape}
        if color is not None:
            item["color"] = color
        if position is not None:
            item["position"] = list(position)
        item.update(extra)
        self._nodes.append(item)
        return self

    def plan(self) -> dict[str, Any]:
        if not self._nodes:
            raise ValueError("graph has no nodes")
        graph: dict[str, Any] = {"kind": KIND_GRAPH, "nodes": [dict(n) for n in self._nodes]}
        if self._host:
            graph["host"] = self._host
        return validate_plan(
            {
                "v": IR_VERSION,
                "kind": KIND_PLAN,
                "id": self._id,
                "graph": graph,
            }
        )

    def apply(self, *, host: str | None = None, cap: Any) -> dict[str, Any]:
        """Cap-gated verb → Channel-shaped Result. Cap mint stays Channel."""
        hid = host or self._host
        return to_result(apply_ops(self, host=hid, cap=cap))

    def __repr__(self) -> str:
        return f"Graph(id={self._id!r}, host={self._host!r}, nodes={len(self._nodes)})"


def space(gid: str | None = None) -> Graph:
    """Build one space graph. Dual door with ux-motion ``scene()`` — do not alias."""
    return Graph(gid)
