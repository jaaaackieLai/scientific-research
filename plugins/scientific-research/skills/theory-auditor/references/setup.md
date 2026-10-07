# Setup

Run these only after the user agrees (SKILL.md step 3). `scripts/check_env.py` has already confirmed disk and RAM.

## Requirements
| | Mathlib only | With PhysLib |
|---|---|---|
| Free disk | 12 GB (10 GB if Lean is installed) | 17 GB |
| RAM | 8 GB minimum, 16 GB comfortable | same |
| First run | download the Mathlib cache (several GB) | plus compiling PhysLib locally, tens of minutes |

## 1. Install elan (the Lean version manager)
- Linux / macOS: `curl https://elan.lean-lang.org/elan-init.sh -sSf | sh`
- Windows (PowerShell):
  ```
  curl -O --location https://elan.lean-lang.org/elan-init.ps1
  powershell -ExecutionPolicy Bypass -f elan-init.ps1
  del elan-init.ps1
  ```
Open a new terminal afterwards so `lake` is on PATH, and check `elan --version` (2.0.0 or newer; otherwise `elan self update`).

## 2. Mathlib workspace (shared by all audits)
```
mkdir -p ~/.theory-auditor && cd ~/.theory-auditor
lake +leanprover-community/mathlib4:lean-toolchain new mathlib_ws math
cd mathlib_ws
lake exe cache get
mkdir -p TheoryAuditor
```
`lake exe cache get` must print something like "Decompressing 5000 file(s)". Never skip it: without the cache, Lean compiles all of Mathlib, which takes hours.

## 3. PhysLib workspace (only when an audit needs it)
1. Read PhysLib's README and `lean-toolchain` at `github.com/leanprover-community/physlib` for the current `require` line and Lean version.
2. `cd ~/.theory-auditor && lake new physlib_ws math`, then replace `physlib_ws/lean-toolchain` with PhysLib's and replace the Mathlib `require` in the lakefile with PhysLib's (PhysLib brings the matching Mathlib).
3. In `physlib_ws`: `lake update`, `lake exe cache get`, then `lake build` to compile PhysLib once.

## Updating
Do not update a workspace in the middle of an audit; proofs can break across Mathlib versions. Between audits, `lake update` followed by `lake exe cache get`.

## Platform notes
- Windows: add `%USERPROFILE%\.theory-auditor` and `%USERPROFILE%\.elan` to the Microsoft Defender exclusions, or file scanning makes builds much slower. WSL2 also works; then run everything inside WSL.
- An editor is optional for the agent (it uses `lake env lean`), but for reading proofs the user can open the workspace in VS Code with the `lean4` extension.
