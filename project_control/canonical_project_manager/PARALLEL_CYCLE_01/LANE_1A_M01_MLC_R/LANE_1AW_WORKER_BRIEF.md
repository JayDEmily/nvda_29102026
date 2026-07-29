# Lane 1AW — Worker Brief

## Assignment identity

- Worker thread: `Lane 1AW`
- Matching tester thread: `Lane 1AT`
- Assignment: `1A`
- Unit: `M01-PROOF-MLC-R-V1`
- Owner module: M01 `source_admission`
- Contract boundary: K01 `SourceArtifactEnvelope`; K02 `CaptureReceipt`; K03 `RawSignalBatch`
- Worker branch: `work/lane-1a-m01-mlc-r-v1`
- Revision: `R1`
- Tester branch: `test/lane-1a-m01-mlc-r-v1`

## Source checkpoint

Use the single full-history canonical archive supplied in the PM launch message as the sole repository input. Before acting, verify the exact archive filename and SHA-256, expected branch and commit, clean worktree and complete `.git` history stated in that message.

Do not proceed if any launch identifier is absent or mismatched. Create the named worker branch from the exact PM-designated source commit.

## Assignment-local full-read manifest

Before substantive work, create and maintain:

`project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/FULL_READ_MANIFEST.tsv`

Record every required file, reason, read status, mutation relevance and pre-mutation SHA-256 where available. This lane-local manifest is inside the authorised write set. Do not modify the global historical `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`.

## Role and one question

Act only as the `M01-PROOF-MLC-R-V1` worker.

> Which physical tests claim current authority over the bounded M01 general `source_admission` contract through governed joins, and which are demonstrably unrelated legacy shadow evidence?

Complete this one leaf and return. Do not choose or begin another leaf.

## Required full reading

1. `00_TASK/PROJECT_EXECUTION_METHOD.md`
2. `AGENTS.md`
3. `PLANS.md`
4. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
5. `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
6. `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
7. `project_control/canonical_project_manager/EXEC_PLAN.md`
8. `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`
9. `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md`
10. `ROADMAP_LEDGER_V2.md`
12. `project_control/canonical_project_manager/modules/M01/M01_AUTHORITY_WORKER_RECORD_V1.md`
13. `project_control/canonical_project_manager/modules/M01/M01_AUTHORITY_PM_REVIEW_V1.md`
14. the complete M01 authority evidence trees named by the PM review
15. `project_control/canonical_project_manager/units/PM-011/P2_PHYSICAL_TEST_CENSUS.tsv` and `project_control/canonical_project_manager/units/PM-011/PM-011_FULL_READ_MANIFEST.tsv`
16. `project_control/normative_authority_top_down_alignment/EXISTING_TEST_DISPOSITION.tsv`
17. `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv`
18. `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv`
19. `project_control/normative_authority_top_down_alignment/GATE_C_TIER_A_PROMOTION_MANIFEST.tsv`
20. every retained `D-xxx` proof envelope and N-decision actually joined to M01
21. `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md`, plus exact M01 rows in `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` and `project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json`
22. every registry, proof-block or source-ownership row used to include or exclude a physical test


### Mandatory test-subtree route

Because this assignment reads paths under `tests/`, read `tests/AGENTS.override.md` and obey its sequence before inspecting any physical test. The required route includes:

1. `AGENTS.md`;
2. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
3. `docs/01_NORMATIVE_CORE.md` and the relevant working companion;
4. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`, `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` and `docs/vocabulary/vocabulary_registry.md`;
5. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`;
6. `config/retained_test_registry.yaml`;
7. `config/proof_blocks.yaml`;
8. `tests/AGENTS.override.md`;
9. only then the specific tests, fixtures, code and retained evidence in scope.

The override and listed registries are read-only.

Read all directly cited proposition and evidence rows in full. Search, joins and scripts may assist inventory and mechanical checking; they may not decide authority or semantic sufficiency.

## Runtime prerequisites

M13 implementation accepted; `M01-PROOF-MLC-A-V1` independently accepted. M01 source and tests remain closed.

## Material read set

M01 accepted authority records; PM-011; current test-authority/requirements/disposition/proof-block/registry rows; M01 architecture and D/N mappings.

If the PM-designated canonical state changes any material read-set item before integration, the assignment requires revalidation.

## Exact writable paths

- `project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/**`

Create no other tracked path. If another path is required, stop before mutation and return `RETURN_SCOPE_REOPEN_REQUIRED`.

## Global and cross-lane locks

Do not modify:

- `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER*.md`, numbered docs or vocabulary authority;
- the ExecPlan, Gate C protocol, parallel architecture or workflow registry;
- accepted architecture report/workbook/JSON/graphs;
- source, physical tests, fixtures, configuration, proof blocks, retained-test registry, packaging or lockfiles;
- another module's control/evidence directory;
- any worker or tester brief.

Do not consume unintegrated work outside this assignment or coordinate its semantic decision with another assignment. No global workflow-registry reading is required.

## Required work and output

Produce a complete physical-test routing inventory for the bounded accepted M01 authority proposition. For each included test, show the governed join chain from physical test census to current proposition/owner evidence. For each excluded test classified `LEGACY_SHADOW_UNADMITTED`, show enough objective routing evidence to establish that it does not currently claim the bounded M01 proposition.

Do not observe test behaviour, interpret assertions, decide Tier A/Tier B admission, design proof or run implementation repair. Filename, directory and import location alone are insufficient routing authority.

Do not label a test authoritative, adequate, weak or false-positive. This leaf routes claims only.

Label the worker result exactly:

`PROPOSED_M01_RELEVANT_TEST_ROUTING_V1_AWAITING_LANE_1AT`

## Validation

1. Prove every routed physical test exists in PM-011.
2. Prove every positive route has at least one current governed join beyond path/location.
3. Prove no physical test is silently omitted from the declared M01 candidate universe.
4. Reconcile counts and duplicate paths mechanically.
5. Validate that no source/test/config/normative/global-control path changed.

Also run and retain:

- `git status --short --branch` before and after;
- `git diff --check`;
- changed-path validation against the exact write set;
- `git fsck --full --no-dangling`;
- hash validation for every worker evidence file.

No behavioural test pass is required because Cycle 1 does not mutate source or physical tests. A worker may run read-only scoped commands only when they materially support the leaf and must record exact output and exit status.

## Git and exact return artefact

Commit only the bounded worker record and lane-owned evidence. The lane-owned evidence must include `FULL_READ_MANIFEST.tsv`, `WORKER_CLAIM.md`, changed-path evidence, file hashes, raw validation with exit statuses and fresh-extraction reconstruction evidence.

Create exactly one Git-preserving full-history archive outside the repository with this exact filename:

`NVDA_LANE_1A_M01_MLC_R_WORKER_CANDIDATE_R1_FULL_HISTORY.tar.gz`

Verify by fresh extraction: branch, commit, clean worktree, complete `.git`, ancestry to the PM source commit, changed paths and evidence hashes.

Return that archive only, its SHA-256 and a concise result table. End with:

`READY_FOR_LANE_1AT`
