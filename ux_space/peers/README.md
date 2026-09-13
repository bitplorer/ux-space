# peers/

Adapters implement the **Peer contract** defined in `ux_space.core` (`PEER`).

| Adapter | Package name on the wire | Engine | Role |
|---------|--------------------------|--------|------|
| [`threejs/`](threejs/) | `ux-space` | three.js via CDN | Day-1 default |
| [`canvas/`](canvas/) | `ux-space` | 2D canvas (no three.js) | Soft 5 leftover swap proof |

Three.js is **one adapter**, not the identity of this Soft. The Python graph,
Plan IR, and Cap-gated `apply()` do not mention Three. Soft 5 leftover:
`peers/canvas` proves the swap. Same package name — swap **replaces** the
engine; it does not register a second product (`canvas` / `three`) and is
not dual concurrent Peers as taught product. Day-1 stays threejs.

## Swap path

Same Plan + same `bridge.call` `{method: "apply", args: [plan]}` ops.

1. Keep `uxBridge.register("ux-space", { mount, update, call })`.
2. Load `peers/canvas/` (or another WebGL / independent Peer lib) instead
   of `peers/threejs/` — same `apply` / `update` / `destroy`.
3. Do not change `space()` / `Graph` / `apply()`.
4. Do not register the product as `"three"` or `"canvas"` — those names
   are not this Soft's product surface.

HOLD: zero-Peer 3D, dual concurrent Peers as taught product, materials
catalog, full three.js catalog, R3F, Cap-on-ops, renaming motion,
sixth Cap Host.
Soft 2 leftover: locked SHAPES (`box` / `sphere` / `plane` / `cylinder`).
Soft 3 leftover: optional camera/light node kinds (`perspective` /
`ambient` / `directional`).
Soft 4 leftover: mesh `rotation` / `scale` + `material` `{basic}`.
Soft 5 leftover: canvas Peer proves swap; day-1 stays threejs.
Soft 6 leftover: optional mesh `pickable`; Peer pick reports `node_id`
(+ `point`). Channel owns click=Intent.
Soft 7 leftover: camera `orbit` / `pan` / `zoom`; Cap-gated verbs.
Thin Peer apply — not OrbitControls.
Soft 8 leftover: thin `material.type` `{basic, standard}`. Canvas
honors color/opacity; `standard` degrades as basic.
Soft 9 leftover: thin glTF / texture loader nodes via Cap-gated
`apply`. Canvas degrades (skip / placeholder). HOLD Soft 10
primitives, materials catalog.
