"""Metamath proofs for the two finite algebraic tables behind Task 6.

Why a second representation exists
==================================

``protocol.py`` is an epistemic model checker. Its Python booleans are useful evidence, but they
are not proof objects. This module restates the protocol table in the propositional language owned
by ``metamath-logic`` and constructs every row from kernel-checkable XOR lemmas.

There are two exported theorems:

``dc_parity_table``
    A conjunction of all 32 ground protocol rows. Each conjunct says that the XOR of Alice's,
    Bob's, and Carol's announcements is equivalent to the bit "a cryptographer paid".

``dc_payer_bijection_table``
    A conjunction of 24 transcript-equality rows. Moving the payer across one shared edge while
    toggling that edge's coin preserves all three public statements. The toggle is an involution,
    so these rows exhibit the exact finite bijections Alice <-> Bob, Bob <-> Carol, and
    Carol <-> Alice used by the distributional anonymity argument.

No step uses ``raw`` and neither theorem assumes a protocol-specific hypothesis. A true bit is the
theorem ``phi -> phi``; a false bit is its negation. Internal XOR nodes are proved directly from
``df-xor``: equal child values give a biconditional and hence a false XOR via ``xnor``; unequal
values refute the biconditional and hence prove the XOR. ``pm3.2i`` then joins independently proved
rows into the exported conjunction.

This is intentionally a *finite table proof*, not yet a native modal proof. Metamath checks every
Boolean row. The correspondence between a table position and an epistemic-world description is
still audited by Python bridge tests and readable definitions below. Knowledge and public-model
restriction remain outside the kernel until a modal-to-propositional lowering is added.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Literal, TypeAlias

from logic.propositional.hilbert import System
from skfd.authoring.formula import Wff, render as render_wff
from skfd.proof import Proof, ProofBuilder

Payer: TypeAlias = Literal["nsa", "alice", "bob", "carol"]

NSA: Payer = "nsa"
ALICE: Payer = "alice"
BOB: Payer = "bob"
CAROL: Payer = "carol"
PAYERS: tuple[Payer, ...] = (NSA, ALICE, BOB, CAROL)

CoinTriple: TypeAlias = tuple[bool, bool, bool]


@dataclass(frozen=True)
class XorExpr:
    """One binary node in the fully parenthesized propositional XOR expression."""

    left: bool | XorExpr
    right: bool | XorExpr


BitExpr: TypeAlias = bool | XorExpr


def _xor(left: BitExpr, right: BitExpr) -> XorExpr:
    return XorExpr(left, right)


def _bit(value: bool) -> str:
    # Avoid relying on truth constants here. metamath-logic 0.0.6 does not export ``df-tru`` even
    # though some catalogue truth-table lemmas depend on it. ``φ → φ`` is already an admitted
    # theorem, while its negation is refutable, so the pair is a conservative Boolean encoding.
    truth = "( φ → φ )"
    return truth if value else f"¬ {truth}"


def _render(expression: BitExpr) -> str:
    if isinstance(expression, bool):
        return _bit(expression)
    return f"( {_render(expression.left)} ⊻ {_render(expression.right)} )"


def _truth_value(expression: BitExpr) -> bool:
    """Interpret the small XOR syntax used by the Metamath table generator.

    This evaluator is deliberately tiny and independent of ``protocol.py``. Its purpose is not
    to certify the theorem—``mmverify`` does that—but to let a bridge test compare the two
    independently written descriptions of the protocol. If either description changes without
    the other, that test fails before the formal package is published.
    """

    if isinstance(expression, bool):
        return expression
    return _truth_value(expression.left) ^ _truth_value(expression.right)


def _statements(payer: Payer, coins: CoinTriple) -> tuple[BitExpr, BitExpr, BitExpr]:
    """Spell out Chaum's three public bits without calling the Python semantic model.

    Coin order is AB, BC, CA. Each shared coin therefore occurs at exactly two endpoints. The payer
    bit toggles only that participant's statement.
    """

    coin_ab, coin_bc, coin_ca = coins
    return (
        _xor(_xor(coin_ab, coin_ca), payer == ALICE),
        _xor(_xor(coin_ab, coin_bc), payer == BOB),
        _xor(_xor(coin_bc, coin_ca), payer == CAROL),
    )


def formal_transcript_bits(payer: Payer, coins: CoinTriple) -> tuple[bool, bool, bool]:
    """Expose the table generator's three ground bits for cross-model auditing.

    The formal table and the epistemic model intentionally do not import one another: sharing an
    implementation would make agreement tautological. This narrow observation function lets the
    test suite compare all 32 worlds while preserving that independence.
    """

    alice, bob, carol = _statements(payer, coins)
    return _truth_value(alice), _truth_value(bob), _truth_value(carol)


def _parity(statements: tuple[BitExpr, BitExpr, BitExpr]) -> BitExpr:
    alice, bob, carol = statements
    return _xor(_xor(alice, bob), carol)


def _negate(expression_text: str) -> str:
    return f"¬ ( {expression_text} )"


def _prove_not_equivalent(
    proof: ProofBuilder,
    left_text: str,
    right_text: str,
    left_proof: Wff,
    right_proof: Wff,
    *,
    left_value: bool,
    label: str,
) -> Wff:
    """Prove ``not (left <-> right)`` when exactly one child is true."""

    if left_value:
        # right is false. nbn2 applied in the order (right, left) says that under ¬right,
        # ¬left is equivalent to (right ↔ left). Since left is true, ¬left is false too.
        reduction = proof.ref(
            f"{label}_reduce",
            (
                f"( {_negate(right_text)} → "
                f"( {_negate(left_text)} ↔ ( {right_text} ↔ {left_text} ) ) )"
            ),
            ref="nbn2",
            note="reduce a biconditional under a false left operand",
        )
        swapped_equivalence = proof.mp(
            f"{label}_reduced",
            right_proof,
            reduction,
            note="instantiate the false right operand",
        )
        double_left = proof.ref(
            f"{label}_double",
            _negate(_negate(left_text)),
            left_proof,
            ref="notnoti",
            note="a true left operand refutes its negation",
        )
        not_swapped = proof.ref(
            f"{label}_not_swapped",
            _negate(f"( {right_text} ↔ {left_text} )"),
            double_left,
            swapped_equivalence,
            ref="mtbi",
            note="the swapped biconditional is false",
        )
        commutation = proof.ref(
            f"{label}_commute",
            f"( ( {left_text} ↔ {right_text} ) ↔ ( {right_text} ↔ {left_text} ) )",
            ref="bicom",
            note="commute biconditional back to transcript order",
        )
        return proof.ref(
            f"{label}_not_equivalent",
            _negate(f"( {left_text} ↔ {right_text} )"),
            not_swapped,
            commutation,
            ref="mtbir",
            note="unequal truth values cannot be biconditional",
        )

    # left is false and right is true; nbn2 already has the desired order.
    reduction = proof.ref(
        f"{label}_reduce",
        (
            f"( {_negate(left_text)} → "
            f"( {_negate(right_text)} ↔ ( {left_text} ↔ {right_text} ) ) )"
        ),
        ref="nbn2",
        note="reduce a biconditional under a false left operand",
    )
    equivalence = proof.mp(
        f"{label}_reduced",
        left_proof,
        reduction,
        note="instantiate the false left operand",
    )
    double_right = proof.ref(
        f"{label}_double",
        _negate(_negate(right_text)),
        right_proof,
        ref="notnoti",
        note="a true right operand refutes its negation",
    )
    return proof.ref(
        f"{label}_not_equivalent",
        _negate(f"( {left_text} ↔ {right_text} )"),
        double_right,
        equivalence,
        ref="mtbi",
        note="unequal truth values cannot be biconditional",
    )


def _evaluate(
    proof: ProofBuilder,
    expression: BitExpr,
    *,
    label: str,
) -> tuple[Wff, bool]:
    """Prove ``expression`` when true, or its negation when false."""

    if isinstance(expression, bool):
        truth = _bit(True)
        truth_proof = proof.ref(
            f"{label}_truth",
            truth,
            ref="id",
            note="the implication identity represents a true bit",
        )
        if expression:
            return truth_proof, True
        false_text = _bit(False)
        false_refutation = proof.ref(
            f"{label}_false",
            _negate(false_text),
            truth_proof,
            ref="notnoti",
            note="the negation of an implication identity represents a false bit",
        )
        return false_refutation, False

    left_proof, left_value = _evaluate(
        proof,
        expression.left,
        label=f"{label}l",
    )
    right_proof, right_value = _evaluate(
        proof,
        expression.right,
        label=f"{label}r",
    )
    expression_text = _render(expression)
    value = left_value ^ right_value
    left_text = _render(expression.left)
    right_text = _render(expression.right)
    if not value:
        equivalence_ref = "2th" if left_value else "2false"
        equivalence = proof.ref(
            f"{label}_equivalent",
            f"( {left_text} ↔ {right_text} )",
            left_proof,
            right_proof,
            ref=equivalence_ref,
            note="equal child truth values are biconditional",
        )
        xnor = proof.ref(
            f"{label}_xnor",
            f"( ( {left_text} ↔ {right_text} ) ↔ {_negate(expression_text)} )",
            ref="xnor",
            note="a true biconditional is the negation of XOR",
        )
        result = proof.ref(
            f"{label}_false_xor",
            _negate(expression_text),
            equivalence,
            xnor,
            ref="mpbi",
            note="equal operands make XOR false",
        )
        return result, False

    not_equivalent = _prove_not_equivalent(
        proof,
        left_text,
        right_text,
        left_proof,
        right_proof,
        left_value=left_value,
        label=f"{label}_different",
    )
    xor_definition = proof.ref(
        f"{label}_definition",
        f"( {expression_text} ↔ {_negate(f'( {left_text} ↔ {right_text} )')} )",
        ref="df-xor",
        note="definition of exclusive disjunction",
    )
    result = proof.ref(
        f"{label}_true_xor",
        expression_text,
        not_equivalent,
        xor_definition,
        ref="mpbir",
        note="unequal operands make XOR true",
    )
    return result, True


def _join(proof: ProofBuilder, rows: tuple[Wff, ...], *, label: str) -> Wff:
    """Conjoin theorem rows using only conjunction introduction."""

    if not rows:
        raise ValueError("a finite proof table must contain at least one row")
    result = rows[0]
    for index, row in enumerate(rows[1:], start=1):
        result_text = render_wff(
            result.tokens,
            symtab=proof.sys.interner.symbol_table(),
        )
        row_text = render_wff(
            row.tokens,
            symtab=proof.sys.interner.symbol_table(),
        )
        result = proof.ref(
            f"{label}_{index:02d}",
            f"( {result_text} ∧ {row_text} )",
            result,
            row,
            ref="pm3.2i",
            note="join two independently proved finite rows",
        )
    return result


def prove_dc_parity_table(system: System) -> Proof:
    """Prove protocol parity correctness in every one of the 32 declared worlds."""

    proof = ProofBuilder(system, "dc_parity_table")
    rows: list[Wff] = []
    row_index = 0
    for payer in PAYERS:
        for raw_coins in product((False, True), repeat=3):
            coins: CoinTriple = (raw_coins[0], raw_coins[1], raw_coins[2])
            parity = _parity(_statements(payer, coins))
            row, value = _evaluate(proof, parity, label=f"r{row_index:02d}")
            expected = payer != NSA
            if value is not expected:
                raise RuntimeError(
                    f"formal parity row disagrees with its declared payer: {payer}, {coins}"
                )
            rows.append(row)
            row_index += 1

    if len(rows) != 32:
        raise RuntimeError("Dining Cryptographers parity table must contain exactly 32 rows")
    conclusion = _join(proof, tuple(rows), label="parity_join")
    return proof.build(conclusion)


def _toggle(coins: CoinTriple, edge_index: int) -> CoinTriple:
    values = list(coins)
    values[edge_index] = not values[edge_index]
    return values[0], values[1], values[2]


def _prove_equal_expressions(
    proof: ProofBuilder,
    left: BitExpr,
    right: BitExpr,
    *,
    label: str,
) -> Wff:
    left_proof, left_value = _evaluate(proof, left, label=f"{label}a")
    right_proof, right_value = _evaluate(proof, right, label=f"{label}b")
    if left_value is not right_value:
        raise RuntimeError("declared transcript bijection does not preserve a statement")
    equivalence_ref = "2th" if left_value else "2false"
    return proof.ref(
        f"{label}_same",
        f"( {_render(left)} ↔ {_render(right)} )",
        left_proof,
        right_proof,
        ref=equivalence_ref,
        note="both public statements have the same proved truth value",
    )


def prove_dc_payer_bijection_table(system: System) -> Proof:
    """Prove all transcript rows preserved by the three shared-edge payer toggles."""

    proof = ProofBuilder(system, "dc_payer_bijection_table")
    # Moving the payer across AB, BC, or CA and toggling that same secret coin is an involution.
    # Consequently each eight-element coin space is paired bijectively with the next payer's coin
    # space. The theorem below checks that every paired execution has the same public transcript.
    payer_edges: tuple[tuple[Payer, Payer, int], ...] = (
        (ALICE, BOB, 0),
        (BOB, CAROL, 1),
        (CAROL, ALICE, 2),
    )
    rows: list[Wff] = []
    row_index = 0
    for source_payer, target_payer, edge_index in payer_edges:
        for raw_coins in product((False, True), repeat=3):
            source_coins: CoinTriple = (raw_coins[0], raw_coins[1], raw_coins[2])
            target_coins = _toggle(source_coins, edge_index)
            if _toggle(target_coins, edge_index) != source_coins:
                raise RuntimeError("shared-edge toggle must be an involution")

            source_statements = _statements(source_payer, source_coins)
            target_statements = _statements(target_payer, target_coins)
            statement_equalities = tuple(
                _prove_equal_expressions(
                    proof,
                    source_statement,
                    target_statement,
                    label=f"b{row_index:02d}s{speaker_index}",
                )
                for speaker_index, (source_statement, target_statement) in enumerate(
                    zip(source_statements, target_statements, strict=True)
                )
            )
            rows.append(
                _join(
                    proof,
                    statement_equalities,
                    label=f"b{row_index:02d}_statements",
                )
            )
            row_index += 1

    if len(rows) != 24:
        raise RuntimeError("payer-bijection table must contain exactly 24 rows")
    conclusion = _join(proof, tuple(rows), label="bijection_join")
    return proof.build(conclusion)


__all__ = [
    "formal_transcript_bits",
    "prove_dc_parity_table",
    "prove_dc_payer_bijection_table",
]
