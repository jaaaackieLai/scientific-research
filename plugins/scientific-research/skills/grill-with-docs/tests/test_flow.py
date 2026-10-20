"""Behavior tests for flow.py: aligning the current flow with the planned flow and checking flow.json."""
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "flow.py"
spec = importlib.util.spec_from_file_location("flow", SCRIPT)
flow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)


def step(step_id, label=None, **fields):
    return {"id": step_id, "label": label or step_id.title(), **fields}


def statuses(rows):
    return [(row.id, row.status) for row in rows]


def test_identical_flows_are_all_unchanged():
    steps = [step("submit", next=["review"]), step("review")]

    rows = flow.diff(steps, steps)

    assert statuses(rows) == [("submit", "unchanged"), ("review", "unchanged")]


def test_step_only_in_planned_flow_is_added():
    rows = flow.diff([step("submit")], [step("submit"), step("auto-check")])

    assert statuses(rows) == [("submit", "unchanged"), ("auto-check", "added")]
    assert rows[1].before is None


def test_removed_steps_sit_after_their_current_predecessor():
    as_is = [step("submit"), step("print"), step("sign"), step("review"), step("file")]
    to_be = [step("submit"), step("review"), step("archive")]

    rows = flow.diff(as_is, to_be)

    assert statuses(rows) == [
        ("submit", "unchanged"), ("print", "removed"), ("sign", "removed"),
        ("review", "unchanged"), ("file", "removed"), ("archive", "added"),
    ]
    assert rows[1].after is None


def test_removed_first_step_opens_the_rows():
    rows = flow.diff([step("login"), step("submit")], [step("submit")])

    assert statuses(rows) == [("login", "removed"), ("submit", "unchanged")]


def test_step_with_different_fields_is_changed_and_names_them():
    as_is = [step("review", "Manager reviews", actor="Manager", next=["pay"]), step("pay")]
    to_be = [step("review", "Rules engine reviews", actor="System", next=["pay"]), step("pay")]

    rows = flow.diff(as_is, to_be)

    assert statuses(rows) == [("review", "changed"), ("pay", "unchanged")]
    assert rows[0].changes == ("label", "actor")
    assert rows[1].changes == ()


def test_next_written_as_ids_or_branches_compares_by_target_and_condition():
    as_is = [step("check", next=["pay"]), step("pay"), step("deny")]
    same = [step("check", next=[{"to": "pay"}]), step("pay"), step("deny")]
    branched = [step("check", next=[{"to": "pay", "when": "ok"}, {"to": "deny", "when": "fraud"}]), step("pay"), step("deny")]

    assert flow.diff(as_is, same)[0].status == "unchanged"
    assert flow.diff(as_is, branched)[0].changes == ("next",)


def test_step_that_moved_relative_to_the_others_is_changed_in_order():
    as_is = [step("a"), step("b"), step("c"), step("d")]
    to_be = [step("a"), step("c"), step("d"), step("b")]

    rows = flow.diff(as_is, to_be)

    assert statuses(rows) == [("a", "unchanged"), ("c", "unchanged"), ("d", "unchanged"), ("b", "changed")]
    assert rows[3].changes == ("order",)


def doc(as_is, to_be, title="Refunds"):
    return {"title": title, "as_is": {"steps": as_is}, "to_be": {"steps": to_be}}


def test_a_traced_flow_has_no_problems():
    data = doc([step("submit", next=["review"]), step("review")],
               [step("submit", next=["check"]), step("check", decision="D1")])
    data["as_is"]["steps"][1]["decision"] = "D1"
    data["to_be"]["steps"][0]["decision"] = "D1"

    assert flow.check(data, decisions={"D1"}) == []


def test_duplicate_step_ids_are_a_problem():
    data = doc([step("submit"), step("submit")], [step("submit")])

    assert flow.check(data) == ["as_is: step id 'submit' appears more than once"]


def test_edges_must_point_at_a_step_in_the_same_flow():
    data = doc([step("submit", next=["review"])], [step("submit", next=[{"to": "pay", "when": "ok"}])])
    data["to_be"]["steps"][0]["decision"] = "D1"

    assert flow.check(data) == [
        "as_is: step 'submit' points at missing step 'review'",
        "to_be: step 'submit' points at missing step 'pay'",
    ]


def test_steps_need_a_kebab_case_id_and_a_label():
    data = doc([step("Submit Form"), {"id": "review", "label": " "}], [])

    assert flow.check(data) == [
        "as_is: step id 'Submit Form' must be lowercase letters, digits and hyphens",
        "as_is: step 'review' has no label",
    ]


def test_every_difference_names_the_decision_behind_it():
    data = doc([step("submit"), step("print"), step("review", "Manager reviews")],
               [step("submit"), step("review", "Rules engine reviews"), step("notify")])

    assert flow.check(data) == [
        "as_is: removed step 'print' needs a decision (D<n>) that explains it",
        "to_be: changed step 'review' needs a decision (D<n>) that explains it",
        "to_be: added step 'notify' needs a decision (D<n>) that explains it",
    ]


def test_named_decisions_must_exist_in_the_plan():
    data = doc([step("submit")], [step("submit"), step("notify", decision="D7")])

    assert flow.check(data, decisions={"D1"}) == ["to_be: step 'notify' cites D7, which plan.md does not define"]
    assert flow.check(data) == []


def test_structural_problems_skip_the_trace_check():
    data = doc([step("submit"), step("submit")], [step("notify")])

    assert flow.check(data) == ["as_is: step id 'submit' appears more than once"]


def test_decisions_come_from_plan_headings_with_their_titles():
    plan = "# Plan: Refunds\n\n## Decisions\n\n### D1 - Auto-approve small refunds\n- x\n\n### D12 - Notify by email\n\nSee D99 later.\n"

    assert flow.decisions(plan) == {"D1": "Auto-approve small refunds", "D12": "Notify by email"}


def test_missing_top_level_fields_are_problems_not_crashes():
    assert flow.check({"as_is": {"steps": []}}) == [
        "flow.json: missing a non-empty 'title'",
        "flow.json: missing 'to_be.steps' (a list of steps)",
    ]


def test_a_new_flow_may_start_from_an_empty_current_flow():
    data = doc([], [step("submit", decision="D1")])

    assert flow.check(data, decisions={"D1"}) == []


def test_a_step_without_id_or_an_edge_without_target_is_reported():
    data = doc([{"label": "Submit"}], [step("review", next=[{"when": "ok"}])])

    assert flow.check(data) == [
        "as_is: step id '' must be lowercase letters, digits and hyphens",
        "to_be: step 'review' points at missing step ''",
    ]
