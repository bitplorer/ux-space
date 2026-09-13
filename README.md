# ux-space

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Server-authored space graphs for Python + JSON channels.

Pure Python facade. Thin Peer apply. No React. IR v1 additive.

This layer **owns one graph as data** plus Cap-gated verbs (`apply`,
and leftover `pick` / `orbit` / `pan` / `zoom`). It does not own
product behavior, Cap mint, or a 3D engine. Three.js is the day-1 Peer
adapter, not the identity.

| Layer | Name |
|-------|------|
| **PyPI / pip** | `ux-space` |
| **Import** | `ux_space` |
| **CLI** | *none (library)* |
| **Version** | `0.1.0a1` |
| **Python** | ≥ 3.14 |
| **License** | [MIT](LICENSE) |

**Not `ux-scene`.** That name is a dual door with ux-motion `scene()`.
The facade is `space()` / `Graph`.

## Start

| You are… | Open |
|----------|------|
| **New** | [START_HERE.md](START_HERE.md) — five minutes, then the reading path |
| **Soft 1–10 how-to / reference** | [docs/](docs/) |
| **Need the lock** | [OWNERSHIP.md](OWNERSHIP.md) |
| **What changed** | [CHANGELOG.md](CHANGELOG.md) (`Unreleased`, then Soft leftover history) |

Repo: [bitplorer/ux-space](https://github.com/bitplorer/ux-space)

## Install

```bash
pip install ux-space
# Channel.boot demos:
pip install 'ux-space[channel]'
# or from this tree:
pip install -e .
python -c "from ux_space import space; print(space('x').node('a').plan()['id'])"
```

## Usage

```python
from ux_space import space, apply, to_result

graph = (
    space("stage")
    .host("stage-3d")
    .node("hero", shape="box", color="#6366f1")
)
# `cap` is Channel-minted (ch.control / CapService.mint). Server-side gate
# only — this Soft does not mint, and the token does not ride the Result.
ops = apply(graph, host="stage-3d", cap=channel_minted_cap)
result = to_result(ops)
# result["ops"][0]["op"] == "bridge.call"
# result["ops"][0]["method"] == "apply"
# result["ops"][0]["package"] == "ux-space"
```

Same graph as a Result: `graph.apply(cap=channel_minted_cap)`.

Public names are `ux_space.__all__`, frozen from `ux_space.core` only.
`wire/` is off that `__all__`. Soft 1–10 surfaces, fences, and the HOLD
list live under [docs/](docs/). Leftover teaching that tests lock lives
in [OWNERSHIP.md](OWNERSHIP.md).

## Tests

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
```

Runnable samples: [examples/day1/](examples/day1/) ·
[examples/soft_surface/](examples/soft_surface/).

## License

MIT — see [LICENSE](LICENSE). Copyright 2026 bitplorer.
