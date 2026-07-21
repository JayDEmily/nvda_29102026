# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `p1_restart_handoff_prepared` |
| Active ExecPlan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Frozen governed ancestor | `533ed574ab326f75058aaeab7c1a671de5dea31f` |
| Working branch | `work/NVIDIA_2026_pm001_pm010_restart_20260721` |
| Current unit | `PM-001` restart is first; no worker output accepted |
| Authorised sequence | `PM-001` through `PM-010`, strictly serial under the worker table |
| Next worker state | `ten_unit_handoff_prepared_not_dispatched` |
| Behavioural mutation | `closed` |
| Gate D | `closed` |

This is the mutable successor to the retired `ROADMAP_LEDGER.md`. Historical plans and ledgers remain evidence; they do not displace this pointer.

## Serial programme state

| Sequence | Gate | State | Exit condition |
|---:|---|---|---|
| 0 | PM-000 control activation | `accepted_control_checkpoint` | Plan, full-read manifest, live pointer, validation record, bounded worker brief, and control checks accepted; commit/archive identify the handoff checkpoint |
| 1 | P1 vocabulary semantic authority | `restart_sequence_prepared` | Human registry, builder/projection, generated JSON, aliases, audit evidence, and semantic proof agree |
| 2 | P2 test authority | `not_open` | 166 Tier A and 13 Tier B files each have an explicit current authority/disposition; 46-file Tier A gap resolved |
| 3 | P3 closed-unit proof repair | `not_open` | D-009, D-012, D-015, D-010, D-016, D-033, D-017, D-031, D-021, D-048, D-041 accepted in that order |
| 4 | P4 proof-envelope freeze | `not_open` | All 33 envelopes reissued as executable-now or closed with exact return gate; total order dependency-safe |
| 5 | D serial implementation | `closed` | All 33 canonical units accepted in the fixed order |
| 6 | Whole-system closeout | `closed` | Traceability, proof, replay, modularity, archive, and clean final checkpoint accepted |

## Fixed implementation order

`D-001, D-002, D-003, D-049, D-050, D-006, D-007, D-051, D-052, D-012, D-015, D-053, D-009, D-054, D-010, D-025, D-055, D-027, D-033, D-034, D-016, D-031, D-017, D-020, D-035, D-056, D-021, D-048, D-041, D-042, D-044, D-047, D-057`

This order is not yet executable. P1-P4 must pass first.

## Current known truth

- Current registry: 46 human vocabulary headings.
- Generated canonical vocabulary: 87 entries.
- Punctuation-insensitive case-folded comparison: 26 matches, 20 human-only labels, 61 generated-only labels.
- Tests: 166 physical Tier A files; retained inventory names 120; 46 require explicit disposition. Tier B is 13 physical and 13 inventoried.
- Proof: 33 work units; prior evidence classifies 22 proof-ready and 11 closed, but none is reissued under the new two-status P4 rule.
- Atlas: recoverable historical source objects validate 1,716 records across 18 surfaces; current tree retains only the ten-record vocabulary slice; the asserted 287-row cohort register is absent.
- Runtime: current alpha implementation retains the expected Gate C gaps; no repair has been authorised under this programme.

## Open roadblocks

| ID | Blocker | Affects | Next gate |
|---|---|---|---|
| RB-001 | Stale 42-heading vocabulary count in normative/control evidence | P1 | PM-001 census, then semantic repair |
| RB-002 | 46 physical Tier A files absent from retained reconciliation inventory | P2 and proof freeze | File-by-file P2 reconciliation |
| RB-003 | Asserted 287 Atlas cohort rows not present in supplied checkpoint/history paths inspected | Atlas-dependent units | Supply or lawfully reconstruct and accept register |
| RB-004 | Eleven closed proof units | P4/Gate D | P3 exact return-gate sequence |
| RB-005 | Locked pytest environment cannot currently resolve dependencies; package mirror returned HTTP 502 | Runtime proof claims | Retry locked environment before behavioural validation |

## Worker queue

| Brief | Scope | Mutation class | State |
|---|---|---|---|
| `project_control/canonical_project_manager/PM-001_TO_PM-010_WORKER_TABLE.md` | Exact serial allocation and cross-unit law | Control/evidence | `prepared_not_dispatched` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-001_VOCABULARY_CURRENT_TRUTH_CENSUS.md` | Fresh census; no semantic decision | Project-control evidence | `prepared_not_dispatched` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-002_VOCABULARY_NORMATIVE_TRUTH_REPAIR.md` | Stale truth and authority-direction repair only | Bounded vocabulary normative/workflow | `blocked_by_PM-001` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-003_ARCHITECTURE_MIGRATION_CONTROL_TERMS.md` | Architecture/migration/control family | Human semantic authority | `blocked_by_PM-002` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-004_COEFFICIENT_MODIFIER_EVALUATION_TERMS.md` | Coefficient/modifier/evaluation family | Human semantic authority | `blocked_by_PM-003` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-005_CALENDAR_TEMPORAL_PROVENANCE_TERMS.md` | Calendar/temporal/provenance family | Human semantic authority | `blocked_by_PM-004` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-006_DMP_PROTOCOL_IDENTITY_LINEAGE_TERMS.md` | DMP/protocol/identity/lineage family | Human semantic authority | `blocked_by_PM-005` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-007_STAGE_INGRESS_SERIAL_CAPITAL_TERMS.md` | Stage/ingress/serial/capital family | Human semantic authority | `blocked_by_PM-006` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-008_OPENING_POSITION_EXIT_CLOSE_TERMS.md` | Opening through close family | Human semantic authority | `blocked_by_PM-007` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-009_PARALLEL_RISK_REVIEW_PLAYBOOK_TERMS.md` | Parallel-risk/review/playbook family | Human semantic authority | `blocked_by_PM-008` |
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-010_P1_INTEGRATION_AND_PROJECTION_FREEZE.md` | Accepted semantic integration and projection | Vocabulary projection only | `blocked_by_PM-009` |

No unit beyond PM-010 is authorised. The same worker may advance to the next listed unit only when the preceding receipt records `unit_result: pass` and all preceding changes satisfy the preceding brief. Project-manager acceptance remains required before P2 opens.

## Ledger update rule

Update this file only after the Project Manager has inspected the unit return, rerun proportionate validation, recorded the acceptance/rejection evidence, and created the expected checkpoint. Never advance a gate from a worker's self-report alone.
