"""Static admission checks for the kernel-bound part of Task 6.

The package build is the authoritative proof test. These smaller checks keep the trust boundary
visible even before the comparatively expensive Metamath run starts.
"""

from pathlib import Path

import proof_lab.tasks.task_06_dining_cryptographers as task_06_package
from proof_lab.registry import PACKAGE_TASK_IDS, TASKS
from proof_lab.tasks.task_06_dining_cryptographers.proofs import formal_transcript_bits
from proof_lab.tasks.task_06_dining_cryptographers.protocol import (
    TRIANGLE_TOPOLOGY,
    transcript_for,
    worlds_for,
)

REPOSITORY_ROOT = Path(__file__).parents[1]
PROOF_SOURCE = (
    REPOSITORY_ROOT
    / "src/proof_lab/tasks/task_06_dining_cryptographers/proofs/finite_tables.py"
)
PACKAGE_INIT = (
    REPOSITORY_ROOT
    / "src/proof_lab/tasks/task_06_dining_cryptographers/__init__.py"
)


def test_task_06_admits_two_named_proof_roots() -> None:
    task = TASKS["task_06"]

    assert "task_06" in PACKAGE_TASK_IDS
    assert task.buildable
    assert tuple((proof.theorem, proof.role) for proof in task.proofs) == (
        ("dc_parity_table", "exhaustive-protocol-correctness-table"),
        ("dc_payer_bijection_table", "exhaustive-transcript-bijection-table"),
    )


def test_task_06_proofs_have_no_raw_steps_or_self_reference() -> None:
    source = PROOF_SOURCE.read_text(encoding="utf-8")

    assert ".raw(" not in source
    assert 'ref="dc_parity_table"' not in source
    assert 'ref="dc_payer_bijection_table"' not in source
    assert 'ref="df-xor"' in source
    assert 'ref="pm3.2i"' in source


def test_formal_import_boundary_does_not_execute_the_semantic_model() -> None:
    package_source = PACKAGE_INIT.read_text(encoding="utf-8")

    assert "from .protocol import" not in package_source
    assert "from .demo import" not in package_source


def test_lazy_package_facade_preserves_the_existing_protocol_api() -> None:
    assert task_06_package.ALICE == "alice"
    assert task_06_package.render_demo_report().startswith(
        "Dining Cryptographers — exhaustive finite audit\n"
    )


def test_formal_table_and_semantic_model_agree_in_all_32_worlds() -> None:
    """Audit the one semantic bridge that a propositional truth table cannot state itself."""

    worlds = worlds_for(TRIANGLE_TOPOLOGY)
    assert len(worlds) == 32
    for world in worlds:
        assert len(world.coins) == 3
        coins = (world.coins[0], world.coins[1], world.coins[2])
        assert formal_transcript_bits(world.payer, coins) == transcript_for(
            TRIANGLE_TOPOLOGY,
            world,
        )
