# Proof Lab Project Plan

- Status: Active
- Plan version: 1
- Last updated: 2026-07-13
- Current checkpoint: Phase 0 repository skeleton implemented; Phase 1 evidence work is not started.

## 1. Mission

Proof Lab is a task laboratory for three forms of auditable mathematical work. Formal claims are
verifier-certified; research frontiers and inconclusive results instead carry an explicit evidence
level. The tasks are not ordered by theorem difficulty. They are ordered by where uncertainty
enters the workflow.

| Workflow | Known at intake | Primary work | Required outcome |
| --- | --- | --- | --- |
| **Task 1 — Proof** | Statement, theory, and expected answer | Construct and verify a proof | Verifier-accepted proof |
| **Task 2 — Formalize** | Source document and intended conclusion | Extract the theory, resolve ambiguity, audit assumptions, and prove the formal claims | Source-locked, assumption-audited, verifier-accepted formalization |
| **Task 3 — Discover** | Research question | Experiment, form conjectures, find counterexamples or proofs, and certify the result | Theorem, counterexample, restricted result, bounded frontier, or audited inconclusion |

The progression is:

```text
given formal statement, find a proof
    -> determine and formalize a statement from prose
    -> determine the statement, answer, and proof through research
```

The project succeeds only if it preserves the difference between these workflows. A model
search is not a proof, an interpretation decision is not a logical axiom, and an unfinished
research candidate is not a package build input.

## 2. Trust and Admission Boundary

The following rules are non-negotiable:

1. Metamath verifier acceptance is the final formal authority.
2. Python builders, paper parsers, LLM output, model finders, SAT/SMT solvers, and conjecture
   generators are untrusted evidence producers.
3. Only tasks explicitly admitted by the Python task registry may enter
   `src/proof_lab/build.py`.
4. Draft formalizations, holes, failed proofs, experiments, conjectures, and solver output must
   remain outside the formal build allowlist.
5. Generated artifacts are outputs. They must never be consumed as trusted proof inputs.
6. Raw or unsupported proof steps must not be silently emitted as axioms.
7. Promotion from research or formalization draft to formal build input requires an explicit
   status change, a complete evidence record, and all applicable verification gates.

`all` always means all **admitted and build-ready** tasks. It never means every directory in the
repository.

Proof Lab distinguishes three evidence levels:

1. **Formal certification** — a Metamath artifact is accepted by the required verifier set. This
   is required for theorem admission and for any result described as formally proved.
2. **Computational certification** — a finite witness, exhaustive enumeration, or proof-producing
   solver certificate is checked independently under a disclosed encoding and checker trust base.
   This may close a computational research outcome, but it is not a formal theorem.
3. **Exploratory evidence** — raw searches, heuristic solver output, LLM proposals, and unchecked
   proof candidates. These may guide research but cannot justify `solved`,
   `counterexample-found`, `restricted-case-proved`, or `bounded-frontier-certified`.

Every report and artifact manifest states its evidence level. Promotion can only preserve or
increase that level; it may never relabel computational evidence as formal certification.

## 3. Repository Architecture

The bootstrap architecture is:

```text
proof-lab/
  PROJECT_PLAN.md
  README.md

  tasks/
    task_01_textbook/
      task.yaml
      README.md
      proofs/

    task_02_sheridan/
      task.yaml
      README.md
      source/
      claims/
      theory/
      proofs/
      reports/

    task_03_finite_models/
      task.yaml
      README.md
      problem/
      experiments/
      conjectures/
      certificates/
      proofs/
      reports/

  src/proof_lab/
    registry.py
    task_runner.py
    build.py
    tasks/
      task_01_textbook/
        builder.py
        proofs/

  artifacts/
    task_01/
    task_02/
    task_03/

  schemas/
    README.md
```

The top-level `tasks/` tree owns task records, source evidence, research state, and reports.
Executable Python that must survive wheel installation lives under `src/proof_lab/tasks/`.
The task manifest links the record tree to its installed implementation.

### 3.1 Build-entrypoint constraint

ProofScaffold 0.0.9 discovers files named `build.py` recursively below `src/`. Therefore:

