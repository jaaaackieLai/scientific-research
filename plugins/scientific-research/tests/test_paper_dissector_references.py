"""Rules that keep paper-dissector easy to override.

Hosts insert their own note sections and turn off rules they do not want, so
other files name note sections instead of numbering them, and the citation rule
is stated once.
"""
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"
SKILL_DIR = SKILLS_DIR / "paper-dissector"
SKILL_FILES = sorted(SKILL_DIR.glob("**/*.md"))
SECTION_NUMBER = re.compile(r"\bSections? \d|§\s?\d")


def test_no_file_refers_to_a_note_section_by_number():
    files = SKILL_FILES + [SKILLS_DIR / "theory-auditor" / "SKILL.md"]
    hits = [
        f"{path.relative_to(SKILLS_DIR)}:{number}: {line.strip()}"
        for path in files
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if SECTION_NUMBER.search(line)
    ]

    assert not hits, "refer to sections by name:\n" + "\n".join(hits)


def section_lines(path, heading):
    """Lines under the given `##` heading of a markdown file, up to the next `##` heading."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("## ") and heading in line)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return set(lines[start:end])


def test_citation_rule_lives_only_in_citing_the_paper():
    citing = section_lines(SKILL_DIR / "references" / "writing.md", "Citing the paper")
    hits = [
        f"{path.relative_to(SKILL_DIR)}:{number}: {line.strip()}"
        for path in SKILL_FILES
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if "location" in line.lower() and line not in citing and "Citing the paper" not in line
    ]

    assert not hits, "state the citation rule once, in writing.md \"Citing the paper\":\n" + "\n".join(hits)
