"""Behavior tests for check_run.py: the deterministic gate an idea-forge run must pass."""
import importlib.util
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_run.py"
spec = importlib.util.spec_from_file_location("check_run", SCRIPT)
check_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_run)

SCORE_DEFAULTS = {
    "Verdict": "survive", "Closest derivation": "D1.1", "Obviousness": "non_obvious_step",
    "Source credibility": "x", "Evidence": "x", "Strongest objection": "x",
}


def write(run, rel, text):
    path = run / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def problems_for(run, files):
    """Write `{relative path: text}` into the run directory and return the checker's problems."""
    for rel, text in files.items():
        write(run, rel, text)
    return check_run.check(run)


def digest(paper_id, first_public="2024-03-28"):
    return f"# Title\n\n- ID: {paper_id}\n- First public: {first_public}\n- Source: x\n\n## What this paper does\nX.\n"


def score_block(candidate="C1", **fields):
    """A `### C<n> verdict` block; keyword arguments override fields (underscores for spaces), None drops one."""
    values = {**SCORE_DEFAULTS, **{k.replace("_", " "): v for k, v in fields.items()}}
    lines = "".join(f"- **{label}:** {value}\n" for label, value in values.items() if value is not None)
    return f"### {candidate} verdict\n{lines}"


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


def valid_run(run):
    write(run, "problem.md", "# P\n\n## Challenge\nC.\n\n## Problem definition\nD.\n\n## Cutoff\n2026-01-01\n")
    for paper_id, date in (("2403.19647", "2024-03-28"), ("2309.08600", "2023-09-15"),
                           ("ref-silver-2017-alphazero", "2017-12-05")):
        write(run, f"papers/{paper_id}.md", digest(paper_id, date))
    write(run, "gaps.md",
          "## Axis: credit assignment\n\n### What has been done\nA [2403.19647].\n\n### Open gaps on this axis\n\n"
          "#### G1 — late failure\n- **Gap:** X via Y leaves Z.\n"
          "- **Near-miss methods:** [2403.19647] — close; [2309.08600] — close.\n"
          "- **Methodological deficiency:** credit-assignment flaw — reason.\n"
          "- **Why it matters:** unlocks W.\n- **Evidence route:** compare V.\n")
    write(run, "derivations.md",
          "## Gap: G1\n\n### D1.1 — reweight steps\n- **Central mechanism:** reweight.\n"
          "- **Derivation steps:** 1) a 2) b\n- **References used:** [2403.19647] — weights\n"
          "- **Key assumption:** stable.\n")
    write(run, "candidates.md",
          "### C1 — value backup\n- **Intuition:** back up value.\n- **Gap it attacks:** G1 — late failure.\n"
          "- **Source inspiration:** [ref-silver-2017-alphazero] — tree backup. "
          "Novelty type: recombination of distant concepts.\n"
          "- **How it maps to this problem:** states are partial programs.\n- **Why it could work:** evaluable states.\n"
          "- **Novelty vs. closest in-domain work:** [2403.19647] — differs.\n- **Main risk:** noisy values.\n")
    write(run, "scores.md", score_block(
        Source_credibility="[ref-silver-2017-alphazero] venue=pass",
        Evidence="\n  - [2309.08600] does not back up value."))
    sections = "".join(f"## {name}\nText [2403.19647].\n\n" for name in check_run.PROPOSAL_SECTIONS)
    write(run, "proposal.md", f"{check_run.NOTICE}\n\n# Title\n\n{sections}")


# Citations


def test_citation_without_digest_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"gaps.md": "Prior work [2403.19647] uses X.\n"})

    assert any("gaps.md:1" in p and "2403.19647" in p for p in problems)


def test_ref_and_old_style_ids_are_checked(tmp_path):
    problems = problems_for(tmp_path, {"gaps.md": "See [ref-vaswani-2017-attention] and [hep-th_9901001].\n"})

    assert any("ref-vaswani-2017-attention" in p for p in problems)
    assert any("hep-th_9901001" in p for p in problems)


def test_versioned_citation_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"gaps.md": "See [2403.19647v2].\n"})

    assert any("gaps.md:1" in p and "2403.19647v2" in p and "version" in p for p in problems)


def test_cited_paper_after_problem_cutoff_is_reported(tmp_path):
    problems = problems_for(tmp_path, {
        "problem.md": "# P\n\n## Challenge\nC\n\n## Problem definition\nD\n\n## Cutoff\n2026-01-01\n",
        "papers/2601.00001.md": digest("2601.00001", "2026-01-05"),
        "papers/2403.19647.md": digest("2403.19647", "2024-03-28"),
        "gaps.md": "A [2601.00001] and B [2403.19647].\n",
    })

    assert any("2601.00001" in p and "cutoff" in p for p in problems)
    assert not any("2403.19647" in p for p in problems)


def test_cited_paper_without_date_under_cutoff_is_reported(tmp_path):
    problems = problems_for(tmp_path, {
        "problem.md": "# P\n\n## Cutoff\n2026-01-01\n",
        "papers/2403.19647.md": "# Title\n\n- ID: 2403.19647\n",
        "gaps.md": "A [2403.19647].\n",
    })

    assert any("2403.19647" in p and "First public" in p for p in problems)


def test_first_public_date_must_match_arxiv_id_month(tmp_path):
    problems = problems_for(tmp_path, {
        "papers/2403.19647.md": digest("2403.19647", "2026-03-01"),
        "gaps.md": "A [2403.19647].\n",
    })

    assert any("2403.19647" in p and "2024-03" in p for p in problems)


