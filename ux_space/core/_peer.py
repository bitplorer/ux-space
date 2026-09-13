"""Peer contract. Three.js is the day-1 adapter, not the identity.

Same Plan + apply() ops run on any Peer that implements this contract.
Swap the adapter under ``peers/`` — do not change Graph / space().
"""

from __future__ import annotations

PACKAGE = "ux-space"

PEER = {
    "package": PACKAGE,
    "identity": "adapter",
    "day1": "threejs",
    "methods": ("apply", "update", "destroy"),
    "ops": ("bridge.mount", "bridge.update", "bridge.call", "bridge.destroy"),
    "swap": (
        "Register another adapter with uxBridge.register('ux-space', {mount, update, call}). "
        "Graph, Plan IR, and apply() stay unchanged. Do not name the product surface 'three'."
    ),
    "holds": (
        "zero-Peer 3D",
        "dual Peers",
        "React/R3F",
        "materials catalog",
        "full three.js catalog",
        "Cap-on-ops",
        "renaming motion",
        "sixth Cap Host",
        "ambient Client authority",
    ),
    "soft2": "locked SHAPES box/sphere/plane/cylinder — not the full three.js catalog",
}
