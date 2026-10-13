"""references/artifacts.md and check_run.py describe the same formats; agents follow the first, the gate enforces the second."""
import importlib.util
import re
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_run", SKILL_DIR / "scripts" / "check_run.py")
check_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_run)

ARTIFACTS_MD = (SKILL_DIR / "references" / "artifacts.md").read_text(encoding="utf-8")
OPTIONAL_FIELDS = {"candidates.md": {"If improving prior candidate"}}


def template(name):
    """The first fenced block under the `## \\`<name>\\`` heading of artifacts.md."""
    match = re.search(rf"^## `{re.escape(name)}`.*?^```markdown\n(.*?)^```", ARTIFACTS_MD, re.M | re.S)
    assert match, f"artifacts.md has no template for {name}"
    return match.group(1)


@pytest.mark.parametrize("name", list(check_run.SPECS))
def test_template_fields_match_checker(name):
    labels = re.findall(r"^- \*\*(.+?):\*\*", template(name), re.M)

    assert set(labels) == set(check_run.SPECS[name].fields) | OPTIONAL_FIELDS.get(name, set())


@pytest.mark.parametrize("name", list(check_run.SPECS))
def test_template_headings_parse_as_blocks(name):
    assert check_run.blocks(template(name).replace("<n>", "1").replace("<k>", "1"), check_run.SPECS[name].heading)


def test_proposal_template_matches_checker():
    text = template("proposal.md")

    assert re.findall(r"^## (.+)$", text, re.M) == list(check_run.PROPOSAL_SECTIONS)
    assert check_run.NOTICE in ARTIFACTS_MD


def test_paper_reader_digest_template_matches_artifacts():
    reader = (SKILL_DIR / "roles" / "paper-reader.md").read_text(encoding="utf-8")
    reader_template = re.search(r"^```markdown\n(.*?)^```", reader, re.M | re.S).group(1)

    def skeleton(text):
        return re.findall(r"^(#+ [A-Z][\w -]*|- [A-Z][\w ]*:)", text, re.M)

    assert skeleton(reader_template) == skeleton(template("papers/<id>.md"))
