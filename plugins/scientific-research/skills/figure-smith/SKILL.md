---
name: figure-smith
description: Use when the user wants to make or modify data figures for papers or slides with matplotlib (method comparisons, per-category performance, ablations, sensitivity to hyperparameters or data size, trends over time, multi-panel figures), or asks you to check existing figures and plotting code. Trigger phrases such as "make a plot for me", "make a comparison figure", "how can I improve this figure", "this figure doesn't look professional". Not for interactive or web charts (Plotly, Altair, Bokeh), and not for schematic diagrams such as architecture or flow diagrams.
---

# figure-smith

One figure supports only one claim. First write down the conclusion the reader should draw from it, then choose a template.


## Confirm before starting

If anything is missing, ask first; when there is no one to ask, decide yourself and list what you decided when delivering:
- Which claim this figure supports
- Whether there are standard deviations from multiple runs; whether each metric is higher-is-better or lower-is-better
- Which is the proposed method, and which baseline methods belong to the same family

## Templates

Every file in `examples/` runs as is, with demo data written at the top of the file. Copy the closest template into the user's folder and then modify it:
- Read data from the raw files; do not copy values by hand
- Put plotting code in the project's `figures/src/` and output figures in `figures/` (e.g. `figures/src/bar_grid.py` produces `figures/bar_grid.png`)
- Change `SCRIPTS` at the top of the file to the absolute path of this skill's `scripts/`; derive the path for `save()` from the script's own location (`Path(__file__).resolve().parent.parent / "name"`), without depending on the working directory at run time

| To show | Template |
|---|---|
| Multiple methods' performance across multiple categories | `bar_grid.py` |
| The same set of methods under different conditions (before and after a change, change in results) | `bar_hatch.py` |
| Multi-metric comparison plus ablation | `bar_metrics.py` |
| Cumulative quantities over time and key events (area chart by default; set `AREA = False` when crossings are dense enough to hide data) | `area_trend.py` |
| Sensitivity to hyperparameters or training data size | `line_sensitivity.py` |

When there is no matching template (e.g. heatmaps, training curves, class distributions), adapt the closest template following `style.md`.

All templates import `scripts/pubstyle.py` (font sizes, color constants, `ranked()`, `sci_label()`, `axis_labels()`, `set_sci_axis()`, `patches()`, `legend_panel()`, `label_bars()`, `tight_ylim()`, `line_zorder()`, `fade_line()`, `pad_ylim()`, `is_dark()`, `save()`).

## Files to read

| Situation | Read |
|---|---|
| Every time you plot or review | `references/style.md` |
| Before delivering, or when reviewing someone else's figure | `references/checklist.md` |

## Attribution

Adapted from figures4papers by Chen Liu (https://github.com/ChenLiu-1996/figures4papers),
licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/).
Changes: condensed and rewritten.
