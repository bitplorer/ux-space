"""Day-1 truth: Plan IR, Graph/space(), ops, Peer contract.

Features import this package. Peers implement PEER. Product public
names are re-exported from ``ux_space`` — do not import private modules.
"""

from ux_space.core._cap import CapRequired
from ux_space.core._contract import CONTRACT
from ux_space.core._graph import Graph, space
from ux_space.core._ir import PlanError, validate_plan
from ux_space.core._ops import (
    APPLY_METHOD,
    OP_APPLY,
    OP_CALL,
    OP_MOUNT,
    OP_UPDATE,
    PICK_METHOD,
    apply,
    dumps,
    host_html,
    loads,
    mount,
    pick,
    to_result,
    update,
)
from ux_space.core._peer import PACKAGE, PEER
from ux_space.core._version import API_VERSION, IR_VERSION, PEER_VERSION, __version__

__all__ = [
    "API_VERSION",
    "APPLY_METHOD",
    "CONTRACT",
    "IR_VERSION",
    "OP_APPLY",
    "OP_CALL",
    "OP_MOUNT",
    "OP_UPDATE",
    "PICK_METHOD",
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
    "pick",
    "space",
    "to_result",
    "update",
    "validate_plan",
]
