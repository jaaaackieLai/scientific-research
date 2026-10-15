"""Rules that keep paper-dissector easy to override.

Hosts insert their own note sections and turn off rules they do not want, so
other files name note sections instead of numbering them.
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

