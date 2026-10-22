"""Stand-in for the handler ctx ux-channel builds, for tests that run without Channel."""

from __future__ import annotations

from types import MappingProxyType, SimpleNamespace


def verified_ctx(action: str, subject: str | None = None) -> SimpleNamespace:
    """A ctx whose ``verified`` mirrors ux-channel ``VerifiedContext``."""
    claims = MappingProxyType({"action": action, "subject": subject})
    return SimpleNamespace(verified=SimpleNamespace(action=action, subject=subject, claims=claims))
