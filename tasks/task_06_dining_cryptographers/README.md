# Task 6 — Dining Cryptographers Security Demo

Task 6 moves finite epistemic logic from recreational puzzles to a small security protocol. In
Chaum's dining-cryptographers story, either the NSA paid for dinner or exactly one of Alice, Bob,
and Carol did. Three pairwise secret coin flips let the group reveal which case occurred without
revealing which cryptographer paid.

The implementation is a 32-world executable model:

```text
4 payer choices × 2³ shared-coin assignments = 32 worlds
```

Every participant sees their two adjacent coins and whether they personally paid. Eve, the
external observer, initially sees nothing. Alice, Bob, and Carol then reveal one simultaneous
three-bit public transcript; the shared public-announcement semantics removes every world that
would have produced a different transcript.

## What is checked

| Claim | Exhaustive result |
| --- | --- |
| Correctness | In all 32 worlds, transcript parity is odd exactly when a cryptographer paid. |
| Public knowledge | After the transcript, Eve knows whether the NSA or a cryptographer paid. |
| Outsider anonymity | Every cryptographer-paid execution leaves all three diners as Eve's payer candidates. |
| Participant anonymity | A non-payer retains exactly the other two diners as payer candidates. |
| Distribution equality | For Alice, Bob, and Carol, each of the four odd transcripts has multiplicity two. |
| Red-team counterexample | Removing Carol's two shared edges yields six anonymity breaches; Carol is uniquely identified in both worlds where she pays. |

The distribution check is exact counting, not sampling. Under the declared assumption that the
three shared bits are independent and uniform, equal multiplicities are equal transcript
probabilities. The disconnected counterexample is evaluated by the same generic topology model;
the test does not contain a separate attacker oracle.

## Reading the executable essay

Start with [`problem/protocol.md`](problem/protocol.md) for the protocol and bit convention. Then
read `src/proof_lab/tasks/task_06_dining_cryptographers/protocol.py` from top to bottom:

1. `ProtocolTopology` declares which pairs share secret bits.
2. `DiningWorld` records a payer and one value per shared edge.
3. `protocol_model` turns private views into S5 information cells.
4. `run_protocol` announces the complete transcript by finite model restriction.
5. `payer_candidates` projects an information cell onto the security-relevant secret.
6. `transcript_distribution` counts exact transcript multiplicities.
7. `outsider_anonymity_breaches` searches the same claim on good and bad topologies.

[`REFERENCES.md`](REFERENCES.md) identifies Chaum's primary paper and explains which local choices
specialize it. [`reports/security-boundary.md`](reports/security-boundary.md) states what this demo
does and does not certify.

Render the deterministic demo report, then run only its evidence suite with:

```bash
uv run --frozen python -m proof_lab.tasks.task_06_dining_cryptographers
uv run --frozen pytest -q tests/test_dining_cryptographers.py
```

## Evidence level

Task 6 is exhaustive computational certification for two declared finite models. It is not
imported by `proof_lab.build`, and its security claims are not Metamath theorems. Promotion requires
a proof-producing lowering of the finite modal and exact-counting obligations; until then the
Python evaluator remains part of the disclosed trust base.
