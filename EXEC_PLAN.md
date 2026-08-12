# Gate-0 admission and recovery ExecPlan

**Authority:** explicitly user-authorised bounded Gate-0 admission/recovery tranche. This ExecPlan operationalises accepted authority only; it cannot create programme or domain authority.

## Scope and sequence

```text
accepted repair bc032b6987ab71cbba24c9e62394548e11d5b15c
-> governance-maintenance acceptance unit
-> independent review of the exact governance patch
-> accepted governance Git state
-> renew changed-hook trust
-> fresh static preflight
-> NEW arm + NEW nonce
-> fresh live Gate 0
-> parent probe
-> integration_auditor
-> semantic_reviewer
-> STOP live Codex
-> ordinary WSL derive / runtime validate / seal / admit / commit-admission
-> Gate 1A unlocked
```

No Raw Signal Gate-1+ work may begin before an admitted Gate-0 PASS. The required live role sequence remains parent probe -> `integration_auditor` -> `semantic_reviewer`.

## Current tranche boundary

This governance-maintenance thread performs no re-arm and no live Gate 0. It creates no new recovery architecture. Hook trust renewal, static preflight, a new arm and nonce, and all later stages require the accepted governance Git state and their separately authorised execution context.

## Universal failure path

```text
first failed or absent invariant
-> STOP
-> preserve exact failure evidence
-> bounded diagnosis/repair only under explicit authority
```

This ExecPlan is retired when Gate 0 closes or when a materially different authorised tranche begins. It is a current bounded plan, not a chronology or receipt ledger.
