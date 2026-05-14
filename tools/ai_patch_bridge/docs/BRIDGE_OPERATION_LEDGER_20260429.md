# Bridge operation ledger — 2026-04-29

## Scope

This ledger records the bridge work completed during the live setup and managed-watcher conversion.

## Proven path

The final proven path is:

```text
ChatGPT posts one AI_PATCH_V1 comment
→ GitHub issue #1 acts as AI_PATCH_INBOX
→ managed local watcher reads the inbox
→ bridge verifies the payload
→ bridge creates the target branch from origin/main
→ Codex applies or fits the patch
→ Codex runs declared checks
→ Codex writes codex_receipt.md
→ outer bridge re-runs checks
→ outer bridge stages decoded patch paths
→ outer bridge commits and pushes the target branch
→ outer bridge verifies remote branch head
→ outer bridge posts LOCAL_CODEX_RECEIPT_V1
→ local repo returns to main
```

## Merged work

- PR #4 merged the live scenario verification documentation.
- PR #7 merged the Makefile-controlled watcher surface.
- A follow-up main commit changed watcher launch to `nohup bash "$0" run-loop` so the script does not depend on executable file mode.

## Managed watcher commands

From the repository root:

```bash
make bridge-on
make bridge-off
make bridge-status
make bridge-dashboard
```

Compatibility commands:

```bash
make bridge on
make bridge off
make watch status
make watch dashboard
```

## Verified managed watcher state

The managed watcher was verified with:

```text
WATCHER: ON
pid: present
last_once_exit: 0
repo: JayDEmily/NVIDIA9_remotetest
branch: main
status: clean
```

## Managed watcher live probe

The watcher consumed an `AI_PATCH_V1` inbox comment and published:

```text
work/managed-watcher-live-probe-20260429
```

That branch added:

```text
tools/ai_patch_bridge/docs/probes/MANAGED_WATCHER_LIVE_PROBE_20260429.md
```

This branch is evidence only. Do not merge it as product work.

## Defects found and resolved

### Raw watcher died on GitHub timeout

The raw `ai-bridge-watch` Python loop exited on transient GitHub API timeout.

Resolution: normal operation now uses the managed watcher wrapper, which repeatedly runs `once` and keeps going after transient failures.

### Pasted watcher loops were invisible

The temporary shell wrapper could stay alive and switch the repo back to `main`.

Resolution: `make bridge-status` detects old pasted loops as `WATCHER: ON_LEGACY`, and `make bridge-off` stops them.

### Script mode was not executable

GitHub-created `watch_control.sh` did not have executable mode, so `nohup "$0" run-loop` failed with permission denied.

Resolution: watcher launch now uses:

```bash
nohup bash "$0" run-loop
```

## Open item

PR #6 is an older watcher-operations documentation PR from the transitional shell-wrapper workflow.

It is superseded by the Makefile-controlled watcher work. It should be closed, not merged.

## Rule going forward

Use one multi-file `AI_PATCH_V1` patch for coherent doc/code updates. Avoid serial file-by-file GitHub connector edits unless the change is genuinely a single-file correction.
