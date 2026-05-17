# FWD-007/008/010/013 test-first failure receipt

The four FWD test files were added before runtime/source mutation for this pass.

Pre-source-mutation command:

```bash
env PYTHONPATH=src python -m pytest \
  tests/tier_a/upstream_signal/test_fwd007_raw_signal_family_rebuild_contract.py \
  tests/tier_a/financial_calendar/test_fwd008_runtime_calendar_query_contract.py \
  tests/tier_a/config/test_fwd010_coefficient_calibration_contract.py \
  tests/tier_a/parallel_risk/test_fwd013_parallel_risk_candidate_enrichment_contract.py
```

Captured output: `proof/test_first_failure.txt`.

The failure occurred during test collection because the new native seams/symbols did not yet exist. This established the test-first gate before source mutation.
