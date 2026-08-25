"""Render a compact, deterministic audit report from the exhaustive model.

The semantic functions remain the source of evidence; this module is only a reader-friendly view
over their results. Keeping presentation separate avoids hiding security checks inside print code.
"""

from __future__ import annotations

from .protocol import (
    ALICE,
    CAROL,
    DISCONNECTED_TOPOLOGY,
    EAVESDROPPER,
    NSA,
    PARTICIPANTS,
    TRIANGLE_TOPOLOGY,
    DiningWorld,
    outsider_anonymity_breaches,
    payer_candidates,
    run_protocol,
    transcript_distribution,
    transcript_for,
    worlds_for,
)


def _render_bits(bits: tuple[bool, bool, bool]) -> str:
    return "".join("1" if bit else "0" for bit in bits)


def _render_payers(payers: frozenset[str]) -> str:
    return ", ".join(participant.title() for participant in PARTICIPANTS if participant in payers)


def render_demo_report() -> str:
    """Compute and render the standard proof obligations and the red-team witness."""

    standard_worlds = worlds_for(TRIANGLE_TOPOLOGY)
    correct_world_count = sum(
        (sum(transcript_for(TRIANGLE_TOPOLOGY, world)) % 2 == 1)
        == (world.payer != NSA)
        for world in standard_worlds
    )
    standard_breaches = outsider_anonymity_breaches(TRIANGLE_TOPOLOGY)

    nsa_example = DiningWorld(NSA, (False, False, False))
    alice_example = DiningWorld(ALICE, (False, False, False))
    nsa_outcome = run_protocol(nsa_example)
    alice_outcome = run_protocol(alice_example)
    alice_candidates = payer_candidates(
        alice_outcome.public,
        EAVESDROPPER,
        alice_example,
    )

    distributions = tuple(
        transcript_distribution(TRIANGLE_TOPOLOGY, participant)
        for participant in PARTICIPANTS
    )
    equal_distributions = all(
        distribution == distributions[0] for distribution in distributions[1:]
    )

    broken_worlds = worlds_for(DISCONNECTED_TOPOLOGY)
    broken_breaches = outsider_anonymity_breaches(DISCONNECTED_TOPOLOGY)
    carol_witness = DiningWorld(CAROL, (False,))
    carol_outcome = run_protocol(carol_witness, DISCONNECTED_TOPOLOGY)
    carol_candidates = payer_candidates(
        carol_outcome.public,
        EAVESDROPPER,
        carol_witness,
    )

    lines = (
        "Dining Cryptographers — exhaustive finite audit",
        "",
        f"standard topology: {TRIANGLE_TOPOLOGY.name}",
        f"worlds: {len(standard_worlds)}",
        f"correct transcript parity: {correct_world_count}/{len(standard_worlds)} worlds",
        f"outsider-anonymity breaches: {len(standard_breaches)}",
        (
            f"NSA example: {_render_bits(nsa_outcome.transcript)}, "
            f"restriction {nsa_outcome.trace.before_count}->{nsa_outcome.trace.after_count}"
        ),
        (
            f"Alice example: {_render_bits(alice_outcome.transcript)}, "
            f"restriction {alice_outcome.trace.before_count}->{alice_outcome.trace.after_count}, "
            f"Eve candidates = {{{_render_payers(alice_candidates)}}}"
        ),
        f"Alice/Bob/Carol transcript distributions equal: {equal_distributions}",
        f"odd-transcript multiplicities: {sorted(distributions[0].values())}",
        "",
        f"red-team topology: {DISCONNECTED_TOPOLOGY.name}",
        f"worlds: {len(broken_worlds)}",
        f"outsider-anonymity breaches: {len(broken_breaches)}",
        (
            f"Carol witness: {_render_bits(carol_outcome.transcript)}, "
            f"Eve candidates = {{{_render_payers(carol_candidates)}}}"
        ),
    )
    return "\n".join(lines)


def main() -> None:
    """Print the deterministic report for ``python -m`` users."""

    print(render_demo_report())


__all__ = ["main", "render_demo_report"]
