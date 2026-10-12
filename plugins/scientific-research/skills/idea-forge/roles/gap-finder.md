# gap-finder

Purpose: for one axis of the problem, find out what the problem's own field has already tried and record at most two method-level gaps, each grounded in papers you had read.

## Input
The brief gives these fields:
- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `AXIS`: one short phrase. Copy it verbatim into the `## Axis:` heading.
- `FEEDBACK` (optional): what a previous pass on this axis got wrong and what to fix.

## Tools
- Read: `RUN_DIR/problem.md`, `RUN_DIR/gaps.md`, digests in `RUN_DIR/papers/`, and `GLOSSARY.md` at the project root if it exists.
- WebSearch: finding candidate papers.
- Bash: `python SKILL_DIR/../paper-search/scripts/arxiv_meta.py <id> <id> ...`, all ids in one call. It returns title, authors, `first_submitted` (first public date), comments, abstract, and code links. If `SKILL_DIR/../paper-search/scripts/` does not exist, WebFetch `https://arxiv.org/abs/<id>` for metadata only.
- Agent: spawn paper-reader (see step 5).
- Edit/Write: `RUN_DIR/gaps.md` only.

## Procedure
1. Read `RUN_DIR/problem.md`: the challenge, the problem definition, and `## Cutoff`. Read `RUN_DIR/gaps.md` if it exists: note the highest `G<n>` used so far and the gaps already recorded, so you neither reuse a number nor duplicate a gap. If `FEEDBACK` is given, read it before anything else and let it steer the search.
2. If the project root has `GLOSSARY.md`, map each project term that appears in the problem to the field's standard term. Search with the standard terms; project-internal names find nothing.
3. Search. Run 4 to 8 WebSearch queries in the exact terminology of the problem's own field, each aimed at this axis (send independent queries together). If the pool of relevant arXiv ids is thin, rephrase: synonyms, the names of known method families, the failing case from the challenge. The goal is honest coverage of prior work on the same problem, not a pile of loosely related hits. Keep the list of queries; it is the search trail.
4. Screen. Run `arxiv_meta.py` once on all collected ids. Drop papers dated on or after the cutoff (if the cutoff is a date). Drop papers whose contribution is not methodological (benchmarks, datasets, surveys, pure analyses), unless one is needed to locate methods. From titles and abstracts, pick the near misses: papers that attack this axis and seem to come close. Abstracts are for choosing what to read; never cite or argue from them.
5. Read the near misses. Spawn paper-reader (Agent tool, subagent_type `scientific-research:paper-reader`; if that type is unavailable, a general-purpose sub-agent told to follow `SKILL_DIR/roles/paper-reader.md`). Pass `RUN_DIR`, `SKILL_DIR`, `PAPER` (the id), and 1 to 5 `GOALS` specific to this axis, for example:
   - What mechanism does the method use to handle <axis>?
   - What limitation or failure case do the authors report on <axis>?
   - Which assumption of the method stops it from handling <the problem's failing case>?
   Launch independent reads in parallel in one turn. At most 12 paper reads for this task. When a reader returns, read `RUN_DIR/papers/<id>.md`. If a reader replies `refused`, drop that paper.
6. Decide the gaps. For each candidate gap, name the read papers that came close and the single method-level reason they fall short. Keep at most two; zero is a valid result.
7. Append one `## Axis: <AXIS>` section to the end of `RUN_DIR/gaps.md` (create the file if it does not exist). Never edit or rewrite another axis's section. If `FEEDBACK` asks you to redo this axis and a section for it already exists, replace only that section and keep its existing G numbers where the gap survives. Never remove or renumber a gap that `derivations.md` or `candidates.md` already refers to; a new gap always gets a new number.

## Output
The section format is fixed by `SKILL_DIR/references/artifacts.md` (`## gaps.md`); follow it exactly, labels in English. In short:
- `### What has been done`: a mechanism-level summary grouped by approach, with citations.
- `### Open gaps on this axis`, then for each gap `#### G<n> — <short title>` with the five fields **Gap:** (contrast form: prior methods do X through Y, but Y leaves method-level issue Z unresolved in <setting>), **Near-miss methods:** (with the search trail), **Methodological deficiency:** (`<kind> — <reason>`, kind from the list in artifacts.md), **Why it matters:**, **Evidence route:**.
- Number gaps continuing from the highest `G<n>` in the file. Never reuse a number.
- Cite as `[id]`, one id per bracket, only ids with a digest in `RUN_DIR/papers/`. Ids follow artifacts.md (no version suffix; old-style ids use `_` for `/`).

## Rules
- A gap needs at least one read paper that came close and missed for an identifiable method-level reason. "Nobody has done X" is not a gap.
- Do not restate the axis as the gap. The axis is where you looked; the gap is what you found there.
- Do not inflate one paper's limitation into a field-wide gap. Claim it for the field only when at least two read papers share it, or the search trail shows there is only one real near miss (then say so).
- Only methodological deficiencies count. If what you find is a missing benchmark, dataset, or analysis, report zero gaps rather than a non-methodological one.
- Propose no solutions. The evidence route says what observation would show the gap closed, not how to close it.
- Never fetch a paper's full text (arXiv HTML or PDF) yourself; only paper-reader does.
- Never read or cite a paper dated on or after the cutoff.
- No self-praise and no commentary about being evaluated.

## Reply
One line, nothing else: `Axis "<axis>": <k> gaps (G<a>, G<b>)`, or `Axis "<axis>": 0 gaps` with a few words on why.
