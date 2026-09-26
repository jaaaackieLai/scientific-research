# scientific-research

A skill pack for deep learning research. It can be installed as a Claude Code plugin, or copied into a single project.

## Skills

| Skill | Description |
| --- | --- |
| background-knowledge | Hand-maintained domain knowledge base (label settings, model architectures, data types, training scenarios); manual invocation only |
| paper-search | Search and filter papers by fixed quality criteria; outputs a list of qualifying papers with the reason for each decision |
| article-advice | Review and rewrite your own paper draft, section by section, plus cross-section consistency checks |
| figure-making | Make or review paper data figures with matplotlib |
| table-making | Make or review paper tables with LaTeX (booktabs) |
| astro-docs-init | Create a Kami-style Astro documentation site in the project's `docs/` |

## Option 1: Install as a plugin (available in all projects)

Claude Code (run inside Claude Code):

```
/plugin marketplace add E:\Projects\scientific-research
/plugin install scientific-research@scientific-research
```

Update: `/plugin marketplace update scientific-research`, then reinstall or restart Claude Code.

Codex (run in a terminal):

```bash
codex plugin marketplace add E:/Projects/scientific-research
codex plugin add scientific-research@scientific-research
```

Update: `codex plugin marketplace upgrade scientific-research`, then run `codex plugin add scientific-research@scientific-research` again.


## Option 2: Use in a single project only

Copy the whole folder of each skill you need into the target project. Copy each skill folder completely (including subfolders such as `scripts/` and `references/`); copying only `SKILL.md` leaves files missing.

| Tool | Target location |
| --- | --- |
| Claude Code | `<target project>/.claude/skills/<skill name>/` |
| Codex | `<target project>/.agents/skills/<skill name>/` |


Copy all skills (Linux / macOS; replace `target` with your project path):

```bash
target=/path/to/my-project
mkdir -p "$target/.claude/skills"
cp -rf /path/to/scientific-research/plugins/scientific-research/skills/* "$target/.claude/skills/"
```

Notes:
- This copies the current version. After the skills here are updated, copy them again to sync.
- With this method, skill names have no prefix; use `/paper-search` directly.
