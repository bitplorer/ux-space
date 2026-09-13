# Changelog

All notable changes to **ux_space** are documented here.

Versioning follows [Semantic Versioning](https://semver.org/) for the
**library API** (`API_VERSION` / `__version__`).
The **plan IR** uses a separate major (`IR_VERSION` / plan field `v`).

New work lands under **Unreleased**. Do not invent a version heading
until the library API / Peer version changes. Dated Soft leftover
entries below are historical teaching for Soft 2–10 on `0.1.0a1`
(IR v1 additive). They stay — leftover-teach tests lock them.

---

## Unreleased

### Docs

- Soft 1–10 human-readable docs under Diátaxis (`docs/`). README is
  the front door; [START_HERE.md](START_HERE.md) is the reading path
  (tutorial). How-to / reference / explanation live under `docs/`.
  There is no empty `docs/tutorials/` shell — START_HERE's five-minute
  path is the tutorial.
- [OWNERSHIP.md](OWNERSHIP.md) leftover teaching stays the lock
  (Soft 2–10 leftover sections + KEEP / HOLD). Docs Soft cites that
  list; it does not invent APIs or dump R3F / dual Peers / Cap Host /
  Cap-on-ops / useFrame / catalogs / OrbitControls / generic pointer
  stack.
- Code fences in `docs/` adapt passing tests (`tests/test_graph.py`,
  `tests/test_ops.py`, `tests/test_soft2_shapes.py` … `tests/test_soft10_primitives.py`).

## 2026-09-13 — Soft 10: additive primitives (leftover)

- Leftover: IR `SHAPES` expands additively with a locked thin set
  `cone` / `torus` — not the geometry catalog. Soft 2 names KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Frozen Graph fluency:
  `.node(..., shape=...)` — no second Graph API. Additive IR v1 —
  keys never reused; unknown fields ignored. Peer `peers/threejs`
  maps `cone` → ConeGeometry and `torus` → TorusGeometry.
  `peers/canvas` swap-proof degrades Soft 10 as 2D fill without
  breaking Soft 1–9. Cap-gated `apply` KEEP. Cap NEVER on
  ops/Result. No second Graph API. `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. Soft 5 canvas swap-proof KEEP; day-1 stays
  threejs. Soft 6 pick/hit KEEP. Soft 7 orbit/pan/zoom KEEP. Soft 8
  `material.type` `{basic, standard}` KEEP. Soft 9 `{gltf, texture}`
  KEEP. `core/` stays truth.
- HOLD: full geometry catalog (`icosahedron` / `dodecahedron` /
  `torusKnot` / `capsule` / …), R3F, materials catalog
  (`phong` / `physical` / `lambert` / …), dual concurrent Peers as
  taught product, Cap-on-ops, zero-Peer, renaming motion, sixth Cap
  Host, generic pointer stack, useFrame, OrbitControls dump,
  GLTFLoader dump as public API.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply
  only — Cap-gated `apply` KEEP.

## 2026-09-13 — Soft 9: glTF / texture loaders (leftover)

- Leftover: thin locked loader surface for glTF and texture — not a
  loader catalog and not a public `GLTFLoader` dump. Frozen Graph
  names: `.gltf(id, src=, position=, rotation=, scale=)` and
  `.texture(id, src=)` — Soft 3 fluency, not `.node(..., kind=)` and
  not a `load()` verb. Additive IR v1 keys: node `kind` `gltf` /
  `texture`, node `src` (relative path or http(s) URL), `material.map`
  (texture node id). Keys never
  reused; unknown fields ignored. Load happens through Cap-gated
  `apply` only. Cap NEVER on ops/Result. `require_cap` server-side
  only. Peer `peers/threejs` applies texture / glTF as a Peer concern.
  `peers/canvas` swap-proof degrades (skip / placeholder). No second
  Graph API. `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. Soft 5 canvas swap-proof KEEP; day-1 stays
  threejs. Soft 6 pick/hit KEEP. Soft 7 orbit/pan/zoom KEEP. Soft 8
  `material.type` `{basic, standard}` KEEP. `core/` stays truth.
- HOLD: Soft 10 primitives, R3F, materials catalog
  (`phong` / `physical` / `lambert` / …), dual concurrent Peers as
  taught product, Cap-on-ops, zero-Peer, renaming motion, sixth Cap
  Host, generic pointer stack, useFrame, OrbitControls dump,
  GLTFLoader dump as public API.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply
  only — Cap-gated `apply` KEEP.

## 2026-09-13 — Soft 8: thin materials beyond basic (leftover)

- Leftover: mesh `material.type` expands to a locked thin set
  `{basic, standard}` — not the materials catalog. Soft 4 `{basic}`
  (`color` / `opacity`) KEEP. Soft 8 adds `standard` plus optional
  `metalness` / `roughness` (0..1). Top-level mesh `color` KEEP;
  `material.color` wins. Frozen Graph names:
  `.node(..., material={type: ...})` — no second Graph API.
  Additive IR v1 — keys never reused; unknown fields ignored.
  Peer `peers/threejs` maps `standard` → MeshStandardMaterial.
  `peers/canvas` swap-proof honors color/opacity; `standard`
  degrades as basic (2D fill). Cap-gated `apply` KEEP. Cap NEVER
  on ops/Result. No second Graph API. `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. Soft 5 canvas swap-proof KEEP; day-1 stays
  threejs. Soft 6 pick/hit KEEP. Soft 7 orbit/pan/zoom KEEP.
  `core/` stays truth.
- HOLD: Soft 9 loaders, Soft 10 primitives, R3F, materials catalog
  (`phong` / `physical` / `lambert` / …), dual concurrent Peers as
  taught product, Cap-on-ops, zero-Peer, renaming motion, sixth Cap
  Host, generic pointer stack.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply
  only — Cap-gated `apply` KEEP.

## 2026-09-13 — Soft 7: orbit/pan/zoom (leftover)

- Leftover: optional camera `orbit` `{azimuth?, polar?}` radians,
  `pan` `{x?, y?}`, and `zoom` (positive distance). Frozen Graph
  names: `.camera(..., orbit=, pan=, zoom=)`. Additive IR v1 — keys
  never reused; unknown fields ignored. Peer `peers/threejs` applies
  those fields as a thin spherical camera pose. `peers/canvas`
  swap-proof accepts the same Cap-gated call methods (2D camera
  control no-ops). Verbs: `orbit` / `pan` / `zoom`
  `(payload, host=, cap=)` → `bridge.call` methods `orbit` / `pan` /
  `zoom` → Result. Soft 7 is camera Plan ops, not a generic pointer
  stack. No OrbitControls product dump. No second Graph API.
  `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. Soft 5 canvas swap-proof KEEP; day-1 stays
  threejs. Soft 6 pick/hit KEEP. `core/` stays truth.
- HOLD: Soft 8 materials, Soft 9 loaders, Soft 10 primitives, R3F,
  materials catalog, dual concurrent Peers as taught product,
  Cap-on-ops, zero-Peer, renaming motion, sixth Cap Host, generic
  pointer stack.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply +
  Cap-gated `orbit()` / `pan()` / `zoom()` only.

## 2026-09-13 — Soft 6: pick/hit (leftover)

- Leftover: optional mesh `pickable` (bool). Frozen Graph name:
  `.node(..., pickable=)`. Additive IR v1 — keys never reused; unknown
  fields ignored. Peer `peers/threejs` raycasts on pointer over the
  canvas and reports `{node_id, point?}`. `peers/canvas` swap-proof
  hit-tests pickable 2D shapes (no three.js). Hit becomes Cap-gated
  Intent args via `pick(hit, host=, cap=)` → `bridge.call` method
  `pick` → Result. Channel owns click=Intent. No second Graph API.
  `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. Soft 5 canvas swap-proof KEEP; day-1 stays
  threejs. `core/` stays truth.
- HOLD: Soft 7 orbit/pan/zoom, R3F, materials catalog, dual concurrent
  Peers as taught product, Cap-on-ops, zero-Peer, renaming motion,
  sixth Cap Host.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer pick +
  Cap-gated `pick()` only.

## 2026-09-13 — Soft-surface example (leftover tour)

- Leftover tour: `examples/soft_surface/` composes the public Soft
  surface (`space()` / `Graph` + Cap-gated `apply` + day-1 Peer).
  Soft 2 SHAPES (`box` / `sphere` / `plane` / `cylinder`), Soft 3
  `.camera` / `.light` (`perspective` / `ambient` / `directional`),
  Soft 4 rotation/scale + `material.type=basic` (top-level color KEEP;
  `material.color` wins), Soft 5 awareness (day-1 stays threejs; canvas
  is swap-proof only — not dual concurrent Peers). No second Graph API.
  `features/` stays empty — Soft-surface demo is examples-only.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2–5 leftovers
  KEEP. `core/` stays truth.
- HOLD: R3F, materials catalog, dual concurrent Peers as taught product,
  Cap-on-ops, zero-Peer, renaming motion, sixth Cap Host. compose #30 +
  Valio stay parked. Soft DO empty.
- Same-commit leftover teaching + locks. Examples only — Graph / apply /
  Peer spine unchanged.

## 2026-09-13 — Soft 5: Peer-swap (canvas adapter leftover)

- Leftover: `peers/canvas` proves the Peer can swap. Same
  `uxBridge.register("ux-space", { mount, update, call })` — not a
  second product name (`canvas` / `three`). 2D canvas applies Soft 2
  mesh nodes (`box` / `sphere` / `plane` / `cylinder`) and Soft 4
  `position` / `rotation` / `scale` / `color` / `material.type=basic`.
  Soft 3 camera/light nodes no-op. Day-1 default stays `peers/threejs`.
  Graph / `space()` / Cap-gated `apply()` unchanged. No second Graph
  API. `features/` stays empty.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). Soft 4 rotation/scale +
  `material` `{basic}` KEEP. `core/` stays truth.
- HOLD: R3F, materials catalog, dual concurrent Peers as taught product,
  Cap-on-ops, zero-Peer, renaming motion, sixth Cap Host.
- Same-commit leftover teaching + locks. Swap path only — Graph/apply
  unchanged.

## 2026-09-13 — Soft 4: transform + material (locked thin leftover)

- Leftover: optional mesh `rotation` `[x,y,z]` radians and `scale`
  (number or `[x,y,z]`). Optional mesh `material` with locked type
  `{basic}` only and optional `color` / `opacity` (0..1). Top-level mesh
  `color` KEEP as shorthand; if both present, `material.color` wins.
  Frozen Graph names: `.node(..., rotation=, scale=, material=)`. Camera
  may take `rotation=`. Lights stay position/color. Peer `peers/threejs`
  applies rotation/scale and basic material; default mesh path stays
  sane when `material` is absent. Soft 2 shapes + Soft 3 camera/light
  unchanged. No second Graph API.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). Soft 3 camera/light KEEP
  (`perspective` / `ambient` / `directional`). `core/` stays truth.
- HOLD: Soft 5 Peer-swap, R3F, materials catalog, dual Peers, Cap-on-ops,
  zero-Peer, renaming motion, sixth Cap Host.
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply only.

## 2026-09-13 — Soft 3: camera/light nodes (locked set)

- Leftover: optional IR node kinds `camera` / `light` — locked set
  `perspective` camera + `ambient` / `directional` lights. Additive IR v1
  fields. Frozen Graph names: `.camera(...)` / `.light(...)`. Peer
  `peers/threejs` applies camera + lights when present; Soft 2 mesh nodes
  still work. No second Graph API.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. Soft 2 SHAPES KEEP
  (`box` / `sphere` / `plane` / `cylinder`). `core/` stays truth.
- HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, zero-Peer,
  renaming motion, Soft 4 transform/material (separate Soft).
- Same-commit leftover teaching + locks. Extend Plan IR + Peer apply only.

## 2026-09-13 — Soft 2: shapes pack (locked set, not catalog)

- Leftover: IR `SHAPES` is a locked Soft 2 set (`box`, `sphere`, `plane`,
  `cylinder`) — **not the full three.js catalog**. Peer `peers/threejs` is
  a thin geometry map. Graph / `space()` / Cap-gated `apply()` unchanged.
- KEEP: Isolation `wire/` only. Cap NEVER on ops/Result (`ops[].meta.cap`
  is disclosure). `require_cap` server-side only. Peer registers as
  `ux-space` not `three`. Cap Host KEEP on Channel (`Channel.boot` /
  `mount_channel`). Never `scene()` / `ux-scene`. `core/` stays truth.
- HOLD: R3F, materials catalog, dual Peers, Cap-on-ops, renaming motion,
  sixth Cap Host, ambient Client authority. Soft 3+ not in this change.
- Same-commit leftover teaching + locks. No second Graph API.

## 0.1.0a1 — 2026-09-13

Soft day-1. Council CLEAR.

### Library

- Package `ux-space` / import `ux_space`, Python ≥ 3.14, optional `channel` extra
- `space()` / `Graph` — one scene graph (not motion `scene()`)
- Plan IR v1 additive JSON + `validate_plan`
- Cap-gated `apply()` → Channel-compatible `bridge.call` method `apply`
- Cap mint stays Channel; missing token raises `CapRequired` server-side
- Cap token is not copied onto Result ops (`ops[].meta.cap` is disclosure)
- Peer contract + thin Three.js adapter registered as `ux-space`
- Isolation door `ux_space.wire` (off top `__all__`)
- `features/` stub for later Softs that import core

### Docs

- README, START_HERE, OWNERSHIP (HARD + Isolation + Cap + Peer-as-adapter)
- examples/day1: Plan print + Channel.boot / compose wire path
- Peer swap path under `ux_space/peers/`
