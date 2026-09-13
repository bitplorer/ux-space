# peers/canvas

Thin 2D-canvas Peer. Soft 5 leftover: proves the adapter can swap.

- **Register:** `uxBridge.register("ux-space", { mount, update, call })`
- **Not:** `uxBridge.register("canvas", …)` or `uxBridge.register("three", …)`
- **Loads:** no three.js — `HTMLCanvasElement` + `getContext("2d")`
- **Applies:** Soft 2 mesh nodes as filled 2D shapes (`box` / `sphere` /
  `plane` / `cylinder`). Honors `position` / `rotation` (2D approximation)
  / `scale` / top-level `color` / `material.type=basic` (`color` +
  `opacity`) when present. Soft 3 camera/light nodes are ignored (2D
  proof — no second camera API). Soft 6 leftover: pickable meshes
  report `{node_id, point?}` via 2D hit-test (no Raycaster / three.js).
  Soft 7 leftover: `orbit` / `pan` / `zoom` call methods are accepted
  (2D proof — camera control no-ops).   Soft 8 leftover: honors
  `material` color/opacity; `standard` degrades as `basic` (2D fill).
  Soft 9 leftover: gltf/texture degrade — skip load, placeholder for
  gltf, ignore `material.map`. Soft 1–8 meshes still paint.

`adapter_path()` returns the packaged `ux-space.js` (same helper as
`peers/threejs`). Day-1 default stays threejs — this Peer is the swap
proof, not a second product name.

`mount` reads optional `props.plan`. `call(..., "apply", [plan])` is the
Cap-gated verb the Python side emits. `update` forwards `props.plan`.
`destroy` removes the canvas.

Swap: see [`../README.md`](../README.md). Core Graph API does not change.
