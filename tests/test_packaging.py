"""Packaging, versions, Peer adapter identity."""

from __future__ import annotations

import unittest
from pathlib import Path

from ux_space import (
    API_VERSION,
    CONTRACT,
    IR_VERSION,
    PACKAGE,
    PEER,
    PEER_VERSION,
    __version__,
)
from ux_space.peers.threejs import ADAPTER_JS, adapter_path

ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_versions(self) -> None:
        self.assertEqual(__version__, "0.1.0a1")
        self.assertEqual(API_VERSION, "0.1.0a1")
        self.assertEqual(PEER_VERSION, "0.1.0a1")
        self.assertEqual(IR_VERSION, "1")
        self.assertEqual(CONTRACT["api"], "0.1.0a1")
        self.assertEqual(CONTRACT["ir"], "1")

    def test_python_floor_is_314(self) -> None:
        text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('name = "ux-space"', text)
        self.assertIn('version = "0.1.0a1"', text)
        self.assertIn('requires-python = ">=3.14"', text)
        self.assertIn("Programming Language :: Python :: 3.14", text)
        self.assertIn('channel = ["ux-channel>=0.1"]', text)
        self.assertNotIn("Programming Language :: Python :: 3.10", text)
        self.assertNotIn("Programming Language :: Python :: 3.11", text)
        self.assertNotIn("Programming Language :: Python :: 3.12", text)

    def test_peer_contract(self) -> None:
        self.assertEqual(PACKAGE, "ux-space")
        self.assertEqual(PEER["package"], "ux-space")
        self.assertEqual(PEER["day1"], "threejs")
        self.assertEqual(PEER["identity"], "adapter")
        self.assertIn("apply", PEER["methods"])
        self.assertIn("bridge.call", PEER["ops"])

    def test_adapter_registers_as_ux_space(self) -> None:
        js = Path(adapter_path()).read_text(encoding="utf-8")
        self.assertIn('uxBridge.register("ux-space"', js)
        self.assertNotIn('uxBridge.register("three"', js)
        self.assertNotIn("ux-scene", js)
        self.assertIn("three@0.160.0", js)
        self.assertTrue(ADAPTER_JS.endswith(".js"))

    def test_license_is_mit(self) -> None:
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", text)
        self.assertIn("bitplorer", text)

    def test_ownership_lock(self) -> None:
        text = (ROOT / "OWNERSHIP.md").read_text(encoding="utf-8")
        self.assertIn("HARD", text)
        self.assertIn("Peer-as-adapter", text)
        self.assertIn("Channel.boot", text)
        self.assertIn("mount_channel", text)
        self.assertIn("ux-scene", text)
        self.assertIn("wire/", text)
        self.assertIn("ops[].meta.cap", text)
        self.assertIn("disclosure", text)
        self.assertIn("server-side", text.lower())
