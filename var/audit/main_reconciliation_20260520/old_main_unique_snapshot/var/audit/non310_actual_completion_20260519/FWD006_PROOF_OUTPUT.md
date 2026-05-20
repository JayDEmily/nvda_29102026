# FWD-006 proof output

## Test-first failure

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd006.py -q
```

Result: expected failure before the native source module for FWD-006 existed. See `reports/FWD006_expected_failure.stdout` and `.status`.

## Targeted proof

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd006.py tests/tier_a/ingress/test_raw_bundle_loader_surface.py tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py -q
```

Result: passed. See `reports/FWD006_targeted.stdout` and `.status`.
