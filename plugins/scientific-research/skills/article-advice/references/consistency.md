# Cross-section consistency

Use when the user provides two or more sections or the whole paper. For each issue, mark the two locations involved (e.g., abstract sentence 5 vs. Table 2) and quote both.

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

List every claim in the abstract and introduction:

```
Claim: ... | Evidence: (which section, which table, which number) | Status: supported / needs evidence
```

Mark "supported" only when a concrete number or result is found; every "needs evidence" is must fix.

## 3. Numbers

- Every number in the abstract, introduction, and conclusion is exactly the same as in the tables (including decimal places).
- Common errors: the abstract says a 5% improvement but the table shows 3.8 percentage points; or the number comes from an old version of the experiments.
- For "improves by X%", make clear whether it is a relative improvement or absolute percentage points.

## 4. Names

- Module names are the same in three places: the introduction overview, the method subsection titles, and the ablation row names.
- The verbs and nouns of the core mechanism, datasets, metrics, baseline methods, and adjectives are consistent throughout.
- Keywords in the method name (Adaptive, Sparse) are explained in the body text as to what operation they denote.
- The same name does not refer to different settings (e.g., Ours in one table is the full version, in another the simplified version).
- List all key terms (method and variants, categories, model roles, metrics) and confirm what each refers to section by section. The ones most likely to silently change meaning are generic words: target, source, baseline, original.

## 5. Unfavorable results

- In every table and figure, places where the proposed method does not win, the gap is smaller than the standard deviation, or it holds only in some settings, are all mentioned in the body text.
- When the body text says "leads across the board", check against the tables.
- This information is already in the tables; write it directly into the body text when rewriting. It does not count as a content gap.

## 6. Consistent statements

- Methods criticized in the introduction are described and criticized consistently in related work.
- Limitations in the conclusion do not contradict claims in the introduction or experiments.
- A concrete example from the introduction reads better if it reappears in the method or experiments; you may suggest this, but it is not an error.
