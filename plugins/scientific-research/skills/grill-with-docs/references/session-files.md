# Session files

One grilling session writes into `docs/grill/<slug>/` under the project root. `<slug>` is a short kebab-case name for the change (`refund-auto-approval`). Create each file at the time the table below gives.

| File | Written by | When |
| --- | --- | --- |
| `plan.md` | orchestrator | created before round 1; one decision added the moment it settles |
| `flow.html` | orchestrator, with the diagram-design skill | the current flow before round 1; redrawn after every round that changes the plan |
| `review-<pass>.md` | plan reviewer | after the interview closes; `<pass>` is 1, then 2 |

The glossary and ADRs do not live here. They go where the repo keeps them (`references/glossary-format.md`, `references/adr-format.md`), because they outlive the session.

`examples/grill-with-docs/` is a complete session in this format.

## plan.md

The decision log. Its job is to hold every decision the session settled, precisely enough that someone who missed the conversation could build from it. Decisions that only lived in chat are the main way a grilling session loses work.

```markdown
# Plan: <title>

- Goal: <one sentence: what changes, for whom>
- Status: grilling | reviewing | ready
- Flow: <which flow flow.html draws, in one line>

## Decisions

### D1 - <short title>
- **Question:** <the question as it was put to the user>
- **Decision:** <what was decided; keep numbers, orderings, limits and the things that must NOT happen exactly as the user said them>
- **Why:** <the reason the user gave or accepted>
- **Flow:** <the parts of the flow it adds, changes, removes or rewires, named as flow.html names them, or `no flow change`>
- **Records:** <GLOSSARY.md terms and ADR files it produced, or `none`>

## Out of scope
- <what this plan deliberately does not do>

## Open risks
- <risk> - <what would show it is happening>
```

Rules:
- Number decisions in the order they settle and never renumber; `flow.html` cites them by number.
- A decision the user later reverses stays in the log with one more field, `- **Status:** superseded by D<m>`, and the new decision says what it replaces. Marks on `flow.html` cite the decision that is in force.
- A fact you found in the code is not a decision. It goes into the question that needed it, not into the log.
- `Out of scope` gets an entry whenever the user says no to something; the reviewer reads it as deliberate.

## flow.html

The flow the change touches, as the code does it today (current) and as the plan will make it (planned), on one page drawn with the diagram-design skill. It is the page the user aligns on and the file the reviewer reads, so it has to stand on its own. Pick one flow per session: the path a user, a request, or a piece of data takes through the part of the system the change touches.

- One HTML file in the Artifact page contract, whether or not the host can publish it: no `<!DOCTYPE>`, `<html>`, `<head>` or `<body>`, with `<title>` and `<style>` first. The same file is published and opened locally.
- The drawing uses the type diagram-design picks for the shape of the change.
- Before round 1 it shows only the current form. The planned form appears with the first decision that changes the flow. A greenfield change has only the planned form.
- The current form comes from the code, not from what the user remembers. When the code and the user disagree, that is a question for the next round.
- Both forms share one drawing area. A switch under the drawing (`Current` / `Planned`, with Planned selected) shows one form at a time. Build it from two radio inputs and `:checked` selectors, with no script. Put each radio inside the switch next to its label and reach the drawing with `:has()`: a radio placed anywhere else scrolls the page to itself when its label is clicked. A part that exists in both forms sits at the same coordinates in both, so switching moves only what changed. This replaces diagram-design's side-by-side panels. When the type is an architecture delta, keep its node and connector grammar and its change vocabulary; its three-panel layout and its `data-*` metadata contract do not apply. Before round 1 there is no switch. When the page has detail figures, one switch at the top of the page drives every figure, and each figure draws both forms at shared coordinates.
- The primary flow runs left to right: inputs on the left, losses and outputs on the right, parallel branches as rows. Use top to bottom only when the flow has more than 6 sequential steps.
- A change ledger under the drawing lists every difference with its mark, the part, and the decision. Write each entry as a mark line plus one `<p>` of text: inline markup (`<sup>`, `<code>`) placed directly inside a grid or flex item breaks into separate rows. `self_check.py` fails on that pattern.
- Labels use the glossary's words and symbols. A node says what happens to the data ("spectrum × M^f → irfft"), never only where the code lives. File, function and CLI names go in a table under the drawing, one row per changed part, not inside nodes.
- Follow diagram-design's budget: at most 9 nodes per drawing, 1–2 focal (accent) elements, group related nodes in zones, and a legend strip at the bottom for every line and box style used. When the change is larger, draw an overview with zones as nodes and a detail diagram for the zone that changes.
- When the change touches, copies or feeds a learned module (an encoder, a mask generator, a head), draw that module's internals in a detail figure: each layer or block as a node, the tensor shape on every edge, and the hyperparameters that define it (d_model, layers, heads). One box labelled with the class name is not a drawing of the module. Read the module's code to draw it; never infer its structure from the class name.
- When a planned part introduces a mechanism (a transform on a signal, a new loss term, a new comparison), add one detail figure under the flow that draws it on its real axes, for example a spectrum with the kept band and the taper edges, or a time axis with each input's span. Name the part the same way in both figures. A mechanism described only in a node label or the ledger is not shown.
- Every difference carries a mark in diagram-design's change vocabulary (`references/type-architecture-delta.md`), readable without color: `+ ADDED`, `Δ CHANGED`, `− REMOVED`, `REWIRED`. Each mark ends with the decision in force (`· D2`). Unchanged parts carry no mark.
- Static: no animation.

## review-<pass>.md

Written by the plan reviewer, never edited afterwards. Pass 2 is a new file; pass 1 stays as the record of what was fixed.

```markdown
# Review: <plan title>

- Verdict: ready | revise | rethink
- Pass: <1 | 2>
- Read: plan.md (D1-D<n>), flow.html, <ADRs, glossary, code paths read>

## Findings

### R1 - <short title>
- **Severity:** blocking | should | nit
- **Where:** <D<n>, step id, or plan.md section>
- **Problem:** <what is wrong or missing>
- **Evidence:** <file:line, the quoted plan text, or the concrete scenario that breaks>
- **Recommended answer:** <the decision you would propose, worded so the user can accept it with "yes">

## Strongest risk
<one paragraph: the thing most likely to make this plan fail once built>
```

- `ready`: no blocking finding.
- `revise`: blocking findings, each closable by one more decision.
- `rethink`: a blocking finding attacks the goal or the core approach (the code already does it, it breaks a constraint an ADR records, the flow it rests on is not the real one).
- A review with no findings still has `## Findings` with the line `None.`
