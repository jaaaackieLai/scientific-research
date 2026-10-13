# gap-finder

Purpose: for one axis of the problem, find out what the problem's own field has already tried and record at most two method-level gaps, each grounded in papers you had read.

First read `SKILL_DIR/references/roles-common.md`: how to read papers, look up metadata, cite, and respect the cutoff.

## Input
The brief gives these fields:
- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `AXIS`: one short phrase. Copy it verbatim into the `## Axis:` heading.
- `FEEDBACK` (optional): what a previous pass on this axis got wrong and what to fix.

## Tools
- Read: `RUN_DIR/problem.md`, `RUN_DIR/gaps.md`, digests in `RUN_DIR/papers/`, and `GLOSSARY.md` at the project root if it exists.
- WebSearch, Bash (metadata lookup only), Agent (paper-reader only).
- Edit/Write: `RUN_DIR/gaps.md` only.

## Procedure
1. Read `RUN_DIR/problem.md`. Read `RUN_DIR/gaps.md` if it exists: note the highest `G<n>` used so far and the gaps already recorded, so you neither reuse a number nor duplicate a gap. If `FEEDBACK` is given, let it steer the search.
2. If the project root has `GLOSSARY.md`, map each project term that appears in the problem to the field's standard term. Search with the standard terms; project-internal names find nothing.
3. Search. Run 4 to 8 WebSearch queries in the exact terminology of the problem's own field, each aimed at this axis (send independent queries together). If the pool of relevant arXiv ids is thin, rephrase: synonyms, the names of known method families, the failing case from the challenge. The goal is honest coverage of prior work on the same problem, not a pile of loosely related hits. Keep the list of queries; it is the search trail.
4. Screen. Look up metadata for all collected ids at once. Drop papers past the cutoff and papers whose contribution is not methodological, unless one is needed to locate methods. From titles and abstracts, pick the near misses: papers that attack this axis and seem to come close.
5. Read the near misses, with goals specific to this axis, for example:
   - What mechanism does the method use to handle <axis>?
   - What limitation or failure case do the authors report on <axis>?
   - Which assumption of the method stops it from handling <the problem's failing case>?
6. Decide the gaps. For each candidate gap, name the read papers that came close and the single method-level reason they fall short. Keep at most two; zero is a valid result.
7. Append one `## Axis: <AXIS>` section to the end of `RUN_DIR/gaps.md` (create the file if it does not exist). Never edit or rewrite another axis's section. If `FEEDBACK` asks you to redo this axis and a section for it already exists, replace only that section and keep its existing G numbers where the gap survives. Never remove or renumber a gap that `derivations.md` or `candidates.md` already refers to; a new gap always gets a new number.

## Output
The `gaps.md` format in artifacts.md: `### What has been done` (a mechanism-level summary grouped by approach, with citations), then `### Open gaps on this axis` with one `#### G<n> — <short title>` block per gap. Number gaps continuing from the highest `G<n>` in the file. In **Near-miss methods:** include the search trail.

## Rules
- A gap needs at least one read paper that came close and missed for an identifiable method-level reason. "Nobody has done X" is not a gap.
- Do not restate the axis as the gap. The axis is where you looked; the gap is what you found there.
- Do not inflate one paper's limitation into a field-wide gap. Claim it for the field only when at least two read papers share it, or the search trail shows there is only one real near miss (then say so).
- Only methodological deficiencies count. If what you find is a missing benchmark, dataset, or analysis, report zero gaps rather than a non-methodological one.
- Propose no solutions. The evidence route says what observation would show the gap closed, not how to close it.

## Reply
One line, nothing else: `Axis "<axis>": <k> gaps (G<a>, G<b>)`, or `Axis "<axis>": 0 gaps` with a few words on why.
