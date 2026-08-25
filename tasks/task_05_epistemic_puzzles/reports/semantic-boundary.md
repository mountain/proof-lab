# Semantic and Trust Boundary

## What the finite engine checks

The engine represents a model `M = (W, R, V)` with a finite ordered world set, one accessibility
relation per agent, and a propositional valuation. Every accessibility relation is checked to be
reflexive, symmetric, and transitive. Knowledge is evaluated by

```text
M, w |= K_i phi  iff  M, v |= phi for every v with w R_i v.
```

A truthful public announcement of `alpha` restricts the model to worlds satisfying `alpha` and
restricts each accessibility relation to the surviving worlds.

## What it does not check

- The Metamath kernel does not parse `K_i` or a public-announcement modality.
- Proof Lab does not yet emit a propositional proof of every finite semantic expansion.
- The muddy-children family is checked for bounded instances, not proved by induction for all `n`.
- Correctness of the Python semantic evaluator belongs to the disclosed computational trust base.

Consequently Task 5 is registered but quarantined from `PACKAGE_TASK_IDS`. Its results may justify
and audit a semantic bridge, but only Task 4's lowered propositional theorem is formally certified
by `mmverify`.

## Promotion gate

The next evidence upgrade is a proof-producing finite compiler: expand each knowledge formula into
a conjunction over its information cell, expand public announcements into restricted finite
models, and emit a propositional proof object. Native S5 or public-announcement syntax is not
required for that intermediate step.
