"""Grouped bars with two encodings: color = method, hatch = condition. Legends get their own row.

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

# Replace with real data.
METHODS = ["Baseline A", "Baseline B", "Ours"]
COLORS = [ps.GREENS[2], ps.PURPLES[-2], ps.OURS]
YLABEL = "Probability"
PANELS = {  # panel title -> {condition: one value per method}
    "Correctness ↑": {
        "Before rewriting": [0.23, 0.50, 0.57],
        "After rewriting": [0.33, 0.63, 0.73],
    },
    # "same result" (0.90 / 0.73 / 0.77) would dwarf these; it goes in the caption instead.
    "Change in result": {
        "correct → incorrect ↓": [0.00, 0.07, 0.03],
        "incorrect → correct ↑": [0.10, 0.20, 0.20],
    },
}
# One hatch per condition name ("" = solid). A condition shared by several panels keeps its hatch.
HATCHES = {"Before rewriting": "", "After rewriting": "||", "correct → incorrect ↓": "\\\\",
           "incorrect → correct ↑": "//"}

if __name__ == "__main__":
    ps.apply_style()
    fig, axes = plt.subplots(2, len(PANELS), figsize=(12 * len(PANELS), 10),
                             gridspec_kw={"height_ratios": [2, 1]})
    x = np.arange(len(METHODS))

    for ax, (title, groups) in zip(axes[0], PANELS.items()):
        width = 0.8 / len(groups)
        for k, (cond, values) in enumerate(groups.items()):
            offset = (k - (len(groups) - 1) / 2) * width * 1.1
            # Black edges because hatches need an outline; dark fills get a white hatch.
            bars = ax.bar(x + offset, values, width=width, color=COLORS, edgecolor="black",
                          linewidth=2, hatch=HATCHES[cond])
            for bar, color in zip(bars, COLORS):
                if ps.is_dark(color):
                    bar.set_hatchcolor("white")
        ax.set_title(title)
        ax.set_ylabel(YLABEL)
        # Each panel scales to its own data. If one condition dwarfs the others and the claim rests
        # on the small ones, move the large condition to its own panel or to the caption.
        ax.set_ylim(0, max(max(v) for v in groups.values()) * 1.15)
        ax.set_xticks([])

    conditions = list(dict.fromkeys(c for groups in PANELS.values() for c in groups))
    ps.legend_panel(axes[1][0], ps.patches(COLORS, edgecolor="black"), METHODS)
    ps.legend_panel(axes[1][1], ps.patches(["white"] * len(conditions),
                                           [HATCHES[c] for c in conditions], edgecolor="black"),
                    conditions)
    print(ps.save(fig, "figures/bar_hatch"))
