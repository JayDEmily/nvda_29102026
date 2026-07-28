# Lane 2AW — Worker Brief

## Assignment identity

- Worker thread: `Lane 2AW`
- Matching tester thread: `Lane 2AT`
- Assignment: `2A`
- Unit: `M04-PROOF-MLC-A-V1`
- Owner module: M04 `packet_protocol`
- Contract boundary: K07 `DmpV3Packet`
- Worker branch: `work/lane-2a-m04-mlc-a-v1`
- Tester branch: `test/lane-2a-m04-mlc-a-v1`

## Source checkpoint

Use the single full-history canonical archive supplied in the PM launch message as the sole repository input. Before acting, verify the exact archive filename and SHA-256, expected branch and commit, clean worktree and complete `.git` history stated in that message.

Do not proceed if any launch identifier is absent or mismatched. Create the named worker branch from the exact PM-designated source commit.

## Role and one question

Act only as the `M04-PROOF-MLC-A-V1` worker.

> Is current numbered authority sufficient to govern the bounded M04 `packet_protocol` contract—one DMPV3 outer envelope, caller/owner-supplied role-specific identity and lineage, deliberate carriage, validation and deterministic domain reproduction—without fabricating source, time, domain or execution truth?

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
11. `project_control/canonical_project_manager/MASTER_WORKFLOW_REGISTRY.md`
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

Read all directly cited proposition and evidence rows in full. Search, joins and scripts may assist inventory and mechanical checking; they may not decide authority or semantic sufficiency.

## Runtime prerequisites

M04 has no runtime prerequisite. M13 is accepted. This brief opens only M04 authority sufficiency; implementation, test routing, test observation and test mutation remain closed.

## Material read set

Numbered DMPV3/domain/architecture/ownership authority; N-03/N-05/N-09; M04/K07 architecture; C-010/C-016 and D-010/D-016 traceability.

If the PM-designated canonical state changes any material read-set item before integration, the assignment requires revalidation.

## Exact writable paths

- `project_control/canonical_project_manager/modules/M04/M04_AUTHORITY_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M04/raw_validation/mlc_a_v1/**`

Create no other tracked path. If another path is required, stop before mutation and return `RETURN_SCOPE_REOPEN_REQUIRED`.

## Global and cross-lane locks

Do not modify:

- `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER*.md`, numbered docs or vocabulary authority;
- the ExecPlan, Gate C protocol, parallel architecture or workflow registry;
- accepted architecture report/workbook/JSON/graphs;
- source, physical tests, fixtures, configuration, proof blocks, retained-test registry, packaging or lockfiles;
- another module's control/evidence directory;
- any worker or tester brief.

Do not consume another lane's unintegrated work or coordinate semantic decisions with another lane.

## Required work and output

Create the MLC-A record with exact propositions and locators; accepted owner/surface/contract; input → validation/carriage → output; identity, lineage, time, state and side effects; prohibited authority; mapped C/D/N/Atlas evidence; contradictions and missing meaning.

Return exactly `AUTHORITY_SUFFICIENT` or `BLOCKED_MISSING_NORMATIVE_AUTHORITY:<exact question>`. Historical tests or code may expose gaps but may not supply missing normative meaning.

Do not route tests, observe tests, specify proof, mutate norms or implement packet code.

Label the worker result exactly:

`PROPOSED_M04_AUTHORITY_V1_AWAITING_LANE_2AT`

## Validation

1. Validate every authority proposition locator against the current file text.
2. Reconcile M04, K07, C-010/C-016 and D-010/D-016 mappings exactly.
3. Challenge pre-DMP versus DMP boundary, role-specific mandatory IDs, caller-owned execution context, emitted-at/domain equivalence and forbidden default fabrication.
4. Record every material contradiction or unresolved term distinctly.
5. Validate no source/test/config/normative/global-control mutation.

Also run and retain:

- `git status --short --branch` before and after;
- `git diff --check`;
- changed-path validation against the exact write set;
- `git fsck --full --no-dangling`;
- hash validation for every worker evidence file.

No behavioural test pass is required because Cycle 1 does not mutate source or physical tests. A worker may run read-only scoped commands only when they materially support the leaf and must record exact output and exit status.

## Git and return

Commit only the bounded worker record and lane-owned evidence. Create exactly one Git-preserving full-history archive outside the repository. Verify by fresh extraction: branch, commit, clean worktree, ancestry to the PM source commit, changed paths and evidence hashes.

Return one archive only, its SHA-256 and a concise result table. End with:

`READY_FOR_LANE_2AT`
