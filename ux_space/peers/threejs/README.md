# peers/threejs

Thin Channel bridge adapter. CDN three.js is OK for day-1.

- **Register:** `uxBridge.register("ux-space", { mount, update, call })`
- **Not:** `uxBridge.register("three", …)` (Channel demo package name)
- **Loads:** `three@0.160.0` UMD from jsDelivr when `THREE` is absent
- **Applies:** Plan IR `graph.nodes` via a thin geometry map
  (Soft 2 leftover: `box` / `sphere` / `plane` / `cylinder` — not the catalog)
  and optional Soft 3 camera/light kinds (`perspective` / `ambient` /
  `directional`) when present. Soft 4 leftover: mesh `rotation` /
  `scale` and `material.type=basic` (color + opacity → MeshBasicMaterial)
  when present. Soft 6 leftover: optional mesh `pickable`. Pointer
  over the canvas raycasts and reports `{node_id, point?}`. Mesh nodes
  still apply without those fields.

`mount` reads optional `props.plan`. `call(..., "apply", [plan])` is the
Cap-gated verb the Python side emits. `update` forwards `props.plan`.

Day-1 default. Soft 5 leftover: [`../canvas/`](../canvas/) proves the
swap under the same `ux-space` register. Core Graph API does not change.

Swap: see [`../README.md`](../README.md).
