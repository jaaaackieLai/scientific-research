---
name: setup-docs-architect
description: Use when initializing or bootstrapping a project's documentation site, setting up docs/ as an Astro project, or adding the Kami-style (parchment, ink-blue, Noto Serif TC, KaTeX) doc layout and page template to a new repository; also when setting up a project's ADRs (architecture/experiment decision records) and GLOSSARY.md, including for a docs site that already exists. Initialize project documentation, build an Astro docs site, set up ADR and glossary.
---

# Astro Docs Init

## Overview
Creates `<root>/docs/` as an Astro site from `template/` (the shared DocLayout, the core components and an auto-grouping index page). It also adds startup instructions to the root `AGENTS.md` and writing rules to `docs/AGENTS.md`, plus the domain docs: the root `AGENTS.md` tells agents to read `GLOSSARY.md` and `docs/adr/` before working, and `docs/AGENTS.md` holds their formats (`## ADRs and glossary`). `scripts/init_astro_docs.py` does the file work so every project gets the same result. Do not copy the files by hand.

## Steps
If `docs/` is already an Astro site (from this skill or by hand) and the user only wants ADRs and the glossary, run `python3 <skill-dir>/scripts/init_astro_docs.py --root . --domain-only` (add `--docs-dir` if it is not `docs`), report the two AGENTS.md changes, and stop.

1. **Collect inputs.**
   - `--title`: the site h1. `--subtitle`: one line. Ask the user if the README and AGENTS.md don't make them obvious. Neither may contain `"` (the script exits 1); use 「」 instead.
   - `--repo-url`: build it from `git remote get-url origin` as `https://github.com/<owner>/<repo>/blob/<default-branch>`. Leave it out if there is no remote.
   - `--docs-dir`: defaults to `docs`.
2. **Run the script** from the project root:
   ```bash
   python3 <skill-dir>/scripts/init_astro_docs.py --root . --title "..." --subtitle "..." --repo-url "..."
   ```
   - It refuses to run (exit 1) when `docs/` already has `package.json` or `astro.config.*`. Stop there and tell the user.
   - It never overwrites anything. Existing files are reported as `skipped`, and an existing `docs/AGENTS.md` gets the `## Astro pages` section appended. An existing `docs/.gitignore` gets its missing lines (`node_modules/`, `dist/`, `.astro/`) appended.
3. **Register existing docs.** If `docs/` already held `.md` or `.html` files, leave them where they are and list each one under `## Contents` in `docs/AGENTS.md`.
4. **Verify the build:**
   ```bash
   cd docs && npm install && npm run build && ls dist/index.html
   ```
   - For a preview, run `npm run dev` in the background, because it blocks.
5. **Report.** List the files that were created, merged and skipped, and the AGENTS.md changes. Do not commit until the user confirms.

## Adding pages
- Copy `reference/page-template.astro` to `docs/src/pages/<name>.astro`. It shows the Note, nav TOC, numbered h2/h3, `<M>`, `<CodeBlock>`, `<Warn>` and table conventions.
- Add `<name>` to `sections` in `src/pages/index.astro`, then add a line for it under `## Contents` in `docs/AGENTS.md`.

## ADRs and glossary
- The script writes only the rules. `GLOSSARY.md` (repository root) and `docs/adr/NNNN-<slug>.md` are created lazily, when the first term or decision is settled; do not create empty ones during setup.
- The formats live in the `## ADRs and glossary` section of `docs/AGENTS.md`, adapted for research: an ADR records a decision that would invalidate past results if changed (evaluation protocol, data split, baseline settings, seed policy), and the glossary has a `## Notation` table mapping each symbol to its meaning and its name in code.
- Adapted from the domain docs part of [mattpocock/skills `setup-matt-pocock-skills`](https://github.com/mattpocock/skills/tree/main/skills/engineering/setup-matt-pocock-skills); its issue tracker and triage label parts are left out.

## Quick reference
| Need | Use |
|---|---|
| Inline or display math | `<M tex={String.raw`...`} />`, plus `display` for its own line |
| Code | `<CodeBlock code={String.raw`...`} />` |
| Callouts | `<Note>`, `<Warn>` |
| Colors | CSS variables from `DocLayout.astro` (`--accent`, `--muted`, …) |
| Result numbers | `src/data/*.json`, imported by the page |

## Common mistakes
- **Bare `{}` in LaTeX or code:** Astro evaluates it as JS. Pass the content as a `String.raw` string.
- **Page missing from `sections`:** the page ends up under "Uncategorized".
- **Changing npm scripts to `astro dev`:** `.npmrc` sets `bin-links=false` so the site works on exFAT, which leaves `node_modules/.bin` empty.
- **Hard-coded hex colors:** they break dark mode.
- **Non-literal `title` or `subtitle` on `DocLayout`:** the index extracts them with a regex, so they must be plain string attributes without `"` (use 「」).
- **Pages in subfolders of `src/pages/`:** the index only lists top-level pages, and the layout's `index.html` home link breaks one level down. Keep pages flat.
- **Promising fully offline pages:** Noto Serif TC and the KaTeX CSS/fonts load from CDNs. Without network, math and fonts fall back.
