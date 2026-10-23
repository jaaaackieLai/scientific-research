---
name: grill-with-docs
description: Grill the user relentlessly about a plan or design in the current repo, in rounds where every question carries a recommended answer, and write what settles as it settles - each decision to a plan file, terms to GLOSSARY.md, hard-to-reverse decisions as ADRs. Draws the current flow against the planned flow on one page with the diagram-design skill (published as an Artifact when the host can) so every difference and the decision behind it is visible, and ends with an isolated plan-reviewer agent that checks the plan against the code before it counts as ready. Runs only when the user types /grill-with-docs.
disable-model-invocation: true
---

# grill-with-docs

Purpose: one session that turns a fuzzy change into a plan someone else can build from. Three things come out of it, all on disk: a decision log (`plan.md`), a picture of the flow before and after the change, and a cold review of both. Sharper domain vocabulary (`GLOSSARY.md`) and the occasional ADR come along the way.

Adapted from Matt Pocock's `grill-with-docs` (MIT, see `UPSTREAM-LICENSE.md`). Upstream delegates to the `grilling` and `domain-modeling` skills, and when they fail to load the interview loses its structure, so their rules are written here.

## Related files
- `references/session-files.md`: the session directory and the exact format of `plan.md`, `flow.html` and `review-<pass>.md` (always follow it)
- `references/glossary-format.md`, `references/adr-format.md`: how to write the glossary and ADRs
- `../diagram-design/`: the diagram-design skill that draws `flow.html`
- `roles/plan-reviewer.md`: what the reviewer does
- `examples/grill-with-docs/`: a finished session (upstream's flow against this skill's), with its `flow.html`

Below, `<SKILL_DIR>` is the absolute path of this skill's directory and `<run>` is `docs/grill/<slug>` under the project root.

## The interview

Map the change as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask now without guessing at answers you have not heard.

Work in **rounds**. Ask the whole frontier in one round, numbered, each with your recommended answer, then wait. Word each question so that "yes" accepts your recommendation. A question whose answer depends on another question in the same round belongs to a later round.

```
❓ **Q1** - **<question title>**: <question body; may be several paragraphs and list the choices>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

After each round, recompute the frontier: settled decisions unblock the questions that hung off them. Speak the user's language; keep step ids, file names and glossary terms as they are.

**Facts are your job, decisions are the user's.** Never ask the user something the repo can answer. Read the code yourself, or for a broad sweep dispatch an Explore sub-agent, and do not block on it: only the questions downstream of a running lookup wait; ask the rest of the frontier now.

While grilling, keep the language sharp:
- **Challenge against the glossary.** When the user uses a term differently from `GLOSSARY.md`, say so at once: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy words.** For a vague or overloaded term, propose one precise canonical term.
- **Use concrete scenarios.** Invent edge cases that force the boundary between two concepts into the open.
- **Cross-check the code.** When the user says how something works, check it. A contradiction becomes a question: "Your code cancels whole Orders, but you said partial cancellation is possible. Which is right?"

The interview is over when the frontier is empty: every branch visited, nothing silently assumed.

## Workflow

### 1. Ground the session
- Read `GLOSSARY.md` (or `GLOSSARY-MAP.md` and the context it points to), `docs/adr/`, and the code the change touches.
- Choose a slug and create `<run>/plan.md` with its header (`Status: grilling`) and empty sections.
- Pick the one flow the change touches and map its current form from the code. If the change touches more than one flow, ask which one in round 1 and map that.
- Draw the current form alone (step 4). Round 1 opens with "Is this the current flow?" with the page attached: the user confirms the baseline before anything is measured against it. A greenfield change has no current form; say so instead.

### 2. Grill
Run the interview above, round after round.

### 3. Write as it settles
After each round, before asking the next:
- Each settled decision gets its `### D<n>` entry in `plan.md` now, not at the end.
- A resolved term goes into `GLOSSARY.md` now, in the format in `glossary-format.md`. No implementation detail in the glossary.
- Offer an ADR only when the decision passes all three tests in `adr-format.md`. Most sessions produce none.
- A decision that changes the flow changes the planned form on the flow page, marked with its decision id as session-files.md says. Redraw `flow.html` and republish it.
- A reversed decision is marked superseded, never deleted (session-files.md).