# gaps.md and derivations.md


def test_gap_missing_required_field_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"gaps.md": "## Axis: a\n\n#### G1 — g\n- **Gap:** x\n"})

    assert any("gaps.md:3" in p and "G1" in p and "Evidence route" in p for p in problems)


def test_axis_with_more_than_two_gaps_is_reported(tmp_path):
    gaps = "".join(f"#### G{n} — g\n- **Gap:** x\n\n" for n in range(1, 4))
    problems = problems_for(tmp_path, {"gaps.md": f"## Axis: a\n\n### Open gaps on this axis\n\n{gaps}"})

    assert any("gaps.md:1" in p and "Axis" in p and "3 gaps" in p for p in problems)


def test_gap_with_more_than_three_derivations_is_reported(tmp_path):
    body = "".join(f"### D1.{k} — m\n" for k in range(1, 5))
    problems = problems_for(tmp_path, {"derivations.md": f"## Gap: G1\n\n{body}"})

    assert any("derivations.md:1" in p and "4 derivations" in p for p in problems)


def test_derivation_missing_field_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"derivations.md": "## Gap: G1\n\n### D1.1 — m\n- **Central mechanism:** x\n"})

    assert any("derivations.md:3" in p and "D1.1" in p and "Key assumption" in p for p in problems)


# candidates.md


def test_candidate_missing_required_field_is_reported(tmp_path):
    problems = problems_for(tmp_path, {
        "candidates.md": "### C1 — idea\n- **Intuition:** do X.\n- **Gap it attacks:** G1 — fails.\n"})

    assert any("candidates.md:1" in p and "C1" in p and "Main risk" in p for p in problems)


def test_candidate_attacking_unknown_gap_is_reported(tmp_path):
    problems = problems_for(tmp_path, {
        "gaps.md": "## Axis: a\n\n### Open gaps on this axis\n\n#### G1 — g\n- **Gap:** x\n",
        "candidates.md": "### C1 — idea\n- **Gap it attacks:** G9 — fails.\n",
    })

    assert any("candidates.md:1" in p and "G9" in p for p in problems)


# scores.md


def test_invalid_verdict_and_obviousness_are_reported(tmp_path):
    problems = problems_for(tmp_path, {"scores.md": score_block(Verdict="accept", Obviousness="novel")})

    assert any("scores.md:1" in p and "Verdict" in p and "accept" in p for p in problems)
    assert any("scores.md:1" in p and "Obviousness" in p and "novel" in p for p in problems)


def test_field_value_on_following_lines_counts_as_filled(tmp_path):
    problems = problems_for(tmp_path, {"scores.md": score_block(Evidence="\n  - point one\n  - point two")})

    assert not any("Evidence" in p for p in problems)


def test_verdict_for_unknown_candidate_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"scores.md": score_block("C9")})

    assert any("scores.md:1" in p and "C9" in p and "candidates.md" in p for p in problems)


def test_unscored_needs_closest_derivation_none(tmp_path):
    problems = problems_for(tmp_path, {"scores.md": score_block(Obviousness="unscored")})

    assert any("scores.md:1" in p and "unscored" in p and "NONE" in p for p in problems)


# proposal.md


def test_proposal_without_notice_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"proposal.md": "# Title\n\n## One-sentence thesis\nX.\n"})

    assert any("proposal.md:1" in p and "notice" in p for p in problems)


def test_proposal_missing_or_empty_section_is_reported(tmp_path):
    problems = problems_for(tmp_path, {
        "proposal.md": f"{check_run.NOTICE}\n\n# Title\n\n## One-sentence thesis\n\n## Method\nX.\n"})

    assert any("One-sentence thesis" in p and "empty" in p for p in problems)
    assert any("Falsifiable predictions" in p and "missing" in p for p in problems)
    assert not any("## Method" in p for p in problems)


def test_proposal_section_with_only_subheadings_is_not_empty(tmp_path):
    problems = problems_for(tmp_path, {
        "proposal.md": f"{check_run.NOTICE}\n\n# Title\n\n## Method\n### Flow\nA -> B.\n"})

    assert not any("## Method" in p for p in problems)


def test_proposal_todo_placeholder_is_reported(tmp_path):
    problems = problems_for(tmp_path, {"proposal.md": f"{check_run.NOTICE}\n\n# Title\n\n## Method\n[TODO: fill]\n"})

    assert any("proposal.md:6" in p and "TODO" in p for p in problems)


# Whole run and CLI


def test_valid_run_has_no_problems(tmp_path):
    valid_run(tmp_path)

    assert check_run.check(tmp_path) == []


def test_cli_exit_codes(tmp_path):
    valid_run(tmp_path)
    ok = run_cli(tmp_path)
    (tmp_path / "papers" / "2309.08600.md").unlink()
    bad = run_cli(tmp_path)

    assert ok.returncode == 0, ok.stdout
    assert ok.stdout.startswith("OK")
    assert bad.returncode == 1
    assert "2309.08600" in bad.stdout


def test_cli_rejects_directory_without_problem_file(tmp_path):
    result = run_cli(tmp_path)

    assert result.returncode == 1
    assert "problem.md" in result.stdout


def test_cli_without_arguments_prints_usage():
    result = run_cli()

    assert result.returncode == 2
    assert "usage" in result.stderr.lower()
