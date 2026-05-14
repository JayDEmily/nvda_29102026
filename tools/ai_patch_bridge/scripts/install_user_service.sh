#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  bash tools/ai_patch_bridge/scripts/install_user_service.sh --repo-root /absolute/path/to/repo [--enable]

Installs and starts a systemd --user service named nvda10-ai-patch-bridge.service.
Use --enable to start it automatically for future user sessions.
USAGE
}

REPO_ROOT=""
ENABLE="false"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    --enable)
      ENABLE="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

if [ -z "$REPO_ROOT" ]; then
  usage
  exit 2
fi

REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
BRIDGE_DIR="$REPO_ROOT/tools/ai_patch_bridge"
UNIT_DIR="$HOME/.config/systemd/user"
UNIT_PATH="$UNIT_DIR/nvda10-ai-patch-bridge.service"

[ -d "$REPO_ROOT/.git" ] || { echo "Repo root is not a Git checkout: $REPO_ROOT" >&2; exit 1; }
[ -f "$BRIDGE_DIR/Makefile" ] || { echo "Bridge Makefile not found: $BRIDGE_DIR/Makefile" >&2; exit 1; }
command -v systemctl >/dev/null 2>&1 || { echo "systemctl not found" >&2; exit 1; }

mkdir -p "$UNIT_DIR"

cat > "$UNIT_PATH" <<UNIT
[Unit]
Description=NVDA10 AI patch bridge watcher
Documentation=file://$BRIDGE_DIR/docs/PERSISTENT_WORKER.md
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$BRIDGE_DIR
Environment=AI_PATCH_REPO_ROOT=$REPO_ROOT
Environment=AI_PATCH_REPO=JayDEmily/nvda10
Environment=AI_PATCH_ISSUE=2
Environment=AI_PATCH_BASE=main
Environment=AI_PATCH_LOCAL_CHECK=make scaffold-check
Environment=AI_PATCH_POLL_SECONDS=60
ExecStart=/usr/bin/env bash -lc 'make ai-bridge-watch'
Restart=always
RestartSec=15

[Install]
WantedBy=default.target
UNIT

systemctl --user daemon-reload
systemctl --user restart nvda10-ai-patch-bridge.service

if [ "$ENABLE" = "true" ]; then
  systemctl --user enable nvda10-ai-patch-bridge.service
fi

systemctl --user status nvda10-ai-patch-bridge.service --no-pager
