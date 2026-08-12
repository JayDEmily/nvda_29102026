#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "FAIL: Gate 0 requires Linux x86_64" >&2
  exit 2
fi
if [[ -z "${WSL_DISTRO_NAME:-}" ]]; then
  echo "FAIL: Gate 0 programme policy requires WSL2" >&2
  exit 2
fi
case "$(pwd -P)" in
  /mnt/*) echo "FAIL: use native WSL /home/... repository storage" >&2; exit 2 ;;
esac
if [[ -n "$(git status --porcelain=v1 --untracked-files=all)" ]]; then
  echo "FAIL: worktree must be clean before Gate 0 arm" >&2
  exit 2
fi
uv sync --locked --extra dev --offline
uv run python tools/validate_architecture.py
uv run python tools/validate_gate0.py --static
uv run python tools/gate0_runtime_evidence.py arm
