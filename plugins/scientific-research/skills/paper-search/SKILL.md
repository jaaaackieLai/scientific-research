---
name: paper-search
description: Search and filter deep learning papers by fixed quality criteria. Checks the publication venue (journal/conference), whether an arXiv paper has a formal publication, the authors' institutions and countries, and whether code is provided; eliminates papers that do not qualify, and outputs the list of papers that pass with the reason for each decision. Use when the user says "find papers", "search papers for me", "what related papers are there", "find a survey", "is this paper trustworthy".
---

# paper-search

Purpose: eliminate untrustworthy and irreproducible papers, keeping only those that pass the thresholds. Do not score or rank papers.

## Related files
- `references/venues.md`: list of acceptable journals and conferences (whitelist)
- `references/institutions.md`: acceptable universities and companies (with country and QS ranking)
- `references/aliases.json`: aliases and easily confused similar names for matching (used by `match.py`)
- `scripts/arxiv_meta.py`: batch-fetch arXiv abstract pages and HTML versions (title, first public date, Comments, author institutions, code links)
- `scripts/match.py`: decide whether the publication venue (G1) and author institutions (G4) are on the lists
- `scripts/check_repo.py`: batch-check GitHub repos (G3)

In the commands below, `scripts/` means the scripts folder in this skill's directory; use absolute paths when running.

## Standard practice
- **Do not read PDFs.** For arXiv papers, always use the abstract page or HTML version (handled by `arxiv_meta.py`).
- **Do not open arXiv or GitHub pages one by one with WebFetch**; hand the whole batch of IDs or repos to the scripts at once.
- **Always decide G1 and G4 with `match.py`**; do not check against the lists yourself. If a result is clearly wrong (e.g. a missing alias), report the decision as is, note it in the remarks, and suggest the user add it to `aliases.json`.
- Use WebSearch in only two places: finding candidate papers, and looking up fields the scripts report as `unknown`. When multiple queries are needed, send them all at once.

## Workflow

### 1. Search for candidate papers
- Use WebSearch; do not call academic APIs.
- What to search, how many papers, and whether to restrict years follow the user's request; this skill does not set them.
- Record each paper's arXiv ID (for papers without an arXiv version, record the title and source).

### 2. Batch lookup and decisions

**Step A: run all arXiv papers at once**

```bash
python scripts/arxiv_meta.py <arXiv ID 1> <arXiv ID 2> ... | python scripts/match.py meta -
```

Each paper gets:
- `G1`: `pass`, `fail` (only excluded venues such as workshops, Findings, under review) or `unknown` (the arXiv page does not state an accepted venue)
- `G4`: `pass`, `fail` (none of the institutions in the author block are in the table) or `unknown` (the author block lists no institutions)
- `code_links`: GitHub links from Comments, the abstract, and the paper's first page, usually the authors' own repo
- `code_links_in_paper`: links elsewhere in the body, possibly citing other people's tools; confirm whether the repo owner is an author

Papers with `fail` on G1 or G4 are eliminated directly (for a G1 `fail`, still search once for another formal version).

**Step B: look up only the `unknown` fields**
- `G1 unknown`: WebSearch the paper title for a formal version (openaccess.thecvf.com, openreview.net, aclanthology.org, proceedings.mlr.press, proceedings.neurips.cc). Once found, decide with `python scripts/match.py venue "venue name"`. If no formal version is found, handle it under G2.
- `G4 unknown`: check each author's personal pages (personal website, Google Scholar, LinkedIn), using their affiliation at the time the paper was published. Once found, decide with `python scripts/match.py inst "institution name"`. Mark "unconfirmed" only if nothing can be found, and treat G4 as failed.
- Papers without an arXiv version: use WebSearch to find the venue and author institutions, then decide with `match.py venue` and `match.py inst`.

**Step C: check the code of all papers that passed G1 and G4 at once**

```bash
python scripts/check_repo.py <repo 1> <repo 2> ...
```

- Use `code_links` first; if none, look at `code_links_in_paper`; only if neither exists, WebSearch `title github`.
- A repo reported as `exists: false` counts as no code.
- A repo whose owner is not an author or the authors' organization (e.g. a community reimplementation package) does not count; G3 fails.

### 3. Hard thresholds (failing any one eliminates the paper)

| ID | Condition | Explanation |
|---|---|---|
| G1 | Venue is on the acceptable list (arXiv handled under G2) | See venues.md |
| G2 | Papers only on arXiv must meet one of the following | (a) a survey with citations ≥ 100; (b) authors are "academic authorities" (defined below) |
| G3 | Provides official code (not for surveys or purely theoretical papers) | Only official repos are accepted (defined below); having only third-party implementations counts as no code |
| G4 | At least one author's institution is in the institutions.md table | Eliminated if none are in the table |

**Academic authority**: the first author or corresponding author meets one of the following
- Their institution is in the `institutions.md` table
- h-index ≥ 40 (look up the author's Google Scholar profile with WebSearch)

**Official code**: meets both
- The repo is maintained by the paper's authors themselves, or by an account of the authors' lab or institution (compare the owner in `full_name` reported by `check_repo.py` against the author list)
- The paper, arXiv page, project page, or an author's personal page links to this repo

**Company matching**: by company. Any division under a company counts, e.g. Alibaba Group and Alibaba DAMO Academy both count as Alibaba; NVIDIA and NVIDIA Research both count as NVIDIA.

Look up citations only for G2 (arXiv surveys need ≥ 100); do not look them up otherwise.

### 4. Output format

List all papers that pass the thresholds, without scoring or ranking. One block per paper:

```
### [Title](link to formal version)
- Published: CVPR 2024 (arXiv: 2403.xxxxx) | on the list
- Author institutions: XX University (USA, QS 16), YY University (Japan, QS 64)
- Code: https://github.com/... (official, owner: author XXX)
- Thresholds: G1 ✓ G2 ✓ G3 ✓ G4 ✓
- Remarks: ...
```

At the end, attach a short "Eliminated papers" table listing the elimination reason (corresponding to G1/G2/G3/G4), so the user can double-check.

## Notes
- Mark information that cannot be found as "unconfirmed"; do not guess.
- Institutions are based on **the institutions listed in the paper's author block**; check authors' personal pages only when the author block lists none.
- Institution and country are only indirect indicators of credibility and cannot prove a paper is correct; when in doubt, check Retraction Watch for retractions.
