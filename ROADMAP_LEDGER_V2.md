# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `p2_clean_review_authorised_not_started` |
| Active ExecPlan | `00_TASK/NVDA_P2_CLEAN_WORKER_SEMANTIC_REVIEW_EXEC_PLAN_20260722.md` |
| Wider programme plan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Frozen governed ancestor | `533ed574ab326f75058aaeab7c1a671de5dea31f` |
| Working branch | `work/NVIDIA_2026_pm001_pm010_restart_20260721` |
| Git HEAD | `21c1e5eccfbb818bdd422afd42117f23b1f74f26` |
| Preserved accepted prerequisite | `PM-001` through `PM-010` |
| Standing mechanical census | `PM-011` |
| Current unit | `PM-012`, not started |
| P2 semantic state | no PM-012–PM-020 candidate evidence present |
| P3 | closed |
| Gate D | closed |

This pointer activates the clean-worker P2 ExecPlan for the bounded test-authority review. The wider canonical programme plan remains programme history and law where it does not conflict with the active bounded plan.

## Serial state

| Sequence | Gate | State | Exit condition |
|---:|---|---|---|
| 0 | PM-000 control activation | `accepted_control_checkpoint` | preserved |
| 1 | P1 vocabulary semantic authority | `preserved_accepted_prerequisite` | PM-001–PM-010 evidence and accepted P1 projections remain intact |
| 2 | PM-011 P2 census | `standing` | 166 Tier A + 13 Tier B files; all 179 clean-baseline hashes reproduced |
| 3 | PM-012–PM-018 semantic review | `authorised_not_started` | every physical file receives a manual semantic receipt and ledger row `YES` |
| 4 | PM-019 integration | `blocked_by_PM-012_to_PM-018` | integrated registers exactly project completed semantic receipts |
| 5 | PM-020 validation/package | `blocked_by_PM-019` | structural and behavioural validation complete; audit candidate returned |
| 6 | P3 | `closed` | opens only after independent Project Manager acceptance of P2 |
| 7 | P4 and Gate D | `closed` | governed by the wider programme after prerequisite acceptance |

## Fixed P2 order

`PM-012, PM-013, PM-014, PM-015, PM-016, PM-017, PM-018, PM-019, PM-020`

No later unit opens before the prior unit's ledger rows and unit receipt are complete.

## Current known truth

- Physical tests: 166 Tier A and 13 Tier B, 179 total.
- PM-011 allocates every physical file exactly once across PM-012–PM-018.
- Every clean-baseline test hash matches `PM-011/P2_PHYSICAL_TEST_CENSUS.tsv`.
- The retained Tier A inventory contains 120 rows; 46 physical Tier A files require explicit disposition.
- The clean snapshot contains no prior P2 relationship register, semantic rationale, self-review, final count set or P2-mutated test/configuration surface.
- The absolute semantic-read ledger contains 179 rows, all `SEMANTICALLY_READ=NO`.

## Open roadblocks

| ID | Blocker | Affects | Required treatment |
|---|---|---|---|
| RB-002 | 46 physical Tier A files are absent from the retained reconciliation inventory | P2 | file-by-file semantic disposition; no admission by location |
| RB-003 | Asserted 287 Atlas cohort rows are absent from the governed checkpoint/history paths previously inspected | later Atlas-dependent work | remains outside P2; do not invent or reconstruct in this review |
| RB-004 | Eleven proof units were historically closed | P3/P4 | remain closed until P2 acceptance and exact P3 return gates |
| RB-005 | Locked dependency route previously failed at the package gateway | PM-020 validation | retry; report `Unknown` if external failure persists; continue other lawful checks |

## Mutation boundary

During PM-012–PM-018, tests, source, normative documents, accepted P1 files, root controls and configuration are read-only. Semantic evidence may be written only under the active plan's named project-control paths.

After all 179 semantic rows close, PM-019 may update only `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` as exact projections of the accepted candidate decisions. The worker may not alter tests to manufacture stronger proof.

## Acceptance authority

The worker may return `P2 candidate returned for independent Project Manager audit`. Only the Project Manager may accept P2 or open P3.
