# Knowledge base maintenance rules

Rules for maintainers. Goal: keep only what is useful, and do not let information pile up without limit.

## 1. Inclusion criteria

Every piece of content must answer: **which mistake does it prevent?** If it cannot answer that, do not include it.

Include only if it meets one of the following:
- Easy to get wrong, and would invalidate experimental conclusions
- The community has a fixed convention, and not following it will be questioned by reviewers
- Controversial, and you need to know each side's position

Do not include: textbook common knowledge, special settings of a single project (put those in that project's AGENTS.md).

Paper notes in `papers/` are the exception: they follow the paper-reading skill's note template instead of these criteria, but Sections 2, 4, and 8 still apply.

## 2. Sources

Every claim comes with a verifiable source. Content without a source is not included.

## 3. Before adding

1. First check whether existing files already have the same or similar content; merge when possible.
2. Decide which axis it goes in; each topic lives in only one place, and other places point to it by file name and section.
3. New files follow `template.md`; file names use lowercase English with hyphens, e.g. `time-series.md`.

## 4. Length limit

A single file does not exceed 200 lines. When adding content to a file already at the limit, first delete the least important content.

## 5. Conflicts

When two sources disagree, write both into the "Open controversies" section with their sources; do not delete one in favor of the other.

## 6. Deletion

Delete if any of the following holds:
- A control test (the same question asked once with the file and once without) shows no difference in the answers
- The source has been refuted or retracted

## 7. Change log

After adding, modifying, or deleting, update the "Existing files" table and verification date in `SKILL.md`.

## 8. Claude's role

Claude may help look things up and draft, but may not write on its own. Drafts are written into files only after the maintainer reviews them.
