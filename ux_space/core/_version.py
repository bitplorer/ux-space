"""Single source for package + IR versions.

IR major is the only legal break. Additive fields stay on the same major.
"""

from __future__ import annotations

__version__ = "0.1.0a1"
API_VERSION = __version__
IR_VERSION = "1"
PEER_VERSION = __version__
