"""Peer contract. Three.js is the day-1 adapter, not the identity.

Same Plan + apply() ops run on any Peer that implements this contract.
Swap the adapter under ``peers/`` — do not change Graph / space().
Soft 5 leftover: ``peers/canvas`` proves the swap; day1 remains threejs.
Soft 6 leftover: optional mesh ``pickable``; Peer pick reports ``node_id``.
Soft 7 leftover: camera ``orbit`` / ``pan`` / ``zoom``; Cap-gated verbs.
"""

from __future__ import annotations

PACKAGE = "ux-space"

PEER = {
    "package": PACKAGE,
    "identity": "adapter",
    "day1": "threejs",
    "methods": ("apply", "update", "destroy", "pick", "orbit", "pan", "zoom"),
    "ops": ("bridge.mount", "bridge.update", "bridge.call", "bridge.destroy"),
    "swap": (
        "Register another adapter with uxBridge.register('ux-space', {mount, update, call}). "
        "Graph, Plan IR, and apply() stay unchanged. Do not name the product surface 'three'. "
        "Soft 5 leftover: peers/canvas proves the swap; day1 remains threejs."
    ),
    "holds": (
        "zero-Peer 3D",
        "dual concurrent Peers as taught product",
        "React/R3F",
        "materials catalog",
        "full three.js catalog",
        "Cap-on-ops",
        "renaming motion",
        "sixth Cap Host",
        "ambient Client authority",
    ),
    "soft2": "locked SHAPES box/sphere/plane/cylinder — not the full three.js catalog",
    "soft3": "optional camera/light node kinds — perspective / ambient / directional",
    "soft4": "optional mesh rotation/scale + material {basic} (color/opacity)",
    "soft5": "swap path locked — canvas peer proves adapter swap; day1 remains threejs",
    "soft6": "optional mesh pickable + Peer pick reports node_id (point optional); Cap-gated pick()",
    "soft7": "camera orbit/pan/zoom fields + Cap-gated orbit()/pan()/zoom(); thin Peer apply, not OrbitControls",
}
