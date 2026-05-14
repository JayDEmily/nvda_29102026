# Gate 2 — Baseline inventory only: proof_executor_contract

Status: `PASS_FOR_SELECTED_FAMILY`

Baseline command:

```bash
python -m pytest tests/tier_b/proof_model/test_proof_executor_contract.py -q
```

Result before amendment:

```text
14 passed in 15.85s
```

Recorded after amendment as selected-family baseline:

```text
19 passed in 25.93s
```

Evidence logs:

- `var/audit/test_false_positive_resistance_001/logs/gate6_selected_test_post_amendment.log`
- `var/audit/test_false_positive_resistance_001/logs/gate6_proof_block_check.log`
- `var/audit/test_false_positive_resistance_001/logs/gate6_proof_block_run.log`

Baseline result is inventory only. It does not prove the tests are reliable, and it does not prove current code correctness.
