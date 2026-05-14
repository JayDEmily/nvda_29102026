# ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_043_RECEIPT

Date: 2026-05-13

## Scope

Check the live pointer and 042 artefact integrity after the post-041 leaf-stop-point scan/classification pass.

## Result

The expected 042 scan, report, receipt, and full-read manifest artefacts were present before moving the live pointer to `ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_043_RECORDED`.

`AGENTS.md` and `PLANS.md` remained frozen.

## Boundaries

No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice boundary was opened.

No `_archive/*.tar.gz` payload was restored or used.

## Evidence

- Report: `var/audit/active_code_atlas_001/current_pointer_integrity_scan_043/reports/ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_043_REPORT.json`
- Full-read manifest: `var/audit/active_code_atlas_001/full_read_manifests/ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_043_FULL_READ_MANIFEST.json`
- Prior 042 report: `var/audit/active_code_atlas_001/post_041_leaf_stop_point_scan_classification_042/reports/ACTIVE_POST_041_LEAF_STOP_POINT_SCAN_CLASSIFICATION_042_REPORT.json`
- Prior 042 receipt: `var/audit/active_code_atlas_001/post_041_leaf_stop_point_scan_classification_042/receipts/ACTIVE_POST_041_LEAF_STOP_POINT_SCAN_CLASSIFICATION_042_RECEIPT.md`

## Proof commands

Recorded in `var/audit/active_code_atlas_001/current_pointer_integrity_scan_043/reports/ACTIVE_CURRENT_POINTER_INTEGRITY_SCAN_043_PROOF_STDOUT.txt`.

## Next

Continue immediately to the next lawful control/audit/evidence/manifest/receipt/ledger hardening leaf. Leaf completion is not a stop point.

## Observed proof result

All five recorded commands exited `0`. The selected-manifest validation reported `PASS`, `error_count=0`, `warning_count=0`, `stale_hash_mismatch_count=0`, and `full_read_false_count=0`.
