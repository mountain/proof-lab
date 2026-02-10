from __future__ import annotations

from logic.propositional.hilbert import HilbertSystem
from logic.propositional.hilbert.lemmas import LemmaBuilder, LemmaProof


# Removed from metamath-logic base_lemmas; parked here for future work.


def prove_L3_or_intro_left(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L3_or_intro_left")
    stmt = lb.raw("s1", "φ → ( ¬ φ → ψ )", note="Or intro left")
    return lb.build(stmt)


def prove_L4_demorgan(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L4_demorgan")
    stmt = lb.raw("s1", "¬ ( φ ∧ ψ ) -> ( ¬ ¬ φ → ¬ ψ )", note="De Morgan")
    return lb.build(stmt)


def prove_L5_contrapositive(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L5_contrapositive")
    stmt = lb.raw("s1", "( φ → ψ ) -> ( ¬ ψ → ¬ φ )", note="Contrapositive")
    return lb.build(stmt)


def prove_L6_double_neg_intro(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L6_double_neg_intro")
    stmt = lb.raw("s1", "φ → ¬ ¬ φ", note="Double negation intro")
    return lb.build(stmt)


def prove_L7_double_neg_elim(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L7_double_neg_elim")
    stmt = lb.raw("s1", "¬ ¬ φ → φ", note="Double negation elim")
    return lb.build(stmt)


def prove_L8_excluded_middle(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L8_excluded_middle")
    stmt = lb.raw("s1", "¬ φ → ¬ φ", note="Excluded middle")
    return lb.build(stmt)


def prove_L9_peirce(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "L9_peirce")
    stmt = lb.raw("s1", "( ( φ → ψ ) -> φ ) -> φ", note="Peirce")
    return lb.build(stmt)
