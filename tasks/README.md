# Task Records

This directory contains the durable records for Proof Lab tasks. A task directory may contain
source locks, claims, local-theory specifications, experiments, proof records, and reports.

Presence in this directory does not make a task buildable. Formal admission is controlled only by
`proof_lab.registry.PACKAGE_TASK_IDS` and an explicit installed builder reference.

| Task | Workflow | Current status | Formal build |
| --- | --- | --- | --- |
| `task_01_textbook` | Proof | Active | Admitted |
| `task_02_sheridan` | Formalize | Scaffolded | Quarantined |
| `task_03_finite_models` | Discover | Research | Quarantined |
| `task_04_hats` | Formalize | Active | Admitted |
| `task_05_epistemic_puzzles` | Formalize | Active | Computational evidence only |
| `task_06_dining_cryptographers` | Formalize | Active | Computational evidence only |

Executable task code that must be included in a wheel lives under `src/proof_lab/tasks/`. Research
records and generated artifacts must never be imported by the formal package build.