- `src/proof_lab/build.py` is the only Proof Lab build entrypoint;
- task implementations use `builder.py`, never task-local `build.py`;
- Task 2 and Task 3 records do not contain importable build hooks until they are admitted;
- the root build delegates only to builder references listed in `proof_lab.registry`.

This constraint prevents a draft task from becoming a formal unit merely because a file was
added to the repository.

### 3.2 Registry contract

Each registered task has:

- a stable task ID;
- a workflow kind: `proof`, `formalize`, or `discover`;
- a lifecycle status;
- a manifest path;
- an artifact namespace;
- an optional installed builder reference;
- optional explicit proof-function and expected-theorem references.

The registry is the executable admission boundary. A separate `PACKAGE_TASK_IDS` tuple is the
explicit release plan and must never be derived from task status. YAML manifests are evidence
records and must eventually validate against a versioned schema, but editing YAML alone must never
enable code.

The desired future CLI is:

```text
skfd verify proof-lab:task_01
skfd verify proof-lab:task_02
skfd verify proof-lab:task_03
skfd verify proof-lab:task_04
skfd verify proof-lab:all
```

ProofScaffold does not yet provide this target namespace. Until it does, package verification
builds the registry's default admitted tasks, currently Tasks 1 and 4. Tasks that share a builder
reference are passed to that builder as one ordered group, preventing duplicate emission of their
common logic-catalogue closure. The project must not introduce an environment-variable selector
into release builds because that would make the same package input produce different formal units.

## 4. Dependency Ownership

The dependency direction is fixed:

```text
proof-scaffold
      ^
metamath-prelude
      ^
metamath-logic
      ^
proof-lab
```

### 4.1 Proof Scaffold

Proof Scaffold owns generic mechanisms:

- authoring IR and its public query API;
- builders, linker, relocation, and verifier integration;
- task-target selection when it becomes generic;
- structured proof traces and dependency closure;
- artifact metadata and deterministic serialization;
- fail-closed handling of holes and unsupported proofs.

It must not import Prelude, Logic, Sheridan theory, or Proof Lab task code.

### 4.2 Metamath Prelude

Prelude owns foundation-level vocabulary and syntax:

- typecodes and canonical variables;
- minimal foundation syntax and floating-hypothesis ownership;
- generic foundation objects needed by every downstream logic.

It must not contain Sheridan-specific predicates, local set axioms, finite-model concepts, or
research state.

### 4.3 Metamath Logic

Logic owns reusable mathematical logic:

- classical propositional logic;
- first-order quantification and binding;
- equality, substitution, and capture constraints;
- reusable predicate-logic lemmas;
- public assertion signatures needed by downstream authoring.

Generic missing FOL capabilities discovered by Task 2 belong here. `Lower`, `Upper`, `Succ`,
`Pred`, the two Sheridan axioms, and all finite-model claims remain local to Proof Lab.

### 4.4 Proof Lab

Proof Lab owns:

- task manifests and admission state;
- paper locks, claim ledgers, interpretation decisions, and assumption deltas;
- local theories and task-specific axioms;
- experiments, conjectures, witnesses, certificates, and research reports;
- admitted proofs that exercise the upstream stack.

Research mechanisms should mature here first. Only stable and domain-independent mechanisms move
upstream.

## 5. Common Task and Artifact Contract

Every task eventually produces an `artifact-manifest.json` with:

- task ID, workflow kind, schema version, and outcome;
- source Git revision and dirty-state flag;
- exact dependency versions and `uv.lock` digest;
- normalized statement and admitted assumptions;
- executed commands and tool versions;
- output paths and SHA-256 digests;
- an evidence-level declaration;
- formal verifier identity, result, and log digest when a formal claim is present;
- experiment, witness, or certificate evidence when a computational claim is present;
- direct and transitive dependency closure;
- proof trace or experimental evidence references;
- source and provenance references where applicable.

The manifest uses typed optional sections. `formal_verification` is mandatory for admitted proof
claims but absent for a purely audited inconclusion. `computational_certification` records the
encoding, checker trust base, and certificates for bounded or witness-based research outcomes.

The shared evidence model distinguishes:

```text
source records       what the task received
claim ledger         what the task intends to establish
draft IR             what authoring currently contains, including holes
elaborated IR        what has been resolved and typechecked
lowered proof        what is submitted to Metamath
proof trace          how the admitted claim was actually derived
artifact manifest    what was run, verified, and hashed
```

