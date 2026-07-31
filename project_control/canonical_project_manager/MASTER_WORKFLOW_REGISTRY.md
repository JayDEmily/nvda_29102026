# Master Workflow Registry

## Status

`HISTORICAL:PARALLEL_CYCLE_01_AGGREGATE_VALIDATED_CLOSED`

This registry is PM-owned. Parallel Cycle 01 worker and tester assignments are closed. No lane may continue, select follow-on work or mutate from its former worker/tester branch. Any later assignment requires a new PM brief from the published canonical closeout checkpoint.

The 31 July 2026 MVP amendment makes parallel lanes and independent
worker/tester pairs optional execution tools rather than mandatory Gate C
leaves. Current delivery state is governed by `EXEC_PLAN.md`,
`GATE_C_COMPLETION_PROTOCOL.md` and `ROADMAP_LEDGER_V2.md`. The tables below
remain exact Cycle 01 history.

## Current control lineage

| Field | Value |
|---|---|
| Accepted pre-parallel checkpoint branch | `review/m01-authority-v1` |
| Accepted pre-parallel checkpoint commit | `ae7c8b05bf3742a5c0be530a26617d999313d232` |
| Accepted parallel-control tester commit | `e672b27ca01efbd1f47de27d41fa54733bc73c63` |
| Worker-launch source branch | `review/parallel-control-r2-accepted` |
| Worker-launch source commit | `ee67c752d14073a959fda478f31f4466b6952cae` |
| Worker-launch archive | `NVDA_PARALLEL_WORKFLOW_WORKER_LAUNCH_CHECKPOINT_R1_FULL_HISTORY.tar.gz` |
| Worker-launch archive SHA-256 | `983d0ffdb977a75a4cd3063bd9d645d24ae7817ff47620e543f9e1f8bfb5a381` |
| Canonical integration branch | `integration/parallel-cycle-01` |
| Integrated state before aggregate closeout | `d6cfff9ab00cb5772baad26b14a8d388b08a241a` |
| Integration order | `1A → 2A → 3A → 4A` |
| Aggregate disposition | `PASS:PARALLEL_CYCLE_01_AGGREGATE_VALIDATED_CLOSED` |
| Aggregate record | `project_control/canonical_project_manager/parallel_cycle_01_closeout/CYCLE_01_PM_AGGREGATE_CLOSEOUT.md` |
| Published closeout commit/archive | reported externally after the committed bytes and archive exist; no self-hash claim |
| Lane-local continuation | prohibited |

## Cycle 01 allocation and lineage

| Lane | Assignment | Revision | Worker thread | Tester thread | Semantic unit | Owner / contract | Worker branch | Tester branch | Worker commit | Tester evidence commit | Tester verdict | Approved portability artefact | Artefact SHA-256 | PM disposition | Queue | PM integration commit | Aggregate validation | State / blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|
| 1 | `1A` | `R1` | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | M01 / K01–K03 | `work/lane-1a-m01-mlc-r-v1` | `test/lane-1a-m01-mlc-r-v1` | `f504c89ce852da2ce01f2034c68da77a9c73dcb0` | `d935f6d669e8ee7e21818d3df4ff1d6df54ca8b6` | `PASS` | `NVDA_LANE_1A_M01_MLC_R_TESTER_APPROVED_R1.tar.gz` | `479adac5022921a3f6a3c0ad970c648bacc34798af0c6ad643fd4e2701ef4bb8` | accepted | 1 | `4ff92943bc881d2a1996ea5cd54da4e7ba0bcebe` | `PASS` | `CLOSED:M01_MLC_R_ACCEPTED` |
| 2 | `2A` | `R1` | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | M04 / K07 | `work/lane-2a-m04-mlc-a-v1` | `test/lane-2a-m04-mlc-a-v1` | `b24260fa27248fae61f2537dc59905f62099fcee` | `23289785e154110686a146671ef3d483f8f05f0b` | `PASS` | `NVDA_LANE_2A_M04_MLC_A_TESTER_APPROVED_R1.tar.gz` | `3851f48653891c54d99bdb061e45d713bcd1973cb83d5471c1243a4c54cc1636` | accepted truthful blocker | 2 | `a538880f14f5e47a063412714a980400b4a18c19` | `PASS` | `CLOSED:BLOCKED_MISSING_NORMATIVE_AUTHORITY_K07_ROLE_MATRIX` |
| 3 | `3A` | `R1` | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | M07 / K12; `OBL-M07-POSITIVE` | `work/lane-3a-m07-mlc-a-v1` | `test/lane-3a-m07-mlc-a-v1` | `a83919a208b9a91fc768116b5f1ee12100568654` | `a78ce0642b257b0bf3779e46cd962f95dec3781a` | `PASS` | `NVDA_LANE_3A_M07_MLC_A_TESTER_APPROVED_R1.tar.gz` | `6e0a0c3a0c822be28b688a8250b7245b2efa07c8719a448df29d24680caa4afc` | accepted truthful blocker | 3 | `391781b0f576619063b0c3dbc559a62b71fa9baa` | `PASS` | `CLOSED:BLOCKED_MISSING_NORMATIVE_AUTHORITY_K12_APPLICATION_CONTRACT` |
| 4 | `4A` | `R1` | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | M08 / K13 | `work/lane-4a-m08-mlc-a-v1` | `test/lane-4a-m08-mlc-a-v1` | `120b08ff4a27199364c1543bae8e7253708744d7` | `f13ed3bf551f6c9ca25b522e9a17b23c5ed0528c` | `PASS` | `NVDA_LANE_4A_M08_MLC_A_TESTER_APPROVED_R1.tar.gz` | `5232de8c99684d19281f1f0066c47c7e7437853838d54980add0f6f4fda17b5e` | accepted truthful blocker | 4 | `d6cfff9ab00cb5772baad26b14a8d388b08a241a` | `PASS` | `CLOSED:BLOCKED_MISSING_NORMATIVE_AUTHORITY_K13_DECISION_CONTRACT` |
| 5 | — | — | — | — | held | — | — | — | — | — | — | — | — | — | — | — | — | `HELD_BLOCKED_DEPENDENCY` |
| 6 | — | — | — | — | held | — | — | — | — | — | — | — | — | — | — | — | — | `HELD_BLOCKED_DEPENDENCY` |

