# FWD-011 proof output

## Test-first failure

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd011.py -q
```

Result: expected failure before the native source module for FWD-011 existed. See `reports/FWD011_expected_failure.stdout` and `.status`.

## Targeted proof

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/atlas_migration/test_non310_actual_completion_fwd011.py tests/tier_a/playbook -q
```

Result: passed. See `reports/FWD011_targeted.stdout` and `.status`.
