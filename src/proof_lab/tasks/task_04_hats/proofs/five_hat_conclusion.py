from __future__ import annotations

from logic.propositional.hilbert import System
from skfd.proof import Proof, ProofBuilder


def prove_five_hat_conclusion(system: System) -> Proof:
    """The five-hat puzzle's compiled core: Carol cannot be wearing black."""
    proof = ProofBuilder(system, "five_hat_conclusion")

    alice_unknown = proof.hyp("hats.1", "φ")
    bob_not_knows_white = proof.hyp("hats.2", "¬ χ")
    epistemic_bridge = proof.hyp("hats.3", "φ → ( ψ → χ )")

    black_implies_bob_knows = proof.mp(
        "s1",
        alice_unknown,
        epistemic_bridge,
        note="Alice's announcement specializes the epistemic bridge",
    )
    contraposition = proof.ref(
        "s2",
        "( ψ → χ ) -> ( ¬ χ → ¬ ψ )",
        ref="con3",
        note="contraposition",
    )
    bob_unknown_implies_not_black = proof.mp(
        "s3",
        black_implies_bob_knows,
        contraposition,
        note="MP s1, s2",
    )
    carol_not_black = proof.mp(
        "s4",
        bob_not_knows_white,
        bob_unknown_implies_not_black,
        note="Bob's announcement eliminates Carol-black",
    )

    return proof.build(carol_not_black)
