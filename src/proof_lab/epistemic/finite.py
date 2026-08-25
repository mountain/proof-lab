"""Finite epistemic models, written as a small executable essay.

Why this module exists
======================

The puzzle programs need to distinguish three things that ordinary propositional logic
collapses together:

1. a fact is true at the actual world;
2. an agent knows that fact because it is true at every world the agent still considers
   possible; and
3. a public statement changes knowledge by deleting worlds for everybody at once.

The standard mathematical object is a Kripke model ``M = (W, R, V)``. ``W`` is a finite set of
possible worlds, ``R_i`` records which worlds agent ``i`` cannot distinguish, and ``V`` records
the atomic facts true at each world. We use S5 information: each ``R_i`` is an equivalence
relation. This is the usual ideal-agent interpretation in epistemic logic [FHMMV95, VDK07].

The two semantic clauses that do the real work are implemented almost verbatim below::

    M, w |= K_i phi       iff M, v |= phi for every v with w R_i v
    M|alpha               =   M restricted to worlds satisfying alpha

The second clause is a truthful public announcement in the sense introduced by Plaza [P89].
It is *not* an assignment that makes ``alpha`` true: it removes the worlds where ``alpha`` was
false and restricts every information cell to the surviving worlds.

Reading map
===========

``Formula`` and its dataclasses are syntax. ``FiniteModel.holds`` is the interpreter.
``FiniteModel.announce`` is model change. ``relation_from_observations`` turns a concrete
observation—such as "the month Albert heard"—into an S5 relation. The puzzle modules then only
have to say what the worlds and observations are.

Trust boundary
==============

This is executable semantic evidence, deliberately not imported by ``proof_lab.build``. The
Metamath verifier therefore certifies Task 4's lowered propositional theorem, not this Python
interpreter. See ``tasks/task_05_epistemic_puzzles/REFERENCES.md`` for full references and
``reports/semantic-boundary.md`` for the precise evidence claim.
"""

from __future__ import annotations

from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass
from typing import TypeAlias

Agent: TypeAlias = str
World: TypeAlias = Hashable


class ModelInvariantError(ValueError):
    """Raised when a finite epistemic model is not a well-formed S5 model."""


class Formula:
    """Marker base class for syntax trees interpreted by :meth:`FiniteModel.holds`.

    Formula objects intentionally contain no evaluation logic. Keeping syntax as inert data makes
    the recursive semantic clauses in ``holds`` visible in one place and easy to audit.
    """


@dataclass(frozen=True)
class Top(Formula):
    """Truth."""


@dataclass(frozen=True)
class Bottom(Formula):
    """Falsity."""


@dataclass(frozen=True)
class Atom(Formula):
    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("atom name must not be empty")


@dataclass(frozen=True)
class Not(Formula):
    operand: Formula


@dataclass(frozen=True)
class And(Formula):
    operands: tuple[Formula, ...]


@dataclass(frozen=True)
class Or(Formula):
    operands: tuple[Formula, ...]


@dataclass(frozen=True)
class Implies(Formula):
    antecedent: Formula
    consequent: Formula


@dataclass(frozen=True)
class Knows(Formula):
    agent: Agent
    operand: Formula

    def __post_init__(self) -> None:
        if not self.agent:
            raise ValueError("knowledge agent must not be empty")


@dataclass(frozen=True)
class KnowsWhichWorld(Formula):
    """The agent's current information cell is a singleton.

    In a finite model this abbreviates knowing the complete state: the current information cell
    contains only the actual world. It is useful for Cheryl's Birthday, where worlds *are* dates.

    This is a convenience predicate rather than a new modal operator. In a fully propositional
    encoding it could be expanded into knowledge of a complete description of the current world.
    """

    agent: Agent

    def __post_init__(self) -> None:
        if not self.agent:
            raise ValueError("knowledge agent must not be empty")


def conjunction(*operands: Formula) -> Formula:
    if not operands:
        return Top()
    if len(operands) == 1:
        return operands[0]
    return And(tuple(operands))


def disjunction(*operands: Formula) -> Formula:
    if not operands:
        return Bottom()
    if len(operands) == 1:
        return operands[0]
    return Or(tuple(operands))


def knows_whether(agent: Agent, proposition: Formula) -> Formula:
    """Return ``K_i p or K_i not-p``."""
    return disjunction(Knows(agent, proposition), Knows(agent, Not(proposition)))


@dataclass(frozen=True)
class AnnouncementTrace:
    """An audit record for one public announcement.

    Deterministic world ordering is retained so that a reader can inspect not only the counts but
    also the exact alternatives removed by a line of dialogue.
    """

    label: str
    before: tuple[World, ...]
    after: tuple[World, ...]
    eliminated: tuple[World, ...]

    @property
    def before_count(self) -> int:
        return len(self.before)

    @property
    def after_count(self) -> int:
        return len(self.after)


