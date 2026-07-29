# Lane 1AT — Independent Tester Brief

## Assignment identity

- Tester thread: `Lane 1AT`
- Worker thread: `Lane 1AW`
- Assignment: `1A`
- Unit: `M01-PROOF-MLC-R-V1`
- Owner module: M01 `source_admission`
- Contract boundary: K01 `SourceArtifactEnvelope`; K02 `CaptureReceipt`; K03 `RawSignalBatch`
- Expected worker branch: `work/lane-1a-m01-mlc-r-v1`
- Revision: `R1`
- Tester branch: `test/lane-1a-m01-mlc-r-v1`

## Inputs

Use only:

1. the exact PM canonical archive and launch identifiers supplied for Cycle 1; and
2. the exact worker candidate archive returned by `Lane 1AW`.

Verify both archive hashes, complete `.git` history, worker ancestry to the PM source commit, expected worker branch/commit and clean worker worktree. Reconstruct the exact candidate, then create the named tester branch from the exact worker candidate commit before adding tester-owned evidence.

## Assignment-local full-read manifest

Before substantive review, independently create and maintain:

`project_control/canonical_project_manager/modules/M01/raw_validation/tester_mlc_r_v1/FULL_READ_MANIFEST.tsv`

Record every required file, reason, read status, mutation relevance and pre-review SHA-256 where available. Do not copy the worker manifest as proof of tester reading and do not modify the global historical `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`.

## Role and one question

Act only as the independent tester for `M01-PROOF-MLC-R-V1`.

> Does the worker route the complete bounded M01 physical-test candidate population through current governed joins without performing observation, semantic disposition or location-based admission?

Do not repair worker output, broaden authority or review another assignment. No global workflow-registry reading is required.

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
23. the complete Lane 1AW worker record and raw routing evidence


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

Read the worker's complete changed files and evidence in full. Do not accept a worker conclusion from summaries, hashes, counts or green commands alone.

## Scope and locks

The worker is permitted to change only:

- `project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M01/raw_validation/mlc_r_v1/**`

The tester may add only:

- `project_control/canonical_project_manager/modules/M01/M01_RELEVANT_TEST_ROUTING_TESTER_REVIEW_V1.md`
- `project_control/canonical_project_manager/modules/M01/raw_validation/tester_mlc_r_v1/**`

All source, physical tests, configuration, numbered docs, global controls, architecture artefacts, proof/vocabulary registries and other lane paths remain read-only. Any out-of-scope worker mutation is an automatic `HARD_BLOCK` unless the PM reopens scope.

## Independent checks

1. Independently reproduce the candidate universe and governed joins.
2. Sample nothing: reconcile every routed physical test and every exclusion.
3. Challenge at least one plausible false-positive path-only route and one plausible false-negative omission.
4. Confirm the worker made no factual assertion observation or test-admission decision.
5. Confirm exact write-set compliance and no cross-lane/global mutation.

The tester must perform at least one independent challenge not copied from the worker's validation approach.

## Verdict

Return exactly one:

- `PASS`
- `FAIL_REPAIRABLE`
- `HARD_BLOCK`

`PASS` means only `SUITABLE_FOR_PM_M01_MLC_R_INTEGRATION_REVIEW`. It is not canonical acceptance and does not open the next leaf.

For `FAIL_REPAIRABLE`, list bounded defects within the existing authority/write set. For `HARD_BLOCK`, identify the missing authority, invalid baseline, architecture conflict or required scope change.

## Tester record and exact portability artefact

Create the tester review record and raw evidence only in the tester-owned paths. Commit the tester evidence after the unchanged worker commit or ordered worker commit series. Never modify, squash or rewrite worker commits.

Return exactly one tar archive outside the repository, named by verdict:

- PASS: `NVDA_LANE_1A_M01_MLC_R_TESTER_APPROVED_R1.tar.gz`
- FAIL_REPAIRABLE: `NVDA_LANE_1A_M01_MLC_R_TESTER_FAIL_REPAIRABLE_R1.tar.gz`
- HARD_BLOCK: `NVDA_LANE_1A_M01_MLC_R_TESTER_HARD_BLOCK_R1.tar.gz`

The archive must contain exactly one portability package with:

- `MANIFEST.json` recording assignment `1A`, revision `R1`, PM source archive/SHA/branch/commit, worker branch/commit(s), tester branch/evidence commit, verdict, exact worker/tester write sets and package member hashes;
- `changes.bundle`, created from the tester branch and verified with `git bundle verify`, containing the worker and tester evidence commits with reconstructable PM-source ancestry;
- `CHANGED_PATHS.tsv`;
- `FILE_SHA256.tsv`;
- `WORKER_CLAIM.md` copied byte-for-byte from worker evidence;
- `TESTER_VERDICT.md`;
- `validation/` with raw independent command output and at least one tester-owned challenge;
- `RECONSTRUCTION.txt` proving fresh reconstruction, exact commits, expected branch and clean worktree;
- `SHA256SUMS` for every other package member.

Verify package SHA-256, `git bundle verify`, fresh reconstruction, exact changed paths, evidence hashes, `git diff --check` and `git fsck --full --no-dangling`. Return the one archive, its SHA-256, the verdict and a concise defect/evidence table.

End a PASS with:

`SUITABLE_FOR_PM_M01_MLC_R_INTEGRATION_REVIEW`
