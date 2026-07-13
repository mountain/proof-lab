# proof-lab

`proof-lab` is a small demo playground for authoring and verifying proofs using ProofScaffold.
It is intentionally lightweight and is not meant to be a stable library; the primary deliverable is a few runnable proof scripts.

This repository uses ProofScaffold's **single-file verification** mode: each `prove_*.py` file is verified independently.

Additionally, the `proof-lab` *package build* aggregates all `prove_*.py` scripts at the repository root, so `skfd verify proof-lab` verifies the whole demo set as one monolith.

## Versioning

- Package version: `0.0.1`
- ProofScaffold dependency: `proof-scaffold==0.0.9`
- Prelude dependency: `metamath-prelude==0.0.5`
- Logic dependency: `metamath-logic==0.0.6`

The lockfile resolves these published releases directly; sibling checkouts are not substituted.

## Installation

With `uv`:

```bash
uv add proof-lab
```

## Proof scripts

- `prove_modus_tollens.py`: Modus Tollens
- `prove_mp2.py`: Double Modus Ponens
- `prove_linearity.py`: Linearity

## Verification

From the `proof-lab/` directory:

```bash
uv sync --locked --dev
uv run --frozen ruff check .
uv run --frozen mypy .
uv run --frozen python -m pytest

# Single-file verification (emits target/<script>_script.mm)
uv run --frozen skfd verify prove_modus_tollens.py
uv run --frozen skfd verify prove_mp2.py
uv run --frozen skfd verify prove_linearity.py

# Package verification (emits target/proof-lab_full.mm)
uv run --frozen skfd verify proof-lab
```

When verifying a script, `skfd` discovers functions named `prove_*`, executes them, emits `target/<script>_script.mm`, and runs the configured verifiers.

When verifying the package, `src/proof_lab/build.py` loads every `prove_*.py` at the repository root (by file path, not via `PYTHONPATH`) and emits them into the package unit so that `skfd verify proof-lab` covers the full demo.
