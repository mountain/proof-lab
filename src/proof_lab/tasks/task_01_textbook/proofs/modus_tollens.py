from __future__ import annotations

from logic.propositional.hilbert import System
from skfd.proof import Proof, ProofBuilder


def prove_modus_tollens(system: System) -> Proof:
    """Modus Tollens: phi -> psi, not psi |- not phi."""
    proof = ProofBuilder(system, "modus_tollens")

    implication = proof.hyp("h1", "φ → ψ")
    negated_consequent = proof.hyp("h2", "¬ ψ")

    contraposition = proof.ref(
        "s1",
        "( φ → ψ ) -> ( ¬ ψ → ¬ φ )",
        ref="con3",
        note="con3",
    )
    lifted = proof.mp("s2", implication, contraposition, note="MP h1, s1")
    result = proof.mp("s3", negated_consequent, lifted, note="MP h2, s2")

    return proof.build(result)
