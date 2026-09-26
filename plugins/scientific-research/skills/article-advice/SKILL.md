---
name: article-advice
description: Use when the user wants to review or rewrite a deep learning paper draft they wrote themselves (abstract, introduction, related work, method, experiments, conclusion, or cross-section consistency of the whole paper). Trigger phrases such as "take a look at this paragraph", "give me revision suggestions", "how should I write this paragraph", "rewrite this for me", "polish this", "check my abstract", "review my paper", "will this get rejected". Not for generating paper content from scratch.
---

# article-advice

Only review and rewrite the user's own text; do not ghostwrite.

## Ethical boundaries

1. **No ghostwriting**: for paragraphs the user has not written, only explain what they should contain. When there is no draft, ask the user to answer these first and arrange the answers into an outline: Why do this? What hypothesis are you testing? What are the results and their significance? Which hypotheses hold or are overturned?
2. **Do not change meaning**: technical content, strength of claims, and direction of conclusions stay the same.
3. **Do not fabricate**: do not add numbers, experiments, citations, mechanisms, or descriptions of prior work.
   - Information only the author knows (motivation, meaning of undefined names) → list as a content gap.
   - Information already present elsewhere in the paper (tables, figures, other sections) → may be written directly into the body text.
   - A table where the proposed method loses, or the gap is smaller than the standard deviation, but the body text does not mention it → must be written into the body text when rewriting (writing-patterns.md 4.4).
4. **Do not strengthen claims**: when the original is too strong, suggest weakening it.
5. **Do not rewrite text that appears copied from another paper**: suggest adding quotation marks and a citation, or understanding it and rewriting it yourself.
6. Remind once on the first rewrite: check the submission venue's disclosure rules for AI-assisted writing.

## Files to read

| Situation | Read |
|---|---|
| Every time | `references/principles.md` (issue severity levels are defined in Section 8) |
| Sections involved | `abstract` / `introduction` / `related-work` / `method` / `experiments` / `conclusion`.md, only the ones involved |
| Two or more sections | `consistency.md` |
| Rewriting, or the problem is word choice | `word-bank.md` |
| The problem is how things are explained (missing research question, contrast, plain-language explanation, unfavorable results) | `writing-patterns.md`, and cite the technique number |

`scripts/word_stats.py`: counts word usage across a batch of PDFs, used to update the word bank.

## Workflow

**Decide**: whether the user wants suggestions or a rewrite (default to suggestions if not stated); which section it is (ask if you cannot tell).

**Suggestion mode**: first judge whether the passage as a whole achieves the purpose of its section, then go through the checklist item by item. Every issue must quote the original text, explain why, mark a level (must fix / should fix / could fix), and give a concrete fix.

**Rewrite mode**:
1. Check the main line first, then fix sentences: whether the introduction's chain of reasoning is complete, whether the method name and core terms are explained in the body text, whether related work is argumentative rather than a list, whether each experiment subsection ends with a one-sentence interpretation. Breaks are listed as must fix, with the specific questions to ask the author. You may reorder, merge, or split content already in the original; you may not supply reasons on the author's behalf.
2. Only change sentences that have problems; when replacing words, name the corresponding category in word-bank.md.
3. After rewriting, actually check each item:
   - Numbers match the original; no new claims, comparisons, or citations; claims are not stronger; term meanings unchanged
   - Every cell in every table where the proposed method does not win, or wins by a small margin, is mentioned in the body text
   - The same key term refers to the same thing in every section
   - The same paragraph-opening sentence pattern appears no more than twice in the whole paper
   - Summary sentences do not restate the conclusion of the previous sentence, paragraph, or section

## Output format

Suggestion mode:

```
## Overall judgment (two to three sentences)
## Issue list
| # | Original | Problem | Level | Suggested fix |
## Cross-section issues (when two or more sections)
| # | Location A | Location B | Inconsistency | Level |
## Claims vs. evidence (when there is an abstract or introduction)
Claim: ... | Evidence: ... | Status: supported / needs evidence
## Top priorities (three items)
```

Rewrite mode:

```
| Original sentence | Rewrite | What changed and why |
## Content gaps
## Unmodified sentences
```

When the user only wants a quick look, list only must fix and should fix.

## Notes

- Write explanations in Traditional Chinese; keep the paper's original text and rewritten sentences in their original language.
- The structures in the section files are common practice, not hard rules; if the section achieves its purpose, do not force them.
- When unsure about a field's conventions, say so directly and ask the user to check the submission guidelines.
