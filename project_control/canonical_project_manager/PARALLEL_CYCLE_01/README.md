# Parallel Cycle 01 — Launch Index

## Exact thread names

| Lane | Worker thread | Tester thread | Unit |
|---|---|---|---|
| 1A | `Lane 1AW` | `Lane 1AT` | M01 relevant-test routing |
| 2A | `Lane 2AW` | `Lane 2AT` | M04 authority sufficiency |
| 3A | `Lane 3AW` | `Lane 3AT` | M07 authority sufficiency |
| 4A | `Lane 4AW` | `Lane 4AT` | M08 authority sufficiency |

Lanes 5 and 6 are held.

The exact eight-brief inventory and SHA-256 values are recorded in `project_control/canonical_project_manager/PARALLEL_CYCLE_01/BRIEF_PACK_MANIFEST.tsv`.

## Manual launch sequence

1. Use the same PM-published full-history checkpoint for every worker.
2. Create the four worker threads using the exact names above and attach the checkpoint plus the matching `W` brief.
3. Do not create a tester task until its matching worker archive is returned.
4. Give the tester the same PM source checkpoint, the worker archive and the matching `T` brief.
5. Return tester-approved archives to the Master Project Manager. Do not integrate them manually.

The PM launch message must state the exact source archive filename, SHA-256, branch and commit. Those values are deliberately supplied at issue time because the final archive cannot embed its own SHA-256.
