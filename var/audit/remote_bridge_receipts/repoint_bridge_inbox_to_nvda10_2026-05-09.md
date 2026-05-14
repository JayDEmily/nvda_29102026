# Repoint bridge inbox to NVDA10

Status: BRIDGE_INBOX_REPOINTED_TO_NVDA10

old_repo: JayDEmily/NVIDIA9_remotetest
old_issue: 1
new_repo: JayDEmily/nvda10
new_issue: 2
new_issue_url: https://github.com/JayDEmily/nvda10/issues/2
starting_sha: f5e9259e2095312abb5960bb207a08f4d0bf7317
control_hash: sha256:2a9626937a131a7ff4472a8644664aa8f0b22eb240b8ea510b101cb6d6385ba1

## Files Changed

- project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md
- tools/ai_patch_bridge/AGENTS.override.md
- tools/ai_patch_bridge/Makefile
- tools/ai_patch_bridge/WATCHER_CONTROL.md
- tools/ai_patch_bridge/docs/BRANCH_AS_PAYLOAD_VALIDATION_RUNBOOK.md
- tools/ai_patch_bridge/docs/INSTALL_AI_PATCH_BRIDGE.md
- tools/ai_patch_bridge/docs/PERSISTENT_WORKER.md
- tools/ai_patch_bridge/docs/TRANSPORT_AND_RECEIPT_HARDENING_IMPLEMENTATION_20260430.md
- tools/ai_patch_bridge/docs/WATCHER_OPERATIONS.md
- tools/ai_patch_bridge/scripts/install_user_service.sh
- tools/ai_patch_bridge/scripts/watch_control.sh
- tools/ai_patch_bridge/systemd/nvda10-ai-patch-bridge.service.template
- tools/ai_patch_bridge/tests/test_persistent_worker_assets.py
- var/audit/remote_bridge_receipts/repoint_bridge_inbox_to_nvda10_2026-05-09.md

## Checks Run

```text
make bridge-off || true
WATCHER: OFF
```

```text
pkill -f "python3 -m ai_patch_bridge.cli once" || true
exit: no active once child remained after stop sequence
```

```text
pgrep -af "ai_patch_bridge.cli once" || true
no persistent once child; output only matched the pgrep command itself
```

```text
git switch main
git fetch origin
git pull --ff-only origin main
git status --short
git branch --show-current
git rev-parse HEAD
Already on 'main'
Your branch is up to date with 'origin/main'.
Already up to date.
main
f5e9259e2095312abb5960bb207a08f4d0bf7317
```

```text
gh issue list --repo JayDEmily/nvda10 --state open --search "NVDA10 AI Patch Bridge Inbox in:title" --json number,title,url
[]
```

```text
gh issue create --repo JayDEmily/nvda10 --title "NVDA10 AI Patch Bridge Inbox" --body "Inbox for NVDA10 AI_PATCH_V1 bridge jobs. This issue is polled by the local Ubuntu bridge watcher. Do not paste unrelated discussion here."
https://github.com/JayDEmily/nvda10/issues/2
```

```text
gh issue list --repo JayDEmily/nvda10 --state open --search "NVDA10 AI Patch Bridge Inbox in:title" --json number,title,url
[{"number":2,"title":"NVDA10 AI Patch Bridge Inbox","url":"https://github.com/JayDEmily/nvda10/issues/2"}]
```

```text
grep -R "JayDEmily/NVIDIA9_remotetest" tools/ai_patch_bridge project_control/remote_bridge Makefile .github var/audit/remote_bridge_receipts || true
tools/ai_patch_bridge/docs/LIVE_SCENARIO_VERIFICATION_20260429.md:This report records live verification of the repo-local AI Patch Bridge in `JayDEmily/NVIDIA9_remotetest`.
tools/ai_patch_bridge/docs/TRANSPORT_AND_RECEIPT_HARDENING_PLAN_20260429.md:repo: JayDEmily/NVIDIA9_remotetest
tools/ai_patch_bridge/docs/BRIDGE_OPERATION_LEDGER_20260429.md:repo: JayDEmily/NVIDIA9_remotetest
project_control/remote_bridge/REMOTE_BRIDGE_BLUEPRINT.md:Small proof exists in `JayDEmily/NVIDIA9_remotetest`: ChatGPT wrote chunked base64 payload files to `main`, read them back, reconstructed the tarball, verified SHA256, and wrote a receipt.
```

```text
bash -n tools/ai_patch_bridge/scripts/watch_control.sh
bash -n tools/ai_patch_bridge/scripts/bridge_doctor.sh
bash -n tools/ai_patch_bridge/scripts/install_user_service.sh
bash -n watch_control.sh: PASS
bash -n bridge_doctor.sh: PASS
bash -n install_user_service.sh: PASS
```

```text
make bridge-blueprint-check
remote bridge blueprint present and key doctrine tokens found
```

```text
make proof-executor-check
proof-block executor present and manifest contract tokens found
```

```text
make -C tools/ai_patch_bridge ai-bridge-blueprint-check
remote bridge blueprint present and key doctrine tokens found
```

```text
make -C tools/ai_patch_bridge ai-bridge-proof-executor-check
proof-block executor present and manifest contract tokens found
```

```text
.venv/bin/python -m pytest -q tools/ai_patch_bridge/tests/test_persistent_worker_assets.py
....                                                                     [100%]
4 passed in 0.03s
```

```text
make bridge-status
WATCHER: OFF
repo: JayDEmily/nvda10
control_hash: sha256:2a9626937a131a7ff4472a8644664aa8f0b22eb240b8ea510b101cb6d6385ba1
CURRENT ONCE CHILD: no active once child
```

## Non-Claims

- watcher was not started
- systemd service was not started or enabled
- no AI_PATCH_V1 job was posted
- end-to-end NVDA10 inbox processing remains unproven until a deliberate test job is posted
