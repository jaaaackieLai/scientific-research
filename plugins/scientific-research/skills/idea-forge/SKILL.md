---
name: idea-forge
description: Turn a research problem (what current methods fail at, plus the setting) into one grounded research proposal through isolated sub-agents that hand off only through files - a gap finder maps method-level gaps in the problem's own field, a deriver freezes the obvious solutions, an innovator transfers a mechanism from another field, an adversarial reviewer checks it against the obvious solutions, and a writer develops the survivor. Every cited paper must have been read. Use when the user says "help me find a research idea", "brainstorm a method for this problem", "what could I propose for X", "find a research gap", "幫我想研究 idea", "找研究缺口", "這個問題可以怎麼解", "幫我發想方法". Not for reading one paper (paper-dissector) or filtering papers (paper-search).
---

# idea-forge

Purpose: one methodological idea that addresses a real gap, borrows a mechanism that solved a structurally similar difficulty elsewhere, says why it transfers, and survives an adversarial check against the solutions anyone would try first. The output is a proposal file and its trail of evidence, not a chat answer.

The method adapts IdeaScientist (Liu et al., 2026, arXiv:2610.04074), rewritten from scratch. Unlike the paper, the blind derivation of obvious mechanisms runs inside the loop (deriver, then reviewer), because cross-domain framing alone inflates judged novelty.

## Related files
- `references/artifacts.md`: the run directory and the exact format of every file (always follow it)
- `references/roles-common.md`: rules every sub-agent shares (reading papers, metadata, citations, cutoff)
- `roles/*.md`: the instructions each sub-agent follows (gap-finder, deriver, innovator, reviewer, writer, paper-reader)
- `scripts/check_run.py`: the deterministic gate for a run directory (always run it in step 7)

## You are the orchestrator
- You do not search and you do not read papers. Everything you know about the literature comes from the files the sub-agents write. If you want to look something up, spawn the role that owns that question.
- You write only `problem.md` (once, in step 1) and `plan.md`. Every other file belongs to the role that writes it; to change it, spawn that role again with feedback.
- One active direction at a time: drive a gap through derive, ideate, and review before trying another. Do not spawn several innovators hoping one wins.
- Each brief is narrow and self-contained: the sub-agent sees only its brief and the files, never this conversation.

