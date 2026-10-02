# Paper vs code check

Always done. Goal: confirm the code runs the architecture the paper describes, with the values the paper states. Only two kinds of mismatch are reported.

## 1. Find the official code
- Look in this order: the paper (abstract, footnotes, end of intro), the arXiv Comments field, the project page.
- Official means the repo belongs to an author or the authors' lab or organization. A third-party reimplementation does not count; if only that exists, record "no official code" and name the third-party repo separately.
- Clone into a scratch directory with full history (`git clone --filter=blob:none <repo>`); the code may have changed a lot since the paper.
- Pick the commit closest to the paper: a tag or branch named for the paper first, otherwise the earliest tag or commit after the paper's first arXiv version. Record its hash and date.
- When an item does not match, check whether a later version near the camera-ready date fixes it; record which versions were checked.

## 2. What to compare
1. **Architecture**: the model structure the paper describes (components and their order, normalization position, attention or layer computation, key equations, loss). Compare against the model definition.
2. **Stated values**: every number or setting the paper explicitly states (dimensions, layer counts, dropout, learning rate schedule, optimizer...). Compare against the configs that produce the paper's results (the ones the README names for reproduction), not only code defaults.

Do not report:
- Settings the code has but the paper never states (initialization, length filters, batching details, default step counts). Hyperparameters are tunable; they are not mismatches.
- Items that match. List only the mismatches.
- Changes made in versions after the paper. If a later version changes the architecture or defaults in a way that breaks reproduction, add one line under "Reproduction notes", not in the mismatch table.

Evaluation details the paper omits (e.g. how the metric is computed) belong to setup-checklist 3.3, not here; cite the code there if it answers the question.

Before marking a value as a mismatch, trace it to where it is finally used. Constants are often split across files (e.g. a learning rate multiplied in one place and divided inside the optimizer); compute the effective value.

## 3. Report

| Item | Type | Paper (location) | Code (file:line) | Impact |
|---|---|---|---|---|
| ... | architecture / stated value | ... | ... | which result it could change, or "equivalent, no effect" with the reason |

- If nothing mismatches, write "No mismatches in architecture or stated values" and the commit checked.
- Reproduction notes (optional): at most a few lines, e.g. "later versions changed X; use config Y".
- If the code cannot be found or will not open, record why. Do not claim a match without having seen the code.
