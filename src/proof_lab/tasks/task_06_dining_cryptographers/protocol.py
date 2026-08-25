"""The Dining Cryptographers protocol as a finite, executable security argument.

The story
=========

Three cryptographers finish dinner. Either the NSA paid, or exactly one cryptographer did. They
want to learn *which of those two cases* occurred without revealing which cryptographer paid.
Chaum's 1988 protocol [C88] gives each neighbouring pair one secret fair coin. Each diner publicly
says whether the two coins they can see are equal, except that the payer lies. An odd number of
"different" answers means a cryptographer paid; an even number means the NSA paid.

This module turns the paragraph above into a finite Kripke model. For the usual triangle there are
exactly ``4 * 2**3 = 32`` worlds:

* four possible payers: NSA, Alice, Bob, or Carol; and
* three independent shared coin bits: Alice--Bob, Bob--Carol, and Carol--Alice.

The public answer of participant ``i`` is written algebraically as

``statement_i = XOR(adjacent secret coins) XOR (i is the payer)``.

Every shared coin occurs in exactly two statements, so it cancels when all statements are XORed.
What remains is the single payer bit. This is the protocol's correctness argument in one line.

Knowledge and announcement
==========================

Before anyone speaks, a participant distinguishes worlds using only their incident coins and the
private fact "I paid". The eavesdropper distinguishes nothing. The complete three-bit transcript
is then a single truthful public announcement. Treating the simultaneous transcript as one formula
is faithful to the protocol and avoids inventing an order between the three speakers. The shared
finite S5 interpreter restricts the model to worlds with exactly that transcript.

For an odd transcript, the 32-world triangle shrinks to six worlds: two coin assignments for each
of the three possible cryptographer payers. The eavesdropper therefore learns that *someone at the
table* paid but not who. A non-paying participant also retains both other participants as payer
candidates. For an even transcript, two worlds survive and both have the NSA as payer.

Why the topology is data
========================

Security claims are often more convincing when the same executable semantics can break a bad
design. ``DISCONNECTED_TOPOLOGY`` leaves Carol without a shared coin. Her public statement then is
literally her payer bit, so an eavesdropper identifies her whenever she pays. The attack is not a
special assertion wired into the test: it is a counterexample found by running the same model over
the one-edge graph.

Evidence boundary
=================

Enumeration is exact for the declared finite models, and ``transcript_distribution`` counts the
coin assignments rather than sampling them. It therefore proves equality of the discrete
transcript distributions *within this model*, assuming independent uniform coins and truthful
execution. It does not model compromised participants, biased or reused coins, side channels,
network metadata, or Chaum's general multi-round constructions. It is computational semantic
evidence, not a theorem emitted into the repository's Metamath package.

Reference: [C88] David Chaum, "The Dining Cryptographers Problem: Unconditional Sender and
Recipient Untraceability," *Journal of Cryptology* 1(1), 1988, pp. 65--75. The primary CWI record
and a precise claim ledger live under ``tasks/task_06_dining_cryptographers``.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Hashable
from dataclasses import dataclass
from itertools import product
from typing import Literal, TypeAlias

from proof_lab.epistemic import (
    AnnouncementTrace,
    Atom,
    FiniteModel,
    Formula,
    Not,
    World,
    conjunction,
    relation_from_observations,
)

Participant: TypeAlias = Literal["alice", "bob", "carol"]
Payer: TypeAlias = Literal["nsa", "alice", "bob", "carol"]
Transcript: TypeAlias = tuple[bool, bool, bool]

ALICE: Participant = "alice"
BOB: Participant = "bob"
CAROL: Participant = "carol"
NSA: Payer = "nsa"
EAVESDROPPER = "eve"

PARTICIPANTS: tuple[Participant, ...] = (ALICE, BOB, CAROL)
PAYERS: tuple[Payer, ...] = (NSA, ALICE, BOB, CAROL)


@dataclass(frozen=True, order=True)
class KeyEdge:
    """One secret fair coin known to exactly the two endpoint participants."""

    left: Participant
    right: Participant

    def __post_init__(self) -> None:
        if self.left == self.right:
            raise ValueError("a shared-key edge must have two distinct endpoints")

    def incident_to(self, participant: Participant) -> bool:
        return participant == self.left or participant == self.right


@dataclass(frozen=True)
class ProtocolTopology:
    """The public communication graph whose edges carry independently uniform bits."""

    name: str
    edges: tuple[KeyEdge, ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("topology name must not be empty")
        undirected_edges = {frozenset((edge.left, edge.right)) for edge in self.edges}
        if len(undirected_edges) != len(self.edges):
            raise ValueError("topology must not contain duplicate undirected edges")


TRIANGLE_TOPOLOGY = ProtocolTopology(
    "three-party-cycle",
    (
        KeyEdge(ALICE, BOB),
        KeyEdge(BOB, CAROL),
        KeyEdge(CAROL, ALICE),
    ),
)

# This deliberately broken graph is an executable red-team case. Alice and Bob share one bit;
# Carol is isolated. Correctness survives because every edge bit still occurs twice, but anonymity
# does not: Carol has no mask to cancel against another public statement.
DISCONNECTED_TOPOLOGY = ProtocolTopology(
    "alice-bob-edge-with-isolated-carol",
    (KeyEdge(ALICE, BOB),),
)


@dataclass(frozen=True, order=True)
class DiningWorld:
    """A complete protocol state: who paid and the value of every topology edge bit."""

    payer: Payer
    coins: tuple[bool, ...]


@dataclass(frozen=True)
class DiningOutcome:
    """The before/after evidence for one actual execution."""

    topology: ProtocolTopology
    actual: DiningWorld
    transcript: Transcript
    initial: FiniteModel
    public: FiniteModel
    trace: AnnouncementTrace


def _xor(bits: tuple[bool, ...]) -> bool:
    """XOR a finite bit tuple; the empty XOR is false."""

    return sum(bits) % 2 == 1


def worlds_for(topology: ProtocolTopology) -> tuple[DiningWorld, ...]:
    """Enumerate every payer and every assignment of the topology's secret bits."""

    coin_assignments = tuple(product((False, True), repeat=len(topology.edges)))
    return tuple(
        DiningWorld(payer, tuple(coins))
        for payer in PAYERS
        for coins in coin_assignments
    )