The worker-commit column records each tester package's original worker candidate tip. The tester-evidence column records the original tester evidence commit retained under `refs/remotes/lane*/test`. The PM integration commits are the canonical sequential acceptance points on `integration/parallel-cycle-01`.

## Aggregate validation summary

| Check | Result |
|---|---|
| Accepted launch checkpoint ancestry | `PASS` |
| Declared PM integration order | `PASS` — 1A, 2A, 3A, 4A |
| Pairwise lane write-set disjointness | `PASS` |
| Lane scope confinement | `PASS` — 18 M01, 25 M04, 20 M07, 19 M08 paths |
| Behavioural-surface mutation | `PASS` — none |
| Brief-pack hashes | `PASS` — 8/8 |
| Original tester provenance refs | `PASS` — 4/4 |
| M01 routing reconciliation | `PASS` — 179 unique, 20 route, 159 shadow, 20 exact chains |
| M04 exact locators | `PASS` — 63/63, zero failures |
| Atlas contract ownership | `PASS` — K01–K03→M01, K07→M04, K12→M07, K13→M08 |
| Git structural validation | `PASS` — diff check and full fsck |

Mechanical evidence is retained under `project_control/canonical_project_manager/parallel_cycle_01_closeout/`. Mechanical validation does not replace the semantic PM closeout.

## Exact lane artefact contracts — historical Cycle 01 record

| Assignment | Worker Candidate Archive | PASS portability artefact |
|---|---|---|
| `1A` | `NVDA_LANE_1A_M01_MLC_R_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_1A_M01_MLC_R_TESTER_APPROVED_R1.tar.gz` |
| `2A` | `NVDA_LANE_2A_M04_MLC_A_WORKER_CANDIDATE_R2_FULL_HISTORY.tar.gz` | `NVDA_LANE_2A_M04_MLC_A_TESTER_APPROVED_R1.tar.gz` |
| `3A` | `NVDA_LANE_3A_M07_MLC_A_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_3A_M07_MLC_A_TESTER_APPROVED_R1.tar.gz` |
| `4A` | `NVDA_LANE_4A_M08_MLC_A_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_4A_M08_MLC_A_TESTER_APPROVED_R1.tar.gz` |

## Next allocation boundary

- No new parallel cycle is required for the current M04 K07 Gate D slice.
- M04 is implementation-open under the current MVP protocol, not under this
  historical registry.
- M01 minimum proof and the M07/M08 normative closures may use optional parallel
  assignments only when their write sets are disjoint and the PM explicitly
  allocates them.
- Lanes 5 and 6 remain unallocated; there is no obligation to fill them.
