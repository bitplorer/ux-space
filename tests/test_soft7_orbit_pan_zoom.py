"""Soft 7 leftover locks — camera orbit/pan/zoom + Cap-gated Plan ops.

Graph / space() stay Soft day-1. Soft 2 SHAPES, Soft 3 camera/light,
Soft 4 rotation/scale + material {basic}, Soft 5 canvas swap, Soft 6
pick/hit stay locked. Isolation + Cap-on-ops absence stay locked.

Frozen Graph names: ``.camera(..., orbit=, pan=, zoom=)``.
IR fields on camera nodes (additive v1):
  ``orbit`` ``{azimuth?, polar?}`` radians,
  ``pan`` ``{x?, y?}``,
  ``zoom`` number (distance).
Cap-gated verbs: ``orbit`` / ``pan`` / ``zoom`` (host=, cap=)
  → ``bridge.call`` methods ``orbit`` / ``pan`` / ``zoom``.
Peer ``peers/threejs`` applies those fields/verbs as thin camera pose.
Not OrbitControls. Not a generic pointer stack. Not a second Graph API.

HOLD Soft 8 materials, Soft 9 loaders, Soft 10 primitives, R3F,
generic pointer stack, Behavior/Motion clone, Cap-on-ops, zero-Peer,
renaming motion, dual concurrent Peers, sixth Cap Host.
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
    pan,
    pick,
    space,
    to_result,
    validate_plan,
    zoom,
)
from ux_space.core._ir import CAMERAS, LIGHTS, MATERIALS, SHAPES
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
            material={"type": "basic", "color": "#22c55e", "opacity": 0.8},
            pickable=True,
        )
    )


class Soft7OrbitPanZoomTests(unittest.TestCase):
    def test_locked_sets_unchanged(self) -> None:
        self.assertEqual(SHAPES, SOFT10_SHAPES)
        self.assertTrue(SOFT2_SHAPES <= SHAPES)
        self.assertEqual(CAMERAS, SOFT3_CAMERAS)
        self.assertEqual(LIGHTS, SOFT3_LIGHTS)
        self.assertEqual(MATERIALS, SOFT8_MATERIALS)
        self.assertTrue(SOFT4_MATERIALS <= MATERIALS)
        self.assertNotIn("icosahedron", SHAPES)
        self.assertNotIn("torusKnot", SHAPES)
        self.assertNotIn("orthographic", CAMERAS)
        self.assertNotIn("point", LIGHTS)
        self.assertNotIn("phong", MATERIALS)

    def test_validate_accepts_orbit_pan_zoom_on_camera(self) -> None:
        out = validate_plan(_mixed().plan())
        eye = out["graph"]["nodes"][0]
        self.assertEqual(eye["kind"], "camera")
        self.assertEqual(eye["id"], "eye")
        self.assertEqual(eye["camera"], "perspective")
        self.assertEqual(eye["orbit"], {"azimuth": 0.4, "polar": 1.2})
        self.assertEqual(eye["pan"], {"x": 0.1, "y": 0.2})
        self.assertEqual(eye["zoom"], 5.0)
        self.assertEqual(eye["rotation"], [0, 0.1, 0])
        hero = out["graph"]["nodes"][3]
        self.assertIs(hero["pickable"], True)
        self.assertEqual(hero["shape"], "box")

    def test_orbit_pan_zoom_absent_by_default(self) -> None:
        """Optional fields — Soft 1–6 cameras stay unmarked."""
        plan = space("s").camera("eye").node("a").plan()
        cam = plan["graph"]["nodes"][0]
        self.assertEqual(cam["kind"], "camera")
        self.assertNotIn("orbit", cam)
        self.assertNotIn("pan", cam)
        self.assertNotIn("zoom", cam)

    def test_unknown_fields_still_kept(self) -> None:
        plan = _mixed().plan()
        plan["graph"]["nodes"][0]["spin"] = 1
        plan["graph"]["nodes"][0]["orbit"]["hint"] = "keep"
        out = validate_plan(plan)
        self.assertEqual(out["graph"]["nodes"][0]["spin"], 1)
        self.assertEqual(out["graph"]["nodes"][0]["orbit"]["hint"], "keep")
        self.assertEqual(out["graph"]["nodes"][0]["orbit"]["azimuth"], 0.4)

    def test_validate_rejects_bad_orbit_pan_zoom(self) -> None:
        with self.assertRaises(PlanError):
            space("s").camera("eye", orbit="spin").plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", orbit=True).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", orbit={"azimuth": "left"}).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", pan=[0, 1]).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", pan={"x": True}).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", zoom="near").plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", zoom=True).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", zoom=0).plan()
        with self.assertRaises(PlanError):
            space("s").camera("eye", zoom=-1).plan()
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
                                "kind": "camera",
                                "id": "c",
                                "camera": "perspective",
                                "orbit": "yes",
                            }
                        ],
                    },
                }
            )

    def test_frozen_graph_camera_orbit_pan_zoom(self) -> None:
        """Frozen Soft 7 names: Graph.camera(orbit=, pan=, zoom=). Not a second Graph."""
        cam_params = inspect.signature(Graph.camera).parameters
        self.assertIn("orbit", cam_params)
        self.assertIn("pan", cam_params)
        self.assertIn("zoom", cam_params)
        self.assertIn("camera", cam_params)
        self.assertIn("rotation", cam_params)
        self.assertNotIn("kind", cam_params)
        self.assertFalse(hasattr(Graph, "orbit"))
        self.assertFalse(hasattr(Graph, "pan"))
        self.assertFalse(hasattr(Graph, "zoom"))
        self.assertFalse(hasattr(Graph, "control"))
        node_params = inspect.signature(Graph.node).parameters
        light_params = inspect.signature(Graph.light).parameters
        self.assertNotIn("orbit", node_params)
        self.assertNotIn("pan", node_params)
        self.assertNotIn("zoom", node_params)
        self.assertNotIn("orbit", light_params)
        self.assertNotIn("pan", light_params)
        self.assertNotIn("zoom", light_params)
        self.assertIn("pickable", node_params)

    def test_soft1_to_soft6_spine_unchanged(self) -> None:
        self.assertTrue(callable(space))
        self.assertTrue(callable(apply))
        self.assertTrue(callable(pick))
        self.assertIsInstance(space("stage"), Graph)
        for shape in sorted(SOFT2_SHAPES):
            with self.subTest(shape=shape):
                plan = space("stage").node("hero", shape=shape).plan()
                self.assertEqual(plan["graph"]["nodes"][0]["kind"], "node")
                self.assertEqual(plan["graph"]["nodes"][0]["shape"], shape)
        plan = (
            space("s")
            .camera("eye")
            .light("fill")
            .node("a", pickable=True)
            .plan()
        )
        self.assertEqual(plan["graph"]["nodes"][0]["kind"], "camera")
        self.assertEqual(plan["graph"]["nodes"][1]["kind"], "light")
        self.assertEqual(plan["graph"]["nodes"][2]["kind"], "node")
        self.assertIs(plan["graph"]["nodes"][2]["pickable"], True)
        hit = pick({"node_id": "a"}, host="h", cap="tok")
        self.assertEqual(hit[0]["method"], "pick")

    def test_orbit_pan_zoom_are_cap_gated_plan_ops(self) -> None:
        token = "soft7-cap-MUST-NOT-SHIP"
        for method, fn, payload in (
            ("orbit", orbit, {"azimuth": 0.2, "polar": 1.1}),
            ("pan", pan, {"x": 0.3, "y": -0.1}),
            ("zoom", zoom, {"distance": 3.5}),
        ):
            with self.subTest(method=method):
                ops = fn(payload, host="stage-3d", cap=token)
                result = to_result(ops)
                self.assertEqual(len(ops), 1)
                op = ops[0]
                self.assertEqual(op["op"], "bridge.call")
                self.assertEqual(op["method"], method)
                self.assertEqual(op["package"], "ux-space")
                self.assertEqual(op["id"], "stage-3d")
                self.assertEqual(op["args"][0], payload)
                self.assertNotIn("meta", op)
                self.assertNotIn("cap", op)
                dumped_ops = json.dumps(ops)
                dumped_result_ops = json.dumps(result["ops"])
                self.assertNotIn(token, dumped_ops)
                self.assertNotIn(token, dumped_result_ops)
                self.assertNotIn('"cap"', dumped_ops)
                self.assertTrue(result["ok"])

    def test_orbit_pan_zoom_keep_unknown_fields(self) -> None:
        ops = orbit({"azimuth": 0.1, "hint": "keep"}, host="h", cap="tok")
        self.assertEqual(ops[0]["args"][0]["hint"], "keep")
        ops = pan({"x": 1, "source": "peer"}, host="h", cap="tok")
        self.assertEqual(ops[0]["args"][0]["source"], "peer")
        ops = zoom({"distance": 2.0, "easing": "none"}, host="h", cap="tok")
        self.assertEqual(ops[0]["args"][0]["easing"], "none")

    def test_orbit_pan_zoom_require_cap(self) -> None:
        for fn, payload in (
            (orbit, {"azimuth": 0.1}),
            (pan, {"x": 0.1}),
            (zoom, {"distance": 2.0}),
        ):
            with self.subTest(fn=fn.__name__):
                with self.assertRaises(CapRequired):
                    fn(payload, host="h", cap=None)
                with self.assertRaises(CapRequired):
                    fn(payload, host="h", cap="")
                with self.assertRaises(CapRequired):
                    fn(payload, host="h", cap="   ")

    def test_orbit_pan_zoom_require_host_and_payload(self) -> None:
        with self.assertRaises(ValueError):
            orbit({"azimuth": 0.1}, cap="tok")
        with self.assertRaises(ValueError):
            pan({"x": 0.1}, cap="tok")
        with self.assertRaises(ValueError):
            zoom({"distance": 2.0}, cap="tok")
        with self.assertRaises(ValueError):
            orbit({}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            orbit({"azimuth": "left"}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            pan({}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            pan({"x": True}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            zoom({}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            zoom({"distance": 0}, host="h", cap="tok")
        with self.assertRaises(ValueError):
            zoom("near", host="h", cap="tok")

    def test_apply_mixed_graph_no_cap_on_ops(self) -> None:
        token = "soft7-apply-cap-MUST-NOT-SHIP"
        ops = apply(_mixed(), cap=token)
        result = to_result(ops)
        self.assertEqual(ops[0]["op"], "bridge.call")
        self.assertEqual(ops[0]["method"], "apply")
        self.assertEqual(ops[0]["package"], "ux-space")
        eye = ops[0]["args"][0]["graph"]["nodes"][0]
        self.assertEqual(eye["orbit"]["azimuth"], 0.4)
        self.assertEqual(eye["pan"]["y"], 0.2)
        self.assertEqual(eye["zoom"], 5.0)
        self.assertNotIn("meta", ops[0])
        self.assertNotIn("cap", ops[0])
        self.assertNotIn(token, json.dumps(ops))
        self.assertNotIn(token, json.dumps(result["ops"]))

    def test_threejs_peer_applies_orbit_pan_zoom_without_orbitcontrols(self) -> None:
        js = Path(threejs_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn("azimuth", js)
        self.assertIn("polar", js)
        self.assertIn("cam.orbit", js)
        self.assertIn("cam.pan", js)
        self.assertIn("cam.zoom", js)
        self.assertIn("orbit:", js)
        self.assertIn("pan:", js)
        self.assertIn("zoom:", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("lookAt(", js)
        self.assertIn("pointerdown", js)
        self.assertIn("pickable", js)
        self.assertIn("BoxGeometry", js)
        self.assertIn("PerspectiveCamera", js)

    def test_canvas_peer_soft7_without_breaking_soft5(self) -> None:
        from ux_space.peers.canvas import adapter_path as canvas_adapter_path

        js = Path(canvas_adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("canvas"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertIn('getContext("2d")', js)
        self.assertIn("orbit:", js)
        self.assertIn("pan:", js)
        self.assertIn("zoom:", js)
        self.assertIn("pickable", js)
        self.assertIn("node_id", js)
        self.assertIn("pointerdown", js)
        self.assertNotIn("Raycaster", js)
        self.assertNotIn("three@0.160.0", js)
        self.assertNotIn("global.THREE", js)
        self.assertNotIn("PerspectiveCamera", js)
        self.assertNotIn("OrbitControls", js)
        self.assertNotIn("lookAt(", js)

    def test_peer_contract_soft7(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("pick", PEER["methods"])
        self.assertIn("orbit", PEER["methods"])
        self.assertIn("pan", PEER["methods"])
        self.assertIn("zoom", PEER["methods"])
        self.assertIn("soft6", PEER)
        self.assertIn("soft7", PEER)
        self.assertIn("orbit", PEER["soft7"].lower())
        self.assertIn("pan", PEER["soft7"].lower())
        self.assertIn("zoom", PEER["soft7"].lower())
        laws = " ".join(CONTRACT["laws"])
        self.assertIn("Soft 7 leftover", laws)
        self.assertIn("Soft 6 leftover", laws)

    def test_features_stays_empty(self) -> None:
        """Soft 7 lives in core IR + orbit/pan/zoom() + Peer apply — not a second Graph."""
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])


class Soft7LeftoverTeachingTests(unittest.TestCase):
    def test_teaching_surfaces_exist(self) -> None:
        missing = [str(p.relative_to(ROOT)) for p in TEACHING if not p.is_file()]
        self.assertEqual(missing, [])

    def test_ownership_changelog_leftover_teach_soft7(self) -> None:
        """OWNERSHIP / CHANGELOG leftover-teach Soft 7 orbit/pan/zoom + Cap-gated verbs."""
        for path in (ROOT / "OWNERSHIP.md", ROOT / "CHANGELOG.md"):
            text = path.read_text(encoding="utf-8")
            lowered = text.replace("**", "").replace("``", "").replace("`", "")
            self.assertIn("Soft 7", text, path)
            self.assertIn("leftover", lowered, path)
            self.assertIn("orbit", lowered, path)
            self.assertIn("pan", lowered, path)
            self.assertIn("zoom", lowered, path)
            self.assertIn(".camera", lowered, path)
            self.assertIn("wire/", lowered, path)
            self.assertIn("ops[].meta.cap", text, path)
            self.assertIn("Channel.boot", text, path)
            self.assertIn("mount_channel", text, path)
        ownership = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        leftover = ownership.split("## 12. Soft 7 leftover")[1]
        hold = leftover.lower()
        self.assertIn("soft 8", hold)
        self.assertIn("r3f", hold)
        self.assertIn("cap-on-ops", hold)
        self.assertIn("zero-peer", hold)
        self.assertIn("renaming motion", hold)
        self.assertIn("sixth cap host", hold)

    def test_start_here_soft7_oneliner(self) -> None:
        text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        lowered = text.replace("**", "").replace("``", "").replace("`", "")
        self.assertIn("Soft 7", text)
        self.assertIn("orbit", lowered)
        self.assertIn("pan", lowered)
        self.assertIn("zoom", lowered)
        self.assertTrue(
            "camera" in lowered,
            "START_HERE must leftover-teach Soft 7 camera orbit/pan/zoom in one line",
        )
