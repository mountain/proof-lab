# proof-lab

`proof-lab` is a small experimental package for authoring and verifying proofs using ProofScaffold.

## Installation

With `uv`:

```bash
uv add proof-lab
```

## Verification

From the `proof-lab/` directory:

```bash
uv sync --locked --dev
uv run --frozen ruff check .
uv run --frozen mypy .
uv run --frozen python -m pytest
uv run --frozen python tools/run_skfd.py verify --level 1 proof-lab
```

