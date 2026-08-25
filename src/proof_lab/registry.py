from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping

TaskKind = Literal["proof", "formalize", "discover"]
TaskStatus = Literal["active", "scaffolded", "research"]


@dataclass(frozen=True)
class ProofEntry:
    function: str
    theorem: str
    role: str


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    slug: str
    title: str
    kind: TaskKind
    status: TaskStatus
    manifest_path: str
    artifact_namespace: str
    builder: str | None = None
    implementation_module: str | None = None
    proofs: tuple[ProofEntry, ...] = ()

    @property
    def buildable(self) -> bool:
        return self.builder is not None


_TASKS = {
    "task_01": TaskSpec(
        task_id="task_01",
        slug="textbook",
        title="Propositional Proof Reconstruction",
        kind="proof",
        status="active",
        manifest_path="tasks/task_01_textbook/task.yaml",
        artifact_namespace="artifacts/task_01",
        builder="proof_lab.tasks._propositional_builder:build_tasks",
        implementation_module="proof_lab.tasks.task_01_textbook.proofs",
        proofs=(
            ProofEntry(
                function="prove_mp2",
                theorem="mp2",
                role="proof-construction",
            ),
            ProofEntry(
                function="prove_modus_tollens",
                theorem="modus_tollens",
                role="proof-construction",
            ),
            ProofEntry(
                function="prove_linearity",
                theorem="linearity",
                role="dependency-resolution-smoke-test",
            ),
        ),
    ),
    "task_02": TaskSpec(
        task_id="task_02",
        slug="sheridan",
        title="Sheridan Paper to Formalization",
        kind="formalize",
        status="scaffolded",
        manifest_path="tasks/task_02_sheridan/task.yaml",
        artifact_namespace="artifacts/task_02",
    ),
    "task_03": TaskSpec(
        task_id="task_03",
        slug="finite-models",
        title="Finite-Model Research to Proof",
        kind="discover",
        status="research",
        manifest_path="tasks/task_03_finite_models/task.yaml",
        artifact_namespace="artifacts/task_03",
    ),
    "task_04": TaskSpec(
        task_id="task_04",
        slug="hats",
        title="Five-Hat Knowledge Puzzle",
        kind="formalize",
        status="active",
        manifest_path="tasks/task_04_hats/task.yaml",
        artifact_namespace="artifacts/task_04",
        builder="proof_lab.tasks._propositional_builder:build_tasks",
        implementation_module="proof_lab.tasks.task_04_hats.proofs",
        proofs=(
            ProofEntry(
                function="prove_five_hat_conclusion",
                theorem="five_hat_conclusion",
                role="compiled-epistemic-inference",
            ),
        ),
    ),
    "task_05": TaskSpec(
        task_id="task_05",
        slug="epistemic-puzzles",
        title="Finite Public-Announcement Puzzle Suite",
        kind="formalize",
        status="active",
        manifest_path="tasks/task_05_epistemic_puzzles/task.yaml",
        artifact_namespace="artifacts/task_05",
    ),
    "task_06": TaskSpec(
        task_id="task_06",
        slug="dining-cryptographers",
        title="Dining Cryptographers Security Demo",
        kind="formalize",
        status="active",
        manifest_path="tasks/task_06_dining_cryptographers/task.yaml",
        artifact_namespace="artifacts/task_06",
    ),
}

TASKS: Mapping[str, TaskSpec] = MappingProxyType(_TASKS)

# This is an explicit release admission plan. Do not derive it from task status.
PACKAGE_TASK_IDS: tuple[str, ...] = ("task_01", "task_04")


def get_task(task_id: str) -> TaskSpec:
    try:
        return TASKS[task_id]
    except KeyError as exc:
        known = ", ".join(sorted(TASKS))
        raise KeyError(f"unknown task {task_id!r}; known tasks: {known}") from exc


__all__ = [
    "PACKAGE_TASK_IDS",
    "TASKS",
    "ProofEntry",
    "TaskKind",
    "TaskSpec",
    "TaskStatus",
    "get_task",
]
