# Active Codebase Alignment Repair Pack

Status: closed
Pack ID: active_codebase_alignment_repair_tranche

## Purpose

This pack owns the small audit-repair tranche that follows the reviewed downstream capital deployment authority pilot tranche.

The pack reconciles control truth and Tier A registry truth before any new Atlas blueprint-surface tranche is opened.

## Scope

This pack may touch only:

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `intent_migration/active_codebase_alignment_repair/AGENTS.override.md`
- `config/retained_test_registry.yaml`
- `var/audit/briefs/2026-04-28_ACTIVE_CODEBASE_ALIGNMENT_REPAIR_TRANCHE.md`
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.json`
- `var/audit/ledgers/active_codebase_alignment_repair_tranche_ledger.schema.json`
- `var/audit/ledgers/active_codebase_alignment_repair_presence_inventory.json`

## Read-only mandatory surfaces

Read and obey before editing within this pack:

- `AGENTS.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `config/retained_test_registry.yaml`
- `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`

## Prohibited work

This pack must not:

- open a new Atlas blueprint-surface tranche;
- process the full 1716-record Atlas as execution scope;
- edit runtime source under `src/`;
- edit native pytest files under `tests/`;
- claim full-suite pytest health unless the suite is actually rerun and passes in the current pass;
- convert presence-test inventory into broad behavioural refactors.

## Leaf order

1. `ACR-L01` — plan and route the active-codebase alignment repair tranche.
2. `ACR-L02` — reconcile Tier A registry inventory truth.
3. `ACR-L03` — inventory shallow / presence-only Tier A proof surfaces without refactor.
4. `ACR-L04` — mandatory closeout.

## Closeout rule

Closeout must state remaining blockers truthfully and must not promote new Atlas work.
