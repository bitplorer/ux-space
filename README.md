# ux-space

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Server-authored space graphs for Python + JSON channels.

Pure Python facade. Thin Peer apply. No React. IR v1 additive.

This layer **owns one graph as data** plus one Cap-gated `apply`. It does not
own product behavior, Cap mint, or a 3D engine. Three.js is the day-1 Peer
adapter, not the identity.

| Layer | Name |
|-------|------|
| **PyPI / pip** | `ux-space` |
| **Import** | `ux_space` |
| **CLI** | *none (library)* |
| **Version** | `0.1.0a1` |
| **Python** | ≥ 3.14 |
| **License** | [MIT](LICENSE) |

**Not `ux-scene`.** That name is a dual door with ux-motion `scene()`. The
facade is `space()` / `Graph`.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Ownership](#ownership)
- [Audience](#audience)
- [API](#api)
- [Package contents](#package-contents)
- [Tests](#tests)
- [License](#license)

## Install

```bash
pip install ux-space
# Channel.boot demos:
pip install 'ux-space[channel]'
# or from this tree:
pip install -e .
python -c "from ux_space import space; print(space('x').node('a').plan()['id'])"
```

Repo: [bitplorer/ux-space](https://github.com/bitplorer/ux-space)

## Usage

```python
from ux_space import space, apply, to_result

graph = (
    space("stage")
    .host("stage-3d")
    .node("hero", shape="box", color="#6366f1")
)
# `cap` is Channel-minted (ch.control / CapService.mint). Server-side gate only —
# this Soft does not mint, and the token does not ride the Result.
ops = apply(graph, host="stage-3d", cap=channel_minted_cap)
result = to_result(ops)
# result["ops"][0]["op"] == "bridge.call"
# result["ops"][0]["method"] == "apply"
# result["ops"][0]["package"] == "ux-space"
```

Same graph as a Result:

```python
result = graph.apply(cap=channel_minted_cap)
```

The Peer (`peers/threejs`) registers as **`ux-space`** and applies the Plan
(Soft 2 leftover: locked shapes `box` / `sphere` / `plane` / `cylinder` —
not the three.js catalog. Soft 3 leftover: optional `.camera` / `.light`
nodes — `perspective` / `ambient` / `directional`. Soft 4 leftover:
optional mesh `rotation` / `scale` + `material.type=basic`. Soft 5
leftover: `peers/canvas` proves the swap under the same `ux-space`
register; day-1 stays threejs). Same ops — no second Graph API.

Five-minute path: [START_HERE.md](START_HERE.md). Hard invariants:
[OWNERSHIP.md](OWNERSHIP.md). Runnable samples: [examples/day1/](examples/day1/).

## Ownership

| Owns | Does **not** own |
|------|------------------|
| Plan IR v1, `space()` / `Graph` | Product `@action` (`ux-behavior`) |
| Cap-gated `apply` → `bridge.call` | Cap mint / Intent (`ux-channel`) |
| Peer contract + day-1 Three.js adapter | HTML construction (`ux-dom`) |
| Isolation door `wire/` | Product CLI (`ux-compose`) |

Full contract: [OWNERSHIP.md](OWNERSHIP.md).

## Audience

| You are… | Start |
|----------|--------|
| **New** | [START_HERE.md](START_HERE.md) |
| **Need the lock** | [OWNERSHIP.md](OWNERSHIP.md) |
| **Wiring Channel** | [ux_space/wire/README.md](ux_space/wire/README.md) · [examples/day1/](examples/day1/) |
| **Swapping the Peer** | [ux_space/peers/README.md](ux_space/peers/README.md) |

## API

Public names are `ux_space.__all__`. Frozen from `ux_space.core` only.

| Export | Role |
|--------|------|
| `space`, `Graph` | One scene graph |
| `apply` | Cap-gated verb → `bridge.call` method `apply` |
| `mount`, `update` | Channel-compatible bridge op builders (not verbs) |
| `to_result`, `host_html` | Result dict / SSR host attributes |
| `validate_plan`, `dumps`, `loads` | Plan IR |
| `PACKAGE`, `PEER`, `CONTRACT` | Wire package name + Peer contract |
| `CapRequired`, `PlanError` | Fail closed |

IR major is `v: "1"`. Additive fields only. Never reuse keys.

`wire/` is off this `__all__`. Product never imports `ux_channel` except
through that door (or a compose `wire/`).

## Package contents

| Path | Role |
|---|---|
| `ux_space/core/` | Plan IR, Graph, ops, Peer contract — day-1 truth |
| `ux_space/features/` | Stub for future Softs that import core |
| `ux_space/peers/threejs/` | Day-1 Three.js adapter (`uxBridge.register("ux-space")`) |
| `ux_space/peers/canvas/` | Soft 5 leftover swap-proof canvas Peer (same `ux-space` register) |
| `ux_space/wire/` | Isolation door (optional `ux-channel`) |
| `tests/` | Unit tests (no browser) |
| `examples/day1/` | Plan print + Channel.boot / compose path |

## Tests

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE). Copyright 2026 bitplorer.
