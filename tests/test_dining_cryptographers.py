"""Executable claims for Task 6: correctness, anonymity, distribution, and attack.

The tests deliberately range over complete finite state spaces. There is no random seed and no
sampling error: the triangle has 32 worlds, while the disconnected red-team graph has 8.
"""

from proof_lab.epistemic import Knows, Not
from proof_lab.tasks.task_06_dining_cryptographers.demo import render_demo_report
from proof_lab.tasks.task_06_dining_cryptographers.protocol import (
    CAROL,
    DISCONNECTED_TOPOLOGY,
    EAVESDROPPER,
    NSA,
    PARTICIPANTS,
    TRIANGLE_TOPOLOGY,
    DiningWorld,
    outsider_anonymity_breaches,
    payer_atom,
    payer_candidates,
    run_protocol,
    transcript_distribution,
    transcript_for,
    worlds_for,
)


def _parity(transcript: tuple[bool, bool, bool]) -> bool:
    return sum(transcript) % 2 == 1


def test_triangle_correctness_is_exhaustive_and_epistemic() -> None:
    """Transcript parity is right in all 32 worlds, and Eve knows the resulting case."""

    worlds = worlds_for(TRIANGLE_TOPOLOGY)
    assert len(worlds) == 32

    for actual in worlds:
        outcome = run_protocol(actual)
        cryptographer_paid = actual.payer != NSA

        # Algebraic correctness: the three public bits have odd parity exactly when one diner paid.
        assert _parity(outcome.transcript) is cryptographer_paid
        assert outcome.trace.before_count == 32
        assert outcome.trace.after_count == (6 if cryptographer_paid else 2)

        # Epistemic correctness: after hearing the transcript, even an outsider knows which case
        # occurred. This is stronger evidence than checking parity only at the actual world.
        nsa_paid = payer_atom(NSA)
        expected_knowledge = Not(nsa_paid) if cryptographer_paid else nsa_paid
        assert outcome.public.holds(
            actual,
            Knows(EAVESDROPPER, expected_knowledge),
        )


def test_triangle_hides_a_cryptographer_payer_from_the_outsider() -> None:
    """Every odd transcript leaves Alice, Bob, and Carol as Eve's exact candidate set."""

    for actual in worlds_for(TRIANGLE_TOPOLOGY):
        outcome = run_protocol(actual)
        candidates = payer_candidates(outcome.public, EAVESDROPPER, actual)
        if actual.payer == NSA:
            assert candidates == frozenset((NSA,))
        else:
            assert candidates == frozenset(PARTICIPANTS)

    assert outsider_anonymity_breaches(TRIANGLE_TOPOLOGY) == ()


def test_triangle_hides_the_payer_from_each_non_paying_participant() -> None:
    """A payer knows their own act; each non-payer retains exactly the other two diners."""

    for actual in worlds_for(TRIANGLE_TOPOLOGY):
        if actual.payer == NSA:
            continue
        outcome = run_protocol(actual)
        for observer in PARTICIPANTS:
            candidates = payer_candidates(outcome.public, observer, actual)
            if observer == actual.payer:
                assert candidates == frozenset((observer,))
            else:
                assert candidates == frozenset(
                    participant for participant in PARTICIPANTS if participant != observer
                )


def test_triangle_transcript_distributions_are_exactly_equal_between_diners() -> None:
    """Uniform secret coins give every odd transcript multiplicity two for every diner."""

    participant_distributions = tuple(
        transcript_distribution(TRIANGLE_TOPOLOGY, participant)
        for participant in PARTICIPANTS
    )
    first = participant_distributions[0]

    assert all(distribution == first for distribution in participant_distributions[1:])
    assert len(first) == 4
    assert set(first.values()) == {2}
    assert all(_parity(transcript) for transcript in first)

    # NSA-paid executions occupy the complementary even-parity support, also with exact
    # multiplicity two. This makes explicit what the protocol intentionally reveals.
    nsa_distribution = transcript_distribution(TRIANGLE_TOPOLOGY, NSA)
    assert len(nsa_distribution) == 4
    assert set(nsa_distribution.values()) == {2}
    assert all(not _parity(transcript) for transcript in nsa_distribution)


def test_disconnected_graph_produces_an_explicit_anonymity_attack() -> None:
    """With Carol isolated, her statement equals her payer bit and Eve identifies her."""

    worlds = worlds_for(DISCONNECTED_TOPOLOGY)
    assert len(worlds) == 8

    carol_worlds = tuple(world for world in worlds if world.payer == CAROL)
    assert carol_worlds == (
        DiningWorld(CAROL, (False,)),
        DiningWorld(CAROL, (True,)),
    )
    for actual in carol_worlds:
        outcome = run_protocol(actual, DISCONNECTED_TOPOLOGY)
        assert transcript_for(DISCONNECTED_TOPOLOGY, actual)[2]
        assert payer_candidates(outcome.public, EAVESDROPPER, actual) == frozenset((CAROL,))
        assert outcome.public.holds(
            actual,
            Knows(EAVESDROPPER, payer_atom(CAROL)),
        )

    # The generic breach search also finds every cryptographer-paid execution on this graph:
    # Alice and Bob retain only one another as candidates, while Carol is identified uniquely.
    breaches = outsider_anonymity_breaches(DISCONNECTED_TOPOLOGY)
    assert len(breaches) == 6
    assert {breach.actual for breach in breaches} == {
        world for world in worlds if world.payer != NSA
    }


def test_human_readable_demo_report_is_derived_from_the_same_checks() -> None:
    """The command-line view exposes the two audit outcomes without a second model."""

    report = render_demo_report()

    assert "correct transcript parity: 32/32 worlds" in report
    assert "Alice example: 100, restriction 32->6" in report
    assert "Eve candidates = {Alice, Bob, Carol}" in report
    assert "Alice/Bob/Carol transcript distributions equal: True" in report
    assert "odd-transcript multiplicities: [2, 2, 2, 2]" in report
    assert "red-team topology: alice-bob-edge-with-isolated-carol" in report
    assert "outsider-anonymity breaches: 6" in report
    assert "Carol witness: 001, Eve candidates = {Carol}" in report
