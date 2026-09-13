"""Soft 6 leftover locks — optional mesh pick/hit + Cap-gated pick.

Graph / space() stay Soft day-1. Soft 2 SHAPES, Soft 3 camera/light,
Soft 4 rotation/scale + material {basic}, Soft 5 canvas swap stay locked.
Isolation + Cap-on-ops absence stay locked.

Frozen Graph name: ``.node(..., pickable=)``.
IR field: ``pickable`` (bool) on mesh nodes.
Hit / Intent args: ``node_id`` + optional ``point`` [x,y,z].
Cap-gated verb: ``pick(hit, host=, cap=)`` → ``bridge.call`` method ``pick``.

HOLD Soft 7 orbit/pan/zoom, generic pointer stack, Behavior/Motion clone,
R3F, materials catalog, Cap-on-ops, zero-Peer, renaming motion,
dual concurrent Peers, sixth Cap Host.
"""

from __future__ import annotations

import inspect
import json
import unittest
from pathlib import Path

from ux_space import (
    CONTRACT,
    PACKAGE,
    PEER,
    CapRequired,
    Graph,
    PlanError,
    apply,
    pick,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import CAMERAS, LIGHTS, MATERIALS, SHAPES
from ux_space.peers.threejs import adapter_path as threejs_adapter_path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
SOFT10_SHAPES = frozenset({"box", "sphere", "plane", "cylinder", "cone", "torus"})
SOFT3_CAMERAS = frozenset({"perspective"})
SOFT3_LIGHTS = frozenset({"ambient", "directional"})
SOFT4_MATERIALS = frozenset({"basic"})
SOFT8_MATERIALS = frozenset({"basic", "standard"})
TEACHING = (
    ROOT / "OWNERSHIP.md",
    ROOT / "CHANGELOG.md",
    ROOT / "START_HERE.md",
)


def _mixed() -> Graph:
    return (
        space("stage")
        .host("stage-3d")
        .camera("eye", camera="perspective", position=(0, 0.35, 4.2), rotation=(0, 0.1, 0))
        .light("fill", light="ambient", color="#ffffff")
        .light("key", light="directional", position=(3, 4, 5))
        .node(
            "hero",
            shape="box",
            color="#6366f1",
            rotation=(0.1, 0.2, 0.3),
            scale=1.5,
            material={"type": "basic", "color": "#22c55e", "opacity": 0.8},
            pickable=True,
        )
    )


class Soft6PickHitTests(unittest.TestCase):
    def test_locked_sets_unchanged(self) -> None:
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertTrue(SOFT4_MATERIALS <= MATERIALS)
        self.assertNotIn("icosahedron", SHAPES)
        self.assertNotIn("torusKnot", SHAPES)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)
        self.assertNotIn("phong", MATERIALS)

    def test_validate_accepts_pickable_on_mesh(self) -> None:
        out = validate_plan(_mixed().plan())
        hero = out["graph"]["nodes"][3]
        self.assertEqual(hero["kind"], "node")
        self.assertEqual(hero["id"], "hero")
        self.assertIs(hero["pickable"], True)
        self.assertEqual(hero["shape"], "box")
        self.assertEqual(hero["rotation"], [0.1, 0.2, 0.3])

    def test_validate_accepts_pickable_false(self) -> None:
        plan = space("s").node("a", shape="sphere", pickable=False).plan()
        self.assertIs(plan["graph"]["nodes"][0]["pickable"], False)

    def test_pickable_absent_by_default(self) -> None:
        """Optional field — Soft 1–5 meshes stay unmarked."""
        plan = space("s").node("a", shape="box").plan()
        self.assertNotIn("pickable", plan["graph"]["nodes"][0])

    def test_unknown_fields_still_kept(self) -> None:
        plan = _mixed().plan()
        plan["graph"]["nodes"][3]["spin"] = 1
        out = validate_plan(plan)
        self.assertEqual(out["graph"]["nodes"][3]["spin"], 1)
        self.assertIs(out["graph"]["nodes"][3]["pickable"], True)

    def test_validate_rejects_bad_pickable(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", pickable="yes").plan()
        with self.assertRaises(PlanError):
            space("s").node("a", pickable=1).plan()
        with self.assertRaises(PlanError):
            validate_plan(
                {
                    "v": "1",
                    "kind": "plan",
                    "id": "x",
                    "graph": {
                        "kind": "graph",
                        "nodes": [
                            {
                                "kind": "node",
                                "id": "a",
                                "shape": "box",
                                "pickable": "true",
                            }
                        ],
                    },
                }
            )

    def test_frozen_graph_node_pickable(self) -> None:
        """Frozen Soft 6 name: Graph.node(pickable=). Not a second Graph API."""
        params = inspect.signature(Graph.node).parameters
        self.assertIn("pickable", params)
        self.assertIn("shape", params)
        self.assertIn("rotation", params)
        self.assertIn("scale", params)
        self.assertIn("material", params)
        self.assertNotIn("kind", params)
        self.assertFalse(hasattr(Graph, "pick"))
        self.assertFalse(hasattr(Graph, "hit"))
        self.assertFalse(hasattr(Graph, "pickable"))
        cam_params = inspect.signature(Graph.camera).parameters
        light_params = inspect.signature(Graph.light).parameters
        self.assertNotIn("pickable", cam_params)
        self.assertNotIn("pickable", light_params)

    def test_soft2_to_soft5_spine_unchanged(self) -> None:
        self.assertTrue(callable(space))
        self.assertTrue(callable(apply))
        self.assertIsInstance(space("stage"), Graph)
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                self.assertEqual(plan["graph"]["nodes"][0]["kind"], "node")
                self.assertEqual(plan["graph"]["nodes"][0]["shape"], shape)
        plan = space("s").camera("eye").light("fill").node("a").plan()
        self.assertEqual(plan["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(plan["graph"]["nodes"][1]["kind"], "light")
        self.assertEqual(plan["graph"]["nodes"][2]["kind"], "node")

    def test_pick_is_cap_gated_intent_args_to_result(self) -> None:
        token = "soft6-cap-MUST-NOT-SHIP"
        hit = {"node_id": "hero", "point": [0.1, 0.2, 0.3]}
        ops = pick(hit, host="stage-3d", cap=token)
        result = to_result(ops)
        self.assertEqual(len(ops), 1)
        op = ops[0]
        self.assertEqual(op["op"], "bridge.call")
        self.assertEqual(op["method"], "pick")
        self.assertEqual(op["package"], "ux-space")
        self.assertEqual(op["id"], "stage-3d")
        self.assertEqual(op["args"][0]["node_id"], "hero")
        self.assertEqual(op["args"][0]["point"], [0.1, 0.2, 0.3])
        self.assertNotIn("meta", op)
        self.assertNotIn("cap", op)
        dumped_ops = json.dumps(ops)
        dumped_result_ops = json.dumps(result["ops"])
        self.assertNotIn(token, dumped_ops)
        self.assertNotIn(token, dumped_result_ops)
        self.assertNotIn('"cap"', dumped_ops)
        self.assertTrue(result["ok"])

    def test_pick_point_optional(self) -> None:
        ops = pick({"node_id": "hero"}, host="h", cap="tok")
        self.assertEqual(ops[0]["args"][0]["node_id"], "hero")
        self.assertNotIn("point", ops[0]["args"][0])

    def test_pick_keeps_unknown_hit_fields(self) -> None:
        ops = pick({"node_id": "hero", "uv": [0.5, 0.5]}, host="h", cap="tok")
        self.assertEqual(ops[0]["args"][0]["uv"], [0.5, 0.5])

    def test_pick_requires_cap(self) -> None:
        hit = {"node_id": "hero"}
        with self.assertRaises(CapRequired):
            pick(hit, host="h", cap=None)
        with self.assertRaises(CapRequired):
            pick(hit, host="h", cap="")
        with self.assertRaises(CapRequired):
            pick(hit, host="h", cap="   ")

    def test_pick_requires_host_and_node_id(self) -> None:
        with self.assertRaises(ValueError):
            pick({"node_id": "hero"}, cap="tok")
        with self.assertRaises(ValueError):
            pick({}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            pick({"node_id": ""}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            pick({"node_id": "hero", "point": [1, 2]}, host="h", cap="tok")

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft6-apply-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        hero = ops[0]["args"][0]["graph"]["nodes"][3]
        self.assertIs(hero["pickable"], True)
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))

    def test_threejs_peer_raycasts_pickable_and_reports_node_id(self) -> None:
        js = Path(threejs_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("Raycaster", js)
        self.assertIn("pickable", js)
        self.assertIn("node_id", js)
        self.assertIn("pointerdown", js)
        self.assertIn("intersectObjects", js)
        self.assertIn("uxChannel.runAction", js)
        self.assertIn("data-channel-action", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("lookAt(", js)
        self.assertIn("BoxGeometry", js)
        self.assertIn("PerspectiveCamera", js)

    def test_canvas_peer_pick_without_breaking_soft5(self) -> None:
        from ux_space.peers.canvas import adapter_path as canvas_adapter_path

        js = Path(canvas_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn('getContext("2d")', js)
        self.assertIn("pickable", js)
        self.assertIn("node_id", js)
        self.assertIn("pointerdown", js)
        self.assertNotIn("Raycaster", js)
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("global.THREE", js)
        self.assertNotIn("PerspectiveCamera", js)
        self.assertNotIn("OrbitControls", js)

    def test_peer_contract_soft6(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("pick", PEER["methods"])
        self.assertIn("soft6", PEER)
        self.assertIn("pickable", PEER["soft6"].lower())
        self.assertIn("node_id", PEER["soft6"])
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 6 leftover", laws)

    def test_features_stays_empty(self) -> None:
        """Soft 6 lives in core IR + pick() + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft6LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft6(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 6 pick/hit + Cap-gated pick."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 6", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("pickable", lowered, path)
            self.assertIn("node_id", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 11. Soft 6 leftover")[1]
        hold = leftover.lower()
        self.assertIn("r3f", hold)
        self.assertIn("orbit", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)

    def test_start_here_soft6_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 6", text)
        self.assertIn("pickable", lowered)
        self.assertTrue(
            "pick" in lowered or "hit" in lowered,
            "START_HERE must leftover-teach Soft 6 pick/hit in one line",
        )
