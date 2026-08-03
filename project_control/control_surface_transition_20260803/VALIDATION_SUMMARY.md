# Control-Surface Transition — Validation Summary

## Outcome

The completed Gate C, continuation-readiness and semantic-continuity programme is retired from current execution authority without deleting or moving its historical evidence. The standing route now separates:

- `PLANS.md`: programme-neutral plan-selection law;
- `ROADMAP_LEDGER_V2.md`: compact current state and active-plan pointer;
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`: normative-document retrieval;
- one task-specific ExecPlan when the roadmap names one;
- `project_control/canonical_project_manager/`: completed historical programme record.

The final live state contains no active task-specific ExecPlan. `README.md` and `AGENTS.md` are unchanged.

## Behavioural proof change

`TP-CONTROL-001` and `scripts/proof_authority.py::validate_active_control` now admit exactly two programme-neutral live states:

1. `Active ExecPlan | none`, reconciled with the process overlay; or
2. one safe repository-relative plan path, reconciled with one existing plan carrying an active status and the exact process declaration.

Legacy control fixtures remain supported only when the newer `Active ExecPlan` roadmap row is absent. The existing proposition that live control surfaces resolve to one reconciled state is preserved and strengthened; no test was skipped, weakened, retired or redirected.

## Validation executed before checkpoint commit

| Check | Command | Result |
|---|---|---|
| Diff hygiene | `git diff --check` | PASS |
| Focused proof-authority contract | `python -m pytest -q tests/tier_b/proof_model/test_proof_authority_contract.py` | PASS — 23 passed |
| Complete physical Tier B | `python -m pytest -q tests/tier_b` | PASS — 96 passed |
| Authority model | `python scripts/proof_authority.py --check --json` | PASS — 201 families, 73 proof blocks, 203 paths |
| Manifest proof-block structure | `python scripts/run_proof_block.py --check-all` | PASS — 73 blocks |
| Formatting | pinned wheelhouse `black==26.3.1 --check` on changed Python files | PASS after applying the pinned formatter |
| Lint | pinned wheelhouse `ruff==0.15.11 check` on changed Python files | PASS |
| Compilation | `python -m compileall -q scripts/proof_authority.py tests/tier_b/proof_model/test_proof_authority_contract.py` | PASS |
| Current-route stale-token search | bounded `rg` search across `PLANS.md`, live roadmap, routing index and routed process/testing/architecture overlays | PASS — no continuation-ready or active-pack route remained |

Black and Ruff were installed into an external temporary virtual environment from the supplied locked development wheelhouse. The first Black check correctly reported both changed Python files required formatting; they were formatted and the repeated check passed. Pytest inside that minimal tooling environment could not collect because PyYAML was not installed there; the repository-capable system Python executed the focused and complete Tier B suites successfully.

## Historical repair closure

The supplied M03→M05 full-history archive was independently extracted before mutation:

- archive: `NVDA_M03_M05_SEMANTIC_CONTINUITY_ACCEPTED_74D2F2C_20260803_FULL_HISTORY.tar(4).gz`;
- SHA-256: `4502c0be3717613bce8d0c87d199bf1a9973781e1153794d2f6f486a6bda0d67`;
- extracted branch: `work/m03-m05-semantic-continuity-repair-v1`;
- extracted HEAD: `74d2f2c3fa403538fd11e428a928c5de517dc165`;
- pre-transition worktree: clean.

That identity is recorded in the repair's `FINAL_ARCHIVE_RECEIPT.md`; no claim is made that its historical test suites were rerun during extraction.

## Exact-checkpoint acceptance

The commit carrying this closeout is the control-surface transition checkpoint on `main`. Before the acceptance tag is created, signed `alpha_current` promotion must run against that exact clean commit with its receipt outside the repository. Tag creation is evidence selection and does not mutate the committed tree.

## Open state

No successor development phase has been defined. This is deliberate, not a missing plan: the live roadmap lawfully records `Active ExecPlan | none` until the user authorises the next phase.
