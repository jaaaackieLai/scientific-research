"""The Codex manifest exists and carries the same version as the Claude Code marketplace entry.

Codex keys its plugin cache by this version, so a stale or missing version means users never get updates.
"""
import json
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_DIR.parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_codex_manifest_version_matches_claude_marketplace():
    codex = load(PLUGIN_DIR / ".codex-plugin" / "plugin.json")
    claude = load(REPO_ROOT / ".claude-plugin" / "marketplace.json")["plugins"][0]

    assert codex["name"] == claude["name"]
    assert codex["version"] == claude["version"]
    assert (PLUGIN_DIR / codex["skills"]).is_dir()
