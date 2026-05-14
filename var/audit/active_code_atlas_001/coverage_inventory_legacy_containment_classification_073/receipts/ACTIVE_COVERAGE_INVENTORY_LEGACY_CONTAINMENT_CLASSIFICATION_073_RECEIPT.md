# ACTIVE_COVERAGE_INVENTORY_LEGACY_CONTAINMENT_CLASSIFICATION_073_RECEIPT

## Scope

Current user authority opened code inspection and update for the failing `tier_a_remaining_coverage_inventory` result, plus downloadable package creation.

## Finding

The discretionary remaining coverage inventory failed because `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py` treated raw text occurrences of `legacy_import` as imported-module containment violations. The failing paths were transform-boundary tests that intentionally mention donor roots while proving non-import/transform boundaries.

## Change

Repaired `tests/tier_a/legacy_imported/test_imported_module_containment_surface.py` so imported-module containment is classified by AST import statements for `legacy_import` and `nvda_desk.legacy.imported`, not raw string presence. Added `test_transform_boundary_guard_strings_are_not_imported_legacy_modules` to preserve the distinction: transform-boundary tests may name donor roots as guard-string evidence but must not import them.

Updated `NVDA10_CURRENT_STATE_ARCHITECTURE_MAP.md` row 5.17 and `ROADMAP_LEDGER.md` with the 073 current pointer/history.

## Proof summary

- Red proof reproduced: `PYTHONPATH=src python scripts/run_proof_block.py --block tier_a_remaining_coverage_inventory` returned status 1 with 1 failed and 51 passed.
- Targeted containment proof: `python -m pytest tests/tier_a/legacy_imported/test_imported_module_containment_surface.py -q` returned status 0 with 3 passed.
- Remaining coverage inventory: `PYTHONPATH=src python scripts/run_proof_block.py --block tier_a_remaining_coverage_inventory` returned status 0 with 53 passed.
- `git diff --check` returned status 0.
- `python var/audit/active_code_atlas_001/tools/validate_surface_records_and_registry.py` returned status 0.
- `PYTHONPATH=src python scripts/run_proof_block.py --check-all` returned status 0 with `proof_blocks_check_all=PASS count=46`.

## Boundaries

`PLANS.md` remained frozen. No dependency, vocabulary, original Atlas/Bridge, generated-slice, runtime trading, new broker order placement, broker execution, capital deployment, exit/close, strategy-decision, or unrelated implementation mutation was opened.

## Next state

Stop for the explicit current user tarball/output request. Fresh authority is required before opening dynamic-import/string-execution policy hardening or any separate architecture surface.
