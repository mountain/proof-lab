from pathlib import Path

from proof_lab.registry import TASKS


REPOSITORY_ROOT = Path(__file__).parents[1]


def test_hat_formalization_keeps_the_epistemic_boundary_explicit() -> None:
    task = TASKS["task_04"]
    assert task.kind == "formalize"
    assert task.buildable
    assert task.proofs[0].role == "compiled-epistemic-inference"

    report = (
        REPOSITORY_ROOT
        / "tasks/task_04_hats/reports/interpretation-decisions.md"
    ).read_text(encoding="utf-8")
    assert "native knowledge modality" in report
    assert "explicit hypothesis" in report


def test_hat_proof_has_no_raw_or_self_reference() -> None:
    proof_source = (
        REPOSITORY_ROOT
        / "src/proof_lab/tasks/task_04_hats/proofs/five_hat_conclusion.py"
    ).read_text(encoding="utf-8")
    assert ".raw(" not in proof_source
    assert 'ref="five_hat_conclusion"' not in proof_source
