"""The worked example in examples/ is a valid session: its flow traces every difference to a plan decision."""
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
EXAMPLE = SKILL_DIR / "examples" / "grill-with-docs"


def test_example_session_passes_the_flow_check():
    result = subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / "render_flow.py"), str(EXAMPLE), "--check"],
        capture_output=True, text=True,
    )

    assert result.returncode == 0, result.stdout
    assert {"plan.md", "flow.json", "flow.svg", "review-1.md"} <= {p.name for p in EXAMPLE.iterdir()}
