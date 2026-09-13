"""ux_space — server-authored space graphs for Python + JSON channels.

    from ux_space import space, apply

    graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
    result = graph.apply(cap=channel_minted_cap)
    # result == {"ok": True, "ops": [{"op": "bridge.call", "method": "apply", ...}]}

Public names come from ``ux_space.core`` only. ``wire/`` is the Isolation
door (off this ``__all__``). Never ``scene()`` — that name is ux-motion.
"""

from ux_space.core import (
    API_VERSION,
    APPLY_METHOD,
    CONTRACT,
    IR_VERSION,
    OP_APPLY,
    OP_CALL,
    OP_MOUNT,
    OP_UPDATE,
    PACKAGE,
    PEER,
    PEER_VERSION,
    CapRequired,
    Graph,
    PlanError,
    __version__,
    apply,
    dumps,
    host_html,
    loads,
    mount,
    space,
    to_result,
    update,
    validate_plan,
)

__all__ = [
    "API_VERSION",
    "APPLY_METHOD",
    "CONTRACT",
    "IR_VERSION",
    "OP_APPLY",
    "OP_CALL",
    "OP_MOUNT",
    "OP_UPDATE",
    "PACKAGE",
    "PEER",
    "PEER_VERSION",
    "CapRequired",
    "Graph",
    "PlanError",
    "__version__",
    "apply",
    "dumps",
    "host_html",
    "loads",
    "mount",
    "space",
    "to_result",
    "update",
    "validate_plan",
]
