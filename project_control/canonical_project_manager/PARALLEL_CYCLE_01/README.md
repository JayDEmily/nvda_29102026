# Parallel Cycle 01 — Controlled Launch Index

## Current launch status

`WORKER_LAUNCH_BLOCKED_PENDING_PARALLEL_CONTROL_T1_AND_PM_ACCEPTANCE`

The four assignments and names are reserved, but no lane thread may be launched from the control-repair branch. The independent control tester must first return PASS and the Project Manager must accept the tested checkpoint. The repair archive issued to that tester is named `NVDA_PARALLEL_WORKFLOW_CYCLE_01_CONTROL_REPAIR_1_20260729_FULL_HISTORY.tar.gz`.

## Exact thread names and revision

| Lane | Worker thread | Tester thread | Unit | Revision |
|---|---|---|---|---|
| 1A | `Lane 1AW` | `Lane 1AT` | M01 relevant-test routing | `R1` |
| 2A | `Lane 2AW` | `Lane 2AT` | M04 authority sufficiency | `R1` |
| 3A | `Lane 3AW` | `Lane 3AT` | M07 authority sufficiency | `R1` |
| 4A | `Lane 4AW` | `Lane 4AT` | M08 authority sufficiency | `R1` |

Lanes 5 and 6 are held. The exact eight-brief inventory and SHA-256 values are recorded in `project_control/canonical_project_manager/PARALLEL_CYCLE_01/BRIEF_PACK_MANIFEST.tsv`.

## Pre-launch control test

Create one independent thread named `Parallel Control T1` only. Use:

`project_control/canonical_project_manager/PARALLEL_CYCLE_01_CONTROL_REPAIR/PARALLEL_CONTROL_T1_INDEPENDENT_TESTER_BRIEF.md`

Do not create `Lane 1AW`–`Lane 4AW` until that control result has been returned to and accepted by the Project Manager.

## Lane launch sequence after PM acceptance

1. Use the same PM-published, independently tested full-history checkpoint for every worker.
2. Create the four worker threads using the exact names above and attach the checkpoint plus the matching `W` brief.
3. Do not create a lane tester task until its matching Worker Candidate Archive is returned.
4. Give the tester the same PM source checkpoint, the Worker Candidate Archive and the matching `T` brief.
5. Return the exact-named tester portability artefact to the Master Project Manager. Do not integrate it manually.

The PM launch message must state the exact source archive filename, SHA-256, branch and commit. Those values are supplied at issue time because the final archive cannot embed its own SHA-256.
