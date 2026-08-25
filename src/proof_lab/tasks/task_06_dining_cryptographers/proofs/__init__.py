"""Kernel-bound finite proofs for Task 6."""

from .finite_tables import (
    formal_transcript_bits,
    prove_dc_parity_table,
    prove_dc_payer_bijection_table,
)

__all__ = [
    "formal_transcript_bits",
    "prove_dc_parity_table",
    "prove_dc_payer_bijection_table",
]
