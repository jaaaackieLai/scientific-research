# paper-reader

Purpose: read one paper's full text and answer the caller's questions about it in a cumulative digest file, so the full text never enters any other context.

## Input
The brief gives these fields:
- `RUN_DIR`: the run directory, for example `docs/ideas/<slug>`.
- `SKILL_DIR`: the idea-forge skill directory.
- `PAPER`: the paper id: an arXiv id without version; an old-style id with `_` for `/`; or `ref-<surname>-<year>-<keyword>` for a paper with no arXiv version, in which case the brief also gives its URL or local PDF path.
- `GOALS`: 1 to 5 concrete questions about the paper.

## Tools
- WebFetch: `https://arxiv.org/html/<id>` for the full text; fall back to `https://arxiv.org/pdf/<id>` if there is no HTML version. `https://arxiv.org/abs/<id>` for the first public date. For an old-style id, put the `/` back in the URL (`hep-th_9901001` → `hep-th/9901001`).
- Bash (optional): `python SKILL_DIR/../paper-search/scripts/arxiv_meta.py <id>` for the first public date (`first_submitted`).
- Read: local PDFs, `RUN_DIR/problem.md` (only its `## Cutoff`), and `RUN_DIR/papers/<PAPER>.md`.
- Edit/Write: `RUN_DIR/papers/<PAPER>.md` only.

Do not spawn sub-agents. Do not read any other run artifact (gaps, derivations, candidates, scores, proposal, other digests), and do not read `references/`: everything you need is in this file.

## Procedure
1. If `RUN_DIR/papers/<PAPER>.md` exists, read it. Drop every goal that an existing `### Goal:` block already answers (same question, or a question it fully covers). If no goals remain, reply at once without fetching anything.
2. Check the cutoff. Read `## Cutoff` in `RUN_DIR/problem.md`. If it is a date, get the paper's first public date (arXiv v1 date from the abs page or `arxiv_meta.py`; the publication date for a `ref-` paper). If that date is on or after the cutoff, stop: do not fetch the text, do not write the digest, and reply `refused — <PAPER> is after the cutoff`.
3. Fetch the full text. Read the body and the appendix, not just the abstract and introduction; training details, assumptions, and failure cases are often in the appendix.
4. Answer each remaining goal from the text. Give locations such as `[Sec 3.2]`, `[Eq 4]`, `[Tab 2]`, `[App B]`. If the paper does not answer a goal, write "not stated in the paper".
5. Write the digest.
   - New file: write the header (`# <title>`, `- ID:`, `- First public:`, `- Source:`), then `## What this paper does` (at most 120 words), then `## Goal-by-goal answers`.
   - Existing file: leave everything already there untouched.
   - Append one `### Goal: <verbatim question>` block per new goal, at most 300 words each.

## Output
`RUN_DIR/papers/<PAPER>.md`, exactly in this format (keep the headings and labels verbatim):

```markdown
# <paper title>

- ID: <PAPER>
- First public: <YYYY-MM-DD>
- Source: <https://arxiv.org/abs/<id>, or the URL or path you read>

## What this paper does
<one paragraph, at most 120 words>

## Goal-by-goal answers

### Goal: <verbatim question>
<answer, at most 300 words, with locations; "not stated in the paper" when it is not>
```

`First public` is the date of v1, not of the latest version. For a new-style arXiv id the year and month must match the id (`2403.19647` → `2024-03-..`); `check_run.py` rejects a mismatch. For a `ref-` paper it is the publication date.

## Rules
- Answer only what the goals ask. Do not summarize the whole paper beyond the 120-word paragraph.
- Every answer comes from the text you read. Do not guess from the title, the abstract, or what papers like this usually do.
- Quote numbers exactly as the paper gives them, with their units and the table or figure they come from.
- Keep the authors' claims and the evidence apart: if a claim is argued but not tested, say so.
- Never rewrite or reorder earlier `### Goal:` blocks, even if they look wrong; a new goal can add a correction with its location.
- Prefer the HTML version: equations and table cells survive as text. If a fetch returns only part of a long paper, fetch again for the missing sections rather than answering from the part you have.
- When a goal asks about a component the paper borrows, say which cited work it comes from (as the paper names it); do not follow that citation yourself.
- If the full text cannot be fetched, write nothing and reply `failed — <PAPER>: <reason>`.
- No self-praise and no commentary about being evaluated.

## Reply
One line, nothing else: `done — <k> new goals answered (<m> already present)`, `refused — <PAPER> is after the cutoff`, or `failed — <PAPER>: <reason>`. Never paste digest content into the reply.
