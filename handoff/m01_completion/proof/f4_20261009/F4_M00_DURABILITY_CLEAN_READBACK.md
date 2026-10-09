# F4 M00 PostgreSQL durability — clean isolated tool-environment readback

Status: **55/55 passing test cases**, eight non-overlapping invocation groups; not a Stage-1 acceptance statement.

## Source and execution authority

- Test source: `tests/product/raw_signal/test_u05_postgresql_durability.py` (unchanged by F4).
- Collected exact test identifiers: `F4_M00_DURABILITY_COLLECTED_NODES.txt` (55 unique entries).
- PostgreSQL 17.9; DSN from the portable PostgreSQL proof bootstrap under `NVDA_TEST_POSTGRES_DSN`.
- Test Python: `Python 3.13.5`.
- Test tool: `pytest 9.0.3`; psycopg 3.3.4.
- Fresh virtualenv constructed using `python -m venv /mnt/data/f4_clean_py313`, then exact
  pinned pytest 9.0.3 and psycopg[binary] 3.3.4 from the user-supplied U05
  proof-wheelhouse with `pip install --no-index --find-links=...`.
- In this isolated venv, `importlib.util.find_spec('pydantic')` is `None`.
- To reproduce, run each group against the node identifiers in the collected
  file using `PYTHONPATH=.:src /mnt/data/f4_clean_py313/bin/python -m pytest -q
  <fully qualified test nodes for the group>`. Index numbers below are 1-based
  inclusive bounds into the checked-in collection list.

| Group | Cases | Observed outcome | Log |
|---|---:|---|---|
| 01–15 | 15 | 15 passed in 3.97 s | `F4_M00_CLEAN_DURABILITY_01_15.log` |
| 16–21 | 6 | 6 passed in 10.82 s | `F4_M00_CLEAN_DURABILITY_16_21.log` |
| 22–22 | 1 | 1 passed in 4.72 s | `F4_M00_CLEAN_DURABILITY_22_22.log` |
| 23–25 | 3 | 3 passed in 3.00 s | `F4_M00_CLEAN_DURABILITY_23_25.log` |
| 26–28 | 3 | 3 passed in 3.46 s | `F4_M00_CLEAN_DURABILITY_26_28.log` |
| 29–29 | 1 | 1 passed in 4.40 s | `F4_M00_CLEAN_DURABILITY_29_29.log` |
| 30–40 | 11 | 11 passed in 1.46 s | `F4_M00_CLEAN_DURABILITY_30_40.log` |
| 41–55 | 15 | 15 passed in 0.80 s | `F4_M00_CLEAN_DURABILITY_41_55.log` |

## Preserved first failure — environmental distinction

The initial durability 41–55 invocation under the ambient global interpreter
produced **14 passed, 1 failed**, in
`F4_M00_DURABILITY_41_55.log`. The single failure was the existing
`test_record_only_proxy_rewrite_rewrites_nested_public_storage_capabilities`:
`contains_target_capability` recursively traversed globally loaded objects
and raised `pydantic.errors.PydanticUserError` while calling `vars()` on
`pydantic._internal._mock_val_ser.MockValSer`. The unchanged test also failed
in isolated ambient runs (`F4_M00_DURABILITY_NESTED_ISOLATED_RERUN.log`) and
with external pytest plug-in autoload disabled
(`F4_M00_DURABILITY_NESTED_NO_PLUGIN_RERUN.log`). Correcting the globally
installed pytest from 9.0.2 to the repository-pin 9.0.3 did not itself remove
this failure (`F4_M00_DURABILITY_NESTED_PINNED_PYTEST_RERUN.log`).

The same unchanged test passed in the newly created, separately isolated
pinned virtualenv (`F4_M00_DURABILITY_NESTED_CLEAN_VENV.log`), followed by all
55 tests in eight groups, as recorded above. **Inference:** unrelated globally
installed Pydantic is implicated in the ambient test graph walk. This is not
proof of an M00 production defect; no tests were changed, skipped or weakened.

## Scope and exclusions

The full M01 applicable non-durability regression is separately recorded as
832 passing with native PostgreSQL 17.9 and distinct `f4_m00`/`f4_m01` roles:
`F4_RC01_RC14_832_PINNED_PYTEST_COMBINED_REGRESSION.log`.
Durability here is a bounded M00 PostgreSQL proof, not a substitute for the
outstanding Stage-1-closed public edges or 30 cross-stage kernel/refusal rows.
