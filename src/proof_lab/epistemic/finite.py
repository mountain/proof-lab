"""A minimal finite S5 model with public-announcement updates.

This module is executable semantic evidence. It is deliberately not imported by
``proof_lab.build`` and is not part of the Metamath verifier's trust boundary.
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
    """Marker base class for the finite epistemic formula language."""


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

    In a finite model this abbreviates knowing the complete state. It is useful for
    puzzles such as Cheryl's Birthday, whose question is which candidate world is actual.
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
    """A finite multi-agent Kripke model with S5 accessibility relations."""

    worlds: tuple[World, ...]
    valuations: Mapping[World, frozenset[str]]
    accessibility: Mapping[Agent, Mapping[World, frozenset[World]]]

    def __post_init__(self) -> None:
        world_set = set(self.worlds)
        if len(world_set) != len(self.worlds):
            raise ModelInvariantError("worlds must be unique")
        if set(self.valuations) != world_set:
            raise ModelInvariantError("valuations must be defined for exactly the model worlds")

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
        """Restrict the model to worlds satisfying a truthful public announcement."""
        if not label:
            raise ValueError("announcement label must not be empty")

        kept = self.satisfying_worlds(formula)
        kept_set = set(kept)
        eliminated = tuple(world for world in self.worlds if world not in kept_set)
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
    """Construct the S5 equivalence relation induced by an observation key."""
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
