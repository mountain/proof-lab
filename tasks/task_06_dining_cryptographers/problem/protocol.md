# Protocol Statement and Modeling Convention

Three cryptographers—Alice, Bob, and Carol—learn that dinner was paid for either by the NSA or by
exactly one of them. They want to discover which of those two cases holds while hiding the identity
of a cryptographer payer.

Each neighbouring pair privately obtains one independent fair bit:

```text
Alice ----- c_AB ----- Bob
   \                     /
    c_CA               c_BC
      \                 /
              Carol
```

Every participant compares the two bits they can see. A non-payer truthfully reports whether the
bits differ; a payer says the opposite. We encode “different” as `1` and “same” as `0`, so the
public statement of participant `i` is

```text
s_i = XOR(bits on edges incident to i) XOR [i paid].
```

The three reports are simultaneous. Their XOR is

```text
s_A XOR s_B XOR s_C
  = c_AB XOR c_AB XOR c_BC XOR c_BC XOR c_CA XOR c_CA
      XOR [Alice paid] XOR [Bob paid] XOR [Carol paid]
  = [a cryptographer paid].
```

Every shared bit cancels because it appears at both endpoints. Thus even parity means the NSA paid
and odd parity means one cryptographer paid.

## Possible worlds and private information

A standard world is `(payer, c_AB, c_BC, c_CA)`, giving 32 worlds. A participant's private
observation contains only the two incident bits and the boolean fact that they personally paid.
Two worlds are indistinguishable to that participant precisely when these observations agree.
Eve's initial observation is constant, so her initial information cell contains every world.

The exact three-bit transcript is represented as one truthful public announcement. This matches
the protocol's simultaneous broadcast: all worlds producing a different transcript are removed at
once, and every agent's information cell is intersected with the survivors.

## Security statements used locally

The local correctness and anonymity claims are deliberately concrete:

1. **Correctness:** transcript parity identifies whether the NSA or a cryptographer paid.
2. **Outsider anonymity:** conditional on a cryptographer having paid, Eve's payer candidates are
   exactly `{Alice, Bob, Carol}`.
3. **Non-payer anonymity:** each non-paying participant's candidates are exactly the other two
   participants.
4. **Distribution equality:** over uniform secret bits, Alice-, Bob-, and Carol-paid executions
   induce identical transcript distributions.

These are stronger than testing one example execution but narrower than a universal claim about
all anonymous-broadcast implementations or all adversary models.

## Deliberately broken topology

For a red-team comparison, retain only the Alice--Bob edge and isolate Carol. The statement rule
does not change. Carol has no incident secret bit, so

```text
s_C = [Carol paid].
```

Correctness still holds—the remaining Alice--Bob bit still cancels twice—but anonymity fails.
This distinction is useful: functional correctness alone is not a security proof.
