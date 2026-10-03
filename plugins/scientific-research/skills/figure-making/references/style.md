# Style rules

`scripts/pubstyle.py` already implements these rules; check against this file when writing your own code or reviewing someone else's figure.

## Principles

A figure should make the data understandable at a glance, and look good enough that readers want to look at it. Three things determine the impression:
1. **The proposed method is the only saturated color in the whole figure**; everything else uses light colors, so the reader's eye naturally lands on the proposed method.
2. **Gaps must be visible**: tighten the y axis to the range where the data lies, so bars are not squeezed to the same height.
3. **Text in the figure keeps only the information the claim needs**: verifiable gaps, proportions, baselines, and events may be labeled directly on the figure; method details and secondary explanations go in the caption.

## Font sizes and canvas

| Figure title | Axis title | Ticks, legend | Value labels, event annotations |
|---|---|---|---|
| 36 | 32 | 28 | 24 |

Each subplot is 7 to 12 inches wide and 6 to 8 inches tall; a single subplot with a time axis or many categories can be widened to 28 inches. When placed in the paper, scale the whole figure to column width. If labels are too crowded, widen the canvas; do not shrink the font size.

Regular line width is 5 pt and markers are 10 pt. Gradient lines from `fade_line()` stay at 4 pt with 16 pt markers; area chart outlines and reference dashed lines are 4 pt.

## Colors

| Role | `pubstyle` constant |
|---|---|
| Proposed method | `OURS` (`#b62b2e`), the only deep red in the whole figure |
| Ablation variants of the proposed method | `REDS`, lighter the more components are removed, deepening toward the full method |
| Baseline methods in the same family | `BLUES`, `GREENS`, `YELLOWS`, `PURPLES`; all arrays go from dark to light (index 0 darkest), small or weak ones light, large or strong ones dark |
| Unrelated baseline methods | Take one color each from `PASTELS` in order |
| A group of baseline methods ranked by performance | `ranked(n)`: one hue from dark to light |
| Category to emphasize when there is no proposed method | `BLUES[2]`; the rest use `GRAY` |
| Reference baseline line | `REFERENCE` (black dashed line at 30% opacity) |
| Error band of a mean curve | Same-color `fill_between`, ±1 standard deviation, `BAND_ALPHA` |
| Area chart | `AREA_BLUE`, `AREA_RED`, `AREA_GREEN`: light fill with a dark outline; when drawn as lines, follow the method colors above |

- All palettes go from dark to light: `BLUES = [#163973, #23629e, #3290cb, #6dbfe2, #b9ebf6]`, `GREENS = [#014e31, #1f7b42, #429a4d, #8dcb83, #c5efb9]`, `YELLOWS = [#995313, #c67d1c, #f0a928, #ffc95c, #ffe091]`, `PURPLES = [#5d338c, #8d56b7, #b885d3, #d3a8e3, #edcef4]`.
- The proposed method's red scale is the full method `OURS = #b62b2e`, followed by the lighter ablation shades `REDS = [#e85941, #f58667, #ffbfa4, #ffe3d5]`.
- When the proposed method is present, baseline methods do not use red; prefer light or mid tones of blue, green, yellow, and purple; the red scale is only for the proposed method and its ablations.
- When a family has more than 5 members, use `ranked(n, dark=darkest color of the family, light=lightest color of the family)` to generate n steps of the same hue, dark to light like the arrays.
- Within the same paper, the same method uses the same color in every figure.
- When several lines from the same family appear together, use different markers (`o`, `s`, `^`) and line styles (solid, dashed, dash-dot) in addition to color; do not rely on color shades alone.
- Hatching and text on dark fills are white (`is_dark()`).
- Heatmaps use `Reds` (positive values only) or `RdBu` (both positive and negative), with white lines between cells and a value in each cell; cells of a different nature (e.g. the diagonal of a confusion matrix) use `GRAY`.

## Layout

- y axis:
  - Bar charts comparing methods: when the claim is about ranking or gaps, use `tight_ylim()` to tighten to the data range and note in the caption that the y axis does not start at 0; fix it to 0 to 1 only when the claim is about absolute probabilities or proportions.
  - When two or more subplots are meant for readers to compare trends or levels, the y axes use the same range; split into subplots only when a single figure would be too cluttered. When each subplot's claim is compared only within that subplot, each uses its own range.
  - When line values span more than one order of magnitude, use a log scale and note (log) in the axis title. Bar charts do not use log scales.
  - When values in the same subplot differ greatly in size and the claim depends on the small values, move the large group into the caption or into another subplot.
- x axis (hyperparameters, data size): geometric sequences (1e-5, 1e-4, …) use a log axis with actual values; irregular grids are spaced evenly, noted in the caption. Scientific notation is applied uniformly per axis and cannot switch partway along the same axis: if any nonzero value satisfies `abs(x) < 0.01`, or all nonzero values satisfy `abs(x) >= 10^3`, use `axis_labels()` to show all ticks in scientific notation; otherwise keep all as regular numbers. So learning-rate axes consistently use scientific notation, and batch-size axes like `[64, 256, 1024, 4096]` consistently use integers. A coefficient of 1 is still written as `1 × 10^n`, not shortened to `10^n`. For actual continuous scientific-notation axes, use `set_sci_axis()`.
- Text in the figure:
  - With 10 bars or fewer, you may label values with `label_bars()`; label gaps only when the proposed method's winning margin is the point of the claim. Use only one main type of numeric label per figure.
  - Differences, cumulative values, proportions, and lead times that can be recomputed directly from the input data may be labeled; do not impute values or combine quantities with no scientific meaning.
  - If information such as the error bar definition or reference values is necessary for reading the figure, it may go in a separate legend area; the full definition still goes in the caption.
  - Event annotations label only the events the claim needs; when dense, specify each label's coordinates individually.
- Legend: when method names are in the legend, the x axis has no tick labels. The legend does not cover data: put it in a separate subplot (`legend_panel()`), in blank space at the top (`pad_ylim()`), or in a full column on the right.
- Lines:
  - Keep the proposed method's line and markers above all other data layers at crossings and overlapping points. Set explicit `zorder`: fills/error bands and reference lines `1`, baseline/ablation lines and markers `2`, proposed-method lines and markers `3`. Use `line_zorder(color)` for method lines; `fade_line()` applies it to both segments and markers. This priority is independent of plotting order; legends and annotations remain readable above the data.
  - When the x axis has a direction (training steps, data size), you may use `fade_line()`: segments go from light to dark, with enlarged dots.
- When cumulative quantities, totals, and overtaking events are the claim, overlapping area charts may be used; draw all fills first, then all outlines, so crossings stay visible. Switch to lines only when crossings are so dense that fills interfere with reading values.
- Add black borders to bars only when they are distinguished by hatching alone. When two dimensions must be distinguished at once, color and hatching each handle one.
- Add ↑ or ↓ after metric names to mark direction.
- Do not put numbers on the figure that cannot be verified from the input data, and do not arbitrarily average metrics of different natures; differences, cumulative values, and proportions may be derived from the raw columns.
- Font sizes, line widths, and color mappings are exactly consistent across a row of subplots.

## Output

- `save(fig, path)` outputs PNG only (300 dpi), not PDF.
- Figures are saved to the project's `figures/`, and the code that produces them goes in `figures/src/`.
- When running in an environment without a display, call `matplotlib.use("Agg")` before importing `pyplot` (the templates already do this).
