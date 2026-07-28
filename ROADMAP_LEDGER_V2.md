# ROADMAP_LEDGER_V2 — Live Programme Pointer

## Current authority

| Field | Value |
|---|---|
| Status | `parallel_cycle_01_allocated_awaiting_worker_launch` |
| Programme ExecPlan | `project_control/canonical_project_manager/EXEC_PLAN.md` |
| Module-local Gate C protocol | `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md` |
| Parallel operating law | `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md` |
| PM workflow registry | `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md` |
| PM control decision | `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_PM_REVIEW_V1.md` |
| Cycle 1 brief pack | `project_control/canonical_project_manager/PARALLEL_CYCLE_01/` |
| Accepted architecture | `project_control/canonical_project_manager/architecture/` |
| Current branch | `control/parallel-workflow-enablement-v1` |
| Source checkpoint | `review/m01-authority-v1` at `ae7c8b05bf3742a5c0be530a26617d999313d232` |
| Accepted M13 worker commit | `616fade4123def7870b7950bb3e644ffcc0ccc5a` |
| Accepted M01 authority worker commit | `eef4a2ff16d4aaf782ebe047c342999810fa102f` |
| Active lane pairs | `1AW/1AT`, `2AW/2AT`, `3AW/3AT`, `4AW/4AT` |
| Held lanes | 5 and 6; no additional dependency-safe root |
| Production/source mutation | closed for Cycle 1 |
| Physical test mutation | closed for Cycle 1 |
| Global control mutation by lanes | prohibited |
| Gate D | module-local only; no global opening |

Read the ExecPlan, Gate C protocol and parallel operating law before using the registry or issuing a brief.

## Accepted strategy

- One repository and one canonical PM control front remain authoritative.
- Six permanent lanes are capacity slots, not permanent module ownership.
- Each assignment uses one worker thread `Lane <n><letter>W`, one tester thread `Lane <n><letter>T` and fresh short-lived branches.
- Each active lane owns one semantic leaf or bounded implementation slice only.
- Parallel assignments require dependency readiness, disjoint semantic ownership, exact read/write sets and declared locks.
- Workers and testers do not coordinate with other lanes or update global PM controls.
- Tester PASS means suitable for PM integration review only.
- PM acceptance and integration are sequential; a new canonical checkpoint follows aggregate validation.
- No lane-local continuation from unintegrated work is permitted during the pilot.

## Preserved accepted truth

- `M13 state_kernel` implementation repair V1 remains independently accepted.
- `M01-PROOF-MLC-A-V1` remains independently accepted for the bounded general source-admission contract.
- P1 `PM-001`–`PM-010`, PM-011, historical P2/Gate C evidence, all 33 `D-xxx` records and the accepted Atlas architecture remain preserved evidence under their existing limits.
- `M07` remains `coefficient_modifier_authority`.
- Production, paper, live, durability and end-to-end readiness remain unclaimed.

## Parallel control gate

| Leaf | State | Exit condition |
|---|---|---|
| `PAR-CTRL-001-A` | `accepted_in_control_branch` | standing controls permit PM-managed parallel lanes and serial integration |
| `PAR-CTRL-001-B` | `accepted_in_control_branch` | parallel architecture and registry are routed |
| `PAR-CTRL-001-C` | `accepted_in_control_branch` | four worker and four tester briefs are standalone and non-overlapping |
| `PAR-CTRL-001-D` | `accepted_in_control_branch` | Lanes 5 and 6 are explicitly held |
| `PAR-CTRL-001-E` | `ready_for_external_checkpoint_verification` | final commit, archive hash, fresh extraction and clean Git validation supplied in the PM launch block |

## Cycle 1 allocation

| Lane | Worker thread | Tester thread | Unit | Worker branch | Tester branch | State |
|---|---|---|---|---|---|---|
| 1A | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | `work/lane-1a-m01-mlc-r-v1` | `test/lane-1a-m01-mlc-r-v1` | `ALLOCATED_AWAITING_LAUNCH` |
| 2A | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | `work/lane-2a-m04-mlc-a-v1` | `test/lane-2a-m04-mlc-a-v1` | `ALLOCATED_AWAITING_LAUNCH` |
| 3A | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | `work/lane-3a-m07-mlc-a-v1` | `test/lane-3a-m07-mlc-a-v1` | `ALLOCATED_AWAITING_LAUNCH` |
| 4A | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | `work/lane-4a-m08-mlc-a-v1` | `test/lane-4a-m08-mlc-a-v1` | `ALLOCATED_AWAITING_LAUNCH` |
| 5 | — | — | held | — | — | `HELD_BLOCKED_DEPENDENCY` |
| 6 | — | — | held | — | — | `HELD_BLOCKED_DEPENDENCY` |

## Dependency waves

1. Current roots: M01, M04, M07 and M08.
2. M02 after the required M01 contracts are canonical.
3. M03 after M01 and M02.
4. M05 and M06 after their prerequisites; they may be independent parallel assignments.
5. M09 → M10 → M11 remains serial.
6. M12 waits for stable evidence-export contracts.
7. M00 is final composition.
8. M14 and M15 remain PM-controlled governance planes.

## Mutation boundary

Cycle 1 lane workers and testers may mutate only the module-local record and raw-evidence paths named in their briefs. They may not mutate `AGENTS.md`, `PLANS.md`, numbered docs, the ExecPlan, Gate C protocol, roadmap, workflow registry, architecture artefacts, source, tests, configuration, proof/vocabulary registries, packaging files or another lane's module directory.

## Integration order

1. 1A / M01
2. 2A / M04
3. 3A / M07
4. 4A / M08
5. aggregate control, traceability and Git validation
6. one new canonical checkpoint

## Next gate

Publish the Phase 0 full-history checkpoint and issue the exact worker briefs to `Lane 1AW`, `Lane 2AW`, `Lane 3AW` and `Lane 4AW`. Create the matching tester threads only when each worker candidate is returned. No fifth or sixth assignment and no `B` assignment is open.
