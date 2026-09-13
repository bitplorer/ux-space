# Changelog

All notable changes to **ux_space** are documented here.

Versioning follows [Semantic Versioning](https://semver.org/) for the
**library API** (`API_VERSION` / `__version__`).
The **plan IR** uses a separate major (`IR_VERSION` / plan field `v`).

---

## 0.1.0a1 — 2026-09-13

Soft day-1. Council CLEAR.

### Library

- Package `ux-space` / import `ux_space`, Python ≥ 3.14, optional `channel` extra
- `space()` / `Graph` — one scene graph (not motion `scene()`)
- Plan IR v1 additive JSON + `validate_plan`
- Cap-gated `apply()` → Channel-compatible `bridge.call` method `apply`
- Cap mint stays Channel — documented; missing token raises `CapRequired`
- Peer contract + thin Three.js adapter registered as `ux-space`
- Isolation door `ux_space.wire` (off top `__all__`)
- `features/` stub for later Softs that import core

### Docs

- README, START_HERE, OWNERSHIP (HARD + Isolation + Cap + Peer-as-adapter)
- examples/day1: Plan print + Channel.boot / compose wire path
- Peer swap path under `ux_space/peers/`
