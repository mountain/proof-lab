# Problem Statement and Semantic Boundary

Status: **Not yet locked**

## Research question

Do the successor and predecessor existence-and-uniqueness axioms from Sheridan's
Incomprehensive Set Theory have a finite model?

The initial active conjecture may be named `NoFiniteModel`, but the name is not a result. A finite
model would refute that conjecture.

## Intended object-language signature

Use classical first-order logic with equality over a nonempty domain, with:

- a binary relation `Membership(z, x)`;
- a unary predicate `Set(x)`.

For a structure with domain `D`, define the intended relation schemas:

```text
Succ(x, y) := Set(y) and forall z in D.
              Membership(z, y) iff (Membership(z, x) or z = x)

Pred(x, y) := Set(y) and forall z in D.
              Membership(z, y) iff (Membership(z, x) and z != x)
```

The two intended axioms are:

```text
forall x in D. exists exactly one y in D. Succ(x, y)
forall x in D. exists exactly one y in D. Pred(x, y)
```

Before experiments become acceptance evidence, this formulation must be compared with the locked
Task 2 source and assigned a stable normalized representation.

The final outcome record also carries a normalized result claim, because a generic outcome such as
`counterexample-found` does not identify its polarity. For this task, the claim must say explicitly
whether a finite model exists, no finite model exists, only a named restriction is proved, only
declared cardinalities are excluded, or no mathematical conclusion is claimed.

## Finite-model convention

A candidate finite model must provide:

1. a nonempty finite domain `D`;
2. a total interpretation of `Set` on `D`;
3. a total truth table for `Membership` on `D x D`;
4. independent validation of both existence-and-uniqueness axioms for every `x in D`.

Every witness must be serialized canonically and checked by code independent from the search
encoding.

## Assumption boundary

The core problem must not silently assume:

- Extensionality;
- Foundation;
- unrestricted Comprehension or Separation;
- that every object is a set;
- that successor and predecessor are inverse functions;
- any ambient set theory stronger than the locked two-axiom theory.

Any result that adds one of these conditions is a different, restricted statement and must record
the complete assumption delta.

## Certification boundary

Finite model search answers bounded instances. It does not by itself prove nonexistence at every
finite cardinality.

Certification of `NoFiniteModel` requires a declared host metatheory in which finite structures,
object-language satisfaction, and finiteness are formalized. Until that representation and its
soundness bridge are independently verified, the strongest admissible negative-search outcome is
`bounded-frontier-certified` or `inconclusive-but-audited`.

The first host representation may specialize to finite domains, `Set`, `Membership`, and direct
semantic forms of the two axioms. A generic FOL satisfaction development is optional, but an
adequacy proof to the locked FOL sentences is mandatory before claiming that no finite FOL model
exists.

## Planned proof route

The planned route is intentionally provisional:

1. use finite search to find models, counterexamples to candidate invariants, or structural
   patterns;
2. define `Toggle(x, y)` as a relation and prove totality and uniqueness before introducing any
   function notation;
3. prove the finite-cycle lemma required for the induced operation graph;
4. connect those lemmas to `NoFiniteModel` in the locked metatheory;
5. stop or reclassify immediately if a checked finite model invalidates the route.

Locking this file requires explicit decisions for the source version, unique-existence encoding,
finite-structure representation, satisfaction semantics, and certification target.
