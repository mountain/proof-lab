from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from itertools import combinations
from typing import TypeAlias

from proof_lab.epistemic import (
    AnnouncementTrace,
    Atom,
    FiniteModel,
    Knows,
    Not,
    World,
    conjunction,
    disjunction,
    knows_whether,
    relation_from_observations,
)

MuddyWorld: TypeAlias = frozenset[int]


def _agent(child: int) -> str:
    return f"child_{child}"


def _muddy_atom(child: int) -> str:
    return f"muddy_{child}"


@dataclass(frozen=True)
class MuddyOutcome:
    child_count: int
    actual: MuddyWorld
    final: FiniteModel
    traces: tuple[AnnouncementTrace, ...]

    @property
    def muddy_count(self) -> int:
        return len(self.actual)


def _powerset(child_count: int) -> tuple[MuddyWorld, ...]:
    children = tuple(range(child_count))
    return tuple(
        frozenset(group)
        for size in range(child_count + 1)
        for group in combinations(children, size)
    )


def _muddy_model(child_count: int) -> FiniteModel:
    if child_count < 1:
        raise ValueError("child_count must be positive")
    muddy_worlds = _powerset(child_count)
    worlds: tuple[World, ...] = tuple(muddy_worlds)
    valuations: dict[World, frozenset[str]] = {
        world: frozenset(_muddy_atom(child) for child in world) for world in muddy_worlds
    }
    accessibility: dict[str, dict[World, frozenset[World]]] = {}

    for child in range(child_count):
        observations: dict[World, Hashable] = {
            world: world - frozenset((child,)) for world in muddy_worlds
        }
        accessibility[_agent(child)] = relation_from_observations(worlds, observations)
    return FiniteModel(worlds, valuations, accessibility)


def solve_muddy_children(child_count: int, actual: MuddyWorld) -> MuddyOutcome:
    if not actual:
        raise ValueError("the father's announcement requires at least one muddy child")
    if not actual <= frozenset(range(child_count)):
        raise ValueError("actual world contains an unknown child")

    model = _muddy_model(child_count)
    at_least_one = disjunction(
        *(Atom(_muddy_atom(child)) for child in range(child_count))
    )
    model, father_trace = model.announce(
        at_least_one,
        label="Father: At least one child is muddy",
    )
    traces: list[AnnouncementTrace] = [father_trace]

    everyone_ignorant = conjunction(
        *(
            Not(knows_whether(_agent(child), Atom(_muddy_atom(child))))
            for child in range(child_count)
        )
    )
    for round_number in range(1, len(actual)):
        model, trace = model.announce(
            everyone_ignorant,
            label=f"Round {round_number}: every child says no",
        )
        traces.append(trace)
        if actual not in model.worlds:
            raise RuntimeError("a truthful muddy-children announcement eliminated the actual world")

    for child in actual:
        knows_muddy = Knows(_agent(child), Atom(_muddy_atom(child)))
        if not model.holds(actual, knows_muddy):
            raise RuntimeError(f"muddy child {child} does not know after the expected rounds")

    return MuddyOutcome(
        child_count=child_count,
        actual=actual,
        final=model,
        traces=tuple(traces),
    )


__all__ = ["MuddyOutcome", "MuddyWorld", "solve_muddy_children"]
