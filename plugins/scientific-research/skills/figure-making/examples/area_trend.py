"""Cumulative trend over time with arrows marking events, one panel per data split.
AREA=True (default) draws every fill first and every dark outline second, so overtaking remains
visible when series cross. Set AREA=False only when frequent crossings make the fills obscure data.
SHARE_Y=True when the reader compares trends across panels; False when each panel's claim stands alone.

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

# Replace with real data: monthly counts per series, starting at START.
AREA = True
SHARE_Y = True
START, N_MONTHS = (2022, 11), 33
rng = np.random.default_rng(0)
COLORS = {"Application": ps.AREA_BLUE, "Method": ps.AREA_GREEN}  # fixed per series name
PANELS = [
    {
        "ylabel": "Cumulative count\n(Text)",
        "series": {"Application": rng.poisson(3.0, N_MONTHS), "Method": rng.poisson(0.4, N_MONTHS)},
        "hatches": None,
        # (month, label, series the arrow points at, level): raise level to lift a colliding label.
        "events": [("2022-11", "Model A", "Application", 0), ("2023-03", "Model B", "Application", 1),
                   ("2023-12", "Model C", "Application", 0), ("2024-04", "Model D", "Application", 0),
                   ("2025-06", "Model E", "Application", 0)],
    },
    {
        "ylabel": "Cumulative count\n(Multimodal)",
        "series": {"Application": rng.poisson(0.8, N_MONTHS), "Method": rng.poisson(0.2, N_MONTHS)},
        "hatches": {"Application": "\\\\\\", "Method": "///"},
        "events": [("2023-02", "Model F", "Application", 0), ("2023-10", "Model G", "Application", 1),
                   ("2024-12", "Model H", "Method", 0)],
    },
]


def month_labels(year, month, n):
    return [f"{year + (month - 1 + i) // 12}-{(month - 1 + i) % 12 + 1:02d}" for i in range(n)]


def mark_events(ax, months, curves, events, step=0.1):
    """Arrow from each label down to its series' curve; label height grows with `level`."""
    index = {m: i for i, m in enumerate(months)}
    y0, y1 = ax.get_ylim()
    for month, label, series, level in events:
        i = index[month]
        y = curves[series][i]
        lift = (1 + 0.8 * level) * step * (y1 - y0)
        ax.annotate(label, xy=(i, y), xytext=(i, y + lift), ha="center", va="bottom",
                    fontsize=ps.FONT["annot"],
                    arrowprops={"arrowstyle": "-|>", "lw": 2, "color": "black", "mutation_scale": 25})


if __name__ == "__main__":
    ps.apply_style()
    months = month_labels(*START, N_MONTHS)
    x = np.arange(N_MONTHS)
    fig, axes = plt.subplots(len(PANELS), 1, figsize=(28, 8 * len(PANELS)), sharey=SHARE_Y)
    all_curves = [{name: np.cumsum(c) for name, c in p["series"].items()} for p in PANELS]
    shared_top = max(y.max() for curves in all_curves for y in curves.values())

    for ax, panel, curves in zip(axes, PANELS, all_curves):
        hatches = panel["hatches"] or {}
        # Fills first (largest behind), outlines last so no fill hides an outline.
        order = sorted(curves, key=lambda name: -curves[name][-1])
        if AREA:
            for name in order:
                fill, _ = COLORS[name]
                hatch = hatches.get(name)
                ax.fill_between(x, 0, curves[name], facecolor=fill, edgecolor="black" if hatch else fill,
                                hatch=hatch, linewidth=0, label=name)
        for name in order:
            ax.plot(x, curves[name], color=COLORS[name][1], linewidth=4,
                    label=None if AREA else name)
        top = shared_top if SHARE_Y else max(y.max() for y in curves.values())
        ax.set_ylim(0, top * 1.35)
        ax.set_xlim(-1.5, N_MONTHS - 0.5)  # room for a label on the first month
        ax.set_xticks(x[2::6], [months[i] for i in x[2::6]])
        ax.set_xlabel("Month")
        ax.set_ylabel(panel["ylabel"])
        ax.legend(loc="upper left")
        mark_events(ax, months, curves, panel["events"])

    print(ps.save(fig, "figures/area_trend"))
