# M01 F4 worker internal checkpoint — authorised D134/D135 dependency correction

Date: 09-10-2026. This is **not** an F4 or Stage-1 acceptance candidate.
Authority: Programme-Owner D134/D135 R187 amendment (09-10-2026) overrides only the prohibition on the two specific normative edge changes and their necessary mechanical synchronisation. The accepted calculation mathematics, M00 ownership, GUARDRAILS, AGENTS, and Stage-2 prohibition remain unchanged.

## Proof-first sequence

- Base Git commit: `12e6598`. Historical three-field public-interface failing witness at `450b7e6` (preserved in immutable Git ancestry).
- New discriminating tests committed first at `b0faa71` before the production reconstruction repair. Original red results: `F4_POSITIONAL_CLASS_PROOF_FIRST_RED.log`.
- Subsequent production repair uses a single row-shifting mutation helper for the shared reconstruction and book final-state paths, plus D142's applicable positional state handling; insertion shifts higher rows, deletion shifts them down, and update targets an existing row; invalid required predecessor state is refused.
- D134/D135 authoritative and runtime catalogues now declare `R185;R187;R188;R190`; SHA256 `8045c8c0c4a62fbc3b88759a65b415efb1f0d549764ddbdcae2c5c911cd8a64a`. Units, definitions, kernel IDs and other normative fields remain unchanged.
- The retained D134/D135 witness keeps the original expected values, now supplies explicit `R187=insert` for its positive case. Its earlier three-field red state remains in Git ancestry and the new tests separately prove a missing operation fails closed.
- F1 corrected census: **174 Stage-1 rows**, **144 Stage-1-closed**, **30 cross-stage**, **490 declared edges** (two newly authorised R187 dependencies), plus D007 zero-edge sentinel. Historical 488/489 counts and original catalogue SHA are superseded *as current-state assertions* but retained in prior evidence.
- F4 ledger reconciles historical F2/F3 proof identities to the current 490-edge census, adds precisely D134/R187 and D135/R187, provisionally records bounded F4 proofs and leaves **309 Stage-1-closed edges** requiring additional evidence plus 107 Stage-2-deferred edges. Edge-level evidence is **not** identical to full public proof for every row.

## Exact environmental and verification boundary

- Restored offline Python 3.13 proof virtualenv and PostgreSQL 17.9 portable runtime from provided project archives, with separate M00 and M01 role/schema DSNs, not embedded M00 table reads from M01. Verified command transcripts/logs are in this folder.
- `PYTHONPATH=.:src python -m pytest -q tests/product tests/architecture tests/bootstrap tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py`: **743 passed**. See `F4_REPAIR_POSTGRESQL_COMBINED_743_PASS.log`.
- `PYTHONPATH=.:src python -m pytest -q tests/product/derived_signal/test_m01_f4_positional_book_class.py tests/product/derived_signal/test_m01_f4_depth_snapshot_authority.py`: **9 passed**.
- `PYTHONPATH=.:src python tools/validate_architecture.py`: **PASS**, zero dependency/public-seam violations.
- `python -m ruff check src tests tools`: **All checks passed**.
- `python -m mypy src`: **NOT PASS**, five pre-existing missing `types-PyYAML` stub errors, not observed type errors in modified source. `python -m mypy src --disable-error-code=import-untyped` yields **no issues in 21 source files**, but does not substitute for unmodified full typecheck.
- F1 readback and F4 ledger readback: exited 0 with new digest and counts.
- Separate `tests/product/raw_signal/test_u05_postgresql_durability.py`: one attempted invocation **interrupted by 140-second command timeout**; no fresh pass is claimed. F3 historical M00 durability evidence retained.

## Outstanding obligations and no-admission boundary

- Public end-to-end proof for all 144 Stage-1-closed rows, own-kernel plus lawful fail-closed public proof for all 30 cross-stage rows, and edge-class reconciliation of the remaining 309 Stage-1-closed edges are not completed.
- RC12 unresolved public rows recorded as D131, D137, D138, D141, D142 in current F4 readback. No implication of proven defects from these outstanding proof gaps.
- The repair used controlled positional provider operations consistent with the admitted semantics; it does not claim real native broker message trace conformance without provider-specific input authority evidence.
- Do not request routine independent review of this checkpoint; continue F4 under the existing ExecPlan. F4 and Stage 1 remain unaccepted; Stage 2 unauthorised.

## Follow-on same-session F4 evidence (supersedes earlier run counts and U05 non-run)

- Additional admitted M00 public tests of positional SMART/direct insertion, update and deletion at independent source venues (D143/D144); configured top-1/top-3 SMART depth and independent-instrument exclusion (D134/D135/D136). Correct numerical results and raw lineage are asserted.
- New readbacks: `F4_ROW_EVIDENCE_MATRIX.csv` (all 174 Stage-1 rows) and `F4_CLASS_PROOF_RECONCILIATION.csv` (each F1 relationship class). Their statuses strictly distinguish bounded edge-level evidence, 122 Stage-1-closed rows retaining 309 pending edges, and all 30 cross-stage kernel/refusal obligations. They do not promote a single additional row into acceptance.
- The separate **55-case** M00 PostgreSQL durability suite was re-executed on the same PostgreSQL 17.9 portable server with its required proof-administrator DSN (`NVDA_TEST_POSTGRES_DSN`), distinct from the non-durability M00/M01 role-isolation DSNs: **55 passed in 38.97 seconds** (`F4_M00_POSTGRESQL_DURABILITY_55_PASS.log`). This successful invocation supersedes earlier unsuccessful non-administrator/time-limited attempts, which remain evidenced in the session record.
- The expanded non-durability product/architecture/bootstrap/derived-implementation regression suite, same command and split M00/M01 DSNs as above, passed; authoritative exact count is in `F4_EXPANDED_PUBLIC_REGRESSION_746_PASS.log`. Expanded Ruff and structural architecture validation passed (`F4_EXPANDED_RUFF_PASS.log`, `F4_EXPANDED_ARCHITECTURE_PASS.log`). The full unmodified mypy environment issue remains unresolved and is **not** marked passing.
- F4 remains an **internal** recovery checkpoint; independently reviewed Stage-1/F4 acceptance is neither requested nor claimed.

