# Persistent Ubuntu bridge worker

Status: local operating note

## Purpose

The existing bridge worker can already be started manually with:

```bash
make bridge-on
make bridge-status
make bridge-dashboard
make bridge-off
```

For long-running use, the cleaner Ubuntu shape is a `systemd --user` service that runs the bridge watcher in the foreground and lets systemd restart it if it exits.

## Recommended bring-up sequence

From the repo root:

```bash
git pull --ff-only origin main
bash tools/ai_patch_bridge/scripts/bridge_doctor.sh
bash tools/ai_patch_bridge/scripts/install_user_service.sh --repo-root "$PWD"
systemctl --user status nvda10-ai-patch-bridge.service --no-pager
```

## What the persistent service does

The installed user service runs:

```bash
make -C "$REPO_ROOT/tools/ai_patch_bridge" ai-bridge-watch
```

That calls the existing bridge watcher loop. The service does not replace the bridge implementation.

Default inbox:

```text
AI_PATCH_REPO=JayDEmily/nvda10
AI_PATCH_ISSUE=2
AI_PATCH_BASE=main
```

## What GitHub remains responsible for

GitHub remains the transport and receipt surface:

- patch inbox commits;
- GitHub Actions patch-apply lane;
- PR preflight checks;
- receipts under `var/audit/remote_bridge_receipts/`.

## What Codex remains responsible for

Codex CLI remains the local judgement worker when the job is not a clean scripted patch:

- stale-base patch repair;
- final-file-state reconciliation;
- code refactor judgement;
- targeted proof execution;
- committing/pushing when routed by the bridge.

## Kill switch

Stop the service:

```bash
systemctl --user stop nvda10-ai-patch-bridge.service
```

Disable it:

```bash
systemctl --user disable nvda10-ai-patch-bridge.service
```

Manual bridge stop still exists:

```bash
make bridge-off
```
