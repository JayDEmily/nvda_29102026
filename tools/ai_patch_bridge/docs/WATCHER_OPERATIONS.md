# AI Patch Bridge watcher operations

## Purpose

This document records the human operating surface for the managed AI Patch Bridge watcher.

It replaces the temporary shell-wrapper workflow used during live testing.

## Operator commands

Run these from the repository root:

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

## What each command does

`make bridge-on`

- starts the managed watcher;
- stops older pasted shell watcher loops before starting;
- writes `.ai_patch_bridge/state/watcher.pid`;
- writes `.ai_patch_bridge/state/watcher_runtime.json`;
- writes `.ai_patch_bridge/state/watcher_status.txt`;
- appends to `.ai_patch_bridge/logs/watch.log`.

`make bridge-off`

- stops the managed watcher PID;
- stops older pasted shell watcher loops;
- writes an OFF runtime/status record.

`make bridge-status`

- prints one clear state;
- prints the current PID when managed watcher is alive;
- prints runtime JSON;
- prints current branch and dirty status;
- prints the recent watcher log tail.

`make bridge-dashboard`

- refreshes status every five seconds;
- is intended for a second terminal;
- is stopped with `Ctrl-C`;
- does not stop the watcher.

## Status meanings

```text
WATCHER: ON
WATCHER: OFF
WATCHER: ON_LEGACY
WATCHER: BROKEN
```

`WATCHER: ON` means the managed PID is alive and the watcher has written a current runtime record.

`WATCHER: OFF` means no managed watcher or legacy watcher loop is alive.

`WATCHER: ON_LEGACY` means an older pasted `while true ... ai_patch_bridge.cli once` loop is still alive. Run:

```bash
make bridge-off
```

`WATCHER: BROKEN` means the watcher control hash in `WATCHER_CONTROL.md` is missing or mismatched.

## Control contract

The control file is:

```text
tools/ai_patch_bridge/WATCHER_CONTROL.md
```

It contains:

```text
WATCHER_CONTROL_V1
repo: JayDEmily/nvda10
issue: 2
watcher_control_hash: sha256:2a9626937a131a7ff4472a8644664aa8f0b22eb240b8ea510b101cb6d6385ba1
allowed_actions: on, off, status, dashboard, tail
```

The hash is a local project-control key. It is not an internet security boundary.

## Normal flow

1. Start the watcher:

   ```bash
   make bridge-on
   ```

2. Open a second terminal and run:

   ```bash
   make bridge-dashboard
   ```

3. ChatGPT posts one `AI_PATCH_V1` inbox comment.

4. The watcher processes it and returns to `main`.

5. Check the pushed branch on GitHub.

## Do not do this

Do not paste ad hoc `nohup bash -lc 'while true ...'` watcher blocks into a terminal.

That workflow can leave invisible long-running loops that switch branches behind the user's back.
