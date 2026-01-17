from logic.propositional.hilbert import HilbertSystem
from logic.propositional.hilbert.lemmas import LemmaBuilder, LemmaProof


def prove_modus_tollens(sys: HilbertSystem) -> LemmaProof:
    lb = LemmaBuilder(sys, "modus_tollens_bad")

    h1 = lb.hyp("h1", "ph -> ps")
    h2 = lb.hyp("h2", "-. ps")

    s1 = lb.step("s1", "( ph -> ps ) -> ( -. ps -> -. ps )", "con3")
    s2 = lb.mp("s2", h1, s1, "MP h1, s1")
    s3 = lb.mp("s3", h2, s2, "MP h2, s2")

    return lb.build(s3)

