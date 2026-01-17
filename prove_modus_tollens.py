from logic.propositional.hilbert import HilbertSystem
from logic.propositional.hilbert.lemmas import LemmaBuilder, LemmaProof

def prove_modus_tollens(sys: HilbertSystem) -> LemmaProof:
    """Modus Tollens: ph -> ps, -. ps |- -. ph
    
    Source: `https://math.stackexchange.com/questions/767603/hilbert-system-with-propositional-logic-p-rightarrow-q-neg-q-vdash-neg-p`
    """
    lb = LemmaBuilder(sys, "modus_tollens")
    
    # Hypotheses
    h1 = lb.hyp("h1", "ph -> ps")
    h2 = lb.hyp("h2", "-. ps")
    
    # Step 1: (ph -> ps) -> (-. ps -> -. ph)  (Contrapositive)
    s1 = lb.step("s1", "( ph -> ps ) -> ( -. ps -> -. ph )", "con3")
    
    # Step 2: -. ps -> -. ph (MP h1, s1)
    s2 = lb.mp("s2", h1, s1, "MP h1, s1")
    
    # Step 3: -. ph (MP h2, s2)
    s3 = lb.mp("s3", h2, s2, "MP h2, s2")
    
    return lb.build(s3)