def _statement_bit(
    topology: ProtocolTopology,
    world: DiningWorld,
    participant: Participant,
) -> bool:
    """Compute one public answer from precisely the private data available to its speaker."""

    incident_coins = tuple(
        world.coins[index]
        for index, edge in enumerate(topology.edges)
        if edge.incident_to(participant)
    )
    return _xor(incident_coins) ^ (world.payer == participant)


def transcript_for(topology: ProtocolTopology, world: DiningWorld) -> Transcript:
    """Return public answers in the stable order Alice, Bob, Carol."""

    if len(world.coins) != len(topology.edges):
        raise ValueError(
            f"world has {len(world.coins)} coins but topology requires {len(topology.edges)}"
        )
    return (
        _statement_bit(topology, world, ALICE),
        _statement_bit(topology, world, BOB),
        _statement_bit(topology, world, CAROL),
    )


def payer_atom(payer: Payer) -> Atom:
    """Name the proposition that a particular party paid."""

    return Atom(f"payer_{payer}")


def _transcript_atom(participant: Participant) -> Atom:
    return Atom(f"statement_{participant}_different")


def exact_transcript_formula(transcript: Transcript) -> Formula:
    """Describe all three public bits as one simultaneous truthful announcement."""

    clauses: list[Formula] = []
    for participant, bit in zip(PARTICIPANTS, transcript, strict=True):
        atom = _transcript_atom(participant)
        clauses.append(atom if bit else Not(atom))
    return conjunction(*clauses)


def _participant_observation(
    topology: ProtocolTopology,
    world: DiningWorld,
    participant: Participant,
) -> tuple[bool, tuple[bool, ...]]:
    """The private view that induces one participant's S5 information partition."""

    visible_coins = tuple(
        world.coins[index]
        for index, edge in enumerate(topology.edges)
        if edge.incident_to(participant)
    )
    return world.payer == participant, visible_coins


