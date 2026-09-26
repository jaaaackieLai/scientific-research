#!/usr/bin/env python3
"""Batch-fetch basic metadata of arXiv papers for paper-search to decide G1 / G3 / G4.

Reads two web pages per paper (no PDF):
  - arxiv.org/abs/ID : title, authors, first public date, Comments field, Journal-ref, DOI, abstract
  - arxiv.org/html/ID: author block (with institutions), GitHub links in the paper (older papers may have no HTML version)

Usage:
  python arxiv_meta.py 2403.19647 2309.08600 https://arxiv.org/abs/2406.04093 > meta.json
  python arxiv_meta.py 2403.19647 | python match.py meta -

All pages are fetched concurrently, waiting at most TOTAL_TIMEOUT seconds for the whole batch; timed-out fields are marked error and do not block the batch.
"""
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, wait

PER_REQUEST_TIMEOUT = 20
TOTAL_TIMEOUT = 45
WORKERS = 6
UA = "Mozilla/5.0 (paper-search skill; metadata lookup)"

ID_RE = re.compile(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?")
GITHUB_RE = re.compile(r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
IGNORE_GITHUB_OWNERS = {"arxiv", "brucemiller"}  # links belonging to arXiv and LaTeXML themselves
FOOTNOTE_RE = re.compile(r"contribut|equal|joint first|corresponding author|core infrastructure", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=PER_REQUEST_TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # timeout, connection error
        return None, f"{type(e).__name__}: {e}"


def text_of(fragment):
    s = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(html.unescape(s).split())


def meta_tags(page, name):
    return [html.unescape(m) for m in re.findall(rf'<meta name="{name}" content="([^"]*)"', page)]


def table_cell(page, cls):
    m = re.search(rf'<td class="tablecell {cls}[^"]*">(.*?)</td>', page, re.S)
    return text_of(m.group(1)) if m else None


def github_links(*chunks):
    out = []
    for chunk in chunks:
        for owner, repo in GITHUB_RE.findall(chunk or ""):
            repo = re.sub(r"(\.git|[.,;)]+)$", "", repo)
            if owner.lower() in IGNORE_GITHUB_OWNERS or not repo:
                continue
            url = f"https://github.com/{owner}/{repo}"
            if url not in out:
                out.append(url)
    return out


def parse_abs(page):
    comments_html = re.search(r'<td class="tablecell comments[^"]*">(.*?)</td>', page, re.S)
    comments_html = comments_html.group(1) if comments_html else ""
    abstract = (meta_tags(page, "citation_abstract") or [""])[0]
    date = (meta_tags(page, "citation_date") or [""])[0].replace("/", "-")
    hrefs = " ".join(re.findall(r'href="([^"]+)"', comments_html))
    return {
        "title": (meta_tags(page, "citation_title") or [None])[0],
        "authors": meta_tags(page, "citation_author"),
        "first_submitted": date or None,
        "comments": text_of(comments_html) or None,
        "journal_ref": table_cell(page, "jref"),
        "doi": (meta_tags(page, "citation_doi") or [None])[0] or table_cell(page, "doi"),
        "abstract": abstract[:600],
        "_code_from_abs": github_links(hrefs, comments_html, abstract),
    }


def parse_html(page):
    if "ltx_authors" not in page:
        return {"html_available": False}
    i = page.find('class="ltx_authors"')
    j = page.find("ltx_abstract", i)
    block = page[i : j if j > 0 else i + 8000]
    affs = []
    for m in re.findall(r'<span class="ltx_contact ltx_role_(?:affiliation|address)">(.*?)</span>\s*</span>', block, re.S):
        for piece in re.split(r"Affiliation:", text_of(m)):
            piece = re.split(r"Email:|Correspondence to|\S+@\S+|\[", piece)[0].strip(" ,;")
            if not piece or piece.startswith((",", ":")) or FOOTNOTE_RE.search(piece):
                continue  # leftover names or footnotes like "equal contribution", not institutions
            if piece not in affs:
                affs.append(piece)
    # first page (author block + abstract) up to the first section: authors usually put their own repo here
    first_sec = page.find('class="ltx_section"', i)
    front = page[i : first_sec if first_sec > 0 else i + 20000]
    refs = page.find('class="ltx_bibliography')
    body = page[len(front) + i : refs if refs > 0 else len(page)]
    front_links = github_links(front)
    return {
        "html_available": True,
        "affiliations": affs,
        # clues when the author block lists no institution, e.g. g.harvard.edu; for reference only, not used in the G4 decision
        "email_domains": sorted({d.lower() for d in re.findall(r"@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", text_of(block))}),
        "author_block": text_of(block)[:2500],
        "_code_from_front": front_links,
        "code_links_in_paper": [u for u in github_links(body) if u not in front_links][:5],
    }


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ids = []
    for a in argv:
        m = ID_RE.search(a)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    if not ids:
        print(__doc__)
        return 1

    pool = ThreadPoolExecutor(max_workers=WORKERS)
    jobs = {}
    for i in ids:
        jobs[(i, "abs")] = pool.submit(fetch, f"https://arxiv.org/abs/{i}")
        jobs[(i, "html")] = pool.submit(fetch, f"https://arxiv.org/html/{i}")
    wait(jobs.values(), timeout=TOTAL_TIMEOUT)

    results = []
    for i in ids:
        rec = {"id": i, "url": f"https://arxiv.org/abs/{i}"}
        errors = []
        fa, fh = jobs[(i, "abs")], jobs[(i, "html")]
        if fa.done() and fa.result()[0] == 200:
            rec.update(parse_abs(fa.result()[1]))
        else:
            errors.append("abs: " + ("timeout" if not fa.done() else str(fa.result()[0] or fa.result()[1])))
        if fh.done() and fh.result()[0] == 200:
            rec.update(parse_html(fh.result()[1]))
        elif fh.done() and fh.result()[0] == 404:
            rec["html_available"] = False
        else:
            errors.append("html: " + ("timeout" if not fh.done() else str(fh.result()[0] or fh.result()[1])))
        # code_links: links from arXiv Comments, the abstract, and the paper's first page, usually the authors' own repo
        # code_links_in_paper: links elsewhere in the body, possibly citing other people's tools; confirm manually
        rec["code_links"] = github_links(" ".join(rec.pop("_code_from_abs", []) + rec.pop("_code_from_front", [])))
        rec["code_links_in_paper"] = [u for u in rec.get("code_links_in_paper", []) if u not in rec["code_links"]]
        if errors:
            rec["error"] = "; ".join(errors)
        results.append(rec)

    print(json.dumps(results, ensure_ascii=False, indent=1))
    sys.stdout.flush()
    os._exit(0)  # do not wait for unfinished connections


if __name__ == "__main__":
    main(sys.argv[1:])
