# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_017_RAW_SIGNAL_FAMILIES_SURFACE_NEW_TEST_FAMILY_RECEIPT

## Scope

Surface: `5.3 Raw signal families`.

Queue row: `ACATQ-0008` / `ACABC-0008`.

Required action: write new Tier A test family before code.

Structural inventory status: navigation/scaffold only; not semantic authority.

## Full-read manifest

Created and regenerated:

`var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_017_RAW_SIGNAL_FAMILIES_SURFACE_NEW_TEST_FAMILY_FULL_READ_MANIFEST.json`

The manifest covers controlling files and selected material files for row 017, including root control files, raw-signal normative/current-map evidence, upstream-signal source files, existing upstream-signal tests, the new Tier A test family, proof/registry files, the surface record file, and this receipt.

## What changed

- Added new retained Tier A test family `tests/tier_a/upstream_signal/test_raw_signal_contract_copy_boundaries.py` before source repair.
- The pre-repair test exposed a bounded gap: `RawUpstreamSignalInput` retained caller-owned nested payload containers after model construction.
- Repaired `src/nvda_desk/contracts/upstream_signal.py` by adding a payload field validator that deep-copies caller input before raw-signal scope admission.
- Added proof block `raw_signal_contract_copy_boundary_surface` to `config/proof_blocks.yaml`.
- Added retained-test registry admission and Tier A inventory entry for the new family in `config/retained_test_registry.yaml`; Tier A declared/actual count is now `104`.
- Added read-adjudicated surface record file `var/audit/active_code_atlas_001/raw_signal_families_surface_new_test_family/raw_signal_contract_copy_boundary_active_code_atlas_records.json`.
- Updated `PLANS.md` and `ROADMAP_LEDGER.md` to advance the live pointer to row 018.

## Validation

- Pre-repair targeted new family: `1 failed, 1 passed`.
- Post-repair targeted new family: `2 passed`.
- Upstream-signal directory: `10 passed`.
- New proof block `raw_signal_contract_copy_boundary_surface`: `2 passed`.
- Support-spine proof block: `37 passed`.
- Proof-block manifest check: `proof_blocks_check_all=PASS count=29`.
- Surface-record/registry validator: `PASS error_count=0 warning_count=0`.
- Final row `FULL_READ_MANIFEST` validator: recorded in row reports.

## Boundaries not opened

No dependency, VENV, original Atlas/Bridge JSON, generated slice, vocabulary data, live API client, runtime trading, financial/risk policy, raw signal preparation, cognition authority, capital authority, or unrelated refactor work was opened by this row.

## Next target

`ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_018_RAW_SIGNAL_FAMILIES_SURFACE_TRANSFORM_REQUIRED`

Queue row: `ACATQ-0007` / `ACABC-0007`.
