# ACTIVE_SCAN_CLASSIFICATION_ARTEFACT_SCOPE_ALIGNMENT_019 receipt

Date: 2026-05-12

## Scope

Aligned diagnostic hygiene scan scope so prior scan-classification reports and receipts are treated as point-in-time scan evidence, not fresh live-control hits, unless explicitly selected for audit.

## Triggering evidence

The scoped scan after `ACTIVE_PROOF_OUTPUT_TRANSCRIPT_SCOPE_ALIGNMENT_018` still included prior scan-classification reports that quote historical hits. That preserves audit evidence but pollutes current live-control defect discovery.

## Updated control rule

`PLANS.md` section 8A now says prior scan-output artefacts include raw scan text plus scan-classification reports/receipts. Default live-control hygiene scans exclude those artefacts unless a selected leaf explicitly audits them.

## Boundaries

- No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.
- No `_archive/*.tar.gz` payload was restored or used.

## Proof

Final proof passed: git diff check no output; surface-record/registry validator PASS errors 0 warnings 0; proof-block check-all PASS count 46; selected current manifest validation PASS with 20 manifests, stale hash mismatches 0, full_read_false 0.
