# NVDA Parallel Workflow Architecture

## Status and authority

**Status:** `ACTIVE:PARALLEL_CYCLE_01_AGGREGATE_VALIDATED`
**Authorised:** 28 July 2026 by direct user instruction
**Repair authorised:** 29 July 2026 by direct user instruction
**Owner:** Master Project Manager
**Parent plan:** `project_control/canonical_project_manager/EXEC_PLAN.md`
**Live state:** `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`

This document governs parallel execution inside the existing repository and programme. It does not create a second programme, weaken module-local proof or allow parallel canonical states. Repair 2 passed independent control testing and PM acceptance; Cycle 01 then completed its worker/tester and serial-integration lifecycle under this law.

## Operating model

One Master Project Manager controls one canonical repository. Six Parallel Execution Lanes provide capacity. Each Lane Assignment has one disposable worker thread and one independent tester thread. Worker and tester activity may overlap; Project Manager acceptance, integration and checkpoint publication remain sequential.

A lane is not permanent ownership of a module, a long-lived branch, permission to select follow-on work or a substitute for dependency readiness. Lane 5 and Lane 6 may remain held without branches or filler assignments.

## Naming and revision law

For assignment `<lane><letter>`:

- worker thread: `Lane <lane><letter>W`;
- tester thread: `Lane <lane><letter>T`;
- worker branch: `work/lane-<lane><letter-lower>-<module>-<leaf>`;
- tester branch: `test/lane-<lane><letter-lower>-<module>-<leaf>`;
- initial assignment revision: `R1`; bounded repair increments the revision to `R2`, `R3`, and so on without changing the assignment ID.

Cycle 1 exact labels are `Lane 1AW/1AT`, `2AW/2AT`, `3AW/3AT` and `4AW/4AT`.

## Canonical source

The PM launch message supplies one immutable full-history repository archive with exact filename, SHA-256, branch, commit and clean-worktree expectation. All Cycle 1 workers use that same independently tested and PM-accepted checkpoint. The launch identifiers are supplied outside the repository because an archive cannot contain its own final SHA-256 without circularity.

Every worker and tester must verify the source archive, complete `.git` history, expected commit and clean worktree before acting. A worker must not start from the untested control-repair branch.

## Assignment law

One assignment is one MLC leaf or one bounded implementation slice. The standalone brief must define:

- one question and pass/fail boundary;
- assignment revision, owner module and contract;
- runtime prerequisites;
- exact full-read set and assignment-local full-read manifest path;
- Material Read Set for stale-base checking;
- exact writable paths;
- global, contract-owner and test-file locks;
- validation and exact returned artefact names;
- explicit stop and no-follow-on rule.

A newly discovered required write path causes `RETURN_SCOPE_REOPEN_REQUIRED` before mutation.

## Full-read evidence

The global `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv` is cumulative historical evidence and is not the current manifest for an isolated lane.

Each worker and tester must create its own `FULL_READ_MANIFEST.tsv` inside the exact lane-owned raw-validation directory named in the brief before substantive work. The manifest must record path, reason, read status, mutation relevance and pre-mutation SHA-256 where available. The tester independently creates a separate manifest; it does not inherit the worker manifest as proof of its own reading.

## Global locks

Lane workers and testers may not mutate unless an exclusive PM integration unit expressly opens them:

- `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER*.md`;
- numbered normative documents and vocabulary authority;
- ExecPlan, Gate C protocol, this architecture or workflow registry;
- accepted architecture report/workbook/JSON/graphs;
- `config/retained_test_registry.yaml`, `config/proof_blocks.yaml`;
- root packaging, dependency and lock files;
- shared migrations, composition surfaces and global registries;
- any path outside the exact write set in the assignment brief.

A physical test file has one mutating owner at a time. Cycle 1 permits no physical test mutation.

## Lane Assignment lifecycle

`ALLOCATED_CONTROL_TEST_PENDING → ALLOCATED_AWAITING_LAUNCH → WORKER_ACTIVE → CANDIDATE_RETURNED → TESTER_ACTIVE → PASS / FAIL_REPAIRABLE / HARD_BLOCK → PM_ACCEPTED_FOR_INTEGRATION → QUEUED → INTEGRATED → AGGREGATE_VALIDATED → CLOSED`

Additional states are `RETURN_SCOPE_REOPEN_REQUIRED`, `BLOCKED_MISSING_AUTHORITY`, `BLOCKED_DEPENDENCY`, `STALE_REVALIDATION_REQUIRED` and `INTEGRATION_CONFLICT_REPAIR_REQUIRED`.

A repair stays with the same W/T pair only while authority, dependencies and write set remain unchanged. Otherwise the assignment returns to the PM. A tester verdict does not change the canonical programme state.