## Spawning a role
Each role has a plugin agent `scientific-research:idea-<role>`. Brief it with the named fields its role file lists under `## Input`, always including `RUN_DIR` and `SKILL_DIR` (the absolute path of this skill's directory).

If those agent types are not available (the skill was copied without the plugin, or the host has no such agents), spawn a general-purpose sub-agent whose brief starts with `Follow <SKILL_DIR>/roles/<role>.md.` and then the fields. If the host cannot spawn sub-agents at all (for example Codex unless the user asks for sub-agents), play each role yourself, one at a time, reading its role file first; tell the user that isolation is weaker this way, because full paper text and other roles' files then pass through one context.

## Check after every role
After each sub-agent returns, run `python <SKILL_DIR>/scripts/check_run.py docs/ideas/<slug>` before deciding the next move. Files not written yet are not checked, so this works on a partial run. For each problem in a file, spawn the role that owns it again with the problems quoted as `FEEDBACK`; never fix another role's file yourself. Catching a bad citation or a missing field here is cheaper than after three more roles have built on it.

## Workflow

### 1. Set up the run
- Get from the user: the challenge (what current methods fail to meet, why it matters, a concrete failing case) and the problem definition (setting, inputs, outputs). Ask for what is missing; do not invent it.
- Optional cutoff date: only papers first public before it may be used. Offer it when the user wants to test the process on a problem whose answer was published later.
- Ask which language the proposal body should use (default: the user's language).
- Create `docs/ideas/<slug>/` under the project root with `problem.md` (format in artifacts.md). If the project root is unclear, ask.
- Write `plan.md`:
  ```markdown
  # Plan
  - Goal: <one line>
  - Active direction: <G<n>, or none>
  - State: forming
  ## Axes
  - <axis> — <why it matters> — <mapped | not mapped>
  ## History
  - forming: <one line>
  ```
  State is one of `forming`, `drilling`, `under_review`, `survived`, `writing`, `done`, `dead`. On every change, update the State line and append one history line: `<state>: <what happened and why>`.

### 2. Map the landscape (checkpoint 1)
- Propose 2 to 4 axes: distinct sub-questions the challenge implies, each a short phrase in the problem's own terminology. Show them and ask which to map first. Proceed with the user's choice.
- Spawn gap-finder once per axis (`AXIS` verbatim). Run them one after another, not in parallel, so gap numbers do not collide.
- Read `gaps.md` after each. If an axis came back thin or off the brief, spawn gap-finder again on it with `FEEDBACK`.

### 3. Choose a gap (checkpoint 2)
Summarize the gaps (id, one-line gap, deficiency kind, how many near misses were read) and recommend one, saying why. Ask the user to choose. Record it as the active direction; state `drilling`.

### 4. Derive, then ideate
1. Spawn the deriver on the gap, unless `derivations.md` already has its `## Gap:` section. It must run before any innovator touches this gap; that is what keeps its list blind.
2. Spawn the innovator with `TARGET` (the next unused `C<n>`, you choose it) and `GAP`. Record a history line: which candidate, on which gap, building on what, and why.

### 5. Review and act on the verdict
Spawn the reviewer on the candidate; state `under_review`. Then:
- `survive` → state `survived`, go to step 6.
- `revise(focus=<dim>)` → spawn the innovator again with a new `TARGET`, the same `GAP`, and `BUILD_ON` (the candidate, the dimension, the verdict quoted). Review the new candidate. After two revise rounds on the same lineage without `survive`, treat it as reject.
- `reject(...)` → the direction is dead (`dead`, then `forming`). Go back to step 3 with another gap, or to step 2 for a new axis if no gap is left.

The loop is a graph, not a line. Other legitimate moves: gap-finder again when a gap turns out thin; a new axis when every gap is dead; innovator again when the writer replies `blocked`. Let the files, not the step numbers, decide.

### 6. Write up (checkpoint 3)
- Show the user the surviving candidate (intuition, source, mapping, main risk) and the reviewer's verdict, obviousness level, and source-credibility labels.
- Offer a deep read of its main source paper with the paper-dissector skill before writing: the digest answered only the reviewer's questions, and the whole idea rests on that mechanism. Recommend it when the source has no official code or the reviewer's grounding evidence was thin.
- On the user's go-ahead, spawn the writer with `TARGET` and `LANGUAGE`; state `writing`. If the user wants to write up a candidate without `survive`, pass `USER_APPROVED: yes`.
- If the writer replies `blocked — <reason>`, go back to step 4 (innovator with `BUILD_ON`) or step 2, as the reason says.

### 7. Gate
Run `python <SKILL_DIR>/scripts/check_run.py docs/ideas/<slug> --final` (with `--final` a missing or empty `proposal.md` is a problem too) and repeat the fix loop from "Check after every role" until it prints `OK`. State `done`.

### 8. Report
In chat, give only:
- the path of `proposal.md` and its one-sentence thesis;
- the gap it attacks, the source mechanism and field, and the obviousness level the reviewer assigned;
- the reviewer's strongest objection;
- next steps the user can take, each with the skill that does it:
  - theory-auditor: check the derivation behind the proposed objective;
  - table-smith: turn the proposed evaluation into empty main and ablation tables;
  - talk-coach: slides and a script for presenting the idea to the advisor;
  - article-advice: only after the user has verified the idea and made it their own.

## Ethics
- `proposal.md` starts with the AI-generation notice in artifacts.md. Repeat its gist in the report: novelty is judged by models against the papers that were read, not established; the user must check that nobody has done it before using it.
- Never present the idea as the user's own work, and never send it to article-advice as if it were the user's material.
- A paper seen only as a search hit is never cited; `check_run.py` enforces that every citation has a digest.

## Do not
- Do not skip the reviewer, and do not treat `unscored` as evidence of non-obviousness.
- Do not rank or filter papers by venue here; credibility labels inform the user, paper-search decides inclusion.
