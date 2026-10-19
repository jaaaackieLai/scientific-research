#!/usr/bin/env python3
"""Render flow.json as one page that shows the current flow against the planned one.

Usage:
  python render_flow.py docs/grill/<slug>              # writes flow.html, a page to open locally
  python render_flow.py docs/grill/<slug> --artifact   # writes flow.artifact.html, a page to publish as an Artifact
  python render_flow.py docs/grill/<slug> --check      # checks only, writes nothing

Checks flow.json first (against plan.md's decisions when plan.md exists). On problems it prints one per
line, writes nothing, and exits 1; otherwise it prints the path it wrote and exits 0.
"""
import json
import sys
from html import escape
from pathlib import Path

from flow import check, decisions as plan_decisions, diff, edges

CSS = Path(__file__).with_name("flow_page.css")
FONTS = (
    "https://fonts.googleapis.com/css2?family=Archivo:wght@600;700"
    "&family=JetBrains+Mono:wght@400;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap"
)
MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"
STATUS_LABEL = {"added": "Added", "removed": "Removed", "changed": "Changed", "unchanged": "Same"}
MERMAID_ENTITIES = {"&": "#amp;", '"': "#quot;", "<": "#lt;", ">": "#gt;"}
MERMAID_CLASSES = (
    "classDef added fill:#dcf1e3,stroke:#1f7a4d,color:#10261a,stroke-width:2px",
    "classDef removed fill:#fbe3df,stroke:#b3261e,color:#3a1210,stroke-dasharray:5 3",
    "classDef changed fill:#fbedd2,stroke:#9a6200,color:#33240a,stroke-width:2px",
)


def _mermaid_text(text):
    return "".join(MERMAID_ENTITIES.get(c, c) for c in text)


def _mermaid_link(source, target, when):
    label = f'|"{_mermaid_text(when)}"|' if when else ""
    return f"{source} -->{label} {target}"


def mermaid(steps, statuses):
    """A Mermaid flowchart of one flow; `statuses` maps step ids to their diff status."""
    node = {s["id"]: f"n{i}" for i, s in enumerate(steps)}
    nodes = [
        f'{node[s["id"]]}["{_mermaid_text(s["label"])}"]'
        + (f':::{statuses[s["id"]]}' if statuses.get(s["id"], "unchanged") != "unchanged" else "")
        for s in steps
    ]
    links = [_mermaid_link(node[s["id"]], node[to], when) for s in steps for to, when in edges(s)]
    return "\n".join(["flowchart TD", *nodes, *links, *MERMAID_CLASSES])


def _edge_list(s):
    items = "".join(
        f'<li>&rarr; <code>{escape(to)}</code>{f" <span class=when>if {escape(when)}</span>" if when else ""}</li>'
        for to, when in edges(s)
    )
    return f'<ul class="next">{items}</ul>' if items else ""


def _cell(s, side, label):
    if s is None:
        return f'<td class="{side} empty" data-label="{label}"><span class="gap">not in this flow</span></td>'
    actor = f'<span class="actor">{escape(s["actor"])}</span>' if s.get("actor") else ""
    return f'<td class="{side}" data-label="{label}">{actor}<span class="label">{escape(s["label"])}</span>{_edge_list(s)}</td>'


def _decision_cell(row, decisions):
    decision = (row.after or row.before).get("decision", "")
    if row.status == "unchanged" and not decision:
        return '<td class="why"></td>'
    title = f'<span class="dtitle">{escape(decisions.get(decision, ""))}</span>' if decision else ""
    return f'<td class="why" data-label="Decision"><span class="rev">{escape(decision) or "?"}</span>{title}</td>'


def _row_html(index, row, decisions):
    changes = "".join(f'<span class="chip">{escape(c)}</span>' for c in row.changes)
    return (
        f'<tr class="row {row.status}" id="step-{escape(row.id)}">'
        f'<th scope="row"><span class="n">{index:02d}</span><code>{escape(row.id)}</code><br>'
        f'<span class="pill">{STATUS_LABEL[row.status]}</span>{changes}</th>'
        f'{_cell(row.before, "before", "Current")}{_cell(row.after, "after", "Planned")}'
        f"{_decision_cell(row, decisions)}</tr>"
    )


def _summary(rows):
    counts = "".join(
        f'<li class="{status}"><b>{sum(r.status == status for r in rows)}</b> {STATUS_LABEL[status].lower()}</li>'
        for status in STATUS_LABEL
    )
    return f'<ul class="summary">{counts}</ul>'


def _diagrams(data, rows):
    statuses = {row.id: row.status for row in rows}
    return "".join(
        f'<figure class="diagram {side}"><figcaption>{caption}</figcaption>'
        f'<pre class="mermaid">{escape(mermaid(data[side]["steps"], statuses))}</pre></figure>'
        for side, caption in (("as_is", "Current"), ("to_be", "Planned"))
    )


def _content(data, decisions):
    rows = diff(data["as_is"]["steps"], data["to_be"]["steps"])
    body = "".join(_row_html(i, row, decisions) for i, row in enumerate(rows, 1))
    return (
        '<main class="page"><header><p class="eyebrow">Flow change &middot; grill-with-docs</p>'
        f"<h1>{escape(data['title'])}</h1>"
        '<p class="lede">The current flow beside the planned one. Every difference names the decision in '
        f"<code>plan.md</code> that caused it.</p>{_summary(rows)}</header>"
        '<section aria-labelledby="steps-h"><h2 id="steps-h">Step by step</h2><div class="scroll">'
        '<table class="steps"><thead><tr><th scope="col">Step</th><th scope="col">Current</th>'
        f'<th scope="col">Planned</th><th scope="col">Decision</th></tr></thead><tbody>{body}</tbody></table>'
        '</div></section><section aria-labelledby="diagrams-h"><h2 id="diagrams-h">Diagrams</h2>'
        f'<div class="diagrams">{_diagrams(data, rows)}</div></section></main>'
    )


def render(data, decisions, standalone=False):
    """The page for a valid flow.json; `decisions` maps decision ids to their titles in plan.md.

    The default is an Artifact page body (the host adds the document skeleton and draws Mermaid);
    `standalone=True` gives a full document that loads Mermaid itself, for opening the file locally.
    """
    head = (
        f"<title>{escape(data['title'])}</title>"
        '<meta name="claude:viewport-fit-sides" content="cover">'
        f'<link rel="stylesheet" href="{escape(FONTS)}">'
        f"<style>{CSS.read_text(encoding='utf-8')}</style>"
    )
    content = _content(data, decisions)
    if not standalone:
        return head + content
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{head}</head>'
        f'<body>{content}<script src="{MERMAID_JS}"></script>'
        "<script>mermaid.initialize({startOnLoad: true, theme: "
        "matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default'});</script></body></html>"
    )


def main(argv):
    run = Path(argv[0])
    artifact = "--artifact" in argv[1:]
    try:
        data = json.loads((run / "flow.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"flow.json: not valid JSON ({error})")
        return 1
    plan = run / "plan.md"
    decisions = plan_decisions(plan.read_text(encoding="utf-8")) if plan.is_file() else None
    problems = check(data, decisions)
    if problems:
        print("\n".join(problems))
        return 1
    if "--check" in argv[1:]:
        print("OK: no problems found")
        return 0
    out = run / ("flow.artifact.html" if artifact else "flow.html")
    out.write_text(render(data, decisions or {}, standalone=not artifact), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
