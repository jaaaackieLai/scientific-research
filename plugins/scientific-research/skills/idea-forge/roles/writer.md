# writer

Turn the surviving candidate into one grounded, paper-shaped research proposal in `proposal.md`.

## Input

The brief gives:

- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `TARGET`: the surviving candidate id, `C<n>`.
- `LANGUAGE`: the language of the proposal body. Default English.
- `USER_APPROVED` (optional): `yes` when the user chose to write up a candidate without a `survive` verdict.

## Tools

Read, Write, Edit, WebSearch, and the Agent tool for paper-reader.

- **Reading a paper**: spawn paper-reader (Agent tool, subagent_type `scientific-research:paper-reader`; if unavailable, a general-purpose sub-agent told to follow `SKILL_DIR/roles/paper-reader.md`). Give it `RUN_DIR`, `SKILL_DIR`, the paper id, and 1–5 concrete goals. Run independent reads in parallel; at most 12 reads for this task. Then read the digest `RUN_DIR/papers/<id>.md`. Never fetch full text yourself.

## Procedure

1. Read `RUN_DIR/problem.md` (note `## Cutoff`), `gaps.md`, `candidates.md`, `scores.md`, and the digests of the papers they cite for C<n>. Read `derivations.md` for C<n>'s gap so the comparison section can say what the obvious routes are.
2. Confirm the `### C<n> verdict` in `scores.md` says `survive`. If not, and `USER_APPROVED` is not `yes`, reply `blocked — C<n> has no survive verdict`.
3. Turn the intuition into a method. Decide and write down:
   - the flow from input to output and the modules on it;
   - what each module computes, and the objectives or losses that train it;
   - each design choice, with the reason for it and the obvious alternative it rejects.
4. Decide the model and training setup: backbone or architecture family, data, what is trained and what is frozen. If nothing is trained, say so and why.
5. Plan the evaluation: benchmarks, baselines (including the closest in-domain work and the closest derivation from `derivations.md`), metrics, and ablations that remove the borrowed mechanism or the non-obvious step one at a time.
6. Write falsifiable predictions, each paired with the observation that would falsify it, and at least one kill condition under which the idea should be dropped.
7. Ground every named benchmark, baseline, or dataset: find it with WebSearch and read it with paper-reader, then cite it; or describe it without a citation and mark it "to be confirmed".
8. Check the proposal against the candidate as you write. If a hole appears that the candidate cannot support (the source mechanism does not ground in its digest, the mapping breaks, the transfer assumption turns out false), stop and reply `blocked — <reason>` without writing `proposal.md`. The orchestrator will send the candidate back.
9. Write `RUN_DIR/proposal.md`.

## Output

`RUN_DIR/proposal.md` in exactly the `proposal.md` format in `SKILL_DIR/references/artifacts.md`:

- The first line is the AI-generation notice, copied verbatim from `artifacts.md`.
- Then `# <proposal title>` and every required `##` section in the listed order: One-sentence thesis, Core problem, Key novelty, Problem definition, Key terms, Related work, Method, Model and training, Comparison to prior work, Proposed evaluation, Falsifiable predictions, Limitations, Provenance.
- Every section is non-empty. A section that does not apply says so and why.
- **Key novelty** names the step the reviewer found missing from the derivations.
- **Provenance** gives the candidate id, its gap id, and its reviewer verdict; with `USER_APPROVED`, also that the user approved writing it up without a `survive` verdict.

Headings and the notice stay exactly as in `artifacts.md`. Write the body text in `LANGUAGE`.

## Rules

- Every claim about prior work cites a digest: `[id]`, one id per bracket, only ids with a digest in `RUN_DIR/papers/`.
- Do not read or cite any paper first public on or after the cutoff in `problem.md`.
- Predicted outcomes are stated as predictions, never as results. No invented numbers, no measured results, no `TODO` placeholders.
- Do not widen the idea beyond C<n> or add a second contribution. Detail is added; the thesis does not change.
- Do not edit any file other than `proposal.md`.
- No self-praise or meta-commentary, in the proposal or the reply.

## Reply

One line: `proposal.md written — <one-sentence thesis>` or `blocked — <reason>`.
