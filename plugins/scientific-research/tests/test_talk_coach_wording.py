"""talk-coach borrows article-advice's wording rules for slide text instead of restating them.

It names the borrowed sections by heading, so a renamed or deleted heading in article-advice must fail here.
"""
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"
TALK_COACH = SKILLS_DIR / "talk-coach" / "SKILL.md"
ARTICLE_REFS = SKILLS_DIR / "article-advice" / "references"
PRINCIPLES_SECTIONS = [
    "Wording strength matches evidence strength",
    "Exaggerated wording",
    "Consistent terminology",
    "Sentences",
]


def headings(path):
    return [line.lstrip("#").strip() for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("## ")]


def test_talk_coach_names_article_advice_wording_files():
    text = TALK_COACH.read_text(encoding="utf-8")

    for name in ["principles.md", "word-bank.md"]:
        assert f"`article-advice/references/{name}`" in text
        assert (ARTICLE_REFS / name).is_file()


def test_borrowed_principles_sections_exist_and_are_named():
    text = TALK_COACH.read_text(encoding="utf-8")
    existing = [heading.split(". ", 1)[-1] for heading in headings(ARTICLE_REFS / "principles.md")]

    for section in PRINCIPLES_SECTIONS:
        assert section in existing, f"principles.md has no section {section!r}"
        assert f'"{section}"' in text, f"talk-coach does not name {section!r}"
