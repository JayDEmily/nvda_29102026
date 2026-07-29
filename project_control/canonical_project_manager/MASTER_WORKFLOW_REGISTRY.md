# Master Workflow Registry

## Status

`PARALLEL_CONTROL_R2_ACCEPTED_WORKER_LAUNCH_OPEN`

This registry is PM-owned. Lane workers and lane testers must not edit or read it as a required assignment input. The independent control tester may read it but may add evidence only in its separately authorised control-test paths.

Cycle 1 worker launch is authorised only from the PM-published immutable full-history checkpoint created from this accepted review branch. The PM launch message supplies its exact archive filename, SHA-256, branch and commit.

## Current control lineage

| Field | Value |
|---|---|
| Accepted pre-parallel checkpoint branch | `review/m01-authority-v1` |
| Accepted pre-parallel checkpoint commit | `ae7c8b05bf3742a5c0be530a26617d999313d232` |
| Superseded control branch | `control/parallel-workflow-enablement-v1` |
| Superseded control commit | `9e404df7c13f7cca170e05e4c9f76b8ec4548ffa` |
| Repair branch | `control/parallel-workflow-enablement-v1-repair-2` |
| Repair source commit | `44bede21b1d90ec8cdfac386baed7d2ee247eddb` |
| Repair revision | `CONTROL-R2` |
| Current control tester | `Parallel Control T1` |
| Control tester branch | `test/parallel-workflow-enablement-v1-repair-2` |
| Current-target read manifest | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_2_FULL_READ_MANIFEST.tsv` |
| Repair archive filename | `NVDA_PARALLEL_WORKFLOW_CYCLE_01_CONTROL_REPAIR_2_20260729_FULL_HISTORY.tar.gz` |
| Repair archive SHA-256 | supplied in PM control-test launch message after archive verification |
| Repair commit | `f95756e8dfeced446986c856bd28c4dcd6be0c07` |
| Worker-launch source | PM acceptance branch `review/parallel-control-r2-accepted`; exact commit and archive SHA-256 supplied in launch message |
| Integration order | `1A → 2A → 3A → 4A` |
| Lane-local continuation | prohibited for Cycle 1 |

## Cycle 1 allocation and lineage

| Lane | Assignment | Revision | Worker thread | Tester thread | Semantic unit | Owner / contract | Runtime prerequisites | Worker branch | Tester branch | Worker commit | Tester evidence commit | Tester verdict | Approved portability artefact | Artefact SHA-256 | PM disposition | Queue position | Integration commit | Aggregate validation | State / blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `1A` | `R1` | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | M01 / K01–K03 | M13 accepted; M01 MLC-A accepted | `work/lane-1a-m01-mlc-r-v1` | `test/lane-1a-m01-mlc-r-v1` | — | — | — | — | — | pending | not queued | — | not run | `WORKER_LAUNCH_AUTHORISED` |
| 2 | `2A` | `R1` | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | M04 / K07 | none | `work/lane-2a-m04-mlc-a-v1` | `test/lane-2a-m04-mlc-a-v1` | — | — | — | — | — | pending | not queued | — | not run | `WORKER_LAUNCH_AUTHORISED` |
| 3 | `3A` | `R1` | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | M07 / K12 and `OBL-M07-POSITIVE` | none | `work/lane-3a-m07-mlc-a-v1` | `test/lane-3a-m07-mlc-a-v1` | — | — | — | — | — | pending | not queued | — | not run | `WORKER_LAUNCH_AUTHORISED` |
| 4 | `4A` | `R1` | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | M08 / K13 | none | `work/lane-4a-m08-mlc-a-v1` | `test/lane-4a-m08-mlc-a-v1` | — | — | — | — | — | pending | not queued | — | not run | `WORKER_LAUNCH_AUTHORISED` |
| 5 | — | — | — | — | held | — | no lawful additional root | — | — | — | — | — | — | — | — | — | — | — | `HELD_BLOCKED_DEPENDENCY` |
| 6 | — | — | — | — | held | — | no lawful additional root | — | — | — | — | — | — | — | — | — | — | — | `HELD_BLOCKED_DEPENDENCY` |

## Exact lane artefact contracts

| Assignment | Worker Candidate Archive | PASS portability artefact | FAIL portability artefact | HARD_BLOCK portability artefact |
|---|---|---|---|---|
| `1A` | `NVDA_LANE_1A_M01_MLC_R_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_1A_M01_MLC_R_TESTER_APPROVED_R1.tar.gz` | `NVDA_LANE_1A_M01_MLC_R_TESTER_FAIL_REPAIRABLE_R1.tar.gz` | `NVDA_LANE_1A_M01_MLC_R_TESTER_HARD_BLOCK_R1.tar.gz` |
| `2A` | `NVDA_LANE_2A_M04_MLC_A_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_2A_M04_MLC_A_TESTER_APPROVED_R1.tar.gz` | `NVDA_LANE_2A_M04_MLC_A_TESTER_FAIL_REPAIRABLE_R1.tar.gz` | `NVDA_LANE_2A_M04_MLC_A_TESTER_HARD_BLOCK_R1.tar.gz` |
| `3A` | `NVDA_LANE_3A_M07_MLC_A_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_3A_M07_MLC_A_TESTER_APPROVED_R1.tar.gz` | `NVDA_LANE_3A_M07_MLC_A_TESTER_FAIL_REPAIRABLE_R1.tar.gz` | `NVDA_LANE_3A_M07_MLC_A_TESTER_HARD_BLOCK_R1.tar.gz` |
| `4A` | `NVDA_LANE_4A_M08_MLC_A_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz` | `NVDA_LANE_4A_M08_MLC_A_TESTER_APPROVED_R1.tar.gz` | `NVDA_LANE_4A_M08_MLC_A_TESTER_FAIL_REPAIRABLE_R1.tar.gz` | `NVDA_LANE_4A_M08_MLC_A_TESTER_HARD_BLOCK_R1.tar.gz` |

## Write sets and assignment-local read manifests

| Assignment | Worker writable paths | Worker full-read manifest | Tester writable paths | Tester full-read manifest |
|---|---|---|---|---|
| `1A` | M01 routing record and `modules/M01/raw_validation/mlc_r_v1/**` | `project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/FULL_READ_MANIFEST.tsv` | M01 tester review and `modules/M01/raw_validation/tester_mlc_r_v1/**` | `project_control/canonical_project_manager/modules/M01/raw_validation/tester_mlc_r_v1/FULL_READ_MANIFEST.tsv` |
| `2A` | M04 authority record and `modules/M04/raw_validation/mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv` | M04 tester review and `modules/M04/raw_validation/tester_mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv` |
| `3A` | M07 authority record and `modules/M07/raw_validation/mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv` | M07 tester review and `modules/M07/raw_validation/tester_mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv` |
| `4A` | M08 authority record and `modules/M08/raw_validation/mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M08/raw_validation/mlc_a_v1/FULL_READ_MANIFEST.tsv` | M08 tester review and `modules/M08/raw_validation/tester_mlc_a_v1/**` | `project_control/canonical_project_manager/modules/M08/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv` |

All paths outside each exact brief write set are locked. Workers and testers do not update this registry.

## Material Read Set locks

| Assignment | Material Read Set whose canonical change requires revalidation |
|---|---|
| `1A` | M01 PM/worker authority records; PM-011 and governed test-routing registries; Gate C test requirements/authority/disposition registers; accepted architecture module/contract/work-unit projection |
| `2A` | DMPV3 core/working authority; architecture M04/K07 allocation; C-010/C-016 and D-010/D-016 historical trace records; relevant N-03/N-05/N-09 decisions |
| `3A` | coefficient/modifier authority across numbered operating/domain/architecture/ownership documents; M07/K12 allocation; C-012/D-012; mandatory positive M07 obligation |
| `4A` | playbook/eligibility authority across numbered operating/domain/architecture/ownership documents; M08/K13 allocation; C-033/C-034 and D-033/D-034 |

## History

- The original control checkpoint at `9e404df7…` was rejected by PM self-audit before any lane launch.
- No Cycle 1 assignment has been launched, returned, tested, accepted or integrated.
- Repair 1 was hard-blocked correctly. Repair 2 passed `Parallel Control T1` at tester commit `e672b27ca01efbd1f47de27d41fa54733bc73c63` and was accepted by the Project Manager. No worker result has yet returned.
