# Task 5 — Finite Public-Announcement Puzzle Suite

Task 5 supplies executable finite-world semantics for three epistemic puzzles:

| Puzzle | Initial worlds | Public-announcement trace | Result |
| --- | ---: | --- | --- |
| Five hats | 7 | `7 -> 6 -> 4` | Carol is white in every surviving world. |
| Cheryl's Birthday | 10 | `10 -> 5 -> 3 -> 1` | The unique date is July 16. |
| Muddy children | `2^n` | Remove cardinality layers `0, 1, ..., k-1` | With `k` muddy children, they know after `k-1` public “no” rounds. |

The reusable semantic core is installed at `proof_lab.epistemic`. Puzzle models live at
`proof_lab.tasks.task_05_epistemic_puzzles`. Tests exhaust the muddy-children construction for every
nonempty actual world with one through five children.

The code is organized as an executable essay: module docstrings introduce the mathematical object,
comments explain each information partition and announcement, and traces retain the exact eliminated
worlds. [REFERENCES.md](REFERENCES.md) records the semantic sources and puzzle provenance.

## Evidence level

This task provides **computational certification**, not Metamath formal certification. Its Python
model checker validates the finite S5 relations, recursively evaluates knowledge, and records
truthful public-announcement restrictions. It is not imported by `proof_lab.build` and has no
builder in the admission registry.

Task 4 remains the formal endpoint for the five-hat propositional consequence. Task 5 upgrades
Task 4's epistemic bridge from prose-only justification to executable finite-model evidence, but
does not place the bridge's modal semantics inside the verifier kernel.
