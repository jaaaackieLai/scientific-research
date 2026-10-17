"""word_stats.py counts the word-bank terms added for urgency, self-praise and Chinese-English phrasing."""
import re
import sys
import types
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
sys.modules.setdefault("fitz", types.ModuleType("fitz"))  # PyMuPDF is only needed to read PDFs

from word_stats import TERMS


def count(term, text):
    return len(re.findall(TERMS[term], text, re.I))


class NewTermsTest(unittest.TestCase):
    def test_urgency_words(self):
        text = "Robustness is crucial. This presents a pressing need; it is imperative and urgently needed."
        self.assertEqual(count("crucial", text), 1)
        self.assertEqual(count("pressing/urgent", text), 3)

    def test_self_praise_words(self):
        text = "an optimal balance, a powerful decoder, innovative solutions, wonderful performance, incontrovertible proof"
        self.assertEqual(count("optimal", text), 1)
        self.assertEqual(count("powerful/innovative", text), 4)

    def test_claim_words(self):
        text = "effectively adapts; seamless integration; plug-and-play; a marginal increase; negligible cost"
        self.assertEqual(count("effectively", text), 1)
        self.assertEqual(count("seamless", text), 1)
        self.assertEqual(count("plug-and-play", text), 1)
        self.assertEqual(count("marginal/negligible", text), 2)

    def test_chinese_english_openers(self):
        text = "Besides, we also see it. It can be seen that X wins. As we can see, Y. It could be observed that Z."
        self.assertEqual(count("besides", text), 1)
        self.assertEqual(count("it can be seen", text), 3)


if __name__ == "__main__":
    unittest.main()
