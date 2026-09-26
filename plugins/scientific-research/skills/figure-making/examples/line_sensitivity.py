"""Sensitivity curves: data fraction and a hyperparameter per panel, plus a twin-axis panel
for one method scored on two metrics.

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

# Replace with real data. Last method is ours.
METHODS = ["Baseline A", "Baseline B", "Ours"]
COLORS = [ps.BLUES[2], ps.GREENS[2], ps.OURS]
MARKERS = ["s", "^", "o"]  # second cue when two colors are close
METRIC = "Score ↑"
REFERENCE = ("No post-training", 82.1)
FRACTION = {"x": [0.1, 0.25, 0.5, 1.0],
            "y": [[82.8, 83.2, 85.1, 85.7], [84.0, 85.5, 87.1, 87.8], [86.7, 88.2, 89.2, 89.8]]}
OURS_MARK = 1  # dotted line at ours with FRACTION["x"][1]: how much data others need to catch up
BETA = {"x": [0.05, 0.1, 0.2, 0.5],
        "y": [[79.5, 82.8, 81.0, 76.2], [83.2, 84.2, 83.5, 81.0], [86.8, 86.9, 86.5, 85.8]]}
TWIN = {"x": [0.1, 0.5, 1.0, 2.0], "left": ("Metric 1 ↑", [84.5, 86.1, 86.9, 87.2]),
        "right": ("Metric 2 ↑", [49.8, 49.6, 49.5, 48.8])}


def curves(ax, xs, ys, fade=False):
    """Evenly spaced x positions for irregular grids (say so in the caption).
    Geometric grids (1e-5, 1e-4, ...): plot real values with ax.set_xscale("log") instead.
    fade=True when x has a direction (more data, more steps): segments fade in left to right."""
    pos = np.arange(len(xs))
    for y, method, color, marker in zip(ys, METHODS, COLORS, MARKERS):
        if fade:
            ps.fade_line(ax, pos, y, color, label=method, marker=marker)
        else:
            ax.plot(pos, y, color=color, marker=marker, label=method)
    ax.set_xticks(pos)
    return pos


if __name__ == "__main__":
    ps.apply_style()
    fig, axes = plt.subplots(1, 3, figsize=(33, 8))

    ax = axes[0]
    pos = curves(ax, FRACTION["x"], FRACTION["y"], fade=True)
    ax.axhline(REFERENCE[1], label=REFERENCE[0], **ps.REFERENCE)
    ax.hlines(FRACTION["y"][-1][OURS_MARK], pos[0] - 0.1, pos[-1] + 0.1, color=ps.OURS, linestyle=":")
    ax.set_xticklabels([f"{v:.0%}" for v in FRACTION["x"]])
    ax.set_xlabel("Fraction of training data")
    ax.set_ylabel(METRIC)
    ps.pad_ylim(ax, top=0.5)  # legend goes in the empty band, never over data
    ax.legend(loc="upper center", ncols=2)

    ax = axes[1]
    curves(ax, BETA["x"], BETA["y"])
    ax.set_xticklabels([str(v) for v in BETA["x"]])
    ax.set_xlabel(r"Hyperparameter $\beta$")
    ax.set_ylabel(METRIC)
    ps.pad_ylim(ax, top=0.5)
    ax.legend(loc="upper center", ncols=2)

    # Twin axis: same method, two metrics. Left metric faded, right metric solid,
    # each axis label colored like its line so the reader can pair them.
    ax = axes[2]
    pos = np.arange(len(TWIN["x"]))
    (name_l, y_l), (name_r, y_r) = TWIN["left"], TWIN["right"]
    line_l, = ax.plot(pos, y_l, color=ps.OURS, alpha=0.4, marker="o", label=f"{name_l} (left)")
    ax.set_ylabel(name_l, color=ps.OURS, alpha=0.4)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    line_r, = ax2.plot(pos, y_r, color=ps.OURS, marker="o", label=f"{name_r} (right)")
    ax2.set_ylabel(name_r, color=ps.OURS, rotation=270, labelpad=40)
    ax.set_xticks(pos, [str(v) for v in TWIN["x"]])
    ax.set_xlabel(r"Hyperparameter $\lambda$")
    ps.pad_ylim(ax, bottom=0.6)
    ps.pad_ylim(ax2, bottom=0.6)
    ax.legend(handles=[line_l, line_r], loc="lower center")

    print(ps.save(fig, "figures/line_sensitivity"))
