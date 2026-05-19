
## Test-first FWD-006 row proof
Tue May 19 08:59:39 UTC 2026
```
env PYTHONPATH=src python3 -m pytest tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/fwd006_exec/MVD-A10_1704_V1
configfile: pyproject.toml
plugins: json-report-1.5.0, ddtrace-4.4.0, asyncio-1.3.0, Faker-40.1.2, cov-7.0.0, anyio-4.13.0, metadata-3.1.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 108 items

tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py . [  0%]
........................................................................ [ 67%]
...................................                                      [100%]

============================= 108 passed in 0.56s ==============================
exit_status=0
```

## Targeted FWD-006 accepted-audit proof
Tue May 19 08:59:44 UTC 2026
```
env PYTHONPATH=src python3 -m pytest tests/tier_a/ingress/test_raw_bundle_loader_surface.py tests/tier_a/temporal
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.0.2, pluggy-1.6.0
rootdir: /mnt/data/fwd006_exec/MVD-A10_1704_V1
configfile: pyproject.toml
plugins: json-report-1.5.0, ddtrace-4.4.0, asyncio-1.3.0, Faker-40.1.2, cov-7.0.0, anyio-4.13.0, metadata-3.1.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 118 items

tests/tier_a/ingress/test_raw_bundle_loader_surface.py ...               [  2%]
tests/tier_a/temporal/test_fwd006_reopened_row_raw_capture_source_temporal_proof.py . [  3%]
........................................................................ [ 64%]
...................................                                      [ 94%]
tests/tier_a/temporal/test_raw_capture_transform_boundary_surface.py ... [ 96%]
                                                                         [ 96%]
tests/tier_a/temporal/test_source_temporal_standard_surface.py ....      [100%]

============================= 118 passed in 0.61s ==============================
exit_status=0
```

## git diff check
Tue May 19 08:59:48 UTC 2026
```
git diff --check
exit_status=0
```

## scaffold check
Tue May 19 08:59:49 UTC 2026
```
make scaffold-check
repo scaffold present
exit_status=0
```

## proof block check all
Tue May 19 08:59:49 UTC 2026
```
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/run_proof_block.py --check-all
proof_blocks_check_all=PASS count=51
exit_status=0
```
