"""Swap-proof canvas Peer. Register as ``ux-space``, not ``canvas``.

Day-1 default stays ``peers/threejs``. This adapter proves the Peer
can swap without changing Graph / Plan IR / ``apply()``.
"""

from __future__ import annotations

from importlib.resources import files

ADAPTER_JS = "ux-space.js"


def adapter_path() -> str:
    return str(files("ux_space.peers.canvas").joinpath(ADAPTER_JS))
