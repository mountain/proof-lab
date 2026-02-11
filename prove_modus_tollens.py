from __future__ import annotations

from typing import Any


def prove_modus_tollens(sys: Any) -> Any:
    """
    Modus Tollens: φ → ψ, ¬ψ ⊢ ¬φ
    """
    from skfd.proof import ProofBuilder

    lb = ProofBuilder(sys, "modus_tollens")

    h1 = lb.hyp("h1", "φ → ψ")
    h2 = lb.hyp("h2", "¬ ψ")

    s1 = lb.ref("s1", "( φ → ψ ) -> ( ¬ ψ → ¬ φ )", ref="con3", note="con3")
    s2 = lb.mp("s2", h1, s1, note="MP h1, s1")
    s3 = lb.mp("s3", h2, s2, note="MP h2, s2")

    return lb.build(s3)
