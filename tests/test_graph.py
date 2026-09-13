"""Graph / space() API — one graph, not motion scene()."""

from __future__ import annotations

import unittest

from ux_space import Graph, space


class GraphTests(unittest.TestCase):
    def test_space_returns_graph(self) -> None:
        g = space("stage")
        self.assertIsInstance(g, Graph)
        self.assertEqual(g._id, "stage")

    def test_fluent_node_and_host(self) -> None:
        g = space("stage").host("stage-3d").node("hero", shape="box", color="#6366f1")
        plan = g.plan()
        self.assertEqual(plan["graph"]["host"], "stage-3d")
        self.assertEqual(len(plan["graph"]["nodes"]), 1)
        self.assertEqual(plan["graph"]["nodes"][0]["id"], "hero")

    def test_apply_on_graph(self) -> None:
        result = space("stage").host("h").node("n").apply(cap="tok")
        self.assertTrue(result["ok"])
        self.assertEqual(result["ops"][0]["method"], "apply")
        self.assertEqual(result["ops"][0]["id"], "h")

    def test_empty_graph_fails(self) -> None:
        with self.assertRaises(ValueError):
            space("empty").plan()

    def test_default_id(self) -> None:
        g = space()
        self.assertTrue(g._id.startswith("space-"))

    def test_repr(self) -> None:
        text = repr(space("stage").node("a"))
        self.assertIn("Graph", text)
        self.assertIn("stage", text)

    def test_no_scene_alias(self) -> None:
        import ux_space

        self.assertFalse(hasattr(ux_space, "scene"))
        self.assertFalse(hasattr(ux_space, "Scene"))
        self.assertNotIn("scene", ux_space.__all__)
        self.assertNotIn("Scene", ux_space.__all__)
