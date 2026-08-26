# Task 6 — Dining Cryptographers Security Demo

[中文说明：协议历史、有限模型、Metamath 证明与证据边界](README.zh-CN.md)

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

## What is proved and what is checked

| Claim | Evidence | Result |
| --- | --- | --- |
| Correctness table | Metamath theorem `dc_parity_table` | All 32 rows prove odd parity exactly when a cryptographer paid. |
| Payer bijection table | Metamath theorem `dc_payer_bijection_table` | All 24 shared-edge-toggle rows preserve the complete transcript. |
| Public knowledge | Exhaustive S5 model | After the transcript, Eve knows whether the NSA or a cryptographer paid. |
| Outsider anonymity | Formal bijection table + S5 projection | Every cryptographer-paid execution leaves all three diners as candidates. |
| Participant anonymity | Exhaustive S5 model | A non-payer retains exactly the other two diners as payer candidates. |
| Distribution equality | Formal bijection table + exact counting | Each of the four odd transcripts has multiplicity two for every diner. |
| Red-team counterexample | Exhaustive bad-topology model | Isolating Carol yields six breaches; both Carol-paid worlds identify her. |

The distribution check is exact counting, not sampling. Under the declared assumption that the
three shared bits are independent and uniform, equal multiplicities are equal transcript
probabilities. The disconnected counterexample is evaluated by the same generic topology model;
the test does not contain a separate attacker oracle.

## Reading the proof and the executable essay

The actual proof constructors are in
`src/proof_lab/tasks/task_06_dining_cryptographers/proofs/finite_tables.py`. They contain no `raw`
steps and no protocol-specific hypotheses. Each Boolean leaf is represented conservatively by the
theorem `φ → φ` or its negation; each XOR node is derived from `df-xor` and ordinary propositional
lemmas. The two root labels are admitted through `PACKAGE_TASK_IDS` and checked by `mmverify`.

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
uv run --frozen skfd verify proof-lab --level 1 --coverage declared
```

## Evidence level

Task 6 now has mixed evidence. Its 32-row correctness table and 24-row transcript-bijection table
are Metamath theorems. Knowledge, public-model restriction, candidate-set projection, exact finite
counting, and the disconnected attack still use the disclosed Python evaluator. A proof-producing
modal lowering remains the next promotion gate; passing the two table proofs does not silently
promote those epistemic claims.
