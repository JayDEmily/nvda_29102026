# ACTIVE_PROOF_OUTPUT_TRANSCRIPT_SCOPE_ALIGNMENT_018 receipt

Date: 2026-05-12

## Scope

Aligned diagnostic hygiene scan scope so prior proof-output transcripts are point-in-time evidence, not live proof status, unless explicitly selected for audit.

## Triggering evidence

A scoped current-chain scan after `ACTIVE_SCAN_SCOPE_HYGIENE_ALIGNMENT_017` still found `var/audit/active_code_atlas_001/proof_placeholder_closure_013/reports/ACTIVE_PROOF_PLACEHOLDER_CLOSURE_013_PROOF.txt`, which preserves a point-in-time expected manifest-validation failure from before later supersession. Later current reports and manifests record the validator-passing current state.

## Updated control rule

`PLANS.md` section 8A now excludes prior proof-output transcripts from default live-control hygiene scans unless a selected leaf explicitly audits them. A prior transcript may preserve expected failure text; later validator-passing manifests/reports are the current proof status.

## Boundaries

- No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.
- No `_archive/*.tar.gz` payload was restored or used.

## Proof

Final proof passed: git diff check no output; surface-record/registry validator PASS errors 0 warnings 0; proof-block check-all PASS count 46; selected current manifest validation PASS with 19 manifests, stale hash mismatches 0, full_read_false 0.