The claim ledger is an input commitment. The proof trace is generated evidence. CI must join the
two and reject missing claims, undeclared emitted assertions, statement mismatches, and hidden
axioms.

### 5.1 Authoring API requirement

Proof Lab tasks need a versioned public authoring representation suitable for human tools and LLM
authors. The intended API exposes immutable language, assertion, term, and proof structures using
stable qualified references. It must not expose runtime `SymbolId`, interners, builtins objects, or
Python callables as durable identities.

The API must support:

- assertion, term, proof-step, and source-span lookup;
- dependency and dependent queries;
- symbol and sort queries;
- canonical, Unicode, and LaTeX rendering;
- deterministic JSON serialization;
- draft holes for inspection, while rejecting holes during lowering and release.

This is an upstream ProofScaffold dependency, not a reason to create a second private IR in Proof
Lab.

The public stage contract has three APIs and a final runtime binding step:

```text
Source IR
    spelling, unresolved references, source occurrences, provenance, and holes
        -> Elaborated IR
           typed normalized expressions, resolved assertion IDs, explicit substitutions,
           explicit step results, and a proof DAG
               -> Metamath Lowered IR
                  canonical ASCII string keys and verifier-order/RPN structure
                      -> runtime SymbolId binding and emitted Metamath
```

Each transition produces structured diagnostics and a provenance map. Cross-version stability is
promised only for explicit symbol and assertion declaration IDs. Stable semantic identities must
be separate from source occurrences: a shared term can have one normalized identity and many
human- or LLM-authored spans. Automatically generated node or step IDs are occurrence identities;
tools that need persistent step references may supply explicit step keys.

Human and LLM authors use the same semantics but need different affordances. Human tools need
Unicode and LaTeX rendering, navigable dependencies, and compact local errors. LLM tools need
schema discovery, typed constructors, bounded patch operations, explicit goal states, machine-
readable diagnostics, deterministic serialization, and transaction-style validation before a
change is committed. Neither author should manipulate serialized Metamath strings as the primary
authoring model.

The API therefore exposes inspectable drafts but keeps lowering fail-closed: unresolved holes,
ambiguous references, unstated assumptions, unsupported constructors, and stale semantic digests
block formal emission.

LaTeX renderers and LLM-context generators consume Elaborated IR. LaTeX notation is presentation
metadata. An LLM message is a deterministic semantic projection, not a trusted proof artifact; any
LLM response re-enters Source IR, elaboration, and verification.

### 5.2 Authoring simplification target

The authoring surface should converge on one declarative `AuthoringBundle` per theory or task. A
bundle declares imports, notation, definitions, assumptions, theorem roots, proof DAGs, provenance,
and artifact policy. The shared pipeline performs:

```text
register -> elaborate -> validate -> lower -> link -> verify -> publish evidence
```

Task builders should eventually register bundles, not reproduce catalogue closure, external-label
aliases, floating-variable maps, or verifier plumbing. The current shared propositional group
builder is a ProofScaffold 0.0.9 compatibility adapter and a concrete list of upstream
simplification pressure, not the desired long-term public API.

The framework avoids two parallel authoring systems. Humans and LLMs use the same typed operations,
transactions, and semantic IDs; presentation, context selection, and diagnostics differ at the
tooling edge. Reflection-based discovery and filename conventions are replaced by explicit
declarations that can be validated before imports or lowering occur.

## 6. Task 1 — Proof Reconstruction

### 6.1 Purpose

Task 1 answers:

> Given a formal theory, a formal statement, an expected answer, and an allowed dependency set,
> can ProofScaffold construct and verify a nontrivial proof?

It tests proof construction, dependency resolution, lowering, relocation, and verifier acceptance.
It does not test prose interpretation or open-ended research.

### 6.2 Initial examples

The existing examples become the first registered Task 1 proof set:

1. Double Modus Ponens — proof construction from hypotheses.
2. Modus Tollens — derived proof using contraposition and modus ponens.
3. Linearity import smoke test — deliberate dependency-resolution test, not a proof-construction
   benchmark.

Planned additions are hypothetical syllogism and proof by cases. At least one reference proof must
eventually satisfy all of the following:

