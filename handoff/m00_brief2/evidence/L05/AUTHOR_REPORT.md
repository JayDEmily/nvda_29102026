# L05 author implementation and evidence — independent review pending

**Status: AUTHOR CANDIDATE; NOT INDEPENDENTLY ACCEPTED.** No claim of accepted L05, full M00 completion, PostgreSQL runtime, live IBKR, CPython 3.12.14 runtime proof, or L06 review. The user explicitly requested an author attempt without independent review.

## Authority and unchanged contract

Read entire root `GUARDRAILS.md` (165 lines), `AGENTS.md` (88 lines), `EXEC_PLAN.md` (180 lines at ingress), applicable `tests/AGENTS.override.md` (22 lines), original 282-line Brief 2 V3, existing `tools/m00_fixture_io.py`, L02/L03/L04 tests and oracle fixtures. Existing source contract and production modules are unchanged. No modifications to original oracle, controls, negative fixtures, mapping/schema, product tests, previously admitted proof generations or accepted L00–L04 evidence.

## Source and composition

- Parent accepted L04 checkpoint `b05577a3a87b3bc23279075ef052125b9cab8ab1`.
- L05 implementation commit `080dcdd2c364c34ddb1502e2d5b8c41b9ef93fa7` (only new `tools/export_m00_synthetic.py`).
- All reported execution results below use a clean clone of that exact code commit, not unpublished source edits.
- New tool CLI requires `--fixtures DIR --expected DIR --database ABSENT_ABSOLUTE_PATH --output NEW_DIR`. It refuses overwrite, checks admitted immutable file hashes before admission, executes 36 supplied raw observations and five controls via actual M00 commands into SQLite, closes the writer, and performs observation, projection, control discovery, paginated history and absence reads using a *separate process* with the existing public API. All 196 exported rows are validated against the existing L01 JSON output schema. The expected oracle is used only for comparisons and history query role selection, never for constructing actual values.
- Four positive actual-absence public probes cover receipt-only event-time cutoff, native `error(317)`/`error(316)` not becoming R187, and a field-inapplicable R193 absence. The other N01–N18 outcome file references already admitted specific L02/L03/L04 evidence; these negatives are **not rerun by the exporter** and have no invented new PASS claim.

## Observed author-side execution

- Runtime in this container: **CPython 3.13.5**, SQLite **3.46.1**; repository requires **CPython 3.12.14**, previous project environment recorded SQLite **3.53.1**, and pinned tools are not all present. `uv python list --only-installed` reports only 3.13.5 and `uv python install 3.12.14 --offline` returns `No download found`. Online attempt also returned `No download found`. Hence exact pinned environment compliance is **BLOCKED** here. Both successful author-side comparisons return **exit 2 intentionally**, not acceptance.
- Clean clone replay one: 36 observation records, 155 projection records, five separate control records, all per-scenario counts match; exact canonical row mismatch **null**; all **54** public page-exhausted history comparisons equal oracle (155 selected rows in total); four public absence probes match; independently reopened SQLite database file hash unchanged.
- Clean clone replay two: fresh SQLite DB and new output directory, same clean source SHA. Actual JSONL SHA-256 in both: `aac23b90ff1cb16b9ea5434ae2ac3115a53eb6cd60fbfadb39d9db2db63ec4b5`. Control output SHA-256: `5b808cd12cbe566aa26e41c11935cb3efce5f6258299925cb14ed97739267501`. Both runs have `source_clean_at_start=true`, no mismatch, identical per-scenario/history/absence results.
- The scoped `python -m pytest -q tests/product/m00_brief2/` run was attempted on unpinned CPython3.13 and timed out after displaying seven progress dots; no completed result was obtained or treated as proof. `python -m py_compile tools/export_m00_synthetic.py` passed, but this is Python 3.13 static compilation and **not** equivalent to the repository's pinned mypy/Ruff or admitted strict proof engine.
- The previous L00–L04 independent reviewer dispositions are carried forward historically without change, not re-reviewed here.

## First unmet acceptance invariant and handoff

Required L05 independent export/semantic review **NOT PERFORMED**, as explicitly instructed by the owner. Required pinned Python 3.12.14 rerun **NOT PERFORMED / BLOCKED** by absent interpreter. Exact production/proof runner strict invocation **NOT PERFORMED** in this session; unaffected L02–L04 accepted proofs reused without repeating all tests. L05 remains open; L06 remains untouched and pending. `ACTUAL_M00_OUTPUT_VERIFIED` and `SQLITE_READBACK_VERIFIED` are **not formally accepted** in this branch despite provisional author-side public evidence. Checkpoint integrity is independent of semantic acceptance.

Additional fail-closed check: mutated a *copy* of the immutable expected oracle; CLI returned 2 before creating any SQLite DB, retained structured `FAILED_EXPORT` and exact hash-mismatch detail. Original oracle unchanged.
