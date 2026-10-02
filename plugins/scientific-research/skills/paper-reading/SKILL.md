---
name: paper-reading
description: Deep-read one deep learning paper and write a note into the background-knowledge base. The note teaches the reader the paper's idea (how and why, not only what): the insight, the problem with existing methods, which parts of the method are borrowed and which are new and why, why it works, the datasets and baselines, and the experimental setup checklist; it checks every claim against the experiments and always compares the paper against its official code, flagging every mismatch. Lean verification of derivations only when the user asks. Use when the user says "read this paper", "help me understand this paper", "deep dive into", "take notes on this paper", or gives an arXiv link / PDF and wants it analyzed.
---

# paper-reading

Purpose: the reader learns something useful and interesting from the paper: how and why, not only what. The note must work for a person reading it once (a grad student new to the topic) and for an AI using it later. The output is a note file, not a chat reply.

## Related files
- `references/note-template.md`: note structure and what each section must do (always follow it)
- `references/writing.md`: how to write the note so a person can learn from it (always follow it)
- `references/setup-checklist.md`: data, training, evaluation, and baseline questions every note answers
- `references/experiment-check.md`: whether the experiments support the claims
- `references/code-check.md`: comparing the paper against the official code (always done)
- `references/lean.md`: Lean verification of derivations (only when the user asks)

## Workflow

### 1. Get the paper
- arXiv papers: read the HTML version (`arxiv.org/html/<id>`) first, since equations survive as text; fall back to the PDF.
- Local PDF: read all pages, including the appendix. Hyperparameters, proofs, and training details are often only there.
- Read the cited papers' abstracts when needed to say what a baseline or a borrowed component is.
- Do not ask the user about purpose or depth before starting. Read first.

### 2. Understand before writing
Answer these for yourself first; the note is built from them. Cite the section, equation, table, or figure for each.
1. What did people believe or do before, and what specifically fails? (Define every mechanism you mention.)
2. What is the one idea that changes the picture? Why is it surprising or worth knowing?
3. For each component of the method: what problem does it address, is it borrowed (from which paper) or new, and why was it designed this way?
4. Why does the whole thing work? Which links are backed by experiments, which only by the authors' argument, and which are your inference?

Tag statements about mechanism as **[paper]** (the authors say so), **[evidence]** (an experiment shows it), or **[inference]** (your own reasoning). If the paper never explains why the method works, say so; do not invent a mechanism and attribute it to the authors.

### 3. Fill the setup checklist
Follow `references/setup-checklist.md`. Every item gets an answer with its location in the paper, or "not stated in the paper".

### 4. Check the experiments
Follow `references/experiment-check.md`.

### 5. Compare against the official code (always)
Follow `references/code-check.md`. Every mismatch goes into the note and is reported to the user. If there is no official code, say so in the note header and in the reply; the reading is then marked unverified against code.

### 6. Lean verification (only on request)
Only when the user asks. Follow `references/lean.md`.

### 7. Write the note
- Follow `references/note-template.md` and `references/writing.md`. Write in the user's language; keep equations, code identifiers, and paper terms in their original form.
- Location: `papers/<first-author-surname>-<year>-<keyword>.md` inside the background-knowledge skill **of the scientific-research source repo** (the git checkout at `plugins/scientific-research/skills/background-knowledge/`). Never write into a plugin cache or a copied skill folder; they are overwritten on update. If the repo location is unclear, ask the user for it.
- Before writing, show the user the full draft and the target path, and write only after they confirm (background-knowledge `CONTRIBUTING.md` Section 8). If the file already exists, show what changes.
- At most 200 lines. Cut restated results and secondary details before cutting the explanations in Sections 1 to 5 or the code mismatches.

### 8. Reply
In chat, give only: the note path, the insight in one or two sentences, the paper-vs-code mismatches, and claims marked as weak or unsupported.

## Do not
- Do not judge the paper by venue, authors, or citation count (that is paper-search's job).
- Do not add "action items", "takeaways for your life", or star ratings.
- Do not fill gaps with guesses. Write "not stated in the paper" or "not found in the code".
