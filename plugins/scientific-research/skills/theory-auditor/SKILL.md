---
name: theory-auditor
description: Audit a formula derivation step by step and verify it with Lean 4 + Mathlib (PhysLib when the derivation needs physics definitions). Splits the derivation into numbered steps, lists every physical and mathematical assumption, formalizes the steps in Lean with approximations as explicit hypotheses, and reports which steps are Lean-proved, which were only checked by the agent, and which rest on unverified physical assumptions. First checks whether this machine can install and run Lean; if it cannot, every result is labeled "agent 檢查，未經過 Lean 驗證". Use when the user says "check this derivation", "is this formula right", "verify with Lean", "prove this step", "幫我驗證這個推導", "這個公式推得對嗎", "用 Lean 證明", or when another skill (e.g. paper-dissector) asks for Lean verification of a derivation.
---

# theory-auditor

Purpose: tell the user exactly which parts of a derivation are proved, which are only checked, and which are assumed. Lean proves that a conclusion follows from the stated definitions and hypotheses; it does not prove that a physical model or an approximation matches reality. The audit makes that boundary visible.

## Related files
- `scripts/check_env.py`: decides whether Lean can run here (always run it in step 3)
- `references/setup.md`: installing elan, creating the shared workspaces, platform notes
- `references/physics.md`: when and how to use PhysLib (read it only when step 2 says so)

## Workflow

### 1. Split the derivation
- Get the derivation from the user, a paper (cite the equation numbers), or the calling skill. Pick one derivation with the user; do not audit a whole paper at once.
- Number the steps so that each step is one transformation, from the first premise to the final result.
- List every assumption, in three groups:
  - **Physical model**: what the derivation takes as true about the world (ideal gas, spherical symmetry, point masses).
  - **Approximations**: every ≈, "neglect higher-order terms", "v ≪ c", "for large N".
  - **Mathematical conditions** the source left implicit: nonzero denominators, positivity, differentiability, integrability, convergence, exchange of limits.

### 2. Classify each step
| Class | What it is | How it is checked |
|---|---|---|
| A. Algebra | identities, rearrangement, substitution | Lean (`ring`, `field_simp`, `nlinarith`) |
| B. Analysis | derivatives, integrals, limits, inequalities | Lean with Mathlib, with the conditions made explicit |
| C. Physical assumption | model choices and approximations | written as a hypothesis of the theorem; never proved |
| D. Not formalizable | delta functions used as functions, path integrals, divergent series, renormalization | say so; agent checks only |

If a step uses physical structures (spacetime, fields, quantum states, units) and you want an existing definition for them, read `references/physics.md` and plan to use PhysLib. Pure algebra and calculus need only Mathlib.

### 3. Check the environment
Run `python3 <skill-dir>/scripts/check_env.py`, adding `--physlib` if step 2 decided on PhysLib. It prints JSON with a `verdict`:
- **`ready`**: Lean and the workspace exist. Go to step 4.
- **`installable`**: something is missing but disk and RAM suffice. Tell the user what is missing, the download size (about 7 GB for Mathlib, more with PhysLib), and the first-run time, and show the commands from `references/setup.md`. Install only after the user agrees. If they decline, continue as `insufficient`.
- **`insufficient`**: tell the user the `reasons` from the output. Skip step 4, do step 5, and label every result `agent 檢查，未經過 Lean 驗證`.

Also tell the user any `notes` (e.g. RAM could not be detected).

### 4. Formalize in Lean
- Work in the shared workspace from the script output (`facts.workspace`), one file per audit: `TheoryAuditor/<topic>.lean`. Never create a new Lake project per audit; each one copies Mathlib (about 7 GB).
- Write the theorem statements first. Physical assumptions (class C) and mathematical conditions become hypotheses. Show the user each statement next to the source's version, with every added hypothesis listed, and continue after they confirm the statements are faithful.
- If a proof needs a stronger hypothesis or a weaker conclusion than the confirmed statement, stop and show the user the change. Never quietly weaken a statement to make a proof go through.
- Check with `lake env lean TheoryAuditor/<topic>.lean` from the workspace root and iterate on the errors.
- The final file has no `sorry`, `admit`, or `axiom`. Add `#print axioms <theorem>` for each theorem; the output may list only `propext`, `Classical.choice`, and `Quot.sound`.
- When Lean finds the statement false, find a concrete counterexample (`norm_num` on specific values) and report it.

### 5. Agent checks (every audit)
Run these on every step, whether or not Lean ran. They catch errors that a faithful-looking Lean statement can hide, and they are all the user gets when Lean cannot run.
- **Dimensions**: both sides of every equation have the same units.
- **Limiting cases**: the result reduces to known results (c → ∞, ħ → 0, small angle, a single particle).
- **Symbolic check** of class A steps with SymPy.
- **Numerical spot check**: plug random values that satisfy the assumptions into both sides.

### 6. Report
Reply in the user's language with this table, one row per step:

| Step | Class | Result | Method |
|---|---|---|---|
| (1) → (2) | A | Lean 證明 | `ring` |
| (2) → (3) | C | 物理假設，未驗證 | hypothesis `h_small : v / c < 0.1` |
| (3) → (4) | B | agent 檢查，未經過 Lean 驗證 | SymPy and dimensions |

Result values: `Lean 證明` / `反例` (give the counterexample) / `未完成` (say where it got stuck) / `agent 檢查，未經過 Lean 驗證` / `物理假設，未驗證` / `無法形式化` (class D).

Below the table:
- The full list of assumptions from step 1 and the added hypotheses from step 4.
- The Lean file path, the Lean version (`lake env lean --version`), and the Mathlib (and PhysLib) commits from `lake-manifest.json`.
- If Lean did not run: one line saying why (from the step 3 `reasons`, or the user declined installing).

A failed proof does not mean the derivation is wrong. Say which: a counterexample was found, or the proof was not completed.

When called from paper-dissector, also put the table and the assumption list into Section 10 of its note.

## Do not
- Do not install elan, Lean, Mathlib, or PhysLib without the user's agreement.
- Do not write `Lean 證明` for a step whose Lean proof did not compile with the axiom check passing.
- Do not present a physical assumption or an approximation as proved.
- Do not hard-code what PhysLib contains; search its source (see `references/physics.md`).
