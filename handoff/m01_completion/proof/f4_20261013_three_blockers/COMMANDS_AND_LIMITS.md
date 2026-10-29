# Commands and evidence boundary

Run date: 13-10-2026. Starting HEAD `f491c623d37403884fd4bf05cc47275296e320d1`.

## Successful inspection / integrity operations

```sh
tar --no-same-owner -xzf 'upload/NVDA_M01_F4_D186_AUTHORISED_RECOVERY_FULL_GIT_20261013.tar(3).gz'
git -C repository rev-parse HEAD
git -C repository status --short
git -C repository fsck --full --no-reflogs
sha256sum repository/handoff/m01_completion/authority/*
git -C repository log --all --oneline --grep='D178\|D189\|D192\|risk\|D133\|D177' -i
git -C repository log --all --oneline -G 'risk_breach|risk.*mapping|minimum_edge|expected_slippage_currency|signed_slippage_per_unit' -- src handoff/m01_completion/authority
git -C repository show 1b64bd4 --
git -C repository show 44875e9 --stat
git -C repository show 02af652 -- tests/product/derived_signal
git -C repository show 2f2d0b7 -- src/nvda_desk/derived_signal_calculation_truth/_stage1.py
git -C repository show 0120277 -- handoff/m01_completion/authority
git -C repository show 72f2039 --stat
git -C repository show b6a300e -- src/nvda_desk/derived_signal_calculation_truth/_stage1.py
```

Digest, catalogue-copy and row-count checks executed with Python standard-library CSV/hashlib and assert statements; exact resulting source rows and hashes are retained in AUTHORITY_READBACK.json. Reference workbook rows read using openpyxl 3.1.5 in the primary Python 3.12.14 runtime; resulting 19 exact row records are in WORKBOOK_REFERENCE_ROWS.json. Historical metadata search did not stand in for the actual diffs cited by the report.

## Diagnostic runtime only

Created an isolated diagnostic virtualenv with the ambient Python 3.12.14, installed pytest 9.0.3 and its pure-Python dependencies from the supplied offline bootstrap wheelhouse. Project Python 3.13.5 was not established. No supported-runtime product installation is claimed.

From repository root:

```sh
../diagnostic_env/bin/python -m pytest -q \
 tests/product/derived_signal/test_m01_f4_cross_stage_declared_predecessor_fail_closed.py \
 tests/product/derived_signal/test_m01_f4_cross_stage_rule_algebra_own_kernel.py \
 tests/product/derived_signal/test_m01_f4_cross_stage_remaining_own_kernel.py
PYTHONPATH=src ../diagnostic_env/bin/python \
 handoff/m01_completion/proof/f4_20261013_three_blockers/reproduce_omissions.py
```

Observed: 19 inherited focused tests passed; all probes completed. Raw outputs are retained. This reproduces inherited behaviour, not the proposed repair. No inherited test has been weakened or rewritten. Proposal numeric examples were independently checked with standard-library Fraction arithmetic; this establishes only the displayed example arithmetic, not model acceptance or production correctness.

## Recoverable failures and non-runs

- Initial tar extraction returned ownership-change errors. Re-extraction with `--no-same-owner` returned success; fsck and authority digests were checked afterwards. Initial failure is not recorded as successful extraction.
- Ambient `import pytest` failed before the isolated diagnostic installation.
- First workbook read failed due to incorrect relative path. Later corrected read succeeded. First write of the row evidence failed on an empty row; guarded enumeration then succeeded with the expected 19 rows.
- Required Python 3.13.5 was not found in inspected runtime paths; the supplied bootstrap checks the interpreter version and does not include a Python executable. This is not a claim that obtaining that interpreter is impossible.
- Full regression, supported-runtime verification, PostgreSQL checks, architecture/dependency/public-seam suites, Ruff and Mypy: not run for this evidence-only checkpoint. No production/test/schema/catalogue/governance changes are made.
- No Stage-1 status ledger entries were promoted. Remaining Stage-1 reconciliation depends on the unresolved semantics and required verification.
- Admission-handover archive copies (1) and (2) were reported unavailable by attachment delivery; neither was used.

The full-Git checkpoint is for authority review and recoverability. It is not an implementation candidate.
