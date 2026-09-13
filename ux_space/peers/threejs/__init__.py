"""Day-1 Three.js Peer. Register as ``ux-space``, not ``three``."""

from __future__ import annotations

from importlib.resources import files

ADAPTER_JS = "ux-space.js"


def adapter_path() -> str:
    return str(files("ux_space.peers.threejs").joinpath(ADAPTER_JS))
