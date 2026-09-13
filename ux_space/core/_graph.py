"""Graph / space() — one scene graph. Not motion's scene()."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from ux_space.core._ir import (
    KIND_CAMERA,
    KIND_GLTF,
    KIND_GRAPH,
    KIND_LIGHT,
    KIND_NODE,
    KIND_PLAN,
    KIND_TEXTURE,
    validate_plan,
)
from ux_space.core._ops import apply as apply_ops
from ux_space.core._ops import to_result
from ux_space.core._version import IR_VERSION


class Graph:
    """One space graph. Method names are frozen. Not a motion Scene.

    Frozen builders: ``host``, ``node``, ``camera``, ``light``, ``plan``,
    ``apply``. Soft 3 leftover: ``camera(id, camera="perspective")`` and
    ``light(id, light="ambient"|"directional")`` — not ``node(..., kind=)``.
    Soft 4 leftover: ``node(..., rotation=, scale=, material=)``. Camera
    may take ``rotation=``. Lights stay position/color. Soft 6 leftover:
    ``node(..., pickable=)`` — optional bool on mesh nodes. Soft 7 leftover:
    ``camera(..., orbit=, pan=, zoom=)`` — camera control fields, not a
    second Graph API. Soft 8 leftover: ``material.type`` thin set
    ``{basic, standard}`` — same ``material=`` kwarg, not a second Graph.
    Soft 9 leftover: ``gltf(id, src=)`` and ``texture(id, src=)`` —
    loader nodes, not ``node(..., kind=)`` and not a ``load()`` verb.
    Texture composes with Soft 8 via ``material.map`` (texture node id).
    """

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
        rotation: list[float] | tuple[float, float, float] | None = None,
        scale: float | list[float] | tuple[float, float, float] | None = None,
        material: dict[str, Any] | None = None,
        pickable: bool | None = None,
        **extra: Any,
    ) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {"kind": KIND_NODE, "id": nid.strip(), "shape": shape}
        if color is not None:
            item["color"] = color
        if position is not None:
            item["position"] = list(position)
        if rotation is not None:
            item["rotation"] = rotation
        if scale is not None:
            item["scale"] = scale
        if material is not None:
            item["material"] = material
        if pickable is not None:
            item["pickable"] = pickable
        item.update(extra)
        self._nodes.append(item)
        return self

    def camera(
        self,
        nid: str,
        *,
        camera: str = "perspective",
        position: list[float] | tuple[float, float, float] | None = None,
        rotation: list[float] | tuple[float, float, float] | None = None,
        orbit: dict[str, Any] | None = None,
        pan: dict[str, Any] | None = None,
        zoom: float | None = None,
        **extra: Any,
    ) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {
            "kind": KIND_CAMERA,
            "id": nid.strip(),
            "camera": camera,
        }
        if position is not None:
            item["position"] = list(position)
        if rotation is not None:
            item["rotation"] = rotation
        if orbit is not None:
            item["orbit"] = orbit
        if pan is not None:
            item["pan"] = pan
        if zoom is not None:
            item["zoom"] = zoom
        item.update(extra)
        self._nodes.append(item)
        return self

    def light(
        self,
        nid: str,
        *,
        light: str = "ambient",
        color: str | None = None,
        position: list[float] | tuple[float, float, float] | None = None,
        **extra: Any,
    ) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {"kind": KIND_LIGHT, "id": nid.strip(), "light": light}
        if color is not None:
            item["color"] = color
        if position is not None:
            item["position"] = list(position)
        item.update(extra)
        self._nodes.append(item)
        return self

    def gltf(
        self,
        nid: str,
        *,
        src: str | None = None,
        position: list[float] | tuple[float, float, float] | None = None,
        rotation: list[float] | tuple[float, float, float] | None = None,
        scale: float | list[float] | tuple[float, float, float] | None = None,
        **extra: Any,
    ) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {"kind": KIND_GLTF, "id": nid.strip()}
        if src is not None:
            item["src"] = src
        if position is not None:
            item["position"] = list(position)
        if rotation is not None:
            item["rotation"] = rotation
        if scale is not None:
            item["scale"] = scale
        item.update(extra)
        self._nodes.append(item)
        return self

    def texture(self, nid: str, *, src: str | None = None, **extra: Any) -> "Graph":
        if not isinstance(nid, str) or not nid.strip():
            raise ValueError("node id must be a non-empty string")
        item: dict[str, Any] = {"kind": KIND_TEXTURE, "id": nid.strip()}
        if src is not None:
            item["src"] = src
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
