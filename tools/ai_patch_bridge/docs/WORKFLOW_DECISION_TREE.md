# AI Patch Bridge workflow decision tree

## Purpose

This document defines the default workflow selection rules for ChatGPT, GitHub mobile, local Ubuntu, Codex, and the AI Patch Bridge.

The user should not need to choose Git mechanics.

The user only needs to state operational availability, such as:

```text
computer is off
computer is on
phone only
local repo is dirty
```

ChatGPT must then choose the safest lane and execute within that lane.

## Default rule

Do not ask the user to drive terminal commands unless a local-only gate is genuinely required.

Prefer this order:

```text
1. GitHub-only draft PR when the computer is off or the user is phone-only.
2. GitHub mobile checkpoint when the user can tap Ready for review or Merge.
3. Local watcher/Codex only when the local repo is clean and local proof is required.
4. Queue/preserve payload when apply or validation cannot safely run now.
```

## User input to lane mapping

| User state | Default lane | What ChatGPT does | What the user may do |
|---|---|---|---|
| Computer off | GitHub-only draft PR | create branch, apply safe changes, open draft PR, record proof state | inspect / Ready / Merge from phone if comfortable |
| Phone only | GitHub mobile checkpoint | keep work reviewable in GitHub PRs and comments | tap Ready for review, Approve, Merge, or Close |
| Computer on and repo clean | Local bridge/Codex lane | use watcher or Codex for local tests, repair, receipts | no terminal work unless a gate fails and cannot be observed remotely |
| Computer on but repo dirty | Stop local automation | avoid watcher/probe; preserve work in GitHub; request or defer dirty-tree classification | do not leave watcher running |
| Patch supplied in chat | Separate patch branch or payload queue | apply on separate branch if safe; otherwise store patch as artefact | review / merge applied PR from phone later |
| Large generated patch | Blob or repo-file payload | avoid inline base64 comments; use blob/file/control comment | no manual Git work |
| Existing GitHub branch needs testing | Branch-as-payload validation | queue `LOCAL_BRANCH_VALIDATE_V1`; watcher later posts receipt | none until local clean-state gate |
| Connector write fails | Smaller write or payload queue | retry smaller unit, or store artefact and open draft PR | no terminal work |

## Hard safety boundaries

ChatGPT must not:

```text
merge without explicit user instruction
force-push unless explicitly authorised
run or rely on watcher when the last known local repo state is dirty
apply unrelated work to PR #14
mix bridge-work branches with governance-work branches
claim local tests passed without command output or receipt
claim a patch applied if only queued as payload
use inline base64 comments for real patch payloads
```

## GitHub-only draft PR lane

Use when the computer is off, unreachable, or the user is phone-only.

Flow:

```text
create non-orphan work branch from current main or declared base
apply small/safe changes through GitHub connector
open draft PR
record changed files and proof limitations
leave merge decision to user or explicit later instruction
```

This lane proves only:

```text
GitHub accepted the branch/commits/PR
```

It does not prove:

```text
local tests passed
watcher ran
Codex repaired anything
runtime behaviour works
```

## GitHub mobile checkpoint lane

Use when the user can use the GitHub app but not the computer.

Allowed user actions:

```text
Ready for review
Approve / Submit review
Merge
Close PR
```

Meanings:

```text
Ready for review: converts draft PR into normal PR.
Approve / Submit review: satisfies a review gate if required.
Merge: integrates the branch into the base branch.
Close PR: closes without merging.
```

Rules:

```text
Ready for review is not local validation.
Approval is not local validation.
Merge is allowed only after explicit user instruction or documented gate acceptance.
```

## Local watcher/Codex lane

Use only when local proof is required and the local repo is clean.

Minimum clean-state gate:

```bash
git status --short
make ai-bridge-watch-status
```

Required state:

```text
worktree clean
watcher off before setup, or deliberately on for a specific probe
branch known
```

Then run only the required local lane:

```text
branch-as-payload validation
blob fallback validation
Codex repair/test/push
```

The proof surface is:

```text
LOCAL_CODEX_RECEIPT_V1
```

## Dirty local repo rule

If the repo is dirty, the local automation lane is closed.

Do not run live watcher/probe work when status includes modified, deleted, or untracked files that are not intentionally part of the current lane.

Correct action:

```text
stop watcher
preserve work in GitHub branch, PR, or payload queue
wait for clean-state classification
```

## Patch handling rule

When the user provides a patch:

```text
1. Never apply directly to main.
2. Never apply to an unrelated active PR.
3. Create a separate non-orphan work branch.
4. If safe, apply the patch there and open a draft PR.
5. If not safe, store the patch as a payload artefact and open a queue PR.
6. Label the result honestly as applied or queued.
```

Phone-compatible result:

```text
Applied patch PR: user can Ready/Merge from GitHub mobile.
Queued patch PR: user can preserve or later route to Codex/local repair.
```

## Branch-as-payload rule

When ChatGPT can create or update a GitHub branch directly, the branch is the payload.

```text
payload = GitHub branch
control = PR or LOCAL_BRANCH_VALIDATE_V1 comment
receipt = LOCAL_CODEX_RECEIPT_V1
```

This is preferred over carrying large patches inside issue comments.

## Blob fallback rule

Use GitHub blob or repo-file payloads when a patch must be transported but cannot safely be applied directly through GitHub connector writes.

Inline base64 comments are allowed only for tiny compatibility probes.

## Assistant behaviour requirements

ChatGPT must:

```text
choose the lane automatically from the user's availability state
keep work branch-scoped
state what was actually done
record proof limitations
prefer draft PRs over terminal tasks for phone-only users
use PR comments or docs as durable receipts
avoid pushing terminal work onto the user unless unavoidable
```

## Current proven workflow examples

### Phone-only merge example

A patch was applied on a separate work branch and opened as a draft PR. The user marked it ready and merged it from the GitHub mobile app.

This proves:

```text
GitHub-only branch + draft PR + mobile Ready/Merge is a valid workflow for suitable governance/doc patches.
```

It does not prove local runtime tests.

### Bridge hardening example

Bridge work remains on a separate PR and requires local watcher receipt proof before merge.

This proves:

```text
some work is GitHub-mobile mergeable
some work still needs local watcher/Codex proof
```

The lane depends on proof requirement, not user patience.

## One-line operating rule

```text
If the user says computer off or phone only, create safe GitHub draft PRs and use mobile checkpoints.
If the user says computer on and clean, use local watcher/Codex receipts where proof matters.
If the repo is dirty, stop local automation and preserve work without running the watcher.
```
