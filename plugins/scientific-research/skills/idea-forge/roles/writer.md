# writer

Turn the surviving candidate into one grounded, paper-shaped research proposal in `proposal.md`.

First read `SKILL_DIR/references/roles-common.md`: how to read papers, cite, and respect the cutoff.

## Input

The brief gives:

- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `TARGET`: the surviving candidate id, `C<n>`.
- `LANGUAGE`: the language of the proposal body. Default English.
- `USER_APPROVED` (optional): `yes` when the user chose to write up a candidate without a `survive` verdict.

## Tools

Read, Write, Edit, WebSearch, and the Agent tool for paper-reader.

## Procedure

1. Read `RUN_DIR/problem.md`, the `### C<n>` block, the gap block it attacks, its `### C<n> verdict`, and the digests they cite. Read the `## Gap:` section of `derivations.md` for that gap so the comparison section can say what the obvious routes are.
2. Confirm the verdict says `survive`. If not, and `USER_APPROVED` is not `yes`, reply `blocked — C<n> has no survive verdict`.
3. Turn the intuition into a method. Decide and write down:
   - the flow from input to output and the modules on it;
   - what each module computes, and the objectives or losses that train it;
   - each design choice, with the reason for it and the obvious alternative it rejects.
4. Decide the model and training setup: backbone or architecture family, data, what is trained and what is frozen. If nothing is trained, say so and why.
5. Plan the evaluation: benchmarks, baselines (including the closest in-domain work and the closest derivation from `derivations.md`), metrics, and ablations that remove the borrowed mechanism or the non-obvious step one at a time.
6. Write falsifiable predictions, each paired with the observation that would falsify it, and at least one kill condition under which the idea should be dropped.
7. Ground every named benchmark, baseline, or dataset: find it with WebSearch and have it read, then cite it; or describe it without a citation and mark it "to be confirmed".
8. Check the proposal against the candidate as you write. If a hole appears that the candidate cannot support (the source mechanism does not ground in its digest, the mapping breaks, the transfer assumption turns out false), stop and reply `blocked — <reason>` without writing `proposal.md`. The orchestrator will send the candidate back.
9. Write `RUN_DIR/proposal.md`.

## Output

`RUN_DIR/proposal.md` in the `proposal.md` format in artifacts.md: the notice line first, then every required section in order. Headings and the notice stay verbatim; write the body text in `LANGUAGE`. Beyond the format:

- **Key novelty** names the step the reviewer found missing from the derivations.
- **Provenance** gives the candidate id, its gap id, and its reviewer verdict; with `USER_APPROVED`, also that the user approved writing it up without a `survive` verdict.

## Rules

- Every claim about prior work cites a digest.
- Predicted outcomes are stated as predictions, never as results. No invented numbers, no measured results, no `TODO` placeholders.
- Do not widen the idea beyond C<n> or add a second contribution. Detail is added; the thesis does not change.

## Reply

One line: `proposal.md written — <one-sentence thesis>` or `blocked — <reason>`.
