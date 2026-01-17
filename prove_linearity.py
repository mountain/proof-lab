from logic.propositional.hilbert import HilbertSystem
from logic.propositional.hilbert.lemmas import LemmaBuilder, LemmaProof

def prove_linearity(sys: HilbertSystem) -> LemmaProof:
    """Linearity: -. ( ph -> ps ) -> ( ps -> ph )
       Equivalent to (ph -> ps) \/ (ps -> ph)

       Source: `https://math.stackexchange.com/questions/4476682/prove-that-p-to-q-lor-q-to-p-is-a-tautology-in-hilbert-system`
    """
    lb = LemmaBuilder(sys, "linearity")
    
    # Goal: -. ( ph -> ps ) -> ( ps -> ph )
    
    # Strategy:
    # 1. -. ( ph -> ps ) -> ph
    # 2. ph -> ( ps -> ph )  (A1)
    # 3. -. ( ph -> ps ) -> ( ps -> ph ) (Syllogism)
    
    # Proof of 1: -. ( ph -> ps ) -> ph
    # We know -. ph -> ( ph -> ps ) (pm2.21)
    # Contrapositive (con3): ( -. ph -> ( ph -> ps ) ) -> ( -. ( ph -> ps ) -> -. -. ph )
    # So we can get: -. ( ph -> ps ) -> -. -. ph
    # Then -. -. ph -> ph (L7)
    # So -. ( ph -> ps ) -> ph
    
    # Step 1.1: -. ph -> ( ph -> ps )
    s1_1 = lb.step("s1.1", "-. ph -> ( ph -> ps )", "pm2.21")
    
    # Step 1.2: ( -. ph -> ( ph -> ps ) ) -> ( -. ( ph -> ps ) -> -. -. ph )
    # This is con3 with phi = -. ph, psi = (ph -> ps)
    s1_2 = lb.step("s1.2", "( -. ph -> ( ph -> ps ) ) -> ( -. ( ph -> ps ) -> -. -. ph )", "con3 instance")
    
    # Step 1.3: -. ( ph -> ps ) -> -. -. ph
    s1_3 = lb.mp("s1.3", s1_1, s1_2)
    
    # Step 1.4: -. -. ph -> ph
    s1_4 = lb.step("s1.4", "-. -. ph -> ph", "L7_double_neg_elim")
    
    # Step 1.5: -. ( ph -> ps ) -> ph
    # Constructing syl steps for s1.5:
    # s1.4_lift: ( -. -. ph -> ph ) -> ( -. ( ph -> ps ) -> ( -. -. ph -> ph ) ) (A1)
    s1_4_lift = lb.step("s1.4_lift", "( -. -. ph -> ph ) -> ( -. ( ph -> ps ) -> ( -. -. ph -> ph ) )", "A1")
    
    # s1_5_pre: -. ( ph -> ps ) -> ( -. -. ph -> ph )
    s1_5_pre = lb.mp("s1.5_pre", s1_4, s1_4_lift)
    
    # s1_5_dist: ( -. ( ph -> ps ) -> ( -. -. ph -> ph ) ) -> ( ( -. ( ph -> ps ) -> -. -. ph ) -> ( -. ( ph -> ps ) -> ph ) ) (A2)
    s1_5_dist = lb.step("s1.5_dist", "( -. ( ph -> ps ) -> ( -. -. ph -> ph ) ) -> ( ( -. ( ph -> ps ) -> -. -. ph ) -> ( -. ( ph -> ps ) -> ph ) )", "A2")
    
    # s1_5_impl: ( -. ( ph -> ps ) -> -. -. ph ) -> ( -. ( ph -> ps ) -> ph )
    s1_5_impl = lb.mp("s1.5_impl", s1_5_pre, s1_5_dist)
    
    # s1_5: -. ( ph -> ps ) -> ph
    s1_5 = lb.mp("s1.5", s1_3, s1_5_impl)
    
    # Step 2: ph -> ( ps -> ph )
    s2 = lb.step("s2", "ph -> ( ps -> ph )", "A1")
    
    # Step 3: -. ( ph -> ps ) -> ( ps -> ph )
    # syl(s1.5, s2)
    # s1.5: -. ( ph -> ps ) -> ph
    # s2: ph -> ( ps -> ph )
    
    # Constructing syl steps for s3:
    # s2_lift: ( ph -> ( ps -> ph ) ) -> ( -. ( ph -> ps ) -> ( ph -> ( ps -> ph ) ) ) (A1)
    s2_lift = lb.step("s2_lift", "( ph -> ( ps -> ph ) ) -> ( -. ( ph -> ps ) -> ( ph -> ( ps -> ph ) ) )", "A1")
    
    # s3_pre: -. ( ph -> ps ) -> ( ph -> ( ps -> ph ) )
    s3_pre = lb.mp("s3_pre", s2, s2_lift)
    
    # s3_dist: ( -. ( ph -> ps ) -> ( ph -> ( ps -> ph ) ) ) -> ( ( -. ( ph -> ps ) -> ph ) -> ( -. ( ph -> ps ) -> ( ps -> ph ) ) ) (A2)
    s3_dist = lb.step("s3_dist", "( -. ( ph -> ps ) -> ( ph -> ( ps -> ph ) ) ) -> ( ( -. ( ph -> ps ) -> ph ) -> ( -. ( ph -> ps ) -> ( ps -> ph ) ) )", "A2")
    
    # s3_impl: ( -. ( ph -> ps ) -> ph ) -> ( -. ( ph -> ps ) -> ( ps -> ph ) )
    s3_impl = lb.mp("s3_impl", s3_pre, s3_dist)
    
    # s3: -. ( ph -> ps ) -> ( ps -> ph )
    s3 = lb.mp("s3", s1_5, s3_impl)
    
    return lb.build(s3)
