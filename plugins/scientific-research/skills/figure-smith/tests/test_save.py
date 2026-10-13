"""save() writes a vector PDF with selectable text alongside the PNG preview."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pubstyle as ps


class SaveTest(unittest.TestCase):
    def save_default(self, out_dir):
        ps.apply_style()
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.plot([0, 1], [0, 1])
        ax.set_ylabel("Accuracy ↑")
        written = ps.save(fig, Path(out_dir) / "fig")
        plt.close(fig)
        return written

    def test_default_writes_pdf_and_png(self):
        with tempfile.TemporaryDirectory() as out_dir:
            written = self.save_default(out_dir)
            self.assertEqual({p.suffix for p in written}, {".pdf", ".png"})
            self.assertTrue(all(p.exists() for p in written))

    def test_pdf_embeds_text_as_truetype_not_outlines(self):
        with tempfile.TemporaryDirectory() as out_dir:
            pdf = next(p for p in self.save_default(out_dir) if p.suffix == ".pdf")
            data = pdf.read_bytes()
            self.assertIn(b"/FontFile2", data)  # embedded TrueType: text stays selectable
            self.assertNotIn(b"/Type3", data)


if __name__ == "__main__":
    unittest.main()
