from __future__ import annotations

from typing import Any


def prove_linearity(sys: Any) -> Any:
    """
    Linearity: ¬(φ → ψ) → (ψ → φ)
    """
    from skfd.proof import ProofBuilder

    lb = ProofBuilder(sys, "linearity")
    res = lb.ref("res", "¬ ( φ → ψ ) -> ( ψ → φ )", ref="pm2.521", note="pm2.521")
    return lb.build(res)
