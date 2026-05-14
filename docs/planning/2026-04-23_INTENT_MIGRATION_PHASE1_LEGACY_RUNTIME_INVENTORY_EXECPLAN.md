# Intent Migration Phase 1 — Legacy Runtime Inventory ExecPlan

## Purpose

This execution plan defines Phase 1 of the intent-migration programme.

Phase 1 establishes the runtime-only donor inventory that later intent-extraction work will depend on.

This phase does not rebuild behaviour.

This phase does not re-author tests.

This phase does not change native runtime contracts.

## Scope boundary

In scope for Phase 1:

- identify the legacy files that belong to the donor runtime surface
- classify each donor file by runtime role and dependency shape
- separate active runtime candidates from support-only or unclear surfaces
- seed the machine-readable inventory ledger that later phases will consume

Out of scope for Phase 1:

- intent extraction from donor behaviour blocks
- target-owner mapping for recovered intent units
- native implementation work in `src/`
- native test re-authoring in `tests/`
- runtime or packet-law changes
- additional routing-law changes after Leaf 0 closes

## Authority and evidence to read

Read these before executing Phase 1:

1. `AGENTS.md`
2. `intent_migration/AGENTS.override.md`
3. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
4. `docs/01_NORMATIVE_CORE.md`
5. `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`
6. `docs/05_GUARDRAILS_CORE.md`
7. `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
8. `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
9. `docs/08_TESTING_AND_PROMOTION_CORE.md`
10. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
11. `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
12. `PLANS.md`
13. `legacy_import/README.md` when donor runtime reading starts

No external planning-pack file is required to restart this Phase 1 work. The repo-local routed surfaces above are the required restart set.

## Touched surfaces

For the current Phase 1 execution state, touch only:

- `docs/planning/2026-04-23_INTENT_MIGRATION_PHASE1_LEGACY_RUNTIME_INVENTORY_EXECPLAN.md`
- `var/audit/ledgers/intent_migration/legacy_runtime_inventory.json`
- `var/audit/ledgers/intent_migration/legacy_file_synopsis.json` when Phase 1 seed state needs truthful reconciliation only
- `var/audit/ledgers/intent_migration/legacy_intent_ledger.json` when Phase 1 seed state needs truthful reconciliation only
- `var/audit/ledgers/intent_migration/intent_to_architecture_map.json` when Phase 1 seed state needs truthful reconciliation only
- `var/audit/ledgers/intent_migration/intent_migration_queue.json` when Phase 1 seed state needs truthful reconciliation only

## Read-only mandatory-reading surfaces

Read-only mandatory-reading surfaces for this phase include:

- `AGENTS.md`
- `intent_migration/AGENTS.override.md`
- `PLANS.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`
- `docs/05_GUARDRAILS_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `legacy_import/README.md`
- all donor files under `legacy_import/` once Phase 1 execution starts

## Prohibited surfaces

During Phase 1 execution, do not touch:

