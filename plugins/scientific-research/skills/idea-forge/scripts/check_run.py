#!/usr/bin/env python3
"""Deterministic gate for an idea-forge run directory.

Usage:
  python check_run.py docs/ideas/<slug>

Prints one line per problem as `<file>:<line>: <message>` and exits 1 if there are any;
prints `OK: no problems found` and exits 0 otherwise.
"""
import re
import sys
from collections import namedtuple
from pathlib import Path

CITATION_RE = re.compile(r"\[(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?_\d{7}|ref-[a-z0-9-]+)\]")
VERSIONED_RE = re.compile(r"\[(\d{4}\.\d{4,5}v\d+)\]")
ARXIV_MONTH_RE = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
FIRST_PUBLIC_RE = re.compile(r"^- First public:\s*(\d{4}-\d{2}-\d{2})", re.M)
FIELD_RE = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
BLOCK_ID_RE = re.compile(r"^([CDG]\d+(?:\.\d+)?)\b")

# One entry per block-structured artifact, mirroring references/artifacts.md.
#   heading: regex of a block heading, group 1 is the block id
#   fields:  required `- **Label:**` fields
#   parent:  (regex of a parent section, most blocks allowed under it, artifact the parent id must be in or None)
#   values:  {label: regex the value must match}
#   refs:    {label: artifact whose block ids the value must start with}
#   id_in:   artifact whose block ids this block's own id must be one of
Spec = namedtuple("Spec", "heading fields parent values refs id_in", defaults=(None, {}, {}, None))
SPECS = {
    "gaps.md": Spec(
        heading=re.compile(r"^#### (G\d+)\s+[—-]\s+\S"),
        fields=("Gap", "Near-miss methods", "Methodological deficiency", "Why it matters", "Evidence route"),
        parent=(re.compile(r"^## (Axis: .+?)\s*$"), 2, None),
        values={
            "Methodological deficiency": re.compile(
                r"^(missing mechanism|algorithmic limitation|wrong inductive bias|credit-assignment flaw"
                r"|training-objective mismatch|representation limitation|scalability limit|other: [^—]+?) — \S"),
        },
    ),
    "derivations.md": Spec(
        heading=re.compile(r"^### (D\d+\.\d+)\s+[—-]\s+\S"),
        fields=("Central mechanism", "Derivation steps", "References used", "Key assumption"),
        parent=(re.compile(r"^## Gap: (G\d+)\s*$"), 3, "gaps.md"),
    ),
    "candidates.md": Spec(
        heading=re.compile(r"^### (C\d+)\s+[—-]\s+\S"),
        fields=(
            "Intuition", "Gap it attacks", "Source inspiration", "How it maps to this problem",
            "Why it could work", "Novelty vs. closest in-domain work", "Main risk",
        ),
        refs={"Gap it attacks": "gaps.md"},
    ),
    "scores.md": Spec(
        heading=re.compile(r"^### (C\d+) verdict\s*$"),
        fields=("Verdict", "Closest derivation", "Obviousness", "Source credibility", "Evidence",
                "Strongest objection"),
        values={
            "Verdict": re.compile(
                r"^(survive|revise\(focus=(novelty|grounding|mapping|feasibility|clarity|coherence)\)"
                r"|reject\(reason=.+\))$"),
            "Closest derivation": re.compile(r"^(D\d+\.\d+|NONE)$"),
            "Obviousness": re.compile(
                r"^(trivial_combination|routine_extension|non_obvious_step|surprising|unscored)$"),
        },
        id_in="candidates.md",
    ),
}
ARTIFACTS = (*SPECS, "proposal.md")
NOTICE = "以下研究構想為 AI 生成，新穎性與可行性未經實驗驗證；引用、主張與是否已有人做過，請自行查證後再使用。"
PROPOSAL_SECTIONS = (
    "One-sentence thesis", "Core problem", "Key novelty", "Problem definition", "Key terms", "Related work",
    "Method", "Model and training", "Comparison to prior work", "Proposed evaluation", "Falsifiable predictions",
    "Limitations", "Provenance",
)

Block = namedtuple("Block", "lineno id fields")


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def section(text, heading):
    """Body of the section under the exact `heading` line, up to the next heading of the same or a higher level.

    None when the heading is absent."""
    level = len(heading) - len(heading.lstrip("#"))
    match = re.search(rf"^{re.escape(heading)}[ \t]*\n?(.*?)(?=^#{{1,{level}}} |\Z)", text, re.M | re.S)
    return match.group(1).strip() if match else None


def problem_cutoff(run_dir):
    match = DATE_RE.search(section(read(run_dir / "problem.md"), "## Cutoff") or "")
    return match.group(0) if match else None


def blocks(text, heading_re):
    """Each block whose heading matches; a block ends at the next heading.

    A field's value is the text after its label plus any indented lines below it."""
    found, current, label = [], None, None
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("#"):
            heading = heading_re.match(line)
            current, label = (Block(lineno, heading.group(1), {}) if heading else None), None
            if current:
                found.append(current)
            continue
        if not current:
            continue
        field = FIELD_RE.match(line)
        if field:
            label = field.group(1)
            current.fields[label] = field.group(2).strip()
        elif label and line[:1].isspace() and line.strip():
            current.fields[label] = f"{current.fields[label]} {line.strip()}".strip()
    return found