### 4. Show the flow
Draw `<run>/flow.html` with the diagram-design skill. It ships beside this skill in `<SKILL_DIR>/../diagram-design/`; if that folder is missing, invoke the `diagram-design` skill instead. This page is what you and the user align on, and what the reviewer reads.

Before drawing, read `<SKILL_DIR>/../diagram-design/SKILL.md` §1 (deletion and focal rules), §3 (type guide) and §7 (complexity budget), then the reference file of the type it picks. Reading one type reference alone is not enough. After drawing, run `python3 <SKILL_DIR>/../diagram-design/scripts/self_check.py --node-budget 9 <run>/flow.html` and fix every error before publishing. Over budget means an overview diagram plus a detail diagram, not smaller boxes.
- Let diagram-design pick the type from the shape of the change (its §3 guide). A rewired data path or module graph is usually an architecture delta; a process with branches is a flowchart. Never flatten a graph into a list of steps to fit a type.
- Follow the format in session-files.md (`## flow.html`). Its layout, one drawing with a Current/Planned switch, replaces diagram-design's side-by-side panels.
- Write `flow.html` once and edit it in place at each redraw. Do not write a script that generates it.
- Skip only diagram-design's style-guide gate and its pause to confirm the type (its rules, budget and checklist still apply): use the project's `.diagram-design` profile when there is one, otherwise the default tokens. Do not interrupt the grilling to ask about the drawing.
- `examples/grill-with-docs/flow.html` is a finished one.

If the host has an Artifact tool, publish `<run>/flow.html` (icon `flow` on the first publish) and republish the same file after each redraw so the link stays the same. Otherwise give the user its path; it opens in a browser.

Show the page at three points: the baseline before round 1, after any round that changed the planned form, and at the end. Rounds that change nothing on the flow publish nothing.

### 5. Close the interview
When the frontier is empty, list the decisions (id and title), link the flow page, and ask the user to confirm that this is the shared understanding. On confirmation, set `Status: reviewing`.

### 6. Plan review
Spawn the plugin agent `scientific-research:grill-plan-reviewer` with the brief `SESSION_DIR: <run>`, `SKILL_DIR: <SKILL_DIR>`, `PASS: 1`. Pass nothing from the conversation; the review tests whether the files stand on their own.

If that agent type is not available (the skill was copied without the plugin), spawn a general-purpose sub-agent with model `inherit` and effort `high` whose brief starts with `Follow <SKILL_DIR>/roles/plan-reviewer.md.` and then the same fields. If the host cannot spawn sub-agents at all, do the review yourself following the role file, and tell the user that it is weaker this way because you saw the conversation.

Then read `<run>/review-1.md`:
- `ready` → set `Status: ready`. Mention any `should` findings in the report.
- `revise` → the blocking findings become the next round: each is a question carrying the reviewer's recommended answer. Never close a blocking finding by editing the plan without the user's answer. Errors of fact in the plan (a wrong file path, a step the code does not do) you correct yourself, and say so in that round. Update `plan.md` and `flow.html` as in step 3, then run the reviewer again with `PASS: 2`.
- `rethink` → stop grilling details. Put the reviewer's strongest objection to the user and ask whether the goal or approach changes; continue from step 2 with what they decide.

At most two review passes. If pass 2 is still not `ready`, report the open findings and let the user decide whether the plan is ready anyway.

### 7. Report
In chat, give only:
- the path of `plan.md`, the number of decisions, and the link or path of the flow page;
- the count of added, changed and removed parts on the flow page;
- the glossary terms and ADRs written (or none);
- the reviewer's verdict and its strongest risk;
- the next step: build from `plan.md`, starting with the parts the flow page marks added or changed, test first.

## Do not
- Do not write code or change anything outside `<run>`, `GLOSSARY.md` and `docs/adr/` during the session. The session produces a plan; building it is a separate step the user starts.
- Do not skip the baseline confirmation or the review because the session ran long; they are the two checks that the plan rests on something real.
