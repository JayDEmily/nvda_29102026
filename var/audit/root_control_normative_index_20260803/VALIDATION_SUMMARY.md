# Root-control and normative-index transition validation

## Scope

- Imported the revised root control documents supplied in `NVDA_ROOT_CONTROL_DOCUMENTS_478245B_20260803.tar(1).gz`.
- Consolidated the retired/successor roadmap pair into one live `ROADMAP_LEDGER.md` and removed `ROADMAP_LEDGER_V2.md`.
- Added the inactive root `EXEC_PLAN.md` placeholder.
- Added `NVDA_FEATURE_EVOLUTION_TEMPLATE.md` from the supplied canonical methodology source because the revised `PLANS.md` names it as optional advisory material; trailing whitespace was normalised without changing semantic content.
- Amended `AGENTS.md` so the active ExecPlan owns the exact complete normative read set.
- Replaced `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md` with a compact LLM document-family directory.
- Reconciled directly affected process, testing, proof-authority and promotion-control surfaces.

## Result

PASS for the changed content before commit.

The index is 35 lines / 495 words and lists all 26 numbered normative documents exactly once. It routes at document-family granularity and requires full reading of every selected prose document. It does not route individual clauses or sections.

## Validation

| Check | Result |
|---|---|
| Locked offline environment | PASS — CPython 3.13.5; 38 compatible distributions; project installed non-editably |
| Tier A split | PASS — 2,007 tests |
| Tier B + Tier C split | PASS — 102 tests |
| Combined split total | PASS — 2,109 tests |
| Vocabulary proof block | PASS — 105 tests |
| M00 application-shell block | PASS — 26 tests |
| Proof-control focused block | PASS — 39 tests |
| Proof-authority model | PASS — 201 families, 73 proof blocks, 203 test paths |
| `alpha_current` resolution | PASS — 19 proof blocks, 19 families, 21 paths |
| Installed package import outside repository | PASS — import resolved from `.venv/.../site-packages` |
| Ruff | PASS |
| Black | PASS |
| Python compilation | PASS |
| Git diff whitespace check | PASS |
| Git object integrity | PASS |

An initial Tier B/C run under the pre-existing `/opt/pyvenv` interpreter produced two Tier C failures because `nvda_desk` was not installed in that interpreter's `purelib`. The accepted locked offline environment was then recreated from the supplied V6 runtime and V4 development wheelhouses; both tests passed there. No test or production-code change was made to suppress that environment failure.

## Historical-reference boundary

Historical receipts, manifests, handovers and archived project-control records that mention `ROADMAP_LEDGER_V2.md` were retained unchanged as historical evidence. No active root, normative, test-control, proof-control or promotion-control surface retains that path.

## Post-commit gate

Recreate or refresh the non-editable installation at the resulting clean commit and rerun the two deterministic suite sets before publishing the checkpoint.
