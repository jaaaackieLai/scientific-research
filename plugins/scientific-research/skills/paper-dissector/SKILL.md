---
name: paper-dissector
description: "Deep-read one deep learning paper, check its claims against its experiments and official code, and write a teaching note into the project's `docs/papers/`. Use when the user says \"read this paper\" or \"take notes on this paper\", gives an arXiv link or PDF to analyze, or another agent asks for a paper note."
---

# paper-dissector

Purpose: the reader learns something useful and interesting from the paper: how and why, not only what. The note must work for a person reading it once (a grad student new to the topic) and for an AI using it later. The output is a note file, not a chat reply.

## Related files
Each file is required reading at the step named.
- `references/writing.md`: how to write the note so a person can learn from it, and how to cite the paper (steps 2 and 8)
- `references/setup-checklist.md`: data, training, evaluation, and baseline questions every note answers (step 3)
- `references/experiment-check.md`: whether the experiments support the claims (step 4)
- `references/code-check.md`: comparing the paper against the official code (step 5)
- `references/note-template.md`: note structure and what each section must do (step 8)

## Workflow

### 1. Get the paper
- arXiv papers: read the HTML version (`arxiv.org/html/<id>`) first, since equations survive as text; fall back to the PDF.
- Local PDF: read all pages, including the appendix. Hyperparameters, proofs, and training details are often only there.
- Read the cited papers' abstracts when needed to say what a baseline or a borrowed component is.
- Do not ask the user about purpose or depth before starting. Read first.

### 2. Understand before writing
Answer these for yourself first; the note is built from them, but the answers are not listed as a separate section. Cite the paper for each answer as `references/writing.md` "Citing the paper" says. Questions 1 to 5 follow the Stanford InfoLab five-question structure for an Introduction. Answer them from the whole paper, not only the Introduction, and note when the Introduction itself leaves a question unanswered; that is a finding.
1. What is the problem? State it in one sentence: input, desired output, and what counts as success. (Note: Background and the problem, last sentence)
2. Why is it interesting and important? Give the authors' reason, tagged as below; importance is the claim most often asserted without evidence. (Note: Insight; Background and the problem)
3. Why is it hard? Why does the naive approach fail? Say whether the paper shows this with an experiment or only asserts it. "Hard" and "not done before" are different: a problem nobody tried is not thereby hard. (Note: Background and the problem)
4. Why has it not been solved before? What did people believe or do, and what specifically fails in existing methods? (Define every mechanism you mention.) (Note: Background and the problem)
5. What are the key components and results, and what are the limitations? For each component: what problem it addresses, whether it is borrowed (from which paper) or new, and why it was designed this way. (Note: Method; Claims vs evidence; Limitations and failure conditions)
6. What is the one idea that changes the picture? Why is it surprising or worth knowing? (Note: Insight)
7. Why does the whole thing work? Which links are backed by experiments, which only by the authors' argument, and which are your inference? (Note: Why it works)

Tag statements about mechanism as **[paper]** (the authors say so), **[evidence]** (an experiment shows it), or **[inference]** (your own reasoning). If the paper never explains why the method works, say so; do not invent a mechanism and attribute it to the authors.

### 3. Fill the setup checklist
Follow `references/setup-checklist.md`. Done when every item from 1.1 to 4.3 has an answer or "not stated in the paper".

### 4. Check the experiments
Follow `references/experiment-check.md`. Done when every claim in the claim-to-evidence table has a verdict.

### 5. Compare against the official code (always)
Follow `references/code-check.md`. Every mismatch goes into the note and is reported to the user. If there is no official code, say so in the note header and in the reply; the reading is then marked unverified against code. Done when the note has the commit hash and the mismatch table (or "No mismatches in architecture or stated values"), or says why the code was not checked.

### 6. Check the main derivation
Always, without Lean. It fills the Derivation check section of the note, whose heading says it was not verified by Lean.
- Pick the main derivation: the equations the method's central claim rests on. In a paper without one, take the chain of argument from the key design choice to the main result.
- List its assumptions, including the ones the paper leaves implicit.
- Check each step against the previous one and the assumptions.
- Look for counterexamples, and state the conditions the result needs.
- Tag each step's support as [paper], [evidence], or [inference].

Done when every step has a verdict.

When the user asks for Lean, also load the theory-auditor skill and audit the derivation the user picks; it fills the Lean verification section of the note.

### 7. Add figures (optional)
Do this step when the user or caller wants figures in the note. The extraction or cropping tool is the caller's or the environment's choice.
- Pick the figures that explain the method or show the main results.
- Label each figure with the number its paper caption uses ("Figure 1", "Fig. 3"). The label is the caption's number, not the output file name (`fig-1.png`).
- Embed each figure in the note section it supports, with a short paragraph under it saying what the figure shows.
- When a figure cannot be obtained, put "figure not included: <reason>" where it would go.

### 8. Write the note
- Follow `references/note-template.md` and `references/writing.md`. Write in the user's language; keep equations, code identifiers, and paper terms in their original form.
- If the project has `GLOSSARY.md` at its root, keep the paper's own terms but map each one that names a glossary concept to the glossary term once (paper "teacher" = project "reference model"). If the paper's setup differs from a project ADR (in the folder the root `AGENTS.md` names under `## Domain docs`, `docs/adr/` by default), such as the evaluation split or a metric definition, say so in the note.
- Path: the one the caller names; otherwise `docs/papers/<first-author-surname>-<year>-<keyword>.md` under the current project's root. Create the folder if it does not exist. If the project root is unclear, ask the user or the calling agent.
- Before writing, show the full draft and the target path to the user, or to the calling agent when another agent invoked this skill, and write only after they confirm (a caller can confirm in advance in its request). If the file already exists, show what changes.
- Length: each section follows its own length rule in `references/note-template.md`; the note has no total line limit. When trimming, cut restated results and secondary details first, and the explanations in the Insight through Why it works sections and the code mismatches last.

### 9. Reply
Use the format the caller names, if any. Otherwise, in chat, give only: the note path, the insight in one or two sentences, the paper-vs-code mismatches, and claims marked as weak or unsupported.

## Do not
- Do not judge the paper by venue, authors, or citation count (that is paper-search's job).
- Do not add "action items", "takeaways for your life", or star ratings.
- Do not fill gaps with guesses. Write "not stated in the paper" or "not found in the code".
