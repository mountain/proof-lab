from __future__ import annotations

import importlib
from collections.abc import Callable, Sequence
from typing import Any, cast

from logic.propositional.hilbert import System
from logic.propositional.hilbert.theorems import SETMM_TO_HILBERT_LEMMAS
from skfd.api_v2 import BuildContextV2
from skfd.authoring.emit import emit_lowered_lemmas
from skfd.proof import Proof

from proof_lab.registry import TaskSpec

ProofConstructor = Callable[[System], Proof]


def _proof_references(proof: Any) -> set[str]:
    references: set[str] = set()
    for step in getattr(proof, "steps", ()):
        if getattr(step, "op", None) != "ref":
            continue
        reference = getattr(step, "ref", None)
        if isinstance(reference, str) and reference:
            references.add(reference)
    return references


def _load_root_proofs(task: TaskSpec, system: System) -> list[Proof]:
    if task.implementation_module is None:
        raise RuntimeError(f"task {task.task_id!r} has no proof implementation module")

    module = importlib.import_module(task.implementation_module)
    roots: list[Proof] = []
    seen_theorems: set[str] = set()
    for entry in task.proofs:
        if entry.theorem in seen_theorems:
            raise RuntimeError(
                f"task {task.task_id!r} declares duplicate theorem {entry.theorem!r}"
            )
        seen_theorems.add(entry.theorem)

        candidate = getattr(module, entry.function, None)
        if not callable(candidate):
            raise RuntimeError(
                f"task {task.task_id!r} proof function {entry.function!r} is not callable"
            )
        constructor = cast(ProofConstructor, candidate)
        proof = constructor(system)
        if proof.name != entry.theorem:
            raise RuntimeError(
                f"task {task.task_id!r} expected theorem {entry.theorem!r}, "
                f"but {entry.function!r} built {proof.name!r}"
            )
        roots.append(proof)
    return roots


def _close_over_logic_catalog(roots: list[Proof], system: System) -> dict[str, Proof]:
    compiled_axioms = system.compile_axioms()
    reserved = {"wi", "wn", "wa", "mp"}
    queue: list[Proof] = list(roots)
    lemma_by_name: dict[str, Proof] = {}

    while queue:
        proof = queue.pop(0)
        if not proof.name:
            raise RuntimeError("encountered a proof without a theorem name")
        if proof.name in lemma_by_name:
            continue
        lemma_by_name[proof.name] = proof

        for reference in _proof_references(proof):
            if reference in compiled_axioms or reference in reserved or reference in lemma_by_name:
                continue
            constructor = SETMM_TO_HILBERT_LEMMAS.get(reference)
            if constructor is not None:
                queue.append(constructor(system))

    unresolved: set[str] = set()
    for proof in lemma_by_name.values():
        for reference in _proof_references(proof):
            if (
                reference in compiled_axioms
                or reference in reserved
                or reference in lemma_by_name
            ):
                continue
            unresolved.add(reference)
    if unresolved:
        raise RuntimeError(f"unresolved lemma references: {sorted(unresolved)}")
    return lemma_by_name


def _external_labels(ctx: BuildContextV2) -> dict[str, int]:
    prelude = ctx.deps["metamath-prelude"]
    logic = ctx.deps["metamath-logic"]
    labels = cast(dict[str, int], prelude.as_dict())

    for name, symbol_id in logic.items():
        existing = labels.get(name)
        if existing is not None and existing != symbol_id:
            raise RuntimeError(
                f"dependency label {name!r} has conflicting exported SymbolIds: "
                f"{existing} and {symbol_id}"
            )
        labels[name] = symbol_id

    aliases = {
        "mp": logic["ax-mp"],
        "A1": logic["ax-1"],
        "A2": logic["ax-2"],
        "A3": logic["ax-3"],
    }
    for name, symbol_id in aliases.items():
        existing = labels.get(name)
        if existing is not None and existing != symbol_id:
            raise RuntimeError(
                f"compatibility alias {name!r} conflicts with exported SymbolId {existing}"
            )
        labels[name] = symbol_id
    return labels


def build_tasks(ctx: BuildContextV2, tasks: Sequence[TaskSpec]) -> None:
    """Build a group of propositional tasks with one shared dependency closure."""
    if not tasks:
        raise RuntimeError("propositional task group must not be empty")

    mm = ctx.mm
    prelude = ctx.deps["metamath-prelude"]
    system = System.make(interner=mm.interner, names=ctx.names)
    roots_by_task = tuple((task, _load_root_proofs(task, system)) for task in tasks)
    roots = [proof for _, task_roots in roots_by_task for proof in task_roots]
    emitted_proofs = list(_close_over_logic_catalog(roots, system).values())

    for task, _ in roots_by_task:
        ctx.coverage.declare_labels(
            f"proof-lab:{task.task_id}",
            (entry.theorem for entry in task.proofs),
            require_verified=True,
        )

    emit_lowered_lemmas(
        mm,
        system,
        emitted_proofs,
        typecode=prelude["|-"],
        wff_typecode=prelude["wff"],
        label_ids=_external_labels(ctx),
        floating_by_var={
            prelude["ph"]: prelude["wph"],
            prelude["ps"]: prelude["wps"],
            prelude["ch"]: prelude["wch"],
            prelude["th"]: prelude["wth"],
            prelude["ta"]: prelude["wta"],
            prelude["et"]: prelude["wet"],
            prelude["ze"]: prelude["wze"],
            prelude["si"]: prelude["wsi"],
            prelude["rh"]: prelude["wrh"],
            prelude["mu"]: prelude["wmu"],
            prelude["la"]: prelude["wla"],
            prelude["ka"]: prelude["wka"],
        },
    )

    # The reconstructed catalogue closure is an implementation detail. Only task roots are public.
    mm.export(*(mm.sym.label(proof.name) for proof in roots))


def build_task(ctx: BuildContextV2, task: TaskSpec) -> None:
    """Backward-compatible single-task adapter."""
    build_tasks(ctx, (task,))


__all__ = ["build_task", "build_tasks"]
