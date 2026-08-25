import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from proof_lab import task_runner
from proof_lab.registry import PACKAGE_TASK_IDS, TASKS, TaskSpec


REPOSITORY_ROOT = Path(__file__).parents[1]


def test_repository_has_one_proofscaffold_build_entrypoint() -> None:
    build_files = tuple(
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for path in sorted((REPOSITORY_ROOT / "src").rglob("build.py"))
    )

    assert build_files == ("src/proof_lab/build.py",)
    assert tuple(REPOSITORY_ROOT.glob("prove_*.py")) == ()


def test_registry_describes_admitted_and_quarantined_tasks() -> None:
    assert tuple(TASKS) == (
        "task_01",
        "task_02",
        "task_03",
        "task_04",
        "task_05",
        "task_06",
    )
    assert PACKAGE_TASK_IDS == ("task_01", "task_04", "task_06")

    task_01 = TASKS["task_01"]
    assert task_01.status == "active"
    assert task_01.builder == "proof_lab.tasks._propositional_builder:build_tasks"
    assert task_01.implementation_module == "proof_lab.tasks.task_01_textbook.proofs"
    assert tuple((proof.function, proof.theorem) for proof in task_01.proofs) == (
        ("prove_mp2", "mp2"),
        ("prove_modus_tollens", "modus_tollens"),
        ("prove_linearity", "linearity"),
    )

    for task_id in ("task_02", "task_03"):
        draft = TASKS[task_id]
        assert not draft.buildable
        assert draft.builder is None
        assert draft.implementation_module is None
        assert draft.proofs == ()

    task_04 = TASKS["task_04"]
    assert task_04.status == "active"
    assert task_04.kind == "formalize"
    assert task_04.builder == "proof_lab.tasks._propositional_builder:build_tasks"
    assert task_04.implementation_module == "proof_lab.tasks.task_04_hats.proofs"
    assert tuple((proof.function, proof.theorem) for proof in task_04.proofs) == (
        ("prove_five_hat_conclusion", "five_hat_conclusion"),
    )

    task_05 = TASKS["task_05"]
    assert task_05.status == "active"
    assert task_05.kind == "formalize"
    assert not task_05.buildable
    assert task_05.builder is None
    assert task_05.implementation_module is None
    assert task_05.proofs == ()

    task_06 = TASKS["task_06"]
    assert task_06.status == "active"
    assert task_06.kind == "formalize"
    assert task_06.buildable
    assert task_06.builder == "proof_lab.tasks._propositional_builder:build_tasks"
    assert task_06.implementation_module == (
        "proof_lab.tasks.task_06_dining_cryptographers.proofs"
    )
    assert tuple((proof.function, proof.theorem) for proof in task_06.proofs) == (
        ("prove_dc_parity_table", "dc_parity_table"),
        ("prove_dc_payer_bijection_table", "dc_payer_bijection_table"),
    )


def test_default_package_plan_admits_only_explicit_tasks() -> None:
    plan = task_runner.resolve_package_plan()

    assert tuple(task.task_id for task in plan) == ("task_01", "task_04", "task_06")


@pytest.mark.parametrize(
    ("task_ids", "message"),
    [
        ((), "must not be empty"),
        (("task_01", "task_01"), "duplicate task"),
        (("task_02",), "no admitted builder"),
        (("task_03",), "no admitted builder"),
        (("task_05",), "no admitted builder"),
        (("task_99",), "unknown task"),
    ],
)
def test_package_plan_rejects_implicit_or_invalid_admission(
    task_ids: tuple[str, ...], message: str
) -> None:
    with pytest.raises(task_runner.TaskAdmissionError, match=message):
        task_runner.resolve_package_plan(task_ids)


def test_plan_resolution_does_not_import_task_code(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_import(module_name: str) -> None:
        pytest.fail(f"plan resolution imported {module_name!r}")

    monkeypatch.setattr("proof_lab.task_runner.importlib.import_module", fail_import)

    assert tuple(task.task_id for task in task_runner.resolve_package_plan()) == (
        "task_01",
        "task_04",
        "task_06",
    )
    with pytest.raises(task_runner.TaskAdmissionError, match="no admitted builder"):
        task_runner.resolve_package_plan(("task_02",))


def test_build_loads_only_the_admitted_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    imported_modules: list[str] = []
    builder_calls: list[tuple[object, tuple[TaskSpec, ...]]] = []

    def build_tasks(context: object, tasks: tuple[TaskSpec, ...]) -> None:
        builder_calls.append((context, tasks))

    def import_module(module_name: str) -> SimpleNamespace:
        imported_modules.append(module_name)
        return SimpleNamespace(build_tasks=build_tasks)

    monkeypatch.setattr("proof_lab.task_runner.importlib.import_module", import_module)
    context = object()

    task_runner.build_registered_tasks(context)

    assert imported_modules == ["proof_lab.tasks._propositional_builder"]
    assert builder_calls == [
        (context, (TASKS["task_01"], TASKS["task_04"], TASKS["task_06"])),
    ]


def test_build_rejects_a_quarantined_task_before_import(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_import(module_name: str) -> None:
        pytest.fail(f"quarantined task imported {module_name!r}")

    monkeypatch.setattr("proof_lab.task_runner.importlib.import_module", fail_import)

    with pytest.raises(task_runner.TaskAdmissionError, match="no admitted builder"):
        task_runner.build_registered_tasks(object(), ("task_02",))


def test_cli_list_reports_admission_without_importing_task_code(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail_import(module_name: str) -> None:
        pytest.fail(f"list command imported {module_name!r}")

    monkeypatch.setattr("proof_lab.task_runner.importlib.import_module", fail_import)

    assert task_runner.main(["list"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "task_01\tproof\tactive\tadmitted\tPropositional Proof Reconstruction",
        "task_02\tformalize\tscaffolded\tquarantined\tSheridan Paper to Formalization",
        "task_03\tdiscover\tresearch\tquarantined\tFinite-Model Research to Proof",
        "task_04\tformalize\tactive\tadmitted\tFive-Hat Knowledge Puzzle",
        "task_05\tformalize\tactive\tquarantined\tFinite Public-Announcement Puzzle Suite",
        "task_06\tformalize\tactive\tadmitted\tDining Cryptographers Security Demo",
    ]


def test_cli_show_returns_registry_metadata_without_importing_task_code(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail_import(module_name: str) -> None:
        pytest.fail(f"show command imported {module_name!r}")

    monkeypatch.setattr("proof_lab.task_runner.importlib.import_module", fail_import)

    assert task_runner.main(["show", "task_02"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["task_id"] == "task_02"
    assert payload["kind"] == "formalize"
    assert payload["status"] == "scaffolded"
    assert payload["builder"] is None
    assert payload["implementation_module"] is None
    assert payload["proofs"] == []
