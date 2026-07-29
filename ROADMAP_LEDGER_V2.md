# ROADMAP_LEDGER_V2 — Live Canonical Programme Pointer

## Current state

| Field | Value |
|---|---|
| Status | `parallel_control_repair_1_awaiting_independent_control_test` |
| Current programme | existing canonical M00–M15 module-local delivery programme |
| Parallel operating law | `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md` |
| Workflow registry | `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md` |
| Superseded PM decision | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_PM_REVIEW_V1.md` |
| Self-audit rejection | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_SELF_AUDIT_REJECTION_V1.md` |
| Repair record | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_PM_RECORD_V1.md` |
| Independent control tester | `Parallel Control T1` |
| Control tester brief | `project_control/canonical_project_manager/PARALLEL_CYCLE_01_CONTROL_REPAIR/PARALLEL_CONTROL_T1_INDEPENDENT_TESTER_BRIEF.md` |
| Repair archive | `NVDA_PARALLEL_WORKFLOW_CYCLE_01_CONTROL_REPAIR_1_20260729_FULL_HISTORY.tar.gz` |
| Cycle 1 brief pack | `project_control/canonical_project_manager/PARALLEL_CYCLE_01/` |
| Current-target read manifest | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_FULL_READ_MANIFEST.tsv` |
| Current branch | `control/parallel-workflow-enablement-v1-repair-1` |
| Accepted M01 authority checkpoint | `review/m01-authority-v1` / `ae7c8b05bf3742a5c0be530a26617d999313d232` |
| Superseded control checkpoint | `control/parallel-workflow-enablement-v1` / `9e404df7c13f7cca170e05e4c9f76b8ec4548ffa` |
| Worker launch | blocked pending independent control PASS and later PM acceptance |
| Production/source mutation | closed for Cycle 1 |
| Physical test mutation | closed for Cycle 1 |

Read the ExecPlan, Gate C protocol and parallel operating law before using the registry or issuing any brief.

## Control repair gate

| Leaf | State | Acceptance boundary |
|---|---|---|
| `PAR-CTRL-R1-A` | repaired | durable workflow terms admitted through M15 and deterministic projection regenerated |
| `PAR-CTRL-R1-B` | repaired | task-local and lane-local full-read-manifest law resolves global write-set conflict |
| `PAR-CTRL-R1-C` | repaired | Lane 1 test-subtree override route is explicit |
| `PAR-CTRL-R1-D` | repaired | exact worker/tester artefact names, revisions and portability members are defined |
| `PAR-CTRL-R1-E` | repaired | registry contains source, revision, commit, verdict, artefact, queue, integration and aggregate lineage fields |
| `PAR-CTRL-R1-F` | open | independent `Parallel Control T1` review and PM acceptance |

No repaired leaf above proves its own acceptance. The current gate closes only after independent tester evidence is returned and the PM adjudicates it.

## Reserved Cycle 1 allocation

| Assignment | Worker | Tester | Unit | Revision | State |
|---|---|---|---|---|---|
| `1A` | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | `R1` | `ALLOCATED_CONTROL_TEST_PENDING` |
| `2A` | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | `R1` | `ALLOCATED_CONTROL_TEST_PENDING` |
| `3A` | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | `R1` | `ALLOCATED_CONTROL_TEST_PENDING` |
| `4A` | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | `R1` | `ALLOCATED_CONTROL_TEST_PENDING` |
| 5 | — | — | held | — | `HELD_BLOCKED_DEPENDENCY` |
| 6 | — | — | held | — | `HELD_BLOCKED_DEPENDENCY` |

## Dependency waves

1. Current roots after control acceptance: M01, M04, M07 and M08.
2. M02 after required M01 contracts are canonical.
3. M03 after M01 and M02.
4. M05 and M06 after their prerequisites; they may be independent assignments.
5. M09 → M10 → M11 remains serial.
6. M12 waits for stable evidence-export contracts.
7. M00 is final composition.
8. M14 and M15 remain PM-controlled governance planes.

## Immediate next gate

Publish the repair archive and create `Parallel Control T1` only. Do not create `Lane 1AW`–`Lane 4AW` until the control tester result is returned and the PM explicitly accepts the tested checkpoint.
