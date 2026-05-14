# PLANS.md

## Purpose

This file defines the scenario plan for the local AI Patch Bridge. It tells future agents and Codex which lane to use when the user is working from ChatGPT, phone, sandbox, GitHub, or local WSL.

## Core rule

Choose exactly one promotion intent for each ChatGPT work session:

```text
direct_pr
local_codex_execute
rescue_only
```

Do not mix lanes inside one patch comment.

## Current execution split

For `local_codex_execute`, Codex and the outer bridge have separate jobs:

```text
Codex: apply or fit the decoded patch, run declared checks, write codex_receipt.md
Outer bridge: re-run declared checks, stage decoded patch paths, commit, push, verify origin, post receipt
```

This split is binding for the bridge because live testing showed Codex may not have write access to `.git` inside its sandbox.

## Active tranche — bridge transport design pivot and validation prep, 2026-04-30

### Promotion intent

```text
direct_pr
```

This tranche updates PR #14 so the bridge design no longer treats inline issue-comment payloads as a real patch transport. It prepares the branch for local validation, but it does not claim local proof.

### Current machine state

The user reports that the Ubuntu/Linux environment is running and has pulled the GitHub work branch. That is useful operational context, but it is not yet a bridge proof surface in this chat.

Observed by ChatGPT so far:

```text
GitHub branch and PR state only
```

Not yet observed by ChatGPT:

```text
make bridge-status output
local git status output
local test output
local lint output
local watcher receipt
Codex execution receipt
```

Therefore the first local proof gate remains:

```bash
make bridge-status
```

### Branch and PR

```text
branch: work/bridge-transport-and-receipt-hardening-20260430
primary PR: #14 Harden bridge transport and receipt handling
```

### Transport diagnosis

The known defect is not patch size alone.

The real defect is:

```text
GitHub issue comment body used as payload carrier
→ inline base64+gzip text
→ text mutation/truncation/format boundary risk
→ strict base64 decode failure before Codex can reason about the patch
```

Therefore the design pivot is:

```text
Comments are control plane and receipt plane.
Branches, blobs, or repo files are data plane.
```

### Canonical transport strategy

Preferred order:

```text
1. Branch-as-payload primary lane
2. GitHub blob fallback lane
3. Repo-file or manifest lane for future large/multipart payloads
4. Inline base64 only for tiny compatibility probes
```

#### Lane 1 — Branch-as-payload primary

Use when ChatGPT can safely create the branch directly through GitHub connector writes.

```text
payload = GitHub branch
control = PR or issue comment requesting validation
proof = LOCAL_CODEX_RECEIPT_V1
```

Flow:

```text
ChatGPT creates branch and draft PR
→ local bridge validates the branch
→ Codex repairs if needed
→ outer bridge pushes repaired branch if changed
→ bridge posts GitHub-visible receipt
```

This lane avoids inline patch transport completely. It is preferred for normal ChatGPT-created work because the user sees a normal GitHub PR rather than an opaque payload.

#### Lane 2 — GitHub blob fallback

Use when a branch cannot sensibly be created first and the bridge must receive a patch payload.

```text
payload = GitHub blob
control = AI_PATCH_V1 issue comment with blob SHA and hashes
proof = LOCAL_CODEX_RECEIPT_V1
```

This lane keeps large payload bytes out of issue comments.

#### Lane 3 — Repo-file or manifest future lane

Use later if payloads need to be human-inspectable or multipart.

```text
payload = repo file or manifest on payload branch
control = comment pointing at manifest
proof = LOCAL_CODEX_RECEIPT_V1
```

This is not required before PR #14 can be locally tested unless branch/blob lanes fail.

#### Lane 4 — Inline compatibility/probe only

Inline base64 comments remain allowed only for tiny probes and backwards-compatible parser tests.

```text
payload = inline base64+gzip in comment
use = tiny probe only
```

Do not use inline comments for real multi-file patches.

### Three operating channels

There are three valid work channels. They are not interchangeable.

```text
Channel 1 — ChatGPT direct GitHub connector write
Channel 2 — GitHub mobile human checkpoint
Channel 3 — Local bridge / Ubuntu / Codex execution
```

Each channel must declare its proof surface. A GitHub commit SHA is not a local test receipt. A mobile Ready-for-review action is not a local bridge receipt. A local bridge receipt is not a merge command.

### Binding stop rules

Do not:

```text
merge PR #14
mark PR #14 ready for review
claim watcher readiness
claim Codex execution
claim local tests passed
change NVDA trading runtime code
send real patch payloads through inline base64 comments
expand beyond bridge transport/receipt hardening and operating docs
```

Allowed now:

```text
edit bridge docs/plans/tests through GitHub connector
keep PR #14 draft
add PR comments and checklists
perform full static review of bridge files
prepare branch-as-payload and receipt contracts
prepare local-return runbook
```

