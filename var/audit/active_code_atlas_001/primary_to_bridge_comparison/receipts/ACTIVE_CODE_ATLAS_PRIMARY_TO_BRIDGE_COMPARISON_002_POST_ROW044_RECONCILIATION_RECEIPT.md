# ACTIVE_CODE_ATLAS_PRIMARY_TO_BRIDGE_COMPARISON_002_POST_ROW044_RECONCILIATION receipt

## Scope

This pass refreshed the primary-to-Bridge comparison after row044 and primary synthesis 002.

## Inputs

- `var/audit/active_code_atlas_001/primary_active_code_atlas.json`
- `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json`
- `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_bridge_comparison.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_record_join.json`
- `var/audit/active_code_atlas_bridge_comparison_001/active_code_atlas_test_first_execution_queue.json`

## Output

Updated:

- `var/audit/active_code_atlas_001/primary_to_bridge_comparison/primary_to_bridge_comparison.json`
- `var/audit/active_code_atlas_001/primary_to_bridge_comparison/reports/primary_to_bridge_comparison_report.json`

## Result

Comparison command result: `PASS error_count=0 warning_count=36`.

Key counts:

- primary records: `65`
- governed primary surfaces: `18`
- legacy Atlas records: `1,716`
- native satisfaction ledger records: `1,716`
- static comparison records: `48`
- execution queue rows: `46`
- primary-linked comparison groups: `43`
- primary-linked execution queue rows: `43`
- execution queue rows without primary link: `3`
- comparison groups without primary link: `5`

The prior residual playbook gap `ACATQ-0025` / `ACABC-0025` is no longer reported as unlinked after row044.

Remaining unlinked queue rows:

- `ACATQ-0044`
- `ACATQ-0045`
- `ACATQ-0046`

Remaining unlinked comparison groups:

- `ACABC-0035`
- `ACABC-0045`
- `ACABC-0046`
- `ACABC-0047`
- `ACABC-0048`

## Validation

Validation evidence after comparison refresh:

- comparison command: `PASS error_count=0 warning_count=36`
- row `FULL_READ_MANIFEST` validator: `PASS error_count=0 warning_count=0`; `entry_count=24`; `stale_hash_mismatch_count=0`; `full_read_false_count=0`
- surface-record/registry validator: `PASS error_count=0 warning_count=0`; surface record count `65`; Tier A registry declared/actual count `120`
- proof-block check-all: `PASS count=46`
- `git diff --check`: status `0`

## Unchanged boundaries

No source, test, runtime, dependency, vocabulary data/admission, original Atlas/Bridge JSON, generated Atlas slice, runtime trading, capital deployment, broker execution, source-ingestion, or row045 work was opened.
