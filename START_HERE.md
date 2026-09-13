# Start here — ux-space

**Audience:** first-time users of this package.
**Promise:** one graph on the wire in five minutes.
**Time:** ~5 minutes. Facade **0.1.0a1**, IR v1.

Hard lock + leftover teaching: [OWNERSHIP.md](OWNERSHIP.md).
Human-readable Soft 1–10: [docs/](docs/).
Runnable sample: [examples/day1/](examples/day1/).
Soft-surface leftover tour: [examples/soft_surface/](examples/soft_surface/).
Soft 2 leftover: locked shapes `box` / `sphere` / `plane` / `cylinder` — not the three.js catalog.
Soft 3 leftover: optional `.camera` / `.light` nodes (`perspective` / `ambient` / `directional`) — not a materials catalog.
Soft 4 leftover: optional mesh `rotation` / `scale` + `material.type=basic` (`color` / `opacity`) — not a materials catalog.
Soft 5 leftover: canvas Peer proves swap — same `ux-space` register; day-1 stays threejs. Not dual concurrent Peers.
Soft 6 leftover: optional mesh `pickable` + Cap-gated `pick(hit)` — Peer reports `node_id` (and `point` if hit).
Soft 7 leftover: optional camera `orbit` / `pan` / `zoom` + Cap-gated `orbit` / `pan` / `zoom` — thin Peer apply, not OrbitControls.
Soft 8 leftover: mesh `material.type` thin set `{basic, standard}` — Soft 4 `basic` KEEP; optional `metalness` / `roughness` on `standard`. Not a materials catalog.
Soft 9 leftover: `.gltf(id, src=)` / `.texture(id, src=)` + `material.map` (texture id) — Cap-gated `apply` only. Not a public GLTFLoader dump.
Soft 10 leftover: additive shapes `cone` / `torus` — Soft 2 `box` / `sphere` / `plane` / `cylinder` KEEP. Same `.node(..., shape=)`. Not a geometry catalog.

## Reading path

This file is the tutorial. There is no `docs/tutorials/` copy.

| Step | Open | Diátaxis |
|------|------|----------|
| 1 | This file (five minutes below) | tutorial |
| 2 | [docs/how-to/author-and-apply.md](docs/how-to/author-and-apply.md) | how-to |
| 3 | [docs/how-to/swap-the-peer.md](docs/how-to/swap-the-peer.md) | how-to |
| 4 | [docs/reference/public-api.md](docs/reference/public-api.md) · [docs/reference/plan-ir.md](docs/reference/plan-ir.md) | reference |
| 5 | [docs/explanation/soft-leftovers.md](docs/explanation/soft-leftovers.md) · [OWNERSHIP.md](OWNERSHIP.md) | explanation |
| 6 | [CHANGELOG.md](CHANGELOG.md) | Unreleased, then Soft leftover history |

---

## 1. What this layer is (and is not)

**ux-space** turns a space graph into **data**: a Plan (JSON IR v1) that
travels on a Channel Result and is applied by a thin Peer.

| Owns | Does **not** own |
|------|------------------|
| Plan IR, `space()` / `Graph`, `apply` | Product behavior (`ux-behavior`) |
| Peer contract + day-1 Three.js adapter | DOM construction (`ux-dom`) |
| Isolation `wire/` | Intent / Cap mint (`ux-channel`) |

Not React. Not R3F. Not a Three.js catalog. Not motion — do not call this
`scene()`. That name is ux-motion.

Seat: **Python Plan / Ops → Channel Result → thin Peer apply.**

---

## 2. Five minutes

```bash
pip install ux-space
# or from this tree:
pip install -e .
```

```python
from ux_space import space, apply

graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
plan = graph.plan()
print(plan["kind"], plan["graph"]["nodes"][0]["id"])

# In product, `cap` comes from Channel (ch.control / CapService.mint).
# require_cap is server-side only — the token does not ride the Result.
ops = apply(graph, cap="channel-minted-cap-token")
print(ops[0]["op"], ops[0]["method"], ops[0]["package"])
print("cap" in ops[0], "meta" in ops[0])
```

Success: printed `plan hero` then `bridge.call apply ux-space` then `False False`.

Missing Cap fails closed:

```python
from ux_space import CapRequired

try:
    apply(graph, cap=None)
except CapRequired as exc:
    print(type(exc).__name__)
```

---

## 3. Peer apply (no browser required to author)

The day-1 Peer is `ux_space/peers/threejs/ux-space.js`. It registers as
**`ux-space`** (wrapping three.js from CDN) so the product surface is not
the Channel demo name `"three"`.

Same ops apply to the Soft 5 leftover canvas Peer (`peers/canvas`) or
another swap. Day-1 stays threejs. Do not change `space()`.

SSR host (Channel-compatible attributes, no `ux_channel` import):

```python
from ux_space import host_html

print(host_html("stage-3d", plan=graph.plan()))
```

---

## 4. Channel.boot / compose

Cap mint, `Channel.boot`, and `mount_channel` stay Channel. Product code
imports Channel only through `ux_space.wire` or a compose `wire/` door.

```python
# Isolation door — off ux_space.__all__
from ux_space.wire import boot, apply, space

ch = boot(app, secret="dev-secret-key-32chars-minimum!!!!")
```

Walkthrough: [examples/day1/README.md](examples/day1/README.md).
Soft-surface leftover tour: [examples/soft_surface/](examples/soft_surface/).

---

## 5. Where next

| Goal | Doc |
|------|-----|
| Author Soft 1–10 surfaces | [docs/how-to/author-and-apply.md](docs/how-to/author-and-apply.md) |
| Swap the Peer | [docs/how-to/swap-the-peer.md](docs/how-to/swap-the-peer.md) |
| Public names / Plan IR | [docs/reference/public-api.md](docs/reference/public-api.md) · [docs/reference/plan-ir.md](docs/reference/plan-ir.md) |
| Why leftovers + HOLD | [docs/explanation/soft-leftovers.md](docs/explanation/soft-leftovers.md) |
| HARD invariants | [OWNERSHIP.md](OWNERSHIP.md) |
| Isolation door | [ux_space/wire/README.md](ux_space/wire/README.md) |
| Examples | [examples/](examples/) · [day1](examples/day1/) · [soft_surface](examples/soft_surface/) |
