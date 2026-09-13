# Start here — ux-space

**Audience:** first-time users of this package.
**Promise:** one graph on the wire in five minutes.
**Time:** ~5 minutes. Facade **0.1.0a1**, IR v1.

Hard lock: [OWNERSHIP.md](OWNERSHIP.md). Runnable sample: [examples/day1/](examples/day1/).
Soft 2 leftover: locked shapes `box` / `sphere` / `plane` / `cylinder` — not the three.js catalog.

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

Same ops apply to a future canvas / WebGL Peer. Do not change `space()`.

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

---

## 5. Where next

| Goal | Doc |
|------|-----|
| HARD invariants | [OWNERSHIP.md](OWNERSHIP.md) |
| Peer swap | [ux_space/peers/README.md](ux_space/peers/README.md) |
| Isolation door | [ux_space/wire/README.md](ux_space/wire/README.md) |
| Examples | [examples/day1/](examples/day1/) |