- the target theorem may not be directly referenced;
- only an explicit lemma allowlist may be used;
- the complete dependency closure is emitted;
- a step-level proof trace is produced;
- a clean replay is deterministic.

### 6.3 Task 1 completion

Task 1 is complete when the expected theorem is emitted, the proof passes level-1 linking and an
independent verifier, and the artifact manifest, trace, closure, maps, logs, and digests are
complete.

## 7. Task 2 — Sheridan Paper to Formalization

Task ID: `PS-PAPER-001`

Working title: *Sheridan Incomprehensive Set Theory and the Russell Paradox*

### 7.1 Scope and non-negotiable boundaries

The task formalizes the mathematical core of Sections 2–6. Classical first-order logic with
equality is imported as substrate and is not reimplemented here.

The local signature uses membership from the audited FOL substrate when available and adds the
local `set` predicate. Phase 2 fixes symbol ownership explicitly. The theory's only local non-
definitional assumptions are the recorded successor and predecessor existence-and-uniqueness
axioms.

The dependency closure must not silently add:

- unrestricted Comprehension or abstraction;
- Separation;
- Foundation;
- Extensionality;
- Class Theory;
- ZF, NBG, NF, or an equivalent stronger set theory;
- an assumption that every object is a set.

The relation representation is primary:

```text
Succ(x, y) := set(y) and forall z. z in y iff (z in x or z = x)
Pred(x, y) := set(y) and forall z. z in y iff (z in x and z != x)
```

Function symbols `succ(x)` and `pred(x)` are optional later elaborations.

When Task 2 becomes executable, installed code will live under:

```text
src/proof_lab/tasks/task_02_sheridan/
  builder.py
  theory/
  proofs/
```

The source, claim, interpretation, and report records remain under top-level
`tasks/task_02_sheridan/` and are never imported as executable build hooks.

The selected layout is an intentional reinterpretation of the original Task 2 proposal:

| Original deliverable | Proof Lab location |
| --- | --- |
| `theories/sheridan_russell/` | specification in `tasks/task_02_sheridan/theory/`; admitted implementation in `src/proof_lab/tasks/task_02_sheridan/` |
| `generated/sheridan_russell/` | `artifacts/task_02/` |
| task document | `tasks/task_02_sheridan/README.md` and `task.yaml` |
| formalization report | `tasks/task_02_sheridan/reports/` |

### 7.2 Required scholarly artifacts

Task 2 treats the following as first-class inputs:

1. `source/source.lock.json` — exact source version, byte digest, locator convention, and scope.
2. `claims/claims.yaml` — source-to-formal claim ledger.
3. `reports/interpretation-decisions.md` — append-only interpretation decisions.
4. `reports/assumption-delta.json` — paper assumptions, imported logic, additions, and omissions.

The published article and arXiv v5 must not be treated as silently identical. The published edition
is the bibliographic and numbering authority; an exact source may be used as the formalization
basis only after its bytes are locked and the relevant sections are compared.

No proof implementation begins while the primary formalization source digest is a placeholder.

### 7.3 Formalization milestones

The relation-based acceptance surface is explicit:

- **M1:** `LowerSelf`, `UpperSelf`, and pointwise `NoStrictByLowerUpper`:
  `forall x. not (Lower(x) and Upper(x))`.
- **M2:** `PredNoSelf` and `SuccHasSelf`.
- **M3:** `LowerSuccDistinct`, `LowerSuccLower`, `UpperPredDistinct`, `UpperPredUpper`, and
  `UpperPredInUpper`.
- **M4:** existential `NoLowerUpperIntersection`, `LowerAscendingStep`,
  `UpperDescendingStep`, `LowerHasAscendingStep`, and `UpperHasDescendingStep`.
- **M5 core:** `StrictImpliesLower`, `StrictImpliesUpper`, and `StrictContradiction`.

`LowerAscendingLink` and `UpperDescendingLink` become mandatory definitions for M4. This decision
makes the two existential fidelity claims stable rather than duplicating their conjuncts inline.

The exact M3–M5 core statements are:

