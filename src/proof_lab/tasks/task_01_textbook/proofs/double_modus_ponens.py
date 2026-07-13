from __future__ import annotations

from logic.propositional.hilbert import System
from skfd.proof import Proof, ProofBuilder


def prove_mp2(system: System) -> Proof:
    """Double Modus Ponens: phi, psi, phi -> (psi -> chi) |- chi."""
    proof = ProofBuilder(system, "mp2")

    h_phi = proof.hyp("mp2.1", "φ")
    h_psi = proof.hyp("mp2.2", "ψ")
    h_imp = proof.hyp("mp2.3", "φ → ( ψ → χ )")

    step_1 = proof.mp("s1", h_phi, h_imp, note="MP mp2.1, mp2.3")
    step_2 = proof.mp("s2", h_psi, step_1, note="MP mp2.2, s1")

    return proof.build(step_2)
