# examples/day1

Day-1 path: **Graph → Channel action `space.apply` → Channel Result → Peer apply.**

## 1. In-process Channel

```bash
pip install 'ux-space[channel]'
PYTHONPATH=. python examples/day1/plan.py
```

Boots a dev Channel, registers the `space.*` actions, mints a Cap for
`space.apply` and dispatches it. Prints the Plan, the `bridge.call` op
(the Cap is not on it), and the refusal of an Intent without a Cap.

## 2. Channel.boot (optional extra)

```bash
pip install 'ux-space[channel]' fastapi uvicorn
PYTHONPATH=. uvicorn examples.day1.app:app --host 127.0.0.1 --port 8080
```

`examples/day1/app.py` imports Channel **only** through `ux_space.wire`
(`boot`, `register_actions`). Cap mint stays `ch.control`. The page hosts
the Peer as package **`ux-space`**, not `"three"`.

## 3. Compose wire path

Product apps should not `import ux_channel`. Compose (or this Soft's
`ux_space.wire`) is the door:

```python
# compose-style Isolation — same seat as ux_space.wire
from ux_space import apply, space

graph = space("stage").host("stage-3d").node("hero", color="#6366f1")
ops = apply(graph)  # plan builder; clients reach it only as Channel action space.apply
# fold ops into the Channel Result the compose wire already builds
```

`Channel.boot` / `mount_channel` / Cap mint remain Channel. Do not stand
up a second Cap Host.

## Peer swap

The JS under `ux_space/peers/threejs/` is the day-1 adapter. Soft 5
leftover: `ux_space/peers/canvas/` proves the same `ops` apply after a
swap. Graph API does not change. See
[`ux_space/peers/README.md`](../../ux_space/peers/README.md).