```text
Lower(x) and Succ(x, y) -> y != x
Lower(x) and Succ(x, y) -> Lower(y)
Upper(x) and Pred(x, y) -> y != x
Upper(x) and Pred(x, y) -> Upper(y)
Upper(x) and Pred(x, y) -> y in x

not exists x. (Lower(x) and Upper(x))
Lower(x) and Succ(x, y) -> LowerAscendingLink(x, y)
Upper(x) and Pred(x, y) -> UpperDescendingLink(x, y)
Lower(x) -> exists y. LowerAscendingLink(x, y)
Upper(x) -> exists y. UpperDescendingLink(x, y)

StrictRussellian(r) -> Lower(r)
StrictRussellian(r) -> Upper(r)
StrictRussellian(r) -> false
```

M4 must include the existential fidelity claims:

```text
Lower(x) -> exists y. LowerAscendingLink(x, y)
Upper(x) -> exists y. UpperDescendingLink(x, y)
```

Conditional link theorems alone do not express the paper's claim that every approximation has an
improvement step.

### 7.4 Coextensiveness, equality, and explosion

For optional M5 analysis, the task defines:

```text
Coextensive(x, y) := forall z. (z in x iff z in y)
```

Coextensiveness is not object equality. A claim replacing the paper's equality with
coextensiveness is recorded as a task-added weakened consequence; it does not establish the
paper's equality statement. The core task omits Extensionality.

Any experiment adding a coextensiveness-to-equality bridge uses a separate theory profile,
dependency closure, and artifact namespace. It cannot alter the core Sheridan theory or count
toward core M5 completion.

`StrictRussellian(r)` is contradictory in classical logic. Therefore any equality under that
antecedent is available by explosion. A fixed-point proof records one of these modes, which CI
checks against the actual dependency closure:

- `direct` — depends on neither `StrictContradiction`/explosion nor an Extensionality bridge;
- `extensional` — depends on the separately admitted bridge profile;
- `ex_falso` — depends on contradiction elimination.

The fixed-point portion of the paper must not be presented as a nontrivial stopping argument when
its only dependency is `StrictContradiction` followed by explosion. Proof traces must expose any use
of ex falso.

### 7.5 Task 2 completion levels

- **Minimum accepted:** M1 and M2 verified, with all scholarly artifacts and the formalization
  report complete.
- **Complete:** M4 verified, including the existential improvement-step fidelity claims.
- **Extended:** core M5 verified with proof modes and assumptions classified. Function notation, if
  attempted, is a separate optional extension and does not change the relation-based core.

## 8. Task 3 — Research to Proof

Task ID: `PS-RESEARCH-001`

Research question: *Do Sheridan's two local axioms have a finite model?*

### 8.1 Outcome model

A research task may close with exactly one of:

- `solved`;
- `counterexample-found`;
- `restricted-case-proved`;
- `bounded-frontier-certified`;
- `inconclusive-but-audited`.

The last outcome is valid when the explored space, failed conjectures, surviving hypotheses, and
remaining obligations are all explicit. Research status such as `exploring` or `candidate` is not a
closed outcome.

Outcome names do not hide their certification basis:

| Outcome | Minimum certification |
| --- | --- |
| `solved` | Formal certification of the original result at the required semantic level |
| `counterexample-found` | Canonical finite witness checked independently against the locked semantics; formalization is required before theorem admission |
| `restricted-case-proved` | Formal certification of the changed statement plus a complete assumption delta |
| `bounded-frontier-certified` | Replayable exhaustive enumeration or independently checkable UNSAT certificate, together with a validated encoding and exact bounds |
| `inconclusive-but-audited` | Complete and reproducible audit; it makes no new mathematical claim |

An ordinary solver `UNSAT` line is exploratory evidence. It cannot support
`bounded-frontier-certified` unless the proof certificate or exhaustive coverage is independently
checkable and the translation from the locked axioms to the search encoding is validated.

Because generic outcome names do not encode polarity, the final manifest also carries a normalized
`result_claim`. For this task it states exactly one of: a finite model exists, no finite model
exists, a named restriction holds, no model exists for the enumerated sizes, or no mathematical
conclusion is claimed.

### 8.2 Candidate toggle argument

First define a relation `Toggle(x, y)` by choosing the predecessor case when `x in x` and the
successor case when `x not in x`. Prove totality and uniqueness before introducing host-level
function notation `t(x)`; no choice principle is assumed.

