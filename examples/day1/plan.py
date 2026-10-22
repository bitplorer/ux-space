"""Day-1: one graph → Channel action ``space.apply`` → Channel-shaped Result.

    pip install 'ux-space[channel]'
    PYTHONPATH=. python examples/day1/plan.py

Boots an in-process dev Channel, mints a Cap for ``space.apply`` and
dispatches it. Channel verifies the Cap; the token is not copied onto ops.
"""

from __future__ import annotations

from ux_space import dumps, host_html, space
from ux_space.wire import boot, register_actions

graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
plan = graph.plan()
print(dumps(plan))

ch = boot(secret="dev-secret-key-32chars-minimum!!!!")
register_actions(ch, graph, host="stage-3d")
cap = ch.mint("space.apply", {})
op = ch.registry.dispatch({"action": "space.apply", "args": {}, "cap": cap}).ops[0]
print(op["op"], op["method"], op["package"], cap in repr(op))
print("without Cap:", ch.registry.dispatch({"action": "space.apply", "args": {}}).error.code)
print(host_html("stage-3d", plan=plan)[:80], "...")
