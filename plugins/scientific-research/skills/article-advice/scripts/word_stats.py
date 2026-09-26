"""Count word-bank terms in the main body of each PDF in a folder.

Usage:
    python word_stats.py <papers_dir>

The main body is the text before the first line that reads "References"
(or "Bibliography"); appendices after the references are ignored.
Requires PyMuPDF (pip install pymupdf).
"""
import collections
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

TERMS = {
    # A. vague verbs
    "utilize": r"\butiliz\w*",
    "leverage": r"\bleverag\w*",
    "adopt/employ": r"\b(adopt|employ)\w*",
    # B. self-evaluation
    "novel": r"\bnovel\b",
    "effectiveness": r"\beffectiveness\b",
    "superior": r"\bsuperior\w*",
    "remarkable": r"\bremarkabl\w*",
    "powerful": r"\bpowerful\b",
    "promising": r"\bpromising\b",
    "extensive": r"\bextensive(ly)?\b",
    "comprehensive": r"\bcomprehensive\w*",
    "SOTA": r"state-of-the-art|\bSoTA\b",
    "wisely": r"\bwisely\b",
    # C. intensifiers
    "significant(ly)": r"\bsignificant(ly)?\b",
    "statistically significant": r"\bstatistically significant\b",
    "seriously": r"\bseriously\b",
    "very": r"\bvery\b",
    # D. result verbs, strong to weak
    "prove": r"\bprov(e|es|ed|en)\b",
    "show": r"\bshow(s|ed|n)?\b",
    "demonstrate": r"\bdemonstrat\w*",
    "confirm": r"\bconfirm\w*",
    "find/found": r"\b(find|finds|found)\b",
    "observe": r"\bobserv\w*",
    "suggest": r"\bsuggest\w*",
    "indicate": r"\bindicat\w*",
    "consistent with": r"\bconsistent with\b",
    "may": r"\bmay\b",
    "likely": r"\blikely\b",
    "tend to": r"\btend(s)? to\b",
    # E. connectives
    "typically": r"\btypically\b",
    "specifically": r"\bspecifically\b",
    "however": r"\bhowever\b",
    "in contrast": r"\bin contrast\b",
}

REF_HEADING = re.compile(r"^\s*(\d+\s+)?(References|REFERENCES|Bibliography)\s*$", re.M)


def main_body(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        text = "\n".join(page.get_text() for page in doc)
    match = REF_HEADING.search(text)
    body = text[: match.start()] if match else text
    # Join words split across lines so multi-word terms still match.
    return " ".join(body.split())


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: python word_stats.py <papers_dir>")
    papers_dir = Path(sys.argv[1])
    pdfs = sorted(papers_dir.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDFs found in {papers_dir}")

    totals = collections.Counter()
    total_words = 0
    per_paper = []
    for pdf in pdfs:
        body = main_body(pdf)
        words = len(body.split())
        counts = {k: len(re.findall(p, body, re.I)) for k, p in TERMS.items()}
        totals.update(counts)
        total_words += words
        per_paper.append((pdf.stem, words, counts))

    print(f"{len(pdfs)} papers, {total_words} words in main bodies\n")
    print(f"{'term':26s}{'total':>7s}{'per10k':>8s}  most frequent in")
    for term in TERMS:
        top_name, _, top_counts = max(per_paper, key=lambda r: r[2][term])
        share = top_counts[term] / totals[term] if totals[term] else 0
        print(f"{term:26s}{totals[term]:7d}{totals[term] / total_words * 1e4:8.1f}  "
              f"{top_name[:45]} ({share:.0%})")


if __name__ == "__main__":
    main()
