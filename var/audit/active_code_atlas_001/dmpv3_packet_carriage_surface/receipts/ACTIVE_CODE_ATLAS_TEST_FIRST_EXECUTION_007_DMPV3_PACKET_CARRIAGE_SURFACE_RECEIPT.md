# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE_RECEIPT

Date: 2026-05-11
Branch: `worker/full-read-manifest-hardening-001`
Base commit for this row: `a061f2085d10b85bc897f02521d4c9d475705752`
Surface: `5.6 DMPV3 packet carriage`
Queue row: `ACATQ-0017` / `ACABC-0017`
Action class: `extend_existing_test_family_before_code`

## What changed

- Created a DMPV3 surface `FULL_READ_MANIFEST` before DMPV3 substantive work.
- Added surface-specific records in `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface/dmpv3_packet_carriage_active_code_atlas_records.json`.
- Extended `tests/tier_a/packets/test_reference_packet_carriage.py` with `test_dmpv3_extensions_cannot_replace_canonical_schema_identifiers` before source repair.
- Repaired only `src/nvda_desk/contracts/packets.py` so custom `dmpextensions` can preserve extra `nvda` execution context but cannot replace repo-owned canonical `nvda.schema_identifiers`.
- Updated `PLANS.md` and `ROADMAP_LEDGER.md` to advance the live pointer to `ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_008_DMPV3_PACKET_CARRIAGE_SURFACE_NEW_TEST_FAMILY`.

## Why it changed

`docs/09_DMPV3_PROTOCOL_CORE.md` requires a single canonical DMPV3 packet grammar and states that `dmpextensions` must not replace or weaken canonical fields or repo-owned `nvda` compatibility leaves. The new Tier A test exposed that caller-supplied `dmpextensions.nvda.schema_identifiers` could overwrite canonical payload/output schema identifiers. The repair restores canonical schema identifiers after custom extension merge.

## Files read in full before DMPV3 substantive work

Recorded in `var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE_FULL_READ_MANIFEST.json`, including:

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md`
- `docs/09_DMPV3_PROTOCOL_CORE.md`
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `config/proof_blocks.yaml`
- selected DMPV3 packet/source/schema files
- `tests/tier_a/packets/test_reference_packet_carriage.py`

The manifest was regenerated after test/source/control-doc mutations for files relied on at closure.

## Files modified

- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `src/nvda_desk/contracts/packets.py`
- `tests/tier_a/packets/test_reference_packet_carriage.py`
- `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface/dmpv3_packet_carriage_active_code_atlas_records.json`
- `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface/reports/*`
- `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface/receipts/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE_RECEIPT.md`
- `var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_007_DMPV3_PACKET_CARRIAGE_SURFACE_FULL_READ_MANIFEST.json`

## Validation run

- Pre-repair targeted packet pytest: `1 failed, 5 passed`, `exit_status=1`.
- Post-repair targeted packet pytest: `6 passed`, `exit_status=0`.
- Support-spine proof block `support_spine_prepared_packet_review_surface`: `34 passed`, `exit_status=0`.
- Proof-block manifest check: `proof_blocks_check_all=PASS count=21`, `exit_status=0`.
- Surface-record/registry validator: `PASS`, `error_count=0`, `warning_count=0`.
- DMPV3 `FULL_READ_MANIFEST` validator: `PASS`, `error_count=0`, `stale_hash_mismatch_count=0`.
- `git diff --check`: `exit_status=0`.

## What remains unchanged

- Generated all-surface active-code Atlas remains structural inventory/navigation only.
- Original Atlas/Bridge JSON was not mutated.
- Generated Atlas slices were not rebuilt or mutated.
- Vocabulary data was not changed.
- Dependency files and VENV were not changed.
- Runtime trading behaviour, broker/API execution, capital/risk policy, financial policy, and refactor work remain closed.

## Next pointer

`ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_008_DMPV3_PACKET_CARRIAGE_SURFACE_NEW_TEST_FAMILY`
