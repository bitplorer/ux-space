"""Soft 4 leftover locks — mesh transform + thin material {basic}.

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES and
Soft 3 camera/light stay locked. Isolation + Cap-on-ops absence stay
locked. Frozen Graph.node kwargs: rotation / scale / material.
HOLD materials catalog, R3F, Soft 5 Peer-swap.
"""

from __future__ import annotations

import inspect
import json
import unittest
from pathlib import Path

from ux_space import (
    Graph,
    PlanError,
    apply,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import CAMERAS, LIGHTS, MATERIALS, SHAPES
from ux_space.peers.threejs import adapter_path

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
        )
    )


class Soft4TransformMaterialTests(unittest.TestCase):
    def test_locked_sets(self) -> None:
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertTrue(SOFT4_MATERIALS <= MATERIALS)
        self.assertIn("basic", MATERIALS)
        self.assertIn("standard", MATERIALS)
        self.assertNotIn("physical", MATERIALS)
        self.assertNotIn("phong", MATERIALS)
        self.assertNotIn("icosahedron", SHAPES)
        self.assertNotIn("torusKnot", SHAPES)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)

    def test_validate_accepts_rotation_scale_material(self) -> None:
        out = validate_plan(_mixed().plan())
        hero = out["graph"]["nodes"][3]
        self.assertEqual(hero["kind"], "node")
        self.assertEqual(hero["rotation"], [0.1, 0.2, 0.3])
        self.assertEqual(hero["scale"], 1.5)
        self.assertEqual(hero["material"]["type"], "basic")
        self.assertEqual(hero["material"]["color"], "#22c55e")
        self.assertEqual(hero["material"]["opacity"], 0.8)
        eye = out["graph"]["nodes"][0]
        self.assertEqual(eye["kind"], "camera")
        self.assertEqual(eye["rotation"], [0.0, 0.1, 0.0])

    def test_validate_accepts_scale_xyz(self) -> None:
        out = validate_plan(
            {
                "v": "1",
                "kind": "plan",
                "id": "stage",
                "graph": {
                    "kind": "graph",
                    "nodes": [
                        {
                            "kind": "node",
                            "id": "hero",
                            "shape": "sphere",
                            "scale": [1, 2, 3],
                        }
                    ],
                },
            }
        )
        self.assertEqual(out["graph"]["nodes"][0]["scale"], [1.0, 2.0, 3.0])

    def test_validate_accepts_top_level_color_shorthand(self) -> None:
        """Top-level mesh color KEEP — still works without material."""
        out = space("s").node("a", shape="plane", color="#111111").plan()
        self.assertEqual(out["graph"]["nodes"][0]["color"], "#111111")
        self.assertNotIn("material", out["graph"]["nodes"][0])

    def test_material_color_wins_over_top_level_color(self) -> None:
        """If both present, material.color wins — both fields stay on IR."""
        plan = (
            space("s")
            .node(
                "a",
                color="#111111",
                material={"type": "basic", "color": "#eeeeee"},
            )
            .plan()
        )
        node = plan["graph"]["nodes"][0]
        self.assertEqual(node["color"], "#111111")
        self.assertEqual(node["material"]["color"], "#eeeeee")
        js = Path(adapter_path()).read_text(encoding="utf-8")
        # Peer must prefer material.color over top-level color shorthand.
        self.assertIn("material.color", js)
        self.assertIn("|| node.color", js)

    def test_validate_rejects_bad_rotation(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", rotation=(1, 2)).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", rotation="yaw").plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", rotation=(1, True, 0)).plan()

    def test_validate_rejects_bad_scale(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", scale=(1, 2)).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", scale=True).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", scale="2").plan()

    def test_validate_rejects_catalog_material(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "phong"}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "physical"}).plan()
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
                                "material": {"type": "lambert"},
                            }
                        ],
                    },
                }
            )

    def test_validate_rejects_bad_opacity(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "basic", "opacity": 1.5}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "basic", "opacity": -0.1}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "basic", "opacity": True}).plan()

    def test_soft2_shapes_and_soft3_camera_light_unchanged(self) -> None:
        """Soft 4 does not invent a second Graph API or change Soft 2/3."""
        self.assertTrue(callable(space))
        g = space("stage")
        self.assertIsInstance(g, Graph)
        params = inspect.signature(Graph.node).parameters
        self.assertIn("shape", params)
        self.assertEqual(params["shape"].default, "box")
        self.assertNotIn("kind", params)
        self.assertFalse(hasattr(Graph, "sphere"))
        self.assertFalse(hasattr(Graph, "box"))
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                self.assertEqual(plan["graph"]["nodes"][0]["kind"], "node")
                self.assertEqual(plan["graph"]["nodes"][0]["shape"], shape)
        plan = space("s").camera("eye").light("fill").node("a").plan()
        self.assertEqual(plan["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(plan["graph"]["nodes"][0]["camera"], "perspective")
        self.assertEqual(plan["graph"]["nodes"][1]["kind"], "light")
        self.assertEqual(plan["graph"]["nodes"][1]["light"], "ambient")
        self.assertEqual(plan["graph"]["nodes"][2]["kind"], "node")

    def test_frozen_graph_node_kwargs(self) -> None:
        """Frozen Soft 4 names: Graph.node(rotation=, scale=, material=)."""
        params = inspect.signature(Graph.node).parameters
        self.assertIn("rotation", params)
        self.assertIn("scale", params)
        self.assertIn("material", params)
        cam_params = inspect.signature(Graph.camera).parameters
        self.assertIn("rotation", cam_params)
        light_params = inspect.signature(Graph.light).parameters
        self.assertNotIn("rotation", light_params)
        self.assertNotIn("scale", light_params)
        self.assertNotIn("material", light_params)

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft4-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        hero = ops[0]["args"][0]["graph"]["nodes"][3]
        self.assertEqual(hero["rotation"], [0.1, 0.2, 0.3])
        self.assertEqual(hero["material"]["type"], "basic")
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))

    def test_peer_applies_transform_and_basic_material(self) -> None:
        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("MeshBasicMaterial", js)
        self.assertIn("MeshStandardMaterial", js)
        self.assertIn("rotation", js)
        self.assertIn("scale", js)
        self.assertIn("opacity", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("lookAt(", js)
        self.assertNotIn("MeshPhysicalMaterial", js)
        self.assertIn("PerspectiveCamera", js)
        self.assertIn("AmbientLight", js)
        self.assertIn("BoxGeometry", js)

    def test_features_stays_empty(self) -> None:
        """Soft 4 lives in core IR + Graph + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft4LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft4(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 4 transform + material {basic}."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 4", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("rotation", lowered, path)
            self.assertIn("scale", lowered, path)
            self.assertIn("material", lowered, path)
            self.assertIn("basic", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
            self.assertIn("Soft 5", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        self.assertNotIn(
            "Soft 4 transform/material (separate Soft)",
            ownership,
        )

    def test_start_here_soft4_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 4", text)
        self.assertIn("rotation", lowered)
        self.assertIn("scale", lowered)
        self.assertIn("material", lowered)
        self.assertIn("basic", lowered)
