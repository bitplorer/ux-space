"""Soft 2 leftover locks — locked SHAPES pack, not the three.js catalog.

Graph / space() / Cap-gated apply stay Soft day-1. Isolation + Cap-on-ops
absence stay locked. Teaching surfaces leftover-teach the catalog HOLD.
"""

from __future__ import annotations

import inspect
import json
import unittest
from pathlib import Path

from ux_space import (
    Graph,
    apply,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import SHAPES
from ux_space.peers.threejs import adapter_path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
SOFT10_SHAPES = frozenset({"box", "sphere", "plane", "cylinder", "cone", "torus"})
TEACHING = (
    ROOT / "OWNERSHIP.md",
    ROOT / "CHANGELOG.md",
    ROOT / "START_HERE.md",
)
GEOMETRY = {
    "box": "BoxGeometry",
    "sphere": "SphereGeometry",
    "plane": "PlaneGeometry",
    "cylinder": "CylinderGeometry",
}


class Soft2ShapesTests(unittest.TestCase):
    def test_shapes_locked_set(self) -> None:
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertNotIn("icosahedron", SHAPES)
        self.assertNotIn("torusKnot", SHAPES)

    def test_validate_plan_accepts_soft2_shapes(self) -> None:
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                out = validate_plan(
                    {
                        "v": "1",
                        "kind": "plan",
                        "id": "stage",
                        "graph": {
                            "kind": "graph",
                            "nodes": [{"kind": "node", "id": "n", "shape": shape}],
                        },
                    }
                )
                self.assertEqual(out["graph"]["nodes"][0]["shape"], shape)

    def test_validate_plan_rejects_unknown_shape(self) -> None:
        with self.assertRaises(ValueError):
            validate_plan(
                {
                    "v": "1",
                    "kind": "plan",
                    "id": "x",
                    "graph": {
                        "kind": "graph",
                        "nodes": [{"kind": "node", "id": "a", "shape": "torusKnot"}],
                    },
                }
            )

    def test_graph_api_unchanged(self) -> None:
        """Soft 2 does not invent a second Graph API."""
        self.assertTrue(callable(space))
        g = space("stage")
        self.assertIsInstance(g, Graph)
        self.assertTrue(callable(g.host))
        self.assertTrue(callable(g.node))
        self.assertTrue(callable(g.plan))
        self.assertTrue(callable(g.apply))
        params = inspect.signature(Graph.node).parameters
        self.assertIn("shape", params)
        self.assertEqual(params["shape"].default, "box")
        self.assertFalse(hasattr(Graph, "sphere"))
        self.assertFalse(hasattr(Graph, "plane"))
        self.assertFalse(hasattr(Graph, "cylinder"))
        self.assertFalse(hasattr(Graph, "box"))

    def test_apply_shape_unchanged_no_cap_on_ops(self) -> None:
        token = "soft2-cap-MUST-NOT-SHIP"
        graph = space("stage").host("stage-3d").node("hero", shape="sphere")
        ops = apply(graph, cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        self.assertEqual(ops[0]["args"][0]["graph"]["nodes"][0]["shape"], "sphere")
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))

    def test_peer_thin_geometry_map(self) -> None:
        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        for shape, ctor in GEOMETRY.items():
            with self.subTest(shape=shape):
                self.assertIn(f'"{shape}"', js)
                self.assertIn(ctor, js)
        self.assertIn("ConeGeometry", js)
        self.assertIn("TorusGeometry", js)
        self.assertNotIn("IcosahedronGeometry", js)
        self.assertNotIn("TorusKnotGeometry", js)

    def test_features_stays_empty(self) -> None:
        """Soft 2 lives in core SHAPES + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft2LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft2(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 2 as locked set, not catalog."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 2", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("sphere", lowered, path)
            self.assertIn("plane", lowered, path)
            self.assertIn("cylinder", lowered, path)
            self.assertIn("not the full three.js catalog", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)

    def test_start_here_soft2_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 2", text)
        self.assertTrue(
            "locked shapes" in lowered or "locked set" in lowered,
            "START_HERE must leftover-teach Soft 2 locked shapes in one line",
        )
        self.assertIn("sphere", lowered)
        self.assertIn("not the", lowered.lower())
        self.assertIn("catalog", lowered)
