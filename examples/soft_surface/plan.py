"""Soft-surface leftover tour: public space() / Graph + Cap-gated apply.

    PYTHONPATH=. python examples/soft_surface/plan.py

Soft 2–5 leftovers on the day-1 spine. The token here is a stand-in for
the server-side gate. Product code passes a Channel-minted Cap
(ch.control / CapService.mint). The token is not copied onto Result ops.

Soft 5 awareness: day-1 Peer stays threejs. Canvas Peer is swap-proof
only — same ``ux-space`` register, not a second concurrent Peer.
Soft 6 leftover: mesh ``pickable`` + Cap-gated ``pick(hit)``.
"""

from __future__ import annotations

from ux_space import Graph, apply, dumps, host_html, pick, space, to_result

# Stand-in only. Product mints on Channel. Never copy onto ops/Result.
STAND_IN_CAP = "channel-minted-cap-token"


def soft_surface() -> Graph:
    """Compose Soft leftovers on the public Graph — not a second API."""
    return (
        space("soft-surface")
        .host("stage-3d")
        .camera(
            "eye",
            camera="perspective",
            position=(0, 1.4, 7.2),
            rotation=(-0.15, 0, 0),
        )
        .light("fill", light="ambient", color="#f8fafc")
        .light("key", light="directional", color="#fff7ed", position=(4, 6, 3))
        .node(
            "box",
            shape="box",
            color="#6366f1",
            position=(-2.4, 0.5, 0),
            rotation=(0.25, 0.6, 0.05),
            scale=1.0,
            pickable=True,
        )
        .node(
            "sphere",
            shape="sphere",
            color="#f59e0b",
            position=(-0.8, 0.55, 0),
            scale=0.85,
            material={"type": "basic", "color": "#22c55e", "opacity": 0.85},
        )
        .node(
            "plane",
            shape="plane",
            color="#1e293b",
            position=(0, -0.4, -1.2),
            rotation=(-1.15, 0, 0),
            scale=5.0,
        )
        .node(
            "cylinder",
            shape="cylinder",
            position=(2.2, 0.55, 0),
            rotation=(0.15, 0.4, 0),
            scale=[0.65, 1.15, 0.65],
            material={"type": "basic", "color": "#38bdf8", "opacity": 0.9},
        )
    )


if __name__ == "__main__":
    graph = soft_surface()
    plan = graph.plan()
    print(dumps(plan))

    ops = apply(graph, cap=STAND_IN_CAP)
    result = to_result(ops)
    op = result["ops"][0]
    print(op["op"], op["method"], op["package"])
    print("cap" in op, "meta" in op)
    hit_ops = pick({"node_id": "box", "point": [0.0, 0.5, 0.0]}, host="stage-3d", cap=STAND_IN_CAP)
    hit_op = to_result(hit_ops)["ops"][0]
    print(hit_op["op"], hit_op["method"], hit_op["package"])
    print("cap" in hit_op, "meta" in hit_op)
    print(host_html("stage-3d", plan=plan)[:80], "...")
