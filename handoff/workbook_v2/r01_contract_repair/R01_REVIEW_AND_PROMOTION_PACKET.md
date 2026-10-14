# R01 — exact reviewer candidate (not independent acceptance)

**Date:** 14 October 2026, Australia/Melbourne.
**Work branch:** `work/v2-contract-repair-authority-20261014`.
**Source implementation commit:** `27aa7cb8f127f7cded3b4a4b8f1fa45e9744b6ab` (tree `5e171151410208dccd0ee0e35a543ad53f18400c`).
**Proof-first commit:** `c3c17c2` (before any R01 production correction).
**Parent handoff:** `f7c81bb0d88d0b2cf1980af06e80c8834143c7d7`.
**Binding:** `IMPLEMENTATION_INGRESS.yaml`; underlying previously accepted exact M01 source brief SHA-256 `603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c` targeting `modify:M01`.

## Scope and propositions

1. D025 canonical R039 High, R040 Low, R037 Last, proof `(90−80)/(120−80) = 0.25` through M00 projection and public M01 owner. Minimal swap of code's R field selection only; no change in accepted mathematics.
2. D099/D100 canonical R015 right C/P, R111 model IV, R112 native delta; expiry/contract/strike selection metadata must align, strict same-source and same-contract joins remain. Numeric strikes masquerading as R015 and categorical disagreement with contract identity refuse. Expected IV spreads 10 and 30 volatility points.
3. Existing historical RC14, D104 integration and skew kernel tests had invalid numeric-strike R015 fixtures. Their values were corrected to native C/P; their independently expected calculation results and refusal assertions were not weakened. D120 tests/implementation remain untouched pending normative source-contract amendment.

## Executed tests and original failure preserved

All logs/exit statuses are in `proof_logs/`. Commands executed from repository root under Python 3.13 and `PYTHONPATH=src`:

- Before production: `python -m pytest -q handoff/workbook_v2/g01/proofs/test_g01_public_authority_witnesses.py tests/product/derived_signal/test_m01_f4_rc14_skew_from_native_delta_public.py tests/product/derived_signal/test_m01_f4_rc02_scalar_algebra_public.py`; **34 passed / 7 failed**, exit 1, committed in `c3c17c2`.
- After production same focused command: **41 passed**, exit 0.
- Broader `python -m pytest -q tests/product/derived_signal`: first **778 passed / 2 failed**, because D104 and skew kernel historic fixtures still used numerical R015; after correcting those two sources: **780 passed**, exit 0.
- `PYTHONPATH=src python tools/validate_architecture.py`: exit 0.
- `PYTHONPATH=src python tools/check_dependencies.py`: exit 0.
- `PYTHONPATH=src python tools/check_public_seams.py`: exit 0.
- `PYTHONPATH=src python tools/validate_implementation_authority.py --binding handoff/workbook_v2/r01_contract_repair/IMPLEMENTATION_INGRESS.yaml --brief handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md`: exit 0, resolved `modify:M01`.
- `ruff` lint not run: module not installed in this environment. PostgreSQL/live IBKR validation not performed and is not required to prove controlled-input mathematical corrections.

These results establish tested corrections in the identified path, **not** fresh independent semantic acceptance or total M01 completion. No actual live IBKR provider observations are asserted.

## Separate unresolved source-contract and original G01 status

- **D120 authority decision remains blocked.** Accepted normative equation uses `multiplier` but direct raw list omits R016; R015 is option right C/P and may not be repurposed. Proposed amendment: add R016 as an explicit D120 raw dependency, preserve R015 for option right, specify exact per-contract native occurrence selection, versioning and lineage, then commit contract-correct red proof *before* D120 source repair. Cannot infer owner approval merely from this packet.
- Original V2 **G01 remains PARTIAL/BLOCKED**. Its 114 M01-1 candidate population and 65 measurement-convention reviews are not admitted by these local repairs.
- **Independent review is outstanding.** Author has run proof and checks but is not a different reviewer. Reviewer should challenge native raw field identity, mismatch-refusal tests, D104 history/join cases, negative aliases, source/units lineage, and limits of the environment.
- **Main promotion is blocked.** Local Git has no `refs/heads/main`, no `refs/remotes/origin/main`; configured origin points to an unavailable local source. A separately connected GitHub repository identifies `main` at `892a6c042f19d19d84a3d1fb2c639033789f9bc1`, which is absent from this Git object database. `git merge-base --is-ancestor 892a6c... HEAD` exited 128 due to missing commit. No safe branch ancestry was established, so do not create a substitute main, rebase onto unknown tree, force push or claim promotion.

## Required independent reviewer verdict

A reviewer other than the Worker must give exact PASS or RETURN_TO_WORKER on the source commit/tree and authority/tests. Promotion may be attempted only after reviewer admission and successful resolution of the intended target main branch with demonstrable common ancestry and guarded merge semantics. Any unresolved migration authority or absence of common ancestry is a blocker, not a reason for history rewriting.
