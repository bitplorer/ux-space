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
        "Product never imports ux_channel outside the compose-style wire/ door.",
        "Ops speak the Channel bridge plane only: bridge.mount / update / call.",
        "JSON is the shared language. Unknown fields are ignored. Keys are never reused.",
        "A new v is the only legal break. Additive fields only inside v1.",
        "Features import ux_space.core only. Peers implement the Peer contract.",
        "HOLD: React/R3F, full three.js catalog, zero-Peer 3D, day-1 dual Peers, renaming motion.",
    ),
}
