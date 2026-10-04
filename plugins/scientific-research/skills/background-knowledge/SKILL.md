---
name: background-knowledge
description: Reads hand-maintained deep learning domain knowledge (label settings, model architectures, data types, training scenarios) for experiment design, evaluation, and reviewing. Use only when the user invokes it manually.
disable-model-invocation: true
---

# background-knowledge

A hand-maintained domain knowledge base that only holds content that affects experimental conclusions. Content is managed by people; see `CONTRIBUTING.md` for the rules.

## File organization

| Axis | Location |
|---|---|
| Label settings | `core/learning-paradigms.md` |
| Model architectures | `core/architectures/<architecture>.md` |
| Data types | `data/<type>.md` |
| Training scenarios | `settings/<scenario>.md` |

## Existing files

| File | Content | Last verified |
|---|---|---|
| `core/learning-paradigms.md` | Training, evaluation, label usage, and research pitfalls for supervised, unsupervised, and semi-supervised learning | 2026-09-25 |

## Which files to read

Decide in this order; do not guess:
1. The files or axis the user specified when invoking.
2. If none specified, check whether the project's AGENTS.md declares its domain.
3. If neither, list the existing files and ask the user to choose.

## Usage rules

- When citing content, give the file name and section.
- For anything the files do not cover, say explicitly "the knowledge base does not have this", then mark separately which parts are general knowledge.
- **Do not add or modify knowledge files on your own.** If you find gaps, outdated content, or contradictions with new literature during use, list them for the user with sources.
- When the user asks you to draft new content, give the draft in the conversation following `CONTRIBUTING.md` and `template.md`, and write it only after the user confirms.