## Worker Candidate Archive

The worker returns exactly one Git-preserving Worker Candidate Archive using the exact filename in its brief. It contains the complete repository and `.git`, the named worker branch, a clean worktree and one bounded worker commit or declared ordered commit series.

The worker-owned raw-validation directory must include:

- `FULL_READ_MANIFEST.tsv`;
- `WORKER_CLAIM.md`;
- changed-path evidence;
- file-hash evidence;
- raw validation output and exit statuses;
- fresh-extraction reconstruction evidence.

The worker stops after return. It does not create canonical state or begin the next assignment.

## Independent tester and portability artefact

The tester starts from the exact Worker Candidate Archive, verifies ancestry to the PM source checkpoint and independently reviews the exact result. It may add only tester-owned review/evidence paths named in its brief and must not repair, squash or rewrite worker output.

Verdicts:

- `PASS` — suitable for PM integration review;
- `FAIL_REPAIRABLE` — bounded defects within the original assignment;
- `HARD_BLOCK` — missing authority, invalid baseline, architecture conflict or scope change.

For every verdict the tester returns one exact-named tar archive. A PASS archive is the Tester-approved Portability Artefact and must contain:

- `MANIFEST.json` with assignment, revision, PM source identifiers, worker and tester commits, verdict and declared write sets;
- `changes.bundle`, verified with `git bundle verify`, containing the worker and tester evidence commits with the PM source commit as reconstructable ancestry;
- `CHANGED_PATHS.tsv`;
- `FILE_SHA256.tsv`;
- `WORKER_CLAIM.md` copied unchanged from worker evidence;
- `TESTER_VERDICT.md`;
- `validation/` containing raw tester command output and independent challenges;
- `RECONSTRUCTION.txt` proving fresh reconstruction, branch, commits and clean worktree;
- `SHA256SUMS` for every package member other than `SHA256SUMS` itself.

A `FAIL_REPAIRABLE` or `HARD_BLOCK` archive uses the exact verdict filename in the brief and the same evidence structure, with the verdict and defects recorded. Tester PASS is not canonical acceptance.

## Informational isolation

A lane brief contains its own source, authority, read set, write set, locks and return contract. A worker or tester is not required to read the global workflow registry or another lane brief, coordinate with another lane, or consume another lane's unintegrated work. Repository visibility is not represented as secrecy; the operative guarantee is assignment independence and non-consumption.

## Material Read Set and stale-base law

The PM registry records each assignment's Material Read Set. If a canonical integration changes any material read-set item before the assignment is integrated, its tester verdict becomes `STALE_REVALIDATION_REQUIRED`.

No lane-local continuation from unintegrated work is permitted during Cycle 1.

## Integration

The PM:

1. verifies package hash, bundle, ancestry, branches, commits and clean reconstructed state;
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

## Independent Control Test

A newly authored or materially repaired parallel-control checkpoint must be reviewed by a separate control-tester thread before any lane launch. Cycle 1 uses the exact thread name `Parallel Control T1`. The control tester may add only its named evidence paths, must not repair the control package and returns one full-history tester checkpoint. PASS means suitable for PM control acceptance, not automatic launch authority.

## Cycle 1

| Lane | Unit | Worker | Tester | Revision | State |
|---|---|---|---|---|---|
| 1A | `M01-PROOF-MLC-R-V1` | `Lane 1AW` | `Lane 1AT` | `R1` | `AGGREGATE_VALIDATED_CLOSED` |
| 2A | `M04-PROOF-MLC-A-V1` | `Lane 2AW` | `Lane 2AT` | `R1` | `AGGREGATE_VALIDATED_CLOSED_AUTHORITY_RETURN` |
| 3A | `M07-PROOF-MLC-A-V1` | `Lane 3AW` | `Lane 3AT` | `R1` | `AGGREGATE_VALIDATED_CLOSED_AUTHORITY_RETURN` |
| 4A | `M08-PROOF-MLC-A-V1` | `Lane 4AW` | `Lane 4AT` | `R1` | `AGGREGATE_VALIDATED_CLOSED_AUTHORITY_RETURN` |
| 5 | held | — | — | — | `HELD_BLOCKED_DEPENDENCY` |
| 6 | held | — | — | — | `HELD_BLOCKED_DEPENDENCY` |

Cycle 1 changed no production source, physical tests or runtime configuration. The four accepted results were integrated in order M01, M04, M07, M08 and passed aggregate validation. M01 may advance only through a new PM brief to MLC-O; M04, M07 and M08 remain at bounded numbered-authority return gates. Any future parallel cycle requires a new PM allocation and immutable source checkpoint.
