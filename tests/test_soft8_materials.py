"""Soft 8 leftover locks — thin material set beyond Soft 4 {basic}.

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES,
Soft 3 camera/light, Soft 4 rotation/scale + material {basic}, Soft 5
canvas swap, Soft 6 pick/hit, Soft 7 orbit/pan/zoom stay locked.
Isolation + Cap-on-ops absence stay locked.

Frozen Graph fluency: ``.node(..., material={type: ...})`` — same Soft 4
kwarg, no second Graph API.
IR: ``MATERIALS`` locked thin set ``{basic, standard}``. Soft 4 ``color``
/ ``opacity`` KEEP. Soft 8 optional ``metalness`` / ``roughness`` (0..1)
belong to ``standard``. Additive v1 — keys never reused; unknown fields
ignored.
Peer ``peers/threejs`` maps ``standard`` → MeshStandardMaterial.
``peers/canvas`` swap-proof honors color/opacity; ``standard`` degrades
as basic (2D fill).

HOLD Soft 9 loaders, Soft 10 primitives, R3F, materials catalog
(phong/physical/lambert/...), Cap-on-ops, zero-Peer, renaming motion,
dual concurrent Peers, sixth Cap Host, generic pointer stack.
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
    PlanError,
    apply,
    orbit,
    pick,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import CAMERAS, LIGHTS, MATERIALS, SHAPES
from ux_space.peers.canvas import adapter_path as canvas_adapter_path
from ux_space.peers.threejs import adapter_path as threejs_adapter_path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
SOFT3_CAMERAS = frozenset({"perspective"})
SOFT3_LIGHTS = frozenset({"ambient", "directional"})
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
        .camera(
            "eye",
            camera="perspective",
            position=(0, 0.35, 4.2),
            rotation=(0, 0.1, 0),
            orbit={"azimuth": 0.4, "polar": 1.2},
            pan={"x": 0.1, "y": 0.2},
            zoom=5.0,
        )
        .light("fill", light="ambient", color="#ffffff")
        .light("key", light="directional", position=(3, 4, 5))
        .node(
            "hero",
            shape="box",
            color="#6366f1",
            rotation=(0.1, 0.2, 0.3),
            scale=1.5,
            material={
                "type": "standard",
                "color": "#22c55e",
                "opacity": 0.8,
                "metalness": 0.2,
                "roughness": 0.55,
            },
            pickable=True,
        )
    )


class Soft8MaterialsTests(unittest.TestCase):
    def test_locked_thin_set(self) -> None:
        self.assertEqual(SHAPES, SOFT2_SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertIn("basic", MATERIALS)
        self.assertIn("standard", MATERIALS)
        self.assertNotIn("phong", MATERIALS)
        self.assertNotIn("physical", MATERIALS)
        self.assertNotIn("lambert", MATERIALS)
        self.assertNotIn("toon", MATERIALS)
        self.assertNotIn("torus", SHAPES)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)

    def test_validate_accepts_standard_material(self) -> None:
        out = validate_plan(_mixed().plan())
        hero = out["graph"]["nodes"][3]
        self.assertEqual(hero["kind"], "node")
        self.assertEqual(hero["material"]["type"], "standard")
        self.assertEqual(hero["material"]["color"], "#22c55e")
        self.assertEqual(hero["material"]["opacity"], 0.8)
        self.assertEqual(hero["material"]["metalness"], 0.2)
        self.assertEqual(hero["material"]["roughness"], 0.55)
        self.assertEqual(hero["rotation"], [0.1, 0.2, 0.3])
        self.assertIs(hero["pickable"], True)

    def test_soft4_basic_still_works(self) -> None:
        """Soft 4 leftover KEEP — basic color/opacity + material.color wins."""
        plan = (
            space("s")
            .node(
                "a",
                color="#111111",
                material={"type": "basic", "color": "#eeeeee", "opacity": 0.5},
            )
            .plan()
        )
        node = plan["graph"]["nodes"][0]
        self.assertEqual(node["color"], "#111111")
        self.assertEqual(node["material"]["type"], "basic")
        self.assertEqual(node["material"]["color"], "#eeeeee")
        self.assertEqual(node["material"]["opacity"], 0.5)
        self.assertNotIn("metalness", node["material"])
        self.assertNotIn("roughness", node["material"])

    def test_standard_absent_fields_stay_optional(self) -> None:
        plan = space("s").node("a", material={"type": "standard"}).plan()
        mat = plan["graph"]["nodes"][0]["material"]
        self.assertEqual(mat["type"], "standard")
        self.assertNotIn("color", mat)
        self.assertNotIn("opacity", mat)
        self.assertNotIn("metalness", mat)
        self.assertNotIn("roughness", mat)

    def test_unknown_material_fields_still_kept(self) -> None:
        plan = _mixed().plan()
        plan["graph"]["nodes"][3]["material"]["hint"] = "keep"
        out = validate_plan(plan)
        self.assertEqual(out["graph"]["nodes"][3]["material"]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][3]["material"]["type"], "standard")

    def test_validate_rejects_catalog_material(self) -> None:
        for catalog in ("phong", "physical", "lambert", "toon"):
            with self.subTest(catalog=catalog):
                with self.assertRaises(PlanError):
                    space("s").node("a", material={"type": catalog}).plan()

    def test_validate_rejects_bad_metalness_roughness(self) -> None:
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "metalness": 1.5}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "metalness": -0.1}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "metalness": True}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "roughness": 2}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "roughness": True}).plan()

    def test_frozen_graph_node_material_kwarg(self) -> None:
        """Soft 8 reuses Soft 4 ``material=`` — no second Graph API."""
        params = inspect.signature(Graph.node).parameters
        self.assertIn("material", params)
        self.assertIn("rotation", params)
        self.assertIn("scale", params)
        self.assertIn("pickable", params)
        self.assertNotIn("kind", params)
        self.assertNotIn("metalness", params)
        self.assertNotIn("roughness", params)
        self.assertFalse(hasattr(Graph, "standard"))
        self.assertFalse(hasattr(Graph, "material"))
        self.assertFalse(hasattr(Graph, "phong"))
        light_params = inspect.signature(Graph.light).parameters
        cam_params = inspect.signature(Graph.camera).parameters
        self.assertNotIn("material", light_params)
        self.assertNotIn("material", cam_params)

    def test_soft1_to_soft7_spine_unchanged(self) -> None:
        self.assertTrue(callable(space))
        self.assertTrue(callable(apply))
        self.assertTrue(callable(pick))
        self.assertTrue(callable(orbit))
        self.assertIsInstance(space("stage"), Graph)
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                self.assertEqual(plan["graph"]["nodes"][0]["kind"], "node")
                self.assertEqual(plan["graph"]["nodes"][0]["shape"], shape)
        plan = (
            space("s")
            .camera("eye", orbit={"azimuth": 0.1}, pan={"x": 0.0}, zoom=4.0)
            .light("fill")
            .node("a", pickable=True, material={"type": "basic", "opacity": 1})
            .plan()
        )
        self.assertEqual(plan["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(plan["graph"]["nodes"][0]["orbit"]["azimuth"], 0.1)
        self.assertEqual(plan["graph"]["nodes"][1]["kind"], "light")
        self.assertEqual(plan["graph"]["nodes"][2]["kind"], "node")
        self.assertIs(plan["graph"]["nodes"][2]["pickable"], True)
        self.assertEqual(plan["graph"]["nodes"][2]["material"]["type"], "basic")
        hit = pick({"node_id": "a"}, host="h", cap="tok")
        self.assertEqual(hit[0]["method"], "pick")
        cam = orbit({"azimuth": 0.2}, host="h", cap="tok")
        self.assertEqual(cam[0]["method"], "orbit")

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft8-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        hero = ops[0]["args"][0]["graph"]["nodes"][3]
        self.assertEqual(hero["material"]["type"], "standard")
        self.assertEqual(hero["material"]["metalness"], 0.2)
        self.assertEqual(hero["material"]["roughness"], 0.55)
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        dumped_ops = json.dumps(ops)
        dumped_result_ops = json.dumps(result["ops"])
        self.assertNotIn(token, dumped_ops)
        self.assertNotIn(token, dumped_result_ops)
        self.assertNotIn('"cap"', dumped_ops)
        self.assertTrue(result["ok"])

    def test_threejs_peer_maps_standard_thinly(self) -> None:
        js = Path(threejs_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("MeshBasicMaterial", js)
        self.assertIn("MeshStandardMaterial", js)
        self.assertIn("metalness", js)
        self.assertIn("roughness", js)
        self.assertIn('"standard"', js)
        self.assertNotIn("MeshPhysicalMaterial", js)
        self.assertNotIn("MeshPhongMaterial", js)
        self.assertNotIn("MeshLambertMaterial", js)
        self.assertNotIn("MeshToonMaterial", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("useFrame", js)

    def test_canvas_peer_honors_color_opacity_and_degrades_standard(self) -> None:
        js = Path(canvas_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("material.color", js)
        self.assertIn("material.opacity", js)
        self.assertIn("standard", js)
        self.assertIn('getContext("2d")', js)
        self.assertNotIn("MeshStandardMaterial", js)
        self.assertNotIn("MeshPhysicalMaterial", js)
        self.assertNotIn("MeshPhongMaterial", js)
        self.assertNotIn("Raycaster", js)
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("global.THREE", js)
        self.assertNotIn("GLTFLoader", js)

    def test_peer_contract_soft8(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("pick", PEER["methods"])
        self.assertIn("orbit", PEER["methods"])
        self.assertIn("soft4", PEER)
        self.assertIn("soft7", PEER)
        self.assertIn("soft8", PEER)
        self.assertIn("standard", PEER["soft8"].lower())
        self.assertIn("basic", PEER["soft8"].lower())
        self.assertIn("materials catalog", PEER["holds"])
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 8 leftover", laws)
        self.assertIn("Soft 7 leftover", laws)
        self.assertIn("standard", laws.lower())

    def test_features_stays_empty(self) -> None:
        """Soft 8 lives in core IR + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft8LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft8(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 8 thin {basic, standard}."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 8", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("standard", lowered, path)
            self.assertIn("basic", lowered, path)
            self.assertIn("material", lowered, path)
            self.assertIn("metalness", lowered, path)
            self.assertIn("roughness", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 13. Soft 8 leftover")[1]
        hold = leftover.lower()
        self.assertIn("soft 9", hold)
        self.assertIn("soft 10", hold)
        self.assertIn("r3f", hold)
        self.assertIn("materials catalog", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)

    def test_start_here_soft8_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 8", text)
        self.assertIn("standard", lowered)
        self.assertIn("material", lowered)
        self.assertTrue(
            "basic" in lowered,
            "START_HERE must leftover-teach Soft 8 thin materials beyond basic",
        )
