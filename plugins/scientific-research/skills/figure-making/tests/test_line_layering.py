"""Render crossings to verify proposed-method lines and markers remain visible."""
import importlib.util
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

import pubstyle as ps

spec = importlib.util.spec_from_file_location("line_sensitivity", SKILL / "examples" / "line_sensitivity.py")
template = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template)


class LineLayeringTest(unittest.TestCase):
    def render(self, fade, crossing, ours_last=False):
        # Draw ours FIRST: priority must survive a baseline drawn later.
        template.METHODS = ["Ours", "Baseline"]
        template.COLORS = [ps.OURS, ps.BLUES[-2]]
        template.MARKERS = ["o", "s"]
        ys = [[-1, 1], [1, -1]] if crossing else [[0, 1], [0, -1]]
        if ours_last:
            template.METHODS.reverse()
            template.COLORS.reverse()
            template.MARKERS.reverse()
            ys.reverse()
        ps.apply_style()
        fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
        template.curves(ax, [0, 1], ys, fade=fade)
        # Bands and reference lines added later also belong behind the methods.
        ax.fill_between([-1, 2], -2, 2, color=ps.GRAY, zorder=1)
        ax.axhline(0, **ps.REFERENCE)
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_axis_off()
        fig.canvas.draw()
        x, y = ax.transData.transform((0.5 if crossing else 0, 0))
        pixels = np.asarray(fig.canvas.buffer_rgba())
        rgb = pixels[pixels.shape[0] - 1 - round(y), round(x), :3]
        plt.close(fig)
        return rgb

    def check_ours_visible(self, fade, crossing):
        expected = np.array(to_rgb(ps.OURS)) * 255
        np.testing.assert_allclose(self.render(fade, crossing), expected, atol=2,
                                   err_msg="The baseline obscures the proposed method")

    def test_regular_crossing(self):
        self.check_ours_visible(fade=False, crossing=True)

    def test_regular_overlapping_marker(self):
        self.check_ours_visible(fade=False, crossing=False)

    def test_gradient_crossing(self):
        # A translucent foreground must match drawing ours last, regardless
        # of the actual method iteration order.
        rgb = self.render(fade=True, crossing=True)
        expected = self.render(fade=True, crossing=True, ours_last=True)
        np.testing.assert_allclose(rgb, expected, atol=2,
                                   err_msg="The later baseline gradient hides ours")

    def test_gradient_overlapping_marker(self):
        self.check_ours_visible(fade=True, crossing=False)


if __name__ == "__main__":
    unittest.main()
