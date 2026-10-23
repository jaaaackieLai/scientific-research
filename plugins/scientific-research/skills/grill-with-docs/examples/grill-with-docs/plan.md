# Plan: grill-with-docs for this skill pack

- Goal: A grill-with-docs that a researcher can run in one session and leave with a reviewed plan on disk, not only a glossary and a conversation.
- Status: ready
- Flow: one grilling session, from invoking the skill to a plan someone can build from.

## Decisions

### D1 - One self-contained skill
- **Question:** Should the skill keep delegating to separate `grilling` and `domain-modeling` skills, as upstream does?
- **Decision:** No. The interview rules and the glossary and ADR rules are written into this skill and its `references/`. It must not depend on any other skill being installed.
- **Why:** Upstream's most-reported failure is the two dependencies not loading, which gives an unstructured interview with no paper trail.
- **Flow:** removes "Load the grilling and domain-modeling skills"; changes "User types /grill-with-docs"
- **Records:** none

### D2 - Show the current flow against the planned flow
- **Question:** Should the session draw the flow the change touches, as the code does it today and as the plan will make it?
- **Decision:** Yes. Before round 1 the agent draws the current flow from the code on the flow page and shows it for confirmation. After every round that changes the plan it updates the planned side and republishes the same page, so the link stays the same. Every difference on the page names the decision behind it.
- **Why:** The user wants to see what changes at a glance, and a wrong picture of the current flow is cheaper to catch before round 1 than after.
- **Flow:** changes "Explore the codebase for facts"; adds "Show the current flow and confirm it", "Update the planned flow and republish the flow page"
- **Records:** GLOSSARY.md: Current flow, Planned flow

### D3 - Log every decision as it settles
- **Question:** Should every settled decision be written to `plan.md` the moment it settles, not only the ones that earn an ADR?
- **Decision:** Yes. Each decision gets a numbered `### D<n>` entry with the question, the decision, the reason, and the flow steps it touches. Numbers are never reused.
- **Why:** Upstream keeps most decisions only in the conversation, and later steps soften them.
- **Flow:** changes "Write resolved terms to GLOSSARY.md and qualifying decisions as ADRs"
- **Records:** none

### D4 - Isolated plan review before the plan is ready
- **Question:** When the interview ends, should a separate agent that never saw the conversation review the plan before it counts as ready?
- **Decision:** Yes. The reviewer reads only the session files, the glossary, the ADRs and the code, and writes `review-<pass>.md` with a verdict. Blocking findings go back to the user as the next round, never fixed silently. At most two review passes; after the second the user decides.
- **Why:** A reviewer without the conversation is the only test of whether the plan stands on its own.
- **Flow:** changes "Confirm the shared understanding"; adds "Isolated reviewer checks plan.md, flow.html and the code", "Plan is ready to build"
- **Records:** none

## Out of scope
- Writing a spec or tickets from the plan; the plan is the hand-off.
- Multi-session planning for efforts too big for one sitting.

## Open risks
- Flows with many branches crowd the flow page - a session draws more than 15 parts on a side.
