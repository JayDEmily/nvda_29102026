# 2026-04-28 Downstream Capital Deployment Authority Pilot Tranche

Status: closed
Tranche ID: downstream_capital_deployment_authority_pilot_tranche
Blueprint surface: Downstream capital deployment authority
Target owner: capital deployment authority

## 1. Purpose

Create one bounded native implementation tranche for the Downstream capital deployment authority blueprint surface using the completed Bridge ledger as the routing surface.

This tranche-creation change seeds the active pack, the pilot brief, and the child ledger only.

It does not execute the queued implementation leaves.

## 2. Scope boundary

This tranche is limited to the following Bridge satisfaction records:

- `NIS-0278` = `atlas_donor_downstream_018` / `iu_downstream_opening_authorisation_result_contract`
- `NIS-0559` = `atlas_donor_cognition_025` / `iu_cognition_posture_hard_invariants_surface`

Current Bridge truth for this slice is:

- `NIS-0278` = `partially_satisfied` with implementation leaf type `later_test_first_leaf`
- `NIS-0559` = `transform_required` with implementation leaf type `later_blueprint_leaf`

This tranche-creation change does not add native runtime behaviour, does not modify tests, and does not process any Atlas record outside these two admitted records.

## 3. Authority and evidence to read

Read and obey:

- `AGENTS.md`
- `intent_migration/native_intent_implementation/AGENTS.override.md`
- `docs/00_CONTROL_SURFACE_ROUTING_INDEX.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md`
- `docs/05_GUARDRAILS_CORE.md`
- `docs/06_PROCESS_AND_TRANCHE_LAW_CORE.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md`
- `docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `docs/vocabulary/CONSOLIDATION_WORKFLOW.md`
- `PLANS.md`
- `config/retained_test_registry.yaml`
- `config/proof_blocks.yaml`
- `tests/AGENTS.override.md` before any future test touch
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_validation_report.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json` for `NIS-0278` and `NIS-0559`

## 4. Touched surfaces

