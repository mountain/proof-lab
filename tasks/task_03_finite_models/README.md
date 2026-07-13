# Task 3 — Finite Models of Sheridan's Two-Axiom Theory

External ID: `PS-RESEARCH-001`

This Discover task asks whether Sheridan's successor and predecessor axioms have a finite model.
The answer is not known at intake. The work therefore proceeds through reproducible experiments,
conjecture formation, adversarial counterexample search, and formal certification.

The task is quarantined from the formal package build. Nothing in this directory is an admitted
proof merely because it is executable, mathematically plausible, or supported by finite search.

## Research program

1. Lock the object-language signature, the two axioms, and the finite-model convention.
2. Search finite cardinalities and independently validate every candidate structure.
3. State and stress-test the proposed Toggle invariant.
4. isolate the exact finite-cycle lemma needed by the argument.
5. Attempt a certified `NoFiniteModel` result, or record evidence against it.
6. Publish an audited report with exactly one legal outcome.

## Legal outcomes

The closed task must use exactly one of these values:

- `solved`: the original research question has a verifier-accepted certificate at the required
  semantic level.
- `counterexample-found`: an independently checked finite structure refutes the active
  `NoFiniteModel` conjecture.
- `restricted-case-proved`: a verified result holds only for an explicitly narrower statement or
  stronger assumption set; the original question remains open.
- `bounded-frontier-certified`: an exhaustive, replayable search establishes a result only through
  declared finite bounds.
- `inconclusive-but-audited`: the evidence, failed approaches, and remaining obligations are fully
  recorded, but no stronger outcome is justified.

The final manifest also states a normalized result claim so the polarity is unambiguous. A
computationally checked witness or bounded certificate may close its corresponding research
outcome, but only formal certification can admit a theorem to the package build.

The current research phase is tracked separately from the outcome. An open task has no outcome;
terms such as "likely", "probably solved", or "no model found" are not terminal outcomes.

## Metatheory gate

`NoFiniteModel` is a claim about models of Sheridan's object theory. It cannot be certified merely
by proving another formula inside that object theory or by observing UNSAT for finitely many
cardinalities.

The task may report `solved` via `NoFiniteModel` only after a host metatheory formally represents:

- finite structures for the locked signature;
- the satisfaction relation for the object language, or an adequate direct semantics for the two
  locked sentences;
- the finiteness premise;
- satisfaction of both Sheridan axioms; and
- the bridge from the Toggle and finite-cycle lemmas to nonexistence of a finite model.

Until this gate opens, negative search results can justify only `bounded-frontier-certified` or
`inconclusive-but-audited`. A concrete finite model can still justify `counterexample-found` after
an independent checker confirms every axiom instance.

## Directory roles

- `problem/` freezes the research question and semantic boundary.
- `experiments/` records model-search protocols and reproducible runs.
- `conjectures/` records candidate invariants and their refutation history.
- `certificates/` indexes independently checkable witnesses and certificates.
- `proofs/` records formal candidates without admitting them to the package build.
- `reports/` contains the audited outcome report.

Promotion into installed formal proof code is a separate, explicit operation. It requires the
appropriate semantic gate, verifier acceptance, complete evidence, and admission through the
formal task registry.
