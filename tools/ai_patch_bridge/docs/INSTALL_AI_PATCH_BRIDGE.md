# Local AI Patch Bridge install and operating guide

## Purpose

This document installs and operates the repo-local `AI_PATCH_V1` bridge.

The bridge connects a ChatGPT-authored patch comment in GitHub issue `#1` to the user's local WSL/Linux checkout and Codex CLI.

## Proven local-Codex flow

```text
ChatGPT posts one AI_PATCH_V1 comment
→ local bridge reads GitHub issue #1
→ bridge verifies and decodes the payload
→ bridge creates the target branch from origin/<base_branch>
→ Codex applies or fits the patch
→ Codex runs declared local checks
→ Codex writes codex_receipt.md
→ outer bridge re-runs declared local checks
→ outer bridge stages decoded patch paths
→ outer bridge creates the branch commit and publishes the branch
→ outer bridge verifies the remote branch head
→ outer bridge posts LOCAL_CODEX_RECEIPT_V1
```

Codex does not own final source-control publication. Live testing showed Codex may run with `.git` mounted read-only inside its sandbox. The outer bridge owns staging, commit creation, branch publication, and remote-head verification.

## Required local tools

```text
Python 3.13.5
Git
GitHub CLI: gh
Codex CLI
Node/npm for Codex CLI installation or update
```

The live verification pass used `codex-cli 0.125.0` after `codex-cli 0.117.0` was rejected for GPT-5.5 execution.

## Runtime state

The bridge writes runtime state under:

```text
.ai_patch_bridge/state/
.ai_patch_bridge/runs/<comment_id>/
```

Codex may write local runtime state under:

```text
.codex
```

Both paths are ignored by Git.

## Managed watcher commands

The preferred operator surface is the root Makefile. Run these from the repository root:

```bash
make bridge-on
make bridge-off
make bridge-status
make bridge-dashboard
```

The same controls are available as compatibility commands:

```bash
make bridge on
make bridge off
make watch status
make watch dashboard
```

Expected status output includes one of these states:

```text
WATCHER: ON
WATCHER: OFF
WATCHER: ON_LEGACY
WATCHER: BROKEN
```

State meanings:

- `WATCHER: ON` means the managed watcher PID is alive.
- `WATCHER: OFF` means no managed watcher or legacy watcher is alive.
- `WATCHER: ON_LEGACY` means an older pasted `while true ... ai_patch_bridge.cli once` loop is still alive. Run `make bridge-off`.
- `WATCHER: BROKEN` means the local watcher control hash is missing or mismatched.

The managed watcher writes:

```text
.ai_patch_bridge/state/watcher.pid
.ai_patch_bridge/state/watcher_runtime.json
.ai_patch_bridge/state/watcher_status.txt
.ai_patch_bridge/logs/watch.log
```

The control contract is:

```text
tools/ai_patch_bridge/WATCHER_CONTROL.md
```

## Local readiness gate

Run from the host repo root:

```bash
make -C tools/ai_patch_bridge ai-bridge-preflight
```

Preflight checks Python, Git, GitHub CLI auth, Codex CLI version, clean Git state, remote origin, and `git fetch origin`.

## Offline bridge gates

Run from the host repo root:

```bash
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-self-test
```

The bridge test and lint gates are stdlib-only for the bridge pack.

## Process the inbox once

Run from the host repo root:

```bash
PYTHONPATH=tools/ai_patch_bridge/src python3 -m ai_patch_bridge.cli once \
  --repo JayDEmily/nvda10 \
  --issue-number 2 \
  --repo-root . \
  --state-dir .ai_patch_bridge/state \
  --runs-dir .ai_patch_bridge/runs \
  --local-check "make scaffold-check"
```

For normal Makefile use:

```bash
make -C tools/ai_patch_bridge ai-bridge-once
```

## Rescue branch processing

Rescue payloads are skipped by default. To process a rescue branch explicitly:

```bash
PYTHONPATH=tools/ai_patch_bridge/src python3 -m ai_patch_bridge.cli once \
  --repo JayDEmily/nvda10 \
  --issue-number 2 \
  --repo-root . \
  --state-dir .ai_patch_bridge/state \
  --runs-dir .ai_patch_bridge/runs \
  --accepted-executor rescue-branch \
  --local-check "make scaffold-check"
```

## AI_PATCH_V1 comment requirements

The comment must include:

```text
AI_PATCH_V1
repo: owner/repo
base_branch: main
target_branch: work/some-task or rescue/some-task
scope: short task description
executor: local-codex, github-action, or rescue-branch
mode: local_patch_fit_test_commit_push or rescue_branch_preservation
commit_policy: single_commit
test_policy: required, not_run_allowed, or rescue_unvetted

payload_encoding: base64+gzip
payload_raw_sha256: <sha256 of decoded patch>
payload_gzip_sha256: <sha256 of gzip bytes>
payload_raw_bytes: <decoded byte count>
payload_gzip_bytes: <gzip byte count>

PAYLOAD_BEGIN
<base64 gzip payload>
PAYLOAD_END
```

The decoded payload must contain at least one `diff --git` section.

## Lane ownership

```text
local-codex: consumed by default; target branch must be work/...
github-action: skipped by default by local bridge; target branch must be work/...
rescue-branch: skipped by default; target branch must be rescue/... and test_policy must be rescue_unvetted
```

## Live verification report

Live scenario evidence is recorded in:

```text
tools/ai_patch_bridge/docs/LIVE_SCENARIO_VERIFICATION_20260429.md
```

That report records bad-payload rejection, dry-run verification, Scenario B skip, Scenario C repaired local-Codex execution, Scenario D cumulative export, Scenario E skip, Scenario F fallback, and Scenario G explicit rescue preservation.

## Operating cautions

- Patch transport is separate from architectural correctness.
- Keep the worktree clean before preflight and bridge execution.
- Use one target branch per patch comment.
- Do not use `--allow-dirty` for normal operation.
- A rescue branch is storage, not validation.
- A `status: pushed` receipt means the outer bridge verified the remote branch head after publication.
