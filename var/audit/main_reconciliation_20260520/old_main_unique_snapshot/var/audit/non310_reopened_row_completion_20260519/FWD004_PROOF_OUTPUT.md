# FWD-004 reopened rows — proof output

Command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/packets`

Status: `0`

## stdout tail

```text
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/non310_reopen/MVD-A10_1704_V1
configfile: pyproject.toml
collected 12 items

tests/tier_a/packets/test_dmpv3_extension_canonical_leaf_surface.py ...  [ 25%]
tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py ...        [ 50%]
tests/tier_a/packets/test_reference_packet_carriage.py ......            [100%]

============================== 12 passed in 0.17s ==============================
```

## stderr tail

```text

```
