# How to swap the Peer

**Diátaxis:** how-to. Soft 5 leftover. Graph / `space()` / Cap-gated
`apply()` do not change. Authoritative swap contract:
[ux_space/peers/README.md](../../ux_space/peers/README.md).

## What stays

Same Plan + same `bridge.call` `{method: "apply", args: [plan]}` ops
from `ux_space.apply`. Product surface stays **`ux-space`**.

Day-1 default stays `ux_space/peers/threejs/ux-space.js`.

## Steps

1. Keep `uxBridge.register("ux-space", { mount, update, call })`.
2. Load `ux_space/peers/canvas/ux-space.js` **instead of**
   `ux_space/peers/threejs/ux-space.js` — or another adapter that
   implements the Peer contract (`PEER` in `ux_space.core`).
3. Do not change `space()` / `Graph` / `apply()`.
4. Do not register the product as `"three"` or `"canvas"`.

Python helper (both adapters):

```python
from ux_space.peers.canvas import adapter_path
from ux_space.peers.threejs import adapter_path as threejs_adapter_path

# packaged ux-space.js — same filename, different engine
assert adapter_path().endswith("ux-space.js")
assert threejs_adapter_path().endswith("ux-space.js")
```

## What canvas proves (and what it does not)

From `tests/test_soft5_peer_swap.py` and the later Soft leftover tests:

| Soft | canvas Peer |
|------|-------------|
| 2 | Soft 2 meshes as 2D fill (`box` / `sphere` / `plane` / `cylinder`) |
| 3 | camera / light nodes no-op (2D proof) |
| 4 | `position` / `rotation` / `scale` / color / `material.type=basic` |
| 6 | 2D hit-test on `pickable` — `{node_id, point?}` |
| 7 | `orbit` / `pan` / `zoom` call methods accepted (camera no-ops) |
| 8 | color / opacity; `standard` degrades as `basic` |
| 9 | gltf / texture skip or placeholder; `material.map` ignored |
| 10 | `cone` / `torus` as 2D fill; Soft 1–9 meshes still paint |

Swap **replaces** the engine. It is not dual concurrent Peers as taught
product. Do not load both adapters on one page.

HOLD: zero-Peer 3D, dual concurrent Peers as taught product, R3F,
materials catalog, full three.js catalog, Cap-on-ops, renaming motion,
sixth Cap Host. See [../explanation/soft-leftovers.md](../explanation/soft-leftovers.md).
