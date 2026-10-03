"""Illustrative sparsity curves adapted from figure-making/line_sensitivity.py.

Synthetic data only: these are not measured results or digitized image values.
Style adapted from figures4papers by Chen Liu, CC BY-NC 4.0.
"""
import csv
import sys
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(
    r"E:\Projects\scientific-research\plugins\scientific-research\skills\figure-making\scripts"
)
sys.path.insert(0, str(SCRIPTS))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import pubstyle as ps

FIGURES = Path(__file__).resolve().parent.parent
DATA = FIGURES / "data" / "sparsity_sample.csv"
METHODS = ["TiltDiff", "SANE_sub"]  # Demo assumption: TiltDiff is the proposed method.
PANELS = [
    ("first", "(a) First convolutional layer"),
    ("all", "(b) All convolutional layers"),
]


def make_demo_data():
    """Create a reproducible input CSV once; preserve later user edits."""
    x = np.arange(11, dtype=float)
    sigmoid = lambda center, slope: 1 / (1 + np.exp(-slope * (x - center)))
    tilt_first = -1.1 * x - 2.5 * (1 - np.exp(-x / 1.5))
    sane_first = (
        -0.55 * x
        - 3.0 * sigmoid(2.6, 3.0)
        - 4.0 * sigmoid(4.7, 2.6)
        - 5.8 * (x / 10) ** 1.7
    )
    sane_first -= sane_first[0]
    tilt_all = -1.3 * x - 6.0 * (1 - np.exp(-x / 2.0))
    extra_drop = 3.0 * sigmoid(2.25, 3.0)
    sane_all = sane_first - 0.2 * x - (extra_drop - extra_drop[0])
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with DATA.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["panel", "method", "sparsity_pct", "relative_accuracy_change_pct"])
        for panel, curves in [("first", [tilt_first, sane_first]), ("all", [tilt_all, sane_all])]:
            for method, curve in zip(METHODS, curves):
                writer.writerows((panel, method, int(sparsity), f"{change:.6f}")
                                 for sparsity, change in zip(x, curve))


def main():
    if not DATA.exists():
        make_demo_data()
    with DATA.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    ps.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(24, 9))
    for ax, (panel, subtitle) in zip(axes, PANELS):
        for method, color, marker, linestyle, label in [
            ("TiltDiff", ps.OURS, "o", "-", "TiltDiff"),
            ("SANE_sub", ps.BLUES[-2], "s", "--", r"SANE$_{sub}$"),
        ]:
            data = sorted(
                (row for row in rows if row["panel"] == panel and row["method"] == method),
                key=lambda row: float(row["sparsity_pct"]),
            )
            x = np.array([float(row["sparsity_pct"]) for row in data])
            y = np.array([float(row["relative_accuracy_change_pct"]) for row in data])
            ax.plot(x, y, color=color, marker=marker, linestyle=linestyle, label=label,
                    zorder=ps.line_zorder(color))
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-26, 1)
        ax.set_xticks(np.arange(11))
        ax.set_yticks(np.arange(-25, 1, 5))
        ax.set_xlabel("Sparsity (%)")
        ax.set_ylabel("Relative accuracy\nchange (%) \u2191")
        ax.legend(loc="upper right", handlelength=2.5)
        ax.text(0.5, -0.25, subtitle, transform=ax.transAxes,
                ha="center", va="top", fontsize=ps.FONT["title"])
    # Put the demo notice outside the data area, under the right panel.
    axes[1].text(1, -0.36, "Illustrative data", transform=axes[1].transAxes,
                 ha="right", va="top", fontsize=ps.FONT["annot"], color="#666666")
    # Pre-layout once so save() can refine axes-relative footer spacing.
    fig.tight_layout(pad=2)
    for path in ps.save(fig, FIGURES / "sparsity_sample"):
        print(path)
    plt.close(fig)


if __name__ == "__main__":
    main()
