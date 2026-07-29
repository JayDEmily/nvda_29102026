# Parallel Cycle 01 — Controlled Launch Index

## Current launch status

`WORKER_LAUNCH_OPEN_FROM_PM_PUBLISHED_ACCEPTED_CHECKPOINT`

The four assignments are authorised for worker launch only from the single immutable full-history checkpoint published by the Project Manager after independent Repair 2 control PASS and PM acceptance. Repair 1 remains historical hard-block evidence; the Repair 2 tester result is preserved at commit `e672b27ca01efbd1f47de27d41fa54733bc73c63`.

## Exact thread names and revision

| Lane | Worker thread | Tester thread | Unit | Revision |
|---|---|---|---|---|
| 1A | `Lane 1AW` | `Lane 1AT` | M01 relevant-test routing | `R1` |
| 2A | `Lane 2AW` | `Lane 2AT` | M04 authority sufficiency | `R1` |
| 3A | `Lane 3AW` | `Lane 3AT` | M07 authority sufficiency | `R1` |
| 4A | `Lane 4AW` | `Lane 4AT` | M08 authority sufficiency | `R1` |

Lanes 5 and 6 are held. The exact eight-brief inventory and SHA-256 values are recorded in `project_control/canonical_project_manager/PARALLEL_CYCLE_01/BRIEF_PACK_MANIFEST.tsv`.

## Accepted pre-launch control test

`Parallel Control T1` returned PASS and the Project Manager accepted Repair 2. The tester brief and evidence remain historical control records. Worker threads must use the PM-published accepted checkpoint, not either repair archive directly.

## Lane launch sequence after PM acceptance

1. Use the same PM-published, independently tested full-history checkpoint for every worker.
2. Create the four worker threads using the exact names above and attach the checkpoint plus the matching `W` brief.
3. Do not create a lane tester task until its matching Worker Candidate Archive is returned.
4. Give the tester the same PM source checkpoint, the Worker Candidate Archive and the matching `T` brief.
5. Return the exact-named tester portability artefact to the Master Project Manager. Do not integrate it manually.

The PM launch message must state the exact source archive filename, SHA-256, branch and commit. Those values are supplied at issue time because the final archive cannot embed its own SHA-256.
