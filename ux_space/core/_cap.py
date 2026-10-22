"""Cap gate. Cap mint and verify stay Channel.

Verbs authorize from ``ctx.verified``: what the Channel Cap Host verified for
this Intent (ux-channel ``VerifiedContext``, built only from verify output).
This Soft never reads a Cap token, never verifies one, and never copies Cap
data onto Result ops. Peer does not need it.
"""

from __future__ import annotations

from typing import Any


class CapRequired(ValueError):
    """A verb ran without a verified Cap for its action. This Soft does not mint Caps."""


def require_verified(ctx: Any, method: str) -> None:
    """Fail closed unless ``ctx.verified`` holds a Cap whose action covers ``method``.

    A Cap covers ``method`` when its action is ``method`` or ends in
    ``.method`` (``Space.apply`` covers ``apply``).
    """
    verified = getattr(ctx, "verified", None)
    if verified is None:
        raise CapRequired(
            f"{method} requires a handler ctx whose ctx.verified is set; "
            "the Intent must carry a Channel-minted Cap."
        )
    action = getattr(verified, "action", None)
    if not isinstance(action, str) or not (action == method or action.endswith(f".{method}")):
        raise CapRequired(f"verified Cap is for {action!r}, not {method!r}")