- `AGENTS.md`
- `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- `intent_migration/native_intent_implementation/AGENTS.override.md`
- `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`
- `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.schema.json`

## 5. Read-only mandatory-reading surfaces

- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_validation_report.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `src/nvda_desk/contracts/downstream.py`
- `src/nvda_desk/contracts/capital.py`
- `src/nvda_desk/capital/authority.py`
- `src/nvda_desk/downstream/opening.py`
- `tests/tier_a/capital_deployment/test_capital_contract_models.py`
- `tests/tier_a/capital_deployment/test_capital_authority_service_surface.py`

## 6. Prohibited surfaces

During tranche creation, do not touch:

- runtime code under `src/`
- native tests under `tests/`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- vocabulary surfaces
- the Bridge validation report
- the Bridge satisfaction ledger
- the imported Atlas evidence bundle

## 7. Output contracts

### 7.1 Active-pack route

- path: `AGENTS.md`
- format: markdown
- owner: repo route
- completion condition: routes to the new pilot pack truthfully

### 7.2 Working route supplement

- path: `docs/06.1_PROCESS_AND_TRANCHE_LAW_WORKING.md`
- format: markdown
- owner: tranche-law supplement
- completion condition: admits the pilot pack truthfully

### 7.3 Pilot pack surface

- path: `intent_migration/native_intent_implementation/AGENTS.override.md`
- format: markdown
- owner: active bounded pack
- completion condition: declares read order, touch rule, and bounded scope truthfully

### 7.4 Pilot tranche brief

- path: `var/audit/briefs/2026-04-28_DOWNSTREAM_CAPITAL_DEPLOYMENT_AUTHORITY_PILOT_TRANCHE.md`
- format: markdown
- owner: tranche brief
- completion condition: defines scope, queue, stop conditions, and current open-state truthfully

### 7.5 Pilot child ledger

- path: `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.json`
- format: json
- owner: tranche receipt
- completion condition: records the two admitted Bridge records, the queued leaves, and current open-state truthfully

### 7.6 Pilot child-ledger schema

- path: `var/audit/ledgers/downstream_capital_deployment_authority_pilot_tranche_ledger.schema.json`
- format: json
- owner: tranche receipt schema
- completion condition: validates the child ledger shape used by this tranche

## 8. Ordered leaf queue

### DCA-PILOT-L01

- status: closed
- implementation leaf type: `later_blueprint_leaf`
- source record: `NIS-0559`
- bounded job: define the lawful native blueprint/contract surface for the posture hard-invariants material without letting capital deployment authority absorb posture ownership
- stop condition: satisfied; `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md` now routes posture permission into capital deployment only through serial candidate material or downstream pre-deployment result

### DCA-PILOT-L02

- status: closed
- implementation leaf type: `later_test_first_leaf`
- source record: `NIS-0278`
- bounded job: extend or replace proof so that the downstream opening-authorisation result shell is governed by truthful native tests before any code refactor
- stop condition: satisfied; `tests/tier_a/capital_deployment/test_capital_contract_models.py` now proves bounded capital values, downstream opening-authorisation shell carriage, and no capital-contract absorption of downstream shell fields

### DCA-PILOT-L03

- status: closed
- implementation leaf type: `mandatory_closeout_leaf`
- bounded job: reconcile route, brief, ledger, proof receipts, and carry-forward blockers after L01 and L02
- stop condition: satisfied; brief, child ledger, registry receipt, proof commands, and packaging checks reconciled

## 9. Proof obligations

For tranche creation only, prove:

- the route surfaces parse and agree on the same active pack
- the pilot brief exists and matches the child ledger scope
- the child ledger parses as JSON
- the child ledger validates against its schema
- no runtime code or tests changed in this creation change
- the pilot queue is bounded to exactly two Bridge records and three leaves

## 10. Stop conditions

Stop if any condition occurs:

1. the active route cannot be updated without touching additional governance surfaces
2. the pilot scope expands beyond `NIS-0278` and `NIS-0559`
3. runtime code or native tests become necessary during tranche creation
4. the pilot brief and child ledger disagree on scope or queue truth
5. the child ledger cannot be validated against its schema

## 11. Progress log

- 2026-04-28: pilot tranche creation started from the recovered healthy bridge snapshot on branch `work/downstream-capital-authority-pilot-20260428`
- 2026-04-28: active route updated to the pilot pack
- 2026-04-28: pilot pack, brief, child ledger, and child-ledger schema created
- 2026-04-28: tranche creation completed; execution leaves queued
- 2026-04-28: `DCA-PILOT-L01` closed as a blueprint-boundary correction
- 2026-04-28: `DCA-PILOT-L02` closed as test-first downstream opening-authorisation shell proof
- 2026-04-28: `DCA-PILOT-L03` closed after receipt and closeout reconciliation

## 12. Discoveries and corrections

- The recovered healthy snapshot is the current lawful base for recreation work in this thread.
- The Bridge validation report already isolates this blueprint surface to exactly two records.
- The current native baseline remains placeholder-thin on the downstream opening-authorisation contract, so tranche creation must stop before code/test work.

## 13. Decision log

- Decision: use the Bridge validation report and Bridge ledger as the tranche-routing surface rather than re-reading the full raw Atlas during tranche creation.
- Decision: keep tranche creation code-free and test-free.
- Decision: queue one blueprint leaf, one test-first leaf, and one mandatory closeout leaf only.

## 14. Open questions or carry-forward blockers

- `DCA-PILOT-L01` is closed.
- `DCA-PILOT-L02` is closed.
- `DCA-PILOT-L03` is closed.
- The downstream opening-authorisation shell is present and governed by Tier A proof.
- Broader capital sizing semantics remain placeholder-thin outside this pilot and require a later proof-hardening tranche before they are treated as mature behaviour.

## 15. Closeout proof record

- `PYTHONPATH=src pytest tests/tier_a/capital_deployment -q` passed.
- `PYTHONPATH=src pytest tests -q` was not reverified in this review pass; system Python became unstable after the targeted capital slice and the broader run is therefore Unknown for this pass.
- child ledger JSON parsed.
- child ledger schema JSON parsed.
- retained test registry YAML parsed.
- parent brief SHA was reconciled into the child ledger after closeout edits.
- `git diff --check` passed.
- final zip integrity check passed.
- Earlier full-suite success from the previous pass was not treated as current evidence after the executed artefact was lost; this replay records only checks directly re-run here.
