from logic.propositional.hilbert import System
from skfd.proof import Proof, ProofBuilder


def prove_mp2(sys: System) -> Proof:
    """
    Double Modus Ponens: φ, ψ, (φ → (ψ → χ)) ⊢ χ
    """
    lb = ProofBuilder(sys, "mp2")
 
    h_phi = lb.hyp("mp2.1", "φ")
    h_psi = lb.hyp("mp2.2", "ψ")
    h_imp = lb.hyp("mp2.3", "φ → ( ψ → χ )")
 
    s1 = lb.mp("s1", h_phi, h_imp, note="MP mp2.1, mp2.3")
    s2 = lb.mp("s2", h_psi, s1, note="MP mp2.2, s1")
 
    return lb.build(s2)
