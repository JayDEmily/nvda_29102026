# Module 7 — DMPV3 packet carriage implementation brief (v1)

## Purpose

Advance **Module 7 — DMPV3 packet carriage** only.

This tranche is for the **canonical DMPV3 outer-envelope contracts, typed helper surfaces, lawful packet builders, compatibility wrappers, proof, and receipts**.

It is **not** a serial-spine redesign tranche.
It is **not** a parallel-risk behaviour tranche.
It is **not** a downstream/review business-logic tranche.

## Why this brief is tighter than the earlier ones

This brief is written to avoid follow-up supplementary briefs.

The executor must therefore satisfy **all** of these before stopping:

1. mandatory authority read order completed
2. mandatory vocabulary-admission gate completed
3. mandatory invariant/test-family gate completed
4. branch-local report complete
5. live workbook receipts complete
6. every leaf closure recorded with its exact closing commit hash in **both** the report and the live workbook
7. no blank receipt fields left behind for this tranche

If any one of those is not complete, do **not** claim the tranche complete.

## Mandatory execution stance

1. Work on a new work branch only.
2. Do all work on that branch.
3. Do **not** merge to `main`.
4. When finished, zip the full repo including `.git`.
5. Stop and await further instructions from the user.

## Baseline and branching rule

1. Repo root: `work_api_dto`
2. Complete the outstanding Module 4 supplementary brief first.
3. Confirm the corrected Module 4 branch remains unmerged.
4. Record the exact corrected Module 4 HEAD commit hash.
5. Create this new branch **from that corrected Module 4 HEAD**, not from `main`.

### Required branch name

`work/module-7-dmpv3-packet-carriage-truth-pass-20260421`

### Stop condition before coding

If the uploaded repo does not contain the corrected Module 4 branch state, stop and say so.

## Mandatory read order before changing anything

Read these fully, in order, before coding:

1. `AGENTS.md`
2. `migration_prebuild/00_hierarchical_order.md`
3. `migration_prebuild/01_nvda_best_practice_blueprint_v3_final.xlsx`
4. `migration_prebuild/02_vocabulary_dictionary_system_audit.md`
5. `migration_prebuild/03_nvda_test_ordering_review_2026-04-18.md`
6. `migration_prebuild/04_rebuild_execution_order.md`
7. `migration_prebuild/05_nvda_final_recommendations_report_2026-04-18.md`
8. `migration_prebuild/06_tier_family_normalisation.md`
9. `migration_prebuild/07_wave1_truth_pass_and_completeness_2026-04-19.md`
10. `migration_prebuild/08_repository_runtime_hardening_2026-04-19.md`
11. `migration_prebuild/09_upstream_serial_domain_hardening_2026-04-19.md`
12. `migration_prebuild/10_adapter_registry_hardening_2026-04-19.md`
13. `migration_prebuild/11_completeness_matrix_all_workbook_paths_present_2026-04-19.md`
14. `migration_prebuild/12_future_brief_and_carry_forward_law_2026-04-19.md`
15. `migration_prebuild/13_tranche_leaf_commit_promotion_law_2026-04-20.md`
16. `docs/01_NORMATIVE_CORE.md`
17. `docs/03_DOMAIN_MODEL_CORE.md`
18. `docs/04_TECHNICAL_ARCHITECTURE_CORE.md`
19. `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md`
20. `docs/08_TESTING_AND_PROMOTION_CORE.md`
21. `docs/09_DMPV3_PROTOCOL_CORE.md`
22. `docs/09.1_DMPV3_PROTOCOL_WORKING.md`  
   Read this as a working/support surface only. It does **not** outrank `docs/09_DMPV3_PROTOCOL_CORE.md`.
23. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
24. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
25. `data/vocabulary/canonical_vocabulary.json`
26. `src/nvda_desk/schemas/vocabulary.py`
27. `tests/AGENTS.override.md`
28. `var/audit/nvda_running_audit_log.xlsx`

Do not skip the workbook.
Do not skip `docs/09_DMPV3_PROTOCOL_CORE.md`.
Do not skip the vocabulary surfaces.
Do not skip the running audit workbook.

## Explicit DMPV3 normative note

The repo **does** contain a standalone DMPV3 protocol document.

That document is:

`docs/09_DMPV3_PROTOCOL_CORE.md`

It explicitly defines:

1. the canonical DMPV3 outer envelope
2. mandatory carriage fields
3. producer identity law
4. packet role law
5. lineage law
6. validation law
7. summary law
8. extension law
9. canonical builder law
10. emitter coverage law

This tranche must treat that document as a mandatory governing source.

## Module 7 benchmark owner map

Use the workbook plus the DMPV3 core doc together.

### Workbook anchors

1. `Component_Skeleton` row for `packets/dmp_packets.py`
   1. target responsibility: `Packet carriage`
   2. class family: `DmpPacketBuilder`
   3. function families: `build_stage_packet`, `build_reference_packet`, `build_parallel_risk_packet`
   4. model families: `DmpV3Envelope`, `DmpV3Packet`
   5. preferred form: `functions + schema classes`
   6. note: `Cross-cutting carriage`

