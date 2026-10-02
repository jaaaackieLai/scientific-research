---
name: presentation
description: Use when the user wants slides for a scientific talk (lab meeting, progress report to their professor, proposal, defense, paper presentation) - generating slide text in English plus a spoken Chinese script, or reviewing an existing deck's layout, text amount, or script. Trigger phrases such as "make slides", "presentation", "簡報", "投影片", "講稿", "報告給老師", "meeting 要報告", "這頁字太多", "這頁太空". Not for paper writing (use article-advice) or making plots (use figure-making).
---

# presentation

Produces two things per slide: **slide content in English** (complete sentences) and a **script in spoken Traditional Chinese**, as a PhD student talking to their professor. Layout and structure advice follows Püschel's guide; text amount follows the user's measured 24 pt capacity.

References:
- `references/puschel-guide.md`: layout and structure rules with page numbers into `references/puschel-small-guide-to-giving-presentations.pdf`.
- `references/text-density.md`: how much text fits at 24 pt (measured from `references/font-size-24-layout.png`), length rules, correction log.
- `references/spoken-chinese.md`: written-to-spoken word list, banned fillers, PhD tone.

## Confirm before starting

Ask if missing; if no one can answer, decide and list the decisions on delivery:
- Talk length in minutes, and the occasion (lab meeting, proposal, defense, conference).
- Source material: paper, notes, result files. Take every number from the source; never invent results, citations, or co-authors.
- Which figures already exist.

## Workflow

1. **Outline.** Slides ≤ 2/3 × minutes, counting every slide. Default order: motivation and precise problem statement → background and related work → our method → results → conclusion. Overview slide: once for 10–25 min talks, before each section above 25 min, none under 10 min. Write the outline (one message per slide) and confirm it before writing slides.
2. **Slides.** For each slide, follow the output format below. Check the line budget in `text-density.md`.
3. **Script.** Follow `spoken-chinese.md`. About 200 characters per minute of speaking; per slide that is 200 × minutes / slides.
4. **Check** against the list at the end.

## Slide rules

- Template: section name in the top bar, title 44 pt bold, subtitle 24 pt bold underlined, body 24 pt, bullet spacing 12 pt (sub-bullet 6 pt), gray page number `n / N`.
- Title fits one line (≤ ~50 characters). The subtitle, if used, states the slide's takeaway in one sentence.
- Body: complete sentences, one idea each, one line preferred, two at most. Text-only slides 5–8 lines, never over 10.
- First slide and no two consecutive slides are text-only. Where a picture would explain better (problem setup, pipeline, method, results), specify the figure: what it shows, where it sits (half or full width), and which existing file it comes from, or mark it `TODO: make with figure-making`.
- Left-align everything. Sans-serif (Calibri). Emphasis in desaturated red text; boxes in pastel colors. Math in LaTeX.
- Related work cited on the slide by name: `Author et al. [Venue Year]`. Borrowed figures carry a small gray source line.
- Results slides: one plot or table with the conclusion as the subtitle. Plot rules (axis labels, horizontal y-label, direct labels instead of a legend) are in `puschel-guide.md`; produce plots with figure-making and tables with table-making.
- Conclusion slide repeats the one or two key messages from the talk.

## Output format

Write the deck to a Markdown file in the project (e.g. `slides/<topic>.md`) unless the user names another format.

```markdown
## Slide 3 / 12: <Title>
Section: <Introduction | Method | Results | ...>
Subtitle: <takeaway sentence>
Body:
- <sentence>
  - <sub-sentence>
Figure: <half/full width, right/left; what it shows; source file or TODO>
Lines: 7 / 10

講稿:
<spoken Chinese script>
```

## Checks before delivery

- Slide count ≤ 2/3 × minutes; every slide has one message
- Every slide within its line budget; none under 4 lines without a figure
- No text-only first slide, no two text-only slides in a row
- All numbers and claims traceable to the source material
- Script: no written words from the table, no fillers or stage directions, plots explained as compared / x / y / direction / one point / conclusion
- Co-authors named on the title slide and in the opening line of the script
- If the user corrected text length, a line was added to the log in `text-density.md`
