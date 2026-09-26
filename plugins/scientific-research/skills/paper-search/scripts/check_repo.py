#!/usr/bin/env python3
"""Batch-check GitHub repos for paper-search to decide G3 (whether code exists).

For each repo, reports: whether it exists, owner, description, last update time, whether archived, root directory files,
and whether the root has a README, environment files (requirements.txt, environment.yml, etc.), and training or run scripts.

Usage:
  python check_repo.py saprmarks/feature-circuits https://github.com/openai/sparse_autoencoder

Uses the GitHub API first (2 requests per repo). Without a token GitHub allows only 60 requests per hour;
set the environment variable GITHUB_TOKEN or GH_TOKEN to raise the limit. When the API quota runs out, falls back to reading the repo web page,
which can only confirm existence and root file names.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, wait

PER_REQUEST_TIMEOUT = 20
TOTAL_TIMEOUT = 45
WORKERS = 8
REPO_RE = re.compile(r"(?:github\.com/)?([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?/?$")
ENV_FILES = re.compile(r"^(requirements.*\.txt|environment.*\.ya?ml|setup\.py|setup\.cfg|pyproject\.toml|Pipfile|Dockerfile|conda.*\.ya?ml)$", re.I)
RUN_FILES = re.compile(r"(train|run|main|eval|demo|inference|reproduce).*\.(py|sh|ipynb)$|\.ipynb$|^(scripts?|configs?|notebooks?)$", re.I)


def get(url, api):
    headers = {"User-Agent": "paper-search-skill"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=PER_REQUEST_TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", dict(e.headers or {})
    except Exception as e:
        return None, f"{type(e).__name__}: {e}", {}


def summarize_files(names):
    return {
        "has_readme": any(n.lower().startswith("readme") for n in names),
        "env_files": [n for n in names if ENV_FILES.match(n)],
        "run_files": [n for n in names if RUN_FILES.search(n)][:10],
    }


def check(owner, repo):
    base = {"repo": f"{owner}/{repo}", "url": f"https://github.com/{owner}/{repo}"}
    code, body, headers = get(f"https://api.github.com/repos/{owner}/{repo}", api=True)
    if code == 200:
        info = json.loads(body)
        out = {
            **base,
            "exists": True,
            "via": "api",
            "full_name": info["full_name"],  # renamed or transferred repos show the new name
            "owner_type": info["owner"]["type"],
            "description": info.get("description"),
            "fork": info.get("fork"),
            "archived": info.get("archived"),
            "stars": info.get("stargazers_count"),
            "pushed_at": info.get("pushed_at"),
        }
        c2, b2, _ = get(f"https://api.github.com/repos/{info['full_name']}/contents", api=True)
        if c2 == 200:
            names = [x["name"] for x in json.loads(b2)]
            out.update({"root_files": names[:40], **summarize_files(names)})
        else:
            out["contents_error"] = c2
        return out
    if code == 404:
        return {**base, "exists": False, "via": "api"}

    # API quota exhausted (403/429) or connection failed: fall back to the web page
    reason = "rate_limited" if code in (403, 429) else f"api_error {code or body}"
    c3, page, _ = get(base["url"], api=False)
    if c3 == 404:
        return {**base, "exists": False, "via": "html", "note": reason}
    if c3 != 200:
        return {**base, "exists": None, "via": "html", "error": f"{reason}; html {c3}"}
    names = sorted(set(re.findall(r'"name":"([^"/]+)","path":"[^"/]+","contentType":"(?:file|directory)"', page)))
    return {**base, "exists": True, "via": "html", "note": reason, "root_files": names[:40], **summarize_files(names)}


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    repos = []
    for a in argv:
        m = REPO_RE.search(a.strip())
        if m and (m.group(1), m.group(2)) not in repos:
            repos.append((m.group(1), m.group(2)))
    if not repos:
        print(__doc__)
        return 1
    pool = ThreadPoolExecutor(max_workers=WORKERS)
    jobs = [(r, pool.submit(check, *r)) for r in repos]
    wait([f for _, f in jobs], timeout=TOTAL_TIMEOUT)
    out = [f.result() if f.done() else {"repo": f"{o}/{r}", "exists": None, "error": "timeout"} for (o, r), f in jobs]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
