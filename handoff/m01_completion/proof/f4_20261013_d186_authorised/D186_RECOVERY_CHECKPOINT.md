# M01 Stage-1 F4 — D186 authorised recovery checkpoint

Date: 2026-10-13 (Australia/Melbourne).

## Authority and scope

The Programme Owner explicitly authorised the proposed D186 repair on 2026-10-13: reuse the existing K07 scalar extractor repertoire with flat immutable indexed `P_RULE` features, weights and scales; select the exact entry D155 occurrence by `EntryStateContextV1.d155_occurrence_id`; preserve the canonical similarity law and fail-closed lineage. The authority is restricted to D186. `GUARDRAILS.md`, `AGENTS.md`, active `EXEC_PLAN.md`, the accepted M01 brief and CSV remain unchanged.

Starting exact recovery proof/evidence HEAD: `2bb4831570d36c4b9199b0953840b142793f6aac` (RC08 ancestor `44875e9b98cace7a3337230fe9997bd355f7a6f1`). Production implementation checkpoint: `2fdbcaa37b34b1afb629601a3bb709c96ead67ee`.

## Meaning implemented

- `P_RULE` configuration requires indexed `similarity_feature:j = (D155 component Dxxx, K07 extractor, *extractor_arguments)`, `similarity_weight:j = Decimal`, `similarity_scale:j = Decimal`. Indices are contiguous canonical 1..N. Every declared feature must have exactly one weight and one scale; no undeclared field, implicit extractor, missing/duplicate feature, weight renormalisation, non-Decimal weight/scale, non-positive scale or non-unit weight sum is admitted.
- The D155 payload must have the complete accepted K16 component identity set with exact component ordering, stored component occurrence IDs and explicit units; entry/current component order, value types, units and outer structured-carrier identity must agree.
- The current state is the latest eligible D155 occurrence; the entry is the one exact earlier occurrence identified by the context. Missing, competing, future, same-as-current, cross-subject and incompatible entry/current pairs refuse. Unselected intermediate history does not contaminate the kernel's result input IDs.
- D186 computes `d² = Σ w_j*((current_j-entry_j)/s_j)²`, `similarity = exp(-0.5*d²)`, and the indexed raw/standardised deltas. K07's existing `extract_scalar` implements each explicit feature extraction; no implicit D155 flattening.
- The M01 public-owner D155 predecessor-history path selects both persisted entry and current occurrences for immediate derived predecessor IDs, inherited raw lineage, conventions and kernel inputs. The existing version-compatible history and no-look-ahead filters remain in force. Stage-2 D155 dependencies are not implemented or bypassed.

## Proof-first commit sequence

1. `a6292e2` — approved D186 flat/extractor/entry tests, committed RED (21 fails, one pass against prior code).
2. `863d7a5` — preserve runtime dispatch census with mandatory typed anchor.
3. `9464cdd` — formatting/closure of test proof.
4. `60d9fc3` — separate RED full-D155 schema-shape adversaries (two fails before source repair).
5. `0205f22`, `1891206` — complete lawful D155-carrier metadata in catalogue dispatch-only proof.
6. `2fdbcaa` — production change, strictly after tests.

## Current-run validation, exact scope

- `python -m pytest -q tests/product/derived_signal/test_m01_f4_cross_stage_d186_entry_anchor.py`: **24 passed** (`D186_FOCUSED_GREEN.log`).
- `python -m pytest -q tests/product --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`: **1,119 passed** (`PRODUCT_NON_PG_GREEN.log`). These tests deliberately exclude the unrelated M00 PostgreSQL durability test module; they do not replace it.
- `python -m pytest -q tests/architecture tests/bootstrap`: **74 passed** (`ARCH_BOOTSTRAP_GREEN.log`).
- `python -m mypy` scoped to changed production source modules: **no issues** (`MYPY_SCOPED_GREEN.log`).
- `ruff check` changed source and D186/dispatch tests: **all checks passed** (`RUFF_SCOPED_GREEN.log`).
- `ruff format --check` changed source and dedicated D186 test: **3 files formatted** (`RUFF_FORMAT_SCOPED_GREEN.log`). The inherited dispatch-census test file was not claimed to be globally Ruff-formatted.
- `git diff --check`: **no whitespace defects** (`GIT_DIFF_CHECK_GREEN.log`).
- Offline U05 bootstrap hash verification succeeded; PostgreSQL 17.9 on a local Unix socket returned `17.9|UTF8|on|on|on|` (`POSTGRES_RUNTIME_READBACK.log`).
- **NOT PASS — PostgreSQL durability:** initial full product suite without DSN: 1,119 passed and 55 setup errors (`PRODUCT_ALL.log`). A local-PostgreSQL full-suite attempt timed out after partial progress (`PRODUCT_ALL_WITH_POSTGRES.log`); a separately run PostgreSQL durability suite also timed out after partial progress. Neither timed-out run proves the remaining tests. The first isolated trial failed from a child-process `psycopg` environment path problem; a correctly bootstrapped isolated Python virtualenv was then supplied and the test progressed through 49 cases before timeout. None of these interruptions establishes a D186 product defect or full M00 durability acceptance.

## Unresolved and downstream boundary

This is **D186-only implementation and focused proof**, not full Stage-1 acceptance. D178 cost/edge-reserve unit conversion, D189 four-Greek currency-risk clipping and D192 typed risk-breach predicate retain separate unresolved programme/domain authority documented in `handoff/m01_completion/proof/f4_20261012_rc08_bounded/CONSOLIDATED_OWNER_CLARIFICATION_PROPOSAL.md` (C2–C4). All 30 cross-stage rows still require F4 row-level reconciliation and mandatory lawful public fail-closed evidence. The F4 row ledger's historical `NOT_READY` entries have not been silently promoted. No Stage-2 kernels or independent-review acceptance are claimed.

The immediate next decision, before further D178/D189/D192 implementation, is to obtain the exact C2–C4 semantics from the Programme Owner or an accepted normative clarification. Then continue F4, finish full Stage-1 proof and freeze a single independent-review candidate under the active ExecPlan.
