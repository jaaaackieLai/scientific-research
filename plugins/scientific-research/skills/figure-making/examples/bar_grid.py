"""Per-category bars: one panel per category, legend in a spare grid cell.

Adapted from figures4papers by Chen Liu (https://github.com/ChenLiu-1996/figures4papers),
licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/).
Changes: condensed and rewritten.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__
# Copied elsewhere? Replace with the absolute path of the skill's scripts/ folder.
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import pubstyle as ps

# Replace with real data. Soft hue = model family, shade = model size (light = small);
# ours is the only saturated color.
METHODS = ["Family A 1B", "Family A 7B", "Family A 70B", "Family B chat", "Family B reasoner", "Ours"]
COLORS = [ps.GREENS[0], ps.GREENS[1], ps.GREENS[2], ps.PURPLES[0], ps.PURPLES[1], ps.OURS]
YLABEL = "Accuracy ↑"
CATEGORIES = {  # category -> one value per method
    "Algebra": [0.20, 0.54, 0.57, 0.66, 0.75, 0.82],
    "Geometry": [0.13, 0.42, 0.38, 0.29, 0.38, 0.67],
    "Logic": [0.03, 0.41, 0.45, 0.52, 0.62, 0.76],
    "Pattern": [0.00, 0.21, 0.18, 0.36, 0.64, 0.75],
    "Counting": [0.25, 0.42, 0.42, 0.63, 0.67, 0.75],
    "Number": [0.44, 0.56, 0.53, 0.68, 0.82, 0.85],
    "Language": [0.00, 0.07, 0.07, 0.47, 0.40, 0.80],
}
TIGHT_PER_PANEL = True  # ranking/gap claim; set False when absolute 0-1 level is the claim
NROWS, NCOLS = 2, 4
LEGEND_CELL = NCOLS - 1  # top-right cell holds the legend

if __name__ == "__main__":
    ps.apply_style()
    fig, axes = plt.subplots(NROWS, NCOLS, figsize=(9 * NCOLS, 6 * NROWS))
    axes = axes.ravel()
    data_axes = [ax for i, ax in enumerate(axes) if i != LEGEND_CELL]

    for ax, (name, values) in zip(data_axes, CATEGORIES.items()):
        ax.bar(np.arange(len(METHODS)), values, color=COLORS)
        ax.set_title(name)
        ax.set_ylabel(YLABEL)
        if TIGHT_PER_PANEL:
            ps.tight_ylim(ax, values, pad=0.3)  # caption notes that axes do not start at 0
        else:
            ax.set_ylim(0, 1)
        ax.set_xticks([])  # method names live in the legend
    for ax in data_axes[len(CATEGORIES):]:
        ax.set_axis_off()

    ps.legend_panel(axes[LEGEND_CELL], ps.patches(COLORS), METHODS)
    print(ps.save(fig, "figures/bar_grid"))
