# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `active_control_only` |
| Active ExecPlan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Baseline commit | `f7bd3f46862fe9b33340f3f13951518795724fe7` |
| Working branch | `work/NVIDIA_2026_canonical_project_manager_20260720` |
| Current unit | None open; `PM-000` accepted |
| Next unit | `PM-001` — vocabulary current-truth census, queued but not dispatched |
| Next worker state | `brief_prepared_not_dispatched` |
| Behavioural mutation | `closed` |
| Gate D | `closed` |

This is the mutable successor to the retired `ROADMAP_LEDGER.md`. Historical plans and ledgers remain evidence; they do not displace this pointer.

## Serial programme state

| Sequence | Gate | State | Exit condition |
|---:|---|---|---|
| 0 | PM-000 control activation | `accepted_control_checkpoint` | Plan, full-read manifest, live pointer, validation record, bounded worker brief, and control checks accepted; commit/archive identify the handoff checkpoint |
| 1 | P1 vocabulary semantic authority | `not_open` | Human registry, builder/projection, generated JSON, aliases, audit evidence, and semantic proof agree |
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
| `project_control/canonical_project_manager/WORKER_BRIEFS/PM-001_VOCABULARY_CURRENT_TRUTH_CENSUS.md` | Reproducible vocabulary census and discrepancy register only | Project-control evidence | `prepared_not_dispatched` |

No other worker brief is authorised. Later work is selected only after the current unit is accepted.

## Ledger update rule

Update this file only after the Project Manager has inspected the unit return, rerun proportionate validation, recorded the acceptance/rejection evidence, and created the expected checkpoint. Never advance a gate from a worker's self-report alone.
