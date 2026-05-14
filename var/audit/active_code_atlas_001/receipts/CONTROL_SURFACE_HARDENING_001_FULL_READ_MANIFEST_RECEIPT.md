# CONTROL_SURFACE_HARDENING_001_FULL_READ_MANIFEST_RECEIPT

Date: 2026-05-11
Branch: `worker/full-read-manifest-hardening-001`
Base accepted commit: `cb74f43`
Pass type: control-surface hardening only; not Atlas content adjudication.

## What changed

Installed a mandatory `FULL_READ_MANIFEST` control before future substantive worker work.

Changed control documents now require every future worker pass to create an auditable manifest before any surface record, test extension, source repair, receipt, proof-closure statement, or ledger update can rely on selected files.

The manifest rule requires these fields for every controlling file and selected material file:

- `path`
- `byte_count`
- `line_count`
- `sha256`
- `read_method`
- `full_read`
- `chunk_ranges` when chunked
- `notes` only where needed

The rule also states that search, grep, AST extraction, generated inventories, summaries, and prior chat memory may assist discovery but cannot satisfy the full-read requirement.

## Why it changed

The generated all-surface active-code Atlas is accepted only as structural inventory/navigation. It is not the primary semantic active-code Atlas. Future surface adjudication therefore needs auditable proof that selected governing and material files were actually read before workers mutate tests/source/records/receipts or close ledger entries.

This pass also records that blueprint surface numbers are taxonomy labels, not execution order. The live dependency order is now explicitly recorded in `PLANS.md` and `ROADMAP_LEDGER.md`.

## Files read in full for this hardening pass

The following files are recorded in `var/audit/active_code_atlas_001/full_read_manifests/CONTROL_SURFACE_HARDENING_001_FULL_READ_MANIFEST.json`:

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `var/audit/active_code_atlas_001/receipts/ACTIVE_CODE_ATLAS_EXECUTION_CADENCE_PLAN_CLARIFICATION_RECEIPT.md`
- `var/audit/active_code_atlas_001/persistence_ledgers_receipts_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_004_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE_RECEIPT.md`
- `var/audit/active_code_atlas_001/persistence_ledgers_receipts_surface_new_test_family/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_005_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE_NEW_TEST_FAMILY_RECEIPT.md`
- `var/audit/active_code_atlas_001/persistence_ledgers_receipts_surface_transform_required/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_006_PERSISTENCE_LEDGERS_RECEIPTS_SURFACE_TRANSFORM_REQUIRED_RECEIPT.md`
- `var/audit/active_code_atlas_001/receipts/ACTIVE_CODE_ATLAS_REGISTRY_AND_EVIDENCE_RANGE_REPAIR_RECEIPT.md`
- `var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py`
- `var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py`

## Files modified

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `var/audit/active_code_atlas_001/full_read_manifests/CONTROL_SURFACE_HARDENING_001_FULL_READ_MANIFEST.json`
- `var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py`
- `var/audit/active_code_atlas_001/reports/validate_full_read_manifest_output.json`
- `var/audit/active_code_atlas_001/reports/validate_full_read_manifest_output.txt`
- `var/audit/active_code_atlas_001/receipts/CONTROL_SURFACE_HARDENING_001_FULL_READ_MANIFEST_RECEIPT.md`

## Validation run

```bash
python3 var/audit/active_code_atlas_001/tools/validate_full_read_manifest.py
```

Observed result:

```text
validation_status=PASS
error_count=0
warning_count=0
manifest_count=1
entry_count=10
stale_hash_mismatch_count=0
full_read_false_count=0
exit_status=0
```

## Ledger state

The latest accepted ledger already advanced persistence/ledger/receipt rows 004-006 and points to:

```text
ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE
```

This hardening pass does not rewind to persistence row 004 because no concrete defect was found in the accepted persistence receipts or ledger state.

## What remains unchanged

This pass did not perform Atlas content adjudication, source/runtime repair, unrelated test implementation, dependency or VENV work, original Atlas/Bridge JSON mutation, generated Atlas slice mutation, vocabulary data/admission changes, trading behaviour changes, financial/risk-policy changes, or refactor work.
