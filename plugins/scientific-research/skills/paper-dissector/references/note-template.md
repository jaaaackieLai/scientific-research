# Note template

Sections in this order. How to write each one is in `writing.md`. If a section has nothing, write "None" rather than deleting it (except Lean verification, which appears only when Lean was requested). The numbers give reading order only; other files refer to a section by its heading name.

Translate the headings into the user's language, use the same translation in every note, and keep the order. If the notes folder already has a note, copy its headings.

```markdown
# <Paper title>

> <Venue Year> | arXiv: <id> | Code: <repo URL>@<commit hash> (<date>), or "no official code"
> Read: YYYY-MM-DD | Code check: done / not possible (<reason>) | Lean: not requested / <result>

## Notation
| Symbol | Meaning | Shape / domain |
|---|---|---|
Note every place where this note renames a symbol the paper uses for two things.

## 1. Insight
Three to five sentences a colleague would find interesting: what everyone assumed, what this paper did instead, why it matters, and the lesson that transfers.

## 2. Background and the problem
Why the problem matters (the authors' reason, with its support), why it is hard (why the naive approach fails), then how existing methods work (each mechanism defined), what specifically fails, and what evidence the authors give for each failure (experiment / complexity argument / assertion only). Keep "hard" and "not solved before" apart. End with the problem stated in one sentence: the goal the authors set.

## 3. Method
A short overview of the whole pipeline (input to output), then one paragraph per component:
problem it solves → what it does (equation) → borrowed (from where) or new (what exactly) → why designed this way.

## 4. Why it works
Start from a question the reader would ask, reason through it, then state the support for each step ([paper] / [evidence] / [inference]). End with the assumptions the mechanism rests on and an honest answer to "what really made it better".

## 5. Data, training, and evaluation setup
The answers to the data, training, and evaluation questions of setup-checklist.md (one table each). Introduce each dataset in prose first.

## 6. Baselines
| Baseline | Source | How it works (one sentence) | Numbers rerun or copied | Same setting? |
|---|---|---|---|---|

## 7. Claims vs evidence
Table from experiment-check.md.

## 8. Paper vs code
Mismatch table from code-check.md (architecture and stated values only), then optional reproduction notes.

## 9. Limitations and failure conditions
- Stated by the authors: ...
- Not stated, but follow from the assumptions in Why it works: ...

## 10. Derivation check (not verified by Lean)
The main derivation in numbered steps, after the list of its assumptions.
| Step | Verdict | Reason or counterexample | Support |
|---|---|---|---|
| (1) → (2) | holds / holds only if <condition> / fails | ... | [paper] / [evidence] / [inference] |
End with the conditions the result needs and which of them the paper states.

## 11. Lean verification
(Only when requested; filled by the theory-auditor skill.)

## Sources
- Paper: <link>
- Code: <repo>@<commit>
```
