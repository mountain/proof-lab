# Formal Proof Candidates

This directory will index Task 3 proof candidates and their evidence. It intentionally contains no
admitted executable Python modules.

The Toggle invariant and finite-cycle lemma may be certified independently once their statements
and assumption boundaries are locked. A `NoFiniteModel` candidate additionally requires the
metatheory gate described in `../task.yaml` and `../problem/problem.md`.

No candidate may enter the installed Proof Lab build until:

1. its exact semantic level is explicit;
2. its dependency and assumption closure is complete;
3. the relevant gate is open;
4. Level 1 linking and an independent verifier accept it; and
5. the formal task registry admits its installed builder explicitly.

Incomplete or failed candidates remain research records and must never be imported by formal build
code.
