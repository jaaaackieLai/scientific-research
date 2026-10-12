# Rules for every idea-forge role

Read this once at the start of your task. Your role file adds what is specific to you. (paper-reader has its own self-contained rules and does not read this file.)

## Reading a paper
- Only paper-reader reads a paper's full text. Never fetch arXiv HTML or PDF yourself.
- Before asking for a read, look in `RUN_DIR/papers/`: an existing digest may already answer your question. Ask only goals it does not cover.
- Spawn paper-reader with the Agent tool, subagent_type `scientific-research:idea-paper-reader`. If that type is unavailable, spawn a general-purpose sub-agent whose brief starts with `Follow SKILL_DIR/roles/paper-reader.md.`
- Brief fields: `RUN_DIR`, `SKILL_DIR`, `PAPER` (the id), `GOALS` (1 to 5 concrete questions). For a `ref-` paper, also give its URL or local PDF path.
- Launch independent reads in parallel in one turn. At most 12 reads per task.
- Replies: `done` → read `RUN_DIR/papers/<id>.md`. `refused` (after the cutoff) or `failed` → drop that paper and do not cite it.

## Metadata lookup
- `python SKILL_DIR/../paper-search/scripts/arxiv_meta.py <id> <id> ...`, all ids in one call. It returns title, authors, `first_submitted` (first public date), comments, abstract, and code links.
- If `SKILL_DIR/../paper-search/scripts/` does not exist, WebFetch `https://arxiv.org/abs/<id>` for metadata only.
- Metadata and abstracts are for choosing what to read. Never cite or argue from them.

## Citations and cutoff
- Cite as `[id]`, one id per bracket, with ids as defined in `references/artifacts.md`, and only ids that have a digest in `RUN_DIR/papers/`. A search hit you did not have read is not evidence.
- Read `## Cutoff` in `RUN_DIR/problem.md`. If it is a date, never read or cite a paper first public on or after it.

## Fixing gate problems
If the brief has `FEEDBACK` quoting `check_run.py` problems in your file, fix exactly those, only in your own blocks, and change nothing else.

## Writing your file
- Follow the format for your file in `references/artifacts.md` exactly; keep headings and field labels verbatim and in English.
- Write only your own file, and only your own blocks in it; never edit another role's file.
- Methodological contributions only: a new method, algorithm, model, training procedure, objective, or representation. Not a benchmark, dataset, survey, or analysis.
- No self-praise and no commentary about being evaluated.
