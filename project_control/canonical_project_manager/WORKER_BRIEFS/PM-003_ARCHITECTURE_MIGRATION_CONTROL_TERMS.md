# Worker Brief PM-003 — Architecture, Migration and Programme-Control Terms

## Dispatch state

`authorised_after_PM-002_pass`

## Exact outcome

Semantically adjudicate the architecture, migration and programme-control vocabulary family. Produce one governed decision per assigned concept and update only the human semantic authority needed to express accepted decisions. Do not regenerate machine vocabulary in this unit.

## Prerequisite

PM-002 must record `unit_result: pass`, and all PM-001/PM-002 changes must remain inside their allowed paths.

## Fixed concept set

Human headings:

`Component Skeleton`; `Module Allocation Appendix`; `Native Architecture Blueprint Core`; `Ownership Matrix`; `Persistence Architecture`; `Reservations`; `Provisional Allocations`; `Seam Contract`; `Seam Contracts`; `Sequential Native Architecture Surface`; `Sequential Native Architecture Surfaces`; `Bridge and Shell Policy`; `Shell Policy`; `Target Structure`; `Test Architecture`; `Traceability Appendix`.

Working-overlay admissions:

`donor evidence`; `behaviour block`; `intent unit`; `atomic intent unit`; `target owner`; `leaf`; `authority intake gate`; `execution read sequence`; `active bounded pack`; `active bounded pack surface`; `semantic acceptance`; `implementation truth`; `normative baseline`; `alpha implementation`; `modular monolith`; `composition root`.

No PM-004 through PM-009 concept may be decided here.

## Authority and tests

Normative architecture/process meaning precedes vocabulary wording. Existing registry text, generated entries, tests and code cannot override the architecture and process normatives. Tests are read-only context; test colour has no acceptance role in PM-003.

## Required full reads

Create the unit full-read manifest first, then read:

- root controls, active ExecPlan, worker table, and all prior unit outputs;
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`;
- `docs/01_NORMATIVE_CORE.md` and `docs/01.1_NORMATIVE_WORKING.md`;
- `docs/04_TECHNICAL_ARCHITECTURE_CORE.md` and `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`;
- `docs/05_GUARDRAILS_CORE.md` and `docs/05.1_GUARDRAILS_WORKING.md`;
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md` and `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`;
- `docs/08_TESTING_AND_PROMOTION_CORE.md` and `docs/08.1_TESTING_AND_PROMOTION_WORKING.md`;
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md` and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`;
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` and `docs/11.1_NATIVE_ARCHITECTURE_BLUEPRINT_WORKING.md`;
- all three files under `docs/vocabulary/`;
- `data/vocabulary/canonical_vocabulary.json` and `src/nvda_desk/vocabulary_builder.py` as read-only implementation evidence.

If a directly governing architecture or process file is routed by those documents, read it in full and add it to the manifest before deciding the affected concept.

## Decision method

For every fixed concept record:

- exact label and normalised slug;
- governing proposition and source locator;
- bounded definition and scope;
- semantic owner;
- relationships and distinctions from adjacent concepts;
- canonical label/slug;
- lawful aliases and disallowed/misleading phrases;
- lifecycle/status;
- semantic disposition: `retain`, `enrich`, `admit_new`, `alias`, `quarantine`, `retire`, or `reject`;
- candidate action, when applicable: `enrich_existing`, `add_new`, `alias_only`, or `quarantine`;
- downstream projection action deferred to PM-010;
- rationale and evidence.

Singular/plural pairs and shell/bridge labels require explicit alias-versus-distinct-concept decisions; string similarity is not a decision.

## Allowed changes

- `project_control/canonical_project_manager/units/PM-003/**`;
- assigned entries in `docs/vocabulary/vocabulary_registry.md`;
- only the architecture/migration/programme-control admission text in sections 10.7 and 10.8 of `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` when required to remove a contradiction or complete an accepted semantic record.

Do not edit any generated vocabulary, builder, test, configuration, Atlas, other numbered normative, runtime implementation, root control, roadmap or ExecPlan.

## Required outputs

1. `PM-003_FULL_READ_MANIFEST.tsv`
2. `ARCHITECTURE_MIGRATION_CONTROL_ADJUDICATION_REGISTER.tsv`
3. `PM-003_RECEIPT.md`
4. `VALIDATION_OUTPUT.txt`

## Novel findings

A newly discovered durable concept within this exact family may be adjudicated after being logged as `novel_in_family`. A concept belonging to another family must be logged with its destination unit and left unchanged. A conflict with architecture/process normative authority blocks only the affected concept if the remaining decisions can be completed honestly; PM-003 itself is blocked if any assigned concept remains undecided.

## Validation and pass

Prove every fixed concept appears exactly once in the adjudication register, every accepted human entry is internally complete, no unassigned registry heading changed, generated JSON/builder/tests are unchanged, and all changed paths are allowed. Record `git diff --check` and a scoped before/after registry comparison.

PM-003 passes only with a complete decision for every assigned concept. On pass, continue to PM-004.