For a structure `M` with finite domain `D`, `Ext_M(x)` is meta-level notation for
`{z in D | M satisfies z in x}`. It is not an object-language set term. The intended invariant is:

```text
Ext(t(x)) = Ext(x) symmetric-difference {x}
```

In a finite nonempty model, the collection of all objects satisfying `set` is nonempty and closed
under `t`, so iteration enters a cycle. Nonemptiness is derived by choosing an object from the
nonempty domain and applying the successor axiom, whose output satisfies `set`; it is not added as
another object-theory axiom. Traversing a simple cycle would toggle one distinct coordinate at each
step, apparently preventing the extension from returning to its starting value.

This is a conjectural proof program, not an admitted theorem. It must audit:

- totality and uniqueness of `t` on set objects;
- the standard nonempty-domain convention and the derivation of a set object;
- distinctness of nodes on a minimal cycle;
- the pointwise membership form of the symmetric-difference argument;
- why object-theory Extensionality is unnecessary, while separately auditing any host-level
  extensional equality of semantic subsets or functions;
- the exact host formalism used for finite structures and satisfaction.

### 8.3 Research stages

1. **R1 — Semantics and finite-model search**
   - Lock the signature, axioms, equality semantics, nonempty-domain convention, and finite-model
     encoding.
   - Search declared sizes with deterministic configurations.
   - Independently check every model witness.
   - For negative bounds, require a checked UNSAT certificate, replayable exhaustive enumerator, or
     formal bound-specific proof.
   - Validate equality-as-identity, quantifier expansion, uniqueness encoding, assignment-to-
     structure correspondence, and the satisfiability preservation of any symmetry breaking.
   - Retain encodings, seeds, bounds, raw results, and certificates.

2. **R2 — Toggle invariant**
   - Define `SetObject`, `Toggle`, and extension equivalence.
   - Counterexample-test the candidate invariant.
   - Verify totality, uniqueness, exact-coordinate change, and distinctness obligations.

3. **R3 — Finite-cycle argument**
   - Formalize the required finite functional-graph lemma.
   - Formalize the contradiction produced by an exact-coordinate toggle around a simple cycle.

4. **R4 — Main result or bounded frontier**
   - Produce either a certified finite countermodel, a formally certified no-finite-model theorem,
     a restricted result, or exact bounded UNSAT evidence.

5. **R5 — Research report**
   - Record the problem, initial hypotheses, experiments, failed conjectures, surviving invariant,
     formal evidence, remaining assumptions, and novelty status.

### 8.4 Metatheory gate

`NoFiniteModel` is a model-theoretic metatheorem. It is not an object-theory theorem of Sheridan's
first-order axioms.

Before the outcome may be `solved`, the project must select and lock a host formalization of:

- finite domains;
- first-order structures;
- interpretation of the signature;
- satisfaction of formulas;
- the connection between the encoded axioms and the searched structures.

The first acceptable host may be a Task 3-local ProofScaffold/Metamath semantics record containing
finite `D`, `set`, membership, and direct satisfaction fields for the two sentences. A full generic
FOL syntax-and-satisfaction development is optional, but the local record must prove adequacy to
the locked FOL sentences before the report says "no finite FOL model." If the metatheory is kept in
an external proof assistant or ordinary program, it is external evidence and cannot satisfy the
current formal `solved` gate.

Generic finite functional-graph mathematics does not belong automatically in Metamath Logic. It
starts task-local and moves upstream only after a separate ownership review identifies a reusable
mathematics package.

Without this semantics layer, exhaustive UNSAT searches for sizes `1..N` can establish only
`bounded-frontier-certified`, never a universal no-finite-model theorem.

## 9. Engineering Phases

### Phase 0 — Task laboratory skeleton

Deliver:

- minimal v1 task, source-lock, claim-ledger, artifact, and research-outcome schemas;
- explicit Python task registry and runner;
- Task 1 implementation moved into the installed package;
- no root `prove_*.py` glob discovery;
- Task 2 and Task 3 quarantined record trees;
- common plan and artifact layout;
- tests for registry admission behavior.

Exit gate: incomplete Task 2/3 material cannot affect `skfd verify proof-lab`.

