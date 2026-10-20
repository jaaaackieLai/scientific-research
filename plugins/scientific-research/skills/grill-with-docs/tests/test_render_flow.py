"""Behavior tests for render_flow.py: the page that shows the current flow against the planned one."""
import importlib.util
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("render_flow", SCRIPTS / "render_flow.py")
render_flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_flow)

DATA = {
    "title": "Refund approval",
    "as_is": {"steps": [
        {"id": "submit", "label": "Customer submits refund form", "actor": "Customer", "next": ["print"]},
        {"id": "print", "label": "Clerk prints the form", "actor": "Clerk", "next": ["review"], "decision": "D2"},
        {"id": "review", "label": "Manager reviews", "actor": "Manager"},
    ]},
    "to_be": {"steps": [
        {"id": "submit", "label": "Customer submits refund form", "actor": "Customer", "next": ["review"], "decision": "D2"},
        {"id": "review", "label": "Rules engine reviews", "actor": "System",
         "next": [{"to": "notify", "when": "amount < 100"}], "decision": "D1"},
        {"id": "notify", "label": "Email the customer", "actor": "System", "decision": "D3"},
    ]},
}
DECISIONS = {"D1": "Auto-approve small refunds", "D2": "Drop paper forms", "D3": "Notify by email"}


def rows_in(page):
    return re.findall(r'<tr class="row (\w+)" id="step-([a-z0-9-]+)"', page)


def test_page_shows_each_step_once_with_its_status_in_diff_order():
    page = render_flow.render(DATA, DECISIONS)

    assert rows_in(page) == [
        ("changed", "submit"), ("removed", "print"), ("changed", "review"), ("added", "notify"),
    ]


def test_summary_counts_each_kind_of_difference():
    page = render_flow.render(DATA, DECISIONS)

    summary = re.search(r'<ul class="summary">(.*?)</ul>', page, re.S).group(1)
    counts = dict((kind, int(n)) for n, kind in re.findall(r"<b>(\d+)</b> (\w+)", summary))
    assert counts == {"added": 1, "removed": 1, "changed": 2, "same": 0}


def test_step_text_is_escaped():
    data = {**DATA, "title": "A <b> & C", "to_be": {"steps": [
        {"id": "submit", "label": "<script>alert(1)</script>", "decision": "D2"}]}}

    page = render_flow.render(data, DECISIONS)

    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "<title>A &lt;b&gt; &amp; C</title>" in page


def test_each_difference_shows_its_decision_and_title():
    page = render_flow.render(DATA, DECISIONS)

    review = re.search(r'id="step-review".*?</tr>', page, re.S).group(0)
    removed = re.search(r'id="step-print".*?</tr>', page, re.S).group(0)
    assert '<span class="rev">D1</span><span class="dtitle">Auto-approve small refunds</span>' in review
    assert '<span class="rev">D2</span><span class="dtitle">Drop paper forms</span>' in removed


def test_planned_diagram_colors_steps_by_difference_and_labels_branches():
    text = render_flow.mermaid(DATA["to_be"]["steps"], {"submit": "changed", "review": "changed", "notify": "added"})

    assert text.splitlines()[0] == "flowchart TD"
    assert 'n0["Customer submits refund form"]:::changed' in text
    assert 'n2["Email the customer"]:::added' in text
    assert 'n1 -->|"amount #lt; 100"| n2' in text
    assert "n0 --> n1" in text


def test_page_draws_the_current_and_planned_diagrams():
    page = render_flow.render(DATA, DECISIONS)

    diagrams = re.findall(r'<pre class="mermaid">(.*?)</pre>', page, re.S)
    assert len(diagrams) == 2
    assert ":::removed" in diagrams[0] and "Clerk prints the form" in diagrams[0]
    assert ":::added" in diagrams[1] and "Clerk prints the form" not in diagrams[1]


def test_standalone_page_is_a_full_document_that_loads_mermaid():
    page = render_flow.render(DATA, DECISIONS, standalone=True)

    assert page.startswith("<!doctype html>")
    assert re.search(r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@\d+\.\d+\.\d+/dist/mermaid\.min\.js">', page)


def test_artifact_fragment_leaves_the_skeleton_and_mermaid_to_the_host():
    page = render_flow.render(DATA, DECISIONS)

    assert page.startswith("<title>")
    assert "<html" not in page and "<body" not in page and "mermaid.min.js" not in page


PLAN = "# Plan: Refund approval\n\n## Decisions\n\n### D1 - Auto-approve small refunds\n\n### D2 - Drop paper forms\n\n### D3 - Notify by email\n"


def session(tmp_path, data=DATA, plan=PLAN):
    import json
    (tmp_path / "flow.json").write_text(json.dumps(data), encoding="utf-8")
    if plan is not None:
        (tmp_path / "plan.md").write_text(plan, encoding="utf-8")
    return tmp_path


def test_cli_writes_the_standalone_page_for_a_valid_session(tmp_path, capsys):
    run = session(tmp_path)

    assert render_flow.main([str(run)]) == 0
    page = (run / "flow.html").read_text(encoding="utf-8")
    assert page.startswith("<!doctype html>") and "Auto-approve small refunds" in page
    assert str(run / "flow.html") in capsys.readouterr().out


def test_cli_artifact_flag_writes_the_artifact_page(tmp_path):
    run = session(tmp_path)

    assert render_flow.main([str(run), "--artifact"]) == 0
    assert (run / "flow.artifact.html").read_text(encoding="utf-8").startswith("<title>")


def test_cli_reports_problems_and_writes_nothing(tmp_path, capsys):
    run = session(tmp_path, plan=PLAN.replace("### D3 - Notify by email\n", ""))

    assert render_flow.main([str(run)]) == 1
    assert capsys.readouterr().out.splitlines() == ["to_be: step 'notify' cites D3, which plan.md does not define"]
    assert not (run / "flow.html").exists()


def test_cli_reports_unreadable_json(tmp_path, capsys):
    (tmp_path / "flow.json").write_text("{not json", encoding="utf-8")

    assert render_flow.main([str(tmp_path)]) == 1
    assert capsys.readouterr().out.startswith("flow.json: not valid JSON")


def test_cli_check_flag_only_checks(tmp_path, capsys):
    run = session(tmp_path)

    assert render_flow.main([str(run), "--check"]) == 0
    assert capsys.readouterr().out == "OK: no problems found\n"
    assert not (run / "flow.html").exists()
