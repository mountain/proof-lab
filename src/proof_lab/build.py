from __future__ import annotations

from skfd.api_v2 import BuildContextV2

from logic.propositional.hilbert import System
from logic.propositional.hilbert._structures import Imp, phi


def build(ctx: BuildContextV2) -> None:
    mm = ctx.mm

    prelude = ctx.deps["metamath-prelude"]
    logic = ctx.deps["metamath-logic"]

    system = System.make(interner=mm.interner, names=ctx.names)
    provable = prelude["|-"]

    stmt = system.compile(Imp(phi, phi), ctx="proof-lab.lab-id")
    lab_id = mm.sym.label("lab-id")

    mm.p(lab_id, tc=provable, expr=stmt.tokens, proof=[prelude["wph"], logic["id"]])
    mm.export(lab_id)
