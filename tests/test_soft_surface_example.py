"""Soft-surface example locks — public Graph leftover tour, Cap-gated apply.

The example composes Soft 2–5 leftovers on the day-1 spine. It does not
invent a second Graph API, mint Caps, or teach dual concurrent Peers.
Cap token stays server-side — absent from ops/Result.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from ux_space import (
    CapRequired,
    Graph,
    apply,
    space,
    to_result,
    validate_plan,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.soft_surface.plan import STAND_IN_CAP, soft_surface  # noqa: E402

PKG = ROOT / "ux_space"
EXAMPLE = ROOT / "examples" / "soft_surface"
SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})


def _nodes_by_id(plan: dict) -> dict:
    return {n["id"]: n for n in plan["graph"]["nodes"]}


class SoftSurfaceExampleTests(unittest.TestCase):
    def test_example_builds_valid_plan_ir(self) -> None:
        graph = soft_surface()
        self.assertIsInstance(graph, Graph)
        plan = validate_plan(graph.plan())
        self.assertEqual(plan["v"], "1")
        self.assertEqual(plan["kind"], "plan")
        self.assertEqual(plan["id"], "soft-surface")
        self.assertEqual(plan["graph"]["kind"], "graph")
        self.assertEqual(plan["graph"]["host"], "stage-3d")

    def test_example_composes_soft2_shapes(self) -> None:
        plan = validate_plan(soft_surface().plan())
        meshes = [n for n in plan["graph"]["nodes"] if n["kind"] == "node"]
        shapes = {n["shape"] for n in meshes}
        self.assertEqual(shapes, SOFT2_SHAPES)
        self.assertEqual({n["id"] for n in meshes}, SOFT2_SHAPES)

    def test_example_composes_soft3_camera_light(self) -> None:
        plan = validate_plan(soft_surface().plan())
        by_id = _nodes_by_id(plan)
        self.assertEqual(by_id["eye"]["kind"], "camera")
        self.assertEqual(by_id["eye"]["camera"], "perspective")
        self.assertEqual(by_id["fill"]["kind"], "light")
        self.assertEqual(by_id["fill"]["light"], "ambient")
        self.assertEqual(by_id["key"]["kind"], "light")
        self.assertEqual(by_id["key"]["light"], "directional")

    def test_example_composes_soft4_transform_and_material(self) -> None:
        plan = validate_plan(soft_surface().plan())
        by_id = _nodes_by_id(plan)
        box = by_id["box"]
        self.assertEqual(box["color"], "#6366f1")
        self.assertNotIn("material", box)
        self.assertEqual(box["rotation"], [0.25, 0.6, 0.05])
        self.assertEqual(box["scale"], 1.0)
        sphere = by_id["sphere"]
        self.assertEqual(sphere["color"], "#f59e0b")
        self.assertEqual(sphere["material"]["type"], "basic")
        self.assertEqual(sphere["material"]["color"], "#22c55e")
        self.assertEqual(sphere["material"]["opacity"], 0.85)
        cylinder = by_id["cylinder"]
        self.assertEqual(cylinder["material"]["type"], "basic")
        self.assertEqual(cylinder["scale"], [0.65, 1.15, 0.65])

    def test_apply_bridge_call_cap_absent_from_ops_and_result(self) -> None:
        token = STAND_IN_CAP
        ops = apply(soft_surface(), cap=token)
        result = to_result(ops)
        self.assertEqual(len(ops), 1)
        op = ops[0]
        self.assertEqual(op["op"], "bridge.call")
        self.assertEqual(op["method"], "apply")
        self.assertEqual(op["package"], "ux-space")
        self.assertEqual(op["id"], "stage-3d")
        self.assertEqual(op["args"][0]["id"], "soft-surface")
        self.assertNotIn("meta", op)
        self.assertNotIn("cap", op)
        dumped_ops = json.dumps(ops)
        dumped_result_ops = json.dumps(result["ops"])
        self.assertNotIn(token, dumped_ops)
        self.assertNotIn(token, dumped_result_ops)
        self.assertNotIn('"cap"', dumped_ops)
        self.assertTrue(result["ok"])

    def test_apply_requires_cap(self) -> None:
        with self.assertRaises(CapRequired):
            apply(soft_surface(), cap=None)

    def test_plan_script_runs(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        proc = subprocess.run(
            [sys.executable, str(EXAMPLE / "plan.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("bridge.call", proc.stdout)
        self.assertIn("apply", proc.stdout)
        self.assertIn("ux-space", proc.stdout)
        self.assertIn("False False", proc.stdout)
        self.assertNotIn(STAND_IN_CAP, proc.stdout)

    def test_example_uses_public_graph_not_a_second_api(self) -> None:
        self.assertIsInstance(soft_surface(), type(space("x").node("n")))
        plan_src = (EXAMPLE / "plan.py").read_text(encoding="utf-8")
        self.assertIn("from ux_space import", plan_src)
        self.assertIn("space(", plan_src)
        self.assertIn(".camera(", plan_src)
        self.assertIn(".light(", plan_src)
        self.assertIn(".node(", plan_src)
        self.assertIn("apply(", plan_src)
        self.assertNotIn("scene(", plan_src)
        self.assertNotIn("ux-scene", plan_src)
        self.assertNotIn("kind=", plan_src)

    def test_app_isolation_and_day1_peer_only(self) -> None:
        app = (EXAMPLE / "app.py").read_text(encoding="utf-8")
        self.assertIn("from ux_space.wire import", app)
        self.assertNotIn("from ux_channel", app)
        self.assertNotIn("import ux_channel", app)
        self.assertIn("ux_space.peers.threejs", app)
        self.assertNotIn("peers.canvas", app)
        self.assertNotIn('uxBridge.register("three"', app)
        self.assertNotIn('uxBridge.register("canvas"', app)
        self.assertNotIn("scene()", app)
        self.assertNotIn("ux-scene", app)

    def test_features_stays_empty(self) -> None:
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])

    def test_start_here_points_at_soft_surface(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("examples/soft_surface", text)
