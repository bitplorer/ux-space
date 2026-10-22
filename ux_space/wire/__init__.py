"""Isolation door — the only place this package may import ux_channel.

Off the top-level ``ux_space.__all__``. Cap mint, Channel.boot, and
mount_channel stay Channel. This Soft does not host Caps.
"""

from __future__ import annotations

from typing import Any

from ux_space.core import PACKAGE, apply, host_html, orbit, pan, pick, space, to_result, zoom

__all__ = [
    "ACTIONS",
    "PACKAGE",
    "apply",
    "as_channel_result",
    "boot",
    "host_html",
    "mount_channel",
    "orbit",
    "pan",
    "pick",
    "register_actions",
    "register_manifest",
    "space",
    "to_result",
    "zoom",
]

# Channel action name per verb. Channel verifies a Cap for exactly one name.
ACTIONS = {method: f"space.{method}" for method in ("apply", "pick", "orbit", "pan", "zoom")}


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


def register_actions(ch: Any, graph: Any, *, host: str) -> None:
    """Expose the verbs as the Channel actions in ``ACTIONS``.

    The Channel Host verifies each Intent's Cap for exactly that action name
    (and its sealed args) before the handler runs; ux-space adds no check of
    its own. ``space.apply`` emits the server-authored ``graph``; the other
    actions take their payload from the Intent args.
    """
    registry = ch.registry
    if not registry.require_cap:
        raise ValueError("register_actions needs require_cap=True: the space.* actions must not be open")

    def call(verb: Any) -> Any:
        def handler(**args: Any) -> Any:
            return as_channel_result(verb(args, host=host))

        return handler

    registry.register(ACTIONS["apply"], lambda **_: as_channel_result(apply(graph, host=host)))
    for method, verb in (("pick", pick), ("orbit", orbit), ("pan", pan), ("zoom", zoom)):
        registry.register(ACTIONS[method], call(verb))
