# Note template

Sections in this order. How to write each one is in `writing.md`. If a section has nothing, write "None" rather than deleting it (except Section 10, which appears only when Lean was requested).

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
How existing methods work (each mechanism defined), what specifically fails, and what evidence the authors give that it fails (experiment / complexity argument / assertion only). End with the goal the authors set.

## 3. Method
A short overview of the whole pipeline (input to output), then one paragraph per component:
problem it solves → what it does (equation) → borrowed (from where) or new (what exactly) → why designed this way.

## 4. Why it works
Start from a question the reader would ask, reason through it, then state the support for each step ([paper] / [evidence] / [inference]). End with the assumptions the mechanism rests on and an honest answer to "what really made it better".

## 5. Data, training, and evaluation setup
The answers to setup-checklist.md Sections 1 to 3 (table per section). Introduce each dataset in prose first.

## 6. Baselines
| Baseline | Source | How it works (one sentence) | Numbers rerun or copied | Same setting? |
|---|---|---|---|---|

## 7. Claims vs evidence
Table from experiment-check.md.

## 8. Paper vs code
Mismatch table from code-check.md (architecture and stated values only), then optional reproduction notes.

## 9. Limitations and failure conditions
- Stated by the authors: ...
- Not stated, but follow from the assumptions in Section 4: ...

## 10. Lean verification
(Only when requested; filled by the theory-auditor skill.)

## Sources
- Paper: <link>
- Code: <repo>@<commit>
```
