"""Soft 3 leftover locks — camera/light node kinds, not a materials catalog.

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES stay locked.
Isolation + Cap-on-ops absence stay locked. Frozen Graph names: camera / light.
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
from ux_space.core._ir import CAMERAS, LIGHTS, SHAPES
from ux_space.peers.threejs import adapter_path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
SOFT3_CAMERAS = frozenset({"perspective"})
SOFT3_LIGHTS = frozenset({"ambient", "directional"})
TEACHING = (
    ROOT / "OWNERSHIP.md",
    ROOT / "CHANGELOG.md",
    ROOT / "START_HERE.md",
)


def _mixed() -> Graph:
    return (
        space("stage")
        .host("stage-3d")
        .camera("eye", camera="perspective", position=(0, 0.35, 4.2))
        .light("fill", light="ambient", color="#ffffff")
        .light("key", light="directional", position=(3, 4, 5))
        .node("hero", shape="box", color="#6366f1")
    )


class Soft3CameraLightTests(unittest.TestCase):
    def test_locked_sets(self) -> None:
        self.assertEqual(SHAPES, SOFT2_SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)
        self.assertNotIn("spot", LIGHTS)

    def test_validate_accepts_camera_and_lights(self) -> None:
        plan = _mixed().plan()
        out = validate_plan(plan)
        kinds = [n["kind"] for n in out["graph"]["nodes"]]
        self.assertEqual(kinds, ["camera", "light", "light", "node"])
        self.assertEqual(out["graph"]["nodes"][0]["camera"], "perspective")
        self.assertEqual(out["graph"]["nodes"][1]["light"], "ambient")
        self.assertEqual(out["graph"]["nodes"][2]["light"], "directional")
        self.assertEqual(out["graph"]["nodes"][3]["shape"], "box")

    def test_validate_accepts_ir_camera_light_nodes(self) -> None:
        out = validate_plan(
            {
                "v": "1",
                "kind": "plan",
                "id": "stage",
                "graph": {
                    "kind": "graph",
                    "nodes": [
                        {"kind": "camera", "id": "eye", "camera": "perspective"},
                        {"kind": "light", "id": "fill", "light": "ambient"},
                        {"kind": "light", "id": "key", "light": "directional"},
                        {"kind": "node", "id": "hero", "shape": "sphere"},
                    ],
                },
            }
        )
        self.assertEqual(out["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(out["graph"]["nodes"][3]["shape"], "sphere")

    def test_validate_rejects_unknown_camera_and_light(self) -> None:
        with self.assertRaises(PlanError):
            validate_plan(
                {
                    "v": "1",
                    "kind": "plan",
                    "id": "x",
                    "graph": {
                        "kind": "graph",
                        "nodes": [{"kind": "camera", "id": "c", "camera": "orthographic"}],
                    },
                }
            )
        with self.assertRaises(PlanError):
            validate_plan(
                {
                    "v": "1",
                    "kind": "plan",
                    "id": "x",
                    "graph": {
                        "kind": "graph",
                        "nodes": [{"kind": "light", "id": "p", "light": "point"}],
                    },
                }
            )
        with self.assertRaises(PlanError):
            space("stage").camera("eye", camera="orthographic").plan()
        with self.assertRaises(PlanError):
            space("stage").light("spot", light="spot").plan()

    def test_soft2_shapes_unchanged_via_node(self) -> None:
        """Soft 3 does not invent a second Graph API or change Soft 2 node()."""
        self.assertTrue(callable(space))
        g = space("stage")
        self.assertIsInstance(g, Graph)
        params = inspect.signature(Graph.node).parameters
        self.assertIn("shape", params)
        self.assertEqual(params["shape"].default, "box")
        self.assertFalse(hasattr(Graph, "sphere"))
        self.assertFalse(hasattr(Graph, "plane"))
        self.assertFalse(hasattr(Graph, "cylinder"))
        self.assertFalse(hasattr(Graph, "box"))
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                self.assertEqual(plan["graph"]["nodes"][0]["kind"], "node")
                self.assertEqual(plan["graph"]["nodes"][0]["shape"], shape)

    def test_frozen_graph_names_camera_light(self) -> None:
        """Frozen Soft 3 builders: Graph.camera / Graph.light (not node kind=)."""
        self.assertTrue(callable(Graph.camera))
        self.assertTrue(callable(Graph.light))
        cam_params = inspect.signature(Graph.camera).parameters
        light_params = inspect.signature(Graph.light).parameters
        self.assertIn("camera", cam_params)
        self.assertEqual(cam_params["camera"].default, "perspective")
        self.assertIn("light", light_params)
        self.assertEqual(light_params["light"].default, "ambient")
        plan = space("s").camera("eye").light("fill").node("a").plan()
        self.assertEqual(plan["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(plan["graph"]["nodes"][1]["kind"], "light")
        self.assertEqual(plan["graph"]["nodes"][2]["kind"], "node")

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft3-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        kinds = [n["kind"] for n in ops[0]["args"][0]["graph"]["nodes"]]
        self.assertEqual(kinds, ["camera", "light", "light", "node"])
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))

    def test_peer_applies_camera_lights_and_meshes(self) -> None:
        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("PerspectiveCamera", js)
        self.assertIn("AmbientLight", js)
        self.assertIn("DirectionalLight", js)
        self.assertIn('kind === "camera"', js)
        self.assertIn('kind === "light"', js)
        self.assertIn('"box"', js)
        self.assertIn("BoxGeometry", js)
        self.assertNotIn("OrthographicCamera", js)
        self.assertNotIn("PointLight", js)
        self.assertNotIn("SpotLight", js)

    def test_features_stays_empty(self) -> None:
        """Soft 3 lives in core IR + Graph + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft3LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft3(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 3 camera/light locked set."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 3", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("perspective", lowered, path)
            self.assertIn("ambient", lowered, path)
            self.assertIn("directional", lowered, path)
            self.assertIn(".camera", lowered, path)
            self.assertIn(".light", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)

    def test_start_here_soft3_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 3", text)
        self.assertIn("camera", lowered)
        self.assertIn("light", lowered)
        self.assertIn("perspective", lowered)
        self.assertTrue(
            "ambient" in lowered and "directional" in lowered,
            "START_HERE must leftover-teach Soft 3 locked lights in one line",
        )
