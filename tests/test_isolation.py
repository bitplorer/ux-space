"""OWN — Isolation, Cap Host, banned public names."""

from __future__ import annotations

import ast
import importlib
import sys
import unittest
from pathlib import Path

import ux_space

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "ux_space"

BANNED_IMPORTS = ("ux_channel", "cek_", "cek_host", "cek_runtime")
BANNED_PUBLIC = frozenset(
    {
        "scene",
        "Scene",
        "ux_scene",
        "Channel",
        "CapService",
        "CapMachine",
        "mint",
    }
)
def _py_files() -> list[Path]:
    return [p for p in PKG.rglob("*.py") if p.is_file()]


def _in_wire(path: Path) -> bool:
    return "/wire/" in str(path).replace("\\", "/")


class IsolationTests(unittest.TestCase):
    def test_public_surface_from_core_only(self) -> None:
        for name in ux_space.__all__:
            self.assertTrue(hasattr(ux_space, name), name)
        self.assertNotIn("wire", ux_space.__all__)
        self.assertNotIn("boot", ux_space.__all__)
        self.assertNotIn("mount_channel", ux_space.__all__)

    def test_banned_public_names(self) -> None:
        names = set(ux_space.__all__)
        leaked = names & BANNED_PUBLIC
        self.assertEqual(leaked, set())

    def test_core_never_imports_channel(self) -> None:
        violations: list[str] = []
        for path in _py_files():
            if _in_wire(path):
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if any(alias.name == b or alias.name.startswith(f"{b}.") for b in BANNED_IMPORTS if not b.endswith("_")):
                            violations.append(f"{path}:{node.lineno}: import {alias.name}")
                        if alias.name.startswith("ux_channel"):
                            violations.append(f"{path}:{node.lineno}: import {alias.name}")
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module == "ux_channel" or node.module.startswith("ux_channel."):
                        violations.append(f"{path}:{node.lineno}: from {node.module}")
        self.assertEqual(violations, [])

    def test_importing_package_does_not_load_channel(self) -> None:
        sys.modules.pop("ux_space", None)
        sys.modules.pop("ux_channel", None)
        importlib.invalidate_caches()
        importlib.import_module("ux_space")
        self.assertNotIn("ux_channel", sys.modules)

    def test_apply_source_does_not_emit_meta_cap(self) -> None:
        text = (PKG / "core" / "_ops.py").read_text(encoding="utf-8")
        self.assertIn("require_cap(cap)", text)
        self.assertNotIn('meta={"cap"', text)
        self.assertNotIn('"cap": token', text)

    def test_no_cap_host_clone(self) -> None:
        for path in _py_files():
            if _in_wire(path):
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("class CapService", text, path)
            self.assertNotIn("CapMachine", text, path)
            self.assertNotIn("URLSafeTimedSerializer", text, path)

    def test_no_ux_scene_in_public_docs_of_api(self) -> None:
        self.assertNotIn("ux-scene", "".join(ux_space.__all__))
        self.assertEqual(ux_space.PACKAGE, "ux-space")

    def test_wire_is_importable_without_channel(self) -> None:
        import ux_space.wire as door

        self.assertIn("boot", door.__all__)
        self.assertIn("mount_channel", door.__all__)
        self.assertIn("register_manifest", door.__all__)
        self.assertTrue(callable(door.boot))

    def test_day1_example_uses_wire_door(self) -> None:
        app = (ROOT / "examples" / "day1" / "app.py").read_text(encoding="utf-8")
        self.assertIn("from ux_space.wire import", app)
        self.assertNotIn("from ux_channel", app)
        self.assertNotIn("import ux_channel", app)

    def test_features_has_no_python(self) -> None:
        feature_py = list((PKG / "features").glob("*.py"))
        self.assertEqual(feature_py, [])
