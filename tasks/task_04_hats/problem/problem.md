# Five-Hat Knowledge Puzzle

There are three white hats and two black hats. Alice, Bob, and Carol each receive one hat. Every
hat used is one of those five, each person wears exactly one hat, and everyone knows these facts.

They stand in a line:

- Alice can see Bob's and Carol's hats.
- Bob can see Carol's hat but not Alice's.
- Carol cannot see either of the other hats.

Alice is asked whether she knows the color of her own hat. She answers, "I do not know." Bob hears
Alice's answer and is asked the same question. He also answers, "I do not know."

What color is Carol's hat?

## Intended reasoning

If Bob and Carol both wore black, Alice would see the two available black hats and know that her
own hat must be white. Alice's ignorance therefore rules out the case in which Bob and Carol are
both black.

Bob hears this. If Carol wore black, Bob could infer from Alice's ignorance that Bob himself must
wear white. Bob nevertheless says that he does not know. Carol therefore does not wear black and,
because every hat is either black or white, Carol wears white.

## Scope

This task verifies the final inference after the finite epistemic reasoning has been compiled into
an explicit bridge proposition. It does not claim that Proof Lab 0.0.1 has a native modal or
epistemic logic. The bridge is audited in the claim ledger and interpretation report rather than
silently treated as a theorem of propositional logic.