def children(text, parent_re, heading_re):
    """[line number, parent id, [child block ids]] for each parent section (e.g. an axis and its gaps)."""
    sections = []
    for lineno, line in enumerate(text.splitlines(), 1):
        parent = parent_re.match(line)
        child = heading_re.match(line)
        if parent:
            sections.append((lineno, parent.group(1), []))
        elif sections and child:
            sections[-1][2].append(child.group(1))
    return sections


def check_parents(name, text, parent, heading_re, ids):
    """Each parent section (e.g. an axis) holds at most `limit` blocks (e.g. gaps) and names a known id."""
    parent_re, limit, parent_in = parent
    problems = []
    for lineno, label, children_ids in children(text, parent_re, heading_re):
        if len(children_ids) > limit:
            problems.append(
                f"{name}:{lineno}: {label} has {len(children_ids)} {Path(name).stem}, at most {limit} allowed")
        if parent_in and label not in ids[parent_in]:
            problems.append(f"{name}:{lineno}: {label} is not in {parent_in}")
    return problems


def check_blocks(name, text, spec, parsed):
    ids = {artifact: {b.id for b in found} for artifact, found in parsed.items()}
    problems = check_parents(name, text, spec.parent, spec.heading, ids) if spec.parent else []
    for block in parsed[name]:
        where = f"{name}:{block.lineno}: {block.id}"
        for label in spec.fields:
            value = block.fields.get(label)
            if not value:
                problems.append(f"{where} is missing **{label}:**")
            elif label in spec.values and not spec.values[label].match(value):
                problems.append(f"{where} has **{label}:** `{value}`, which is not an allowed value")
            elif label in spec.refs:
                match = BLOCK_ID_RE.match(value)
                if match and match.group(1) not in ids[spec.refs[label]]:
                    problems.append(f"{where} refers to {match.group(1)}, which is not in {spec.refs[label]}")
        if spec.id_in and block.id not in ids[spec.id_in]:
            problems.append(f"{where} has no matching block in {spec.id_in}")
    return problems


def check_scores(scores, candidates, derivations_text):
    """A verdict's obviousness must agree with the frozen derivations of the gap its candidate attacks."""
    spec = SPECS["derivations.md"]
    derived = {gap: ids for _, gap, ids in children(derivations_text, spec.parent[0], spec.heading)}
    gap_of = {}
    for c in candidates:
        match = BLOCK_ID_RE.match(c.fields.get("Gap it attacks", ""))
        if match:
            gap_of[c.id] = match.group(1)
    problems = []
    for b in scores:
        where = f"scores.md:{b.lineno}: {b.id}"
        obviousness = b.fields.get("Obviousness")
        if obviousness == "unscored" and b.fields.get("Closest derivation") != "NONE":
            problems.append(f"{where} is unscored, so **Closest derivation:** must be NONE")
        gap = gap_of.get(b.id)
        if gap and not derived.get(gap) and obviousness and obviousness != "unscored":
            problems.append(f"{where} attacks {gap}, which has no derivations, so **Obviousness:** must be unscored")
        closest = b.fields.get("Closest derivation")
        if gap and closest not in (None, "", "NONE") and closest not in derived.get(gap, []):
            problems.append(f"{where} names {closest}, which is not a derivation of {gap}")
        if gap and derived.get(gap) and obviousness == "unscored":
            problems.append(f"{where} is unscored, but {gap} has derivations to compare against: "
                            f"{', '.join(derived[gap])}")
    return problems


def check_proposal(text):
    if not text:
        return []
    problems = []
    if text.splitlines()[0].strip() != NOTICE:
        problems.append("proposal.md:1: the first line must be the AI-generation notice from references/artifacts.md")
    for name in PROPOSAL_SECTIONS:
        body = section(text, f"## {name}")
        if body is None:
            problems.append(f"proposal.md: section `## {name}` is missing")
        elif not body:
            problems.append(f"proposal.md: section `## {name}` is empty")
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


def check_citations(run_dir, texts, cutoff):
    problems, verdicts = [], {}
    for name, text in texts.items():
        for lineno, line in enumerate(text.splitlines(), 1):
            for paper_id in CITATION_RE.findall(line):
                if paper_id not in verdicts:
                    verdicts[paper_id] = check_citation(run_dir, paper_id, cutoff)
                if verdicts[paper_id]:
                    problems.append(f"{name}:{lineno}: {verdicts[paper_id]}")
            for versioned in VERSIONED_RE.findall(line):
                problems.append(f"{name}:{lineno}: [{versioned}] cite the id without its version")
    return problems


def check(run_dir):
    run_dir = Path(run_dir)
    texts = {name: read(run_dir / name) for name in ARTIFACTS}
    parsed = {name: blocks(texts[name], spec.heading) for name, spec in SPECS.items()}
    problems = []
    if not (run_dir / "problem.md").is_file():
        problems.append("problem.md: missing; is this an idea-forge run directory?")
    problems += check_citations(run_dir, texts, problem_cutoff(run_dir))
    for name, spec in SPECS.items():
        problems += check_blocks(name, texts[name], spec, parsed)
    problems += check_scores(parsed["scores.md"], parsed["candidates.md"], texts["derivations.md"])
    problems += check_proposal(texts["proposal.md"])
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
