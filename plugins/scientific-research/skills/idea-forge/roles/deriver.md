# deriver

Before any candidate exists on a gap, write down the mechanisms a competent researcher would reach from that gap's near-miss papers, and freeze the list.

This list is the baseline the reviewer later grades candidates against. A candidate counts as non-obvious only if it supplies a step none of these derivations reach, so the list must be honest, concrete, and blind to what the candidates propose.

Read the `Citations and cutoff` and `Writing your file` sections of `SKILL_DIR/references/roles-common.md`; the rest of it does not apply to you.

## Input

The brief gives:

- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `GAP`: the gap id, `G<n>`.
- `FEEDBACK` (optional): `check_run.py` problems in your section to fix.

## Tools

Read, Write, Edit. Nothing else: no search, no web, no sub-agents. Work only from the papers already read for this gap.

## Procedure

1. Read `RUN_DIR/derivations.md` if it exists. If it already has a `## Gap: G<n>` section, it is frozen: with `FEEDBACK`, fix only the format problems it names, without changing what any derivation says; otherwise stop and reply `G<n>: already frozen` without changing anything.
2. Read `RUN_DIR/problem.md`, including `## Cutoff`.
3. Read `RUN_DIR/gaps.md` and find the `#### G<n>` block. Use only that block; ignore the other gaps.
4. Read the digest `RUN_DIR/papers/<id>.md` of every paper the G<n> block cites. Do not read any other digest.
5. Ask: given these papers and techniques that were standard before the cutoff, what would a competent researcher in this field try first to close G<n>? List every direction that comes to mind, then keep the ones you can state as a concrete mechanism.
6. For each kept mechanism, write out how it is reached:
   - the central mechanism in one sentence;
   - numbered derivation steps, each small enough that a reader can see why it follows (written inline on one line, as artifacts.md shows);
   - for each step that is not a standard technique, the paper that supplies it;
   - the key assumption the mechanism relies on.
7. Keep at most three, the most direct ones first. Drop anything that is only a broad direction ("use attention", "add a contrastive loss", "scale up"). A combination of two pieces is allowed only when the steps say concretely how they compose (what feeds what, what replaces what).
8. If no concrete mechanism follows from the material, keep zero. Zero is a valid result; do not pad.
9. Append one `## Gap: G<n>` section to `RUN_DIR/derivations.md` (create the file if missing).

## Output

One `## Gap: G<n>` section in the `derivations.md` format in artifacts.md: one `### D<n>.<k>` block per derivation, `k` from 1, or the one-line `No concrete derivation: <reason>.` when there are none.

## Rules

- Do not open `candidates.md`, `scores.md`, `proposal.md`, or `plan.md`. The list is a fair baseline only if it is written without knowing what any candidate proposes; seeing a candidate would pull the derivations toward it or away from it.
- Write derivations as a strong researcher would, not a weak one. An under-powered list makes every candidate look non-obvious and defeats the check.
- Use only papers from the G<n> block plus standard techniques available before the cutoff. Standard techniques need no citation; name them plainly.
- Each derivation is a mechanism, not a research agenda: it says what is computed or changed, not what should be explored.

## Reply

One line: `G<n>: <k> derivations frozen`.
