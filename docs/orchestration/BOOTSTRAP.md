# Gate 0 bootstrap and empirical runbook

**Purpose:** prove only the exact runtime/control capability required to unlock Gate 1A. Gate 0 performs no Raw Signal semantic work and no persistent model-authored project mutation.

## Authority and stop rule

`docs/governance/GATE0_ADMISSION_MANIFEST.json` is the tracked Gate 0 proposition/policy. The protected arm record created by ordinary WSL binds that policy to the exact clean branch, HEAD, guarded hashes, and run nonce.

At the first absent or failed invariant: **STOP LIVE EXECUTION**. The protected Gate 0 state records the first failure. After that record exists, every later hook-observable local tool call is denied and the run cannot derive PASS. Do not request the next child, derive downstream evidence, or redesign an unreached stage.

## Phase A — ordinary WSL static admission and arm

Run from the exact native-WSL repository intended for admission:

```bash
pwd -P
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 --untracked-files=all
bash tools/bootstrap_preflight.sh
```

PASS requires native Linux/WSL policy, a clean worktree, parseable admitted control files, exact guarded hashes, and a protected arm record under Git metadata. After arming, do not edit the repository.

## Phase B — Desktop preparation by the human/operator

1. Confirm the ChatGPT desktop **Codex agent** is set to WSL. If changing from Windows-native to WSL, restart the app before the run.
2. Open the exact WSL project path and establish project trust.
3. Review/trust the exact current non-managed project hooks and account for any other matching user/system/plugin hook sources in the Desktop app's actual Codex configuration home.
4. Confirm the live tool surface does not expose a specialised hook-exempt tool capable of doing the semantic work that Gate 0 forbids. If such a tool is exposed and cannot be disabled, **BLOCK Gate 0 as a product-mechanism Unknown**; do not weaken the proposition.
5. Start a fresh Gate 0 chat/run after arm and trust actions.
6. Select `read-only` sandbox mode with `on-request` approvals.

The repository configuration disables Codex web search, app/connector tools, the local `view_image` attachment tool, and the remote plugin catalogue for this execution surface. `PreToolUse`/`PostToolUse` match every supported local tool path. During an armed run, the Gate 0 policy denies every hook-observable local tool except the exact nonce-bound mechanical probe, the exact next `spawn_agent` call, and `wait_agent` used only to await an already-authorised child.

The integrated terminal is configured independently from the agent and is not evidence that the agent runtime is WSL.

## Phase C — live Gate 0

### C1 SessionStart and parent probe

The trusted `SessionStart` hook must bind the session to the protected arm and add one exact nonce-bound parent probe command as developer context. The human approves **only that exact command**.

The parent executes the command exactly once. PASS requires the machine-readable probe result to prove the admitted read-only boundary. If running it requires a broader filesystem capability than the boundary being measured, Gate 0 fails.

### C2 integration_auditor

After the parent probe passes, the parent requests exactly one `spawn_agent` call with `agent_type = "integration_auditor"`. The armed `PreToolUse` hook must authenticate that exact next role and persist a `SpawnRequest` before the spawn is allowed.

The subsequent protected `SubagentStart` must match that recorded request. The start hook injects the exact child nonce-bound probe command. Approve only that exact command, require probe PASS, then require a matching clean `SubagentStop`. The parent may use `wait_agent` only to await the already-authorised child; it may not send follow-up work or resume another agent.

No source pre-read or semantic-index work occurs during this capability probe.

### C3 semantic_reviewer

Only after C2 PASS, repeat the same bounded sequence for exactly one fresh `semantic_reviewer`:

`SpawnRequest -> SubagentStart -> exact approved probe PASS -> SubagentStop`.

### C4 current Codex lifecycle limitation

`SubagentStart` is evidence that a child already started; the lifecycle hook cannot undo that creation. Therefore invalid role/order is prevented earlier at the `spawn_agent` `PreToolUse` boundary. If an unexpected child nevertheless appears (for example through a product path that did not expose the expected pre-spawn control), the hook records first failure, tells the child to use no tools and stop, and all later hook-observable local tools are denied. The run is permanently non-admissible.

This is intentionally fail-closed. If the current Desktop build does not expose a selectable custom `agent_type` at the pre-spawn tool boundary, Gate 0 fails at the first spawn invariant. Do not substitute `task_name` or a generic child and call it equivalent.

### C5 stop live Codex

After both children stop cleanly, **STOP** the live Gate 0 interaction. The model does not run derive, strict validation, seal, admission, or Gate 1A work.

## Phase D — ordinary WSL closure and admission

From ordinary WSL, against the unchanged armed repository:

```bash
uv run python tools/gate0_runtime_evidence.py derive
uv run python tools/validate_gate0.py --runtime
uv run python tools/gate0_runtime_evidence.py seal
uv run python tools/gate0_runtime_evidence.py admit
```

Only these ordinary-WSL operations may turn successful protected lifecycle evidence into an explicit `GATE0_PASS` admission record and advance `ADMITTED_STATE.json` to unlock Gate 1A.

Hooks are evidence binders/guards. They never implement automatic final-`SubagentStop` closure or final admission.

## PASS scope

A PASS proves only the exact parent + `integration_auditor` + `semantic_reviewer` runtime/control proposition bound to the exact armed bytes. It does not prove Raw Signal semantic correctness, the five later role capabilities, write-bearing rollback, prompt-cache behaviour, or autonomous recovery.