2. `Module_Allocation_Appendix` row `MA-016`
   1. target area: `contracts/packets.py`
   2. responsibility: `DMPV3 outer-envelope contracts and packet builders for lawful inter-module carriage`
   3. inputs: `module payloads`
   4. outputs: `DeskModulePacketV3 / DmpV3Envelope`
   5. forbidden content: `business meaning, stage ownership`
   6. legacy references: `schemas/dmp.py`, `schemas/dmp_envelope.py`

3. `Seam_Contracts` row for `Serial runtime -> packet carriage`
   1. seam contract: `packet/envelope`
   2. invariants:
      1. `Trace ID`
      2. `run ID`
      3. `stage dependencies`
      4. `packet role`
      5. `validation status`
   3. anti-pattern: `Packet role drift between modules`
   4. named carriers: `DmpV3Packet / DmpV3Envelope`

4. `Test_Architecture` row for `Packet carriage`
   1. proof family: `packet construction tests`
   2. focus: `DMP envelope, packet role, lineage fields`
   3. failure class: `Packet IDs/roles/lineage invalid or unstable`

### DMPV3 core-doc anchors

From `docs/09_DMPV3_PROTOCOL_CORE.md`, the executor must implement and prove:

1. one canonical DMPV3 outer envelope for live inter-module packet carriage
2. mandatory outer-envelope fields
3. truthful producer identity
4. explicit packet role and behaviour-class interpretation
5. bounded lineage
6. validation carriage
7. human-facing summary carriage
8. bounded `dmpextensions`
9. canonical builders through the repo-owned DMP surfaces
10. no bespoke alternative outer packet grammar

## Scope of this tranche

### In scope

1. lawful DMPV3 contract and schema surfaces
2. lawful canonical builder surfaces
3. compatibility-safe wrapper alignment where needed
4. packet-construction tests and any directly affected fixture updates
5. truthful receipt and audit updates

### Out of scope

1. redesign of Module 6 serial runtime behaviour
2. redesign of Module 8 parallel-risk behaviour
3. redesign of Module 10 capital-deployment behaviour
4. redesign of Module 11 downstream behaviour
5. broad consumer rewrites unrelated to lawful DMP carriage
6. API/public DTO redesign

### Limited seam glue allowed

Minimal call-site changes are allowed only where required to keep lawful DMPV3 carriage coherent and the repo green.

Do not expand the tranche beyond that.

## Known reconciliation problem this tranche must resolve

There is a live surface mismatch that must be handled truthfully.

1. `docs/09_DMPV3_PROTOCOL_CORE.md` names the canonical live surfaces as:
   1. `src/nvda_desk/schemas/dmp_envelope.py`
   2. `src/nvda_desk/schemas/dmp.py`
2. the current native repo instead has the thin live surfaces in:
   1. `src/nvda_desk/contracts/packets.py`
   2. `src/nvda_desk/packets/dmp_packets.py`

This tranche must resolve that mismatch lawfully.

That means:

1. establish one truthful canonical live ownership path
2. preserve compatibility only where needed and label it explicitly
3. do **not** leave the repo in a state where docs, contracts, and builders point at different competing truths

## Vocabulary-admission gate — mandatory before code changes

This gate is mandatory and comes **before** changing code, contracts, docs, tests, manifests, receipts, or fixtures.

1. Build the candidate term list for this tranche from:
   1. workbook-owned DMP terms
   2. `docs/09_DMPV3_PROTOCOL_CORE.md`
   3. contract/model names
   4. builder names
   5. fixture names
   6. test names
   7. any new helper/class/function names proposed in implementation
2. Reconcile each candidate term against:
   1. `data/vocabulary/canonical_vocabulary.json`
   2. `src/nvda_desk/schemas/vocabulary.py`
   3. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
   4. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
3. For each term, classify it exactly one way:
   1. already admitted canonical term
   2. lawful alias of an admitted term
   3. new term requiring admission in this same bounded gate
   4. blocked/quarantined term that must not enter live repo surfaces
4. Do **not** use a term in live code or tests merely because it appears in the workbook or `docs/09`.
5. If a term is missing but required for this tranche, admit it lawfully in the same bounded gate **before** using it elsewhere.
6. If lawful admission is not possible within this tranche boundary, stop and record the missing term as a blocker.

### Terms that must be checked explicitly

At minimum, classify these explicitly:

1. `DmpV3Envelope`
2. `DmpV3Packet`
3. `DeskModulePacketV3`
4. `packetrole`
5. `producer`
6. `lineage`
7. `validation`
8. `summary`
9. `dmpextensions`
10. `module_id`
11. `module_version`
12. `module_instance_id`
13. `grammar_role`
14. `behaviour_class`
15. `traceid`
16. `runid`
17. `scenarioid`

## Test-family and invariant gate — mandatory before implementation

