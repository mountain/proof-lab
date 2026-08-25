# Proof Lab

Proof Lab is a laboratory for auditable mathematical work built on ProofScaffold, with formal
claims verifier-certified. It organizes work by where uncertainty enters, rather than by how
difficult a theorem appears.

| Task | Workflow | Known at intake | Intended result | Current state |
| --- | --- | --- | --- | --- |
| Task 1 | **Prove** | Statement, theory, and expected answer | Verified proof | Admitted |
| Task 2 | **Formalize** | Source paper and intended conclusion | Verified, auditable formalization | Scaffolded |
| Task 3 | **Discover** | Research question | Certified theorem, counterexample, restricted result, bounded frontier, or audited inconclusion | Quarantined research |
| Task 4 | **Formalize** | Five-hat puzzle and intended answer | Verified propositional core with an explicit epistemic boundary | Admitted |

The progression is an uncertainty chain:

```text
given formal statement, find a proof
    -> determine and formalize a statement from prose
    -> determine the statement, answer, and proof through research
```

The detailed roadmap, phase gates, cross-repository responsibilities, and definitions of done are
in [PROJECT_PLAN.md](PROJECT_PLAN.md).

## Trust boundary

Only tasks explicitly admitted by `proof_lab.registry.PACKAGE_TASK_IDS` can enter the package
build. The registry uses exact builder and proof-function references; it never discovers task code
by scanning filenames.

ProofScaffold 0.0.9 recursively discovers `src/**/build.py`, so
`src/proof_lab/build.py` is deliberately the repository's only build entry point. Tasks on the
same authoring stack may share one exact group-builder reference so their dependency closure is
emitted only once; task-specific adapters use `builder.py` when needed. Draft formalizations,
experiments, solver output, conjectures, holes, and generated artifacts remain outside the formal
build boundary.

## Repository layout

```text
PROJECT_PLAN.md                 project roadmap and engineering gates
tasks/                          durable task records and research evidence
  task_01_textbook/             proof reconstruction
  task_02_sheridan/             paper-to-formalization pipeline
  task_03_finite_models/        research-to-proof pipeline
  task_04_hats/                 small puzzle-to-formalization pipeline
src/proof_lab/
  registry.py                   task catalogue and explicit admission plan
  task_runner.py                read-only registry CLI and build dispatcher
  build.py                      the single ProofScaffold build entry point
  tasks/task_01_textbook/       installed Task 1 implementation
  tasks/task_04_hats/           installed Task 4 implementation
artifacts/                      generated-evidence namespaces
schemas/                        minimal v1 evidence contracts
```

The top-level `tasks/` tree is a record layer. Executable code that must work from an installed
wheel belongs under `src/proof_lab/tasks/`.

## Current tasks

### Task 1 — Prove

Task 1 currently contains:

- Double Modus Ponens, constructed from three hypotheses and two MP steps;
- Modus Tollens, constructed with contraposition and MP;
- Linearity, intentionally retained as a dependency-resolution smoke test rather than a proof-
  construction benchmark.

### Task 2 — Formalize

Task 2 prepares a source-locked and assumption-audited formalization of Flash Sheridan's *A Closer
Look at the Russell Paradox*. Its record tree already separates the source lock, claim ledger,
interpretation decisions, assumption delta, local theory, proofs, and reports. No Task 2 code is
admitted until the source and first-order-logic capability gates pass.

### Task 3 — Discover

Task 3 asks whether Sheridan's two local existence-and-uniqueness axioms have a finite model. It
starts with bounded model search and a candidate toggle invariant. Search results are evidence, not
proofs. A universal `NoFiniteModel` result requires a formal host semantics for finite structures
and satisfaction; without that layer, the strongest admissible negative result is an exact bounded
frontier.

### Task 4 — Formalize

Task 4 formalizes the classic five-hat knowledge puzzle: Alice and Bob successively say that they
do not know their own hat colors, allowing Carol's hat to be determined. The natural-language
epistemic step is recorded as an explicit bridge assumption; the emitted theorem verifies its
propositional consequence without pretending that the current toolchain has a native knowledge
modality.

## Toolchain

- Proof Lab: `0.0.1`
- ProofScaffold: `0.0.9`
- Metamath Prelude: `0.0.5`
- Metamath Logic: `0.0.6`

The lockfile resolves published releases directly. Editable sibling substitutions are not part of
release evidence.

## Setup and validation

From the repository root:

```bash
uv sync --locked --dev
uv run --frozen ruff check .
uv run --frozen mypy .
uv run --frozen python -m pytest
```

Inspect the registry without importing quarantined task implementations:

```bash
uv run --frozen proof-lab-tasks list
uv run --frozen proof-lab-tasks show task_02
```

Run the Task 1 scripts independently:

```bash
uv run --frozen skfd verify src/proof_lab/tasks/task_01_textbook/proofs/double_modus_ponens.py
uv run --frozen skfd verify src/proof_lab/tasks/task_01_textbook/proofs/modus_tollens.py
uv run --frozen skfd verify src/proof_lab/tasks/task_01_textbook/proofs/linearity_import.py
uv run --frozen skfd verify src/proof_lab/tasks/task_04_hats/proofs/five_hat_conclusion.py
```

Run the admitted package build with strict interfaces and declared coverage:

```bash
uv run --frozen skfd verify proof-lab --level 1 --coverage declared
```

The desired future interface is `skfd verify proof-lab:task_01` and
`skfd verify proof-lab:all`. ProofScaffold 0.0.9 does not yet support namespaced task targets, so
the package build currently executes the explicit admission tuple, which contains Tasks 1 and 4.

## Development rule

Adding a task directory does not admit a task. Admission requires an installed builder, an
explicit registry record, an explicit entry in `PACKAGE_TASK_IDS`, and all applicable plan gates.
Do not add another `build.py`, import research code from the package builder, or consume generated
artifacts as proof inputs.
