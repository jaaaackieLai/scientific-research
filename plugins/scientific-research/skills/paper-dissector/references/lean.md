# Lean verification

Only when the user asks. Goal: check that a derivation in the paper actually holds.

## 1. Before starting
- Run `lake --version`. If Lean is not installed, tell the user and stop; do not install it yourself.
- Pick with the user which derivation to verify (a theorem, a gradient, a complexity bound). Do not try to verify the whole paper.
- If the statement cannot be formalized faithfully (e.g. it is about "learned representations" with no precise definition), say so and stop.

## 2. Formalize
- Work in a scratch Lean project with Mathlib.
- Write the statement first and show it to the user next to the paper's version, with every added assumption listed (e.g. a nonzero denominator, finite dimension, a norm the paper did not specify). Proceed after the user confirms the statement is faithful.
- No `sorry`, no `axiom`, no `admit` in the final proof.

## 3. Result
Write into Section 9 of the note:

| Item | Content |
|---|---|
| Statement | Paper version (Eq. / Thm number) and Lean version |
| Added assumptions | Ones the paper left implicit |
| Result | proved / false (with counterexample) / not finished (where it got stuck) |
| Proof file | Path, and the Lean and Mathlib versions |

A failed proof does not mean the paper is wrong. Say which: a counterexample was found, or the proof simply was not completed.
