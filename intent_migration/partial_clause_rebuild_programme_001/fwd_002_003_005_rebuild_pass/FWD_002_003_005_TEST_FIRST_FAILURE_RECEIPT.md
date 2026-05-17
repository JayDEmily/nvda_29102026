# FWD-002/FWD-003/FWD-005 test-first failure receipt

Status: `recorded_from_pre_source_mutation_run`

Before implementation, the new Tier A contract tests were run and failed during collection because the required native seams did not exist yet.

Command:

```bash
PYTHONPATH=src pytest -q tests/tier_a/testing_proof/test_fwd002_replay_harness_contract.py tests/tier_a/testing_proof/test_fwd002_fixture_and_sidecar_contract.py tests/tier_a/persistence/test_fwd003_import_registry_contract.py tests/tier_a/persistence/test_fwd003_durable_sql_contract.py tests/tier_a/api/test_fwd005_api_exposure_contract.py
```

Observed failing import/symbol obligations:

- `nvda_desk.analysis.replay.walk_forward` missing.
- `nvda_desk.analysis.replay.sidecar` missing.
- `nvda_desk.persistence.import_registry` missing.
- `nvda_desk.persistence.durable_sql` missing.
- `get_events_service` missing from `nvda_desk.api.deps`.

The temporary `tests/tier_a/testing_proof/` paths were then moved into existing Tier A families before final proof registration:

- `tests/tier_a/analysis/test_fwd002_replay_harness_contract.py`
- `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py`
