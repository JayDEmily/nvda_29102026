# ACTIVE_VALIDATOR_SIDE_EFFECT_OUTPUT_EXCLUSION_031 receipt

Date: 2026-05-12

## Scope

Repair the manifest/tool-output loop discovered during post-030 proof.

## Result

The 030 manifest no longer lists `var/audit/active_code_atlas_001/reports/validate_full_read_manifest_output.json`. `PLANS.md` section 7A now records that this validator side-effect output must not be included in the same manifest being validated, because the validator rewrites it during validation.

The 030 post-commit dual-manifest proof failure is retained as the evidence that triggered this repair; current closure proof validates the 031 manifest explicitly.

## Boundaries

- No runtime/source/test/refactor/dependency/vocabulary/original Atlas/Bridge/generated-slice mutation was opened.
- No `_archive/*.tar.gz` payload was restored or used.

## Proof

Final proof passed: git diff check no output; surface-record/registry validator PASS errors 0 warnings 0; proof-block check-all PASS count 46; selected current 031 manifest validation PASS with stale hash mismatches 0 and full_read_false 0.
