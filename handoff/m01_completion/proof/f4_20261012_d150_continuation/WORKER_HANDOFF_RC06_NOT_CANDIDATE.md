# M01 F4 — RC06 D150 bounded proof, D104 authority hold

Date: 2026-10-12 (Australia/Melbourne)
Status: **F4 INCOMPLETE / NOT STAGE-1 REVIEW CANDIDATE**
Incoming state: `c2d640cc6f7496b4edd8bb4f314f825d885a5cf2` (RC05).
Branch: `work/m01-f4-authorised-reconstruction-20261011`.

## Authorised, independent work completed

- Read root `GUARDRAILS.md`, `AGENTS.md`, `EXEC_PLAN.md`, and the authoritative M01 brief/catalogue. No governing/normative files or production source were modified.
- D150 is K07/P_SCORE with exactly six declared predecessors: `D070;D146;D147;D148;D149;D048`. F1 class `RC21`. The existing M01 recursion supports independent immutable `P_SCORE` definitions per nested calculation and exact raw/correlated source histories.
- Added controlled M00-to-M01 public test `tests/product/derived_signal/test_m01_f4_d150_composite_public.py`. Separate first Git commit was RED for D150 positive materialisation (its inherited fixture lacked D052/D053 five-minute comparison profiles); a second test-only commit supplied those versioned P_WINDOW references. **No production repair was necessary.** A passing test result alone was not assumed to prove a live-data source.
- Public tests establish six persisted direct predecessor occurrence references, independent expected scalar `195.8972630820587276330172811` (within Decimal precision tolerance), 51 exact ultimately contributing raw lineage entries, deterministic repeat result, per-parent missing-input refusal, distinct native release actual/consensus history, knowledge cutoff, mapping-version incompatibility, wrong subject and future-input refusal. Controlled observations are not represented as provider integration.
- Rebuilt the authoritative 491-edge reconciliation (plus one sentinel). Six D150 edges changed from outstanding to bounded public row proof; D104's two edges remain outstanding. All 30 cross-stage Stage-1 own-kernel/refusal obligations remain outstanding. The updated ledger is still not Stage-1 acceptance.

## Known unresolved authority — D104

Sources: accepted brief `handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md` §5 K03 D104; catalogue row D104. The calculation requires D099 25-delta skew and D100 10-delta skew but supplies no authorised scalar combination/family-selection rule. Existing production concatenates histories and permits cross-family pairing.

The retained adverse witness `tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py` demonstrates 25-delta skew 10→20 and 10-delta skew 30→40 (both family-consistent changes +10), but the current kernel emits **−10** by crossing families. The test remains intentionally failing. **No D104 implementation/normative repair was made.**

Required Programme Owner rule: exactly how the two corresponding family changes combine into D104's one vol-point result (or which explicitly versioned family is selected), and whether both D099/D100 are always mandatory. This cannot be guessed from chronology, the catalogue or the accepted brief.

## Exact validation and limitations

- `python -m pytest -q tests/product/derived_signal/test_m01_f4_d150_composite_public.py` — **14 passed** (controlled public in-memory owner seam).
- `python -m pytest -q tests/architecture tests/bootstrap tests/product tests/implementation/derived_signal --ignore=tests/product/raw_signal/test_u05_postgresql_durability.py --ignore=tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py` with independent M00/M01 PostgreSQL role DSNs and isolated Python/PyYAML path — **1,169 passed**. Exclusions are material; this is not a whole-suite PASS. See `BROADER_EXCLUDING_D104_RED_AND_M00_DURABILITY.log`.
- `python -m pytest -q tests/product/derived_signal/test_m01_f4_d104_skew_family_collision_red.py` — **1 failed** as required by the still-open authority/implementation defect. See `D104_AUTHORITY_RED.log`.
- M00 durability `test_u05_postgresql_durability.py`: this session's whole-suite rerun was **interrupted after 29 test progress marks** by the execution timeout; no complete PASS. See `M00_DURABILITY.log`. An earlier 55/55 pass in historical evidence is not substituted for current verification.
- Scoped Ruff check of D150 test and derived source — passed. Scoped Ruff formatting of new D150 test — passed. Ruff lint of the updated ledger generator — passed. Ruff format of the full generator has inherited formatting debt, and full repository formatting is not claimed.
- Derived-source Mypy: `Success: no issues found in 5 source files`.
- Authoritative F4 ledger regeneration executed successfully after conservatively updating the six D150 dispositions and the exact counts. See `F4_RECONCILIATION.log`.
- D150 does **not** establish live international/macro provider integration or a real-provider release-family mapping. Raw samples are controlled, versioned fixtures.

## Stop boundary

Stage 1 remains **unaccepted**. Stage 2 remains **unauthorised**. The only closed-stage edges still open are D104's two; 30 cross-stage rows still need own-kernel and lawful public refusal proofs. Do not send this checkpoint as a Stage-1/F4 final independent-acceptance candidate. Preserve Git history; no squash, force reset, or implicit re-admission of reconstructed commits.
