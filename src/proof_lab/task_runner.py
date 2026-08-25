from __future__ import annotations

import argparse
import importlib
import json
from collections.abc import Callable, Sequence
from dataclasses import asdict
from typing import cast

from skfd.api_v2 import BuildContextV2

from proof_lab.registry import PACKAGE_TASK_IDS, TASKS, TaskSpec, get_task

TaskBuilder = Callable[[BuildContextV2, Sequence[TaskSpec]], None]


class TaskAdmissionError(ValueError):
    """Raised when a task is requested across the formal build boundary."""


def resolve_package_plan(task_ids: Sequence[str] = PACKAGE_TASK_IDS) -> tuple[TaskSpec, ...]:
    if not task_ids:
        raise TaskAdmissionError("the package task plan must not be empty")

    seen: set[str] = set()
    plan: list[TaskSpec] = []
    for task_id in task_ids:
        if task_id in seen:
            raise TaskAdmissionError(f"duplicate task in package plan: {task_id}")
        seen.add(task_id)

        try:
            task = get_task(task_id)
        except KeyError as exc:
            raise TaskAdmissionError(str(exc)) from exc
        if not task.buildable:
            raise TaskAdmissionError(
                f"task {task.task_id!r} is {task.status!r} and has no admitted builder"
            )
        plan.append(task)
    return tuple(plan)


def _load_builder(reference: str) -> TaskBuilder:
    module_name, separator, attribute = reference.partition(":")
    if not separator or not module_name or not attribute:
        raise TaskAdmissionError(
            f"invalid builder reference {reference!r}; expected 'module:attribute'"
        )

    module = importlib.import_module(module_name)
    candidate = getattr(module, attribute, None)
    if not callable(candidate):
        raise TaskAdmissionError(f"builder reference {reference!r} is not callable")
    return cast(TaskBuilder, candidate)


def build_registered_tasks(
    ctx: BuildContextV2,
    task_ids: Sequence[str] = PACKAGE_TASK_IDS,
) -> None:
    tasks_by_builder: dict[str, list[TaskSpec]] = {}
    for task in resolve_package_plan(task_ids):
        if task.builder is None:  # Narrowing guard for static type checkers.
            raise TaskAdmissionError(f"task {task.task_id!r} has no builder")
        tasks_by_builder.setdefault(task.builder, []).append(task)

    for builder_reference, tasks in tasks_by_builder.items():
        _load_builder(builder_reference)(ctx, tuple(tasks))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="proof-lab-tasks",
        description="Inspect the explicit Proof Lab task registry.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List all registered tasks without importing task code.")
    show = subparsers.add_parser("show", help="Show one task record as JSON.")
    show.add_argument("task_id", choices=sorted(TASKS))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "list":
        for task in TASKS.values():
            admission = "admitted" if task.task_id in PACKAGE_TASK_IDS else "quarantined"
            print(f"{task.task_id}\t{task.kind}\t{task.status}\t{admission}\t{task.title}")
        return 0

    if args.command == "show":
        print(json.dumps(asdict(get_task(args.task_id)), indent=2, sort_keys=True))
        return 0

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "TaskAdmissionError",
    "build_registered_tasks",
    "main",
    "resolve_package_plan",
]
