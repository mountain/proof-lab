"""The muddy-children induction pattern as a bounded executable model.

The puzzle illustrates why publicly saying an already visible fact can still change what a group
knows. Every child sees the other foreheads, but not their own. The father's announcement—"at least
one child is muddy"—removes the empty world and makes that fact public. The children's synchronized
answers then expose higher-order ignorance. This is a standard example in the knowledge and common-
knowledge literature [FHMMV95, FHMV98].

Worlds are sets of muddy child indices. Child ``i`` cannot distinguish ``w`` from the world obtained
by toggling only ``i``: all other foreheads look identical. After the father's statement, each public
round of "no" removes one cardinality layer:

* zero muddy children disappears after the father's announcement;
* one muddy child disappears after the first all-no announcement;
* two muddy children disappears after the second; and so on.

If the actual world contains ``k`` muddy children, the program performs ``k - 1`` all-no rounds and
then checks that every muddy child knows they are muddy. Tests enumerate every nonempty actual world
for ``1 <= n <= 5``. That is strong bounded evidence, not a Metamath induction theorem for arbitrary
``n``. Full references and the trust boundary are documented beside Task 5.
"""

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
    """Enumerate all ``2^n`` assignments in increasing muddy-count order."""

    children = tuple(range(child_count))
    return tuple(
        frozenset(group)
        for size in range(child_count + 1)
        for group in combinations(children, size)
    )


def _muddy_model(child_count: int) -> FiniteModel:
    """Build the pre-announcement model from what each child can see."""

    if child_count < 1:
        raise ValueError("child_count must be positive")
    muddy_worlds = _powerset(child_count)
    worlds: tuple[World, ...] = tuple(muddy_worlds)
    valuations: dict[World, frozenset[str]] = {
        world: frozenset(_muddy_atom(child) for child in world) for world in muddy_worlds
    }
    accessibility: dict[str, dict[World, frozenset[World]]] = {}

    for child in range(child_count):
        # Removing the observer from the set leaves exactly the muddy foreheads that child sees.
        # Consequently two worlds share an observation precisely when they differ, if at all, in
        # that child's own status.
        observations: dict[World, Hashable] = {
            world: world - frozenset((child,)) for world in muddy_worlds
        }
        accessibility[_agent(child)] = relation_from_observations(worlds, observations)
    return FiniteModel(worlds, valuations, accessibility)


def solve_muddy_children(child_count: int, actual: MuddyWorld) -> MuddyOutcome:
    """Run the dialogue up to the round where the actual muddy children know."""

    if not actual:
        raise ValueError("the father's announcement requires at least one muddy child")
    if not actual <= frozenset(range(child_count)):
        raise ValueError("actual world contains an unknown child")

    model = _muddy_model(child_count)

    # The father contributes higher-order information even though each muddy child can already see
    # mud when k > 1. Formally, the announcement deletes the empty world for every observer at once.
    at_least_one = disjunction(
        *(Atom(_muddy_atom(child)) for child in range(child_count))
    )
    model, father_trace = model.announce(
        at_least_one,
        label="Father: At least one child is muddy",
    )
    traces: list[AnnouncementTrace] = [father_trace]

    # A synchronized "no" means every child truthfully says that their own status is not yet known.
    # The formula is built once but re-evaluated in the successively restricted model each round.
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

    # After k - 1 such rounds, every muddy child sees that the only remaining compatible alternative
    # has them muddy. Clean children's knowledge is not the conclusion asserted by this function.
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