### Phase 1 — Task 1 reference vertical slice

Deliver:

- normalized statement locks and explicit dependency allowlists;
- one nontrivial proof that cannot cite its target theorem;
- structured proof traces and dependency closure;
- deterministic replay and artifact manifests.

Exit gate: every Task 1 proof passes the common formal gates from a clean checkout.

### Phase 2 — FOL readiness across repositories

Audit released Prelude and Logic for:

- quantifiers and binder ownership;
- capture-safe substitution;
- equality rules;
- relation definitions;
- unique existence or its explicit expansion;
- required classical predicate-logic lemmas;
- public assertion signatures and authoring IR access.

Generic gaps are implemented upstream. Sheridan-specific code is not.

Exit gate: a small task-local predicate theory verifies without private FOL machinery in Proof Lab.

### Phase 3 — Task 2 source and interpretation lock

Deliver:

- final source lock and section comparison;
- complete initial claim ledger;
- interpretation decisions;
- assumption delta;
- selected unique-existence encoding;
- exact local axiom allowlist;
- packaging and namespace decision.

Exit gate: all source digests and claim locators are populated, and every substrate capability is
either available or recorded as an upstream blocker.

### Phase 4 — Task 2 verified core

Deliver M1 and M2 as genuine verified proofs, plus traces, closures, maps, logs, and a complete
formalization report for the accepted M1–M2 surface.

Exit gate: no raw fallback, no hidden local axioms, and no forbidden foundation in transitive
closure.

### Phase 5 — Task 2 completion

Deliver M3 and M4. Generate the complete core formalization report and artifact manifest.

Exit gate: M4 is verifier-accepted; paper mapping, proof modes, interpretation choices, and
assumption deltas agree with generated evidence.

### Phase 6 — Task 2 extension

Deliver the classified core M5 results. Function-notation elaboration, if pursued, is a separate
optional extension and does not change the relation-based core.

Exit gate: every fixed-point consequence declares `direct`, `extensional`, or `ex_falso`; all
equality bridges and uses of explosion are visible in the generated dependency evidence.

### Phase 7 — Task 3 research infrastructure

Deliver:

- versioned experiment and outcome schemas;
- deterministic bounded model search;
- independent witness checker;
- conjecture and counterexample ledgers;
- immutable run records;
- explicit promotion records.

Exit gate: experiments are reproducible and cannot enter the formal build without promotion.

### Phase 8 — Task 3 research execution and certification

Execute the locked research protocol, retain failed and revised conjectures, and deliver one legal
closed outcome. The toggle invariant, finite-cycle route, and metatheory proof are attempted
research directions, not mandatory conclusions: a checked countermodel or an audited failure may
supersede them.

Exit gate: the selected outcome meets its evidence-level requirements; universal language is used
only when supported by a formal metatheoretic proof, while computational conclusions state exact
bounds, checker assumptions, or restrictions.

### Phase 9 — Productization

Deliver:

- namespaced task targets in ProofScaffold;
- stable authoring/evidence schemas and documented migrations from the minimal v1 contracts;
- public IR query APIs for LaTeX and LLM tooling;
- cross-repository CI and clean-checkout replay;
- documented promotion and release procedures.

## 10. Cross-Repository Phase Coordination

No phase is complete merely because Proof Lab code exists. A vertical slice uses the released
stack and records evidence in every repository that owns part of the capability.

| Phase | Proof Scaffold | Prelude | Logic | Proof Lab |
| --- | --- | --- | --- | --- |
| 0–1 | Preserve deterministic builder/linker behavior; expose trace gaps | No change unless a foundation defect is proven | Keep exported assertion identities stable | Registry, Task 1 proofs, admission tests |
| 2 | Generic authoring IR, diagnostics, and task-target mechanisms | Foundation and binder ownership canary | Reusable FOL/equality/substitution capability | Capability matrix and minimal local-theory canary |
| 3–6 | Evidence schemas and fail-closed lowering | Only genuinely universal symbols | Generic lemmas required by Sheridan | Source audit, local theory, proofs, reports |
| 7–8 | Generic certificate and provenance hooks where justified | Normally no change | Logical or semantic interface gaps only; finite mathematics stays task-local pending ownership review | Search, conjectures, witnesses, outcome-dependent certification |
| 9 | Stable APIs and namespace support | Release compatibility evidence | Authoring interface and catalogue evidence | Consumer and distribution replay |

