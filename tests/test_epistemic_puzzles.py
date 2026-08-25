"""Executable claims for the three public-announcement stories.

Counts make the dialogue auditable: they reveal exactly when information enters the model instead
of testing only the final answer. The muddy suite goes further and visits every nonempty actual
assignment through five children.
"""

from math import comb
from itertools import combinations

from proof_lab.epistemic import Atom, Not
from proof_lab.tasks.task_05_epistemic_puzzles import (
    CHERYL_SOLUTION,
    solve_cheryl_birthday,
    solve_five_hat_semantics,
    solve_muddy_children,
)


def test_five_hat_public_announcements_validate_the_bridge_and_conclusion() -> None:
    """Alice removes one world; Bob removes the Carol-black layer; Carol must be white."""

    outcome = solve_five_hat_semantics()

    assert tuple((trace.before_count, trace.after_count) for trace in outcome.traces) == (
        (7, 6),
        (6, 4),
    )
    assert outcome.bridge_holds
    assert all(
        outcome.after_bob.holds(world, Not(Atom("carol_black")))
        for world in outcome.after_bob.worlds
    )


def test_cheryl_birthday_has_the_standard_unique_solution() -> None:
    """The three dialogue lines shrink ten dates to five, three, and finally July 16."""

    outcome = solve_cheryl_birthday()

    assert tuple((trace.before_count, trace.after_count) for trace in outcome.traces) == (
        (10, 5),
        (5, 3),
        (3, 1),
    )
    assert outcome.solution == CHERYL_SOLUTION
    assert str(outcome.solution) == "July 16"


def test_muddy_children_eliminate_one_cardinality_layer_per_no_round() -> None:
    """Every nonempty assignment through n=5 follows the cardinality-layer argument."""

    for child_count in range(1, 6):
        for muddy_count in range(1, child_count + 1):
            for muddy_children in combinations(range(child_count), muddy_count):
                actual = frozenset(muddy_children)
                outcome = solve_muddy_children(child_count, actual)

                assert len(outcome.traces) == muddy_count
                assert outcome.traces[0].after_count == 2**child_count - 1
                for no_round, trace in enumerate(outcome.traces[1:], start=1):
                    # After round r, exactly the worlds with more than r muddy children survive.
                    expected = sum(
                        comb(child_count, size)
                        for size in range(no_round + 1, child_count + 1)
                    )
                    assert trace.after_count == expected
