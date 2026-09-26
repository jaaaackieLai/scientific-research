"""Comparison + ablation across metrics: one panel per metric in a row, error bars, legend panel last.

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

# Replace with real data. Baselines in soft non-red hues; ablated variants of ours in REDS,
# lighter = more components removed, so the reds build up toward the full method (OURS).
METHODS = ["Baseline A", "Baseline B", "Baseline C",
           "Ours (w/o X + Y)", "Ours (w/o Y)", "Ours"]
COLORS = [ps.GREENS[1], ps.GREENS[2], ps.PURPLES[1], ps.REDS[0], ps.REDS[1], ps.OURS]
METRICS = {  # metric (with direction arrow) -> (mean per method, std per method)
    "RMSE ↓": ([0.94, 1.05, 0.99, 0.89, 0.75, 0.62], [0.08, 0.09, 0.09, 0.07, 0.06, 0.05]),
    "MAE ↓": ([0.75, 0.85, 0.78, 0.70, 0.59, 0.48], [0.07, 0.08, 0.07, 0.06, 0.05, 0.04]),
    "PCC ↑": ([0.53, 0.49, 0.55, 0.58, 0.65, 0.72], [0.04, 0.02, 0.01, 0.03, 0.02, 0.02]),
    "SCC ↑": ([0.50, 0.47, 0.52, 0.55, 0.68, 0.70], [0.03, 0.02, 0.03, 0.03, 0.03, 0.01]),
}

if __name__ == "__main__":
    ps.apply_style()
    ncols = len(METRICS) + 1
    fig, axes = plt.subplots(1, ncols, figsize=(7 * ncols, 7))
    x = np.arange(len(METHODS))

    for ax, (metric, (mean, std)) in zip(axes, METRICS.items()):
        # Error bars = +-1 std, say so in the caption.
        ax.bar(x, mean, yerr=std, color=COLORS, capsize=8,
               error_kw={"elinewidth": 2, "capthick": 2})
        ps.tight_ylim(ax, mean, std)  # zoom onto the data; caption notes the axis does not start at 0
        ax.set_ylabel(metric)
        ax.set_xticks([])

    ps.legend_panel(axes[-1], ps.patches(COLORS), METHODS)
    print(ps.save(fig, "figures/bar_metrics"))
