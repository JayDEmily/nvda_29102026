# ACTIVE_HISTORICAL_STOP_WORDING_SUPERSESSION_004_RECEIPT

## Scope

Control/audit supersession note only. This pass does not rewrite historical evidence; it records that older pause/stop/fresh-authority wording is historical and superseded for live execution by the current continue-until-tokens authority and the updated root/plan control law.

## Changes

- Updated `ROADMAP_LEDGER.md` current pointer to `ACTIVE_HISTORICAL_STOP_WORDING_SUPERSESSION_004_RECORDED`.
- Added `ROADMAP_LEDGER.md` section `3A. Historical stop-wording supersession note`.
- Appended the `ACTIVE_HISTORICAL_STOP_WORDING_SUPERSESSION_004` ledger row.
- Created `var/audit/active_code_atlas_001/historical_stop_wording_supersession_004/reports/historical_stop_wording_scan.txt`.
- Created `var/audit/active_code_atlas_001/historical_stop_wording_supersession_004/reports/ACTIVE_HISTORICAL_STOP_WORDING_SUPERSESSION_004_REPORT.json`.
- Created this receipt and the dedicated full-read manifest.

## Historical wording found

The scan report captures historical lines containing phrases such as `planning_only_pause`, `paused per user instruction`, `fresh live authority required`, and `exhausted authorised scope`. These are preserved as point-in-time history and are not live stop authority for the current run.

## Boundaries

No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.
No `_archive/*.tar.gz` payload was restored or used.

## Proof result

```text
git diff --check: PASS (no output)
validate_surface_records_and_registry.py: PASS error_count=0 warning_count=0
scripts/run_proof_block.py --check-all: proof_blocks_check_all=PASS count=46
validate_full_read_manifest.py: PASS manifest_count=5 stale_hash_mismatch_count=0 full_read_false_count=0 for all five manifests
```

## Next action

Continue lawful control/audit/evidence/manifest/receipt/ledger hardening under `AGENTS.md` section 1A until context/token exhaustion, tool/runtime exhaustion that prevents further lawful progress, or explicit user stop instruction.
