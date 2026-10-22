"""Soft-surface leftover tour: public space() / Graph + Cap-gated apply.

    PYTHONPATH=. python examples/soft_surface/plan.py

Soft 2–5 leftovers on the day-1 spine. The verbs authorize from
``ctx.verified`` (the Cap the Channel Host verified), so they run inside
Channel handlers: see ``app.py``. Without one they fail closed with
``CapRequired``.

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

from ux_space import CapRequired, Graph, apply, dumps, host_html, space


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

    try:
        apply(graph, ctx=None)
    except CapRequired as exc:
        print("CapRequired:", exc)
    print(host_html("stage-3d", plan=plan)[:80], "...")
