# Worker Brief PM-010 — P1 Integration and Deterministic Projection Freeze

## Dispatch state

`authorised_after_PM-009_pass`

## Exact outcome

Integrate the accepted semantic decisions from PM-003 through PM-009 into one coherent human-readable vocabulary authority, then rebuild the machine projection deterministically from that accepted authority. Refresh audit and touch evidence only after the semantic source and projection agree.

PM-010 does not create new semantic families, reconcile test authority, modify production/trading behaviour, or open Gate D.

## Prerequisite

PM-001 through PM-009 must each contain all required outputs and record `unit_result: pass`. Every assigned concept in PM-003 through PM-009 must have one complete semantic disposition. If a concept remains undecided, duplicated across units, or contradicts another accepted decision, do not project around it; resolve it under the owning prior unit's semantic authority and log the repair, or record PM-010 blocked.

## Authority and test meaning

The required direction is:

`accepted normative meaning → human vocabulary registry/admission record → deterministic builder → generated JSON/audit evidence`.

Schemas, builders, generated JSON, scanners, stamps and tests may validate structure or projection consistency. They cannot decide meaning, novelty, ownership, alias law or admission.

Existing tests remain un-reconciled P2 evidence. They may be run read-only after integration, but green tests are not a PM-010 pass condition and failing tests must not be weakened, edited or used to roll back an accepted semantic decision. Record all test fallout for P2.

## Required full reads

Create `project_control/canonical_project_manager/units/PM-010/PM-010_FULL_READ_MANIFEST.tsv` first. Read in full:

1. root `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, and `ROADMAP_LEDGER_V2.md`;
2. active ExecPlan, PM-001–PM-010 worker table and companion note;
3. every output from PM-001 through PM-009;
4. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
5. `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
6. both guardrail documents;
7. both testing/promotion documents;
8. both vocabulary normatives;
9. `docs/vocabulary/README.md`, `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`, and `docs/vocabulary/vocabulary_registry.md`;
10. vocabulary portions of `config/retained_test_registry.yaml` and `config/proof_blocks.yaml` read-only;
11. `tests/AGENTS.override.md` and every `tests/tier_a/vocabulary/test_*.py` file read-only;
12. `src/nvda_desk/schemas/vocabulary.py`;
13. `src/nvda_desk/vocabulary_builder.py`;
14. `src/nvda_desk/vocabulary_synonym_audit.py`;
15. `scripts/build_canonical_vocabulary.py`;
16. `scripts/vocabulary_synonym_audit.py`;
17. `scripts/vocabulary_candidate_review.py`;
18. `data/vocabulary/README.md`;
19. `data/vocabulary/canonical_vocabulary.json`;
20. `data/vocabulary/vocabulary_touch_stamp.json`;
21. `var/vocabulary/synonym_candidates.json` if present;
22. retained vocabulary adjudication appendix and ten-record Atlas vocabulary slice as read-only evidence.

Any additional file that the builder or audit imports directly must be read in full and added to the manifest before it is changed or relied upon.

## Integration work

1. Build `P1_INTEGRATED_SEMANTIC_REGISTER.tsv` from the accepted prior-unit registers. Prove that every fixed concept is represented once and that aliases do not create duplicate meanings.
2. Re-read the complete resulting `docs/vocabulary/vocabulary_registry.md` as one document. Repair only integration defects such as duplicate entries, inconsistent ownership metadata, broken cross-references, conflicting aliases or missing accepted records. Do not reopen settled meaning without recording the exact contradiction and owning unit.
3. Ensure every accepted durable concept has human-readable meaning, scope, owner, relationships, lifecycle/status, canonical label/slug, aliases, disallowed phrases and traceability to its semantic decision.
4. Ensure every quarantined, retired or rejected concept remains visible in the integrated decision evidence and is absent from the canonical generated concept set unless its accepted lifecycle explicitly requires a compatibility-only projection.
5. Establish one deterministic projection path whose input is the accepted human semantic authority. Remove any builder seed that would independently create or redefine a term. The builder may transform accepted records into machine structure; it may not supply missing semantics.
6. Generate proposed JSON into `/tmp` first. Validate it independently, then update `data/vocabulary/canonical_vocabulary.json` only through the controlled builder route. Do not hand-edit the JSON.
7. Produce `P1_PROJECTION_TRACEABILITY.tsv` with one row per generated entry mapping it to the exact human admission record and prior unit decision.
8. Run the synonym/candidate audit read-only against the integrated state. Every candidate must have a recorded semantic disposition. Correct audit implementation or configuration only when it misrepresents the accepted semantic records and the correction stays inside the allowed vocabulary surfaces.
9. Update the tracked audit report and touch stamp only through their declared generation route and only after the integrated registry, projection and candidate dispositions validate.
10. Run existing vocabulary tests read-only if the environment permits. Record each file's result and strongest honest claim in `P1_TEST_DIAGNOSTIC_REGISTER.tsv`. Route discrepancies to P2; do not edit tests.

