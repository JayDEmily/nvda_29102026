#!/usr/bin/env bash
set -u

COMMAND="${1:-status}"
BRIDGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "${AI_PATCH_REPO_ROOT:-$BRIDGE_DIR/../..}" && pwd)"
REPO_NAME="${AI_PATCH_REPO:-JayDEmily/nvda10}"
ISSUE_NUMBER="${AI_PATCH_ISSUE:-2}"
RUNS_DIR="${AI_PATCH_RUNS_DIR:-.ai_patch_bridge/runs}"
STATE_DIR="${AI_PATCH_STATE_DIR:-.ai_patch_bridge/state}"
LOCAL_CHECK="${AI_PATCH_LOCAL_CHECK:-make scaffold-check}"
POLL_SECONDS="${AI_PATCH_POLL_SECONDS:-60}"
CONTROL_HASH="sha256:2a9626937a131a7ff4472a8644664aa8f0b22eb240b8ea510b101cb6d6385ba1"

STATE_ABS="$REPO_ROOT/$STATE_DIR"
RUNS_ABS="$REPO_ROOT/$RUNS_DIR"
LOG_DIR="$REPO_ROOT/.ai_patch_bridge/logs"
PID_FILE="$STATE_ABS/watcher.pid"
STATUS_FILE="$STATE_ABS/watcher_status.txt"
RUNTIME_FILE="$STATE_ABS/watcher_runtime.json"
LOG_FILE="$LOG_DIR/watch.log"
CONTROL_FILE="$BRIDGE_DIR/WATCHER_CONTROL.md"

mkdir -p "$STATE_ABS" "$RUNS_ABS" "$LOG_DIR"

require_control_hash() {
  if ! grep -q "watcher_control_hash: $CONTROL_HASH" "$CONTROL_FILE" 2>/dev/null; then
    echo "WATCHER: BROKEN"
    echo "reason: missing or mismatched watcher control hash"
    echo "control_file: $CONTROL_FILE"
    exit 3
  fi
}

is_running() {
  local pid
  pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

legacy_pids() {
  pgrep -af "ai_patch_bridge.cli once" \
    | awk '/while true|bash -lc/ {print $1}' \
    | awk -v self="$$" '$1 != self'
}

write_runtime() {
  local state="$1"
  local once_exit="$2"
  cat > "$RUNTIME_FILE" <<EOF
{
  "state": "$state",
  "pid": "$(cat "$PID_FILE" 2>/dev/null || true)",
  "last_tick": "$(date -Is)",
  "last_once_exit": "$once_exit",
  "repo": "$REPO_NAME",
  "control_hash": "$CONTROL_HASH",
  "log_path": "$LOG_FILE"
}
EOF
}

run_loop() {
  require_control_hash
  cd "$BRIDGE_DIR" || exit 1
  export PYTHONUNBUFFERED=1
  echo $$ > "$PID_FILE"
  trap 'rm -f "$PID_FILE"; echo "stopped $(date -Is)" > "$STATUS_FILE"; write_runtime off stopped' EXIT

  while true; do
    echo "running tick $(date -Is)" > "$STATUS_FILE"
    write_runtime on running
    echo "===== watcher tick $(date -Is) ====="

    if [ -n "$(git -C "$REPO_ROOT" status --short)" ]; then
      echo "SKIP: worktree is dirty"
      git -C "$REPO_ROOT" status --short
      echo "once_exit=skipped_dirty"
      write_runtime on skipped_dirty
      sleep "$POLL_SECONDS"
      continue
    fi

    git -C "$REPO_ROOT" switch main >/dev/null 2>&1 || true

    PYTHONPATH=src python3 -m ai_patch_bridge.cli once \
      --repo "$REPO_NAME" \
      --issue-number "$ISSUE_NUMBER" \
      --repo-root "$REPO_ROOT" \
      --state-dir "$STATE_DIR" \
      --runs-dir "$RUNS_DIR" \
      --local-check "$LOCAL_CHECK"

    exit_code="$?"
    echo "once_exit=$exit_code"
    write_runtime on "$exit_code"
    sleep "$POLL_SECONDS"
  done
}

start_watcher() {
  require_control_hash
  stop_legacy_watchers
  if is_running; then
    echo "WATCHER: ON"
    echo "pid=$(cat "$PID_FILE")"
    exit 0
  fi

  nohup bash "$0" run-loop >> "$LOG_FILE" 2>&1 &
  echo "WATCHER: ON"
  echo "pid=$!"
  echo "log=$LOG_FILE"
}

stop_legacy_watchers() {
  local legacy
  legacy="$(legacy_pids | tr '\n' ' ')"
  if [ -n "$legacy" ]; then
    echo "stopping legacy watcher pids: $legacy"
    for legacy_pid in $legacy; do
      kill "$legacy_pid" 2>/dev/null || true
    done
    sleep 1
    for legacy_pid in $legacy; do
      kill -0 "$legacy_pid" 2>/dev/null && kill -9 "$legacy_pid" 2>/dev/null || true
    done
  fi
}

stop_watcher() {
  require_control_hash
  if is_running; then
    local pid
    pid="$(cat "$PID_FILE")"
    kill "$pid" 2>/dev/null || true
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
  fi
  stop_legacy_watchers
  echo "stopped $(date -Is)" > "$STATUS_FILE"
  write_runtime off stopped
  echo "WATCHER: OFF"
}

status_watcher() {
  require_control_hash
  local legacy
  legacy="$(legacy_pids | tr '\n' ' ')"
  echo "=== AI PATCH WATCHER STATUS ==="
  date -Is
  echo
  if is_running; then
    echo "WATCHER: ON"
    echo "pid=$(cat "$PID_FILE")"
  elif [ -n "$legacy" ]; then
    echo "WATCHER: ON_LEGACY"
    echo "legacy_pids=$legacy"
    echo "note: run make bridge-off to stop legacy watcher loops"
  else
    echo "WATCHER: OFF"
  fi
  cat "$STATUS_FILE" 2>/dev/null || echo "no status file"
  echo
  echo "=== RUNTIME ==="
  cat "$RUNTIME_FILE" 2>/dev/null || echo "no runtime file"
  echo
  echo "=== CURRENT ONCE CHILD ==="
  pgrep -af "python3 -m ai_patch_bridge.cli once" || echo "no active once child"
  echo
  echo "=== REPO STATE ==="
  echo -n "branch: "
  git -C "$REPO_ROOT" branch --show-current
  echo "status:"
  git -C "$REPO_ROOT" status --short
  echo
  echo "=== LAST WATCH LOG ==="
  tail -40 "$LOG_FILE" 2>/dev/null || echo "no watch log"
}

dashboard_watcher() {
  while true; do
    clear
    status_watcher
    sleep 5
  done
}

case "$COMMAND" in
  on|start) start_watcher ;;
  off|stop) stop_watcher ;;
  status) status_watcher ;;
  dashboard) dashboard_watcher ;;
  tail) tail -f "$LOG_FILE" ;;
  run-loop) run_loop ;;
  *)
    echo "usage: $0 {on|off|status|dashboard|tail}"
    exit 2
    ;;
esac
