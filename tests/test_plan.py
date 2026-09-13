"""Plan IR validate — additive JSON, fail closed on required fields."""

from __future__ import annotations

import unittest

from ux_space import IR_VERSION, PlanError, space, validate_plan


def _minimal() -> dict:
    return space("stage").node("hero", shape="box", color="#6366f1").plan()


class PlanTests(unittest.TestCase):
    def test_valid_plan(self) -> None:
        plan = _minimal()
        out = validate_plan(plan)
        self.assertEqual(out["v"], IR_VERSION)
        self.assertEqual(out["kind"], "plan")
        self.assertEqual(out["id"], "stage")
        self.assertEqual(out["graph"]["kind"], "graph")
        self.assertEqual(out["graph"]["nodes"][0]["id"], "hero")
        self.assertEqual(out["graph"]["nodes"][0]["shape"], "box")
        self.assertEqual(out["graph"]["nodes"][0]["color"], "#6366f1")

    def test_unknown_fields_kept(self) -> None:
        plan = _minimal()
        plan["future"] = {"ok": True}
        plan["graph"]["nodes"][0]["spin"] = 1
        out = validate_plan(plan)
        self.assertEqual(out["future"], {"ok": True})
        self.assertEqual(out["graph"]["nodes"][0]["spin"], 1)

    def test_missing_graph(self) -> None:
        with self.assertRaises(PlanError):
            validate_plan({"v": "1", "kind": "plan", "id": "x"})

    def test_empty_nodes(self) -> None:
        with self.assertRaises(PlanError):
            validate_plan(
                {"v": "1", "kind": "plan", "id": "x", "graph": {"kind": "graph", "nodes": []}}
            )

    def test_soft2_locked_shapes_accepted(self) -> None:
        """Soft 2 SHAPES: box, sphere, plane, cylinder. Graph API unchanged."""
        for shape in ("box", "sphere", "plane", "cylinder"):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                out = validate_plan(plan)
                self.assertEqual(out["graph"]["nodes"][0]["shape"], shape)

    def test_unknown_shape_fails(self) -> None:
        with self.assertRaises(PlanError):
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
        with self.assertRaises(PlanError):
            space("stage").node("ghost", shape="icosahedron").plan()

    def test_wrong_version(self) -> None:
        plan = _minimal()
        plan["v"] = "2"
        with self.assertRaises(PlanError):
            validate_plan(plan)

    def test_position(self) -> None:
        plan = space("s").node("a", position=(1, 2, 3)).plan()
        self.assertEqual(plan["graph"]["nodes"][0]["position"], [1.0, 2.0, 3.0])

    def test_bad_position(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", position=(1, 2)).plan()
