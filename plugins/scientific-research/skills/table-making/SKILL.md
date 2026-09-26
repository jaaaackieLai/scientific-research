---
name: table-making
description: Use when the user wants to make or modify paper tables in LaTeX (main result comparisons, ablations, tables with multiple datasets or metrics), or asks you to check existing tables. Trigger phrases such as "make a table for me", "organize the results into a table", "how can I improve this table", "ablation table", "this table doesn't look professional". Not for Word, Excel, or Markdown tables.
---

# table-making

One table answers only one question (e.g. "is the proposed method best on every metric"). First decide which two directions the reader will compare (row vs. row, column vs. column), then lay it out.

## Confirm before starting

If anything is missing, ask first; when there is no one to ask, decide yourself and list what you decided when delivering:
- Whether each metric is higher-is-better or lower-is-better (determines where bold and underline go)
- Whether there are standard deviations from multiple runs
- Which row is the proposed method

## Templates

All templates use `booktabs` three rules, caption on top, `\resizebox` to scale to column width, and `mean $\pm$ std`. Copy and then change the content; read values from the raw result files, do not copy them by hand.

Save output tables as `.tex` files in the project's `tables/` folder (e.g. `tables/main_results.tex`), and include them in the paper with `\input{tables/...}`.

| Template | Difference |
|---|---|
| `scripts/table_template.tex` | **Use by default**. |
| `scripts/ablation_template.tex` | Ablation. Same layout as above; module columns use `\checkmark`, and upper grouped headers (Components / Metrics) are separated with `\cmidrule` instead of vertical lines |

Required packages: `booktabs`, `graphicx` (`\resizebox`), `amssymb` (`\checkmark`), `multirow` (when there are merged rows).

## Row and column arrangement

- **Metrics always go on the top horizontal axis**: metrics such as ACC and F1 are columns and methods are rows, so the reader compares the same metric vertically. With multiple datasets, use grouped headers (datasets on the upper level, metrics on the lower level); do not move metrics to rows.
- **The proposed method always goes in the last row**; in ablations the full model is the proposed method, and also goes in the last row.

## Layout rules (Püschel, *Small Guide to Making Nice Tables*)

1. **No vertical lines**.
2. **No boxed cells**: use only three horizontal rules, `\toprule` (table top), `\midrule` (below the header), `\bottomrule` (table bottom).
3. **No double rules**, no `\hline`; always use booktabs commands.
4. **Increase row spacing**: `\renewcommand{\arraystretch}{1.2}` (or 1.3), placed after `\centering`.
5. **When unsure, align left**: text columns align left (`l`); numeric columns center or right, with consistent decimal places within a column.
6. **The first column also needs a header**; do not leave it blank.
7. **Remove left and right edge padding**: `\begin{tabular}{@{}l...@{}}`.
8. **Grouped headers**: upper level uses `\multicolumn{n}{c}{...}`, followed by `\cmidrule(lr){a-b}` drawn only under that group; groups can be separated by an empty column (`\phantom{abc}`).
9. **Grouped rows**: the group name gets its own row (e.g. `\textit{CNN-based}`); use `\midrule` or `\addlinespace` between groups, do not add a rule to every row.
10. **Caption above the table**, with units when needed; supplementary notes go in footnotes below the table, not stuffed into cells.
11. When math symbols are needed, use the default roman font; do not switch to sans serif.

## Highlighting rules

- **Best**: `\textbf{}`; **second best**: `\underline{}`. Compare each column (each metric, each dataset) separately, according to that metric's direction.
- With standard deviations, mark the whole cell: `\textbf{0.694 $\pm$ 0.001}`.
- When tied for best, bold all of them, and do not mark a second best in that case.
- **Ablations**: one column per module, `\checkmark` if used, blank if not; the full model goes in the last row. See `scripts/ablation_template.tex`.

## Checks before delivery

- Metrics on the top horizontal axis, proposed method in the last row
- No extra vertical lines, `\hline`, or double rules
- Bold and underline in each column follow that metric's direction, with only one best (unless tied)
- Consistent decimal places within a column, with spaces around `$\pm$`
- `\caption` comes before `\label`, and `\label` starts with `tab:`
- Table files go in `tables/`
- Only prepare the tables; do not compile
