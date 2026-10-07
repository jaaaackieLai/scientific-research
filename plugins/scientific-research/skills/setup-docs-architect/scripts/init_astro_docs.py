"""Create an Astro docs site in the project (copy template/ to <root>/<docs-dir>/) and add startup instructions to AGENTS.md.

Also adds the ADR/glossary rules to the root and docs AGENTS.md; --domain-only adds just those, for an existing docs site.

See SKILL.md in the same skill for usage. Standard library only; refuses to run when it is already an Astro project, and never overwrites existing files.
"""
import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "template"
SNIPPET_DIR = SKILL_DIR / "snippets"
ASTRO_MARKERS = ("astro.config.mjs", "astro.config.ts", "astro.config.js", "package.json")
# When these already exist, merge the missing lines instead of skipping (e.g. .gitignore must ignore node_modules/ and dist/).
MERGE_FILES = {Path(".gitignore")}


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Initialize an Astro docs site from the template.")
    parser.add_argument("--root", required=True, help="project root directory")
    parser.add_argument("--title", help="docs home page h1 (required unless --domain-only)")
    parser.add_argument("--subtitle", default="", help="docs home page subtitle")
    parser.add_argument("--repo-url", default="", help="prefix for code links, e.g. https://github.com/<owner>/<repo>/blob/main")
    parser.add_argument("--docs-dir", default="docs", help="docs directory (relative to root), defaults to docs")
    parser.add_argument("--domain-only", action="store_true",
                        help="only add the ADR/glossary rules to the AGENTS.md files (for an existing docs site)")
    args = parser.parse_args(argv)
    if not args.domain_only and not args.title:
        parser.error("--title is required unless --domain-only is given")
    if args.domain_only and (args.title or args.subtitle):
        parser.error("--domain-only builds no site, so it takes no --title or --subtitle")
    return args


def package_name(root):
    slug = re.sub(r"[^a-z0-9]+", "-", root.resolve().name.lower()).strip("-")
    return f"{slug or 'project'}-docs"


def fill(text, values):
    # When REPO_URL is empty, drop the whole line so no broken link rule is left behind.
    lines = [line for line in text.splitlines(keepends=True)
             if values["REPO_URL"] or "{{REPO_URL}}" not in line]
    filled = "".join(lines)
    for key, value in values.items():
        filled = filled.replace("{{" + key + "}}", value)
    return filled


def merge_lines(path, text):
    """Append the lines of text that path does not have yet; return whether anything changed."""
    existing = path.read_text(encoding="utf-8")
    have = {line.strip() for line in existing.splitlines()}
    missing = [line for line in text.splitlines() if line.strip() and line.strip() not in have]
    if not missing:
        return False
    sep = "\n" if existing and not existing.endswith("\n") else ""
    path.write_text(existing + sep + "\n".join(missing) + "\n", encoding="utf-8")
    return True


def copy_template(docs, values):
    created, skipped, merged = [], [], []
    for src in sorted(p for p in TEMPLATE_DIR.rglob("*") if p.is_file()):
        rel = src.relative_to(TEMPLATE_DIR)
        dest = docs / rel
        text = fill(src.read_text(encoding="utf-8"), values)
        if dest.exists():
            if rel in MERGE_FILES and merge_lines(dest, text):
                merged.append(rel)
            else:
                skipped.append(rel)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        created.append(rel)
    return created, skipped, merged


def snippet(name, values):
    return fill((SNIPPET_DIR / name).read_text(encoding="utf-8"), values)


def append_section(path, section, marker):
    """Append section to the end of path; leave it alone if the file already contains marker. Return a description of the action.

    A marker starting with # is a heading and must match a whole line, so "### Domain docs" does not count as "## Domain docs".
    """
    if not path.exists():
        path.write_text(section.lstrip("\n"), encoding="utf-8")
        return "created"
    text = path.read_text(encoding="utf-8")
    found = (marker in (line.strip() for line in text.splitlines())) if marker.startswith("#") else marker in text
    if found:
        return "unchanged"
    sep = "" if text.endswith("\n") else "\n"
    path.write_text(text + sep + section, encoding="utf-8")
    return "appended"


def write_docs_agents(docs, values):
    path = docs / "AGENTS.md"
    astro = snippet("docs-agents-astro.md", values)
    if not path.exists():
        path.write_text(snippet("docs-agents-head.md", values) + astro, encoding="utf-8")
        return "created"
    return append_section(path, astro, "## Astro pages")


def write_domain_docs(root, docs, values):
    """Append the ADR/glossary formats to docs/AGENTS.md and the reading rules to the root AGENTS.md."""
    docs_domain = append_section(docs / "AGENTS.md", snippet("docs-agents-domain.md", values),
                                 "## ADRs and glossary")
    root_domain = append_section(root / "AGENTS.md", snippet("root-agents-domain.md", values),
                                 "## Domain docs")
    print(f"{values['DOCS_DIR']}/AGENTS.md ADRs and glossary: {docs_domain}")
    print(f"AGENTS.md domain docs: {root_domain}")


def main(argv=None):
    args = parse_args(argv)
    root = Path(args.root)
    docs = root / args.docs_dir
    values = {
        "TITLE": args.title or "",
        "SUBTITLE": args.subtitle,
        "REPO_URL": args.repo_url.rstrip("/"),
        "DOCS_DIR": args.docs_dir.strip("/"),
        "PACKAGE_NAME": package_name(root),
    }
    existing = [m for m in ASTRO_MARKERS if (docs / m).exists()]
    if args.domain_only:
        if not existing:
            print(f"error: {docs} is not an Astro docs site; run the full init first (or fix --docs-dir).",
                  file=sys.stderr)
            return 1
        write_domain_docs(root, docs, values)
        return 0
    # Astro escapes &quot; in attributes a second time so it shows up literally, and the index's title extraction is cut off at double quotes, so reject outright.
    quoted = [flag for flag, value in (("--title", args.title), ("--subtitle", args.subtitle)) if '"' in value]
    if quoted:
        print(f'error: {", ".join(quoted)} must not contain a double quote ("); use 「」 instead.',
              file=sys.stderr)
        return 1
    if existing:
        print(f"error: {docs} already has {', '.join(existing)}; refusing to overwrite an existing project.",
              file=sys.stderr)
        return 1

    docs.mkdir(parents=True, exist_ok=True)
    created, skipped, merged = copy_template(docs, values)
    docs_agents = write_docs_agents(docs, values)
    root_agents = append_section(root / "AGENTS.md", snippet("root-agents-docs.md", values),
                                 f"{values['DOCS_DIR']}/src/pages")

    print(f"docs dir: {docs}")
    print(f"created {len(created)} files")
    for rel in merged:
        print(f"merged missing lines: {rel}")
    for rel in skipped:
        print(f"skipped (exists): {rel}")
    print(f"{args.docs_dir}/AGENTS.md: {docs_agents}")
    print(f"AGENTS.md: {root_agents}")
    write_domain_docs(root, docs, values)
    return 0


if __name__ == "__main__":
    sys.exit(main())
