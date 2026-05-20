# FWD-006 reopened rows — proof output

Command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/ingress/test_raw_bundle_loader_surface.py tests/tier_a/temporal`

Status: `0`

## stdout tail

```text
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/non310_reopen/MVD-A10_1704_V1
configfile: pyproject.toml
collected 10 items

tests/tier_a/ingress/test_raw_bundle_loader_surface.py ...               [ 30%]
tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py ... [ 60%]
                                                                         [ 60%]
tests/tier_a/temporal/test_source_temporal_standard_surface.py ....      [100%]

============================== 10 passed in 0.18s ==============================
```

## stderr tail

```text

```
