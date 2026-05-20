# FWD-011 reopened rows — proof output

Command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/playbook tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py`

Status: `0`

## stdout tail

```text
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/non310_reopen/MVD-A10_1704_V1
configfile: pyproject.toml
collected 70 items

tests/tier_a/playbook/test_playbook_eligibility_registry_surface.py .... [  5%]
                                                                         [  5%]
tests/tier_a/playbook/test_playbook_library_architecture_surface.py .... [ 11%]
............                                                             [ 28%]
tests/tier_a/playbook/test_playbook_transform_boundary_surface.py ...... [ 37%]
..........................................                               [ 97%]
tests/tier_b/serial_boundaries/test_playbook_eligibility_decontamination.py . [ 98%]
.                                                                        [100%]

============================== 70 passed in 0.42s ==============================
```

## stderr tail

```text

```
