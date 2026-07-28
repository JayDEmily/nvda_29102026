# NVDA Parallel Workflow Architecture

## Status and authority

**Status:** `ACCEPTED_PROJECT_SPECIFIC_PARALLEL_OPERATING_LAW`
**Authorised:** 28 July 2026 by direct user instruction
**Owner:** Master Project Manager
**Parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live state:** `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`

This document governs parallel execution inside the existing repository and programme. It does not create a second programme, weaken module-local proof or allow parallel canonical states.

## Operating model

One Master Project Manager controls one canonical repository. Six permanent lanes provide execution capacity. Each assignment has one disposable worker thread and one independent tester thread. Worker and tester activity may overlap; Project Manager acceptance, integration and checkpoint publication remain sequential.

A lane is not permanent ownership of a module, a long-lived branch, permission to select follow-on work or a substitute for dependency readiness.

## Naming

For assignment `<lane><letter>`:

- worker thread: `Lane <lane><letter>W`;
- tester thread: `Lane <lane><letter>T`;
- worker branch: `work/lane-<lane><letter-lower>-<module>-<leaf>`;
- tester branch: `test/lane-<lane><letter-lower>-<module>-<leaf>`.

Cycle 1 exact labels are `Lane 1AW/1AT`, `2AW/2AT`, `3AW/3AT` and `4AW/4AT`.

## Canonical source

The PM launch message supplies one immutable full-history repository archive with exact filename, SHA-256, branch, commit and clean-worktree expectation. All Cycle 1 workers use that same archive. The launch identifiers are supplied outside the repository because an archive cannot contain its own final SHA-256 without circularity.

Every worker and tester must verify the source archive, complete `.git` history, expected commit and clean worktree before acting.

## Assignment law

One assignment is one MLC leaf or one bounded implementation slice. The brief must define:

- one question and pass/fail boundary;
- owner module and contract;
- runtime prerequisites;
- exact full-read set;
- material read set for stale-base checking;
- exact writable paths;
- global, contract-owner and test-file locks;
- validation and returned artefact;
- explicit stop and no-follow-on rule.

A newly discovered required write path causes `RETURN_SCOPE_REOPEN_REQUIRED` before mutation.

## Global locks

Lane workers and testers may not mutate unless an exclusive PM integration unit expressly opens them:

- `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER*.md`;
- numbered normative documents and vocabulary authority;
- ExecPlan, Gate C protocol, this architecture or workflow registry;
- accepted architecture report/workbook/JSON/graphs;
- `config/retained_test_registry.yaml`, `config/proof_blocks.yaml`;
- root packaging, dependency and lock files;
- shared migrations, composition surfaces and global registries;
- another lane's module-control or evidence paths.

A physical test file has one mutating owner at a time. Cycle 1 permits no physical test mutation.

## Lifecycle

`ALLOCATED_AWAITING_LAUNCH → WORKER_ACTIVE → CANDIDATE_RETURNED → TESTER_ACTIVE → PASS / FAIL_REPAIRABLE / HARD_BLOCK → PM_ACCEPTED_FOR_INTEGRATION → QUEUED → INTEGRATED → AGGREGATE_VALIDATED → CLOSED`

Additional states are `RETURN_SCOPE_REOPEN_REQUIRED`, `BLOCKED_MISSING_AUTHORITY`, `BLOCKED_DEPENDENCY`, `STALE_REVALIDATION_REQUIRED` and `INTEGRATION_CONFLICT_REPAIR_REQUIRED`.

A repair stays with the same W/T pair only while authority, dependencies and write set remain unchanged. Otherwise the assignment returns to the PM.

## Worker return

The worker returns exactly one Git-preserving candidate archive containing the complete repository and `.git`, on the named worker branch, with a clean worktree and one bounded worker commit or declared ordered commit series. The result must include raw validation evidence and a worker record under the exact module-local paths authorised by the brief.

The worker stops after return. It does not create canonical state or begin the next assignment.

## Tester return

The tester starts from the worker candidate, verifies ancestry to the PM source checkpoint and independently reviews the exact result. It may add only tester-owned review/evidence paths named in its brief and must not repair worker output.

Verdicts:

- `PASS` — suitable for PM integration review;
- `FAIL_REPAIRABLE` — bounded defects within the original assignment;
- `HARD_BLOCK` — missing authority, invalid baseline, architecture conflict or scope change.

On PASS, the tester returns exactly one Git-preserving tester-approved archive containing the worker commit(s), tester evidence commit, complete `.git` history and clean worktree. Tester PASS is not canonical acceptance.

## Stale-base law

The registry records each assignment's material read set. If a canonical integration changes any material read-set item before the assignment is integrated, its tester verdict becomes `STALE_REVALIDATION_REQUIRED`.

No lane-local continuation from unintegrated work is permitted during Cycle 1.

## Integration

The PM:

1. verifies archive hash, ancestry, branch, commits and clean state;
2. compares actual changes with the declared write set and locks;
3. rereads worker and tester records;
4. accepts or returns the assignment;
5. imports one assignment only;
6. runs targeted, affected, architecture and governance validation;
7. records the integration result before importing the next assignment;
8. runs aggregate validation after the batch;
9. updates global controls in one PM closeout;
10. publishes one new full-history canonical checkpoint.

An isolated PASS invalidated by combined integration becomes `INTEGRATION_CONFLICT_REPAIR_REQUIRED` and must be repaired from the PM-designated current integration base and independently retested.

## Cycle 1

| Lane | Unit | Worker | Tester | State |
|---|---|---|---|---|
| 1A | `M01-PROOF-MLC-R-V1` | `Lane 1AW` | `Lane 1AT` | allocated |
| 2A | `M04-PROOF-MLC-A-V1` | `Lane 2AW` | `Lane 2AT` | allocated |
| 3A | `M07-PROOF-MLC-A-V1` | `Lane 3AW` | `Lane 3AT` | allocated |
| 4A | `M08-PROOF-MLC-A-V1` | `Lane 4AW` | `Lane 4AT` | allocated |
| 5 | held | — | — | dependency-held |
| 6 | held | — | — | dependency-held |

Cycle 1 changes no production source, physical tests, runtime configuration, normative authority, vocabulary or global proof registries. Integration order is M01, M04, M07, M08.
