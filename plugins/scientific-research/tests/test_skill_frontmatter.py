"""Every SKILL.md starts with valid YAML frontmatter whose name matches its directory."""
import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

SKILLS = sorted((Path(__file__).resolve().parents[1] / "skills").glob("*/SKILL.md"))
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


@pytest.mark.parametrize("skill_md", SKILLS, ids=lambda p: p.parent.name)
def test_frontmatter_is_valid_yaml_with_name_and_description(skill_md):
    match = FRONTMATTER.match(skill_md.read_text(encoding="utf-8"))
    assert match, "missing --- delimiters around the frontmatter"

    data = yaml.safe_load(match.group(1))

    assert data["name"] == skill_md.parent.name
    assert re.fullmatch(r"[a-z0-9-]{1,64}", data["name"])
    assert isinstance(data["description"], str) and 0 < len(data["description"]) <= 1024
