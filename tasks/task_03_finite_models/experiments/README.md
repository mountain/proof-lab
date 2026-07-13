# Experiments

This directory will index reproducible finite-model searches. It is not a proof source directory.

Each run record must include:

- experiment and encoding versions;
- exact domain bounds;
- solver or enumerator identity and version;
- deterministic seeds and configuration;
- input and output hashes;
- elapsed time and completion status;
- SAT witnesses, UNSAT certificates when available, and raw logs;
- independent checker results.

The encoding audit covers equality-as-identity, quantifier expansion, unique existence, the
assignment-to-structure correspondence, and any symmetry breaking. A symmetry reduction is usable
only after its satisfiability preservation is justified.

"No model found" is not a universal result. A run contributes to
`bounded-frontier-certified` only when the declared space was exhaustively covered and that
coverage is replayable or independently certified.
