# Cross-section consistency

For each issue, mark the two locations involved (e.g., abstract sentence 5 vs. Table 2) and quote both.

## 1. Chain of argument (a break is must fix)

| Check | What a break looks like |
|---|---|
| Limitation → challenge | The challenge is a difficulty of this paper's own method, not of the problem the limitation exposes |
| Challenge → key idea | The challenge is about scalability, but the key idea only addresses accuracy |
| Challenge ↔ module | A module with no challenge, or a challenge with no module |
| Module → contribution | The contributions mention theoretical analysis, but the paper has no theory subsection |
| Contribution → experiment | A contribution claims better efficiency, but the experiments do not measure time |
| Module → ablation | Three modules, but the ablation only removes two |

## 2. Claims and evidence

List every claim in the abstract and introduction in the "Claims vs. evidence" format of SKILL.md, giving the section, table, and number as evidence. Mark "supported" only when a concrete number or result is found; every "needs evidence" is must fix. Each claim needs at least one piece of its evidence in the main text; evidence found only in the appendix is should fix.

## 3. Numbers

- Every number in the abstract, introduction, and conclusion is exactly the same as in the tables (including decimal places).
- Common errors: the abstract says a 5% improvement but the table shows 3.8 percentage points; or the number comes from an old version of the experiments.
- The same method on the same task with different numbers in two tables: the setting difference is explained.
- When the method has the best average but not the best value in any single column, the text says so explicitly and explains why the average wins (writing-patterns.md 4.7).

## 4. Names

- Keywords in the method name (Adaptive, Sparse) are explained in the body text as to what operation they denote.
- List all key terms (method and variants, categories, model roles, metrics) and confirm what each refers to section by section (e.g., Ours is the full version in one table and the simplified version in another). The ones most likely to silently change meaning are generic words: target, source, baseline, original.
- If the project has `GLOSSARY.md`, start that list from its terms and `## Notation` table.
- Components keep the same names and order (e.g., DO then PH) in the abstract, introduction overview and contributions, method subsection titles, table and ablation rows, and conclusion.
- When the letters of an acronym method name are not obvious from its expansion, they are marked at first mention (a **syn**chronization **tag**).

## 5. Consistent statements

- Methods criticized in the introduction are described and criticized consistently in related work.
- Limitations in the conclusion do not contradict claims in the introduction or experiments; future work does not contradict limitations (e.g., "should scale better" while limitations say more data did not help).
- The same result keeps the same verb strength in the abstract, figure captions, and conclusion (not mitigates in a caption and overcomes in the conclusion).

## 6. References

- Each citation supports the sentence it is attached to: spot-check the cited title against the claim (a "transformer for classification" citation that is about electrical power transformers; Attention Is All You Need cited for ViT; Torch7 cited for PyTorch).
- Names in "X et al." are surnames, not given names.
- Errors copied from a shared lab .bib propagate across papers; check every reused entry.
