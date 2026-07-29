> **SUPERSEDED AND REJECTED BEFORE LAUNCH:** This historical PM disposition was withdrawn by `PARALLEL_CONTROL_SELF_AUDIT_REJECTION_V1.md`. It is not current launch authority.

# Parallel Workflow Enablement V1 — Project Manager Review

## Disposition

`ACCEPTED:PARALLEL_WORKFLOW_ENABLEMENT_V1`

This disposition accepts the project-control architecture and Cycle 1 allocation only. It does not accept any future M01, M04, M07 or M08 worker result, open implementation, admit physical tests or create a global Gate D state.

## Source and authority

- Direct user authority: establish the parallel method on a new branch, update the operating controls, use exact `Lane 1AW/1AT` through `Lane 4AW/4AT` names and hold Lanes 5 and 6.
- Source checkpoint: `review/m01-authority-v1` at `ae7c8b05bf3742a5c0be530a26617d999313d232` from `NVDA_M01_AUTHORITY_V1_PM_ACCEPTED_ae7c8b0_20260728_FULL_HISTORY.tar.gz`, SHA-256 `0b311e108bb0cdc39cd4776021bdbdfa36f3a498d01fa0b4ae1630daa8d9085a`.
- Control branch: `control/parallel-workflow-enablement-v1`.
- External architecture source: `MASTER_PARALLEL_WORKFLOW_ARCHITECTURE.md`, SHA-256 `58b812adc77c16a7c4368bc7403857152f67b0e4bde5dba84be79f297b1c700f`.
- Project-specific design source: `NVDA_PARALLEL_WORKFLOW_PROJECT_SPECIFIC_ROLLOUT_PLAN_20260728.md`, SHA-256 `4b24f028f0ceb845f75a2853f67ae24a83f313c12b304e6867ff691c2439b5ea`.

## Known true

1. The programme remains one repository with one canonical Project Manager control and integration front.
2. Six lanes are permanent capacity identifiers. They are not permanent module ownership and do not require six long-lived branches.
3. Every assignment uses a fresh worker branch and matching tester branch from a named immutable checkpoint.
4. A worker receives one semantic leaf or bounded implementation slice, exact read/write sets and locks, then returns one candidate archive and stops.
5. A tester is independent, begins from the exact worker commit, adds only tester-owned evidence and returns one tester-result archive. Tester PASS is suitable for PM integration review only.
6. Canonical acceptance and integration remain sequential. Stale material reads or combined conflicts require revalidation or repair.
7. The accepted architecture exposes four current dependency-independent roots after M13: M01, M04, M07 and M08.
8. Cycle 1 therefore lawfully allocates four assignments and holds the remaining two lanes instead of inventing downstream work.
9. Cycle 1 write sets are module-local and pairwise disjoint. Source, physical tests, configuration, normative meaning, vocabulary/proof registries and global controls remain locked to lane workers and testers.
10. The final checkpoint SHA-256 must be supplied externally in the PM launch block because an archive cannot contain its own final hash without circularity.

## Cycle 1 accepted allocation

| Assignment | Worker | Tester | Unit | Owner / contract boundary |
|---|---|---|---|---|
| `1A` | `Lane 1AW` | `Lane 1AT` | `M01-PROOF-MLC-R-V1` | M01 / K01–K03 |
| `2A` | `Lane 2AW` | `Lane 2AT` | `M04-PROOF-MLC-A-V1` | M04 / K07 |
| `3A` | `Lane 3AW` | `Lane 3AT` | `M07-PROOF-MLC-A-V1` | M07 / K12 and `OBL-M07-POSITIVE` |
| `4A` | `Lane 4AW` | `Lane 4AT` | `M08-PROOF-MLC-A-V1` | M08 / K13 |
| Lanes 5 and 6 | held | held | none | no additional dependency-safe root |

## Ruled out

- six permanent divergent working branches;
- workers knowing or coordinating with other active lanes;
- autonomous lane continuation into `B` assignments or later leaves;
- shared writable global control, registry, normative, configuration, test or architecture files;
- testers repairing worker output or canonicalising it;
- parallel integration, parallel canonical branches or manual integration by the user;
- using Lanes 5 and 6 as administrative filler;
- source, test or behavioural change in this control checkpoint.

## Validation boundary

Mechanical checks may establish names, counts, paths, hashes, changed-path boundaries and collisions. They do not establish semantic authority. The PM disposition above follows full control-document reading, architecture/dependency review and manual comparison of each brief with its module boundary.

Behavioural tests are not required for this checkpoint because no source, physical test, configuration or runtime behaviour changes. Future lane results remain subject to their own worker evidence, independent tester verdict and PM integration review.

## Next gate

Publish one Git-preserving full-history checkpoint for this branch and issue the exact matching worker brief to `Lane 1AW`, `Lane 2AW`, `Lane 3AW` and `Lane 4AW`. Create a tester thread only when its matching worker candidate returns. No fifth, sixth or `B` assignment is open.
