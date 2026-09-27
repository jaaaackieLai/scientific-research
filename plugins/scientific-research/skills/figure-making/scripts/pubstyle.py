"""Shared style for publication figures (matplotlib).

Adapted from figures4papers by Chen Liu (https://github.com/ChenLiu-1996/figures4papers),
licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/).
Changes: condensed and rewritten.
"""
from pathlib import Path
import math

import matplotlib as mpl
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, to_hex, to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

# Font sizes in pt. Sized for panels of about 7-12 x 6-8 inches.
FONT = {"title": 36, "label": 32, "tick": 28, "legend": 28, "annot": 24}

# Approved family palettes. Arrays are dark -> light: index 0 is the strongest shade, -1 the softest.
# OURS is the darkest red; REDS contains its four lighter ablation shades.
OURS = "#b62b2e"
BLUES = ["#163973", "#23629e", "#3290cb", "#6dbfe2", "#b9ebf6"]
GREENS = ["#014e31", "#1f7b42", "#429a4d", "#8dcb83", "#c5efb9"]
YELLOWS = ["#995313", "#c67d1c", "#f0a928", "#ffc95c", "#ffe091"]
REDS = ["#e85941", "#f58667", "#ffbfa4", "#ffe3d5"]
PURPLES = ["#5d338c", "#8d56b7", "#b885d3", "#d3a8e3", "#edcef4"]
YELLOW = YELLOWS[-1]  # backward-compatible single-family color
GRAY = "#CFCECE"
# Independent baselines: soft shades from the approved families, plus neutral gray.
PASTELS = [GRAY, YELLOWS[-1], PURPLES[-1], GREENS[-1], BLUES[-1],
           YELLOWS[-2], PURPLES[-2], GREENS[-2], BLUES[-2], YELLOWS[-3]]
# (fill, outline) pairs for area charts: lightest fill + darkest outline.
AREA_BLUE = (BLUES[-1], BLUES[0])
AREA_RED = (REDS[-1], OURS)
AREA_GREEN = (GREENS[-1], GREENS[0])
# Horizontal reference line, e.g. "SFT only" or "random policy".
REFERENCE = {"color": "black", "alpha": 0.3, "linewidth": 4, "linestyle": "--"}
# Uncertainty band around a mean curve (+-1 std).
BAND_ALPHA = 0.2


def apply_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": FONT["tick"],
        "axes.titlesize": FONT["title"],
        "axes.titlepad": 24,
        "axes.labelsize": FONT["label"],
        "axes.labelpad": 12,
        "xtick.labelsize": FONT["tick"],
        "ytick.labelsize": FONT["tick"],
        "legend.fontsize": FONT["legend"],
        "legend.frameon": False,
        "axes.linewidth": 3,
        "xtick.major.width": 2,
        "ytick.major.width": 2,
        "xtick.major.size": 8,
        "ytick.major.size": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "lines.linewidth": 5,
        "lines.markersize": 10,
        "hatch.linewidth": 1.5,
    })


def sci_label(value):
    """Format one tick in normalized scientific notation with an explicit coefficient."""
    value = float(value)
    if value == 0:
        return "0"
    magnitude = abs(value)
    exponent = math.floor(math.log10(magnitude))
    coefficient = value / (10 ** exponent)
    if math.isclose(coefficient, round(coefficient), rel_tol=0, abs_tol=1e-12):
        coefficient = round(coefficient)
    coefficient = float(f"{coefficient:.4g}")
    if abs(coefficient) >= 10:
        coefficient /= 10
        exponent += 1
    return rf"${coefficient:g}\times 10^{{{exponent}}}$"


def axis_labels(values):
    """Format all values on one axis consistently, never switching notation mid-axis."""
    values = [float(value) for value in values]
    magnitudes = [abs(value) for value in values if value != 0]
    use_science = any(value < 0.01 for value in magnitudes)
    use_science = use_science or bool(magnitudes) and all(value >= 1e3 for value in magnitudes)
    return [sci_label(value) if use_science and value != 0 else f"{value:g}" for value in values]


