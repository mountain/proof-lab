# Minimal v1 Evidence Schemas

This directory contains the first structural contracts for Proof Lab records. The schemas use
JSON Schema Draft 2020-12 and intentionally remain open to additional properties so that task
workflows can add domain-specific fields without revising the common envelope.

## Schema index

| Schema | Version marker | Identity and evidence gate | Additional `complete` requirements |
| --- | --- | --- | --- |
| [`task.schema.json`](task.schema.json) | `proof-lab-task-v1` | `task.id`, title, workflow, and status | implementation admission flag, artifact namespace, and acceptance policy |
| [`source-lock.schema.json`](source-lock.schema.json) | `proof-lab-source-lock-v1` | every source has an `id` | `task_id`, `evidence_level`, and retrieval metadata plus a SHA-256 digest for every source |
| [`claim-ledger.schema.json`](claim-ledger.schema.json) | `proof-lab-claim-ledger-v1` | every claim has an `id` and status | `task_id`, ledger and claim evidence levels, locked-source reference, statements, and source mappings |
| [`artifact-manifest.schema.json`](artifact-manifest.schema.json) | `proof-lab-artifact-manifest-v1` | `artifact_id`, `task_id`, status, and `evidence_level` | timestamped outputs with SHA-256 digests and at least one evidence reference |
| [`research-outcome.schema.json`](research-outcome.schema.json) | `proof-lab-research-outcome-v1` | `outcome_id`, `task_id`, status, outcome, and `evidence_level` | one legal terminal outcome, a normalized result claim, a summary, and at least one evidence reference |

## Validation policy

- A status must equal the exact string `complete` before a schema applies its completion gate.
  Other status values remain draft-compatible.
- `evidence_level` is a non-empty policy label. The task or evaluator owns the controlled
  vocabulary; the common schemas enforce its presence without pretending that a label proves a
  claim.
- SHA-256 fields contain the lowercase, 64-character hexadecimal digest only.
- Unknown fields are allowed in v1. Semantic checks such as unique IDs, dependency closure,
  source-to-claim consistency, and verifier independence belong in the Python admission layer.
- Schema validation supplements, but never replaces, the Python admission boundary. Changing a
  manifest status must not make a task executable or promote research code into the formal build.
