# FWD-009 reopened rows — proof output

Command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py`

Status: `0`

## stdout tail

```text
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/non310_reopen/MVD-A10_1704_V1
configfile: pyproject.toml
collected 9 items

tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py . [ 11%]
....                                                                     [ 55%]
tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py . [ 66%]
                                                                         [ 66%]
tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py . [ 77%]
..                                                                       [100%]

============================== 9 passed in 0.05s ===============================
```

## stderr tail

```text

```
