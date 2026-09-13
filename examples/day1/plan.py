"""Day-1: one graph → Cap-gated apply → Channel-shaped Result.

    PYTHONPATH=. python examples/day1/plan.py

The token here is a stand-in for the server-side gate. Product code
passes a Channel-minted Cap (ch.control / CapService.mint). The token
is not copied onto Result ops.
"""

from __future__ import annotations

from ux_space import apply, dumps, host_html, space, to_result

graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
plan = graph.plan()
print(dumps(plan))

ops = apply(graph, cap="channel-minted-cap-token")
result = to_result(ops)
print(result["ops"][0]["op"], result["ops"][0]["method"], result["ops"][0]["package"])
print(host_html("stage-3d", plan=plan)[:80], "...")
