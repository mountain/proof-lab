# Task 2 — Sheridan Paper to Formalization

External ID: `PS-PAPER-001`

This task extracts and verifies the formal core of Flash Sheridan's *A Closer Look at the Russell
Paradox*. Its purpose is to test a paper-to-proof transaction, not merely to reproduce a theorem
whose formal statement has already been supplied.

The task is scaffolded but not admitted to the package build.

## Formalization scope

The intended scope is Sections 2–6. Classical first-order logic with equality is imported from the
released ProofScaffold stack. This task must not implement a private FOL substrate.

The signature uses membership from the audited FOL substrate when available and adds a local `set`
predicate. The ownership decision is locked during the FOL capability audit. The only intended
local non-definitional assumptions are successor and predecessor existence-and-uniqueness:

```text
Succ(x, y) := set(y) and forall z. z in y iff (z in x or z = x)
Pred(x, y) := set(y) and forall z. z in y iff (z in x and z != x)
```

The first implementation is relation-based. Function notation for `succ(x)` and `pred(x)` is an
optional later elaboration.

## Evidence before proof

Proof implementation is blocked until these records are complete:

- `source/source.lock.json` locks the exact formalization source bytes and section scope;
- `claims/claims.yaml` maps source claims to stable local claims;
- `reports/interpretation-decisions.md` records every material interpretation;
- `reports/assumption-delta.json` distinguishes paper assumptions, imported logic, formalizer
  additions, and deliberate omissions.

The published article and arXiv v5 are not assumed to be textually identical. Their relevant formal
statements must be compared after both sources are available.

## Milestones

### M1 — Russellian definitions

- `LowerSelf`: `Lower(x) -> x notin x`.
- `UpperSelf`: `Upper(x) -> x in x`.
- Lower and upper are incompatible.

### M2 — Relation basics

- `PredNoSelf`: `Pred(x, y) -> x notin y`.
- `SuccHasSelf`: `Succ(x, y) -> x in y`.

### M3 — Improvement lemmas

- `LowerSuccDistinct`.
- `LowerSuccLower`.
- `UpperPredDistinct`.
- `UpperPredUpper`.
- `UpperPredInUpper`.

### M4 — Approximation process

M4 distinguishes pointwise incompatibility from the existential theorem and includes both
conditional links and existential fidelity claims:

```text
not exists x. (Lower(x) and Upper(x))
Lower(x) -> exists y. LowerAscendingLink(x, y)
Upper(x) -> exists y. UpperDescendingLink(x, y)
```

`LowerAscendingLink` and `UpperDescendingLink` are mandatory M4 definitions. The existential claims
connect the paper's process language to the two local existence axioms.

### M5 — Russell paradox restated

- Strict Russellian implies lower.
- Strict Russellian implies upper.
- Strict Russellian implies contradiction.
- Optional coextensive or fixed-point consequences are classified by proof mode.

## Coextensiveness and equality

The theory must define:

```text
Coextensive(x, y) := forall z. (z in x iff z in y)
```

Coextensiveness is not equality. A coextensive consequence is a task-added weakening of the
paper's equality statement and must be classified that way. Extensionality is deliberately omitted
from the core theory. Any equality-bridge experiment uses a separate theory profile, dependency
closure, and artifact namespace; it cannot count toward core M5.

Because `StrictRussellian(r)` is contradictory in classical logic, any equality follows under that
antecedent by explosion. A fixed-point proof must carry one of these modes in its trace:

```text
direct
extensional
ex_falso
```

The report must not describe an ex-falso equality as a nontrivial formalization of an approximation
process stopping. CI derives or checks the proof mode from the actual dependency closure: `direct`
excludes contradiction elimination and Extensionality, `extensional` uses the separate bridge
profile, and `ex_falso` depends on contradiction elimination.

## Forbidden hidden assumptions

- Unrestricted Comprehension or abstraction.
- Separation.
- Foundation.
- Extensionality.
- Class Theory.
- ZF, NBG, NF, or an equivalent stronger set theory.
- Every object is a set.
- Successor and predecessor are inverses.

If a generic predicate-logic capability is missing, work stops at an upstream capability gate. The
task must not work around the gap by smuggling a stronger axiom into the local theory.
