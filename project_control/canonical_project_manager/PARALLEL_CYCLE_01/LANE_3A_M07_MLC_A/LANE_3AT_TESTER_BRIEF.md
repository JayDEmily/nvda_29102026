# Lane 3AT — Independent Tester Brief

## Assignment identity

- Tester thread: `Lane 3AT`
- Worker thread: `Lane 3AW`
- Assignment: `3A`
- Unit: `M07-PROOF-MLC-A-V1`
- Owner module: M07 `coefficient_modifier_authority`
- Contract boundary: K12 `PolicyBundle` plus mandatory positive obligation `OBL-M07-POSITIVE`
- Expected worker branch: `work/lane-3a-m07-mlc-a-v1`
- Revision: `R1`
- Tester branch: `test/lane-3a-m07-mlc-a-v1`

## Inputs

Use only:

1. the exact PM canonical archive and launch identifiers supplied for Cycle 1; and
2. the exact worker candidate archive returned by `Lane 3AW`.

Verify both archive hashes, complete `.git` history, worker ancestry to the PM source commit, expected worker branch/commit and clean worker worktree. Reconstruct the exact candidate, then create the named tester branch from the exact worker candidate commit before adding tester-owned evidence.

## Assignment-local full-read manifest

Before substantive review, independently create and maintain:

`project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv`

Record every required file, reason, read status, mutation relevance and pre-review SHA-256 where available. Do not copy the worker manifest as proof of tester reading and do not modify the global historical `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`.

## Role and one question

Act only as the independent tester for `M07-PROOF-MLC-A-V1`.

> Does the proposed M07 disposition truthfully establish or block every required coefficient/modifier authority dimension without over-claiming generic policy ownership?

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
12. `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`
13. `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`, `docs/02.1_BRIEFING_AND_EXECUTION_OPERATING_MODEL_WORKING.md` and `docs/02.2_SIGNAL_INFORMED_INTRADAY_PHASE_WORKING.md`
14. `docs/03_DOMAIN_MODEL_CORE.md` and `docs/03.1_DOMAIN_MODEL_WORKING.md`
15. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`, `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md` and `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md`
16. `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`
17. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`
18. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
19. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
20. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
21. C-012 rows in `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv`, `project_control/normative_authority_top_down_alignment/EXISTING_TEST_DISPOSITION.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C2_PROOF_ENVELOPE_REGISTER.tsv` and `project_control/normative_authority_top_down_alignment/GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv`; plus `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-012.md` and its linked test design
22. accepted M07/K12 rows and the mandatory positive M07 obligation in `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md`, `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` and `project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json`
23. every current numbered proposition concerning coefficient/modifier ownership, version, precedence, bounds, application and receipt
24. directly relevant historical 5.9 control/evidence only after current authority
25. the complete Lane 3AW authority record and raw evidence

Read the worker's complete changed files and evidence in full. Do not accept a worker conclusion from summaries, hashes, counts or green commands alone.

## Scope and locks

The worker is permitted to change only:

- `project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/**`

The tester may add only:

- `project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_TESTER_REVIEW_V1.md`
- `project_control/canonical_project_manager/modules/M07/raw_validation/tester_mlc_a_v1/**`

All source, physical tests, configuration, numbered docs, global controls, architecture artefacts, proof/vocabulary registries and other lane paths remain read-only. Any out-of-scope worker mutation is an automatic `HARD_BLOCK` unless the PM reopens scope.

## Independent checks

1. Independently verify every cited proposition and locator.
2. Falsify any sufficiency claim against bundle identity/version, precedence, hard bounds, deterministic application, receipts and lawful absence.
3. Challenge leakage into domain-owned calendar, playbook, capital, execution, lifecycle or replay policy.
4. Confirm the known positive M07 obligation was resolved or blocked explicitly, not hidden by C-012.
5. Confirm no test/code/history was reverse-promoted and exact write-set compliance.

The tester must perform at least one independent challenge not copied from the worker's validation approach.

## Verdict

Return exactly one:

- `PASS`
- `FAIL_REPAIRABLE`
- `HARD_BLOCK`

`PASS` means only `SUITABLE_FOR_PM_M07_MLC_A_INTEGRATION_REVIEW`. It is not canonical acceptance and does not open the next leaf.

For `FAIL_REPAIRABLE`, list bounded defects within the existing authority/write set. For `HARD_BLOCK`, identify the missing authority, invalid baseline, architecture conflict or required scope change.

## Tester record and exact portability artefact

Create the tester review record and raw evidence only in the tester-owned paths. Commit the tester evidence after the unchanged worker commit or ordered worker commit series. Never modify, squash or rewrite worker commits.

Return exactly one tar archive outside the repository, named by verdict:

- PASS: `NVDA_LANE_3A_M07_MLC_A_TESTER_APPROVED_R1.tar.gz`
- FAIL_REPAIRABLE: `NVDA_LANE_3A_M07_MLC_A_TESTER_FAIL_REPAIRABLE_R1.tar.gz`
- HARD_BLOCK: `NVDA_LANE_3A_M07_MLC_A_TESTER_HARD_BLOCK_R1.tar.gz`

The archive must contain exactly one portability package with:

- `MANIFEST.json` recording assignment `3A`, revision `R1`, PM source archive/SHA/branch/commit, worker branch/commit(s), tester branch/evidence commit, verdict, exact worker/tester write sets and package member hashes;
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

`SUITABLE_FOR_PM_M07_MLC_A_INTEGRATION_REVIEW`
