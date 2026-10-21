"""Executes the day-1 three.js Peer under node (THREE stand-in, no WebGL).

Locks that every mesh node in a Plan lands in the scene, on mount and on update.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from ux_space import space
from ux_space.peers.threejs import adapter_path

HARNESS = Path(__file__).resolve().parent / "js" / "threejs_peer_harness.js"


def _run(mount_plan: dict, update_plan: dict) -> dict:
    out = subprocess.run(
        ["node", str(HARNESS), adapter_path(), json.dumps(mount_plan), json.dumps(update_plan)],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return json.loads(out.stdout)


class ThreejsPeerExecTests(unittest.TestCase):
    def test_every_mesh_node_lands_in_the_scene(self) -> None:
        three = (
            space("stage")
            .host("stage-3d")
            .light("fill", light="ambient")
            .node("a", shape="box")
            .node("b", shape="sphere", position=(1, 0, 0))
            .node("c", shape="torus", position=(-1, 0, 0))
            .plan()
        )
        two = space("stage").host("stage-3d").node("c", shape="cone").node("d").plan()

        scene = _run(three, two)

        self.assertEqual(scene["mount"], ["a", "b", "c"])
        self.assertEqual(sorted(scene["update"]), ["c", "d"])


if __name__ == "__main__":
    unittest.main()
