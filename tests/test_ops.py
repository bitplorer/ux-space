"""Ops shape — Channel bridge plane only. apply is Cap-gated."""

from __future__ import annotations

import unittest

from ux_space import (
    APPLY_METHOD,
    OP_APPLY,
    OP_CALL,
    OP_MOUNT,
    OP_UPDATE,
    PACKAGE,
    CapRequired,
    apply,
    dumps,
    host_html,
    loads,
    mount,
    space,
    to_result,
    update,
)


class OpsTests(unittest.TestCase):
    def test_apply_shape(self) -> None:
        graph = space("stage").host("stage-3d").node("hero")
        ops = apply(graph, cap="channel-minted-token")
        self.assertEqual(len(ops), 1)
        op = ops[0]
        self.assertEqual(op["op"], OP_APPLY)
        self.assertEqual(op["op"], OP_CALL)
        self.assertEqual(op["op"], "bridge.call")
        self.assertEqual(op["method"], APPLY_METHOD)
        self.assertEqual(op["method"], "apply")
        self.assertEqual(op["id"], "stage-3d")
        self.assertEqual(op["package"], PACKAGE)
        self.assertEqual(op["package"], "ux-space")
        self.assertEqual(op["args"][0]["id"], "stage")
        self.assertEqual(op["meta"]["cap"], "channel-minted-token")

    def test_apply_requires_cap(self) -> None:
        graph = space("stage").host("stage-3d").node("hero")
        with self.assertRaises(CapRequired):
            apply(graph, cap=None)
        with self.assertRaises(CapRequired):
            apply(graph, cap="")
        with self.assertRaises(CapRequired):
            apply(graph, cap="   ")

    def test_apply_cap_from_object(self) -> None:
        class Token:
            token = "minted-by-channel"

        graph = space("stage").host("h").node("n")
        ops = apply(graph, cap=Token())
        self.assertEqual(ops[0]["meta"]["cap"], "minted-by-channel")

    def test_apply_needs_host(self) -> None:
        graph = space("stage").node("hero")
        with self.assertRaises(ValueError):
            apply(graph, cap="tok")

    def test_to_result(self) -> None:
        graph = space("stage").host("h").node("n")
        result = to_result(apply(graph, cap="tok"), action="Space.apply")
        self.assertTrue(result["ok"])
        self.assertEqual(result["ops"][0]["op"], "bridge.call")
        self.assertEqual(result["meta"]["action"], "Space.apply")

    def test_mount_and_update_builders(self) -> None:
        m = mount("stage-3d", props={"plan": {}})
        self.assertEqual(m[0]["op"], OP_MOUNT)
        self.assertEqual(m[0]["op"], "bridge.mount")
        self.assertEqual(m[0]["package"], "ux-space")
        u = update("stage-3d", {"color": "#fff"})
        self.assertEqual(u[0]["op"], OP_UPDATE)
        self.assertEqual(u[0]["op"], "bridge.update")

    def test_host_html(self) -> None:
        markup = host_html("stage-3d")
        self.assertIn('data-channel-bridge-id="stage-3d"', markup)
        self.assertIn('data-channel-bridge-package="ux-space"', markup)
        self.assertNotIn('data-channel-bridge-package="three"', markup)

    def test_dumps_loads(self) -> None:
        plan = space("stage").node("hero", color="#abc").plan()
        raw = dumps(plan)
        self.assertEqual(loads(raw)["id"], "stage")
        self.assertIn('"v":"1"', raw)
