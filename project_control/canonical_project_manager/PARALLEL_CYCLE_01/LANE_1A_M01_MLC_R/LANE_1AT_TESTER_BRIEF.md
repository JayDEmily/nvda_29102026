# Lane 1AT — Independent Tester Brief

## Assignment identity

- Tester thread: `Lane 1AT`
- Worker thread: `Lane 1AW`
- Assignment: `1A`
- Unit: `M01-PROOF-MLC-R-V1`
- Owner module: M01 `source_admission`
- Contract boundary: K01 `SourceArtifactEnvelope`; K02 `CaptureReceipt`; K03 `RawSignalBatch`
- Expected worker branch: `work/lane-1a-m01-mlc-r-v1`
- Tester branch: `test/lane-1a-m01-mlc-r-v1`

## Inputs

Use only:

1. the exact PM canonical archive and launch identifiers supplied for Cycle 1; and
2. the exact worker candidate archive returned by `Lane 1AW`.

Verify both archive hashes, complete `.git` history, worker ancestry to the PM source commit, expected worker branch/commit and clean worker worktree. Reconstruct the exact candidate, then create the named tester branch from the exact worker candidate commit before adding tester-owned evidence.

## Role and one question

Act only as the independent tester for `M01-PROOF-MLC-R-V1`.

> Does the worker route the complete bounded M01 physical-test candidate population through current governed joins without performing observation, semantic disposition or location-based admission?

Do not repair worker output, broaden authority or review another lane.

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
11. `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`
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

## Tester record and archive

Create a tester review record and raw evidence only in the tester-owned paths. For every verdict, commit the tester evidence after the unchanged worker commit(s), create exactly one Git-preserving full-history tester-result archive outside the repository and verify by fresh extraction:

- PM source ancestry;
- exact worker commit(s);
- tester evidence commit;
- declared changed paths;
- clean worktree;
- evidence hashes;
- `git diff --check` and `git fsck --full --no-dangling`.

Return exactly one tester-result archive, its SHA-256, the verdict and a concise defect/evidence table. Never modify or rewrite the worker commit(s).

End a PASS with:

`SUITABLE_FOR_PM_M01_MLC_R_INTEGRATION_REVIEW`
