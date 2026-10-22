"""Soft-surface leftover tour: public space() / Graph + Cap-gated apply.

    pip install 'ux-space[channel]'
    PYTHONPATH=. python examples/soft_surface/plan.py

Soft 2–5 leftovers on the day-1 spine. Running it boots an in-process dev
Channel, mints a Cap for each ``space.*`` action and dispatches it. Channel
verifies each Cap for exactly its action; the token is not copied onto ops.

Soft 5 awareness: day-1 Peer stays threejs. Canvas Peer is swap-proof
only — same ``ux-space`` register, not a second concurrent Peer.
Soft 6 leftover: mesh ``pickable`` + Cap-gated ``pick(hit)``.
Soft 7 leftover: camera ``orbit`` / ``pan`` / ``zoom`` + Cap-gated verbs.
Soft 8 leftover: cylinder uses ``material.type=standard`` (metalness /
roughness). Sphere stays Soft 4 ``basic``.
Soft 9 leftover: ``.texture`` + ``material.map`` on the cylinder;
``.gltf`` prop. Load rides Cap-gated ``apply`` — no ``load()`` verb.
Soft 10 leftover: ``cone`` / ``torus`` via Soft 2 ``shape=``.
"""

from __future__ import annotations

from ux_space import Graph, dumps, host_html, space
from ux_space.wire import boot, register_actions


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
            orbit={"azimuth": 0.0, "polar": 1.35},
            pan={"x": 0.0, "y": 0.2},
            zoom=7.2,
        )
        .light("fill", light="ambient", color="#f8fafc")
        .light("key", light="directional", color="#fff7ed", position=(4, 6, 3))
        .texture("stripe", src="stripe.png")
        .gltf(
            "prop",
            src="prop.gltf",
            position=(0.6, 0.2, 0.8),
            rotation=(0.0, 0.4, 0.0),
            scale=0.45,
        )
        .node(
            "box",
            shape="box",
            color="#6366f1",
            position=(-2.4, 0.5, 0),
            rotation=(0.25, 0.6, 0.05),
            scale=1.0,
            pickable=True,
            material={"type": "standard", "map": "stripe"},
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
            material={
                "type": "standard",
                "color": "#38bdf8",
                "opacity": 0.9,
                "metalness": 0.25,
                "roughness": 0.45,
            },
        )
        .node(
            "cone",
            shape="cone",
            color="#f43f5e",
            position=(-1.6, 0.55, 1.8),
            rotation=(0.05, 0.2, 0),
            scale=0.9,
        )
        .node(
            "torus",
            shape="torus",
            color="#a855f7",
            position=(1.6, 0.55, 1.8),
            rotation=(0.8, 0.1, 0),
            scale=0.85,
            material={"type": "basic", "color": "#c084fc", "opacity": 0.95},
        )
    )


if __name__ == "__main__":
    graph = soft_surface()
    plan = graph.plan()
    print(dumps(plan))

    ch = boot(secret="dev-secret-key-32chars-minimum!!!!")
    register_actions(ch, graph, host="stage-3d")
    for action, args in (
        ("space.apply", {}),
        ("space.pick", {"node_id": "box", "point": [0.0, 0.5, 0.0]}),
        ("space.orbit", {"azimuth": 0.2, "polar": 1.2}),
        ("space.pan", {"x": 0.1, "y": 0.0}),
        ("space.zoom", {"distance": 6.0}),
    ):
        cap = ch.mint(action, args)
        op = ch.registry.dispatch({"action": action, "args": args, "cap": cap}).ops[0]
        print(action, op["op"], op["method"], op["package"], cap in repr(op))
    print("without Cap:", ch.registry.dispatch({"action": "space.apply", "args": {}}).error.code)
    print(host_html("stage-3d", plan=plan)[:80], "...")
