# TEST_FALSE_POSITIVE_RESISTANCE_AUDIT_001 cache-clean receipt

## Scope
Generated cache artefacts were removed from the durable handoff source snapshot after validation runs and before packaging.

## Forbidden artefact classes
- `.pytest_cache/`
- `__pycache__/`
- `*.pyc`

## Evidence
- Before-clean path count: `352`.
- Before-clean path list: `var/audit/test_false_positive_resistance_001/final_closeout/cache_artifacts_before_clean.txt`.
- After-clean path count: `0`.
- After-clean path list: `var/audit/test_false_positive_resistance_001/final_closeout/cache_artifacts_after_clean.txt`.
- Final after-receipt-write path count: `0`.
- Final after-receipt-write path list: `var/audit/test_false_positive_resistance_001/final_closeout/cache_artifacts_after_final_receipt_write.txt`.

## Command basis
- `find . \( -path './.git' -o -path './.git/*' \) -prune -o -name '.pytest_cache' -type d -print -exec rm -rf {} +`
- `find . \( -path './.git' -o -path './.git/*' \) -prune -o -name '__pycache__' -type d -print -exec rm -rf {} +`
- `find . \( -path './.git' -o -path './.git/*' \) -prune -o -name '*.pyc' -type f -print -delete`

## Result
The handoff tree is clean of `.pytest_cache`, `__pycache__`, and `*.pyc` paths according to the recorded after-clean file-count proof.
