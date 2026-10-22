"""S2 locks: clients reach the verbs only as Channel actions ``space.*``.

ux-space does no authorization. Channel verifies each Intent's Cap for the
exact action name before the handler runs. Every case runs on both the
cek-host Cap Host and classic CapService.
"""

from __future__ import annotations

import inspect
import unittest

from ux_channel import ChannelConfig

import ux_space
from ux_space import apply, orbit, pan, pick, space, zoom
from ux_space.wire import ACTIONS, boot, register_actions

SECRET = "dev-s2-channel-actions-32chars-min!!"
ARGS = {
    "space.apply": {},
    "space.pick": {"node_id": "hero"},
    "space.orbit": {"azimuth": 0.2},
    "space.pan": {"x": 0.1},
    "space.zoom": {"distance": 3.0},
}


def _channels(require_cap: bool = True):
    for cek in ("require", "off"):
        ch = boot(config=ChannelConfig.development(secret=SECRET, cek=cek, require_cap=require_cap))
        yield cek, ch


class ChannelActionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = space("s").host("stage-3d").node("hero")

    def _dispatch(self, ch, action, args, cap=None):
        intent = {"action": action, "args": args}
        if cap is not None:
            intent["cap"] = cap
        return ch.registry.dispatch(intent)

    def test_actions_are_exact_names(self) -> None:
        self.assertEqual(
            ACTIONS,
            {m: f"space.{m}" for m in ("apply", "pick", "orbit", "pan", "zoom")},
        )

    def test_valid_cap_runs_its_action(self) -> None:
        for cek, ch in _channels():
            register_actions(ch, self.graph, host="stage-3d")
            for method, action in ACTIONS.items():
                with self.subTest(cek=cek, action=action):
                    args = ARGS[action]
                    cap = ch.mint(action, args)
                    r = self._dispatch(ch, action, args, cap)
                    self.assertTrue(r.ok, r.error)
                    (op,) = r.ops
                    self.assertEqual((op["op"], op["method"], op["id"]), ("bridge.call", method, "stage-3d"))
                    self.assertNotIn(cap, repr(r.ops))

    def test_cap_for_one_action_cannot_invoke_another(self) -> None:
        for cek, ch in _channels():
            register_actions(ch, self.graph, host="stage-3d")
            for minted in ACTIONS.values():
                for target in ACTIONS.values():
                    if minted == target:
                        continue
                    with self.subTest(cek=cek, minted=minted, target=target):
                        cap = ch.mint(minted, ARGS[target])
                        r = self._dispatch(ch, target, ARGS[target], cap)
                        self.assertFalse(r.ok)
                        self.assertEqual(r.error.code, "unauthorized")

    def test_forged_cap_strings_are_refused(self) -> None:
        for cek, ch in _channels():
            register_actions(ch, self.graph, host="stage-3d")
            for forged in ("channel-verified", "space.apply", "*", "x" * 64):
                with self.subTest(cek=cek, forged=forged):
                    r = self._dispatch(ch, "space.apply", {}, forged)
                    self.assertFalse(r.ok)
                    self.assertEqual(r.error.code, "unauthorized")

    def test_args_only_callers_are_refused(self) -> None:
        forged_args = {
            "cap": "channel-verified",
            "principal": "admin",
            "subject": "admin",
            "ctx": {"verified": {"action": "space.apply"}},
            "verified": {"action": "space.apply"},
        }
        for cek, ch in _channels():
            register_actions(ch, self.graph, host="stage-3d")
            for action in ACTIONS.values():
                with self.subTest(cek=cek, action=action):
                    r = self._dispatch(ch, action, {**ARGS[action], **forged_args})
                    self.assertFalse(r.ok)
                    self.assertEqual(r.error.code, "unauthorized")

    def test_sealed_args_cannot_be_changed(self) -> None:
        for cek, ch in _channels():
            register_actions(ch, self.graph, host="stage-3d")
            with self.subTest(cek=cek):
                cap = ch.mint("space.zoom", {"distance": 3.0})
                r = self._dispatch(ch, "space.zoom", {"distance": 0.5}, cap)
                self.assertFalse(r.ok)

    def test_open_registry_is_refused(self) -> None:
        for cek, ch in _channels(require_cap=False):
            with self.subTest(cek=cek), self.assertRaises(ValueError):
                register_actions(ch, self.graph, host="stage-3d")


class NoAuthInVerbsTests(unittest.TestCase):
    def test_verbs_take_no_auth_parameter(self) -> None:
        for fn in (apply, pick, orbit, pan, zoom, ux_space.Graph.apply):
            params = inspect.signature(fn).parameters
            with self.subTest(fn=fn.__qualname__):
                self.assertFalse({"cap", "ctx"} & set(params))
        self.assertFalse(hasattr(ux_space, "CapRequired"))


if __name__ == "__main__":
    unittest.main()
