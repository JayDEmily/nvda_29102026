# Gate 0 bootstrap and empirical runbook

**Purpose:** prove only the exact runtime/control capability required to unlock Gate 1A. Gate 0 performs no Raw Signal semantic work and no persistent model-authored project mutation.

## Authority and stop rule

`docs/governance/GATE0_ADMISSION_MANIFEST.json` is the tracked Gate 0 proposition/policy. The protected arm record created by ordinary WSL binds that policy to the exact clean branch, HEAD, guarded hashes, and run nonce.

At the first absent or failed invariant: **STOP LIVE EXECUTION**. Preserve the last proved state and first unmet invariant. Do not request the next child, derive downstream evidence, or redesign an unreached stage.

## Phase A — ordinary WSL static admission and arm

Run from the exact native-WSL repository intended for admission:

```bash
pwd -P
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 --untracked-files=all
uv sync --locked --extra dev --offline
uv run python tools/validate_architecture.py
uv run python tools/validate_gate0.py --static
uv run python tools/gate0_runtime_evidence.py arm
```

PASS requires native Linux/WSL policy, a clean worktree, parseable admitted control files, exact guarded hashes, and a protected arm record under Git metadata. After arming, do not edit the repository.

## Phase B — Desktop preparation by the human/operator

1. Confirm the ChatGPT desktop **Codex agent** is set to WSL. If changing from Windows-native to WSL, restart the app before the run.
2. Open the exact WSL project path and establish project trust.
3. Review/trust the exact current non-managed project hooks and account for any other matching user/system/plugin hook sources in the Desktop app's actual Codex configuration home.
4. Start a fresh Gate 0 chat/run after arm and trust actions.
5. Select `read-only` sandbox mode with `on-request` approvals.

The integrated terminal is configured independently from the agent and is not evidence that the agent runtime is WSL.

## Phase C — live Gate 0

### C1 SessionStart and parent probe

The trusted `SessionStart` hook must bind the session to the protected arm and add one exact nonce-bound parent probe command as developer context. The human approves **only that exact command**.

The parent executes the command exactly once. PASS requires the machine-readable probe result to prove the admitted read-only boundary. If running it requires a broader filesystem capability than the boundary being measured, Gate 0 fails.

### C2 integration_auditor

Spawn exactly one fresh `integration_auditor` for the authenticated capability-probe task only. Require the protected `SubagentStart`, approve only the exact child nonce-bound probe command, require probe PASS, then require a matching clean `SubagentStop`.

No source pre-read or semantic-index work occurs during this capability probe.

### C3 semantic_reviewer

Only after C2 PASS, repeat the same bounded capability probe for exactly one fresh `semantic_reviewer`. Require `SubagentStart` -> exact approved probe PASS -> matching `SubagentStop`.

### C4 stop live Codex

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

Hooks are evidence binders/observers. They never implement automatic final-`SubagentStop` closure or final admission.

## PASS scope

A PASS proves only the exact parent + `integration_auditor` + `semantic_reviewer` runtime/control proposition bound to the exact armed bytes. It does not prove Raw Signal semantic correctness, the five later role capabilities, write-bearing rollback, prompt-cache behaviour, or autonomous recovery.
