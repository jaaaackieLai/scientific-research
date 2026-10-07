# PhysLib

PhysLib (`github.com/leanprover-community/physlib`, called PhysLean before March 2026) is a Lean 4 library of physics definitions and theorems built on Mathlib: spacetime and special relativity, electromagnetism, classical and quantum mechanics, statistical mechanics, quantum field theory, quantum information. It is still changing fast, so this file gives rules, not a list of its contents.

Not to be confused with the smaller PhysLib from the Lean4PHYS paper (ICLR 2026), a separate project.

## When to use it
- Use it when a step needs a physical structure (Minkowski space, a field, a Hilbert space of states, a unit system) and PhysLib already defines it the way the derivation means it.
- Do not use it for pure algebra or calculus; plain Mathlib is enough and avoids the extra download.
- If PhysLib's definition differs from the derivation's (other sign convention, metric signature, normalization, units), define the object locally in the audit file with explicit hypotheses instead. A theorem about a different definition does not verify the derivation. Tell the user which one you chose and why.

## Workspace
- PhysLib pins its own Lean and Mathlib versions, so it gets its own workspace, `~/.theory-auditor/physlib_ws`, separate from `mathlib_ws`. Create it only when an audit needs PhysLib.
- Read PhysLib's README and `lean-toolchain` on its default branch for the current `require` line and Lean version; do not reuse a version from memory. Setup steps are in `setup.md`.
- The Mathlib cache (`lake exe cache get`) covers only Mathlib. PhysLib itself compiles locally on first build; tell the user this may take tens of minutes.

## Finding definitions
Search the source in the workspace rather than guessing names:
- `grep -rni "minkowski" .lake/packages/[Pp]hys*/ --include=*.lean` (replace the word with the concept)
- Read the docstring and the definition itself before using it; check conventions (signature, units, factors of 2π and ħ).
- Record in the report which PhysLib definitions and theorems the proof used, with the PhysLib commit.

## Physics in theorem statements
- Every approximation is a hypothesis with a name and a precise form, e.g. `(h_small : |v| / c < ε)`, not a comment. If the source only says "small", ask the user what bound to use, or state the theorem for an arbitrary bound.
- A truncated expansion is stated with its remainder: prove that the error is bounded (e.g. `|f x - (a + b*x)| ≤ C * x^2` for `|x| ≤ δ`), not that `f x = a + b*x`.
- Plain `ℝ` carries no units. Either use PhysLib's unit system, or keep all quantities in `ℝ` and do the dimension check of step 5 separately; say which in the report.
