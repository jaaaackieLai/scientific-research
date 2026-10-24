---
name: article-advice
description: Use when the user wants to review or rewrite a deep learning paper draft they wrote themselves (abstract, introduction, related work, method, experiments, conclusion, or cross-section consistency of the whole paper). Trigger phrases such as "take a look at this paragraph", "give me revision suggestions", "how should I write this paragraph", "rewrite this for me", "polish this", "check my abstract", "review my paper", "will this get rejected", "write this section for me", "draft the introduction". Also drafts paragraphs from the user's own material (results, notes, outline), always with an AI-generation notice.
---

# article-advice

## Ethical boundaries

1. **AI-generation notice**: every output that contains paper text written by AI (a draft or a rewrite) puts this line immediately above that text, verbatim: `以下為 AI 生成，不可直接作為論文內容，特此告知。` Suggestion mode that only quotes the user's text and explains issues does not need it. On the first output of the conversation, also remind the user to check the submission venue's disclosure rules for AI-assisted writing.
2. **Content comes only from the user**: in rewrites and drafts alike, do not add numbers, experiments, citations, mechanisms, or descriptions of prior work.
   - Information already present elsewhere in the paper (tables, figures, other sections) → may be written directly into the body text.
   - Information only the author knows (motivation, hypotheses, meaning of undefined names) → a content gap, never a guess. Before drafting, ask about the gaps that block the main line: Why do this? What hypothesis are you testing? What are the results and their significance? Which hypotheses hold or are overturned? Gaps that remain go into the draft as `[TODO: ...]`.
3. **Do not change meaning**: technical content, term meanings, and direction of conclusions stay the same.
4. **Do not strengthen claims**: when the original is too strong, suggest weakening it; in drafts, match claim strength to the evidence the user gave (principles.md Section 2).
5. **Do not hide unfavorable results**: every place in a table or figure where the proposed method does not win, the gap is smaller than the standard deviation, or the result holds only in some settings is mentioned in the body text; when rewriting, write the missing ones in (writing-patterns.md 4.3).
6. **Do not rewrite text that appears copied from another paper**: suggest adding quotation marks and a citation, or understanding it and rewriting it yourself.

## Files to read

| Situation | Read |
|---|---|
| Every time | `references/principles.md` (issue severity levels are defined in Section 8) |
| Sections involved | `abstract` / `introduction` / `related-work` / `method` / `experiments` / `conclusion`.md, only the ones involved |
| Two or more sections | `consistency.md` |
| The project has `GLOSSARY.md` at its root | Read it: a term or symbol that differs from it, or one of its _Avoid_ synonyms, is an issue |
| Rewriting, or the problem is word choice | `word-bank.md` |
| The problem is how things are explained (missing research question, framing, contrast, plain-language explanation, mechanism tests, unfavorable results) | `writing-patterns.md`, and cite the technique number |

## Workflow

**Decide**: whether the user wants suggestions, a rewrite, or a draft (default to suggestions if there is a draft and nothing is stated); which section it is (ask if you cannot tell).

**Suggestion mode**: first judge whether the passage as a whole achieves the purpose of its section, then go through the checklist item by item.

**Rewrite mode**:
1. Check the main line before fixing sentences: the chain of argument in the section file (and consistency.md Section 1 for two or more sections). Breaks are listed as must fix, with the specific questions to ask the author. You may reorder, merge, or split content already in the original.
2. Only change sentences that have problems; when replacing words, name the corresponding category in word-bank.md.
3. After rewriting, actually check the result against ethical boundaries 2 to 5 and principles.md Sections 4 and 5. For method text, also search the result for `shape`, `形狀`, `(Section` and `（第`, and rewrite every hit per method.md Dimensions and Cross-references.

**Draft mode** (the user has no text for this section):
1. Collect material: list what the section needs (from its section file's "Common structure") and map each item to the user's material.
2. Write following the section file's structure and writing-patterns.md.
3. Run the same checks as rewrite mode step 3.

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
以下為 AI 生成，不可直接作為論文內容，特此告知。
| Original sentence | Rewrite | What changed and why |
## Content gaps
## Unmodified sentences
```

Draft mode:

```
以下為 AI 生成，不可直接作為論文內容，特此告知。
## Draft
## Source of each claim (sentence → user's material)
## Content gaps ([TODO] items and questions for the author)
```

When the user only wants a quick look, list only must fix and should fix.

## Notes

- Write explanations in Traditional Chinese; keep the paper's original text and rewritten sentences in their original language.
- The structures in the section files are common practice, not hard rules; if the section achieves its purpose, do not force them.
- When unsure about a field's conventions, say so directly and ask the user to check the submission guidelines.
