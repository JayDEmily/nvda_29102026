# Control-Surface Transition ExecPlan

## Status

**Status:** completed and closed by the checkpoint commit carrying this plan
**Date:** 2026-08-03
**Baseline:** `74d2f2c3fa403538fd11e428a928c5de517dc165`
**Branch:** `main`
**Current unit:** none

## Objective

Close the completed Gate C and continuation control programme without deleting its accepted history, restore programme-neutral routing, reconcile executable control proof, and leave one clean committed checkpoint on `main` with no active task-specific ExecPlan.

## Authority

- direct user instruction in the current thread;
- `AGENTS.md`;
- `PLANS.md`;
- `00_TASK/PROJECT_EXECUTION_METHOD.md` where higher authority is silent;
- routed process, testing/promotion and architecture working documents;
- accepted Git history through `74d2f2c`.

## Scope

In scope:

- generalise `PLANS.md` so it does not hard-code the completed programme;
- reduce `ROADMAP_LEDGER_V2.md` to the mutable live state and active-plan pointer;
- retain the normative routing index while removing continuation-era active routing;
- mark `project_control/canonical_project_manager/` and its three programme entry documents completed and retired in place;
- record Gate C, continuation and semantic repairs as closed;
- reconcile live process, testing/promotion and architecture overlays;
- reconcile `validate_active_control` and its admitted Tier B contract;
- close the M03→M05 final archive receipt contradiction;
- commit the accepted transition to `main`.

Out of scope:

- runtime, domain, packet, persistence or feature behaviour;
- reopening Gate C or any completed repair;
- defining the substantive successor development phase;
- deleting or path-moving historical programme evidence;
- pushing or publishing to an external remote.

## Invariants

- `README.md` and `AGENTS.md` remain unchanged.
- Historical programme evidence remains available at its current paths.
- No completed plan is treated as current execution authority.
- `ROADMAP_LEDGER_V2.md` remains the sole mutable live pointer.
- Zero active task-specific ExecPlans is a lawful current state between phases.
- Existing test propositions are preserved or strengthened; no skip, xfail, weakening or proof suppression is permitted.

## Acceptance units

### Unit A — standing and live routing

Pass when `PLANS.md`, the live roadmap, the routing index and the current process/architecture overlays agree that Gate C and continuation are closed, the canonical Project Manager tree is historical, and no task-specific ExecPlan is active.

### Unit B — executable control proof

Pass when `TP-CONTROL-001`, `scripts/proof_authority.py` and the admitted Tier B contract agree that the live state may contain zero or one active task-specific ExecPlan and reject unreconciled routing.

### Unit C — historical closeout and checkpoint

Pass when the completed programme entry files are marked retired, the M03→M05 archive receipt is recorded against the supplied full-history archive, validation passes, this plan is closed, and the resulting worktree is committed and clean on `main`.

## Required reads

Recorded in `FULL_READ_MANIFEST.tsv`.

## Validation

- `git diff --check`
- focused Tier B proof-authority contract
- `python scripts/proof_authority.py --check --json`
- deterministic routing/reference checks for current surfaces
- Git branch, status and committed diff inspection

## Progress

- [x] Accepted baseline and absence of an existing `main` branch established.
- [x] Required current controls and directly affected files read.
- [x] `main` created at exact accepted baseline `74d2f2c`.
- [x] Unit A
- [x] Unit B
- [x] Unit C

## Decisions

- The completed `project_control/canonical_project_manager/` tree will be retired in place, not deleted or moved.
- The normative routing index remains standing; only its completed-programme routing is retired.
- The successor substantive phase is not invented in this transition.

## Roadblocks

None. The extracted repository did not include a project `.venv`; pinned Black and Ruff were therefore installed from the supplied offline development wheelhouse into an external temporary environment.

## Unknowns

None currently material to this bounded transition.

## Closeout

Completed. The live route now contains zero active task-specific ExecPlans, the completed canonical Project Manager programme is retired in place, executable proof is programme-neutral, the final repair archive receipt is closed, and `VALIDATION_SUMMARY.md` records the pre-commit evidence. The exact clean commit must pass signed `alpha_current` promotion before the acceptance tag is created.
