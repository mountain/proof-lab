# Task 1 — Propositional Proof Reconstruction

Task 1 tests the formal proof path when the statement, theory, and expected answer are already
known:

```text
formal statement -> proof construction -> lowering -> verifier acceptance
```

## Current proof set

| Proof | Role | Notes |
| --- | --- | --- |
| Double Modus Ponens | Construction | Derives the conclusion from three hypotheses using two MP steps. |
| Modus Tollens | Construction | Uses `con3` and two MP steps. |
| Linearity | Import smoke test | Intentionally references `pm2.521`; it is not a construction benchmark. |

The installed implementations live in
`src/proof_lab/tasks/task_01_textbook/proofs/`. They are loaded from the explicit registry; no
directory or filename glob participates in package verification.

## Planned reference proofs

- Hypothetical syllogism.
- Proof by cases.
- One longer proof with an explicit dependency allowlist and a prohibition on citing the target
  theorem.

## Acceptance direction

The mature task must emit a structured proof trace, complete dependency closure, artifact
manifest, verifier log, and deterministic clean-checkout replay. The current phase preserves the
existing verified examples while establishing the admission boundary.
