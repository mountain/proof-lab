# Security and Trust Boundary

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

## Why the task remains quarantined

`proof_lab.build` admits only Tasks 1 and 4. Task 6 has no builder and is absent from
`PACKAGE_TASK_IDS`; its tests are computational evidence. A promotion would require generated
propositional obligations for the finite information cells and public restriction, plus checked
counting certificates for the distribution claim. Until that path exists, passing CI confirms the
declared exhaustive computation without relabeling it as a kernel-verified theorem.
