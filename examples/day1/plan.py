"""Day-1: one graph → Plan IR → SSR host. Verbs need a Channel handler.

    PYTHONPATH=. python examples/day1/plan.py

``apply`` authorizes from ``ctx.verified`` (the Cap the Channel Host verified),
so it only runs inside a Channel handler: see ``app.py``. Without one it fails
closed with ``CapRequired``.
"""

from __future__ import annotations

from ux_space import CapRequired, apply, dumps, host_html, space

graph = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
plan = graph.plan()
print(dumps(plan))

try:
    apply(graph, ctx=None)
except CapRequired as exc:
    print("CapRequired:", exc)
print(host_html("stage-3d", plan=plan)[:80], "...")
