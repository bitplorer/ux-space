"""Isolation door — the only place this package may import ux_channel.

Off the top-level ``ux_space.__all__``. Cap mint, Channel.boot, and
mount_channel stay Channel. This Soft does not host Caps.
"""

from __future__ import annotations

from typing import Any

from ux_space.core import PACKAGE, apply, host_html, orbit, pan, pick, space, to_result, zoom

__all__ = [
    "PACKAGE",
    "apply",
    "as_channel_result",
    "boot",
    "host_html",
    "mount_channel",
    "orbit",
    "pan",
    "pick",
    "register_manifest",
    "space",
    "to_result",
    "zoom",
]


def boot(app: Any = None, **kwargs: Any) -> Any:
    """Channel.boot — Cap Host stays Channel."""
    from ux_channel import Channel

    return Channel.boot(app, **kwargs)


def mount_channel(app: Any, registry: Any, **kwargs: Any) -> Any:
    """Pass-through. Do not invent a second Cap Host."""
    from ux_channel.asgi.fastapi import mount_channel as _mount

    return _mount(app, registry, **kwargs)


def register_manifest(
    package: str = PACKAGE,
    *,
    methods: tuple[str, ...] = ("apply", "update", "destroy", "pick", "orbit", "pan", "zoom"),
    description: str = "ux-space Peer",
    hub: Any = None,
) -> Any:
    """Channel bridge manifest. Package name stays ``ux-space``."""
    from ux_channel.bridge.bridge_api import register_simple_manifest

    return register_simple_manifest(
        package, methods=methods, description=description, hub=hub
    )


def as_channel_result(ops: Any, *, ok: bool = True, **kwargs: Any) -> Any:
    """Prefer Channel ``Result`` when installed; else a Result dict."""
    try:
        from ux_channel import Result

        return Result(ok=ok, ops=list(ops), **kwargs)
    except ImportError:
        return to_result(ops, ok=ok)
