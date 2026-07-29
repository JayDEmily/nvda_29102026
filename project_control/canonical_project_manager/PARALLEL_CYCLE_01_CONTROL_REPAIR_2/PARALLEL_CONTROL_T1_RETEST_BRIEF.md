# Parallel Control T1 — Independent Tester Brief

## Identity

- Tester thread: `Parallel Control T1`
- Control revision: `CONTROL-R1`
- Expected source branch: `control/parallel-workflow-enablement-v1-repair-2`
- Tester branch: `test/parallel-workflow-enablement-v1-repair-2`
- Role: independent control-package tester; not a lane tester and not a repair worker

## Source checkpoint

Use `NVDA_PARALLEL_WORKFLOW_CYCLE_01_CONTROL_REPAIR_2_20260729_FULL_HISTORY.tar.gz` as the sole repository input. Verify the exact filename, SHA-256, branch, commit, clean worktree and complete `.git` history supplied in the launch message. Create the tester branch from that exact commit. Do not proceed on any mismatch.

## One question

> Does the repaired parallel-control checkpoint lawfully and deterministically define Cycle 1 assignments, vocabulary, manifests, write locks, isolated worker/tester briefs, exact portability artefacts, stale-base treatment and serial PM integration without authorising a lane launch prematurely?

Do not repair the package. Return defects to the PM.

## Required full reading

Read in full:

