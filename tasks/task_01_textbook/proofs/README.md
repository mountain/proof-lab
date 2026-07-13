# Task 1 Proof Sources

Executable proof modules are installed package code:

```text
src/proof_lab/tasks/task_01_textbook/proofs/
  double_modus_ponens.py
  modus_tollens.py
  linearity_import.py
```

This record directory intentionally contains no duplicate Python implementation. The split keeps
task evidence at the repository level while ensuring that wheel installation does not depend on
files outside `src/`.
