"""Behavior tests for init_astro_docs.py: run the script in a temporary project directory and check the generated files."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_astro_docs.py"

CORE_FILES = [
    "package.json",
    "astro.config.mjs",
    "tsconfig.json",
    ".npmrc",
    ".gitignore",
    "AGENTS.md",
    "src/layouts/DocLayout.astro",
    "src/components/M.astro",
    "src/components/Note.astro",
    "src/components/Warn.astro",
    "src/components/CodeBlock.astro",
    "src/components/ThemeToggle.astro",
    "src/pages/index.astro",
]


def run(root, *extra):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root),
         "--title", "My Docs", "--subtitle", "demo subtitle", *extra],
        capture_output=True, text=True,
    )


def test_creates_core_files_with_placeholders_filled(tmp_path):
    result = run(tmp_path)

    assert result.returncode == 0, result.stderr
    docs = tmp_path / "docs"
    for rel in CORE_FILES:
        assert (docs / rel).is_file(), rel
    for path in docs.rglob("*"):
        if path.is_file():
            assert "{{" not in path.read_text(encoding="utf-8"), path
    index = (docs / "src/pages/index.astro").read_text(encoding="utf-8")
    assert 'title="My Docs"' in index
    assert 'subtitle="demo subtitle"' in index


def test_package_name_derived_from_project_dir(tmp_path):
    root = tmp_path / "My Cool_Project"
    root.mkdir()

    run(root)

    package = (root / "docs/package.json").read_text(encoding="utf-8")
    assert '"name": "my-cool-project-docs"' in package


def test_creates_root_agents_md_with_docs_section(tmp_path):
    run(tmp_path)

    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "npm run dev" in agents
    assert "docs/AGENTS.md" in agents


def test_appends_docs_section_to_existing_root_agents_md(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# AGENTS\n\n## Rules\n- keep me\n", encoding="utf-8")

    run(tmp_path)

    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.startswith("# AGENTS\n\n## Rules\n- keep me\n")
    assert agents.count("npm run dev") == 1


def test_keeps_existing_docs_agents_md_and_appends_astro_rules(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "AGENTS.md").write_text("# docs\n- old.md: legacy notes\n", encoding="utf-8")
    (docs / "old.md").write_text("legacy", encoding="utf-8")

    result = run(tmp_path)

    assert result.returncode == 0, result.stderr
    text = (docs / "AGENTS.md").read_text(encoding="utf-8")
    assert text.startswith("# docs\n- old.md: legacy notes\n")
    assert "## Astro pages" in text
    assert (docs / "old.md").read_text(encoding="utf-8") == "legacy"


def test_refuses_when_docs_already_astro(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "astro.config.mjs").write_text("// existing", encoding="utf-8")

    result = run(tmp_path)

    assert result.returncode != 0
    assert "already" in result.stderr
    assert not (docs / "package.json").exists()
    assert not (tmp_path / "AGENTS.md").exists()


def test_repo_url_rule_only_when_given(tmp_path):
    without = tmp_path / "a"
    with_url = tmp_path / "b"
    without.mkdir()
    with_url.mkdir()

    run(without)
    run(with_url, "--repo-url", "https://github.com/me/proj/blob/main")

    assert "GitHub links" not in (without / "docs/AGENTS.md").read_text(encoding="utf-8")
    assert "https://github.com/me/proj/blob/main/..." in (with_url / "docs/AGENTS.md").read_text(encoding="utf-8")


def test_custom_docs_dir(tmp_path):
    result = run(tmp_path, "--docs-dir", "site")

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "site/src/pages/index.astro").is_file()
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "cd site" in agents
    assert "site/src/pages" in agents


def test_refuses_double_quote_in_title(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--title", 'Say "hi"'],
        capture_output=True, text=True,
    )

    assert result.returncode != 0
    assert "double quote" in result.stderr
    assert not (tmp_path / "docs").exists()


def test_merges_missing_lines_into_existing_gitignore(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / ".gitignore").write_text("*.log\nnode_modules/", encoding="utf-8")

    run(tmp_path)

    lines = (docs / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert lines[0] == "*.log"
    assert lines.count("node_modules/") == 1
    assert "dist/" in lines and ".astro/" in lines


def test_only_agents_md_is_written(tmp_path):
    run(tmp_path)

    assert (tmp_path / "AGENTS.md").is_file()
    assert not (tmp_path / "CLAUDE.md").exists()


def test_root_agents_md_gets_domain_docs_rules_once(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")

    run(tmp_path)

    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert agents.count("## Domain docs") == 1
    assert "GLOSSARY.md" in agents
    assert "docs/adr/" in agents


def test_docs_agents_md_gets_adr_and_glossary_formats(tmp_path):
    run(tmp_path)

    text = (tmp_path / "docs/AGENTS.md").read_text(encoding="utf-8")
    assert text.count("## ADRs and glossary") == 1
    assert "adr/0001-" in text
    assert "## Notation" in text
    assert "_Avoid_" in text


def test_domain_only_adds_rules_to_existing_astro_docs(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "astro.config.mjs").write_text("// existing", encoding="utf-8")
    (docs / "AGENTS.md").write_text("# docs\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path), "--domain-only"],
        capture_output=True, text=True,
    )

    assert result.returncode == 0, result.stderr
    assert not (docs / "package.json").exists()
    assert "## ADRs and glossary" in (docs / "AGENTS.md").read_text(encoding="utf-8")
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "## Domain docs" in agents
    assert "npm run dev" not in agents
