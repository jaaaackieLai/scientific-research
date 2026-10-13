"""Every plugin agent is valid and delegates to an idea-forge role file, and every role file has an agent."""
import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

PLUGIN_DIR = Path(__file__).resolve().parents[1]
ROLES_DIR = PLUGIN_DIR / "skills" / "idea-forge" / "roles"
AGENTS = sorted((PLUGIN_DIR / "agents").glob("*.md"))
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
ROLE_REF = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/skills/idea-forge/roles/([a-z-]+\.md)")


def parse(agent_md):
    match = FRONTMATTER.match(agent_md.read_text(encoding="utf-8"))
    assert match, "missing --- delimiters around the frontmatter"
    return yaml.safe_load(match.group(1)), match.group(2)


@pytest.mark.parametrize("agent_md", AGENTS, ids=lambda p: p.stem)
def test_agent_frontmatter_and_role_reference(agent_md):
    meta, body = parse(agent_md)

    assert meta["name"] == agent_md.stem
    assert re.fullmatch(r"[a-z0-9-]{1,64}", meta["name"])
    assert isinstance(meta["description"], str) and meta["description"]
    assert isinstance(meta["tools"], str) and meta["tools"]
    roles = ROLE_REF.findall(body)
    assert len(roles) == 1, "the body must point at exactly one role file"
    assert (ROLES_DIR / roles[0]).is_file()


def test_every_role_has_an_agent():
    referenced = {ROLE_REF.findall(parse(agent_md)[1])[0] for agent_md in AGENTS}

    assert referenced == {role.name for role in ROLES_DIR.glob("*.md")}
