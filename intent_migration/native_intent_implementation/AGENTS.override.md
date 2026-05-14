# AGENTS.override.md

## Purpose

This file is the active bounded pack surface for the downstream capital deployment authority pilot tranche.

It governs the bounded transition from the completed Bridge ledger into one native implementation tranche.

The active tranche is limited to the Downstream capital deployment authority blueprint surface and the two Bridge satisfaction records admitted by the pilot brief.

## Freeze status

This file is mutable only by a bounded governance change that updates the active route, the active-pack declarations, and the routed tranche brief in the same change.

Do not rewrite this file during routine pilot-tranche execution.

## Required read order for the active pilot pack

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
13. `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
14. `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`
15. `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.schema.json`
16. `var/audit/ledgers/intent_migration/native_intent_satisfaction_validation_report.json`
17. the two admitted Bridge records in `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`:
    - `NIS-0278`
    - `NIS-0559`
18. `config/retained_test_registry.yaml`
19. `config/proof_blocks.yaml`
20. `tests/AGENTS.override.md` before touching `tests/`

## Execution rule

Execute this bounded pack as one native implementation tranche only.

Do not process the full Atlas.

Do not admit any record outside `NIS-0278` and `NIS-0559` without a later bounded-pack change.

## Touch rule

During tranche creation, touched surfaces are limited to:

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- this file
- `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.schema.json`

Runtime code, tests, blueprint surfaces, vocabulary surfaces, and Bridge evidence remain read-only during tranche creation.

Later leaf execution may not expand touched scope silently. Re-open the bounded tranche scope in the pilot brief before touching runtime code or tests.

## Definition of done

Do not claim the pilot tranche exists until the active route, the active-pack declarations, the pilot brief, and the child ledger agree on the same bounded scope, queued leaves, and open-state truth.
