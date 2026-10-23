"""check_flow.py enforces the flow page's node budget and catches grid items that mix text with inline tags."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_flow import flow_errors  # noqa: E402

GRID = "<style>.ledger li { display: grid; }</style>"


def boxes(count):
    return "".join(f'<rect x="{i * 10}" y="0" width="8" height="8" rx="6"/>' for i in range(count))


def test_node_budget_counts_rx6_boxes_once_per_geometry():
    assert flow_errors(f"<svg>{boxes(9)}{boxes(9)}</svg>") == []
    assert "svg 1 has 10 node boxes" in flow_errors(f"<svg>{boxes(10)}</svg>")[0]


def test_node_budget_counts_each_form_with_the_shared_parts():
    shared = '<rect x="0" y="100" width="8" height="8" rx="6"/>'
    page = f'<svg>{shared}<g class="form-current">{boxes(8)}</g><g class="form-planned" transform="translate(-580 0)">{boxes(9)}</g></svg>'
    assert flow_errors(page) == [
        "svg 1 form-planned has 10 node boxes; the budget is 9 (split into an overview and a detail diagram)"
    ]


def test_node_budget_skips_defs_and_hidden_svgs():
    assert flow_errors(f"<svg><defs>{boxes(12)}</defs></svg><svg aria-hidden='true'>{boxes(12)}</svg>") == []


def test_grid_item_mixing_text_and_inline_tag_fails():
    errors = flow_errors(GRID + '<ol class="ledger"><li class="added">A<sup>2</sup> b</li></ol>')
    assert errors == [
        "<li.added> is display grid and mixes text with inline elements; "
        "each inline element becomes its own row. Wrap the text in one <p>"
    ]


def test_grid_item_with_mark_and_paragraph_passes():
    page = GRID + '<ol class="ledger"><li><span class="mark">+ ADDED · D1</span><p>A<sup>2</sup> b</p></li></ol>'
    assert flow_errors(page) == []


def test_shipped_example_keeps_the_flow_rules():
    example = Path(__file__).resolve().parents[1] / "examples" / "grill-with-docs" / "flow.html"
    assert flow_errors(example.read_text(encoding="utf-8")) == []
