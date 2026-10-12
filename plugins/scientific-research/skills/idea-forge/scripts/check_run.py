#!/usr/bin/env python3
"""Deterministic gate for an idea-forge run directory.

Usage:
  python check_run.py docs/ideas/<slug>

Prints one line per problem as `<file>:<line>: <message>` and exits 1 if there are any;
prints `OK: no problems found` and exits 0 otherwise.
"""
import re
import sys
from pathlib import Path

ARTIFACTS = ("gaps.md", "candidates.md", "derivations.md", "scores.md", "proposal.md")
CITATION_RE = re.compile(r"\[(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?_\d{7}|ref-[a-z0-9-]+)\]")
ARXIV_MONTH_RE = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")
VERSIONED_RE = re.compile(r"\[(\d{4}\.\d{4,5}v\d+)\]")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
FIRST_PUBLIC_RE = re.compile(r"^- First public:\s*(\d{4}-\d{2}-\d{2})", re.M)
FIELD_RE = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
AXIS_RE = re.compile(r"^## (Axis: .+?)\s*$")
GAP_RE = re.compile(r"^#### (G\d+)\s+[—-]\s+\S")
GAP_FIELDS = ("Gap", "Near-miss methods", "Methodological deficiency", "Why it matters", "Evidence route")
GAP_ID_RE = re.compile(r"^(G\d+)\b")
DERIVATION_GAP_RE = re.compile(r"^## Gap: (G\d+)\s*$")
DERIVATION_RE = re.compile(r"^### (D\d+\.\d+)\s+[—-]\s+\S")
DERIVATION_FIELDS = ("Central mechanism", "Derivation steps", "References used", "Key assumption")
CANDIDATE_RE = re.compile(r"^### (C\d+)\s+[—-]\s+\S")
CANDIDATE_FIELDS = (
    "Intuition", "Gap it attacks", "Source inspiration", "How it maps to this problem",
    "Why it could work", "Novelty vs. closest in-domain work", "Main risk",
)
SCORE_RE = re.compile(r"^### (C\d+) verdict\s*$")
SCORE_FIELDS = ("Verdict", "Closest derivation", "Obviousness", "Source credibility", "Evidence", "Strongest objection")
SCORE_VALUES = {
    "Verdict": re.compile(
        r"^(survive|revise\(focus=(novelty|grounding|mapping|feasibility|clarity|coherence)\)|reject\(reason=.+\))$"),
    "Closest derivation": re.compile(r"^(D\d+\.\d+|NONE)$"),
    "Obviousness": re.compile(r"^(trivial_combination|routine_extension|non_obvious_step|surprising|unscored)$"),
}
NOTICE = "以下研究構想為 AI 生成，新穎性與可行性未經實驗驗證；引用、主張與是否已有人做過，請自行查證後再使用。"

PROPOSAL_SECTIONS = (
    "One-sentence thesis", "Core problem", "Key novelty", "Problem definition", "Key terms", "Related work",
    "Method", "Model and training", "Comparison to prior work", "Proposed evaluation", "Falsifiable predictions",
    "Limitations", "Provenance",
)


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def section(text, heading):
    """Body of the section under the exact `heading` line, up to the next heading of the same or a higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    match = re.search(rf"^{re.escape(heading)}[ \t]*\n(.*?)(?=^#{{1,{level}}} |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else ""


def problem_cutoff(run_dir):
    match = DATE_RE.search(section(read(run_dir / "problem.md"), "## Cutoff"))
    return match.group(0) if match else None


def blocks(text, heading_re):
    """(line number, id, {field label: value}) for each block whose heading matches; a block ends at the next heading.

    A field's value is the text after its label plus any indented lines below it."""
    found, current, label = [], None, None
    for lineno, line in enumerate(text.splitlines(), 1):
        heading = heading_re.match(line)
        if heading or line.startswith("#"):
            current, label = ((lineno, heading.group(1), {}) if heading else None), None
            if current:
                found.append(current)
            continue
        if not current:
            continue
        field = FIELD_RE.match(line)
        if field:
            label = field.group(1)
            current[2][label] = field.group(2).strip()
        elif label and line[:1].isspace() and line.strip():
            current[2][label] = f"{current[2][label]} {line.strip()}".strip()
    return found


def missing_fields(name, found, required):
    return [
        f"{name}:{lineno}: {block_id} is missing **{label}:**"
        for lineno, block_id, fields in found
        for label in required
        if not fields.get(label)
    ]


def too_many(name, text, parent_re, child_re, limit, kind):
    """Each parent section (e.g. an axis) may hold at most `limit` child blocks (e.g. gaps)."""
    sections = []
    for lineno, line in enumerate(text.splitlines(), 1):
        parent = parent_re.match(line)
        if parent:
            sections.append([lineno, parent.group(1), 0])
        elif sections and child_re.match(line):
            sections[-1][2] += 1
    return [
        f"{name}:{lineno}: {label} has {count} {kind}, at most {limit} allowed"
        for lineno, label, count in sections
        if count > limit
    ]