## Allowed changes

- `project_control/canonical_project_manager/units/PM-010/**`;
- integration corrections in `docs/vocabulary/vocabulary_registry.md`;
- bounded consistency updates in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`, `docs/vocabulary/README.md`, and `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`;
- `src/nvda_desk/schemas/vocabulary.py`;
- `src/nvda_desk/vocabulary_builder.py`;
- `src/nvda_desk/vocabulary_synonym_audit.py`;
- `scripts/build_canonical_vocabulary.py`;
- `scripts/vocabulary_synonym_audit.py`;
- `scripts/vocabulary_candidate_review.py` only if required for the accepted projection/audit route;
- `data/vocabulary/canonical_vocabulary.json` through generation only;
- `data/vocabulary/vocabulary_touch_stamp.json` through its declared update route only;
- `var/vocabulary/synonym_candidates.json` through the audit generation route only.

## Forbidden changes

Do not change:

- any test or test fixture;
- `config/retained_test_registry.yaml` or `config/proof_blocks.yaml`;
- runtime/trading implementation outside the expressly listed vocabulary files;
- other numbered normatives, architecture controls or protocol/domain contracts;
- Atlas material;
- root controls, roadmap ledgers or ExecPlans;
- dependency files merely to obtain a green test run;
- any P2, P3, P4 or Gate D artefact.

## Required outputs

1. `PM-010_FULL_READ_MANIFEST.tsv`
2. `P1_INTEGRATED_SEMANTIC_REGISTER.tsv`
3. `P1_PROJECTION_TRACEABILITY.tsv`
4. `P1_TEST_DIAGNOSTIC_REGISTER.tsv`
5. `PM-010_RECEIPT.md`
6. `VALIDATION_OUTPUT.txt`

## Validation

Record and prove:

- every fixed PM-003–PM-009 concept is present exactly once in the integrated decision set;
- every generated entry maps to exactly one accepted human record;
- no accepted canonical concept is missing from the projection;
- no quarantined/rejected concept is silently canonicalised;
- canonical slugs and aliases have no forbidden exact collisions;
- builder output generated in `/tmp` equals committed JSON as parsed objects;
- a second clean build is byte-stable;
- audit output is reproducible and every candidate is dispositioned;
- touch stamp hashes the current declared sources and did not advance before proof;
- no test changed;
- no production/runtime file outside the allowed vocabulary surfaces changed;
- every changed path is allowed;
- `git diff --check` passes.

Pytest output, if available, must be labelled diagnostic. A test failure blocks a claim that the current test suite is green but does not by itself invalidate higher semantic authority. Record the exact failing proposition for P2.

## Pass, block and return

PM-010 passes only when the human semantic source, deterministic projection, generated JSON and current audit evidence agree and every prior semantic decision is traceable. If accepted meaning cannot be projected without crossing an unopened authority boundary, record `unit_result: blocked`; do not dilute the meaning or change tests.

On pass, record `unit_result: pass` and stop this ten-unit sequence. Return all files changed, all unit receipts, validation commands/results, diagnostic test results, novel findings, unresolved P2 matters and final Git status to the Project Manager. Do not update the roadmap, commit, package, start P2 or claim Gate D open.
