# Muddy Children

There are `n` children. Each child can see every other child's forehead but not their own. Everyone
knows this observation structure and reasons correctly. The father truthfully announces:

> At least one child has mud on their forehead.

He then repeatedly asks every child whether they know whether they themselves are muddy. In each
round before the decisive round, every child publicly answers “no.”

For an actual world with `k >= 1` muddy children, show by finite public-announcement evaluation
that after `k - 1` all-no rounds every muddy child knows that they are muddy.

The implementation is parameterized by `n`. The acceptance suite exhaustively checks every nonempty
actual world for `1 <= n <= 5`; it does not claim an internally formalized induction theorem for
arbitrary `n`.

## Background

The puzzle is a standard example in the logic of knowledge and common knowledge. The implementation
follows the finite information-set account in Fagin, Halpern, Moses, and Vardi's *Reasoning About
Knowledge* and the discussion in their [“Common Knowledge
Revisited”](https://arxiv.org/abs/cs/9809003). See [../REFERENCES.md](../REFERENCES.md) for the exact
scope of those citations and of the local bounded claim.
