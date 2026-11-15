# Exact host SQLite observation — bounded qualification evidence

**Status:** NON_PRODUCT_MECHANISM_EVIDENCE / PRODUCT_RUNNER_NOT_QUALIFIED.

Source inspection: `src/nvda_desk/market_measurement_truth/_record_store.py` uses STRICT tables, immutability triggers, `PRAGMA foreign_keys`, `busy_timeout`, `synchronous=EXTRA`, begin-immediate and durable reopen. M02 `_sqlite.py` and M00 `_sqlite.py` additionally enforce `journal_mode=DELETE`, application/user version, integrity and read-only checks. These are concrete mechanisms to investigate, not an assertion of all SQLite features the final D091 path may require.

**Observed selected Ubuntu candidate** via `/home/jds/nvda_uv3135_20261112/.venv/bin/python`:

- Python 3.13.5; resolved binary `/home/jds/nvda_uv3135_20261112/.uvpython/cpython-3.13.5-linux-x86_64-gnu/bin/python3.13`, SHA256 `0eba26d5f04a3673ee264ca406ef286d5025da098c1a24987a8118c23d69153c`.
- SQLite 3.49.1, source ID `2025-02-18 13:38:58 873d4e274b4988d260ba8354a9718324a1c26187a4ab4c1cc0227c03d0f10e70`; no explicit `LD_LIBRARY_PATH`. Do not label this a 3.54.1 runner.
- New *disposable non-product* SQLite 3.49.1 evidence: all nine targeted mechanisms observed as TRUE (STRICT table, immutable trigger refuses UPDATE, foreign keys enabled and FK refusal, DELETE journal, synchronous EXTRA, busy_timeout zero, integrity check and read-only durable reopen). Source report `SQLITE_3491_NONPRODUCT_MECHANISM_RECEIPT.json`. No project-product import/test, accepted SQLite source/generation substitution, or system installation.
- Earlier historical non-product SQLite 3.54.1 build at `/workspace` has independently reproduced byte-identical library SHA256 `c53706980906943301153b630aeddba1b4aab6fe5eeda5752d8293952707db4e` **in that separate environment** (see `handoff/astra_adr_continuation_20261115/SQLITE_3541_BUILD_AND_PROBE.json`). It is not this Ubuntu process, and runtime-equivalence/ABI is not established.

**Next qualified-runner gate:** independently bind the actual source/claim/runner path under its correct Python/dependency lock and chosen SQLite loaded source ID, compatible schema/transaction/codec requirements, selected proof nodes and independent Tester receiver. A focused compatibility disposition is required; nine mechanisms are necessary evidence for those nine checks, not a full replacement for the historic 3.54.1/3.53.1 proof.

No D091 source, test case, claim, generation, pointer, or test ledger was changed.
