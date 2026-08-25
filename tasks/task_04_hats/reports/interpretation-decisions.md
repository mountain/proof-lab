# Interpretation Decisions

## ID-001 — Use the five-hat version

- **Decision:** Formalize the standard puzzle with three white hats and two black hats.
- **Reason:** “Six Thinking Hats” normally names Edward de Bono's thinking method, not a uniquely
  specified logic puzzle. The five-hat puzzle has a short, determinate argument.

## ID-002 — Compile, do not conceal, the epistemic step

- **Decision:** Use `φ → (ψ → χ)` as an explicit hypothesis, where `φ` means Alice does not know,
  `ψ` means Carol wears black, and `χ` means Bob knows he wears white.
- **Reason:** Proof Lab 0.0.1 exposes classical propositional and first-order foundations but no
  native knowledge modality or possible-world semantics.
- **Consequence:** The verifier certifies the propositional consequence of the bridge, not the
  bridge's modal semantics. Task 5 now checks the bridge exhaustively in the seven-world finite
  model, while keeping that computational evidence outside the Metamath trust boundary.

## ID-003 — Weaken Bob's announcement visibly

- **Decision:** Map Bob's “I do not know my color” to `¬χ`, “Bob does not know that he wears
  white.”
- **Reason:** The source statement entails this weaker proposition, and it is exactly what the
  final inference needs.
- **Consequence:** No unneeded claim about whether Bob knows he wears black enters the proof.

## ID-004 — Verify “not black”; elaborate “white” at the domain boundary

- **Decision:** The formal theorem concludes `¬ψ`. The natural-language result “Carol wears white”
  additionally uses the source's exhaustive two-color inventory.
- **Reason:** This keeps the proof's propositional vocabulary minimal and the domain assumption
  visible.
