from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any

from skfd.api_v2 import BuildContextV2
from skfd.authoring.emit import emit_lowered_lemmas

from logic.propositional.hilbert import System


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _discover_prove_fns(module: ModuleType) -> list[tuple[str, Any]]:
    proofs: list[tuple[str, Any]] = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("prove_") and inspect.isfunction(obj):
            proofs.append((name, obj))
    proofs.sort(key=lambda x: x[1].__code__.co_firstlineno)
    return proofs


def build(ctx: BuildContextV2) -> None:
    mm = ctx.mm

    prelude = ctx.deps["metamath-prelude"]
    logic = ctx.deps["metamath-logic"]

    system = System.make(interner=mm.interner, names=ctx.names)
    wff = prelude["wff"]
    provable = prelude["|-"]

    project_root = Path(__file__).resolve().parents[2]
    script_paths = sorted(project_root.glob("prove_*.py"))

    proofs: list[Any] = []
    for script_path in script_paths:
        module = _load_module(script_path)
        for _, fn in _discover_prove_fns(module):
            sig = inspect.signature(fn)
            p = fn(system) if len(sig.parameters) > 0 else fn()
            if p is not None:
                proofs.append(p)

    compiled_axioms = system.compile_axioms()
    reserved = {"wi", "wn", "wa", "mp"}

    def _refs(p: Any) -> set[str]:
        refs: set[str] = set()
        for st in getattr(p, "steps", ()):
            if getattr(st, "op", None) != "ref":
                continue
            ref = getattr(st, "ref", None)
            if isinstance(ref, str) and ref:
                refs.add(ref)
        return refs

    try:
        from logic.propositional.hilbert.theorems import SETMM_TO_HILBERT_LEMMAS
    except Exception:
        SETMM_TO_HILBERT_LEMMAS = {}

    queue: list[Any] = list(proofs)
    lemma_by_name: dict[str, Any] = {}
    while queue:
        p = queue.pop(0)
        lemma_name = getattr(p, "name", None)
        if not isinstance(lemma_name, str) or not lemma_name:
            continue
        if lemma_name in lemma_by_name:
            continue
        lemma_by_name[lemma_name] = p
        for ref in _refs(p):
            if ref in compiled_axioms or ref in reserved:
                continue
            if ref in lemma_by_name:
                continue
            ctor = SETMM_TO_HILBERT_LEMMAS.get(ref)
            if ctor is not None:
                queue.append(ctor(system))

    unresolved: set[str] = set()
    for p in lemma_by_name.values():
        for ref in _refs(p):
            if ref in compiled_axioms or ref in reserved or ref in lemma_by_name:
                continue
            unresolved.add(ref)
    if unresolved:
        raise RuntimeError(f"unresolved lemma references: {sorted(unresolved)}")

    # Resolve every dependency-owned label to its exported SymbolId.  Falling
    # back to ``mm.sym.label(name)`` would create a proof-lab-local label with
    # the same spelling; the linker then has to rename it, leaving proof steps
    # such as ``ax-1`` or ``wa`` pointed at an assertion that was never emitted.
    external_labels = {
        **prelude.as_dict(),
        **logic.as_dict(),
        "mp": logic["ax-mp"],
        "A1": logic["ax-1"],
        "A2": logic["ax-2"],
        "A3": logic["ax-3"],
    }

    emit_lowered_lemmas(
        mm,
        system,
        list(lemma_by_name.values()),
        typecode=provable,
        wff_typecode=wff,
        label_ids=external_labels,
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

    mm.export(*(mm.sym.label(name) for name in sorted(lemma_by_name.keys())))
