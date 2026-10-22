# examples/soft_surface

Soft-surface leftover tour on the **public** Soft: `space()` / `Graph` +
Cap-gated `apply` + day-1 Peer adapter. No second Graph API.

Council CLEAR: Soft-surface only. Soft DO empty. compose #30 + Valio stay
parked. `features/` stays empty.

| Soft | What this example composes |
|------|----------------------------|
| 2 | Locked SHAPES: `box` / `sphere` / `plane` / `cylinder` |
| 3 | `.camera()` perspective · `.light()` ambient + directional |
| 4 | mesh `rotation` / `scale` + `material.type=basic` (color/opacity). Top-level `color` KEEP; `material.color` wins when both are set (sphere). |
| 5 | Day-1 Peer stays threejs. Canvas Peer is swap-proof only — do not teach dual concurrent Peers. |
| 6 | Optional mesh `pickable` on `box`. Cap-gated `pick(hit)` reports `node_id` (+ `point`). |
| 7 | Camera `orbit` / `pan` / `zoom` + Cap-gated `orbit` / `pan` / `zoom`. Thin Peer apply, not OrbitControls. |
| 8 | Cylinder `material.type=standard` (`metalness` / `roughness`). Sphere stays Soft 4 `basic`. Not a materials catalog. |
| 9 | `.texture("stripe", src=)` + box `material.map="stripe"` (first mesh — day-1 Peer apply). `.gltf("prop", src=)` with Soft 4 transform. Cap-gated `apply` only — not a public GLTFLoader dump. `src` is author-supplied (relative or http(s)). |
| 10 | Additive SHAPES `cone` / `torus` — Soft 2 `box` / `sphere` / `plane` / `cylinder` KEEP. Same `.node(..., shape=)`. Not a geometry catalog. |

## 1. In-process Channel

```bash
pip install 'ux-space[channel]'
PYTHONPATH=. python examples/soft_surface/plan.py
```

Boots a dev Channel, registers the `space.*` actions, mints a Cap for each
and dispatches it. Prints the Plan, each `bridge.call` op, and the refusal
of an Intent without a Cap. The token is not copied onto Result ops
(`ops[].meta.cap` is disclosure).

## 2. Channel.boot (optional extra)

```bash
pip install 'ux-space[channel]' fastapi uvicorn
PYTHONPATH=. uvicorn examples.soft_surface.app:app --host 127.0.0.1 --port 8080
```

`app.py` imports Channel **only** through `ux_space.wire` (`boot`,
`register_actions`). Cap mint stays `ch.control`. The page hosts the
day-1 Peer as package **`ux-space`** (`peers/threejs`), not `"three"` and
not a second canvas script.

## 3. Soft 5 swap (not this host)

Same Plan + same `apply` ops apply after a Peer swap. Load
`ux_space/peers/canvas/` **instead of** `peers/threejs` — same
`uxBridge.register("ux-space", …)`. Do not register `"canvas"` / `"three"`
and do not load both adapters on one page.

Swap steps: [`ux_space/peers/README.md`](../../ux_space/peers/README.md).

## Isolation / Cap

- Product never imports `ux_channel` except through `ux_space.wire`
- Cap Host KEEP on Channel (`Channel.boot` / `mount_channel`)
- Channel verifies each `space.*` action's Cap; ux-space does no authorization and the token never rides ops/Result
- Never `scene()` / `ux-scene`