- `src/`
- `tests/`
- `config/`
- `schemas/`
- `data/`
- `migration_prebuild/`
- `AGENTS.md`
- `intent_migration/AGENTS.override.md`
- `PLANS.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- the numbered live control documents under `docs/` except this Phase 1 ExecPlan and `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` when a later bounded governance step lawfully reopens vocabulary supplementation

This plan is now routed by the live active bounded pack.

Further routing or doctrine changes remain separate bounded governance work.

## Output contracts

Phase 1 owns these machine-readable outputs:

1. `var/audit/ledgers/intent_migration/legacy_runtime_inventory.json`
   - format: JSON object
   - owner: Phase 1 inventory execution
   - status values: `seeded_not_started`, `in_progress`, `complete`
   - completion condition: every donor runtime candidate file is classified as `active_candidate`, `support_only`, or `dead_or_unclear`, carries one explicit `inclusion_rule_class` value, and records minimal provenance and read state

2. `var/audit/ledgers/intent_migration/legacy_file_synopsis.json`
   - format: JSON object
   - owner: later file-synopsis phase
   - status values: `seeded_not_started`, `in_progress`, `complete`
   - completion condition for this phase: seeded only; no synopsis records admitted yet

3. `var/audit/ledgers/intent_migration/legacy_intent_ledger.json`
   - format: JSON object
   - owner: later intent-extraction phase
   - status values: `seeded_not_started`, `in_progress`, `complete`
   - completion condition for this phase: seeded only; no intent records admitted yet

4. `var/audit/ledgers/intent_migration/intent_to_architecture_map.json`
   - format: JSON object
   - owner: later owner-mapping phase
   - status values: `seeded_not_started`, `in_progress`, `complete`
   - completion condition for this phase: seeded only; no mapping records admitted yet

5. `var/audit/ledgers/intent_migration/intent_migration_queue.json`
   - format: JSON object
   - owner: later rebuild-queue phase
   - status values: `seeded_not_started`, `in_progress`, `complete`
   - completion condition for this phase: seeded only; no queue items admitted yet

## Ordered leaf or milestone queue

### Leaf 0 — Governance seeding closeout

Purpose:

- record that the route, plan standard, local vocabulary supplement, and empty machine-readable ledgers were lawfully seeded before Phase 1 execution starts

Output state:

- complete when the routed control surfaces are aligned and the seeded JSON ledgers validate

### Leaf 1 — Donor runtime inclusion rules

Purpose:

- fix the inclusion and exclusion rules for donor inventory scope

Required classifications:

Encode the inclusion taxonomy through `inclusion_rule_class` using exactly these values:

- `runtime_code`
- `runtime_adjacent_support_config_schema`
- `runtime_dependent_fixture_or_reference`
- `excluded_planning_report_or_historical`

Stop condition:

- no donor file is inventoried before the inclusion rules are explicit

### Leaf 2 — Runtime donor inventory population

Purpose:

- read the legacy donor runtime surface file by file and populate `legacy_runtime_inventory.json`

Required fields per record:

- `legacy_file_id`
- `path`
- `file_type`
- `runtime_role`
- `imports`
- `imported_by`
- `config_dependencies`
- `classification`
- `inclusion_rule_class`
- `read_complete`
- `source_lines`
- `evidence_type`
- `notes`

Stop condition:

- do not start synopsis or intent extraction while any active donor runtime candidate remains unread

### Leaf 3 — Inventory closeout

Purpose:

- freeze the Phase 1 completeness state and hand off to the later file-synopsis and intent-extraction phases

Closeout conditions:

- every active donor runtime candidate is read in full
- every inventoried file has one classification
- unresolved files are explicitly marked `dead_or_unclear`
- the progress log, discoveries, and decisions sections are current

## Proof obligations

Leaf 0 was governance-only and seeded the control surfaces. Phase 1 execution after Leaf 0 is inventory work only.

Direct validation required for the current phase state:

- each JSON ledger file must parse as valid JSON
- touched file paths must exist exactly as declared

When Phase 1 executes for real, proof must also show:

- inventory records are structurally complete
- no excluded donor file type was silently treated as active runtime inventory
- no donor runtime candidate was skipped

Tier expectations for later execution:

- Tier A: deterministic inventory-structure checks and completeness checks
- Tier B: bounded consistency checks against donor import or dependency observations when useful
- Tier C: historical or explanatory traces showing why a donor file was classified a particular way

## Stop conditions

Stop and re-plan if any of these become true:

- a required touched surface lies outside the touched-surface list above
- a new durable term is needed and vocabulary governance is not yet updated
- the donor runtime boundary cannot be stated without changing live router or doctrine files
- execution pressure pushes intent extraction or rebuild work into Phase 1

## Progress log

- 2026-04-23: Plan authored. Governance-only seeding step completed. Runtime inventory population not started.
- 2026-04-23: Active-pack routing updated to the intent-migration route. Runtime inventory population still not started.
- 2026-04-23: Top-down control-surface hierarchy aligned so Phase 1 now reads router -> repo law -> plan standard -> phase plan before donor execution.
- 2026-04-23: Local vocabulary now governs `leaf`, and the Phase 1 donor-inclusion taxonomy is now bound mechanically through `inclusion_rule_class`.

## Discoveries and corrections

- 2026-04-23: The programme needs machine-readable ledgers before donor-reading execution starts.
- 2026-04-23: Extra report surfaces are intentionally not created in this step.
- 2026-04-23: The active repo route has now been moved from `migration_prebuild/AGENTS.override.md` to `intent_migration/AGENTS.override.md`.
- 2026-04-23: The Phase 1 restart set is repo-local only. External planning-pack files are not required for restart.
- 2026-04-23: Minimal provenance for this programme means donor file path, donor line range, and evidence type.
- 2026-04-23: After Leaf 0 closeout, Phase 1 mutable scope narrows to this ExecPlan plus the intent-migration ledgers only.
- 2026-04-23: Leaf 1 inclusion rules must not live only in prose; the inventory ledger must bind them through an explicit enum field.

## Decision log

- 2026-04-23: Use one plan-standard file plus one bounded Phase 1 ExecPlan rather than a new report family.
- 2026-04-23: Keep rebuild work out of Phase 1. Phase 1 is inventory only.
- 2026-04-23: Move the active repo route to `intent_migration/AGENTS.override.md` in one bounded governance step, with `AGENTS.md`, `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`, `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`, and this plan updated together so repo truth stays aligned.
- 2026-04-23: Admit the local vocabulary supplement in `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` in the same bounded governance step as the route change.
- 2026-04-23: Freeze upper-layer router and repo-law surfaces before continuing into Phase 1 inventory execution.
- 2026-04-23: Keep `classification` for high-level inventory state and add `inclusion_rule_class` for the explicit Leaf 1 donor-inclusion taxonomy.

## Open questions or carry-forward blockers

- The exact donor inclusion rules for fixtures and runtime-adjacent JSON artefacts remain to be written during Phase 1 execution.

## Blueprint Alignment

This document is subordinate to `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`.

- All structures, stages, and components MUST align to architecture surfaces in `docs/11`.
- All terms MUST be defined in `docs/vocabulary/vocabulary_registry.md`.
- No definitions in this document may contradict `docs/11`.
