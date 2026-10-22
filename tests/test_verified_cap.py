"""S2 locks: verbs authorize from ctx.verified, never from a Cap string.

Each case runs on the bare verbs and through a real Channel dispatch, on both
the cek-host Cap Host and classic CapService.
"""

from __future__ import annotations

import inspect
import unittest
from types import SimpleNamespace

from ux_channel import ChannelConfig, Intent

from tests._verified import verified_ctx
from ux_space import CapRequired, apply, orbit, pan, pick, space, zoom
from ux_space.wire import as_channel_result, boot

SECRET = "dev-s2-verified-cap-32chars-min!!!"
VERBS = (
    ("apply", lambda ctx: apply(space("s").host("h").node("n"), ctx=ctx)),
    ("pick", lambda ctx: pick({"node_id": "n"}, host="h", ctx=ctx)),
    ("orbit", lambda ctx: orbit({"azimuth": 0.1}, host="h", ctx=ctx)),
    ("pan", lambda ctx: pan({"x": 0.1}, host="h", ctx=ctx)),
    ("zoom", lambda ctx: zoom({"distance": 2.0}, host="h", ctx=ctx)),
)


def _channel(cek: str):
    ch = boot(config=ChannelConfig.development(secret=SECRET, cek=cek, require_cap=False))
    graph = space("s").host("stage-3d").node("hero")

    @ch.on("Space.apply")
    def apply_space(ctx, **_):
        return as_channel_result(apply(graph, ctx=ctx))

    @ch.on("Space.pick")  # handler misuses its pick Cap to apply
    def pick_space(ctx, **_):
        return as_channel_result(apply(graph, ctx=ctx))

    return ch


class VerbLocks(unittest.TestCase):
    def test_cap_parameter_is_gone(self) -> None:
        for name, fn in (("apply", apply), ("pick", pick), ("orbit", orbit), ("pan", pan), ("zoom", zoom)):
            self.assertNotIn("cap", inspect.signature(fn).parameters, name)
        with self.assertRaises(TypeError):
            apply(space("s").host("h").node("n"), cap="channel-verified")

    def test_forged_string_is_refused(self) -> None:
        forged = ("channel-verified", {"verified": {"action": "Space.apply"}})
        for method, call in VERBS:
            for ctx in forged:
                with self.subTest(method=method, ctx=ctx), self.assertRaises(CapRequired):
                    call(ctx)

    def test_no_verified_context_is_refused(self) -> None:
        for method, call in VERBS:
            for ctx in (None, SimpleNamespace(verified=None)):
                with self.subTest(method=method, ctx=ctx), self.assertRaises(CapRequired):
                    call(ctx)

    def test_cap_for_another_action_is_refused(self) -> None:
        for method, call in VERBS:
            for action in ("Space.pick" if method != "pick" else "Space.apply", f"Space.{method}x", ""):
                with self.subTest(method=method, action=action), self.assertRaises(CapRequired):
                    call(verified_ctx(action))

    def test_verified_cap_for_the_verb_passes(self) -> None:
        for method, call in VERBS:
            for action in (method, f"Space.{method}"):
                with self.subTest(method=method, action=action):
                    (op,) = call(verified_ctx(action))
                    self.assertEqual((op["op"], op["method"]), ("bridge.call", method))


class ChannelDispatchLocks(unittest.TestCase):
    def _each_host(self):
        for cek in ("require", "off"):
            with self.subTest(cek=cek):
                yield _channel(cek)

    def test_forged_string_is_refused(self) -> None:
        for ch in self._each_host():
            for intent in (
                Intent(action="Space.apply", args={}, cap="channel-verified"),
                Intent(action="Space.apply", args={"cap": "channel-verified"}),
            ):
                self.assertFalse(ch.registry.dispatch(intent).ok, intent)

    def test_no_verified_context_is_refused(self) -> None:
        for ch in self._each_host():
            r = ch.registry.dispatch(Intent(action="Space.apply", args={}))
            self.assertFalse(r.ok)
            self.assertIn("ctx.verified", r.error.message)

    def test_cap_for_another_action_is_refused(self) -> None:
        for ch in self._each_host():
            cap = ch.mint("Space.pick", {})
            r = ch.registry.dispatch(Intent(action="Space.pick", args={}, cap=cap))
            self.assertFalse(r.ok)
            self.assertIn("'Space.pick', not 'apply'", r.error.message)

    def test_minted_cap_passes(self) -> None:
        for ch in self._each_host():
            cap = ch.mint("Space.apply", {})
            r = ch.registry.dispatch(Intent(action="Space.apply", args={}, cap=cap))
            self.assertTrue(r.ok, r.error)
            self.assertEqual(r.ops[0]["method"], "apply")
            self.assertNotIn(cap, repr(r.ops))


if __name__ == "__main__":
    unittest.main()