1. `00_TASK/PROJECT_EXECUTION_METHOD.md`;
2. `AGENTS.md`;
3. `PLANS.md`;
4. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
5. `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` and `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`;
6. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`, `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`, `docs/vocabulary/README.md`, `docs/vocabulary/CONSOLIDATION_WORKFLOW.md` and `docs/vocabulary/vocabulary_registry.md`;
7. `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`;
8. `project_control/canonical_project_manager/EXEC_PLAN.md`;
9. `project_control/canonical_project_manager/GATE_C_COMPLETION_PROTOCOL.md`;
10. `project_control/canonical_project_manager/PARALLEL_WORKFLOW_ARCHITECTURE.md`;
11. `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`;
12. `ROADMAP_LEDGER_V2.md`;
13. all eight files under `project_control/canonical_project_manager/PARALLEL_CYCLE_01/LANE_*`;
14. `project_control/canonical_project_manager/PARALLEL_CYCLE_01/README.md` and `BRIEF_PACK_MANIFEST.tsv`;
15. `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_SELF_AUDIT_REJECTION_V1.md`;
16. `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_PM_RECORD_V1.md`;
17. `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_WORKFLOW_VOCABULARY_ADMISSION_V1.md`;
18. `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_REPAIR_FULL_READ_MANIFEST.tsv`;
19. `project_control/canonical_project_manager/parallel_workflow_validation/validate_parallel_cycle_01.py`;
20. the project-folder attachments `MASTER_PARALLEL_WORKFLOW_ARCHITECTURE.md` (expected SHA-256 `58b812adc77c16a7c4368bc7403857152f67b0e4bde5dba84be79f297b1c700f`) and `NVDA Parallel Workflow — Project-Specific Architecture and Rollout….md` (expected SHA-256 `e6290bd0a10afe5a1f0e0029464603ae4af11bc850bec3462367a6753ce61f16`). If either exact attachment is unavailable or mismatched, return `HARD_BLOCK` rather than substituting summaries.

### Mandatory test-subtree route

Before reading or running any file under `tests/`, obey `tests/AGENTS.override.md` in this order:

1. `AGENTS.md`;
2. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
3. `docs/01_NORMATIVE_CORE.md` and relevant working companions;
4. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`, `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` and `docs/vocabulary/vocabulary_registry.md`;
5. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`;
6. `config/retained_test_registry.yaml`;
7. `config/proof_blocks.yaml`;
8. `tests/AGENTS.override.md`;
9. only then the two vocabulary test files and their runtime surfaces.

All listed test-governance surfaces are read-only.

Before substantive review create:

`project_control/canonical_project_manager/parallel_workflow_validation/independent_control_test_v1/FULL_READ_MANIFEST.tsv`

## Tester write set

The tester may add only:

- `project_control/canonical_project_manager/parallel_workflow_validation/PARALLEL_CONTROL_INDEPENDENT_TESTER_REVIEW_V1.md`;
- `project_control/canonical_project_manager/parallel_workflow_validation/independent_control_test_v1/**`.

Everything else is read-only. Any repair or unrelated mutation is `HARD_BLOCK`.

## Independent checks

1. Reproduce all structural checks without relying solely on the PM validator.
2. Verify the seven vocabulary admissions against the human registry and generated projection; run builder parity and compare the complete vocabulary-test result with the exact superseded control baseline. Two known red node IDs may remain only when independently reproduced at `9e404df7…`; any new failure is `FAIL_REPAIRABLE`.
3. Verify every lane has a unique local full-read manifest inside its write set and no brief requires the global historical manifest or global workflow registry.
4. Verify Lane 1AW and 1AT route `tests/AGENTS.override.md` and its mandatory test-work authority sequence before physical-test inspection.
5. Verify exact worker and tester artefact names, revision `R1`, required portability members, bundle verification and reconstruction requirements.
6. Verify registry fields cover source revision, worker/tester commits, verdict, approved artefact/SHA, PM disposition, queue position, integration commit and aggregate validation.
7. Verify Lanes 5 and 6 are held and all four lane write sets are pairwise disjoint.
8. Verify the controls consistently state that worker launch is blocked pending this independent test and later PM acceptance.
9. Verify no production source, physical test, runtime configuration, dependency or migration changed.
10. Challenge at least one plausible stale-base failure and one portability reconstruction failure.

## Required validation

Run and retain exact output and exit status for:

- `python project_control/canonical_project_manager/parallel_workflow_validation/validate_parallel_cycle_01.py`;
- `PYTHONPATH=src python scripts/build_canonical_vocabulary.py` followed by an idempotence and clean-diff check for the generated projection;
- the complete two-file vocabulary test command `PYTHONPATH=src pytest -q tests/tier_a/vocabulary/test_vocabulary_canonical_builder_parity.py tests/tier_a/vocabulary/test_vocabulary_required_baseline_terms.py` on both the repair checkpoint and exact superseded control commit `9e404df7c13f7cca170e05e4c9f76b8ec4548ffa`; the repair must introduce no new failing node ID;
- the three scoped builder/governance tests `test_canonical_vocabulary_matches_builder_output_via_both_import_paths`, `test_governed_source_hashes_cover_authoritative_vocabulary_surfaces` and `test_disallowed_phrase_guardrails_and_evidence_appendix`, which must pass;
- an independent deterministic check that all seven admitted parallel-control slugs exist in both the human registry and generated projection and map to the parallel-workflow architecture;
- `git diff --check`;
- changed-path validation against the control repair boundary;
- `git fsck --full --no-dangling`;
- fresh archive extraction and repository reconstruction.

## Verdict and output

Return exactly one: `PASS`, `FAIL_REPAIRABLE` or `HARD_BLOCK`. PASS means only `SUITABLE_FOR_PM_PARALLEL_CONTROL_ACCEPTANCE_REVIEW`.

Commit tester evidence without changing the repaired control commit. Return one full-history archive outside the repository:

- PASS: `NVDA_PARALLEL_CONTROL_TESTER_APPROVED_R2_FULL_HISTORY.tar.gz`;
- FAIL_REPAIRABLE: `NVDA_PARALLEL_CONTROL_TESTER_FAIL_REPAIRABLE_R2_FULL_HISTORY.tar.gz`;
- HARD_BLOCK: `NVDA_PARALLEL_CONTROL_TESTER_HARD_BLOCK_R2_FULL_HISTORY.tar.gz`.

Verify the returned archive by SHA-256 and fresh extraction. Never launch or simulate a lane assignment.
