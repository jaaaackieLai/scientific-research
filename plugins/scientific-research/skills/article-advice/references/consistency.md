# Cross-section consistency

For each issue, mark the two locations involved (e.g., abstract sentence 5 vs. Table 2) and quote both.

## 1. Chain of argument (a break is must fix)

| Check | What a break looks like |
|---|---|
| Limitation → key idea | The limitation is about scalability, but the idea only addresses accuracy |
| Key idea → challenge | The challenge is borrowed from another paper, not one encountered when implementing this paper's idea |
| Challenge ↔ module | A module with no challenge, or a challenge with no module |
| Module → contribution | The contributions mention theoretical analysis, but the paper has no theory subsection |
| Contribution → experiment | A contribution claims better efficiency, but the experiments do not measure time |
| Module → ablation | Three modules, but the ablation only removes two |

## 2. Claims and evidence

List every claim in the abstract and introduction in the "Claims vs. evidence" format of SKILL.md, giving the section, table, and number as evidence. Mark "supported" only when a concrete number or result is found; every "needs evidence" is must fix.

## 3. Numbers

- Every number in the abstract, introduction, and conclusion is exactly the same as in the tables (including decimal places).
- Common errors: the abstract says a 5% improvement but the table shows 3.8 percentage points; or the number comes from an old version of the experiments.
- The same method on the same task with different numbers in two tables: the setting difference is explained.

## 4. Names

- Module names are the same in three places: the introduction overview, the method subsection titles, and the ablation row names.
- Keywords in the method name (Adaptive, Sparse) are explained in the body text as to what operation they denote.
- List all key terms (method and variants, categories, model roles, metrics) and confirm what each refers to section by section (e.g., Ours is the full version in one table and the simplified version in another). The ones most likely to silently change meaning are generic words: target, source, baseline, original.
- If the project has `GLOSSARY.md`, start that list from its terms and `## Notation` table.

## 5. Consistent statements

- Methods criticized in the introduction are described and criticized consistently in related work.
- Limitations in the conclusion do not contradict claims in the introduction or experiments; future work does not contradict limitations (e.g., "should scale better" while limitations say more data did not help).
- The same result keeps the same verb strength in the abstract, figure captions, and conclusion (not mitigates in a caption and overcomes in the conclusion).
