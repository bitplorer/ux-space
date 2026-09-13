"""Frozen product contract. Changing this file is a breaking release."""

from __future__ import annotations

from ux_space.core._peer import PACKAGE, PEER
from ux_space.core._version import API_VERSION, IR_VERSION, PEER_VERSION

CONTRACT = {
    "api": API_VERSION,
    "peer_version": PEER_VERSION,
    "ir": IR_VERSION,
    "facade": "ux_space",
    "package": PACKAGE,
    "op.apply": "bridge.call",
    "apply.method": "apply",
    "peer": PEER,
    "laws": (
        "Package is ux-space / import ux_space. Never name anything public ux-scene.",
        "space() / Graph is the facade. motion owns scene(). Dual door — do not alias.",
        "Seat: Python Plan/Ops → Channel Result → thin Peer apply.",
        "Day-1: one graph + one Cap-gated verb (apply) + one thin Peer apply.",
        "Three.js is the day-1 Peer adapter, not the identity. Package name wraps three.",
        "Same Ops apply to a future non-Three Peer without changing Graph / space().",
        "Cap mint stays Channel (ch.control / CapService.mint / Channel.boot / mount_channel).",
        "Do not invent a second Cap Host. This Soft only refuses a missing Cap.",
        "Cap is server-side only. apply() must not put the token on ops or Result (no meta.cap).",
        "Product never imports ux_channel outside the compose-style wire/ door.",
        "Ops speak the Channel bridge plane only: bridge.mount / update / call.",
        "JSON is the shared language. Unknown fields are ignored. Keys are never reused.",
        "A new v is the only legal break. Additive fields only inside v1.",
        "Features import ux_space.core only. Peers implement the Peer contract.",
        "Soft 2 leftover: SHAPES is a locked set (box, sphere, plane, cylinder) — not the full three.js catalog.",
        "Soft 3 leftover: optional camera/light node kinds (perspective / ambient / directional). Frozen Graph.camera / Graph.light. Additive IR v1.",
        "Soft 4 leftover: optional mesh rotation/scale + material {basic} (color/opacity). Top-level color KEEP; material.color wins. Frozen Graph.node rotation/scale/material. Camera may take rotation.",
        "Soft 5 leftover: canvas Peer proves swap. Same uxBridge.register('ux-space'). Day-1 remains threejs. Graph / Plan IR / apply() unchanged. Not dual concurrent Peers as product.",
        "Soft 6 leftover: optional mesh pickable. Peer raycast/pick reports node_id (+ point). Cap-gated pick(hit) → Result. Cap never on ops. Frozen Graph.node pickable=.",
        "Soft 7 leftover: optional camera orbit/pan/zoom. Frozen Graph.camera orbit=/pan=/zoom=. Cap-gated orbit/pan/zoom → Result. Cap never on ops. Thin Peer apply, not OrbitControls.",
        "Soft 8 leftover: mesh material.type thin set {basic, standard}. Soft 4 basic color/opacity KEEP. Optional metalness/roughness on standard. Frozen Graph.node material=. Cap-gated apply KEEP. Cap never on ops. Not a materials catalog.",
        "HOLD: React/R3F, materials catalog, full three.js catalog, dual Peers, Cap-on-ops, zero-Peer, renaming motion, sixth Cap Host, ambient Client authority.",
    ),
}
