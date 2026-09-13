# Soft 1–10 leftovers

**Diátaxis:** explanation. This page teaches why the Soft 1–10 spine
stops where it stops. The lock is [OWNERSHIP.md](../../OWNERSHIP.md)
§ leftover 2–10. Docs Soft does not replace those sections.

## Seat

Python Plan / Ops → Channel Result → thin Peer apply.

ux-space authors one graph and emits Cap-gated `bridge.call` ops.
Channel mints Caps (`Channel.boot` / `mount_channel` / `CapService.mint`).
The Peer applies ops. Three.js is the day-1 adapter, not the identity.

Soft 1 is that seat: `space()` / `Graph`, Plan IR v1, Cap-gated `apply`,
`ux_space/peers/threejs` registered as `"ux-space"`, Isolation `wire/`.
`features/` stays empty — Soft 2–10 live in `core/` + Peer apply.

## What each leftover added

| Soft | Leftover | Still one Graph |
|------|----------|-----------------|
| 1 | Graph + `apply` + day-1 Peer | yes |
| 2 | Locked `SHAPES` `box` / `sphere` / `plane` / `cylinder` | same `.node(..., shape=)` |
| 3 | `.camera` / `.light` (`perspective` / `ambient` / `directional`) | new builders, not `kind=` on `.node` |
| 4 | mesh `rotation` / `scale` + `material` `{basic}` | same `.node` kwargs |
| 5 | `peers/canvas` swap proof | Graph / `apply` unchanged |
| 6 | mesh `pickable` + Cap-gated `pick(hit)` | same `.node`; verb is not a Graph method |
| 7 | camera `orbit` / `pan` / `zoom` + Cap-gated verbs | same `.camera` kwargs |
| 8 | `material.type` `{basic, standard}` + `metalness` / `roughness` | same `material=` |
| 9 | `.gltf` / `.texture` + `material.map` | Cap-gated `apply` only — no `load()` |
| 10 | `cone` / `torus` | Soft 2 `shape=` KEEP |

Each Soft is leftover teaching plus a lock: Isolation `wire/` only;
Cap NEVER on ops / Result; `require_cap` server-side only; Peer
registers as `ux-space` not `three`; Cap Host KEEP on Channel; never
`scene()` / `ux-scene`; `core/` stays truth.

## HOLD (current)

Cited from OWNERSHIP Soft 10 leftover + HARD §1.10. Honest list —
this Soft does not implement these:

- full geometry catalog (`icosahedron` / `dodecahedron` / `torusKnot` /
  `capsule` / …)
- materials catalog (`phong` / `physical` / `lambert` / …)
- React / R3F dump
- dual concurrent Peers as taught product
- Cap-on-ops (token on Result / `ops[].meta.cap`)
- zero-Peer 3D
- renaming motion (`scene()` / `ux-scene`)
- sixth Cap Host beside Channel
- generic pointer stack
- `useFrame`
- OrbitControls dump
- GLTFLoader dump as public API
- ambient Client authority
- teaching Channel specialty ops beyond the bridge plane

Historical leftover sections in OWNERSHIP still HOLD the *next* Soft
as of that landing (Soft 6 HOLD names Soft 7, Soft 8 HOLD names Soft 9 /
10, …). That is leftover teaching, not a claim those Softs are unshipped
in the tree. The tree is Soft 10. Current HOLD is the list above.

## Why not dump the catalogs

The Peer is an adapter. A three.js catalog, R3F, OrbitControls, or a
public GLTFLoader would make the engine the product. Soft 2 / 8 / 9 / 10
unlock thin locked sets so the Plan stays data. Canvas swap-proof
degrades later Softs instead of forking Graph.

## Where leftover teaching lives

| Surface | Role |
|---------|------|
| [OWNERSHIP.md](../../OWNERSHIP.md) §7–15 | Leftover + KEEP / HOLD per Soft (tests lock phrases) |
| [CHANGELOG.md](../../CHANGELOG.md) | Dated Soft leftover entries; Docs Soft under Unreleased |
| [START_HERE.md](../../START_HERE.md) | One leftover line per Soft 2–10 |
| `ux_space.CONTRACT["laws"]` | Frozen product laws |
| `tests/test_soft2_shapes.py` … `tests/test_soft10_primitives.py` | LeftoverTeachingTests |