This gate is mandatory and comes **after** the vocabulary gate and **before** code changes.

1. Identify the real invariants for Module 7:
   1. lawful canonical outer-envelope shape
   2. required DMP carriage fields present
   3. packet role explicit and stable
   4. producer identity truthful
   5. lineage explicit where dependencies exist
   6. validation carriage present
   7. summary carriage present
   8. extension carriage bounded
   9. packet builders deterministic and stable
   10. no bespoke outer packet grammar remains for live packetised outputs touched by this tranche
2. Identify the governing test families already covering this area.
3. Decide truthfully for each affected or missing proof surface whether the right action is:
   1. preserve
   2. re-author
   3. add
   4. defer with explicit reason
   5. archive/block with explicit reason
4. Do **not** pre-decide “no new tests needed” before this invariant check is complete.
5. Record the test-family decision in the branch-local report.

## Required implementation approach

Use a five-leaf plan and keep each leaf bounded.

### Leaf 1 — authority and vocabulary reconciliation

1. complete the mandatory read order
2. perform the vocabulary-admission gate
3. reconcile the canonical-surface conflict between `docs/09` and current native paths
4. decide the truthful target ownership layout for this tranche
5. record that decision in the branch-local report before coding further

### Leaf 2 — canonical contracts and schema surfaces

1. implement or reconcile the canonical DMPV3 envelope contract surfaces
2. ensure the lawful outer-envelope fields are represented truthfully
3. ensure producer, lineage, validation, summary, and extensions are represented truthfully
4. keep business meaning out of the packet-carriage module

### Leaf 3 — canonical builders and compatibility wrappers

1. implement or reconcile the canonical builder path
2. ensure builder outputs emit the lawful canonical shell
3. keep compatibility wrappers only where needed
4. label compatibility wrappers truthfully and avoid double-truth ownership

### Leaf 4 — proof surfaces and fixtures

1. re-author or add packet-construction tests needed by the invariant gate
2. update or add bounded fixtures if required
3. keep proof focused on packet carriage, not broader runtime redesign

### Leaf 5 — proof, receipts, and branch closeout state

1. rerun targeted proof first
2. rerun full shell proof second
3. update the branch-local report completely
4. update the live running audit workbook completely
5. self-audit receipts so no supplementary brief is needed

## Targeted proof requirements

Run targeted proof that directly covers Module 7 before the shell-wide proof.

At minimum, evaluate and truthfully update the relevant proof under these areas if affected:

1. `tests/tier_a/packets/`
2. `tests/tier_a/parallel_risk/test_parallel_risk_packet_builder_surface.py`
3. any DMP-related Tier B lineage tests touched by the carriage changes

If the invariant gate shows additional lawful proof is required, add or re-author it inside this tranche.

## Shell-wide proof requirements

After targeted proof passes, run:

1. `PYTHONPATH=src pytest -q tests/tier_a tests/tier_b`
2. `python -m compileall src`

Record the exact commands and exact outcomes in the branch-local report.

## Receipt surfaces — mandatory and complete

### Branch-local report path

Create or update:

`var/audit/2026-04-21_module_7_dmpv3_packet_carriage_truth_pass_report.md`

The report must contain:

1. repo baseline branch and exact base commit hash
2. new branch name
3. exact final HEAD commit hash
4. explicit leaf table for **L1–L5**
5. exact closing commit hash for **each** leaf
6. exact changed paths
7. vocabulary decision summary
8. invariant/test-family decision summary
9. exact proof commands run
10. exact proof results
11. blocker status: `none` or explicit blockers

### Live workbook updates

Update the existing live workbook only:

`var/audit/nvda_running_audit_log.xlsx`

Do **not** create a new workbook.

The workbook must record this tranche with:

1. module/tranche identity
2. branch name
3. base commit
4. final HEAD commit
5. leaf rows **L1–L5**
6. exact closing commit hash for **each** leaf row
7. proof status
8. report path

### Receipt self-audit — mandatory before zipping

Before zipping the repo, perform this exact self-audit:

1. verify the report contains **all five** leaf IDs
2. verify the report contains **all five** closing commit hashes
3. verify the workbook contains **all five** leaf rows
4. verify the workbook contains **all five** closing commit hashes
5. verify no receipt field for this tranche is left blank where the brief required a value
6. verify report and workbook hashes agree exactly

If any one of those checks fails, fix receipts before stopping.

## Stop boundary

Stop after:

1. the Module 7 tranche is complete on the work branch
2. targeted proof and shell-wide proof have been run and recorded
3. the report and workbook are both complete
4. the repo is zipped including `.git`

Do **not** merge to `main`.
Do **not** start Module 8 or any later tranche.
Do **not** continue into broad consumer rewrites.

## Deliverables back to the user

Return:

1. the updated repo as a full zip including `.git`
2. a concise execution summary stating:
   1. branch name
   2. base commit
   3. final HEAD commit
   4. whether the tranche is complete on-branch
   5. exact proof results
   6. whether any blocker remains

Then stop and await further instructions.