A repository may record a no-change sign-off, but it may not be silently omitted from the phase
evidence.

### 10.1 Release train

When upstream changes are required, releases land in this order:

1. Proof Scaffold;
2. Prelude, only if foundation changes are required;
3. Logic;
4. Proof Lab exact dependency pins and lockfile.

Proof Lab release validation must use published artifacts. Editable sibling substitutions are a
separate candidate-stack lane and cannot be the only evidence.

Each integration record pins:

- all repository SHAs and published versions;
- Python and uv versions;
- schema versions;
- verifier versions;
- source and lockfile digests;
- generated artifact digests.

## 11. Verification Gates

### G0 — Input lock

- Task manifest validates.
- Statement, source, expected answer, and assumption boundary are frozen where applicable.
- Research semantics and bounds are explicit.

### G1 — Dependency and assumption audit

- Published dependency tuple is exact.
- No undeclared axiom or hidden foundation is present.
- Assumption changes and interpretation decisions are recorded.

### G2 — Static and build gate

```bash
uv sync --locked --dev
uv run --frozen ruff check .
uv run --frozen mypy .
uv run --frozen python -m pytest
```

The build must be deterministic and package import boundaries must pass.

### G3F — Formal verification gate

- package-level ProofScaffold verification passes;
- level-1 conformance passes where supported;
- declared coverage has no missing admitted claims;
- an independent Metamath verifier accepts the emitted artifact.

This gate is mandatory for package admission, `solved`, `restricted-case-proved`, and every claim
described as a formally verified theorem.

### G3C — Computational certification gate

- the problem semantics and search encoding are locked and versioned;
- witnesses are serialized canonically and checked independently of the producer;
- negative bounded results include either an independently checkable UNSAT certificate or a
  replayable exhaustive enumeration;
- encoding adequacy, bounds, tool versions, seeds, inputs, outputs, and hashes are recorded;
- the report states the computational trust base and does not claim formal theorem status.

This gate may close `counterexample-found` or `bounded-frontier-certified`. Passing it does not
admit proof code to the package build.

### G4 — Evidence completeness

- manifest, hashes, closure, trace, source maps, and verifier logs are complete;
- claim-ledger entries match emitted statements;
- a clean checkout reproduces equivalent artifacts.

### G5 — Promotion gate

- only admitted work enters the Python builder registry;
- no formal import or proof dependency points into experiments, conjectures, or generated output;
- research promotion records state the exact theorem, assumptions, and evidence being promoted.

## 12. Definitions of Done

### Proof

- Exact expected theorem emitted.
- Required linker and verifier checks pass.
- Closure, trace, logs, and hashes complete.
- Clean replay succeeds.

### Formalize

- Source immutable and cited per formalized claim.
- Every included, omitted, decomposed, or reformulated claim recorded.
- Interpretation decisions and assumption deltas explicit.
- Local axioms enumerated and stronger theories not imported silently.
- Declared milestone set verifier-accepted.

### Discover

- Search and conjecture history reproducible.
- Final outcome is one approved value.
- Counterexamples include canonical independently checked witnesses and the locked semantic
  interpretation.
- Restricted results state added assumptions and changed claims and are formally certified.
- Bounded results state exact exhaustive bounds, pass G3C, and make no universal claim.
- Audited inconclusion records explored space and open obligations.
- Only formally certified results cross into the formal build.

## 13. Immediate Decisions and Open Questions

Decisions already made:

- explicit registry replaces root glob discovery;
- executable Task 1 code is installed package code;
- Task 2 uses relation-based successor and predecessor first;
- Extensionality is omitted by default;
- Task 3 is quarantined and begins with bounded model search;
- no universal finite-model claim is accepted without a formal semantics layer.

Open questions to resolve in their designated phases:

- exact ProofScaffold task-target namespace design;
- source comparison between the published Sheridan article and arXiv v5;
- native versus expanded unique existence;
- the precise public FOL authoring interface exposed by Logic;
- host formalism for finite structures and satisfaction;
- certificate format and independent checker for finite-model search;
- artifact retention and release policy for large generated files.
