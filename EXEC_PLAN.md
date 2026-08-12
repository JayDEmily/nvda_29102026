# Gate-0 permission-boundary recovery ExecPlan

**Authority:** explicitly user-authorised bounded Gate-0 admission/recovery tranche. This ExecPlan operationalises accepted authority only; it cannot create programme or domain authority.

## Established first failure

```text
accepted main fe4d696b9a7c5e05143e0491223f310088b3185e
-> armed nonce 0fa7de5537d59636c12c08173b7ba4c9
-> SessionStart effective danger-full-access / never
-> parent empirical probe found repository, .git, $HOME and /tmp writable
-> WRITE_BOUNDARY first failure
-> failed evidence preserved and active arm retired
```

This is an `OBSERVATION`, not a hypothesis. The failed session rollout records a disabled permission profile with active profile `:danger-full-access`, and its turn context records effective `danger-full-access` with `never` approvals. The trusted `SessionStart` hook independently recorded `permission_mode = bypassPermissions`.

## Authorised recovery sequence

```text
preserved failed evidence
-> direct rollout/config/documentation diagnosis
-> smallest permission-boundary correction
-> fail-earlier hook guard without weakening the empirical probe
-> deterministic validation
-> semantic reread
-> independent read-only control-plane review
-> candidate commit
-> READY_FOR_INDEPENDENT_CONTROL_PLANE_REVIEW or one irreducible UI action
```

The repair may update `EXEC_PLAN.md`, `docs/orchestration/BOOTSTRAP.md`, project-local Codex control files, Gate-0 evidence tooling, and bounded tests. Root `AGENTS.md` and `PLANS.md` remain frozen.

## Current tranche boundary

This recovery does not re-arm and does not run live Gate 0. It performs no Raw Signal semantic work and creates no new recovery authority. A later live run still requires accepted repair Git state, renewed trust for changed hooks, fresh static preflight, a new arm and nonce, the required parent probe, `integration_auditor`, and `semantic_reviewer` sequence, then ordinary-WSL closure.

## Universal failure path

```text
first failed or absent invariant
-> STOP
-> preserve exact failure evidence
-> bounded diagnosis/repair only under explicit authority
```

This ExecPlan is retired when this permission-boundary recovery is accepted or when a materially different authorised tranche begins. It is a current bounded plan, not a chronology or receipt ledger.
