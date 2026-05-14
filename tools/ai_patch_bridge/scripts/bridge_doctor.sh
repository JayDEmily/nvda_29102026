#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "${1:-$(dirname "${BASH_SOURCE[0]}")/../../..}" && pwd)"
BRIDGE_DIR="$ROOT/tools/ai_patch_bridge"

say() { printf '%s\n' "$*"; }
fail() { say "BRIDGE_DOCTOR: FAIL - $*" >&2; exit 1; }
warn() { say "BRIDGE_DOCTOR: WARN - $*" >&2; }

say "BRIDGE_DOCTOR: root=$ROOT"

[ -d "$ROOT/.git" ] || fail "repo root is not a Git checkout"
[ -f "$ROOT/Makefile" ] || fail "root Makefile missing"
[ -f "$BRIDGE_DIR/Makefile" ] || fail "bridge Makefile missing"
[ -f "$BRIDGE_DIR/AGENTS.override.md" ] || fail "bridge AGENTS.override.md missing"
[ -f "$BRIDGE_DIR/WATCHER_CONTROL.md" ] || fail "WATCHER_CONTROL.md missing"
[ -x "$BRIDGE_DIR/scripts/watch_control.sh" ] || warn "watch_control.sh is not executable; bash can still run it"

branch="$(git -C "$ROOT" branch --show-current)"
say "BRIDGE_DOCTOR: branch=$branch"
[ "$branch" = "main" ] || warn "current branch is not main"

status="$(git -C "$ROOT" status --short)"
if [ -n "$status" ]; then
  say "BRIDGE_DOCTOR: worktree dirty"
  printf '%s\n' "$status"
  warn "persistent worker should usually start from a clean worktree"
else
  say "BRIDGE_DOCTOR: worktree clean"
fi

git -C "$ROOT" remote get-url origin >/dev/null 2>&1 || warn "origin remote not configured"

if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    say "BRIDGE_DOCTOR: gh auth ok"
  else
    warn "gh exists but gh auth status failed"
  fi
else
  warn "gh CLI not found; existing bridge may fail if it needs gh for GitHub API calls"
fi

if command -v python3.13 >/dev/null 2>&1; then
  say "BRIDGE_DOCTOR: python3.13=$(python3.13 --version 2>&1)"
else
  warn "python3.13 not found on PATH"
fi

make -C "$ROOT" bridge-blueprint-check
make -C "$ROOT" proof-executor-check
make -C "$BRIDGE_DIR" ai-bridge-blueprint-check
make -C "$BRIDGE_DIR" ai-bridge-proof-executor-check

say "BRIDGE_DOCTOR: PASS"
