"""apply_style() frames every axes on all four sides and sets the agreed font sizes."""
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pubstyle as ps


class StyleTest(unittest.TestCase):
    def setUp(self):
        ps.apply_style()
        self.fig, self.ax = plt.subplots()

    def tearDown(self):
        plt.close(self.fig)

    def test_all_four_spines_visible(self):
        for side in ("top", "right", "bottom", "left"):
            self.assertTrue(self.ax.spines[side].get_visible(), side)

    def test_font_sizes(self):
        self.assertEqual(self.ax.xaxis.label.get_fontsize(), 28)
        self.assertEqual(self.ax.yaxis.label.get_fontsize(), 28)
        self.assertEqual(self.ax.get_xticklabels()[0].get_fontsize(), 28)
        self.assertEqual(self.ax.get_yticklabels()[0].get_fontsize(), 28)
        self.ax.plot([0, 1], [0, 1], label="a")
        legend_text = self.ax.legend().get_texts()[0]
        self.assertEqual(legend_text.get_fontsize(), 24)

    def test_line_widths_are_three(self):
        plain, = self.ax.plot([0, 1], [0, 1])
        self.assertEqual(plain.get_linewidth(), 3)
        ps.fade_line(self.ax, [0, 1, 2], [0, 1, 2], ps.OURS, label="ours")
        segments = self.ax.collections[-1]
        self.assertTrue(all(w == 3 for w in segments.get_linewidths()))
        legend_entry = self.ax.lines[-1]
        self.assertEqual(legend_entry.get_linewidth(), 3)
        self.assertEqual(self.ax.axhline(0.5, **ps.REFERENCE).get_linewidth(), 3)


if __name__ == "__main__":
    unittest.main()
