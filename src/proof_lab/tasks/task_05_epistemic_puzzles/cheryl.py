from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass

from proof_lab.epistemic import (
    AnnouncementTrace,
    FiniteModel,
    Knows,
    KnowsWhichWorld,
    Not,
    World,
    conjunction,
    relation_from_observations,
)

ALBERT = "albert"
BERNARD = "bernard"


@dataclass(frozen=True, order=True)
class Date:
    month: str
    day: int

    def __str__(self) -> str:
        return f"{self.month} {self.day}"


CANDIDATE_DATES: tuple[Date, ...] = (
    Date("May", 15),
    Date("May", 16),
    Date("May", 19),
    Date("June", 17),
    Date("June", 18),
    Date("July", 14),
    Date("July", 16),
    Date("August", 14),
    Date("August", 15),
    Date("August", 17),
)
CHERYL_SOLUTION = Date("July", 16)


@dataclass(frozen=True)
class CherylOutcome:
    initial: FiniteModel
    after_albert_first: FiniteModel
    after_bernard: FiniteModel
    final: FiniteModel
    traces: tuple[AnnouncementTrace, ...]
    solution: Date


def _cheryl_model() -> FiniteModel:
    worlds: tuple[World, ...] = tuple(CANDIDATE_DATES)
    valuations: dict[World, frozenset[str]] = {
        date: frozenset() for date in CANDIDATE_DATES
    }
    month_observations: dict[World, Hashable] = {
        date: date.month for date in CANDIDATE_DATES
    }
    day_observations: dict[World, Hashable] = {
        date: date.day for date in CANDIDATE_DATES
    }
    accessibility = {
        ALBERT: relation_from_observations(worlds, month_observations),
        BERNARD: relation_from_observations(worlds, day_observations),
    }
    return FiniteModel(worlds, valuations, accessibility)


def solve_cheryl_birthday() -> CherylOutcome:
    initial = _cheryl_model()
    albert_first = conjunction(
        Not(KnowsWhichWorld(ALBERT)),
        Knows(ALBERT, Not(KnowsWhichWorld(BERNARD))),
    )
    after_albert, albert_trace = initial.announce(
        albert_first,
        label="Albert: I do not know, but I know Bernard does not know",
    )

    after_bernard, bernard_trace = after_albert.announce(
        KnowsWhichWorld(BERNARD),
        label="Bernard: Now I know",
    )
    final, albert_final_trace = after_bernard.announce(
        KnowsWhichWorld(ALBERT),
        label="Albert: Now I know too",
    )
    if len(final.worlds) != 1 or not isinstance(final.worlds[0], Date):
        raise RuntimeError("Cheryl's Birthday did not reduce to one date")
    return CherylOutcome(
        initial=initial,
        after_albert_first=after_albert,
        after_bernard=after_bernard,
        final=final,
        traces=(albert_trace, bernard_trace, albert_final_trace),
        solution=final.worlds[0],
    )


__all__ = [
    "CANDIDATE_DATES",
    "CHERYL_SOLUTION",
    "CherylOutcome",
    "Date",
    "solve_cheryl_birthday",
]
