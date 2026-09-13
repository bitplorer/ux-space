"""Soft 5 leftover locks — Peer-swap proof (canvas adapter, not dual-product).

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES, Soft 3
camera/light, Soft 4 rotation/scale + material {basic} stay locked.
Isolation + Cap-on-ops absence stay locked. Day-1 Peer remains threejs.
HOLD R3F, materials catalog, Cap-on-ops, zero-Peer, renaming motion,
dual concurrent Peers as taught product, sixth Cap Host.
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
    Graph,
    apply,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import CAMERAS, LIGHTS, MATERIALS, SHAPES
from ux_space.peers.threejs import ADAPTER_JS as THREE_ADAPTER_JS
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
    ROOT / "ux_space" / "peers" / "README.md",
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


class Soft5PeerSwapTests(unittest.TestCase):
    def test_canvas_adapter_exists_and_registers_ux_space(self) -> None:
        """Canvas Peer exists and registers the product as ux-space, not canvas/three."""
        from ux_space.peers.canvas import ADAPTER_JS, adapter_path

        path = Path(adapter_path())
        self.assertTrue(path.is_file(), path)
        self.assertTrue(ADAPTER_JS.endswith(".js"))
        self.assertEqual(path.name, "ux-space.js")
        js = path.read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn("ux-scene", js)

    def test_canvas_peer_has_no_threejs_dependency(self) -> None:
        from ux_space.peers.canvas import adapter_path

        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("cdn.jsdelivr.net/npm/three", js)
        self.assertNotIn("global.THREE", js)
        self.assertNotIn("THREE.", js)
        self.assertIn('getContext("2d")', js)
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                self.assertIn(f'"{shape}"', js)

    def test_canvas_peer_honors_soft4_fields_and_noops_camera_light(self) -> None:
        from ux_space.peers.canvas import adapter_path

        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn("position", js)
        self.assertIn("rotation", js)
        self.assertIn("scale", js)
        self.assertIn("material.color", js)
        self.assertIn("|| node.color", js)
        self.assertIn("opacity", js)
        self.assertIn("basic", js)
        # 2D proof: camera/light must not invent a second camera API.
        self.assertNotIn("PerspectiveCamera", js)
        self.assertNotIn("OrthographicCamera", js)
        self.assertNotIn("AmbientLight", js)
        self.assertNotIn("lookAt(", js)
        self.assertNotIn("OrbitControls", js)

    def test_canvas_peer_contract_methods(self) -> None:
        from ux_space.peers.canvas import adapter_path

        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn("apply:", js)
        self.assertIn("update:", js)
        self.assertIn("destroy:", js)
        self.assertIn("call:", js)
        self.assertIn("innerHTML", js)

    def test_threejs_day1_adapter_still_registers_ux_space(self) -> None:
        path = Path(threejs_adapter_path())
        self.assertTrue(path.is_file(), path)
        self.assertTrue(THREE_ADAPTER_JS.endswith(".js"))
        js = path.read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("three@0.160.0", js)
        self.assertIn("BoxGeometry", js)
        self.assertIn("MeshBasicMaterial", js)

    def test_peer_contract_swap_path_locked_day1_threejs(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertEqual(PEER["identity"], "adapter")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("update", PEER["methods"])
        self.assertIn("destroy", PEER["methods"])
        self.assertIn("bridge.call", PEER["ops"])
        self.assertIn("soft4", PEER)
        self.assertIn("soft5", PEER)
        self.assertIn("rotation", PEER["soft4"])
        self.assertIn("basic", PEER["soft4"])
        self.assertIn("canvas", PEER["soft5"].lower())
        self.assertIn("threejs", PEER["soft5"].lower())
        swap = PEER["swap"].lower()
        self.assertIn("ux-space", swap)
        self.assertIn("graph", swap)
        self.assertIn("apply()", swap)
        self.assertNotIn("three", PEER["holds"])
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 5 leftover", laws)
        self.assertNotIn("Soft 5 Peer-swap", laws)

    def test_graph_apply_soft24_locks_unchanged(self) -> None:
        """Soft 5 does not change Graph, Plan IR, or apply()."""
        self.assertTrue(callable(space))
        self.assertIsInstance(space("stage"), Graph)
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertTrue(SOFT4_MATERIALS <= MATERIALS)
        params = inspect.signature(Graph.node).parameters
        self.assertIn("shape", params)
        self.assertIn("rotation", params)
        self.assertIn("scale", params)
        self.assertIn("material", params)
        self.assertNotIn("kind", params)
        self.assertFalse(hasattr(Graph, "sphere"))
        self.assertFalse(hasattr(Graph, "box"))
        token = "soft5-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        hero = ops[0]["args"][0]["graph"]["nodes"][3]
        self.assertEqual(hero["shape"], "box")
        self.assertEqual(hero["rotation"], [0.1, 0.2, 0.3])
        self.assertEqual(hero["material"]["type"], "basic")
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))
        out = validate_plan(_mixed().plan())
        self.assertEqual(out["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(out["graph"]["nodes"][3]["material"]["opacity"], 0.8)

    def test_features_stays_empty(self) -> None:
        """Soft 5 lives in peers/ + contract — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])

    def test_canvas_packaging_mirrors_threejs(self) -> None:
        from ux_space.peers.canvas import ADAPTER_JS, adapter_path
        from ux_space.peers.threejs import ADAPTER_JS as THREE_JS

        self.assertEqual(ADAPTER_JS, THREE_JS)
        self.assertEqual(ADAPTER_JS, "ux-space.js")
        self.assertTrue(Path(adapter_path()).is_file())
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn("peers/threejs/*.js", pyproject)
        self.assertIn("peers/canvas/*.js", pyproject)
        readme = (PKG / "peers" / "canvas" / "README.md").read_text(encoding="utf-8")
        self.assertIn("adapter_path()", readme)
        self.assertIn('uxBridge.register("ux-space"', readme)
        self.assertIn("day-1", readme.lower())


class Soft5LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft5(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 5 swap path; day-1 threejs."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 5", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("canvas", lowered, path)
            self.assertIn("threejs", lowered, path)
            self.assertIn("ux-space", lowered, path)
            self.assertIn("swap", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
            self.assertIn("dual", lowered, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 10. Soft 5 leftover")[1]
        hold = leftover.lower()
        self.assertIn("r3f", hold)
        self.assertIn("materials catalog", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)
        self.assertNotIn("soft 5 peer-swap", leftover.lower())

    def test_start_here_soft5_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 5", text)
        self.assertIn("canvas", lowered)
        self.assertIn("threejs", lowered)
        self.assertTrue(
            "swap" in lowered,
            "START_HERE must leftover-teach Soft 5 swap in one line",
        )

    def test_peers_readme_leftover_teach_soft5_swap(self) -> None:
        text = (ROOT / "ux_space" / "peers" / "README.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 5", text)
        self.assertIn("leftover", lowered)
        self.assertIn("canvas", lowered)
        self.assertIn("threejs", lowered)
        self.assertIn('uxBridge.register("ux-space"', text)
        self.assertNotIn("Soft 5 Peer-swap", text)
        self.assertIn("HOLD", text)
        self.assertIn("dual", lowered)
