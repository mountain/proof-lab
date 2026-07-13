# Artifact Namespaces

This directory reserves stable namespaces for generated task evidence. Artifacts are build and
research outputs; they are never trusted proof inputs.

Each mature task namespace will contain a versioned `artifact-manifest.json` that records source
and lockfile digests, exact commands and tool versions, output hashes, dependency closure, proof
trace or experimental evidence, verifier results, and the task outcome.

Large or reproducible generated files may be excluded from version control later, but their
schemas, retention policy, and hashes must remain explicit.
