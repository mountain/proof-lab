"""Small semantic laws that make the puzzle traces meaningful.

Puzzle-specific expected answers are not enough: a broken relation or announcement evaluator could
make all three examples agree by accident. These tests therefore isolate the reusable mechanisms.
"""

from collections.abc import Hashable

import pytest

from proof_lab.epistemic import (
    Atom,
    FiniteModel,
    Knows,
    KnowsWhichWorld,
    ModelInvariantError,
    Not,
    World,
    knows_whether,
    relation_from_observations,
)


def test_public_announcement_restricts_worlds_and_information_cells() -> None:
    """Publicly learning ``p`` turns a two-world uncertainty cell into knowledge of ``p``."""

    worlds: tuple[World, ...] = ("p", "not-p")
    valuations: dict[World, frozenset[str]] = {
        "p": frozenset(("p",)),
        "not-p": frozenset(),
    }
    observations: dict[World, Hashable] = {"p": "same", "not-p": "same"}
    model = FiniteModel(
        worlds,
        valuations,
        {"agent": relation_from_observations(worlds, observations)},
    )

    assert model.holds("p", Atom("p"))
    assert not model.holds("p", Knows("agent", Atom("p")))
    assert not model.holds("p", knows_whether("agent", Atom("p")))

    restricted, trace = model.announce(Atom("p"), label="p is publicly announced")

    assert trace.before == worlds
    assert trace.after == ("p",)
    assert trace.eliminated == ("not-p",)
    assert restricted.holds("p", Knows("agent", Atom("p")))
    assert restricted.holds("p", KnowsWhichWorld("agent"))


def test_model_rejects_non_reflexive_accessibility() -> None:
    """The engine refuses a relation that is not S5 instead of evaluating a misleading model."""

    with pytest.raises(ModelInvariantError, match="not reflexive"):
        FiniteModel(
            ("w",),
            {"w": frozenset()},
            {"agent": {"w": frozenset()}},
        )


def test_unknown_world_and_agent_are_rejected() -> None:
    """Misspelled model coordinates fail loudly rather than producing a truth value."""

    model = FiniteModel(
        ("w",),
        {"w": frozenset()},
        {"agent": {"w": frozenset(("w",))}},
    )

    with pytest.raises(KeyError, match="unknown agent"):
        model.holds("w", Knows("nobody", Atom("p")))
    with pytest.raises(KeyError, match="not in the model"):
        model.holds("missing", Not(Atom("p")))