def set_sci_axis(ax, axis="x", minor=False):
    """Apply ``sci_label`` to a numeric x or y axis; optionally include minor ticks."""
    axis_obj = ax.xaxis if axis == "x" else ax.yaxis
    formatter = FuncFormatter(lambda value, _position: sci_label(value))
    axis_obj.set_major_formatter(formatter)
    if minor:
        axis_obj.set_minor_formatter(formatter)


def ranked(n, dark=BLUES[0], light=BLUES[-1]):
    """n soft shades of one hue, dark -> light, for baselines listed best to worst."""
    if n == 1:
        return [dark]
    cmap = LinearSegmentedColormap.from_list("ranked", [dark, light])
    return [to_hex(cmap(i / (n - 1))) for i in range(n)]


def is_dark(color):
    """True for fills that need white text or white hatches."""
    r, g, b = to_rgb(color)
    return 0.299 * r + 0.587 * g + 0.114 * b < 0.5


def patches(colors, hatches=None, edgecolor=None):
    """Legend handles for bars: colored (and optionally hatched) boxes."""
    hatches = hatches or [""] * len(colors)
    return [Patch(facecolor=c, edgecolor=edgecolor or c, hatch=h, linewidth=2 if edgecolor else 0)
            for c, h in zip(colors, hatches)]


def legend_panel(ax, handles, labels, ncols=1, hatches=None, edgecolor=None):
    """Turn ``ax`` into a legend-only panel.

    ``handles`` may be ready-made artists (lines or ``patches()`` output), or a list of
    colors.  The color form keeps the concise API used by the approved output_unseen
    programs and accepts optional hatches and patch outlines.
    """
    if handles and all(mpl.colors.is_color_like(item) for item in handles):
        handles = patches(handles, hatches=hatches, edgecolor=edgecolor)
    ax.legend(handles, labels, loc="center", ncols=ncols)
    ax.set_axis_off()


def label_bars(ax, bars, values, errs=None, fmt="{:.2f}"):
    """Print each value just above its bar (and error bar)."""
    errs = np.zeros(len(values)) if errs is None else np.asarray(errs)
    lo, hi = ax.get_ylim()
    for bar, v, e in zip(bars, values, errs):
        ax.text(bar.get_x() + bar.get_width() / 2, v + e + 0.01 * (hi - lo), fmt.format(v),
                ha="center", va="bottom", fontsize=FONT["annot"])


def tight_ylim(ax, values, errs=None, pad=0.25):
    """Zoom the y-axis onto the data so small differences show; say so in the caption."""
    values = np.asarray(values, dtype=float)
    errs = np.zeros_like(values) if errs is None else np.asarray(errs, dtype=float)
    lo, hi = (values - errs).min(), (values + errs).max()
    span = hi - lo
    ax.set_ylim(max(0.0, lo - pad * span) if lo >= 0 else lo - pad * span, hi + pad * span)


def fade_line(ax, x, y, color, label=None, alpha=(0.3, 0.9), marker="o"):
    """Line whose segments fade in from left to right, with solid markers on top."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    points = np.column_stack([x, y]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    rgb = to_rgb(color)
    colors = [(*rgb, a) for a in np.linspace(*alpha, len(segments))]
    ax.add_collection(LineCollection(segments, colors=colors, linewidths=4, capstyle="round"))
    ax.plot(x, y, linestyle="none", marker=marker, markersize=16, color=color)
    ax.plot([], [], color=color, linewidth=4, marker=marker, markersize=16, label=label)  # legend entry
    ax.autoscale_view()


def pad_ylim(ax, top=0.0, bottom=0.0):
    """Extend y-limits by a fraction of the current range (in log space on log axes)."""
    lo, hi = ax.get_ylim()
    if ax.get_yscale() == "log":
        lo, hi = np.log10(lo), np.log10(hi)
        span = hi - lo
        ax.set_ylim(10 ** (lo - bottom * span), 10 ** (hi + top * span))
    else:
        span = hi - lo
        ax.set_ylim(lo - bottom * span, hi + top * span)


def save(fig, path, formats=("png",), dpi=300):
    """tight_layout, then save one file per format; returns the written paths."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=2)
    out = [path.with_suffix(f".{ext}") for ext in formats]
    for p in out:
        fig.savefig(p, dpi=dpi)
    return out
