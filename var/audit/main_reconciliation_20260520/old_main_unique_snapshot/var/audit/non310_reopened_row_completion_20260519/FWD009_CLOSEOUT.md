# FWD-009 reopened rows — closeout

Decision: `closed_reopened_rows_existing_native_test_and_code`.

Rows completed: `49`.
Rows deferred: `0`.
Rows rejected: `0`.
Remaining open rows: `0`.

Targeted proof command: `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/tier_a/upstream_cognition/test_prepared_runtime_substrate_surface.py tests/tier_a/upstream_cognition/test_prepared_runtime_snapshot_contract_surface.py tests/tier_a/upstream_cognition/test_prepared_runtime_transform_boundary_surface.py`
Targeted proof status: `0`

No source/test/config mutation was required or performed.
