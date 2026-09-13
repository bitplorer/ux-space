# Changelog

All notable changes to **ux_space** are documented here.

Versioning follows [Semantic Versioning](https://semver.org/) for the
**library API** (`API_VERSION` / `__version__`).
The **plan IR** uses a separate major (`IR_VERSION` / plan field `v`).

---

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
