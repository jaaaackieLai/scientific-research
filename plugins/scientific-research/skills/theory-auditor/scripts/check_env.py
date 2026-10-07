"""Decide whether Lean verification can run on this machine.

See SKILL.md in the same skill for usage. Standard library only; never installs anything.
"""
import argparse
import ctypes
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path.home() / ".theory-auditor"
# PhysLib was called PhysLean before March 2026; a workspace pinned to an older release still has that name.
PHYSLIB_PACKAGES = {"physlib", "physlean"}

# Free disk needed for what is still missing (GB): a Lean toolchain via elan, a Mathlib workspace with the
# prebuilt cache (~7 GB plus headroom), and PhysLib's own build output on top of Mathlib.
TOOLCHAIN_GB = 2
MATHLIB_GB = 10
PHYSLIB_GB = 5
# Loading Mathlib in the Lean server takes several GB; below this, proofs stall or the server is killed.
MIN_RAM_GB = 8


def workspace_ready(workspace, physlib):
    workspace = Path(workspace)
    packages = workspace / ".lake" / "packages"
    if not ((workspace / "lake-manifest.json").is_file() and (packages / "mathlib").is_dir()):
        return False
    return not physlib or any(pkg.name.lower() in PHYSLIB_PACKAGES for pkg in packages.iterdir())


def required_disk_gb(lake_ok, physlib):
    return (0 if lake_ok else TOOLCHAIN_GB) + MATHLIB_GB + (PHYSLIB_GB if physlib else 0)


def assess(lake_ok, workspace_ready, free_gb, ram_gb, physlib):
    if lake_ok and workspace_ready:
        return {"verdict": "ready", "reasons": [], "notes": []}
    need = required_disk_gb(lake_ok, physlib)
    reasons, notes = [], []
    if free_gb < need:
        reasons.append(f"free disk {free_gb:.0f} GB < {need} GB needed to install")
    if ram_gb is None:
        notes.append(f"RAM could not be detected; Lean with Mathlib needs at least {MIN_RAM_GB} GB")
    elif ram_gb < MIN_RAM_GB:
        reasons.append(f"RAM {ram_gb:.0f} GB < {MIN_RAM_GB} GB minimum")
    return {"verdict": "insufficient" if reasons else "installable", "reasons": reasons, "notes": notes}


def default_workspace(physlib):
    # Not "mathlib"/"physlib": lake names the package after the directory, which would clash with the dependency.
    return DEFAULT_ROOT / ("physlib_ws" if physlib else "mathlib_ws")


def lake_ok():
    lake = shutil.which("lake") or shutil.which(str(Path.home() / ".elan" / "bin" / "lake"))
    if not lake:
        return False
    try:
        return subprocess.run([lake, "--version"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def free_disk_gb(path):
    path = Path(path).resolve()
    while not path.exists():
        path = path.parent
    return shutil.disk_usage(path).free / 1e9


def ram_gb():
    """Total physical memory in GB, or None when it cannot be read."""
    try:
        system = platform.system()
        if system == "Linux":
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) * 1024 / 1e9
        if system == "Darwin":
            out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=10)
            return int(out.stdout.strip()) / 1e9
        if system == "Windows":
            class MemoryStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            status = MemoryStatus(dwLength=ctypes.sizeof(MemoryStatus))
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return status.ullTotalPhys / 1e9
    except (OSError, ValueError, subprocess.TimeoutExpired):
        pass
    return None


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Check whether Lean verification can run on this machine.")
    parser.add_argument("--physlib", action="store_true", help="the derivation needs PhysLib")
    parser.add_argument("--workspace", help="Lean workspace (default ~/.theory-auditor/mathlib_ws or .../physlib_ws)")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    workspace = Path(args.workspace) if args.workspace else default_workspace(args.physlib)
    ram = ram_gb()
    facts = {
        "workspace": str(workspace),
        "physlib": args.physlib,
        "lake_ok": lake_ok(),
        "workspace_ready": workspace_ready(workspace, args.physlib),
        "free_gb": round(free_disk_gb(workspace), 1),
        "ram_gb": None if ram is None else round(ram, 1),
    }
    result = assess(facts["lake_ok"], facts["workspace_ready"], facts["free_gb"], facts["ram_gb"], args.physlib)
    print(json.dumps({**result, "facts": facts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
