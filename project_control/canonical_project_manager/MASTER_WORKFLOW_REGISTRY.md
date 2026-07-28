# Master Workflow Registry

## Status

`PARALLEL_CYCLE_01_ALLOCATED_AWAITING_WORKER_LAUNCH`

This registry is PM-owned. Workers and testers must not edit it. The PM launch message supplies the exact source archive filename, SHA-256, branch and commit for all four assignments.

## Current canonical control source

| Field | Value |
|---|---|
| Control source branch | `review/m01-authority-v1` |
| Control source commit | `ae7c8b05bf3742a5c0be530a26617d999313d232` |
| Parallel control branch | `control/parallel-workflow-enablement-v1` |
| Cycle source archive | `SUPPLIED_IN_PM_LAUNCH_BLOCK_AFTER_CHECKPOINT_PUBLICATION` |
| Cycle source SHA-256 | `SUPPLIED_IN_PM_LAUNCH_BLOCK_AFTER_CHECKPOINT_PUBLICATION` |
| Cycle source branch/commit | `SUPPLIED_IN_PM_LAUNCH_BLOCK_AFTER_CHECKPOINT_PUBLICATION` |
| Integration order | `1A → 2A → 3A → 4A` |
| Lane-local continuation | prohibited for Cycle 1 |

## Active allocation

| Lane | Assignment | Worker thread | Tester thread | Semantic unit | Owner/contract | Runtime prerequisites | Worker branch | Tester branch | Writable paths | Shared locks | Status | Tester verdict | Approved archive | PM disposition | Integration state |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1A | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | M01 / K01–K03 | M13 accepted; M01 MLC-A accepted | `work/lane-1a-m01-mlc-r-v1` | `test/lane-1a-m01-mlc-r-v1` | M01 routing record and `raw_validation/mlc_r_v1/**`; tester review paths | all global controls; source/tests/config; M04/M07/M08 evidence | `ALLOCATED_AWAITING_LAUNCH` | — | — | pending | not queued |
| 2 | 2A | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | M04 / K07 | none | `work/lane-2a-m04-mlc-a-v1` | `test/lane-2a-m04-mlc-a-v1` | M04 authority record and `raw_validation/mlc_a_v1/**`; tester review paths | all global controls; source/tests/config; M01/M07/M08 evidence | `ALLOCATED_AWAITING_LAUNCH` | — | — | pending | not queued |
| 3 | 3A | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | M07 / K12 | none | `work/lane-3a-m07-mlc-a-v1` | `test/lane-3a-m07-mlc-a-v1` | M07 authority record and `raw_validation/mlc_a_v1/**`; tester review paths | all global controls; source/tests/config; M01/M04/M08 evidence | `ALLOCATED_AWAITING_LAUNCH` | — | — | pending | not queued |
| 4 | 4A | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | M08 / K13 | none | `work/lane-4a-m08-mlc-a-v1` | `test/lane-4a-m08-mlc-a-v1` | M08 authority record and `raw_validation/mlc_a_v1/**`; tester review paths | all global controls; source/tests/config; M01/M04/M07 evidence | `ALLOCATED_AWAITING_LAUNCH` | — | — | pending | not queued |
| 5 | — | — | — | held | — | no lawful additional root | — | — | none | all | `HELD_BLOCKED_DEPENDENCY` | — | — | — | — |
| 6 | — | — | — | held | — | no lawful additional root | — | — | none | all | `HELD_BLOCKED_DEPENDENCY` | — | — | — | — |

## Material read-set locks

| Assignment | Material read set whose canonical change requires revalidation |
|---|---|
| 1A | M01 PM/worker authority records; PM-011 and governed test-routing registries; Gate C test requirements/authority/disposition registers; accepted architecture module/contract/work-unit projection |
| 2A | DMPV3 core/working authority; architecture M04/K07 allocation; C-010/C-016 and D-010/D-016 historical trace records; relevant N-03/N-05/N-09 decisions |
| 3A | coefficient/modifier authority across numbered operating/domain/architecture/ownership documents; M07/K12 allocation; C-012/D-012; mandatory positive M07 obligation |
| 4A | playbook/eligibility authority across numbered operating/domain/architecture/ownership documents; M08/K13 allocation; C-033/C-034 and D-033/D-034 |

## History

No Cycle 1 assignment has yet been launched, returned, tested, accepted or integrated.