Allowed only after local proof gates:

```text
live branch validation probe
live forced blob payload probe
Ready for review
merge consideration
```

## Gate 1 — Durable operating-channel manual

### Objective

Create or update the standalone operating manual:

```text
tools/ai_patch_bridge/docs/BRIDGE_OPERATING_CHANNELS_AND_RECEIPTS.md
```

### Acceptance checks

The document must describe:

1. Channel 1 — ChatGPT direct GitHub connector write.
2. Channel 2 — GitHub mobile human checkpoint.
3. Channel 3 — Local bridge / Ubuntu / Codex execution.
4. Branch-as-payload as the preferred normal workflow.
5. GitHub blob payload as fallback.
6. Inline base64 as tiny-probe compatibility only.
7. What each channel can do.
8. What each channel proves.
9. What each channel does not prove.
10. What user action is required on ChatGPT app, GitHub app, or local computer.
11. How receipts replace manual Ubuntu log inspection.
12. Merge-readiness rules.
13. Failure handling.

## Gate 2 — Receipt contract

### Objective

Define and implement the minimum GitHub-visible receipt shape.

### Required minimum receipt shape

```text
LOCAL_CODEX_RECEIPT_V1
source_comment_id: <control comment id or validation request id>
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

`checked` means an existing remote branch was fetched/inspected, required local checks passed, and no additional patch payload was applied.

### Timestamp rules

Use both machine and human timestamps.

Computer timestamp:

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

Australian date format is binding:

```text
07-04-2026 means 7 April 2026, not 4 July 2026.
```

Minute precision is required. Day-only or hour-only timestamps are insufficient.

Use IANA timezone:

```text
Australia/Melbourne
```

The receipt generator must not hard-code AEST permanently. It must derive AEST/AEDT and UTC offset from `Australia/Melbourne` at runtime.

As of 30-04-2026, Melbourne is on AEST, UTC+10, because Victoria daylight saving for the 2025-2026 season ended on Sunday 05-04-2026 when clocks moved back from AEDT to AEST.

### Example receipt timestamp

```text
computer_unix_epoch_s: 1777522620
computer_utc_minute: 2026-04-30T04:17Z
human_melbourne_minute: 30-04-2026 14:17 AEST
human_timezone: Australia/Melbourne
human_utc_offset: UTC+10
```

## Gate 3 — Branch-as-payload validation design

### Objective

Add or document a validation request path for an existing GitHub branch.

Minimum request shape:

```text
LOCAL_BRANCH_VALIDATE_V1
repo: <owner/repo>
base_branch: main
target_branch: work/...
source_pr: <PR number if available>
validation_mode: branch_checkout_test_repair_receipt
checks_required: <commands or default local checks>
```

Minimum behaviour:

```text
fetch origin
verify target branch exists on origin
checkout target branch locally
run declared checks
allow Codex repair only if checks or static validation fail and scope allows repair
push repaired branch if changed
post LOCAL_CODEX_RECEIPT_V1
```

Acceptance checks:

```text
no inline patch payload required
receipt posted to GitHub-visible surface
receipt includes target_branch and head_sha if pushed
failure receipt posted if branch missing, checks fail, dirty worktree blocks, or repair stops
```

## Gate 4 — Blob fallback transport design

### Objective

Keep GitHub blob transport as fallback for cases where a patch payload is unavoidable.

Acceptance checks:

```text
issue comment carries metadata only
blob SHA is fetched from GitHub
raw hash, gzip hash, raw bytes, gzip bytes are verified
fetched-comment validation occurs before watcher trust
inline payload is not used for real patches
```

## Gate 5 — PR #14 static audit

### Objective

Read every changed file in PR #14 and check against this plan.

In-scope files:

```text
tools/ai_patch_bridge/PLANS.md
tools/ai_patch_bridge/Makefile
tools/ai_patch_bridge/src/ai_patch_bridge/cli.py
tools/ai_patch_bridge/src/ai_patch_bridge/transport_hardening.py
tools/ai_patch_bridge/tests/test_transport_hardening.py
tools/ai_patch_bridge/tests/test_transport_hardening_edge_cases.py
tools/ai_patch_bridge/tests/test_receipt_timestamp_contract.py
tools/ai_patch_bridge/docs/TRANSPORT_AND_RECEIPT_HARDENING_IMPLEMENTATION_20260430.md
tools/ai_patch_bridge/docs/BRIDGE_OPERATING_CHANNELS_AND_RECEIPTS.md
```

Static audit checks:

```text
lane semantics unchanged
branch-as-payload primary documented
blob fallback documented
inline compatibility preserved only as probe/compatibility
blob metadata complete
GitHub blob create/fetch command shape internally consistent
fetch-back validation happens before receipt trust
receipt matching uses exact source_comment_id
receipt posting failure cannot be recorded as success
receipt timestamp fields are produced and visible
Makefile target has required arguments
docs match actual code
tests match planned behaviours
```

## Gate 6 — Static test hardening

### Objective

Harden tests without claiming local execution.

Allowed test additions:

```text
branch validation request parser
branch validation rejects missing target branch metadata
branch validation rejects non-work target branches unless rescue mode is explicit
CLI submit-and-wait argument path
invalid transport rejection
missing payload_blob_sha rejection
GitHub blob fetch encoding rejection
GitHub blob SHA mismatch rejection
receipt parser ignores wrong source_comment_id
receipt parser returns newest matching receipt
submit-and-wait returns timeout distinctly
post_verified_receipt retries before failure
receipt timestamp AEST case
receipt timestamp AEDT case
receipt-visible timestamp contract fields
```

## Gate 7 — Overlay-risk reduction

### Objective

Reduce brittle overlay risk without widening architecture.

Current known risk:

```text
transport_hardening.install() patches:
core.parse_ai_patch_body
core.make_ai_patch_comment
core._post_receipt
```

Allowed improvements:

```text
make overlay installation idempotent and tested
add tests that core.main still receives legacy commands
add tests that submit-and-wait bypasses legacy parser only where intended
document monkeypatch risk as a pre-merge validation item
```

Not allowed:

```text
large rewrite of core.py
new architecture unrelated to branch/blob/control-plane split
changing existing branch publication semantics without tests
changing lane policy without updating this plan
```

## Gate 8 — Documentation consistency

### Objective

Keep bridge documents mutually consistent.

Docs to review or update where mismatched:

```text
PLANS.md
README.md if tool allows safe update
docs/BRIDGE_OPERATING_CHANNELS_AND_RECEIPTS.md
docs/TRANSPORT_AND_RECEIPT_HARDENING_IMPLEMENTATION_20260430.md
docs/TRANSPORT_AND_RECEIPT_HARDENING_PLAN_20260429.md
docs/WATCHER_OPERATIONS.md
docs/EDGE_CASES_AND_BRANCH_LANES.md
docs/INSTALL_AI_PATCH_BRIDGE.md
```

Documentation gates:

```text
branch-as-payload primary described correctly
small inline path described as compatibility/probe only
large blob fallback path described correctly
submit/fetch-back/validate sequence described correctly
receipt polling described correctly
receipt timestamp contract described correctly
local proof state stated truthfully
local gates listed consistently
live probe requirements listed clearly
```

If a README update is blocked by tooling:

```text
Do not fight the tool. Record the blocked README update in PR notes and use dedicated docs instead.
```

## Gate 9 — PR hygiene and mobile checkpoint preparation

### Objective

Keep PR #14 usable from GitHub mobile without confusing user actions.

Safe GitHub-only work:

```text
keep PR #14 draft
update PR body if implementation changes
add closeout comments after each completed static pass
verify branch is not behind main
verify changed files remain under tools/ai_patch_bridge
verify superseded PRs remain closed
```

Mobile GitHub terms must be used exactly:

```text
Ready for review
Approve / Submit review
Merge
Close PR
```

Rules:

```text
Ready for review does not prove local validation.
Approval does not prove local validation.
Merge remains forbidden until required local gates pass unless the user explicitly overrides.
ChatGPT must not confuse Ready for review, Approve, and Merge.
```

## Gate 10 — Local-return runbook

### Objective

Prepare a deterministic sequence for when local validation starts.

Run from repo root:

```bash
make bridge-status
make -C tools/ai_patch_bridge test
make -C tools/ai_patch_bridge lint
make -C tools/ai_patch_bridge ai-bridge-scenarios
make -C tools/ai_patch_bridge ai-bridge-preflight
```

Only if those pass:

```text
branch-as-payload validation probe
forced blob payload probe
confirm receipts visible on GitHub issue #1 or PR comment surface
confirm source_comment_id or validation request correlation
confirm target branch pushed or validated
confirm local repo returned to main with clean worktree
```

Failure handling:

```text
If bridge-status is ON_LEGACY: stop and clean watcher state first.
If worktree is dirty: stop and inspect before running bridge.
If tests fail: do not run live probes.
If lint fails: patch bridge files only.
If branch validation probe fails: do not run blob probe.
If blob probe fails: do not merge.
If receipt is missing: ChatGPT polls GitHub before asking user for logs.
If receipt says log path is required: manual log inspection becomes allowed.
```

## Gate 11 — Closeout

### Objective

Close the tranche cleanly without pretending proof exists.

Required outputs:

```text
updated PLANS.md
BRIDGE_OPERATING_CHANNELS_AND_RECEIPTS.md
updated implementation doc
PR #14 static-review comment
Known / Unknown / Next Local Gate summary
```

Closeout state must say:

```text
static preparation: complete
local proof: pending until command output or GitHub receipt exists
PR state: draft
merge state: forbidden
```

## Known / Unknown template

### Known true

```text
PR branch exists
PR is draft
GitHub-only static edits can be performed
branch-as-payload is the preferred design
blob fallback remains useful
receipt contract is defined
local validation remains required
```

### Unknown until local output or receipt exists

```text
local watcher state
local worktree cleanliness
gh auth state on local machine
Codex version
local test results
branch validation probe result
live blob probe result
```

### Next local gate

```bash
make bridge-status
```

## Scenario A — direct GitHub PR

Use when the change is small, reviewable directly in GitHub, and does not require the local Linux environment.

- Promotion intent: `direct_pr`
- AI_PATCH_V1 executor: none
- Branch namespace: `work/...` if a branch is created
- Trust state: reviewed-only unless external tests ran
- Merge surface: GitHub PR or direct GitHub connector path

This scenario is outside the local bridge watcher.

## Scenario B — GitHub Action clean patch lane

Use when ChatGPT has generated a branch or patch intended for cloud application rather than local WSL/Codex processing.

- Promotion intent: `direct_pr`
- AI_PATCH_V1 executor: `github-action`
- Branch namespace: `work/...`
- Test policy: `not_run_allowed`
- Local watcher default: skip

## Scenario C — local Codex tested lane

Use when runtime code, tests, dependencies, pyproject settings, or local patch fitting matter.

- Promotion intent: `local_codex_execute`
- AI_PATCH_V1 executor: `local-codex`
- Branch namespace: `work/...`
- Test policy: `required`
- Preferred payload: branch-as-payload when the branch already exists
- Fallback payload: GitHub blob when a patch payload is unavoidable
- Inline payload: tiny probe only
- Local watcher default: process

The bridge must fetch `origin` before validating or creating the target branch so Codex starts from the latest GitHub state.

Scenario C is proven live through the repaired outer-bridge publication flow. See `docs/LIVE_SCENARIO_VERIFICATION_20260429.md`.

## Scenario D — long sandbox cumulative export

Use when ChatGPT has performed several internal sandbox branches and merges during one long run.

- Promotion intent: usually `local_codex_execute`
- AI_PATCH_V1 executor: usually `local-codex`
- Commit policy: `single_commit`
- Export shape: prefer branch-as-payload if GitHub branch can be created; otherwise one blob-backed cumulative patch from declared GitHub base to final sandbox state

Sandbox branch history is scratch history. Do not try to replay it unless the user explicitly asks for ordered patch-series support.

Scenario D is proven live for one cumulative payload producing one pushed branch commit containing multiple files.

## Scenario E — unfinished sandbox rescue

Use when sandbox work is valuable but incomplete, untested, or not ready for local execution.

- Promotion intent: `rescue_only`
- AI_PATCH_V1 executor: `rescue-branch`
- Branch namespace: `rescue/...`
- Test policy: `rescue_unvetted`
- Local watcher default: skip

A rescue branch is storage, not validation.

## Scenario F — remote patch failed, local Codex fallback

Use when a GitHub Action patch failed to apply or produced a branch that needs local fitting.

- New promotion intent: `local_codex_execute`
- New AI_PATCH_V1 executor: `local-codex`
- Branch namespace: `work/...`
- Preferred handoff: branch-as-payload validation of the failed branch or repaired branch
- Include the remote failure receipt or log in the local-Codex prompt where available

Do not keep retrying the same GitHub Action patch if the failure is contextual.

Scenario F is proven live as a local fallback lane.

## Scenario G — Linux unavailable, preserve work

Use when the user cannot reach the Linux/Codex environment during the original work session but later wants to preserve the work as unvetted rescue evidence.

- Promotion intent: `rescue_only`
- AI_PATCH_V1 executor: `rescue-branch`
- Branch namespace: `rescue/...`
- Test policy: `rescue_unvetted`
- Local watcher default: skip unless explicitly started with `--accepted-executor rescue-branch`

Later, local Codex or a human can inspect and promote through a normal `work/...` branch.

Scenario G is proven live for explicit rescue acceptance.

## Makefile scenario gates

The Makefile owns offline scenario checks:

```bash
make ai-bridge-scenarios
make ai-bridge-scenario-a
make ai-bridge-scenario-b
make ai-bridge-scenario-c
make ai-bridge-scenario-d
make ai-bridge-scenario-e
make ai-bridge-scenario-f
make ai-bridge-scenario-g
```

These targets do not require GitHub, Codex, or network access. They validate lane metadata, branch namespaces, and watcher filtering.

Live proof is separate from offline gates and is recorded in `docs/LIVE_SCENARIO_VERIFICATION_20260429.md`.
