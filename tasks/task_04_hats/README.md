# Task 4 — Five-Hat Knowledge Puzzle

Task 4 is a small end-to-end formalization example:

```text
natural-language puzzle
    -> explicit interpretation decisions
    -> propositional knowledge bridge
    -> proof construction
    -> Metamath verifier acceptance
```

The certified theorem is:

```text
φ, ¬χ, φ → (ψ → χ) |- ¬ψ
```

Here `φ` means Alice says she does not know, `ψ` means Carol wears black, and `χ` means Bob knows
he wears white. The proof uses modus ponens, contraposition (`con3`), and two further modus ponens
steps. It does not cite `five_hat_conclusion` or use a raw proof fallback.

The epistemic bridge is explicit because the current dependency stack does not supply a native
knowledge modality. See [problem/problem.md](problem/problem.md) for the puzzle and
[reports/interpretation-decisions.md](reports/interpretation-decisions.md) for the exact trust
boundary.
