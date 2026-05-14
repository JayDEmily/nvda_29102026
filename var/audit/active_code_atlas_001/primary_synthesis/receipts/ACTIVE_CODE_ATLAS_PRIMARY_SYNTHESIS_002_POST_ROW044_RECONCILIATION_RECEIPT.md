# ACTIVE_CODE_ATLAS_PRIMARY_SYNTHESIS_002_POST_ROW044_RECONCILIATION receipt

## Scope

This pass refreshed the synthesized primary active-code Atlas after row044 added the residual playbook transform-boundary surface record.

## Inputs

- source surface-record files under `var/audit/active_code_atlas_001/*/*records.json`
- synthesis tool `var/audit/active_code_atlas_001/tools/synthesize_primary_active_code_atlas.py`
- row044 record `var/audit/active_code_atlas_001/playbook_library_architecture_surface_transform_required/playbook_library_transform_boundary_active_code_atlas_records.json`

## Output

Updated:

- `var/audit/active_code_atlas_001/primary_active_code_atlas.json`
- `var/audit/active_code_atlas_001/primary_synthesis/reports/primary_active_code_atlas_synthesis_report.json`

## Validation

Validation evidence after synthesis refresh:

- synthesis command: `PASS error_count=0 warning_count=0`
- source surface-record files: `44`
- synthesized active-code Atlas records: `65`
- governed surfaces: `18`
- duplicate record IDs: `0`
- row `FULL_READ_MANIFEST` validator: `PASS error_count=0 warning_count=0`; `entry_count=62`; `stale_hash_mismatch_count=0`; `full_read_false_count=0`
- surface-record/registry validator: `PASS error_count=0 warning_count=0`; surface record count `65`; Tier A registry declared/actual count `120`
- proof-block check-all: `PASS count=46`
- `git diff --check`: status `0`

## Unchanged boundaries

No source, test, runtime, dependency, vocabulary data/admission, original Atlas/Bridge JSON, generated Atlas slice, runtime trading, capital deployment, broker execution, source-ingestion, or row045 work was opened.
