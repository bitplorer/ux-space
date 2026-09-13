"""Soft 9 leftover locks — thin glTF / texture loaders via Cap-gated apply.

Graph / space() / Cap-gated apply stay Soft day-1. Soft 2 SHAPES,
Soft 3 camera/light, Soft 4 rotation/scale + material {basic}, Soft 5
canvas swap, Soft 6 pick/hit, Soft 7 orbit/pan/zoom, Soft 8
material.type {basic, standard} stay locked.
Isolation + Cap-on-ops absence stay locked.

Frozen Graph fluency: ``.gltf(id, src=)`` and ``.texture(id, src=)`` —
Soft 3-style builders, not ``.node(..., kind=)`` and not a ``load()``
verb. Texture composes with Soft 8 via ``material.map`` (texture node
id). Additive IR v1 — keys never reused; unknown fields ignored.
Load happens through Cap-gated ``apply`` only. Cap NEVER on ops/Result.
``require_cap`` server-side only.

Peer ``peers/threejs`` applies glTF / texture as a Peer concern
(TextureLoader / GLTFLoader stay inside the adapter — not a public
API dump). ``peers/canvas`` swap-proof degrades (skip / placeholder)
without breaking Soft 1–8.

HOLD Soft 10 primitives, R3F, materials catalog, Cap-on-ops, zero-Peer,
renaming motion, dual concurrent Peers, sixth Cap Host, generic pointer
stack, useFrame, OrbitControls dump, GLTFLoader dump as public API.
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
SOFT10_SHAPES = frozenset({"box", "sphere", "plane", "cylinder", "cone", "torus"})
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
                "map": "albedo",
            },
            pickable=True,
        )
    )


class Soft9LoadersTests(unittest.TestCase):
    def test_locked_thin_loader_set(self) -> None:
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertEqual(LOADERS, SOFT9_LOADERS)
        self.assertEqual(NODE_KINDS, SOFT9_NODE_KINDS)
        self.assertIn("gltf", LOADERS)
        self.assertIn("texture", LOADERS)
        self.assertNotIn("fbx", LOADERS)
        self.assertNotIn("obj", LOADERS)
        self.assertNotIn("usdz", LOADERS)
        self.assertNotIn("hdr", LOADERS)
        self.assertNotIn("phong", MATERIALS)
        self.assertNotIn("icosahedron", SHAPES)
        self.assertNotIn("torusKnot", SHAPES)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)

    def test_validate_accepts_gltf_and_texture_nodes(self) -> None:
        out = validate_plan(_mixed().plan())
        kinds = [n["kind"] for n in out["graph"]["nodes"]]
        self.assertEqual(
            kinds, ["camera", "light", "light", "texture", "gltf", "node"]
        )
        tex = out["graph"]["nodes"][3]
        self.assertEqual(tex["id"], "albedo")
        self.assertEqual(tex["src"], "albedo.png")
        gltf = out["graph"]["nodes"][4]
        self.assertEqual(gltf["id"], "prop")
        self.assertEqual(gltf["src"], "prop.gltf")
        self.assertEqual(gltf["position"], [1.2, 0.0, -0.4])
        self.assertEqual(gltf["rotation"], [0.0, 0.3, 0.0])
        self.assertEqual(gltf["scale"], 0.5)
        hero = out["graph"]["nodes"][5]
        self.assertEqual(hero["material"]["type"], "standard")
        self.assertEqual(hero["material"]["map"], "albedo")
        self.assertEqual(hero["material"]["metalness"], 0.2)
        self.assertIs(hero["pickable"], True)

    def test_validate_accepts_ir_loader_nodes(self) -> None:
        out = validate_plan(
            {
                "v": "1",
                "kind": "plan",
                "id": "stage",
                "graph": {
                    "kind": "graph",
                    "nodes": [
                        {"kind": "texture", "id": "albedo", "src": "albedo.png"},
                        {"kind": "gltf", "id": "prop", "src": "prop.gltf"},
                        {"kind": "node", "id": "hero", "shape": "box"},
                    ],
                },
            }
        )
        self.assertEqual(out["graph"]["nodes"][0]["kind"], "texture")
        self.assertEqual(out["graph"]["nodes"][1]["kind"], "gltf")
        self.assertEqual(out["graph"]["nodes"][2]["shape"], "box")

    def test_src_required_and_non_empty(self) -> None:
        with self.assertRaises(PlanError):
            space("s").gltf("prop").plan()
        with self.assertRaises(PlanError):
            space("s").texture("albedo").plan()
        with self.assertRaises(PlanError):
            space("s").gltf("prop", src="").plan()
        with self.assertRaises(PlanError):
            space("s").texture("albedo", src="   ").plan()
        with self.assertRaises(PlanError):
            validate_plan(
                {
                    "v": "1",
                    "kind": "plan",
                    "id": "x",
                    "graph": {
                        "kind": "graph",
                        "nodes": [{"kind": "gltf", "id": "g"}],
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
                        "nodes": [{"kind": "texture", "id": "t"}],
                    },
                }
            )
        with self.assertRaises(PlanError):
            space("s").gltf("prop", src="javascript:alert(1)").plan()
        with self.assertRaises(PlanError):
            space("s").texture("albedo", src="file:///etc/passwd").plan()
        with self.assertRaises(PlanError):
            space("s").gltf("prop", src="blob:https://example.com/x").plan()
        ok = space("s").gltf("prop", src="https://example.com/prop.gltf").plan()
        self.assertEqual(ok["graph"]["nodes"][0]["src"], "https://example.com/prop.gltf")
        ok = space("s").texture("albedo", src="/tex/albedo.png").plan()
        self.assertEqual(ok["graph"]["nodes"][0]["src"], "/tex/albedo.png")

    def test_validate_rejects_catalog_loaders(self) -> None:
        for catalog in ("fbx", "obj", "usdz", "hdr", "loader"):
            with self.subTest(catalog=catalog):
                with self.assertRaises(PlanError):
                    validate_plan(
                        {
                            "v": "1",
                            "kind": "plan",
                            "id": "x",
                            "graph": {
                                "kind": "graph",
                                "nodes": [
                                    {"kind": catalog, "id": "x", "src": "x.bin"},
                                ],
                            },
                        }
                    )

    def test_unknown_loader_fields_kept(self) -> None:
        plan = _mixed().plan()
        plan["graph"]["nodes"][3]["hint"] = "keep"
        plan["graph"]["nodes"][4]["hint"] = "keep"
        out = validate_plan(plan)
        self.assertEqual(out["graph"]["nodes"][3]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][4]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][3]["src"], "albedo.png")
        self.assertEqual(out["graph"]["nodes"][4]["src"], "prop.gltf")

    def test_material_map_optional_and_rejects_empty(self) -> None:
        plan = space("s").node("a", material={"type": "standard"}).plan()
        self.assertNotIn("map", plan["graph"]["nodes"][0]["material"])
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "standard", "map": ""}).plan()
        with self.assertRaises(PlanError):
            space("s").node("a", material={"type": "basic", "map": "   "}).plan()

    def test_soft8_material_without_map_still_works(self) -> None:
        """Soft 8 leftover KEEP — standard without map is still valid."""
        plan = (
            space("s")
            .node(
                "a",
                material={
                    "type": "standard",
                    "color": "#22c55e",
                    "metalness": 0.2,
                    "roughness": 0.55,
                },
            )
            .plan()
        )
        mat = plan["graph"]["nodes"][0]["material"]
        self.assertEqual(mat["type"], "standard")
        self.assertNotIn("map", mat)
        self.assertEqual(mat["metalness"], 0.2)

    def test_frozen_graph_gltf_texture_builders(self) -> None:
        """Soft 9 uses Soft 3 fluency — not node(kind=) and not load()."""
        params = inspect.signature(Graph.node).parameters
        self.assertNotIn("kind", params)
        self.assertNotIn("src", params)
        self.assertIn("material", params)
        self.assertFalse(hasattr(Graph, "load"))
        self.assertFalse(hasattr(Graph, "GLTFLoader"))
        self.assertFalse(hasattr(Graph, "TextureLoader"))
        self.assertTrue(hasattr(Graph, "gltf"))
        self.assertTrue(hasattr(Graph, "texture"))
        gltf_params = inspect.signature(Graph.gltf).parameters
        tex_params = inspect.signature(Graph.texture).parameters
        self.assertIn("src", gltf_params)
        self.assertIn("position", gltf_params)
        self.assertIn("rotation", gltf_params)
        self.assertIn("scale", gltf_params)
        self.assertIn("src", tex_params)
        self.assertNotIn("position", tex_params)
        self.assertNotIn("kind", gltf_params)
        self.assertNotIn("kind", tex_params)

    def test_no_public_loader_dump(self) -> None:
        import ux_space

        leaked = {
            "load",
            "gltf",
            "texture",
            "GLTFLoader",
            "TextureLoader",
        } & set(ux_space.__all__)
        self.assertEqual(leaked, set())
        self.assertFalse(hasattr(ux_space, "load"))
        self.assertFalse(hasattr(ux_space, "GLTFLoader"))
        self.assertFalse(hasattr(ux_space, "TextureLoader"))
        self.assertNotIn("load", PEER["methods"])
        self.assertNotIn("gltf", PEER["methods"])
        self.assertNotIn("texture", PEER["methods"])
        self.assertIn("apply", PEER["methods"])

    def test_soft1_to_soft8_spine_unchanged(self) -> None:
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
        self.assertNotIn("map", plan["graph"]["nodes"][2]["material"])
        hit = pick({"node_id": "a"}, host="h", cap="tok")
        self.assertEqual(hit[0]["method"], "pick")
        cam = orbit({"azimuth": 0.2}, host="h", cap="tok")
        self.assertEqual(cam[0]["method"], "orbit")

    def test_apply_loader_graph_no_cap_on_ops(self) -> None:
        token = "soft9-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        nodes = ops[0]["args"][0]["graph"]["nodes"]
        kinds = [n["kind"] for n in nodes]
        self.assertEqual(kinds, ["camera", "light", "light", "texture", "gltf", "node"])
        self.assertEqual(nodes[3]["src"], "albedo.png")
        self.assertEqual(nodes[4]["src"], "prop.gltf")
        self.assertEqual(nodes[5]["material"]["map"], "albedo")
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        dumped_ops = json.dumps(ops)
        dumped_result_ops = json.dumps(result["ops"])
        self.assertNotIn(token, dumped_ops)
        self.assertNotIn(token, dumped_result_ops)
        self.assertNotIn('"cap"', dumped_ops)
        self.assertTrue(result["ok"])

    def test_apply_requires_cap_for_loader_graph(self) -> None:
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap=None)
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap="")
        with self.assertRaises(CapRequired):
            apply(_mixed(), cap="   ")

    def test_no_load_verb_on_ops(self) -> None:
        from ux_space.core import _ops

        self.assertFalse(hasattr(_ops, "load"))
        self.assertTrue(hasattr(_ops, "apply"))
        src = Path(PKG / "core" / "_ops.py").read_text(encoding="utf-8")
        self.assertNotIn("def load(", src)
        self.assertNotIn('LOAD_METHOD = "load"', src)

    def test_threejs_peer_applies_loaders_internally(self) -> None:
        js = Path(threejs_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("TextureLoader", js)
        self.assertIn("GLTFLoader", js)
        self.assertIn("examples/jsm/loaders/GLTFLoader.js", js)
        self.assertNotIn("examples/js/loaders/GLTFLoader.js", js)
        self.assertIn("isAllowedSrc", js)
        self.assertIn("prev.src === gn.src", js)
        self.assertIn('"gltf"', js)
        self.assertIn('"texture"', js)
        self.assertIn("material.map", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("useFrame", js)
        self.assertNotIn("MeshPhysicalMaterial", js)
        self.assertNotIn("MeshPhongMaterial", js)
        self.assertNotIn("handle.load", js)
        self.assertNotIn("methods: \"load\"", js)
        # Loader stays a Peer concern — not a second public register.
        self.assertNotIn('uxBridge.register("gltf"', js)
        self.assertNotIn('uxBridge.register("GLTFLoader"', js)

    def test_canvas_peer_degrades_loaders_without_breaking(self) -> None:
        js = Path(canvas_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("gltf", js)
        self.assertIn("texture", js)
        self.assertIn("placeholder", js)
        self.assertIn('getContext("2d")', js)
        self.assertNotIn("GLTFLoader", js)
        self.assertNotIn("TextureLoader", js)
        self.assertNotIn("MeshStandardMaterial", js)
        self.assertNotIn("Raycaster", js)
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("global.THREE", js)

    def test_peer_contract_soft9(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("pick", PEER["methods"])
        self.assertIn("orbit", PEER["methods"])
        self.assertIn("soft8", PEER)
        self.assertIn("soft9", PEER)
        self.assertIn("gltf", PEER["soft9"].lower())
        self.assertIn("texture", PEER["soft9"].lower())
        self.assertIn("apply", PEER["soft9"].lower())
        self.assertIn("materials catalog", PEER["holds"])
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 9 leftover", laws)
        self.assertIn("Soft 8 leftover", laws)
        self.assertIn("gltf", laws.lower())
        self.assertIn("texture", laws.lower())

    def test_features_stays_empty(self) -> None:
        """Soft 9 lives in core IR + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft9LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft9(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 9 thin glTF / texture."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 9", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("gltf", lowered, path)
            self.assertIn("texture", lowered, path)
            self.assertIn("src", lowered, path)
            self.assertIn("material.map", lowered, path)
            self.assertIn("apply", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 14. Soft 9 leftover")[1]
        hold = leftover.lower()
        self.assertIn("soft 10", hold)
        self.assertIn("r3f", hold)
        self.assertIn("materials catalog", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)
        self.assertIn("gltfloader", hold.replace(" ", ""))

    def test_start_here_soft9_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 9", text)
        self.assertIn("gltf", lowered)
        self.assertIn("texture", lowered)
        self.assertIn("apply", lowered)
