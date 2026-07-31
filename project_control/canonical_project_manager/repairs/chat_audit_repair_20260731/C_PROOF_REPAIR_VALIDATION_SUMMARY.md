# M03/M05/M06 adversarial repair proof admission

## Authority

The repair law was admitted by commit `97ffc14` before production mutation. The attached M05 selected handoff was treated as non-authoritative input; only deterministic terminal-result identity was admitted. Its cumulative dependency, six-context and generated `not_evaluated` alternatives were dismissed in `REVIEW_AND_DISPOSITION.md`.

## Expected-red proof

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python3.13 -m pytest -q \
  tests/tier_a/m03_k05_k06/test_m03_k05_k06_contract.py \
  tests/tier_a/m05_k08_k09/test_m05_k08_k09_contract.py \
  tests/tier_a/m06_k10/test_m06_k10_contract.py
```

Result before source mutation:

- 87 existing cases passed;
- 12 newly admitted cases failed;
- no collection, import or harness failures remained.

The red cases are bounded to:

1. M03 degraded-source promotion;
2. M03 missing multi-source field-resolution evidence;
3. M03 resolution-receipt/payload disagreement;
4. M03 derivation-receipt/payload disagreement;
5. M05 unknown prepared-state acceptance;
6. M05 valid-context/gap contradiction;
7. M05 missing terminal failed-stage output;
8. M05 missing stable serial-result identity;
9. M05 forged serial-result identity;
10. M06 negative threshold acceptance;
11. M06 unsupported evaluator-policy version;
12. M06 unsupported aggregation version.

Production source remained unchanged during this proof admission.