def protocol_model(topology: ProtocolTopology = TRIANGLE_TOPOLOGY) -> FiniteModel:
    """Build the initial model, before the public transcript is heard."""

    concrete_worlds = worlds_for(topology)
    worlds: tuple[World, ...] = tuple(concrete_worlds)

    valuations: dict[World, frozenset[str]] = {}
    for world in concrete_worlds:
        transcript = transcript_for(topology, world)
        true_atoms = {payer_atom(world.payer).name}
        true_atoms.update(
            _transcript_atom(participant).name
            for participant, bit in zip(PARTICIPANTS, transcript, strict=True)
            if bit
        )
        valuations[world] = frozenset(true_atoms)

    # Eve has no private observation before the simultaneous broadcast, so all worlds share one
    # observation key. Each participant sees only their incident coins and whether they paid.
    eve_observations: dict[World, Hashable] = {
        world: "before-public-transcript" for world in concrete_worlds
    }
    accessibility = {
        EAVESDROPPER: relation_from_observations(worlds, eve_observations),
    }
    for participant in PARTICIPANTS:
        observations: dict[World, Hashable] = {
            world: _participant_observation(topology, world, participant)
            for world in concrete_worlds
        }
        accessibility[participant] = relation_from_observations(worlds, observations)

    return FiniteModel(worlds, valuations, accessibility)


def run_protocol(
    actual: DiningWorld,
    topology: ProtocolTopology = TRIANGLE_TOPOLOGY,
) -> DiningOutcome:
    """Publish the actual transcript and return the induced epistemic submodel."""

    initial = protocol_model(topology)
    if actual not in initial.worlds:
        raise ValueError("actual world is not a world of the selected topology")
    transcript = transcript_for(topology, actual)
    public, trace = initial.announce(
        exact_transcript_formula(transcript),
        label=f"public transcript (Alice, Bob, Carol) = {transcript}",
    )
    return DiningOutcome(topology, actual, transcript, initial, public, trace)


def payer_candidates(
    model: FiniteModel,
    agent: str,
    actual: DiningWorld,
) -> frozenset[Payer]:
    """Project an agent's current information cell onto the possible payer identities."""

    candidates: set[Payer] = set()
    for candidate in model.accessible(agent, actual):
        if not isinstance(candidate, DiningWorld):
            raise TypeError("payer candidates require a DiningWorld model")
        candidates.add(candidate.payer)
    return frozenset(candidates)


def transcript_distribution(
    topology: ProtocolTopology,
    payer: Payer,
) -> Counter[Transcript]:
    """Count exact transcript multiplicities over all secret-bit assignments.

    With independent uniform edge bits, equal counts are equal probabilities. Returning integer
    multiplicities keeps the evidence exact and avoids floating-point or Monte Carlo claims.
    """

    counts: Counter[Transcript] = Counter()
    for world in worlds_for(topology):
        if world.payer == payer:
            counts[transcript_for(topology, world)] += 1
    return counts


def outsider_anonymity_breaches(
    topology: ProtocolTopology,
) -> tuple[DiningOutcome, ...]:
    """Return every cryptographer-paid execution in which Eve narrows identity below all three."""

    expected = frozenset(PARTICIPANTS)
    breaches: list[DiningOutcome] = []
    for actual in worlds_for(topology):
        if actual.payer == NSA:
            continue
        outcome = run_protocol(actual, topology)
        if payer_candidates(outcome.public, EAVESDROPPER, actual) != expected:
            breaches.append(outcome)
    return tuple(breaches)


__all__ = [
    "ALICE",
    "BOB",
    "CAROL",
    "DISCONNECTED_TOPOLOGY",
    "EAVESDROPPER",
    "NSA",
    "PARTICIPANTS",
    "PAYERS",
    "TRIANGLE_TOPOLOGY",
    "DiningOutcome",
    "DiningWorld",
    "KeyEdge",
    "Participant",
    "Payer",
    "ProtocolTopology",
    "Transcript",
    "exact_transcript_formula",
    "outsider_anonymity_breaches",
    "payer_atom",
    "payer_candidates",
    "protocol_model",
    "run_protocol",
    "transcript_distribution",
    "transcript_for",
    "worlds_for",
]
