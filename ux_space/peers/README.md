# peers/

Adapters implement the **Peer contract** defined in `ux_space.core` (`PEER`).

| Day-1 adapter | Package name on the wire | Engine |
|---------------|--------------------------|--------|
| [`threejs/`](threejs/) | `ux-space` | three.js via CDN |

Three.js is **one adapter**, not the identity of this Soft. The Python graph,
Plan IR, and Cap-gated `apply()` do not mention Three.

## Swap path

Same Plan + same `bridge.call` `{method: "apply", args: [plan]}` ops.

1. Keep `uxBridge.register("ux-space", { mount, update, call })`.
2. Replace `peers/threejs/` with a canvas / WebGL / independent Peer lib
   that implements `apply` / `update` / `destroy`.
3. Do not change `space()` / `Graph` / `apply()`.
4. Do not register the product as `"three"` — that name is the Channel demo,
   not this Soft.

HOLD: zero-Peer 3D, dual Peers, materials catalog, full three.js catalog.
Soft 2 leftover: locked SHAPES (`box` / `sphere` / `plane` / `cylinder`).
