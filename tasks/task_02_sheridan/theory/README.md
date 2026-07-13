# Local Theory Scaffold

The future installed implementation will define, in deterministic order:

```text
syntax
definitions
local axioms
M1 lemmas
M2 lemmas
M3 lemmas
M4 theorems
M5 classified theorems
```

Planned definitions include `NonSelfMembered`, `Lower`, `Upper`, `StrictRussellian`, `Succ`,
`Pred`, `Coextensive`, `AscendingLink`, `DescendingLink`, and their lower/upper refinements.

The local axiom allowlist is exactly two native unique-existence axioms, or exactly four expanded
existence/uniqueness axioms. The two encodings must not be enabled simultaneously.

No Python theory module is present yet. Creating one is blocked by the source, interpretation, and
released FOL capability gates described in `PROJECT_PLAN.md`.
