# AGENTS.override.md

## Purpose

This file is the active bounded pack surface for the intent-migration programme.

It governs bounded work that converts legacy donor evidence into native rebuilt behaviour under the current architecture.

The legacy tree is donor evidence only.

The rebuilt repo is the destination.

## Freeze status

This file is mutable only by a bounded governance change that updates the active route and the routed plan surfaces in the same change.

Do not rewrite this file during routine donor reading, intent extraction, mapping, rebuild, or proof work.

## Required read order for the active intent-migration pack

Read these files in this exact order:

1. `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
2. `docs/01_NORMATIVE_CORE.md`
3. `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`
4. `docs/05_GUARDRAILS_CORE.md`
5. `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
6. `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md` when it contains admitted local material
7. `docs/08_TESTING_AND_PROMOTION_CORE.md`
8. `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
9. `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md` when it contains admitted local material
10. `PLANS.md`
11. `docs/planning/2026-04-23_INTENT_MIGRATION_PHASE1_LEGACY_RUNTIME_INVENTORY_EXECPLAN.md`
12. `tests/AGENTS.override.md` when the active task touches `tests/`
13. `legacy_import/README.md` when the active task reads donor runtime surfaces

Later bounded intent-migration ExecPlans enter this ordered list only when they are lawfully admitted in the same bounded governance change that updates this file.

The current routed repo-local plan surfaces are self-contained for restart. Do not require external planning-pack files to restart the current Phase 1 work.

When the active task needs historical prebuild lineage, read `migration_prebuild/AGENTS.override.md` and the routed artefacts there as retained evidence only, not as the active bounded pack.

## Execution rule

Plan and execute rebuild work by atomic intent unit.

Treat files as inventory and reading units, not as migration units.

Do not mark an intent unit complete until provenance, target owner, and Tier A, Tier B, and Tier C proof obligations are satisfied or truthfully declared out of scope by governing law.

## Touch rule

Do not touch runtime code, tests, doctrine files, donor files, or receipts outside the currently admitted bounded scope.

If a new surface becomes necessary, reopen the bounded pack before touching it.

## Definition of done

Do not claim complete, aligned, reviewed, or ready without direct file evidence.

Do not let the routed plan surfaces go stale when branch truth changes.
