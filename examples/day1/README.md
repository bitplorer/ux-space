# examples/day1

Day-1 path: **Graph → Cap-gated apply → Channel Result → Peer apply.**

## 1. No Channel (always works)

```bash
PYTHONPATH=. python examples/day1/plan.py
```

Prints a Plan and a `bridge.call` Result. Uses a stand-in Cap token so you
can see the op shape. In product the token is Channel-minted.

## 2. Channel.boot (optional extra)

```bash
pip install 'ux-space[channel]' fastapi uvicorn
PYTHONPATH=. uvicorn examples.day1.app:app --host 127.0.0.1 --port 8080
```

`examples/day1/app.py` imports Channel **only** through `ux_space.wire`
(`boot`, `as_channel_result`). Cap mint stays `ch.control`. The page hosts
the Peer as package **`ux-space`**, not `"three"`.

## 3. Compose wire path

Product apps should not `import ux_channel`. Compose (or this Soft's
`ux_space.wire`) is the door:

```python
# compose-style Isolation — same seat as ux_space.wire
from ux_space import apply, space

graph = space("stage").host("stage-3d").node("hero", color="#6366f1")
ops = apply(graph, cap=channel_minted_cap)
# fold ops into the Channel Result the compose wire already builds
```

`Channel.boot` / `mount_channel` / Cap mint remain Channel. Do not stand
up a second Cap Host.

## Peer swap

The JS under `ux_space/peers/threejs/` is one adapter. Same `ops` apply
to a future non-Three Peer. Graph API does not change. See
[`ux_space/peers/README.md`](../../ux_space/peers/README.md).