## Further RC12 class examination

- D142's K08 kernel receives a discriminating shifted-level event sequence with two bid levels, insertion at the top, depletion/shock and recovery. Expected numeric values: pre-shock depth 25, shock depth 21, recovered depth 25, elapsed 1 second. Proven by `test_f4_k08_resilience_positional_insert_shifts_depth_before_shock`. This is **kernel-only** evidence and **does not close** D142's pending public-interface/lineage obligations.
- Expanded non-M00-durability suite now logs 747 passing cases (`F4_747_STAGE1_AND_ARCHITECTURE_POSTGRESQL_REGRESSION.log`). The independently rerun M00 PostgreSQL durability suite remains 55 passing tests, documented separately. Do not confuse the two independent runs or add their counts into a claimed single combined execution.

## RC12 follow-on proof-first checkpoint: D137 / D138

- `dc1540c`: independently committed public M00→M01 D137 microprice identity, contemporaneous book-size and raw-lineage proof; exact microprice `101.6`, missing and future values refused.
- `1aa17d7`: committed red public D138 book-slope proof before production. It demonstrated a defect: an incomplete price/size/side native book row was silently omitted by occurrence-ID intersection, allowing an illegitimate shortened regression.
- Bounded source implementation in `_eval_k06` now rejects incomplete native book rows and inconsistent instrument/source/side/invalid numerical payloads before fitting. Positive D138 OLS result is bid slope `12.5`, ask slope `12`, dependent upon public D011 midpoint with propagated lineage. The proof remains in `test_m01_f4_book_slope_public.py`.
- An intermediate full invocation with correct split-role DSNs failed one architecture test because of `mypy` name reuse in the initial repair (`F4_RC12_D138_TYPECHECK_RED_BEFORE_FINAL_REPAIR.log`: 750 passed, 1 failed). Production `row` and `rows` locals were renamed to avoid the cross-branch type conflict; a subsequent full split-role invocation succeeded: **751 passed** (`F4_RC12_D137_D138_EXPANDED_751_PASS.log`); Ruff and structural architecture checks also pass. An earlier invocation lacking required M00/M01 role DSNs yielded environment-related failures and is not claimed as a code regression or passing verification.
- F4 readback now accounts for `D137` and `D138` as bounded public evidence (not acceptance). Counts: 490 declared Stage-1 edges plus one zero-edge sentinel; **301** outstanding closed-stage edge proofs across **120** closed rows; all **30** cross-stage own-kernel/refusal obligations still open; unresolved RC12 public rows `D131`, `D141`, `D142`.
- The historical 309/122 and earlier test-run totals in this file are retained as timed checkpoints, not current status. Stage 1, F4 and Stage 2 acceptance status unchanged.

## Full RC12 selected-book public-evidence extension (10-10-2026)

- Public M00→M01 data and corresponding exact raw-lineage/temporal negative proofs added for **D141** (bid depletion 4, same-side/price restoration 3, score 3/4), **D142** (2-level reconstructed pre-shock 30, shock 22, first joint recovery 30 after 1 second), and **D131** (selected option-contract C1, exact D087 midpoint 100, shifted depth within +/-0.75 of midpoint 25; pre-insert historical result 18; C2 depth excluded). Tests are committed independently of this reconciliation at `7e232e2`, `19e0c8a` and `08ecde3` respectively. The D131 test independently uses the actual M00 public projection with native identity mapping, not the earlier hand-constructed selection fixture.
- The RC12 bounded public row witness register is now nonempty for every previously listed RC12 row; no RC12 public-row *enumeration gap* remains. This does **not** imply class-exhaustive acceptance, proof of real broker-native messages, or acceptance of all other Stage-1 relationships.
- The corrected F4 readback now counts **74 F4-bounded RC12/RC13 relationship records**, **280 Stage-1-closed relationship records without bounded public proof across 117 rows**, 107 Stage-2-deferred records and all 30 cross-stage kernel/refusal proof obligations. All 174 Stage-1 rows and the exact 490 dependency edge identities remain accounted for; the 1 sentinel remains distinct.
- The exact split-role PostgreSQL M00/M01 product/architecture/bootstrap/derived-implementation regression command passed **757 tests** in 9.49 s; log `F4_RC12_ALL_NATIVE_BOOK_PUBLIC_REGRESSION_757_PASS.log`. `python -m ruff check src tests tools`: PASS. `PYTHONPATH=.:src python tools/validate_architecture.py`: PASS (zero boundary violations). `python -m mypy src --disable-error-code=import-untyped`: PASS on 21 files; unmodified mypy still lacks installed YAML typing stubs and is not reported as passing. The separate PostgreSQL durability result remains the earlier verified **55 passed** (not rerun in this extension).
- Stage-1/F4 review candidate is **not ready**; the proof census still has 280 outstanding closed-stage edges and 30 cross-stage obligations. Continue F4 class-based proof and reconcile rather than submit incomplete candidate.
