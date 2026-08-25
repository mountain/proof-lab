"""Cheryl's Birthday, told as three successive restrictions of a ten-date model.

Joseph Yeo set this version for the 2015 Singapore and Asian Schools Math Olympiad. A later paper
coauthored by Yeo gives the puzzle, its provenance, and an indistinguishability-graph solution
[DHKWY17]. We encode that same graph directly:

* a world is one of the ten candidate dates;
* Albert's information cells group dates by month;
* Bernard's information cells group dates by day number.

The conversation then becomes an unusually readable model-checking trace:

``10 -> 5``
    Albert's first statement rules out May and June. Those months contain 19 or 18, on which Bernard
    could initially have known the date; Albert could not then know that Bernard was ignorant.
``5 -> 3``
    Bernard now knows, ruling out the two remaining dates numbered 14.
``3 -> 1``
    Albert now knows. August still offers two alternatives, while July offers only July 16.

Thus the sole survivor is July 16. Full bibliographic details are in
``tasks/task_05_epistemic_puzzles/REFERENCES.md``.
"""

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
    """One candidate world; ordering keeps traces stable and human-readable."""

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
    """Turn Cheryl's private messages into two partitions of the date set."""

    worlds: tuple[World, ...] = tuple(CANDIDATE_DATES)

    # No separate propositional atoms are needed: the complete state is already represented by the
    # Date object itself. Knowledge of the date is therefore the singleton-cell predicate below.
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
    """Interpret each line as a truthful public announcement, in dialogue order."""

    initial = _cheryl_model()

    # Albert says two things at once: his month cell is not a singleton, and every date in that cell
    # lies in a non-singleton Bernard day cell. This nested knowledge is why the first line conveys
    # more than the bare statement "Albert does not know".
    albert_first = conjunction(
        Not(KnowsWhichWorld(ALBERT)),
        Knows(ALBERT, Not(KnowsWhichWorld(BERNARD))),
    )
    after_albert, albert_trace = initial.announce(
        albert_first,
        label="Albert: I do not know, but I know Bernard does not know",
    )

    # Bernard evaluates his day information after hearing Albert. Singleton day cells now correspond
    # to July 16, August 15, and August 17; both dates numbered 14 remain indistinguishable.
    after_bernard, bernard_trace = after_albert.announce(
        KnowsWhichWorld(BERNARD),
        label="Bernard: Now I know",
    )
    # Albert evaluates his month information one last time. July is now a singleton and August is not.
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
