# Session files

One grilling session writes into `docs/grill/<slug>/` under the project root. `<slug>` is a short kebab-case name for the change (`refund-auto-approval`). Create each file at the time the table below gives.

| File | Written by | When |
| --- | --- | --- |
| `plan.md` | orchestrator | created before round 1; one decision added the moment it settles |
| `flow.json` | orchestrator | the current flow before round 1; the planned flow after every round that changes it |
| `flow.html` / `flow.artifact.html` | `scripts/render_flow.py` | every time `flow.json` changes; never edit them by hand |
| `review-<pass>.md` | plan reviewer | after the interview closes; `<pass>` is 1, then 2 |

The glossary and ADRs do not live here. They go where the repo keeps them (`references/glossary-format.md`, `references/adr-format.md`), because they outlive the session.

`examples/grill-with-docs/` is a complete session in this format.

## plan.md

The decision log. Its job is to hold every decision the session settled, precisely enough that someone who missed the conversation could build from it. Decisions that only lived in chat are the main way a grilling session loses work.

```markdown
# Plan: <title>

- Goal: <one sentence: what changes, for whom>
- Status: grilling | reviewing | ready
- Flow: <which flow flow.json maps, in one line>

## Decisions

### D1 - <short title>
- **Question:** <the question as it was put to the user>
- **Decision:** <what was decided; keep numbers, orderings, limits and the things that must NOT happen exactly as the user said them>
- **Why:** <the reason the user gave or accepted>
- **Flow:** <ids of the steps it adds, changes or removes, or `no flow change`>
- **Records:** <GLOSSARY.md terms and ADR files it produced, or `none`>

## Out of scope
- <what this plan deliberately does not do>

## Open risks
- <risk> - <what would show it is happening>
```

Rules:
- Number decisions in the order they settle and never renumber; `flow.json` cites them by number.
- A decision the user later reverses stays in the log with one more field, `- **Status:** superseded by D<m>`, and the new decision says what it replaces. Steps in `flow.json` cite the decision that is in force.
- A fact you found in the code is not a decision. It goes into the question that needed it, not into the log.
- `Out of scope` gets an entry whenever the user says no to something; the reviewer reads it as deliberate.

## flow.json

The flow the change touches, twice: as the code does it today (`as_is`) and as the plan will make it (`to_be`). Pick one flow per session: the path a user, a request, or a piece of data takes through the part of the system the change touches. Keep each side between 3 and 15 steps; merge steps that never differ, split a step only when the plan changes part of it.

```json
{
  "title": "Refund approval",
  "as_is": {"steps": [
    {"id": "submit", "label": "Customer submits the refund form", "actor": "Customer", "next": ["review"]},
    {"id": "review", "label": "Manager reviews every refund", "actor": "Manager"}
  ]},
  "to_be": {"steps": [
    {"id": "submit", "label": "Customer submits the refund form", "actor": "Customer", "next": ["review"]},
    {"id": "review", "label": "Rules engine reviews the refund", "actor": "System", "decision": "D1",
     "next": [{"to": "pay", "when": "amount < 100"}, {"to": "escalate", "when": "amount >= 100"}]},
    {"id": "pay", "label": "Refund is paid", "actor": "System", "decision": "D1"},
    {"id": "escalate", "label": "Manager reviews the refund", "actor": "Manager", "decision": "D1"}
  ]}
}
```

- `id`: kebab-case, unique within its side. The same step keeps the same id on both sides; that is how the diff pairs them. Give a step a new id only when it is a different step, not a reworded one.
- `label`: what happens, in the glossary's words.
- `actor` (optional): who or what does it.
- `next` (optional): the steps that follow, as ids, or as `{"to": "<id>", "when": "<condition>"}` for a branch. A step with no `next` ends the flow.
- `decision`: the `D<n>` that explains the difference. Required on every step the plan adds or changes (on its `to_be` entry) and on every step it removes (on its `as_is` entry).
- A greenfield change has `"as_is": {"steps": []}`.

`as_is` comes from the code, not from what the user remembers. When the code and the user disagree, that is a question for the next round.

`python <SKILL_DIR>/scripts/render_flow.py docs/grill/<slug>` checks the file against `plan.md` and refuses to render while any difference lacks a decision or cites one `plan.md` does not define. A step counts as changed when its label, actor, outgoing edges, or position relative to the shared steps differ.

## review-<pass>.md

Written by the plan reviewer, never edited afterwards. Pass 2 is a new file; pass 1 stays as the record of what was fixed.

```markdown
# Review: <plan title>

- Verdict: ready | revise | rethink
- Pass: <1 | 2>
- Read: plan.md (D1-D<n>), flow.json, <ADRs, glossary, code paths read>

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
