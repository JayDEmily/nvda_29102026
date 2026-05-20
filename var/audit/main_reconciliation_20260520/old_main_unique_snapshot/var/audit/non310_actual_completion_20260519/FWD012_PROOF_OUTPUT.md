# FWD-012 proof output

## Test-first failure

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd012.py -q
```

Result: expected failure before the native source module for FWD-012 existed. See `reports/FWD012_expected_failure.stdout` and `.status`.

## Targeted proof

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd012.py tests/tier_a/runtime/test_serial_stage_packet_emission_surface.py tests/tier_a/serial_recommendation tests/tier_b/serial_boundaries -q
```

Result: passed. See `reports/FWD012_targeted.stdout` and `.status`.
