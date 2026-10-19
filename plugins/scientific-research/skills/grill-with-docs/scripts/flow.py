#!/usr/bin/env python3
"""Align a session's current flow with its planned flow, step by step."""
import re
from collections import namedtuple
from difflib import SequenceMatcher

Row = namedtuple("Row", "id status before after changes")
COMPARED = ("label", "actor", "next")
STEP_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def edges(s):
    """A step's outgoing edges as `(target, condition)` pairs; `next` may list ids or `{to, when}` objects."""
    return tuple(
        (e, "") if isinstance(e, str) else (e.get("to", ""), e.get("when", ""))
        for e in s.get("next", [])
    )


def _value(s, field):
    return edges(s) if field == "next" else s.get(field, "")


def _moved(as_is, to_be):
    """Ids of shared steps outside the order the two flows have in common (difflib matching blocks)."""
    planned = [s["id"] for s in to_be]
    shared_before = [s["id"] for s in as_is if s["id"] in planned]
    shared_after = [i for i in planned if i in set(shared_before)]
    blocks = SequenceMatcher(None, shared_before, shared_after, autojunk=False).get_matching_blocks()
    kept = {shared_after[b.b + k] for b in blocks for k in range(b.size)}
    return set(shared_after) - kept


def _row(before, after, moved):
    if before is None:
        return Row(after["id"], "added", None, after, ())
    changes = tuple(f for f in COMPARED if _value(before, f) != _value(after, f))
    changes += ("order",) if after["id"] in moved else ()
    return Row(after["id"], "changed" if changes else "unchanged", before, after, changes)


def diff(as_is, to_be):
    """Rows in planned order; each pairs a step's current and planned versions."""
    current = {s["id"]: s for s in as_is}
    moved = _moved(as_is, to_be)
    rows = tuple(_row(current.get(s["id"]), s, moved) for s in to_be)
    return list(_insert_removed(rows, as_is, {s["id"] for s in to_be}))


def _insert_removed(rows, as_is, planned_ids):
    """Place each removed step right after the step that preceded it in the current flow."""
    anchor = -1
    for s in as_is:
        if s["id"] in planned_ids:
            anchor = next(i for i, row in enumerate(rows) if row.id == s["id"])
        else:
            anchor += 1
            rows = rows[:anchor] + (Row(s["id"], "removed", s, None, ()),) + rows[anchor:]
    return rows


def _step_problems(name, s, ids):
    bad_id = [] if STEP_ID.fullmatch(s.get("id", "")) else [
        f"{name}: step id {s.get('id', '')!r} must be lowercase letters, digits and hyphens"]
    no_label = [] if s.get("label", "").strip() else [f"{name}: step {s['id']!r} has no label"]
    dangling = [f"{name}: step {s['id']!r} points at missing step {to!r}" for to, _ in edges(s) if to not in ids]
    return bad_id + no_label + dangling


def _flow_problems(name, steps):
    ids = [s.get("id", "") for s in steps]
    duplicates = [f"{name}: step id {i!r} appears more than once" for i in dict.fromkeys(ids) if ids.count(i) > 1]
    return duplicates + [p for s in steps for p in _step_problems(name, s, set(ids))]


def _trace_problems(rows):
    """Every difference between the flows must name the decision that caused it."""
    return [
        f"{'as_is' if row.status == 'removed' else 'to_be'}: {row.status} step {row.id!r} "
        "needs a decision (D<n>) that explains it"
        for row in rows
        if row.status != "unchanged" and not (row.after or row.before).get("decision")
    ]


def _cite_problems(data, decisions):
    return [
        f"{name}: step {s['id']!r} cites {s['decision']}, which plan.md does not define"
        for name in ("as_is", "to_be")
        for s in data[name]["steps"]
        if s.get("decision") and s["decision"] not in decisions
    ]


def _shape_problems(data):
    title = [] if str(data.get("title", "")).strip() else ["flow.json: missing a non-empty 'title'"]
    return title + [
        f"flow.json: missing '{name}.steps' (a list of steps)"
        for name in ("as_is", "to_be")
        if not isinstance(data.get(name, {}).get("steps"), list)
    ]


def check(data, decisions=None):
    """Problems in a flow.json document; `decisions` is the set of decision ids in plan.md, if known."""
    shape = _shape_problems(data)
    if shape:
        return shape
    as_is, to_be = data["as_is"]["steps"], data["to_be"]["steps"]
    structure = _flow_problems("as_is", as_is) + _flow_problems("to_be", to_be)
    if structure:
        return structure
    cites = _cite_problems(data, decisions) if decisions is not None else []
    return _trace_problems(diff(as_is, to_be)) + cites


def decision_ids(plan_text):
    """The `D<n>` ids plan.md defines, one per `### D<n>` heading."""
    return set(re.findall(r"^### (D\d+)\b", plan_text, re.M))
