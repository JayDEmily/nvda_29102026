# Lane 3AW — Worker Brief

## Assignment identity

- Worker thread: `Lane 3AW`
- Matching tester thread: `Lane 3AT`
- Assignment: `3A`
- Unit: `M07-PROOF-MLC-A-V1`
- Owner module: M07 `coefficient_modifier_authority`
- Contract boundary: K12 `PolicyBundle` plus mandatory positive obligation `OBL-M07-POSITIVE`
- Worker branch: `work/lane-3a-m07-mlc-a-v1`
- Tester branch: `test/lane-3a-m07-mlc-a-v1`

## Source checkpoint

Use the single full-history canonical archive supplied in the PM launch message as the sole repository input. Before acting, verify the exact archive filename and SHA-256, expected branch and commit, clean worktree and complete `.git` history stated in that message.

Do not proceed if any launch identifier is absent or mismatched. Create the named worker branch from the exact PM-designated source commit.

## Role and one question

Act only as the `M07-PROOF-MLC-A-V1` worker.

> Is current numbered authority sufficient to define bounded M07 coefficient/modifier ownership, versioned bundles, precedence, hard bounds, deterministic application and application receipts without turning M07 into generic policy ownership?

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

Read all directly cited proposition and evidence rows in full. Search, joins and scripts may assist inventory and mechanical checking; they may not decide authority or semantic sufficiency.

## Runtime prerequisites

M07 has no runtime prerequisite. Its known positive implementation obligation is unresolved and may expose missing normative authority.

## Material read set

Current coefficient/modifier meaning across operating, domain, technical, guardrail, ownership and architecture docs; M07/K12; C-012/D-012; mandatory positive obligation.

If the PM-designated canonical state changes any material read-set item before integration, the assignment requires revalidation.

## Exact writable paths

- `project_control/canonical_project_manager/modules/M07/M07_AUTHORITY_WORKER_RECORD_V1.md`
- `project_control/canonical_project_manager/modules/M07/raw_validation/mlc_a_v1/**`

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

Create the MLC-A record with exact propositions/locators; M07/K12 owner boundary; input → precedence/bounded application → output/receipt; identity, version, lineage, state, time and side effects; prohibited authority; C/D/Atlas mappings; and the known positive-obligation gap.

Return exactly `AUTHORITY_SUFFICIENT` or `BLOCKED_MISSING_NORMATIVE_AUTHORITY:<exact question>`. A broad statement that coefficients exist is not sufficient; each required authority dimension must be separately resolved.

Do not repair missing authority, route or inspect tests, write proof specifications, change configuration or implement M07.

Label the worker result exactly:

`PROPOSED_M07_AUTHORITY_V1_AWAITING_LANE_3AT`

## Validation

1. Validate every cited locator.
2. Reconcile M07, K12, C-012, D-012 and the mandatory positive M07 obligation.
3. Independently challenge bundle identity/version, precedence conflict, hard-bound ownership, deterministic replay and receipt sufficiency.
4. Test the semantic boundary against calendar, playbook, capital, execution, lifecycle and replay policy ownership.
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

`READY_FOR_LANE_3AT`
