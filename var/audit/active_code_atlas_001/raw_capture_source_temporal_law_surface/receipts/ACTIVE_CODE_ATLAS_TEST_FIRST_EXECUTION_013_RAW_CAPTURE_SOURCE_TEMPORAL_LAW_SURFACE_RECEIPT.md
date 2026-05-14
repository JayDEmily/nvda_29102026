# ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_013_RAW_CAPTURE_SOURCE_TEMPORAL_LAW_SURFACE receipt

## Scope

This pass adjudicated the dependency-order row `ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_013_RAW_CAPTURE_SOURCE_TEMPORAL_LAW_SURFACE` for architecture row `5.2 Raw capture and source temporal law`.

The generated all-surface active-code Atlas remained navigation/scaffold only and was not treated as semantic authority.

## Full-read manifest

Created and regenerated:

- `var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_013_RAW_CAPTURE_SOURCE_TEMPORAL_LAW_SURFACE_FULL_READ_MANIFEST.json`

The manifest records the controlling files and selected material files used for this pass, including `AGENTS.md`, `PLANS.md`, `ROADMAP_LEDGER.md`, the row 5.2 normative evidence, selected source files, selected Tier A tests, proof configuration, and this surface's receipt/record material.

## Files read in full via manifest

The pass relied on the row `FULL_READ_MANIFEST` for the controlling and selected material files. The material set included:

- `AGENTS.md`
- `PLANS.md`
- `ROADMAP_LEDGER.md`
- `docs/01_NORMATIVE_CORE.md`
- `docs/04.1_TECHNICAL_ARCHITECTURE_WORKING.md`
- `docs/08_TESTING_AND_PROMOTION_CORE.md`
- `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md`
- `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md`
- `config/proof_blocks.yaml`
- `config/retained_test_registry.yaml`
- `src/nvda_desk/ingress/raw_bundle_loader.py`
- `src/nvda_desk/contracts/temporal.py`
- `src/nvda_desk/upstream/raw_signal_ingress.py`
- `src/nvda_desk/contracts/upstream_signal.py`
- `tests/tier_a/ingress/test_raw_bundle_loader_surface.py`
- `tests/tier_a/upstream_signal/test_upstream_non_interference_and_sanity_traces.py`
- `tests/tier_a/upstream_signal/test_upstream_signal_coverage_map_and_scope_lock.py`

## What changed

- Extended existing Tier A family `tests/tier_a/ingress/test_raw_bundle_loader_surface.py` before source repair.
- Added a source-temporal invariant: raw bundle loading must not accept `captured_at_utc`/`persisted_at_utc` as substitutes for source observation truth.
- Reproduced the bounded pre-repair failure: `1 failed, 2 passed`.
- Repaired only `src/nvda_desk/ingress/raw_bundle_loader.py` by requiring `source_time_utc` or `source_date` on `RawBundleProvenance`.
- Updated the existing options-wrapper fixture to carry `source_time_utc`, because wrappers using the raw bundle loader now must carry source observation truth.
- Added proof block `raw_capture_source_temporal_law_surface`.
- Added one read-adjudicated surface-record file for row 013.
- Updated `PLANS.md` and `ROADMAP_LEDGER.md` to advance to row 014.

## Validation run

- Pre-repair targeted test: `1 failed, 2 passed`.
- Post-repair targeted test: `3 passed`.
- `raw_capture_source_temporal_law_surface` proof block: `3 passed`.
- Proof-block manifest check: `PASS count=26`.
- Surface-record/registry validator: `PASS error_count=0 warning_count=0`.
- Row `FULL_READ_MANIFEST` validator: `PASS error_count=0` after manifest regeneration.

## Unchanged boundaries

No dependency, VENV, original Atlas/Bridge JSON, generated Atlas slice, vocabulary data, runtime trading behaviour, financial/risk authority, live API client, broker path, capital authority, or unrelated refactor work was changed.

## Ledger state after this pass

`PLANS.md` and `ROADMAP_LEDGER.md` now point to:

`ACTIVE_CODE_ATLAS_TEST_FIRST_EXECUTION_014_RAW_CAPTURE_SOURCE_TEMPORAL_LAW_SURFACE_NEW_TEST_FAMILY`

Next queue row: `ACATQ-0005` / `ACABC-0005`.