def unknown_references(name, found, label, id_re, known, kind):
    problems = []
    for lineno, block_id, fields in found:
        match = id_re.match(fields.get(label, ""))
        if match and match.group(1) not in known:
            problems.append(f"{name}:{lineno}: {block_id} refers to {match.group(1)}, which is not a {kind}")
    return problems


def invalid_values(name, found, patterns):
    return [
        f"{name}:{lineno}: {block_id} has **{label}:** `{fields[label]}`, which is not an allowed value"
        for lineno, block_id, fields in found
        for label, pattern in patterns.items()
        if fields.get(label) and not pattern.match(fields[label])
    ]


def check_proposal(text):
    if not text:
        return []
    problems = []
    if text.splitlines()[0].strip() != NOTICE:
        problems.append("proposal.md:1: the first line must be the AI-generation notice from references/artifacts.md")
    for name in PROPOSAL_SECTIONS:
        heading = f"## {name}"
        if not re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.M):
            problems.append(f"proposal.md: section `{heading}` is missing")
        elif not section(text, heading):
            problems.append(f"proposal.md: section `{heading}` is empty")
    problems += [
        f"proposal.md:{lineno}: TODO placeholder"
        for lineno, line in enumerate(text.splitlines(), 1)
        if "TODO" in line
    ]
    return problems


def check_citation(run_dir, paper_id, cutoff):
    digest_text = read(run_dir / "papers" / f"{paper_id}.md")
    if not digest_text:
        return f"[{paper_id}] has no digest papers/{paper_id}.md"
    match = FIRST_PUBLIC_RE.search(digest_text)
    first_public = match.group(1) if match else None
    id_month = ARXIV_MONTH_RE.match(paper_id)
    if first_public and id_month:
        expected = f"20{id_month.group(1)}-{id_month.group(2)}"
        if not first_public.startswith(expected):
            return (f"[{paper_id}] First public {first_public} does not match the id's submission month "
                    f"{expected}; use the v1 date")
    if cutoff and not first_public:
        return f"[{paper_id}] digest has no First public date to compare with the cutoff {cutoff}"
    if cutoff and first_public >= cutoff:
        return f"[{paper_id}] first public {first_public} is not before the cutoff {cutoff}"
    return None


def check_citations(run_dir, cutoff):
    problems = []
    for name in ARTIFACTS:
        for lineno, line in enumerate(read(run_dir / name).splitlines(), 1):
            for paper_id in CITATION_RE.findall(line):
                problem = check_citation(run_dir, paper_id, cutoff)
                if problem:
                    problems.append(f"{name}:{lineno}: {problem}")
            for versioned in VERSIONED_RE.findall(line):
                problems.append(f"{name}:{lineno}: [{versioned}] cite the id without its version")
    return problems


def check_scores(scores, candidates):
    problems = missing_fields("scores.md", scores, SCORE_FIELDS)
    problems += invalid_values("scores.md", scores, SCORE_VALUES)
    problems += [
        f"scores.md:{lineno}: {block_id} is unscored, so **Closest derivation:** must be NONE"
        for lineno, block_id, fields in scores
        if fields.get("Obviousness") == "unscored" and fields.get("Closest derivation") != "NONE"
    ]
    known_candidates = {c[1] for c in candidates}
    problems += [
        f"scores.md:{lineno}: {block_id} verdict has no matching candidate in candidates.md"
        for lineno, block_id, _ in scores
        if block_id not in known_candidates
    ]
    return problems


def check(run_dir):
    run_dir = Path(run_dir)
    problems = []
    if not (run_dir / "problem.md").is_file():
        problems.append("problem.md: missing; is this an idea-forge run directory?")
    problems += check_citations(run_dir, problem_cutoff(run_dir))

    gaps_text = read(run_dir / "gaps.md")
    gaps = blocks(gaps_text, GAP_RE)
    problems += too_many("gaps.md", gaps_text, AXIS_RE, GAP_RE, 2, "gaps")
    problems += missing_fields("gaps.md", gaps, GAP_FIELDS)

    derivations_text = read(run_dir / "derivations.md")
    problems += too_many("derivations.md", derivations_text, DERIVATION_GAP_RE, DERIVATION_RE, 3, "derivations")
    problems += missing_fields("derivations.md", blocks(derivations_text, DERIVATION_RE), DERIVATION_FIELDS)

    candidates = blocks(read(run_dir / "candidates.md"), CANDIDATE_RE)
    problems += missing_fields("candidates.md", candidates, CANDIDATE_FIELDS)
    problems += unknown_references(
        "candidates.md", candidates, "Gap it attacks", GAP_ID_RE, {g[1] for g in gaps}, "gap in gaps.md")

    problems += check_scores(blocks(read(run_dir / "scores.md"), SCORE_RE), candidates)
    problems += check_proposal(read(run_dir / "proposal.md"))
    return problems


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: check_run.py <run directory, e.g. docs/ideas/<slug>>", file=sys.stderr)
        return 2
    problems = check(Path(args[0]))
    for problem in problems:
        print(problem)
    if not problems:
        print("OK: no problems found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
