# Bridge operating channels and receipts

## Purpose

This document defines the valid work channels for the AI Patch Bridge and the GitHub-visible receipt contract used to determine local bridge outcomes.

There are three channels:

```text
Channel 1 — ChatGPT direct GitHub connector write
Channel 2 — GitHub mobile human checkpoint
Channel 3 — Local bridge / Ubuntu / Codex execution
```

Each channel has a different execution surface and a different proof surface.

## Channel matrix

| Channel | Executor | Normal proof | Valid use |
|---|---|---|---|
| ChatGPT direct GitHub connector write | GitHub connector | commit SHA, PR number, changed files | docs, plans, small static bridge edits, PR comments |
| GitHub mobile human checkpoint | user | PR state, review, merge event | Ready for review, approval, merge, close |
| Local bridge / Ubuntu / Codex execution | watcher, Codex, outer bridge | `LOCAL_CODEX_RECEIPT_V1` on issue #1 | runtime code, tests, patch fitting, large patches, local validation |

## Channel 1 — ChatGPT direct GitHub connector write

Mechanism:

```text
ChatGPT proposes GitHub write
→ user approves in ChatGPT UI
→ GitHub branch/file/PR changes directly
```

Proof surface:

```text
commit SHA
PR number
branch comparison
changed file list
```

This proves GitHub accepted the write. It does not prove local tests passed, the watcher ran, Codex ran, or runtime behaviour works.

Use this channel for docs, plans, small static bridge edits, PR comments, closing superseded PRs, and draft PR creation.

## Channel 2 — GitHub mobile human checkpoint

Mechanism:

```text
ChatGPT creates or updates a draft PR
→ user opens GitHub app on iPhone
→ user performs a GitHub-side action
```

Use these terms exactly:

```text
Ready for review
Approve / Submit review
Merge
Close PR
```

Meanings:

```text
Ready for review: converts a draft PR into a normal PR.
Approve / Submit review: satisfies a review gate if branch protection requires it.
Merge: integrates the branch into the base branch.
Close PR: closes without merging.
```

Rules:

```text
Ready for review does not prove local validation.
Approval does not prove local validation.
Merge remains forbidden until required local gates pass unless the user explicitly overrides.
ChatGPT must not confuse Ready for review, Approve, and Merge.
```

## Channel 3 — Local bridge / Ubuntu / Codex execution

Mechanism:

```text
ChatGPT posts AI_PATCH_V1 to GitHub issue #1
→ local watcher processes the inbox comment
→ bridge decodes and verifies payload
→ local Codex applies or fits patch
→ local checks run
→ outer bridge commits and pushes
→ receipt is posted back to GitHub issue #1
→ ChatGPT reads the receipt from GitHub
```

Proof surface:

```text
LOCAL_CODEX_RECEIPT_V1
```

This proves only what the receipt explicitly says.

## Receipt contract

Every normal local bridge run must produce one GitHub-visible receipt unless the machine or GitHub transport itself is unavailable.

Minimum shape:

```text
LOCAL_CODEX_RECEIPT_V1
source_comment_id: <AI_PATCH issue comment id or LOCAL_BRANCH_VALIDATE_V1 comment id>
status: pushed|checked|failed|stopped|timeout|receipt_post_failed|dry_run_ready
computer_unix_epoch_s: <integer seconds since 1970-01-01T00:00:00Z>
computer_utc_minute: <YYYY-MM-DDTHH:MMZ>
human_melbourne_minute: <DD-MM-YYYY HH:MM AEST|AEDT>
human_timezone: Australia/Melbourne
human_utc_offset: UTC+10|UTC+11
target_branch: <branch if known>
head_sha: <sha if pushed or checked>
reason: <failure reason if failed/stopped/timeout/receipt_post_failed>
checks_run: <comma-separated commands or not_run|unknown>
check_outcome: passed|failed|not_run|unknown
codex_receipt_path: <path if written>
run_dir: <local run dir if known>
```

The implemented receipt writer supplies timestamp fields and fills missing `checks_run` and `check_outcome` with `unknown`.

## Timestamp contract

Machine timestamp:

```text
computer_unix_epoch_s: integer epoch seconds
computer_utc_minute: UTC ISO-like minute, e.g. 2026-04-30T04:17Z
```

Human timestamp:

```text
human_melbourne_minute: DD-MM-YYYY HH:MM AEST|AEDT
human_timezone: Australia/Melbourne
human_utc_offset: UTC+10 or UTC+11
```

Australian date format is binding. `07-04-2026` means 7 April 2026, not 4 July 2026. Minute precision is required.

The receipt generator must derive AEST/AEDT and UTC offset from `Australia/Melbourne` at runtime. It must not hard-code AEST permanently.

Example timestamp block:

```text
computer_unix_epoch_s: 1777522620
computer_utc_minute: 2026-04-30T04:17Z
human_melbourne_minute: 30-04-2026 14:17 AEST
human_timezone: Australia/Melbourne
human_utc_offset: UTC+10
```

## Status meanings

| Status | Meaning | Normal next action |
|---|---|---|
| `pushed` | outer bridge pushed target branch and receipt verified | inspect PR or branch |
| `checked` | existing remote branch was fetched/inspected, required local checks passed, and no additional patch payload was applied | inspect PR or branch |
| `failed` | bridge or Codex failed before successful publication | inspect reason; do not merge |
| `stopped` | bridge intentionally stopped because a precondition was unsafe | inspect reason; do not retry blindly |
| `timeout` | submitter did not see matching receipt before timeout | poll GitHub issue #1 again |
| `receipt_post_failed` | execution may have happened but GitHub-visible receipt could not be verified | local inspection allowed |
| `dry_run_ready` | payload decoded/verified without Codex or Git mutation | no runtime proof |

## Merge-readiness rules

Static PR readiness requires scoped files, consistent docs/tests, unchanged lane semantics, and truthful notes about local gates not run.

Local merge readiness requires:

```bash
make bridge-status
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
```

Then:

```text
branch-as-payload validation probe or payload probe as required
forced inline submit-and-wait probe
forced blob submit-and-wait probe
matching receipts visible on GitHub issue #1
source_comment_id correlation confirmed
local repo returned to main with clean worktree
```

## Mobile-only workflow

When the user only has the iPhone, ChatGPT may prepare a draft PR and add clear PR comments. The user may inspect, close, or later advance GitHub state. Ready for review is not local validation.

## Computer-on workflow

When the computer is available:

```text
run make bridge-status first
resolve ON_LEGACY/BROKEN/dirty states before live payloads
run bridge tests and lint before live probes
run inline probe before blob probe
read receipts from GitHub issue #1
only then consider Ready for review / approval / merge
```

## Failure handling

```text
If bridge-status is ON_LEGACY: stop and clean watcher state first.
If worktree is dirty: stop and inspect before running bridge.
If tests fail: do not run live probes.
If lint fails: patch bridge files only.
If inline probe fails: do not run blob probe.
If blob probe fails: do not merge.
If receipt is missing: ChatGPT polls GitHub issue #1 before asking for local inspection.
If receipt says local logs are required: local inspection becomes allowed.
```
