# Lane 4AT — Independent Tester Brief

## Assignment identity

- Tester thread: `Lane 4AT`
- Worker thread: `Lane 4AW`
- Assignment: `4A`
- Unit: `M08-PROOF-MLC-A-V1`
- Owner module: M08 `playbook_catalogue`
- Contract boundary: K13 `PlaybookCatalogue`
- Expected worker branch: `work/lane-4a-m08-mlc-a-v1`
- Tester branch: `test/lane-4a-m08-mlc-a-v1`

## Inputs

Use only:

1. the exact PM canonical archive and launch identifiers supplied for Cycle 1; and
2. the exact worker candidate archive returned by `Lane 4AW`.

Verify both archive hashes, complete `.git` history, worker ancestry to the PM source commit, expected worker branch/commit and clean worker worktree. Reconstruct the exact candidate, then create the named tester branch from the exact worker candidate commit before adding tester-owned evidence.

## Role and one question

Act only as the independent tester for `M08-PROOF-MLC-A-V1`.

> Does the proposed M08 disposition truthfully establish or block the catalogue and eligibility boundary, preserve provisional architecture truth and exclude capital/execution/lifecycle authority?

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
12. `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`
13. `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md` and `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md`
14. `docs/03_DOMAIN_MODEL_CORE.md` and `docs/03.1_DOMAIN_MODEL_WORKING.md`
15. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
16. `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`
17. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`
18. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
19. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
20. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
21. C-033/C-034 rows in `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv`, `project_control/normative_authority_top_down_alignment/EXISTING_TEST_DISPOSITION.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C2_PROOF_ENVELOPE_REGISTER.tsv` and `project_control/normative_authority_top_down_alignment/GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv`; plus `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-033.md`, `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-034.md` and their linked test designs
22. accepted M08/K13 rows in `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md`, `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` and `project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json`
23. current numbered propositions concerning playbook definition, catalogue identity/version, substitution, eligibility, stand-down, candidate-family origin and prohibited capital/broker authority
24. directly relevant historical 5.10 playbook records only after current authority
25. the complete Lane 4AW authority record and raw evidence

Read the worker's complete changed files and evidence in full. Do not accept a worker conclusion from summaries, hashes, counts or green commands alone.

## Scope and locks

The worker is permitted to change only:

- `project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M08/raw_validation/mlc_a_v1/**`

The tester may add only:

- `project_control/canonical_project_manager/modules/M08/M08_AUTHORITY_TESTER_REVIEW_V1.md`
- `project_control/canonical_project_manager/modules/M08/raw_validation/tester_mlc_a_v1/**`

All source, physical tests, configuration, numbered docs, global controls, architecture artefacts, proof/vocabulary registries and other lane paths remain read-only. Any out-of-scope worker mutation is an automatic `HARD_BLOCK` unless the PM reopens scope.

## Independent checks

1. Independently verify every cited proposition and locator.
2. Falsify sufficiency against catalogue identity/version, substitution, candidate-family origin, eligibility, deterministic selection and stand-down.
3. Challenge leakage into M07 coefficient authority, M09 capital, M10 execution and M11 lifecycle.
4. Confirm provisional surface status was not upgraded and code/registry/test evidence was not reverse-promoted.
5. Confirm exact write-set compliance.

The tester must perform at least one independent challenge not copied from the worker's validation approach.

## Verdict

Return exactly one:

- `PASS`
- `FAIL_REPAIRABLE`
- `HARD_BLOCK`

`PASS` means only `SUITABLE_FOR_PM_M08_MLC_A_INTEGRATION_REVIEW`. It is not canonical acceptance and does not open the next leaf.

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

`SUITABLE_FOR_PM_M08_MLC_A_INTEGRATION_REVIEW`
