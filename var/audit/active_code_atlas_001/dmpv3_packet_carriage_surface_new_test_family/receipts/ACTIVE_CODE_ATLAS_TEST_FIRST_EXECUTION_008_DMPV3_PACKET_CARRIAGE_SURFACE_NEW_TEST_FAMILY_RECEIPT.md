# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_008_DMPV3_PACKET_CARRIAGE_SURFACE_NEW_TEST_FAMILY_RECEIPT

Date: 2026-05-11
Branch: `worker/full-read-manifest-hardening-001`
Base commit for this row: `14dce0eb75c692351c0a185c470936b2db4e8813`
Surface: `5.6 DMPV3 packet carriage`
Queue row: `ACATQ-0016` / `ACABC-0016`
Action class: `write_new_test_family_before_code`

## What changed

- Created a row-specific `FULL_READ_MANIFEST` before substantive row 008 work.
- Added retained Tier A family `tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py`.
- Added proof block `dmpv3_extension_canonical_leaf_surface` to `config/proof_blocks.yaml`.
- Added retained-test registry admission and Tier A inventory entry for the new packet family in `config/retained_test_registry.yaml`; Tier A count is now `98`.
- Added surface-specific record file `var/audit/active_code_atlas_001/dmpv3_packet_carriage_surface_new_test_family/dmpv3_extension_canonical_leaf_active_code_atlas_records.json`.
- Repaired only `src/nvda_desk/contracts/packets.py` so custom extensions cannot replace canonical `nvda.semantic_dependencies` derived from DMPV3 lineage.
- Updated `PLANS.md` and `ROADMAP_LEDGER.md` to advance the live pointer to `ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_009_DMPV3_PACKET_CARRIAGE_SURFACE_TRANSFORM_REQUIRED`.

## Why it changed

`docs/09_DMPV3_PROTOCOL_CORE.md` requires live packets to carry bounded lineage and reserves the repo-owned `nvda` extension block for bounded compatibility metadata including semantic dependency annotations. It also says a custom extension must merge without erasing canonical repo-owned `nvda` compatibility leaves. The new Tier A family exposed that caller-supplied `dmpextensions.nvda.semantic_dependencies` could replace canonical dependency truth derived from `lineage.dependencyids`. The bounded repair restores canonical semantic dependencies after custom extension merge while preserving unrelated custom extension leaves.

## Files read in full before substantive row work

Recorded in `var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_008_DMPV3_PACKET_CARRIAGE_SURFACE_NEW_TEST_FAMILY_FULL_READ_MANIFEST.json`, including:

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `var/audit/active_code_atlas_bridge_comparison_001/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_QUEUE_001.md`
- `docs/09_DMPV3_PROTOCOL_CORE.md`
- `docs/09.1_DMPV3_PROTOCOL_WORKING.md`
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- selected DMPV3 packet/source/schema files
- selected packet tests and row 007 DMPV3 records/receipt

The manifest was regenerated after test/source/config/control-doc mutations for files relied on at closure.

## Validation run

- Pre-repair targeted packet pytest: `1 failed, 2 passed`, `exit_status=1`.
- Post-repair targeted packet pytest: `3 passed`, `exit_status=0`.
- Proof block `dmpv3_extension_canonical_leaf_surface`: `3 passed`, `exit_status=0`.
- Proof-block manifest check: `proof_blocks_check_all=PASS count=22`, `exit_status=0`.
- Surface-record/registry validator: `PASS`, `error_count=0`, `warning_count=0`.
- Row `FULL_READ_MANIFEST` validator: `PASS`, `error_count=0`, `stale_hash_mismatch_count=0`.
- `git diff --check`: `exit_status=0`.

## What remains unchanged

- Generated all-surface active-code Atlas remains structural inventory/navigation only.
- Original Atlas/Bridge JSON was not mutated.
- Generated Atlas slices were not rebuilt or mutated.
- Vocabulary data was not changed.
- Dependency files and VENV were not changed.
- Runtime trading behaviour, broker/API execution, capital/risk policy, financial policy, and refactor work remain closed.

## Next pointer

`ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_009_DMPV3_PACKET_CARRIAGE_SURFACE_TRANSFORM_REQUIRED`
