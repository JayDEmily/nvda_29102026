# FWD-001 test-first failure receipt

Command run after adding the strict top-level JSON helper test and before source implementation:

```bash
python -m pytest tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py -q
```

Observed result:

```text
1 failed, 8 passed in 0.40s
FAILED tests/tier_a/vocabulary/test_vocabulary_json_helper_contracts.py::test_from_json_text_rejects_unknown_top_level_fields - Failed: DID NOT RAISE <class 'ValueError'>
```

The failure matched the intended missing delta: top-level unknown fields were silently accepted before the parser was tightened.
