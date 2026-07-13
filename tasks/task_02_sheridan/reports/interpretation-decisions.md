# Interpretation Decisions

Status: Provisional until the primary sources are locked and compared.

This is an append-only decision log. Each accepted entry must cite the locked source, list affected
claims, state alternatives, and define a revisit condition.

## ID-001 — Relation-first successor and predecessor

- **Decision:** Use `Succ(x, y)` and `Pred(x, y)` as relations in the core formalization.
- **Reason:** This exposes existence and uniqueness obligations without requiring function symbols
  or definite descriptions in the first vertical slice.
- **Consequence:** Function notation is an optional elaboration, not part of minimum acceptance.
- **Status:** Accepted for project planning; confirm against the source lock.

## ID-002 — Upper ranges over all objects

- **Decision:** Interpret the displayed upper condition as `forall z. z notin z -> z in x`, without
  inserting `set(z)`.
- **Reason:** The formal formula summarized for the task does not contain the prose-level set
  restriction.
- **Consequence:** The prose/formula difference must remain visible in the report and claim ledger.
- **Status:** Proposed; source comparison required.

## ID-003 — Coextensiveness is not equality

- **Decision:** Define coextensiveness by pointwise membership equivalence and omit Extensionality
  from the core theory.
- **Reason:** Object equality is stronger than the displayed membership equivalence.
- **Consequence:** No fixed-point equality may be inferred from coextensiveness without a separately
  admitted bridge assumption.
- **Status:** Accepted.

## ID-004 — Unique existence encoding

- **Decision:** Undecided between native unique existence and separate existence/uniqueness axioms.
- **Acceptance rule:** Select exactly one representation after the FOL capability audit. Record the
  choice in the manifest and expose the exact local axiom allowlist.
- **Status:** Open.

## ID-005 — Explosion must be visible

- **Decision:** Every M5 fixed-point or equality proof records `direct`, `extensional`, or
  `ex_falso` mode. `StrictContradiction` followed by explosion may not be described as a nontrivial
  approximation-stopping proof.
- **Status:** Accepted.

## ID-006 — Function notation is deferred

- **Decision:** Do not introduce `succ(x)` or `pred(x)` in the first accepted formalization.
- **Revisit condition:** Relation-based M4 is verified and the upstream authoring layer has a clear
  unique-description contract.
- **Status:** Accepted.

## ID-007 — M4 link definitions are mandatory

- **Decision:** Treat `LowerAscendingLink` and `UpperDescendingLink` as mandatory M4 definitions.
- **Reason:** The existential improvement-step fidelity claims need stable predicates rather than
  duplicating their conjunctions inline.
- **Status:** Accepted.

## ID-008 — Extensionality experiments use a separate profile

- **Decision:** Any coextensiveness-to-equality bridge is isolated in a separate theory profile,
  dependency closure, and artifact namespace.
- **Reason:** Extensionality is outside the two-axiom core and cannot silently alter core M5.
- **Status:** Accepted.
