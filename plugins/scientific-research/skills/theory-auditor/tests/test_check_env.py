"""Behavior tests for check_env.py: decide whether Lean verification can run on this machine."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_env.py"
spec = importlib.util.spec_from_file_location("check_env", SCRIPT)
check_env = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_env)


def test_ready_when_lean_and_workspace_exist():
    result = check_env.assess(lake_ok=True, workspace_ready=True, free_gb=1, ram_gb=4, physlib=False)

    assert result["verdict"] == "ready"


def test_installable_when_missing_but_resources_suffice():
    result = check_env.assess(lake_ok=False, workspace_ready=False, free_gb=20, ram_gb=16, physlib=False)

    assert result["verdict"] == "installable"


def test_insufficient_when_disk_too_small_for_install():
    result = check_env.assess(lake_ok=False, workspace_ready=False, free_gb=8, ram_gb=16, physlib=False)

    assert result["verdict"] == "insufficient"
    assert any("disk" in reason for reason in result["reasons"])


def test_insufficient_when_ram_too_small():
    result = check_env.assess(lake_ok=False, workspace_ready=False, free_gb=50, ram_gb=4, physlib=False)

    assert result["verdict"] == "insufficient"
    assert any("RAM" in reason for reason in result["reasons"])


def test_physlib_needs_more_disk_than_mathlib_alone():
    mathlib = check_env.assess(lake_ok=True, workspace_ready=False, free_gb=12, ram_gb=16, physlib=False)
    physlib = check_env.assess(lake_ok=True, workspace_ready=False, free_gb=12, ram_gb=16, physlib=True)

    assert mathlib["verdict"] == "installable"
    assert physlib["verdict"] == "insufficient"


def test_unknown_ram_does_not_block_but_is_noted():
    result = check_env.assess(lake_ok=False, workspace_ready=False, free_gb=50, ram_gb=None, physlib=False)

    assert result["verdict"] == "installable"
    assert any("RAM" in note for note in result["notes"])


def make_workspace(root, manifest_text):
    (root / ".lake" / "packages" / "mathlib").mkdir(parents=True)
    (root / "lake-manifest.json").write_text(manifest_text)
    return root


def test_workspace_ready_needs_manifest_and_mathlib_package(tmp_path):
    assert not check_env.workspace_ready(tmp_path, physlib=False)

    make_workspace(tmp_path, '{"packages": [{"name": "mathlib"}]}')

    assert check_env.workspace_ready(tmp_path, physlib=False)


def test_physlib_workspace_needs_physlib_package(tmp_path):
    mathlib_only = make_workspace(tmp_path / "a", '{"packages": [{"name": "mathlib"}]}')
    with_physlib = make_workspace(tmp_path / "b", '{"packages": [{"name": "mathlib"}, {"name": "PhysLib"}]}')
    (with_physlib / ".lake" / "packages" / "PhysLib").mkdir()

    assert not check_env.workspace_ready(mathlib_only, physlib=True)
    assert check_env.workspace_ready(with_physlib, physlib=True)


def test_cli_reports_verdict_and_measured_facts_as_json(tmp_path):
    workspace = tmp_path / "ws"
    result = subprocess.run([sys.executable, str(SCRIPT), "--workspace", str(workspace)],
                            capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["verdict"] in {"ready", "installable", "insufficient"}
    assert report["facts"]["workspace"] == str(workspace)
    assert report["facts"]["workspace_ready"] is False
    assert isinstance(report["facts"]["lake_ok"], bool)
    assert report["facts"]["free_gb"] > 0


def test_default_workspaces_do_not_reuse_dependency_names():
    assert check_env.default_workspace(physlib=False).name == "mathlib_ws"
    assert check_env.default_workspace(physlib=True).name == "physlib_ws"


def test_physlib_workspace_own_name_does_not_count_as_physlib(tmp_path):
    workspace = make_workspace(tmp_path / "physlib_ws", '{"name": "physlib_ws", "packages": [{"name": "mathlib"}]}')

    assert not check_env.workspace_ready(workspace, physlib=True)
