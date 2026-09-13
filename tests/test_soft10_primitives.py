"""Soft 10 leftover locks — additive mesh primitives beyond Soft 2 SHAPES.

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES names
KEEP (``box`` / ``sphere`` / ``plane`` / ``cylinder``). Soft 3
camera/light, Soft 4 rotation/scale + material {basic}, Soft 5 canvas
swap, Soft 6 pick/hit, Soft 7 orbit/pan/zoom, Soft 8 material.type
{basic, standard}, Soft 9 {gltf, texture} stay locked.
Isolation + Cap-on-ops absence stay locked.

Frozen Graph fluency: ``.node(..., shape=...)`` — Soft 2 fluency, no
second Graph API (no ``.cone()`` / ``.torus()``).
IR: ``SHAPES`` locked thin set
``{box, sphere, plane, cylinder, cone, torus}``. Additive v1 — keys
never reused; unknown fields ignored.
Peer ``peers/threejs`` maps ``cone`` → ConeGeometry and ``torus`` →
TorusGeometry. ``peers/canvas`` swap-proof degrades Soft 10 as 2D
fill without breaking Soft 1–9.

HOLD full geometry catalog, materials catalog beyond Soft 8, R3F,
Cap-on-ops, zero-Peer, renaming motion, dual concurrent Peers, sixth
Cap Host, generic pointer stack, useFrame, OrbitControls dump,
GLTFLoader dump as public API.
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
    orbit,
    pick,
    space,
    to_result,
    validate_plan,
)
from ux_space.core._ir import CAMERAS, LIGHTS, LOADERS, MATERIALS, NODE_KINDS, SHAPES
from ux_space.peers.canvas import adapter_path as canvas_adapter_path
from ux_space.peers.threejs import adapter_path as threejs_adapter_path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

SOFT2_SHAPES = frozenset({"box", "sphere", "plane", "cylinder"})
SOFT10_ADDITIVE = frozenset({"cone", "torus"})
SOFT10_SHAPES = SOFT2_SHAPES | SOFT10_ADDITIVE
SOFT3_CAMERAS = frozenset({"perspective"})
SOFT3_LIGHTS = frozenset({"ambient", "directional"})
SOFT8_MATERIALS = frozenset({"basic", "standard"})
SOFT9_LOADERS = frozenset({"gltf", "texture"})
SOFT9_NODE_KINDS = frozenset({"node", "camera", "light", "gltf", "texture"})
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
    "cone": "ConeGeometry",
    "torus": "TorusGeometry",
}
CATALOG = (
    "icosahedron",
    "dodecahedron",
    "octahedron",
    "tetrahedron",
    "capsule",
    "ring",
    "torusKnot",
    "lathe",
    "extrude",
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
        .texture("albedo", src="albedo.png")
        .gltf(
            "prop",
            src="prop.gltf",
            position=(1.2, 0.0, -0.4),
            rotation=(0.0, 0.3, 0.0),
            scale=0.5,
        )
        .node(
            "hero",
            shape="cone",
            color="#6366f1",
            rotation=(0.1, 0.2, 0.3),
            scale=1.5,
            material={
                "type": "standard",
                "color": "#22c55e",
                "opacity": 0.8,
                "metalness": 0.2,
                "roughness": 0.55,
                "map": "albedo",
            },
            pickable=True,
        )
        .node("ring", shape="torus", color="#f59e0b", position=(1.2, 0.0, 0.4))
    )


class Soft10PrimitivesTests(unittest.TestCase):
    def test_locked_thin_additive_set(self) -> None:
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertTrue(SOFT10_ADDITIVE <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertEqual(LOADERS, SOFT9_LOADERS)
        self.assertEqual(NODE_KINDS, SOFT9_NODE_KINDS)
        self.assertIn("cone", SHAPES)
        self.assertIn("torus", SHAPES)
        self.assertNotIn("phong", MATERIALS)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)
        self.assertNotIn("fbx", LOADERS)
        for catalog in CATALOG:
            with self.subTest(catalog=catalog):
                self.assertNotIn(catalog, SHAPES)

    def test_validate_accepts_soft2_and_soft10_shapes(self) -> None:
        for shape in sorted(SOFT10_SHAPES):
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

    def test_validate_accepts_mixed_graph(self) -> None:
        out = validate_plan(_mixed().plan())
        kinds = [n["kind"] for n in out["graph"]["nodes"]]
        self.assertEqual(
            kinds, ["camera", "light", "light", "texture", "gltf", "node", "node"]
        )
        hero = out["graph"]["nodes"][5]
        self.assertEqual(hero["shape"], "cone")
        self.assertEqual(hero["material"]["type"], "standard")
        self.assertEqual(hero["material"]["map"], "albedo")
        self.assertIs(hero["pickable"], True)
        ring = out["graph"]["nodes"][6]
        self.assertEqual(ring["shape"], "torus")
        self.assertEqual(ring["color"], "#f59e0b")

    def test_unknown_fields_kept(self) -> None:
        plan = _mixed().plan()
        plan["graph"]["nodes"][5]["hint"] = "keep"
        plan["graph"]["nodes"][6]["hint"] = "keep"
        out = validate_plan(plan)
        self.assertEqual(out["graph"]["nodes"][5]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][6]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][5]["shape"], "cone")
        self.assertEqual(out["graph"]["nodes"][6]["shape"], "torus")

    def test_validate_rejects_catalog_shapes(self) -> None:
        for catalog in CATALOG:
            with self.subTest(catalog=catalog):
                with self.assertRaises(PlanError):
                    space("s").node("a", shape=catalog).plan()

    def test_frozen_graph_node_shape_kwarg(self) -> None:
        """Soft 10 reuses Soft 2 ``shape=`` — no second Graph API."""
        params = inspect.signature(Graph.node).parameters
        self.assertIn("shape", params)
        self.assertEqual(params["shape"].default, "box")
        self.assertIn("material", params)
        self.assertIn("rotation", params)
        self.assertIn("scale", params)
        self.assertIn("pickable", params)
        self.assertNotIn("kind", params)
        self.assertFalse(hasattr(Graph, "cone"))
        self.assertFalse(hasattr(Graph, "torus"))
        self.assertFalse(hasattr(Graph, "sphere"))
        self.assertFalse(hasattr(Graph, "box"))
        self.assertFalse(hasattr(Graph, "icosahedron"))

    def test_soft1_to_soft9_spine_unchanged(self) -> None:
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
            .texture("albedo", src="albedo.png")
            .gltf("prop", src="prop.gltf")
            .node("a", pickable=True, material={"type": "basic", "opacity": 1})
            .plan()
        )
        kinds = [n["kind"] for n in plan["graph"]["nodes"]]
        self.assertEqual(kinds, ["camera", "light", "texture", "gltf", "node"])
        self.assertEqual(plan["graph"]["nodes"][0]["orbit"]["azimuth"], 0.1)
        self.assertEqual(plan["graph"]["nodes"][4]["material"]["type"], "basic")
        self.assertEqual(plan["graph"]["nodes"][4]["shape"], "box")
        hit = pick({"node_id": "a"}, host="h", cap="tok")
        self.assertEqual(hit[0]["method"], "pick")
        cam = orbit({"azimuth": 0.2}, host="h", cap="tok")
        self.assertEqual(cam[0]["method"], "orbit")

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft10-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        nodes = ops[0]["args"][0]["graph"]["nodes"]
        self.assertEqual(nodes[5]["shape"], "cone")
        self.assertEqual(nodes[6]["shape"], "torus")
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        dumped_ops = json.dumps(ops)
        dumped_result_ops = json.dumps(result["ops"])
        self.assertNotIn(token, dumped_ops)
        self.assertNotIn(token, dumped_result_ops)
        self.assertNotIn('"cap"', dumped_ops)
        self.assertTrue(result["ok"])

    def test_apply_requires_cap_for_soft10_graph(self) -> None:
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap=None)
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap="")
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap="   ")

    def test_threejs_peer_maps_cone_torus_thinly(self) -> None:
        js = Path(threejs_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        for shape, ctor in GEOMETRY.items():
            with self.subTest(shape=shape):
                self.assertIn(f'"{shape}"', js)
                self.assertIn(ctor, js)
        self.assertNotIn("IcosahedronGeometry", js)
        self.assertNotIn("DodecahedronGeometry", js)
        self.assertNotIn("TorusKnotGeometry", js)
        self.assertNotIn("CapsuleGeometry", js)
        self.assertNotIn("RingGeometry", js)
        self.assertNotIn("LatheGeometry", js)
        self.assertNotIn("ExtrudeGeometry", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("useFrame", js)
        self.assertNotIn("MeshPhysicalMaterial", js)
        self.assertNotIn("MeshPhongMaterial", js)

    def test_canvas_peer_degrades_soft10_without_breaking(self) -> None:
        js = Path(canvas_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn('"cone"', js)
        self.assertIn('"torus"', js)
        self.assertIn('"box"', js)
        self.assertIn('"sphere"', js)
        self.assertIn('"plane"', js)
        self.assertIn('"cylinder"', js)
        self.assertIn('getContext("2d")', js)
        self.assertNotIn("ConeGeometry", js)
        self.assertNotIn("TorusGeometry", js)
        self.assertNotIn("MeshStandardMaterial", js)
        self.assertNotIn("Raycaster", js)
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("global.THREE", js)

    def test_peer_contract_soft10(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("pick", PEER["methods"])
        self.assertIn("orbit", PEER["methods"])
        self.assertIn("soft9", PEER)
        self.assertIn("soft10", PEER)
        self.assertIn("cone", PEER["soft10"].lower())
        self.assertIn("torus", PEER["soft10"].lower())
        self.assertIn("box", PEER["soft2"])
        self.assertIn("full three.js catalog", PEER["holds"])
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 10 leftover", laws)
        self.assertIn("Soft 9 leftover", laws)
        self.assertIn("cone", laws.lower())
        self.assertIn("torus", laws.lower())

    def test_features_stays_empty(self) -> None:
        """Soft 10 lives in core SHAPES + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft10LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft10(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 10 thin cone/torus."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 10", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("cone", lowered, path)
            self.assertIn("torus", lowered, path)
            self.assertIn("box", lowered, path)
            self.assertIn("sphere", lowered, path)
            self.assertIn("plane", lowered, path)
            self.assertIn("cylinder", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 15. Soft 10 leftover")[1]
        hold = leftover.lower()
        self.assertIn("catalog", hold)
        self.assertIn("r3f", hold)
        self.assertIn("materials catalog", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)
        keep = leftover.split("HOLD:")[0].lower()
        self.assertIn("box", keep)
        self.assertIn("gltf", keep)
        self.assertIn("texture", keep)

    def test_start_here_soft10_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 10", text)
        self.assertIn("cone", lowered)
        self.assertIn("torus", lowered)
        self.assertTrue(
            "shape" in lowered or "shapes" in lowered,
            "START_HERE must leftover-teach Soft 10 additive shapes",
        )
