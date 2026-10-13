# Run directory and artifact formats

Every idea-forge run lives in `docs/ideas/<slug>/` under the project root. Each file has one owner; only the owner writes it. `scripts/check_run.py` parses exactly the formats below, so keep the headings and field labels verbatim (they stay in English even when the content is in another language).

```
docs/ideas/<slug>/
  problem.md        orchestrator  the input: challenge + problem definition (+ optional cutoff)
  plan.md           orchestrator  direction, state, one-line history
  gaps.md           gap-finder    one section per axis
  derivations.md    deriver       obvious mechanisms per gap, written BEFORE any candidate on that gap
  candidates.md     innovator     one block per candidate
  scores.md         reviewer      one verdict block per reviewed candidate
  proposal.md       writer        the final proposal
  papers/<id>.md    paper-reader  one cumulative digest per paper
```

## Cutoff

When `problem.md` gives a cutoff date, a paper whose first public date is **on or after** that date must not be read or cited. For a new-style arXiv id, the paper also counts as after the cutoff when the first day of its id month is on or after the cutoff: arXiv makes a paper public in its id month, even when v1 was sent earlier (`2601.00002` with v1 `2025-12-28` is after a `2026-01-01` cutoff).

## Paper ids and citations

- A paper id is its arXiv id without the version: `2403.19647`. Old-style ids replace `/` with `_`: `hep-th/9901001` → `hep-th_9901001`.
- A paper with no arXiv version gets `ref-<first-author-surname>-<year>-<keyword>` in lowercase, for example `ref-vaswani-2017-attention`.
- Cite inline in square brackets, one id per bracket: `[2403.19647]`, several as `[2403.19647][2309.08600]`.
- **Every cited id must have a digest at `papers/<id>.md`.** A paper seen only as a search hit or an abstract is not read and must not be cited.

## `papers/<id>.md` (paper-reader)

```markdown
# <paper title>

- ID: 2403.19647
- First public: 2024-03-28
- Source: https://arxiv.org/abs/2403.19647

## What this paper does
<one paragraph, at most 120 words>

## Goal-by-goal answers

### Goal: <verbatim question>
<answer, at most 300 words, with locations such as [Sec 3.2] or [Eq 4]; "not stated in the paper" when it is not>
```

`First public` is the date of arXiv v1 (or the publication date for a `ref-` paper), as `YYYY-MM-DD`. It can fall before the id month (a month-end submission or a moderation hold) but never after it. Later calls append new `### Goal:` blocks; they never rewrite earlier ones.

## `problem.md` (orchestrator)

```markdown
# <short problem title>

## Challenge
<what current solutions fail to meet, why it matters, a concrete failing case>

## Problem definition
<setting, inputs, outputs>

## Cutoff
<YYYY-MM-DD, or "none">
```

## `gaps.md` (gap-finder)

```markdown
## Axis: <axis phrase, verbatim from the brief>

### What has been done
<mechanism-level summary grouped by approach, with citations>

### Open gaps on this axis

#### G<n> — <short title>
- **Gap:** prior methods do X through Y, but Y leaves method-level issue Z unresolved in <setting>.
- **Near-miss methods:** [id] — how it comes close; [id] — how it comes close. Plus the search trail.
- **Methodological deficiency:** <kind> — <the one reason the near misses fall short, grounded in a digest>.
- **Why it matters:** <who is blocked and what closing it unlocks>.
- **Evidence route:** <what observation would show a future method closes it; no solution here>.
```

- At most two `#### G<n>` blocks per axis; zero is allowed. `n` is numbered across the whole file (G1, G2, G3 ...), never reused.
- `<kind>` is one of: `missing mechanism`, `algorithmic limitation`, `wrong inductive bias`, `credit-assignment flaw`, `training-objective mismatch`, `representation limitation`, `scalability limit`, or `other: <name>`.

## `derivations.md` (deriver)

```markdown
## Gap: G<n>

### D<n>.<k> — <one-line central mechanism>
- **Central mechanism:** <one sentence>
- **Derivation steps:** 1) <step> 2) <step> 3) <step> — inline on this one line, from the supplied papers and standard techniques
- **References used:** [id] — the piece it supplies; ...
- **Key assumption:** <one sentence>
```

- One `## Gap:` section per gap, written before any candidate on that gap exists. At most three `### D` blocks per gap; zero is allowed and means no concrete mechanism follows from the supplied material.
- With zero derivations, the section holds one plain line instead: `No concrete derivation: <reason>.`
- A written `## Gap:` section is frozen: never edit or extend it.

## `candidates.md` (innovator)

```markdown
### C<n> — <short title>
- **Intuition:** <one or two plain sentences>
- **Gap it attacks:** G<n> — <the concrete failure it addresses and why closing it matters>
- **If improving prior candidate:** <optional: C<x>, the weakness addressed, what changed>
- **Source inspiration:** [id] — <mechanism, why it works there, under which condition>. Novelty type: <new topic | recombination of distant concepts | reinforcing a weak connection>.
- **How it maps to this problem:** <what plays the role of what; no equations or pseudocode>
- **Why it could work:** <why the condition the mechanism needs holds here; the key assumption>
- **Novelty vs. closest in-domain work:** [id] — <what it already does and the specific difference>
- **Main risk:** <the single most likely reason it fails>
```

## `scores.md` (reviewer)

```markdown
### C<n> verdict
- **Verdict:** survive | revise(focus=<dimension>) | reject(reason=<short reason>)
- **Closest derivation:** D<n>.<k> | NONE
- **Obviousness:** trivial_combination | routine_extension | non_obvious_step | surprising | unscored
- **Source credibility:** [id] venue=<G1 result>, institutions=<G4 result>, code=<official repo or none> — one entry per source paper and per closest in-domain paper, labels only
- **Evidence:** <bullets, each citing a paper id or quoting the mechanism it challenges>
- **Strongest objection:** <one sentence>
```

- `<dimension>` is one of `novelty`, `grounding`, `mapping`, `feasibility`, `clarity`, `coherence`.
- `unscored` is used exactly when the candidate's gap has zero derivations in `derivations.md`; it is not evidence of non-obviousness. `unscored` goes with **Closest derivation:** `NONE`; otherwise **Closest derivation:** is one of that gap's `D` ids.

## `proposal.md` (writer)

The first line is the notice, verbatim:

```markdown
以下研究構想為 AI 生成，新穎性與可行性未經實驗驗證；引用、主張與是否已有人做過，請自行查證後再使用。

# <proposal title>

## One-sentence thesis
## Core problem
## Key novelty
## Problem definition
## Key terms
## Related work
## Method
## Model and training
## Comparison to prior work
## Proposed evaluation
## Falsifiable predictions
## Limitations
## Provenance
```

- Every `##` section above is required and non-empty. If a section genuinely does not apply (for example no model is trained), say so and why.
- `## Falsifiable predictions`: each prediction paired with the observation that would falsify it.
- `## Provenance`: the candidate id, its gap id, and its reviewer verdict.
- No measured results, no invented numbers, no `TODO` placeholders.
