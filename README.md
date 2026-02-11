# proof-lab

`proof-lab` is a small demo playground for authoring and verifying proofs using ProofScaffold.
It is intentionally lightweight and is not meant to be a stable library; the primary deliverable is a few runnable proof scripts.

This repository uses ProofScaffold's **single-file verification** mode: each `prove_*.py` file is verified independently.

## Versioning

- Package version: `0.0.1`
- ProofScaffold dependency: `proof-scaffold==0.0.5`
- Prelude dependency: `metamath-prelude==0.0.2`
- Logic dependency: `metamath-logic==0.0.2`

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
uv run --frozen skfd verify prove_modus_tollens.py
uv run --frozen skfd verify prove_mp2.py
uv run --frozen skfd verify prove_linearity.py
```

When verifying a script, `skfd` discovers functions named `prove_*`, executes them, emits a temporary Metamath file, and runs the configured verifiers.
