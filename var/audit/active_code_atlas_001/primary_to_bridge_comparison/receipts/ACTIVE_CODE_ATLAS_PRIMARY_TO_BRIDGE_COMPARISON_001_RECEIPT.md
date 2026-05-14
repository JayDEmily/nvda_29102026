# ACTIVE_CODE_ATLAS_PRIMARY_TO_BRIDGE_COMPARISON_001 receipt

Status: `comparison_recorded_with_linkage_gaps`

## Scope

This pass compared the synthesized primary active-code Atlas to read-only Atlas/Bridge evidence after the dependency-order surface queue was exhausted.

Opened work:

- audit comparison artefact generation under `var/audit/active_code_atlas_001/primary_to_bridge_comparison/`;
- comparator tooling under `var/audit/active_code_atlas_001/tools/compare_primary_active_code_atlas_to_bridge.py`;
- `PLANS.md` and `ROADMAP_LEDGER.md` pointer/history updates.

Closed work:

- source implementation changes;
- active tests/proof-block manifest changes;
- runtime trading behaviour;
- dependency changes;
- vocabulary mutation/admission;
- original Atlas/Bridge JSON mutation;
- generated Atlas slice rebuild;
- status-upgrade or full-native-satisfaction claims.

## Inputs

- `var/audit/active_code_atlas_001/primary_active_code_atlas.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_execution_queue.json`

## Outputs

- `var/audit/active_code_atlas_001/tools/compare_primary_active_code_atlas_to_bridge.py`
- `var/audit/active_code_atlas_001/primary_to_bridge_comparison/primary_to_bridge_comparison.json`
- `var/audit/active_code_atlas_001/primary_to_bridge_comparison/reports/primary_to_bridge_comparison_report.json`

## Comparator result

- validation status: `PASS`
- error count: `0`
- warning count: `36`
- primary records: `64`
- primary governed surfaces: `18`
- Atlas records observed: `1716`
- native satisfaction ledger records observed: `1716`
- static comparison groups observed: `48`
- execution queue records observed: `46`
- primary-linked execution queue records: `42`
- primary-linked static comparison groups: `42`

## Gap finding

The comparison artefact is structurally valid but not fully reconciled:

- execution queue rows without a primary active-code Atlas link: `ACATQ-0025`, `ACATQ-0044`, `ACATQ-0045`, `ACATQ-0046`;
- static comparison groups without a primary active-code Atlas link: `ACABC-0025`, `ACABC-0035`, `ACABC-0045`, `ACABC-0046`, `ACABC-0047`, `ACABC-0048`.

These are audit linkage gaps. They do not invalidate the comparison output, but they block any claim that the primary active-code Atlas is fully reconciled to the prior Bridge comparison/queue without a follow-on bounded reconciliation pass.

## Validation evidence

- comparator command: `PYTHONPATH=src .venv/bin/python var/audit/active_code_atlas_001/tools/compare_primary_active_code_atlas_to_bridge.py`
  - status file: `var/audit/active_code_atlas_001/primary_to_bridge_comparison/reports/compare_primary_active_code_atlas_to_bridge.status`
  - observed status: `0`
- black command: `.venv/bin/python -m black var/audit/active_code_atlas_001/tools/compare_primary_active_code_atlas_to_bridge.py`
  - observed status: `0`
- ruff command: `.venv/bin/python -m ruff check var/audit/active_code_atlas_001/tools/compare_primary_active_code_atlas_to_bridge.py`
  - observed status: `0`
- surface-record/registry validator: `PYTHONPATH=src .venv/bin/python var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py`
  - observed status: `0`
  - validation status: `PASS`
  - error count: `0`
- proof-block check-all: `PYTHONPATH=src .venv/bin/python scripts/run_proof_block.py --check-all`
  - observed status: `0`
  - observed output: `proof_blocks_check_all=PASS count=45`
- pre-final-manifest `git diff --check`
  - observed status: `0`

## Next lawful target

`ACTIVE_CODE_ATLAS_PRIMARY_LINKAGE_GAP_RECONCILIATION_001`, bounded to audit linkage-gap artefacts only.
