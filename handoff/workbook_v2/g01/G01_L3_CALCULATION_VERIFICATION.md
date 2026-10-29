# G01-L3 — Focused mathematical public-path verification

**Disposition: COMPLETED BOUNDED TEST INVESTIGATION; THREE CONFIRMED RED PUBLIC-PATH WITNESSES; NO REPAIR.**

## Execution, environment and test evidence

- The original focused files `test_m01_f4_rc02_scalar_algebra_public.py`, `test_m01_f4_rc14_skew_from_native_delta_public.py`, `test_m01_f4_macro_vintage_public.py` ran together: **37 passed**. Those tests use a symmetric D025 fixture and R015-as-numeric-strike test inputs, so they do not prove raw source identity correctness.
- The *separately committed* authority-derived G01 tests ran through admitted M00 projection and M01 `create_owner(...).materialise(...)`: **3 failed**, intentionally left red. `D025` calculated **0.75 instead of 0.25**; `D099` and `D100` returned **None** when R015 carried C/P values. G01 tests were committed before their execution; original tests and production implementation were not touched.
- `PYTHONPATH=src python tools/validate_architecture.py`: PASS (0 dependency/public-seam violations, 6 architecture objects). `PYTHONPATH=src python tools/check_dependencies.py`: PASS. `PYTHONPATH=src python tools/check_public_seams.py`: PASS. Initial bare `python tools/...` attempts failed with `ModuleNotFoundError: nvda_desk`; corrected `PYTHONPATH=src` is the reproducible import environment. These checks do not demonstrate semantic correctness.
- Python 3.13.5, pytest 9.0.2. No PostgreSQL persistence test: `psycopg` was not available through this Python environment, and G01 changes no production persistence. No full original-M01 test suite or unrelated Stage-2 integration suite was run.
- Exact commands, exit codes and logfile SHA-256 identities are in `G01_L3_TEST_MANIFEST.json`; full pytest output is in `test_logs/`.

## Source and mathematical findings

1. **D025—CONFIRMED incorrect numeric result through public path.** With original raw High R039=120, Low R040=80, Last R037=90, expected position `(90-80)/(120-80)=0.25`; actual 0.75 due to reversed `R039/R040` meaning in `_stage1.py`. The symmetric midpoint legacy test is insufficient.
2. **D099 and D100—CONFIRMED source-native C/P refusal through public path.** R015 is option *right* C/P, not strike. Source code requires a Decimal strike under the same R015 identity. Controlled native C/P witnesses refuse while numeric-strike legacy fixtures passed. This evidence proves an incompatibility; it does not prove that a repaired join/source mapping is already available or accepted.
3. **D009—static implementation limitation, not independently exercised RED yet.** The accepted vintage categories are initial, latest-known-at-cutoff and revised. Current source branch produces only the first two. The existing tests pass without proving the third. Exact historical-vintage selection needs a bounded, authority-derived public-path proof; do not invent new selection inputs.
4. **D096—missing public predecessor (static inspection);** dependent D097, D098, D107 and D108 cannot be certified reached under the original Stage-1 public gate. This is not authority to implement Stage 2.

The distinct source/authority cases D117, D123 and D138 are recorded in `G01_L3_FINDINGS.csv`, without asserting a numerical defect where the production provider contract is unresolved. No production code, tests, schemas, calculation definitions, M00 interface, workbook or registry were altered.

**G01-L3 is an evidence-production leaf; it is not `M01-1` implementation acceptance.** Preserve the red proofs until the owner authorises the exact subsequent mathematical/source-contract repair scope.
