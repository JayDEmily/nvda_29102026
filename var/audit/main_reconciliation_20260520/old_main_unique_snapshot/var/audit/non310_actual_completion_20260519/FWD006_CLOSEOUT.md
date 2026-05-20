# FWD-006 actual reopened-row closeout

Surface: FWD-006 — Raw capture and source temporal law

Rows in scope: 108

Final status counts:

- implemented_in_tests_and_code: 108
- already_satisfied_by_existing_tests_and_code: 0
- duplicate_or_subsumed: 0
- deferred_by_authority: 0
- rejected_out_of_scope: 0
- remaining_unsupported_worker_claim: 0

Implementation commit: ce9a7518358596f05895680010053b516bd0cc3d

Targeted proof command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd006.py tests/tier_a/ingress/test_raw_bundle_loader_surface.py tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py -q
```

Targeted proof result: passed; see reports/FWD006_targeted.stdout.
