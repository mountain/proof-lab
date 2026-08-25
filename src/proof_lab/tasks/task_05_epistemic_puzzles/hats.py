"""The five-hat dialogue as a seven-world public-announcement computation.

There are three visible wearers, two black hats, and three white hats. Writing ``True`` for black,
a world is ``(alice, bob, carol)``. The inventory forbids only ``(True, True, True)``, so the initial
model has seven worlds. Alice sees Bob and Carol; Bob sees Carol; Carol sees nobody ahead.

The dialogue is interesting because a statement about *ignorance* is informative:

* Alice's "I do not know" removes the single world where Bob and Carol are both black. Had she seen
  those hats, the inventory would force her own hat to be white. The model goes ``7 -> 6``.
* In that reduced model, if Carol were black, Bob would know that he is white. Bob's "I do not know"
  therefore removes every remaining Carol-black world. The model goes ``6 -> 4``.
* Carol is white in all four survivors.

This module is the executable justification for Task 4's epistemic bridge. Task 4 alone emits a
Metamath theorem; this finite model stays on the disclosed computational side of the trust boundary.
The general semantic background is documented in ``tasks/task_05_epistemic_puzzles/REFERENCES.md``.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TypeAlias

from proof_lab.epistemic import (
    AnnouncementTrace,
    Atom,
    FiniteModel,
    Implies,
    Knows,
    Not,
    World,
    knows_whether,
    relation_from_observations,
)

HatWorld: TypeAlias = tuple[bool, bool, bool]

ALICE = "alice"
BOB = "bob"
CAROL = "carol"
ALICE_BLACK = "alice_black"
BOB_BLACK = "bob_black"
CAROL_BLACK = "carol_black"


@dataclass(frozen=True)
class FiveHatOutcome:
    initial: FiniteModel
    after_alice: FiniteModel
    after_bob: FiniteModel
    traces: tuple[AnnouncementTrace, ...]
    bridge_holds: bool


def _hat_model() -> FiniteModel:
    """Build the initial model from inventory and lines of sight."""

    # Enumerating instead of hand-listing the worlds makes the inventory rule reviewable: all
    # 2^3 colorings are considered, and only the impossible all-black coloring is rejected.
    hat_worlds = tuple(
        (alice, bob, carol)
        for alice in (False, True)
        for bob in (False, True)
        for carol in (False, True)
        if not (alice and bob and carol)
    )
    worlds: tuple[World, ...] = tuple(hat_worlds)
    valuations: dict[World, frozenset[str]] = {}
    alice_observations: dict[World, Hashable] = {}
    bob_observations: dict[World, Hashable] = {}
    carol_observations: dict[World, Hashable] = {}

    for world in hat_worlds:
        alice, bob, carol = world
        atoms = {
            atom
            for atom, present in (
                (ALICE_BLACK, alice),
                (BOB_BLACK, bob),
                (CAROL_BLACK, carol),
            )
            if present
        }
        valuations[world] = frozenset(atoms)
        # An observation is exactly the data the wearer can see. Equal observation keys become one
        # information cell in ``relation_from_observations``.
        alice_observations[world] = (bob, carol)
        bob_observations[world] = carol
        carol_observations[world] = "no-visible-hats"

    accessibility = {
        ALICE: relation_from_observations(worlds, alice_observations),
        BOB: relation_from_observations(worlds, bob_observations),
        CAROL: relation_from_observations(worlds, carol_observations),
    }
    return FiniteModel(worlds, valuations, accessibility)


def solve_five_hat_semantics() -> FiveHatOutcome:
    """Replay the two public statements and expose the audited bridge and trace."""

    initial = _hat_model()

    # ``knows_whether(Alice, AliceBlack)`` means Alice knows either color. Negating it expresses
    # her truthful first sentence and removes precisely the worlds in which her view is decisive.
    alice_unknown = Not(knows_whether(ALICE, Atom(ALICE_BLACK)))
    after_alice, alice_trace = initial.announce(
        alice_unknown,
        label="Alice: I do not know my hat color",
    )

    # This is the exact semantic bridge assumed by the Task 4 propositional proof. Checking it at
    # every world after Alice's announcement upgrades the bridge from prose to exhaustive evidence.
    bridge = Implies(
        Atom(CAROL_BLACK),
        Knows(BOB, Not(Atom(BOB_BLACK))),
    )
    bridge_holds = all(after_alice.holds(world, bridge) for world in after_alice.worlds)

    # Bob's ignorance is evaluated in the *updated* model. That temporal ordering is the point of
    # public-announcement semantics: the same sentence can have a different extension after news.
    bob_unknown = Not(knows_whether(BOB, Atom(BOB_BLACK)))
    after_bob, bob_trace = after_alice.announce(
        bob_unknown,
        label="Bob: I do not know my hat color",
    )
    return FiveHatOutcome(
        initial=initial,
        after_alice=after_alice,
        after_bob=after_bob,
        traces=(alice_trace, bob_trace),
        bridge_holds=bridge_holds,
    )


__all__ = ["FiveHatOutcome", "HatWorld", "solve_five_hat_semantics"]
