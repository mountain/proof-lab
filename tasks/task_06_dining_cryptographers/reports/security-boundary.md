# Security and Trust Boundary

## What Metamath proves

Task 6 exports two theorem labels through the admitted package build:

- `dc_parity_table` conjoins every one of the 32 payer/coin parity rows; and
- `dc_payer_bijection_table` conjoins 24 rows showing that a payer move across a shared edge,
  accompanied by toggling that edge, preserves all three public statements.

Both are constructed without raw steps or protocol-specific hypotheses and accepted by `mmverify`.
The proof module restates the finite protocol table independently of `protocol.py`; bridge tests and
code review audit that the two representations use the same payer and edge conventions.

## What the executable model certifies

For the standard three-party cycle, the test suite visits all 32 combinations of payer and shared
bits. It certifies:

- algebraic correctness of transcript parity;
- Eve's knowledge of whether the NSA or a cryptographer paid;
- Eve's inability to narrow a cryptographer payer below all three participants;
- each honest non-payer's inability to narrow the payer below the other two participants; and
- exact equality of the Alice-, Bob-, and Carol-paid transcript distributions.

For the one-edge disconnected topology, the suite visits all 8 worlds and returns concrete
anonymity breaches, including both worlds in which Eve uniquely identifies Carol.

“Exact distribution” means integer counting over every bit assignment. Probability enters only
when the model assumes those assignments are independent and equiprobable.

## What it does not certify

- No compromised participant, colluding coalition, malicious deviation, abort, or forged message
  is modeled.
- Secret bits are assumed fresh, private, independent, and unbiased; generation and key exchange
  are outside the model.
- Timing, traffic analysis, endpoint identity, implementation leakage, and network metadata are
  outside the model.
- The result covers the declared three-party graphs, not arbitrary group sizes or topologies.
- The Python finite-model evaluator is not independently proof-checked by Metamath.

The word “anonymity” in Task 6 therefore refers only to payer indistinguishability in this ideal
finite observation model. It must not be generalized to production deployment security.

## Remaining formal boundary

`proof_lab.build` now admits Task 6's proof module alongside Tasks 1 and 4. The package initializer
imports neither `protocol.py` nor `demo.py`, so computational evidence is not executed as a side
effect of formal construction. The Python evaluator is still required for accessibility cells,
knowledge, public restriction, candidate sets, exact counting, and the broken-topology search.

The remaining promotion requires a proof-producing finite modal lowering and checked aggregation
of counting obligations. Until then, only the two named finite tables are called formally proved.
