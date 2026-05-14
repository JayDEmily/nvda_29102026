# AGENTS.override.md

## Purpose

This file is the active bounded pack surface for the Atlas-to-Native Intent Satisfaction Bridge.

It governs the first ledger-only Bridge run that adjudicates completed Atlas evidence against the accepted native architecture blueprint and governed vocabulary.

Completed Atlas artefacts are evidence only.

The native repo is the destination and truth surface for satisfaction classification.

## Freeze status

This file is mutable only by a bounded governance change that updates the active route, the active-pack declarations, and the routed Bridge plan surface in the same change.

Do not rewrite this file during routine Bridge ledger execution.

## Required read order for the active Bridge pack

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
10. `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
11. `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
12. `PLANS.md`
13. `docs/planning/2026-04-25_ATLAS_TO_NATIVE_INTENT_SATISFACTION_EXECPLAN.md`
14. `config/retained_test_registry.yaml`
15. `config/proof_blocks.yaml`
16. the repo-local Atlas evidence bundle at `var/audit/imports/atlas_bridge_inputs/` and the Native Blueprint Stabilisation receipts named by the routed Bridge ExecPlan

The current routed Bridge plan surface is self-contained for restart together with the working tree and the repo-local Atlas evidence bundle it names.

`intent_migration/AGENTS.override.md` is retained Stage 1 historical evidence only. It is not the active bounded pack for the Bridge.

`migration_prebuild/AGENTS.override.md` remains retained historical support material only unless a later bounded pack explicitly re-admits it as the active route.

## Execution rule

Execute the Bridge as a ledger-only pass.

Do not reinterpret the routed Bridge ExecPlan as Phase 1 inventory work, donor extraction work, runtime implementation work, feature-test modification work, vocabulary admission work, or blueprint rewrite work.

## Touch rule

Do not touch runtime code, feature tests, vocabulary surfaces, `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`, `config/retained_test_registry.yaml`, `config/proof_blocks.yaml`, or the imported Atlas evidence bundle under `var/audit/imports/atlas_bridge_inputs/` during the first Bridge run.

If further progress requires route correction beyond the admitted Bridge pack, stop and reopen the bounded pack before touching additional governance surfaces.

## Definition of done

Do not claim the Bridge is active, complete, aligned, reviewed, or ready without direct file evidence that the active route, active-pack declarations, and routed Bridge plan surface agree on the same state.
