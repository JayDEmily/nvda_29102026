# FWD-004 proof output

## Test-first failure

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd004.py -q
```

Result: expected failure before source module existed. See `reports/FWD004_expected_failure.stdout` and `.status`.

## Targeted proof

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd004.py tests/tier_a/packets/test_reference_packet_carriage.py -q
```

Result: passed. See `reports/FWD004_targeted.stdout` and `.status`.