@dataclass(frozen=True)
class FiniteModel:
    """A finite multi-agent Kripke model with S5 accessibility relations.

    Construction is deliberately strict. A malformed relation can make a knowledge puzzle appear
    to work for accidental reasons, so every model validates its complete world table and all three
    equivalence-relation laws before any formula is evaluated.
    """

    worlds: tuple[World, ...]
    valuations: Mapping[World, frozenset[str]]
    accessibility: Mapping[Agent, Mapping[World, frozenset[World]]]

    def __post_init__(self) -> None:
        # First audit the database-like part of the model. A world must occur exactly once, and its
        # valuation must be neither missing nor silently supplied for a world outside ``W``.
        world_set = set(self.worlds)
        if len(world_set) != len(self.worlds):
            raise ModelInvariantError("worlds must be unique")
        if set(self.valuations) != world_set:
            raise ModelInvariantError("valuations must be defined for exactly the model worlds")

        # Next audit each agent's indistinguishability relation. Reflexive + symmetric + transitive
        # is the S5/equivalence-relation condition. The nested checks are intentionally explicit:
        # these models are tiny, while readable failure messages are valuable evidence.
        for agent, relation in self.accessibility.items():
            if not agent:
                raise ModelInvariantError("agent names must not be empty")
            if set(relation) != world_set:
                raise ModelInvariantError(
                    f"accessibility for {agent!r} must be defined for every world"
                )
            for world, targets in relation.items():
                if not targets <= world_set:
                    raise ModelInvariantError(
                        f"accessibility for {agent!r} leaves the model at {world!r}"
                    )
                if world not in targets:
                    raise ModelInvariantError(
                        f"accessibility for {agent!r} is not reflexive at {world!r}"
                    )
                for target in targets:
                    if world not in relation[target]:
                        raise ModelInvariantError(
                            f"accessibility for {agent!r} is not symmetric"
                        )
                    if not relation[target] <= targets:
                        raise ModelInvariantError(
                            f"accessibility for {agent!r} is not transitive"
                        )

    @property
    def agents(self) -> tuple[Agent, ...]:
        return tuple(self.accessibility)

    def accessible(self, agent: Agent, world: World) -> frozenset[World]:
        try:
            relation = self.accessibility[agent]
        except KeyError as exc:
            raise KeyError(f"unknown agent {agent!r}") from exc
        try:
            return relation[world]
        except KeyError as exc:
            raise KeyError(f"world {world!r} is not in the model") from exc

    def holds(self, world: World, formula: Formula) -> bool:
        """Evaluate ``formula`` at ``world`` by structural recursion.

        The propositional cases follow their ordinary truth tables. The ``Knows`` case is the
        Kripke clause from the module introduction: universal truth over the agent's current
        information cell. Because S5 relations are reflexive, knowing ``phi`` also entails that
        ``phi`` is true at the current world.
        """
        if world not in self.valuations:
            raise KeyError(f"world {world!r} is not in the model")

        if isinstance(formula, Top):
            return True
        if isinstance(formula, Bottom):
            return False
        if isinstance(formula, Atom):
            return formula.name in self.valuations[world]
        if isinstance(formula, Not):
            return not self.holds(world, formula.operand)
        if isinstance(formula, And):
            return all(self.holds(world, operand) for operand in formula.operands)
        if isinstance(formula, Or):
            return any(self.holds(world, operand) for operand in formula.operands)
        if isinstance(formula, Implies):
            return not self.holds(world, formula.antecedent) or self.holds(
                world, formula.consequent
            )
        if isinstance(formula, Knows):
            # This universal quantifier is the epistemic heart of the interpreter.
            return all(
                self.holds(candidate, formula.operand)
                for candidate in self.accessible(formula.agent, world)
            )
        if isinstance(formula, KnowsWhichWorld):
            return self.accessible(formula.agent, world) == frozenset((world,))
        raise TypeError(f"unsupported formula type: {type(formula).__name__}")

    def satisfying_worlds(self, formula: Formula) -> tuple[World, ...]:
        return tuple(world for world in self.worlds if self.holds(world, formula))

    def announce(
        self,
        formula: Formula,
        *,
        label: str,
    ) -> tuple[FiniteModel, AnnouncementTrace]:
        """Return the Plaza-style restriction of the model to worlds satisfying ``formula``.

        Truthfulness is represented by filtering, not mutation: worlds that already satisfy the
        announcement survive. Accessibility is then restricted to those survivors, which changes
        what agents know. The original model remains available for before/after comparison.
        """
        if not label:
            raise ValueError("announcement label must not be empty")

        # Phase 1: determine the public content extension ``[[formula]]_M`` in the old model.
        kept = self.satisfying_worlds(formula)
        kept_set = set(kept)
        eliminated = tuple(world for world in self.worlds if world not in kept_set)

        # Phase 2: take the induced submodel. We do not recompute observations; we intersect every
        # old information cell with the surviving world set, exactly as public-announcement
        # semantics requires.
        valuations = {world: self.valuations[world] for world in kept}
        accessibility = {
            agent: {
                world: frozenset(candidate for candidate in relation[world] if candidate in kept_set)
                for world in kept
            }
            for agent, relation in self.accessibility.items()
        }
        restricted = FiniteModel(kept, valuations, accessibility)
        trace = AnnouncementTrace(label, self.worlds, kept, eliminated)
        return restricted, trace


def relation_from_observations(
    worlds: Sequence[World],
    observations: Mapping[World, Hashable],
) -> dict[World, frozenset[World]]:
    """Construct the S5 equivalence relation induced by an observation key.

    Two worlds are related exactly when the agent receives the same observation in both. Equality
    of observation keys is automatically reflexive, symmetric, and transitive, so this helper turns
    concrete puzzle visibility rules into a correct S5 relation by construction.
    """
    ordered_worlds = tuple(worlds)
    if set(observations) != set(ordered_worlds):
        raise ModelInvariantError("observations must be defined for exactly the model worlds")
    return {
        world: frozenset(
            candidate
            for candidate in ordered_worlds
            if observations[candidate] == observations[world]
        )
        for world in ordered_worlds
    }


__all__ = [
    "Agent",
    "And",
    "AnnouncementTrace",
    "Atom",
    "Bottom",
    "FiniteModel",
    "Formula",
    "Implies",
    "Knows",
    "KnowsWhichWorld",
    "ModelInvariantError",
    "Not",
    "Or",
    "Top",
    "World",
    "conjunction",
    "disjunction",
    "knows_whether",
    "relation_from_observations",
]
