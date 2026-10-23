"""The worked example in examples/ is a complete session, and the skill names no session file it no longer writes."""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
EXAMPLE = SKILL_DIR / "examples" / "grill-with-docs"
PLUGIN_DIR = SKILL_DIR.parents[1]


def test_example_session_holds_plan_flow_page_and_review():
    assert {p.name for p in EXAMPLE.iterdir()} == {"plan.md", "flow.html", "review-1.md"}


def test_example_flow_page_cites_only_decisions_the_plan_defines():
    cited = set(re.findall(r"\bD\d+\b", (EXAMPLE / "flow.html").read_text(encoding="utf-8")))
    defined = set(re.findall(r"^### (D\d+) ", (EXAMPLE / "plan.md").read_text(encoding="utf-8"), re.M))

    assert cited and cited <= defined


def test_skill_files_name_no_removed_session_file():
    files = [*SKILL_DIR.rglob("*.md"), PLUGIN_DIR / "agents" / "grill-plan-reviewer.md"]

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"flow\.json|flow\.svg|render_flow|flow\.artifact", text), path
