# Branch-as-payload validation runbook

## Purpose

This runbook defines the preferred bridge workflow for normal ChatGPT-created work.

The branch is the payload. GitHub comments are only the control and receipt surface.

```text
payload = GitHub branch
control = LOCAL_BRANCH_VALIDATE_V1
receipt = LOCAL_CODEX_RECEIPT_V1
```

This avoids the failed inline base64 issue-comment transport path.

## When to use

Use branch-as-payload when ChatGPT can create or update a GitHub branch directly.

Use GitHub blob fallback only when a patch payload is unavoidable.

Use inline base64 only for tiny compatibility probes.

## Control comment shape

```text
LOCAL_BRANCH_VALIDATE_V1
repo: <owner/repo>
base_branch: main
target_branch: work/...
validation_mode: branch_checkout_test_repair_receipt
checks_required: default
source_pr: <optional PR number>
```

The control comment is small and human-readable. It does not carry patch bytes.

## Submitter command

From `tools/ai_patch_bridge`:

```bash
PYTHONPATH=src python3 -m ai_patch_bridge.cli validate-branch-and-wait \
  --repo JayDEmily/nvda10 \
  --issue-number 2 \
  --base-branch main \
  --target-branch work/example-branch \
  --source-pr 14 \
  --checks-required default \
  --timeout-seconds 3600 \
  --poll-seconds 30
```

`--source-pr` is optional. Use it when validating a specific draft PR.

## Required local gate before live use

Run from repo root first:

```bash
make bridge-status
```

Do not submit a live validation request if watcher status is `ON_LEGACY`, `BROKEN`, or the worktree is dirty.

Then run:

```bash
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
```

## Receipt rule

A valid local outcome must be visible in GitHub as:

```text
LOCAL_CODEX_RECEIPT_V1
source_comment_id: <LOCAL_BRANCH_VALIDATE_V1 comment id>
status: pushed|checked|failed|stopped|timeout|receipt_post_failed|dry_run_ready
computer_unix_epoch_s: <epoch seconds>
computer_utc_minute: <YYYY-MM-DDTHH:MMZ>
human_melbourne_minute: <DD-MM-YYYY HH:MM AEST|AEDT>
human_timezone: Australia/Melbourne
human_utc_offset: UTC+10|UTC+11
```

`checked` means an existing remote branch was fetched/inspected, required local checks passed, and no additional patch payload was applied.

ChatGPT must read the GitHub-visible receipt before asking the user to inspect local logs.

## Failure handling

```text
If bridge-status is ON_LEGACY: stop and clean watcher state first.
If worktree is dirty: stop and inspect before running bridge.
If tests fail: do not run live validation.
If receipt is missing: poll GitHub issue #1 before asking for local inspection.
If receipt says local logs are required: local inspection becomes allowed.
```

## Merge rule

Branch-as-payload validation is not the same as merge approval.

Do not mark PR #14 ready for review or merge until local gates and live validation receipts pass, unless the user explicitly overrides that rule.
