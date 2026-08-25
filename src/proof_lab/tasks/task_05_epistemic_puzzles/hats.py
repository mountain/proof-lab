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
    initial = _hat_model()
    alice_unknown = Not(knows_whether(ALICE, Atom(ALICE_BLACK)))
    after_alice, alice_trace = initial.announce(
        alice_unknown,
        label="Alice: I do not know my hat color",
    )

    bridge = Implies(
        Atom(CAROL_BLACK),
        Knows(BOB, Not(Atom(BOB_BLACK))),
    )
    bridge_holds = all(after_alice.holds(world, bridge) for world in after_alice.worlds)

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
