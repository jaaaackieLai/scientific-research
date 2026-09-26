#!/usr/bin/env python3
"""Check whether the publication venue (G1) and author institutions (G4) are on the whitelist.

The lists are read directly from the tables in references/venues.md and references/institutions.md;
references/aliases.json only adds aliases and easily confused similar names.

Usage:
  python match.py venue "Accepted to CVPR 2024" "NeurIPS 2023 Workshop"
  python match.py inst "Northeastern University; MIT" "Technion"
  python match.py meta meta.json        # read arxiv_meta.py output and decide G1 / G4 per paper
  python arxiv_meta.py 2403.19647 | python match.py meta -
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "references"


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s):
    """Lowercase, strip accents, turn non-alphanumeric characters into spaces, and pad with spaces for whole-word matching."""
    s = strip_accents(s).lower()
    s = re.sub(r"[^0-9a-z一-鿿]+", " ", s)
    return " " + " ".join(s.split()) + " "


def md_rows(path, first_header):
    """Return all data rows of markdown tables whose first column header is first_header."""
    rows, active = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            active = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == first_header:
            active = True
            continue
        if active and not set(cells[0]) <= set("-: "):
            rows.append(cells)
    return rows


def auto_aliases(cell):
    """Derive aliases from a table name: drop bracketed notes, split out abbreviations in parentheses and slash-separated names."""
    base = re.sub(r"\[.*?\]", "", cell).strip()
    out = []
    for part in base.split(" / "):
        m = re.match(r"^(.*?)\s*\((.*?)\)\s*$", part)
        names = [m.group(1), m.group(2)] if m else [part]
        for n in names:
            n = n.strip()
            if n:
                out.append(n)
                if n.lower().startswith("the "):
                    out.append(n[4:])
    return out


class Entry:
    def __init__(self, name, aliases, exclude=(), drop=(), **info):
        self.name, self.info = name, info
        drop = set(drop)
        seen, self.aliases = set(), []
        for a in aliases:
            if a and a not in drop and a not in seen:
                seen.add(a)
                self.aliases.append(a)
        self.exclude = [re.compile(re.escape(strip_accents(e)), re.I) for e in exclude]

    def hit(self, text):
        raw = strip_accents(text)
        for ex in self.exclude:
            raw = ex.sub(" ## ", raw)
        n = norm(raw)
        for a in self.aliases:
            if len(a) <= 5:  # short abbreviation: case-sensitive, whole-word match
                if re.search(r"(?<![A-Za-z0-9])" + re.escape(strip_accents(a)) + r"(?![A-Za-z0-9])", raw):
                    return a
            elif norm(a) in n:
                return a
        return None


def load():
    extra = json.loads((REF / "aliases.json").read_text(encoding="utf-8"))
    venues = []
    for abbr, full, kind in md_rows(REF / "venues.md", "Abbreviation"):
        x = extra["venues"].get(abbr, {})
        venues.append(Entry(abbr, [abbr, full] + x.get("aliases", []), x.get("exclude", []), x.get("drop", []), full=full, type=kind))
    insts = []
    for country, name, qs in md_rows(REF / "institutions.md", "Country/Region"):
        x = extra["institutions"].get(name, {})
        insts.append(Entry(name, auto_aliases(name) + x.get("aliases", []), x.get("exclude", []), x.get("drop", []), country=country, qs=qs))
    missing = (set(extra["institutions"]) - {e.name for e in insts}) | (set(extra["venues"]) - {e.name for e in venues})
    if missing:
        print(f"[warn] aliases.json has keys not found in the lists: {sorted(missing)}", file=sys.stderr)
    return venues, insts, extra["venue_exclude"]


VENUES, INSTS, VENUE_EXCLUDE = load()


def match_venue(text):
    """Match clause by clause. When a clause contains words such as workshop, findings, or under review, its hits are listed as excluded."""
    accepted, excluded = [], []
    for clause in re.split(r"[;\n|]|\.\s", text or ""):
        hits = [v.name for v in VENUES if v.hit(clause)]
        if not hits:
            continue
        low = clause.lower()
        reasons = [r for k, r in VENUE_EXCLUDE.items() if k in low]
        for h in hits:
            (excluded if reasons else accepted).append({"venue": h, "clause": clause.strip(), **({"reason": reasons} if reasons else {})})
    return {"accepted": accepted, "excluded": excluded}


def match_inst(text):
    found = []
    for e in INSTS:
        a = e.hit(text or "")
        if a:
            found.append({"name": e.name, "country": e.info["country"], "qs": e.info["qs"], "matched_on": a})
    return found


def judge_meta(p):
    if "error" in p and "title" not in p:
        return {"id": p.get("id"), "error": p["error"]}
    venue_text = "\n".join(x for x in [p.get("journal_ref"), p.get("comments")] if x)
    v = match_venue(venue_text)
    if v["accepted"]:
        g1 = "pass"
    elif v["excluded"]:
        g1 = "fail: only excluded venues (" + ", ".join(x["venue"] for x in v["excluded"]) + "); still search for another formal version"
    else:
        g1 = "unknown: the arXiv page states no accepted venue; search for a formal version"
    inst_text = "\n".join(p.get("affiliations") or []) + "\n" + (p.get("author_block") or "")
    insts = match_inst(inst_text) if inst_text.strip() else []
    if insts:
        g4 = "pass"
    elif p.get("affiliations"):
        g4 = "fail: none of the institutions in the author block are in the table (check affiliations for missed matches)"
    else:
        g4 = "unknown: no HTML version or the author block lists no institutions; check the paper's first page or the authors' personal pages"
    return {
        "id": p.get("id"),
        "title": p.get("title"),
        "first_submitted": p.get("first_submitted"),
        "G1": g1,
        "venues": v,
        "G4": g4,
        "institutions": insts,
        "affiliations": p.get("affiliations"),
        "code_links": p.get("code_links"),
        "code_links_in_paper": p.get("code_links_in_paper"),
    }


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) < 2 or argv[0] not in {"venue", "inst", "meta"}:
        print(__doc__)
        return 1
    cmd, args = argv[0], argv[1:]
    if cmd == "venue":
        out = [{"input": t, **match_venue(t)} for t in args]
    elif cmd == "inst":
        out = [{"input": t, "matches": match_inst(t)} for t in args]
    else:
        raw = sys.stdin.buffer.read().decode("utf-8") if args[0] == "-" else Path(args[0]).read_text(encoding="utf-8")
        out = [judge_meta(p) for p in json.loads(raw)]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
