from __future__ import annotations

from logic.propositional.hilbert import System
from skfd.proof import Proof, ProofBuilder


def prove_linearity(system: System) -> Proof:
    """Dependency smoke test: not (phi -> psi) -> (psi -> phi)."""
    proof = ProofBuilder(system, "linearity")
    result = proof.ref(
        "res",
        "¬ ( φ → ψ ) -> ( ψ → φ )",
        ref="pm2.521",
        note="pm2.521 import smoke test",
    )
    return proof.build(result)
