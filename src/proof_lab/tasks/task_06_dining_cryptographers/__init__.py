"""Task 6's lazy public boundary.

Python imports a package initializer before any child module. Consequently, an eager re-export of
``protocol.py`` here would also load the computational model whenever the formal builder asks only
for ``.proofs``. The lazy facade below preserves the original public API for interactive users,
while keeping that semantic code outside proof construction unless one of its names is requested.
"""

from importlib import import_module
from typing import Any

_PROTOCOL_EXPORTS = (
    "ALICE",
    "BOB",
    "CAROL",
    "DISCONNECTED_TOPOLOGY",
    "EAVESDROPPER",
    "NSA",
    "PARTICIPANTS",
    "PAYERS",
    "TRIANGLE_TOPOLOGY",
    "DiningOutcome",
    "DiningWorld",
    "KeyEdge",
    "ProtocolTopology",
    "exact_transcript_formula",
    "outsider_anonymity_breaches",
    "payer_atom",
    "payer_candidates",
    "protocol_model",
    "run_protocol",
    "transcript_distribution",
    "transcript_for",
    "worlds_for",
)


def __getattr__(name: str) -> Any:
    """Resolve computational conveniences only when a caller explicitly asks for one."""

    if name in _PROTOCOL_EXPORTS:
        value = getattr(import_module(f"{__name__}.protocol"), name)
    elif name == "render_demo_report":
        value = getattr(import_module(f"{__name__}.demo"), name)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = value
    return value


__all__ = (*_PROTOCOL_EXPORTS, "render_demo_report")
