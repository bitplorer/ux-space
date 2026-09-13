# examples/

Runnable paths for this Soft. Both compose the public surface —
`space()` / `Graph` + Cap-gated `apply` + Peer adapter. No second Graph.

| Path | What it shows |
|------|----------------|
| [day1/](day1/) | Day-1 spine: one graph → Cap-gated apply → Channel Result → Peer apply |
| [soft_surface/](soft_surface/) | Soft-surface leftover tour: Soft 2 SHAPES, Soft 3 camera/light, Soft 4 transform + `material.type=basic`, Soft 5 awareness (day-1 stays threejs; canvas is swap-proof only), Soft 6 `pickable` + Cap-gated `pick`, Soft 7 camera `orbit` / `pan` / `zoom`, Soft 8 `material.type=standard`, Soft 9 `.gltf` / `.texture` + `material.map`, Soft 10 `cone` / `torus` |

Always-works (no Channel):

```bash
PYTHONPATH=. python examples/day1/plan.py
PYTHONPATH=. python examples/soft_surface/plan.py
```

Isolation: Channel only through `ux_space.wire`. Cap mint stays Channel.
`features/` stays empty — these demos are examples-only.
