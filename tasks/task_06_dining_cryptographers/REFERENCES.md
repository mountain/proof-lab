# References and Provenance

## Primary protocol source

- **[C88]** David Chaum, “The Dining Cryptographers Problem: Unconditional Sender and Recipient
  Untraceability,” *Journal of Cryptology* **1**(1), 1988, pp. 65–75.
  [Primary CWI research record](https://ir.cwi.nl/pub/2438) ·
  [DOI: 10.1007/BF00206326](https://doi.org/10.1007/BF00206326).

  Chaum introduces the dining-cryptographers problem and the shared-randomness announcement
  protocol. Task 6 formalizes the paper's elementary three-diner instance as a finite state space;
  it does not claim to implement every construction or adversary setting in the article.

## Semantic dependency

Task 6 reuses Proof Lab's finite S5 and truthful-public-announcement interpreter. Its semantic
sources—Fagin et al. for reasoning about knowledge, Plaza for public announcement, and van
Ditmarsch, van der Hoek, and Kooi for dynamic epistemic logic—are recorded in
[`../task_05_epistemic_puzzles/REFERENCES.md`](../task_05_epistemic_puzzles/REFERENCES.md).

## Local specialization and new counterexample

The following are explicit modeling decisions made by Proof Lab rather than quotations from [C88]:

- public answers are represented as the Boolean tuple `(Alice, Bob, Carol)`;
- the simultaneous tuple is modeled as one exact public announcement;
- Eve is an outsider with no private edge bits;
- “participant anonymity” is checked only for honest non-payers;
- exact distribution equality assumes independent uniform edge bits; and
- the one-edge graph with isolated Carol is a local red-team topology used to demonstrate failure.

The bibliography establishes provenance, not implementation correctness. The local evidence now
has two layers: `proofs/finite_tables.py` emits the parity and transcript-bijection tables accepted
by Metamath, while `tests/test_dining_cryptographers.py` exhausts the S5 knowledge and attack
models. The Python evaluator remains in the disclosed trust base only for the latter layer.
