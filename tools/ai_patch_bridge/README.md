# NVDA AI Patch Bridge Pack

This pack provides the repo-local bridge between ChatGPT, GitHub, GitHub mobile, local Ubuntu/WSL, and Codex.

## Start here

For workflow selection, start with:

```text
tools/ai_patch_bridge/docs/ASCII_WORKFLOW_FLOWCHART.md
tools/ai_patch_bridge/docs/WORKFLOW_DECISION_TREE.md
```

The ASCII flowchart is the first-read operational map. The decision-tree document expands the same rules in prose.

The user should not need to choose Git mechanics. The user only needs to state operational availability, such as:

```text
computer is off
computer is on
phone only
local repo is dirty
```

ChatGPT must then choose the safest lane automatically.

## Default workflow decision tree

| User state | Default lane | ChatGPT action | User action |
|---|---|---|---|
| Computer off | GitHub-only draft PR | Create safe branch, apply/queue work, open draft PR | Optional phone review / Ready / Merge |
| Phone only | GitHub mobile checkpoint | Keep work reviewable in GitHub PRs and comments | Tap Ready for review, Approve, Merge, or Close |
| Computer on and repo clean | Local bridge / Codex | Use watcher/Codex for local tests, repair, receipts | No terminal work unless a local-only gate fails |
| Computer on but repo dirty | Stop local automation | Do not run watcher; preserve work in GitHub branch/PR/payload queue | Later classify dirty tree |
| Patch supplied in chat | Separate patch branch or queue | Apply on separate branch if safe; otherwise queue patch artefact | Review / merge applied PR later |
| Existing branch needs proof | Branch-as-payload validation | Queue `LOCAL_BRANCH_VALIDATE_V1`; watcher later posts receipt | None until clean local gate |

One-line rule:

```text
If the user says computer off or phone only, create safe GitHub draft PRs and use mobile checkpoints.
If the user says computer on and clean, use local watcher/Codex receipts where proof matters.
If the repo is dirty, stop local automation and preserve work without running the watcher.
```

## Operating channels

See:

```text
tools/ai_patch_bridge/docs/BRIDGE_OPERATING_CHANNELS_AND_RECEIPTS.md
```

There are three valid channels:

```text
Channel 1 — ChatGPT direct GitHub connector write
Channel 2 — GitHub mobile human checkpoint
Channel 3 — Local bridge / Ubuntu / Codex execution
```

Each channel has a different proof surface.

A GitHub commit SHA proves GitHub accepted a write. It does not prove local tests passed.

A GitHub mobile Ready/Merge action proves the user advanced PR state. It does not prove local tests passed.

A `LOCAL_CODEX_RECEIPT_V1` proves only what that receipt explicitly says.

## Current transport rule

Do not use inline issue comments as the main patch data carrier.

Use:

```text
GitHub branch = preferred payload
GitHub blob or repo-file = fallback payload
GitHub comments = control and receipt plane
inline base64 = tiny compatibility probes only
```

This avoids the known failure mode:

```text
large inline base64+gzip issue comment
→ text mutation/truncation/format risk
→ strict base64 decode failure before Codex can help
```

## Proven local-Codex flow

The proven local-Codex flow is:

```text
ChatGPT posts one AI_PATCH_V1 comment
→ local WSL/Linux bridge reads the GitHub issue inbox
→ bridge decodes and verifies the patch payload
→ bridge creates the declared target branch from origin/<base_branch>
→ Codex CLI applies/fits the patch and runs declared checks
→ Codex writes codex_receipt.md
→ outer bridge re-runs declared checks
→ outer bridge stages decoded patch paths only
→ outer bridge creates the commit and publishes the branch
→ outer bridge verifies the remote branch head
→ outer bridge posts LOCAL_CODEX_RECEIPT_V1 back to the inbox
```

Codex does not own the final source-control publication step. Live Scenario C testing showed Codex may run with `.git` mounted read-only. The outer bridge owns staging, commit creation, branch publication, and final remote-head verification.

## GitHub mobile workflow

GitHub mobile is a valid checkpoint lane.

Allowed mobile actions:

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
Merge is allowed only after explicit user instruction or documented gate acceptance.
```

A phone-only patch workflow is valid when the change is suitable for GitHub-only handling:

```text
ChatGPT creates a separate branch
→ ChatGPT opens a draft PR
→ user reviews / marks ready / merges in GitHub mobile
```

## Human watcher controls

Use the root Makefile commands from the repository root:

```bash
make bridge-on
make bridge-off
make bridge-status
make bridge-dashboard
```

Compatibility commands are also supported:

```bash
make bridge on
make bridge off
make watch status
make watch dashboard
```

Bridge-local controls from `tools/ai_patch_bridge` include:

```bash
make ai-bridge-watch-on
make ai-bridge-watch-off
make ai-bridge-watch-status
make ai-bridge-watch-dashboard
```

`make bridge-on` or `make ai-bridge-watch-on` starts the managed watcher. `make bridge-off` or `make ai-bridge-watch-off` stops the managed watcher and any older pasted shell watcher loops. Status commands print an explicit `WATCHER: ON`, `WATCHER: OFF`, `WATCHER: ON_LEGACY`, or `WATCHER: BROKEN` state.

The watcher is controlled by:

```text
tools/ai_patch_bridge/WATCHER_CONTROL.md
tools/ai_patch_bridge/scripts/watch_control.sh
```

Do not operate the watcher by pasting shell loops into the terminal.

## Dirty repo rule

If the local repo is dirty, the local automation lane is closed.

Correct action:

```text
stop watcher
preserve work in GitHub branch, PR, or payload queue
wait for clean-state classification
```

Do not leave the watcher running against a dirty mixed-scope worktree.

## Lane policy

See:

```text
tools/ai_patch_bridge/PLANS.md
tools/ai_patch_bridge/docs/EDGE_CASES_AND_BRANCH_LANES.md
tools/ai_patch_bridge/docs/ASCII_WORKFLOW_FLOWCHART.md
tools/ai_patch_bridge/docs/WORKFLOW_DECISION_TREE.md
```

Current lanes:

- `local-codex` — serious local execution on `work/...` branches. The local bridge consumes this lane by default.
- `github-action` — cloud patch application on `work/...` branches. The local bridge skips this lane by default.
- `rescue-branch` — unvetted preservation on `rescue/...` branches. The local bridge skips this lane unless explicitly started with `--accepted-executor rescue-branch`.

## Scenario gates

Offline lane checks:

```bash
make ai-bridge-scenarios
```

Live scenario evidence is recorded in:

```text
tools/ai_patch_bridge/docs/LIVE_SCENARIO_VERIFICATION_20260429.md
```

## Local readiness gate

Before running the live bridge:

```bash
make ai-bridge-preflight
```

The preflight checks Python, Git, GitHub CLI auth, Codex CLI version, clean Git state, remote origin, and `git fetch origin`.

## Merge rule

Do not merge bridge PRs until the required proof surface exists.

For GitHub-only governance/doc patches, a mobile Ready/Merge checkpoint may be enough if the user explicitly accepts that proof level.

For bridge/runtime/local-proof work, require local gates and/or `LOCAL_CODEX_RECEIPT_V1` before merge unless the user explicitly overrides.
