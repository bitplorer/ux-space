"""Cap-aware gate. Cap mint stays Channel.

This Soft refuses a missing token on the server. It does not HMAC-sign,
verify, host Caps, or copy the token onto Result ops. Peer does not need it.
Channel.boot / CapService.mint / mount_channel remain the Cap Host.
"""

from __future__ import annotations

from typing import Any


class CapRequired(ValueError):
    """apply() requires a Channel-minted Cap. This Soft does not mint Caps."""


def require_cap(cap: Any) -> str:
    """Return a non-empty Cap token for the server gate. Do not put it on ops."""
    if cap is None:
        raise CapRequired(
            "apply requires a Channel-minted Cap; mint stays on Channel "
            "(ch.control / CapService.mint). ux-space does not host Caps."
        )
    if isinstance(cap, str) and cap.strip():
        return cap.strip()
    for attr in ("token", "value", "cap"):
        token = getattr(cap, attr, None)
        if isinstance(token, str) and token.strip():
            return token.strip()
    if isinstance(cap, dict):
        token = cap.get("token") or cap.get("cap")
        if isinstance(token, str) and token.strip():
            return token.strip()
    raise CapRequired(
        "apply requires a Channel-minted Cap token (str or object with .token). "
        "Cap mint stays on Channel — do not invent a second Cap Host."
    )
