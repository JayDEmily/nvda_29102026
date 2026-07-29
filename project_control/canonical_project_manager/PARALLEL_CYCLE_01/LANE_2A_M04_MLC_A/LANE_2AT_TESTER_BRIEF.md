# Lane 2AT — Independent Tester Brief

## Assignment identity

- Tester thread: `Lane 2AT`
- Worker thread: `Lane 2AW`
- Assignment: `2A`
- Unit: `M04-PROOF-MLC-A-V1`
- Owner module: M04 `packet_protocol`
- Contract boundary: K07 `DmpV3Packet`
- Expected worker branch: `work/lane-2a-m04-mlc-a-v1`
- Revision: `R1`
- Tester branch: `test/lane-2a-m04-mlc-a-v1`

## Inputs

Use only:

1. the exact PM canonical archive and launch identifiers supplied for Cycle 1; and
2. the exact worker candidate archive returned by `Lane 2AW`.

Verify both archive hashes, complete `.git` history, worker ancestry to the PM source commit, expected worker branch/commit and clean worker worktree. Reconstruct the exact candidate, then create the named tester branch from the exact worker candidate commit before adding tester-owned evidence.

## Assignment-local full-read manifest

Before substantive review, independently create and maintain:

`project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/FULL_READ_MANIFEST.tsv`

Record every required file, reason, read status, mutation relevance and pre-review SHA-256 where available. Do not copy the worker manifest as proof of tester reading and do not modify the global historical `project_control/canonical_project_manager/FULL_READ_MANIFEST.tsv`.

## Role and one question

Act only as the independent tester for `M04-PROOF-MLC-A-V1`.

> Does the proposed M04 authority disposition follow current numbered meaning, preserve the packet-owner boundary and expose every material ambiguity instead of borrowing authority from tests or code?

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
13. packet-relevant sections of `docs/03_DOMAIN_MODEL_CORE.md` and `docs/03.1_DOMAIN_MODEL_WORKING.md`, with full files read
14. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
15. `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`
16. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`, `docs/07.1_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_WORKING.md` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md`
17. `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
18. `docs/09_DMPV3_PROTOCOL_CORE.md` and `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
19. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
20. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`
21. `project_control/normative_authority_top_down_alignment/normative_completion_decisions/N-03_PREPARED_DATA_COMMON_ENVELOPE.md`, `project_control/normative_authority_top_down_alignment/normative_completion_decisions/N-05_COMMON_METADATA_AND_STAGE_SPECIFIC_CARRIERS.md` and `project_control/normative_authority_top_down_alignment/normative_completion_decisions/N-09_AUTHORITATIVE_REPLAY.md`
22. C-010/C-016 rows in `project_control/normative_authority_top_down_alignment/GATE_C_TEST_REQUIREMENTS.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C_TEST_AUTHORITY_REGISTER.tsv`, `project_control/normative_authority_top_down_alignment/EXISTING_TEST_DISPOSITION.tsv`, `project_control/normative_authority_top_down_alignment/GATE_C2_PROOF_ENVELOPE_REGISTER.tsv` and `project_control/normative_authority_top_down_alignment/GATE_C2_BLOCKED_OR_RETURNED_UNITS.tsv`; plus `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-010.md`, `project_control/normative_authority_top_down_alignment/gate_c2_proof_envelopes/D-016.md` and their linked test designs
23. accepted M04/K07 rows in `project_control/canonical_project_manager/architecture/Atlas_Architecture_Decision_Report.md`, `project_control/canonical_project_manager/architecture/Atlas_Architecture_Traceability.xlsx` and `project_control/canonical_project_manager/architecture/Atlas_Architecture_Machine_Readable.json`
24. all directly referenced normative propositions in full
25. the complete Lane 2AW authority record and raw evidence

Read the worker's complete changed files and evidence in full. Do not accept a worker conclusion from summaries, hashes, counts or green commands alone.

## Scope and locks

The worker is permitted to change only:

- `project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/**`

The tester may add only:

- `project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_TESTER_REVIEW_V1.md`
- `project_control/canonical_project_manager/modules/M04/raw_validation/tester_mlc_a_v1/**`

All source, physical tests, configuration, numbered docs, global controls, architecture artefacts, proof/vocabulary registries and other lane paths remain read-only. Any out-of-scope worker mutation is an automatic `HARD_BLOCK` unless the PM reopens scope.

## Independent checks

1. Independently verify every cited proposition and locator.
2. Attempt to falsify sufficiency using missing role identity, fabricated execution context, source-artifact lineage, packet occurrence identity and emitted-at/domain-equivalence boundaries.
3. Confirm M04 is carriage/validation only and does not absorb M01 source admission or downstream domain decisions.
4. Confirm Atlas/test/code evidence was not reverse-promoted to normative authority.
5. Confirm exact write-set compliance.

The tester must perform at least one independent challenge not copied from the worker's validation approach.

## Verdict

Return exactly one:

- `PASS`
- `FAIL_REPAIRABLE`
- `HARD_BLOCK`

`PASS` means only `SUITABLE_FOR_PM_M04_MLC_A_INTEGRATION_REVIEW`. It is not canonical acceptance and does not open the next leaf.

For `FAIL_REPAIRABLE`, list bounded defects within the existing authority/write set. For `HARD_BLOCK`, identify the missing authority, invalid baseline, architecture conflict or required scope change.

## Tester record and exact portability artefact

Create the tester review record and raw evidence only in the tester-owned paths. Commit the tester evidence after the unchanged worker commit or ordered worker commit series. Never modify, squash or rewrite worker commits.

Return exactly one tar archive outside the repository, named by verdict:

- PASS: `NVDA_LANE_2A_M04_MLC_A_TESTER_APPROVED_R1.tar.gz`
- FAIL_REPAIRABLE: `NVDA_LANE_2A_M04_MLC_A_TESTER_FAIL_REPAIRABLE_R1.tar.gz`
- HARD_BLOCK: `NVDA_LANE_2A_M04_MLC_A_TESTER_HARD_BLOCK_R1.tar.gz`

The archive must contain exactly one portability package with:

- `MANIFEST.json` recording assignment `2A`, revision `R1`, PM source archive/SHA/branch/commit, worker branch/commit(s), tester branch/evidence commit, verdict, exact worker/tester write sets and package member hashes;
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

`SUITABLE_FOR_PM_M04_MLC_A_INTEGRATION_REVIEW`
