# Worker Brief PM-002 — Vocabulary Normative Truth Repair

## Dispatch state

`authorised_after_PM-001_pass`

## Exact outcome

Repair only the stale or contradictory current-state statements exposed by the fresh PM-001 census. Establish an unambiguous doctrine-to-projection direction before any term-family adjudication begins.

This unit may correct facts such as stale inventory counts, stale audit-result descriptions, ambiguous wording about the source of semantic meaning, and workflow text that could be read as allowing a builder, scanner, JSON file, stamp or green test to admit meaning.

This unit does not decide, add, remove, alias, enrich, quarantine or retire any durable term.

## Prerequisite

PM-001 must have all required outputs and `VOCABULARY_CURRENT_TRUTH_RECEIPT.md` must record `unit_result: pass`. If the receipt is missing, blocked, or its changed paths exceed the PM-001 directory, do not begin.

## Authority and test meaning

Apply `AGENTS.md`, `PLANS.md`, the active ExecPlan, the PM-001–PM-010 worker table, and the numbered normative stack in that order. For semantic artefacts, human-readable accepted vocabulary meaning precedes builder code, generated JSON, audit artefacts and tests.

Existing tests are read-only evidence. Passing or failing tests cannot validate a normative statement and are not a PM-002 pass condition.

## Required full reads

Create `project_control/canonical_project_manager/units/PM-002/PM-002_FULL_READ_MANIFEST.tsv` first. Then read in full:

1. `AGENTS.md`
2. `PLANS.md`
3. `ROADMAP_LEDGER_V2.md`
4. `project_control/canonical_project_manager/EXEC_PLAN.md`
5. `project_control/canonical_project_manager/PM-001_TO_PM-010_WORKER_TABLE.md`
6. every PM-001 output
7. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
8. `docs/01_NORMATIVE_CORE.md`
9. `docs/01.1_NORMATIVE_WORKING.md`
10. `docs/05_GUARDRAILS_CORE.md`
11. `docs/05.1_GUARDRAILS_WORKING.md`
12. `docs/08_TESTING_AND_PROMOTION_CORE.md`
13. `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`
14. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
15. `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
16. `docs/vocabulary/README.md`
17. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
18. `docs/vocabulary/vocabulary_registry.md`
19. `src/nvda_desk/schemas/vocabulary.py`
20. `src/nvda_desk/vocabulary_builder.py`
21. `src/nvda_desk/vocabulary_synonym_audit.py`
22. `data/vocabulary/canonical_vocabulary.json`
23. `data/vocabulary/vocabulary_touch_stamp.json`
24. `var/vocabulary/synonym_candidates.json` if present

## Required work

1. Convert every PM-001 discrepancy that alleges stale or contradictory normative/workflow text into one row of `VOCABULARY_NORMATIVE_TRUTH_REPAIR_REGISTER.tsv`.
2. For each row record the exact old proposition, current repository evidence, governing higher proposition, required correction, changed path/section, and whether the change affects meaning or only current-state truth.
3. Correct only rows classified `current_state_truth_repair` or `authority_direction_clarification`.
4. Preserve all explicit term admissions, definitions and dispositions byte-for-byte except unavoidable line movement caused by the bounded edit.
5. State explicitly that generated artefacts, scanners, stamps and tests are evidence/projection surfaces and cannot create semantic admission.
6. State the PM-001-observed counts rather than carrying forward the stale 42-heading claim. If PM-001 differs from the expected 46/87/26/20/61 counts, use the independently reproduced PM-001 values and explain the difference.
7. Reproduce the current synonym audit read-only. Describe exactly what its configured algorithm returns; do not represent it as semantic completeness and do not edit the generated report or stamp.

## Allowed changes

- new files under `project_control/canonical_project_manager/units/PM-002/`;
- bounded truth/authority-direction corrections in:
  - `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
  - `docs/vocabulary/README.md`;
  - `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`.

## Forbidden changes

Do not change the vocabulary registry, any explicit term admission or definition, tests, proof registries, builder/schema/scripts, generated JSON, audit report, touch stamp, Atlas evidence, runtime code, root controls, roadmaps or ExecPlans.

## Required outputs

1. `PM-002_FULL_READ_MANIFEST.tsv`
2. `VOCABULARY_NORMATIVE_TRUTH_REPAIR_REGISTER.tsv`
3. `PM-002_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

## Validation and pass

Record before/after SHA-256 for every allowed governed file. Prove that:

- every changed sentence maps to a PM-001 discrepancy;
- human registry and generated JSON hashes are unchanged;
- the set of explicit admissions in sections 10.7 and 10.8 is unchanged;
- no test, source, configuration, Atlas or generated file changed;
- the corrected counts reproduce from current bytes;
- `git diff --check` passes;
- every changed path is allowed.

PM-002 passes only when the artefact hierarchy and current-state descriptions are accurate without making a term decision. Record `unit_result: pass` and proceed to PM-003. If a correction would change semantic meaning or contradict higher normative authority, record `unit_result: blocked` and stop the sequence.
