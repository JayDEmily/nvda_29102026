# AI Patch Bridge edge cases and branch lanes

## Purpose

This note records the bridge lane policy for sandbox-to-local and GitHub-to-local work.

The bridge supports three distinct lanes:

1. `local-codex` — serious local execution on WSL/Linux.
2. `github-action` — cloud patch application through GitHub Actions or another non-local executor.
3. `rescue-branch` — unvetted preservation of sandbox work.

## Local-Codex execution split

The live bridge uses a split execution model:

```text
Codex applies/fits the decoded patch, runs declared checks, and writes codex_receipt.md.
The outer bridge re-runs declared checks, stages decoded patch paths, creates the commit, pushes the target branch, verifies origin, and posts LOCAL_CODEX_RECEIPT_V1.
```

This split exists because live testing showed Codex can run with `.git` mounted read-only inside its sandbox. Git publication is therefore owned by the outer bridge process.

## Managed watcher surface

The managed watcher is the preferred local execution surface.

Human operator commands from the repository root:

```bash
make bridge-on
make bridge-off
make bridge-status
make bridge-dashboard
```

Do not run pasted `while true` shell watcher loops. They are treated as legacy processes. The managed watcher status command reports them as `WATCHER: ON_LEGACY`, and `make bridge-off` stops them.

The watcher control hash lives in `tools/ai_patch_bridge/WATCHER_CONTROL.md`. It is a project-local control contract, not an internet security boundary.

The raw `ai-bridge-watch` target remains available for direct Python watcher testing, but normal operation uses the managed Makefile commands above.

## Lane 1: local-codex

Use this when the user's local Linux environment is available and the work should be fitted, tested, committed, and pushed through the local bridge.

Required branch namespace:

```text
work/<task-name>
```

Required default metadata:

```text
executor: local-codex
commit_policy: single_commit
test_policy: required
```

The local bridge consumes this lane by default.

## Lane 2: github-action

Use this when a patch is intended for cloud patch application rather than local bridge processing.

Required branch namespace:

```text
work/<task-name>
```

Required metadata:

```text
executor: github-action
commit_policy: single_commit
test_policy: not_run_allowed
```

The local bridge skips this lane by default so it does not compete with the cloud lane.

## Lane 3: rescue-branch

Use this only to preserve temporary or unfinished sandbox work when local Linux/Codex execution is not available or when the user explicitly wants to avoid losing sandbox state.

Required branch namespace:

```text
rescue/<task-name>
```

Required metadata:

```text
executor: rescue-branch
commit_policy: single_commit
test_policy: rescue_unvetted
```

A rescue branch is storage, not validation.

A rescue branch must not be treated as tested, promoted, or merge-ready unless a later local-Codex or human-reviewed process promotes it through a normal work branch.

The local bridge skips this lane by default. It may process this lane only when explicitly started with:

```bash
--accepted-executor rescue-branch
```

or with both lanes:

```bash
--accepted-executor local-codex --accepted-executor rescue-branch
```

## Long sandbox runs with several internal work branches

When ChatGPT performs several internal sandbox branches and commits, those internal branches are scratch history.

The export surface is one cumulative patch against the declared GitHub base SHA.

Do not try to reproduce every internal sandbox branch unless the user explicitly asks for ordered patch-series support.

Current bridge support:

```text
commit_policy: single_commit
```

Reserved future support:

```text
commit_policy: patch_series
```

`patch_series` is recognised as metadata but is not implemented as an execution protocol in this pack.

## Practical rule

For normal serious work:

```text
executor: local-codex
branch: work/...
test_policy: required
```

For cloud patch application:

```text
executor: github-action
branch: work/...
test_policy: not_run_allowed
```

For save-my-work preservation:

```text
executor: rescue-branch
branch: rescue/...
test_policy: rescue_unvetted
```

## Scenario Makefile gates

Each scenario has an offline Makefile gate. These gates are not live GitHub or Codex tests. They validate lane classification, branch namespace, test policy, and watcher ownership.

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

Scenario meaning:

- A: direct GitHub PR lane; no AI_PATCH_V1 local watcher payload.
- B: cloud patch lane; local watcher skips it by default.
- C: local Codex tested lane; local watcher consumes it by default and outer bridge publishes after Codex writes a receipt.
- D: long sandbox cumulative export; one final patch, not sandbox branch replay.
- E: unfinished rescue branch; `rescue/...`, unvetted, skipped by default.
- F: remote patch failure falls back to local Codex.
- G: Linux unavailable preservation uses rescue branch and requires explicit rescue acceptance.

## Remote freshness rule

The local executor must start from latest GitHub state. ChatGPT may have already committed directly to GitHub before a later local-Codex message is sent.

The bridge fetches `origin` before creating the target branch and creates the branch from `origin/<base_branch>`, not from a potentially stale local `main`.

Codex must not assume that local `main` is current.
