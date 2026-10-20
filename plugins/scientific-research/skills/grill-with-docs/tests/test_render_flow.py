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


def diagram(steps):
    """A minimal flow.svg: one group per `(side:id, status)` pair."""
    groups = "".join(f'<g data-step="{step}" data-status="{status}"><rect width="10" height="10"/></g>' for step, status in steps)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><title>Refund approval</title>{groups}</svg>'


STEPS = [
    ("as_is:submit", "changed"), ("as_is:print", "removed"), ("as_is:review", "changed"),
    ("to_be:submit", "changed"), ("to_be:review", "changed"), ("to_be:notify", "added"),
]
SVG = diagram(STEPS)


def rows_in(page):
    return re.findall(r'<tr class="row (\w+)" id="step-([a-z0-9-]+)"', page)


def test_page_shows_each_step_once_with_its_status_in_diff_order():
    page = render_flow.render(DATA, DECISIONS, SVG)

    assert rows_in(page) == [
        ("changed", "submit"), ("removed", "print"), ("changed", "review"), ("added", "notify"),
    ]


def test_summary_counts_each_kind_of_difference():
    page = render_flow.render(DATA, DECISIONS, SVG)

    summary = re.search(r'<ul class="summary">(.*?)</ul>', page, re.S).group(1)
    counts = dict((kind, int(n)) for n, kind in re.findall(r"<b>(\d+)</b> (\w+)", summary))
    assert counts == {"added": 1, "removed": 1, "changed": 2, "same": 0}


def test_step_text_is_escaped():
    data = {**DATA, "title": "A <b> & C", "to_be": {"steps": [
        {"id": "submit", "label": "<script>alert(1)</script>", "decision": "D2"}]}}

    page = render_flow.render(data, DECISIONS, SVG)

    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "<title>A &lt;b&gt; &amp; C</title>" in page


def test_each_difference_shows_its_decision_and_title():
    page = render_flow.render(DATA, DECISIONS, SVG)

    review = re.search(r'id="step-review".*?</tr>', page, re.S).group(0)
    removed = re.search(r'id="step-print".*?</tr>', page, re.S).group(0)
    assert '<span class="rev">D1</span><span class="dtitle">Auto-approve small refunds</span>' in review
    assert '<span class="rev">D2</span><span class="dtitle">Drop paper forms</span>' in removed


def test_page_inlines_the_flow_diagram_in_place_of_mermaid():
    page = render_flow.render(DATA, DECISIONS, SVG)

    figure = re.search(r'<figure class="diagram">(.*?)</figure>', page, re.S).group(1)
    assert '<g data-step="as_is:print" data-status="removed">' in figure
    assert '<g data-step="to_be:notify" data-status="added">' in figure
    assert "mermaid" not in page


def test_standalone_page_is_a_full_document_that_loads_no_script():
    page = render_flow.render(DATA, DECISIONS, SVG, standalone=True)

    assert page.startswith("<!doctype html>")
    assert "<script" not in page


def test_artifact_fragment_leaves_the_skeleton_to_the_host():
    page = render_flow.render(DATA, DECISIONS, SVG)

    assert page.startswith("<title>")
    assert "<html" not in page and "<body" not in page


PLAN = "# Plan: Refund approval\n\n## Decisions\n\n### D1 - Auto-approve small refunds\n\n### D2 - Drop paper forms\n\n### D3 - Notify by email\n"


def session(tmp_path, data=DATA, plan=PLAN, svg=SVG):
    import json
    (tmp_path / "flow.json").write_text(json.dumps(data), encoding="utf-8")
    if svg is not None:
        (tmp_path / "flow.svg").write_text(svg, encoding="utf-8")
    if plan is not None:
        (tmp_path / "plan.md").write_text(plan, encoding="utf-8")
    return tmp_path


def test_cli_writes_the_standalone_page_for_a_valid_session(tmp_path, capsys):
    run = session(tmp_path)

    assert render_flow.main([str(run)]) == 0
    page = (run / "flow.html").read_text(encoding="utf-8")
    assert page.startswith("<!doctype html>") and "Auto-approve small refunds" in page
    assert '<g data-step="to_be:notify" data-status="added">' in page
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


def problems(tmp_path, capsys, svg):
    run = session(tmp_path, svg=svg)
    assert render_flow.main([str(run), "--check"]) == 1
    return capsys.readouterr().out.splitlines()


def test_cli_requires_the_flow_diagram(tmp_path, capsys):
    assert problems(tmp_path, capsys, None) == ["flow.svg: missing; draw it from flow.json (SKILL.md step 4)"]


def test_cli_reports_steps_the_diagram_misses_or_still_shows(tmp_path, capsys):
    stale = [s for s in STEPS if s[0] != "to_be:notify"] + [("to_be:print", "unchanged")]

    assert problems(tmp_path, capsys, diagram(stale)) == [
        "flow.svg: no group for step 'to_be:notify' (data-step)",
        "flow.svg: step 'to_be:print' is not in flow.json",
    ]


def test_cli_reports_a_status_that_disagrees_with_the_diff(tmp_path, capsys):
    wrong = [(s, "unchanged" if s == "as_is:review" else status) for s, status in STEPS]

    assert problems(tmp_path, capsys, diagram(wrong)) == [
        "flow.svg: step 'as_is:review' has data-status 'unchanged', but flow.json makes it 'changed'",
    ]


def test_cli_refuses_a_diagram_that_runs_code(tmp_path, capsys):
    svg = SVG.replace("<title>", '<script>alert(1)</script><a href="javascript:x"><rect onclick="x"/></a><title>')

    assert problems(tmp_path, capsys, svg) == [
        "flow.svg: <script> is not allowed",
        "flow.svg: attribute 'href' runs code",
        "flow.svg: attribute 'onclick' runs code",
    ]


def test_cli_reports_a_diagram_that_is_not_svg(tmp_path, capsys):
    assert problems(tmp_path, capsys, "<svg><g></svg>")[0].startswith("flow.svg: not valid XML")
    assert problems(tmp_path, capsys, "<html/>") == ["flow.svg: the root element must be <svg>"]
