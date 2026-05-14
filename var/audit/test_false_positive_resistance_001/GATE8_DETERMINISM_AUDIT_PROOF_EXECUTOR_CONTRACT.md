# Gate 8 — Determinism audit: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY_LIMITED_REPEAT`

Repeated command under unchanged code:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py -q
```

Observed:

```text
repeat_1_status=0
repeat_2_status=0
repeat_3_status=0
```

Evidence logs:

- `logs/gate8_repeat_run_1.log`: `19 passed in 26.15s`.
- `logs/gate8_repeat_run_2.log`: `19 passed in 26.04s`.
- `logs/gate8_repeat_run_3.log`: `19 passed`.

Scope caveat: this is a limited three-run repeat for the selected family only. It does not prove broader suite determinism.
