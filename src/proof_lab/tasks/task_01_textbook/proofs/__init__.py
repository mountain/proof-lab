from __future__ import annotations

from .double_modus_ponens import prove_mp2
from .linearity_import import prove_linearity
from .modus_tollens import prove_modus_tollens

__all__ = ["prove_linearity", "prove_modus_tollens", "prove_mp2"]
