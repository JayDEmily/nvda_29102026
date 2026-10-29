# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received Tester-025 FAIL TAR SHA-256:
  `0540ce1b6c960693580d0c47648c24f183ad38108b6d3850753196422ae8e682`;
- received filename: `NVDA_G03_TESTER_VI13R_U03_R025_FAIL_FULL_GIT_20260923_REFRESH.tar(3).gz`;
- Reviewer-025 routed FAIL continuity before repair: `8a87fc7ae8a2d55286840159bd9c5fb3610bcf62`;
- Reviewer-025 disposition commit: `04daa3c20773680bfab97a747e88778f276e188e`;
- rejected U03 candidate: `7cf8936f854fbed952a468ce06c2f2a0320d9291`;
- repaired U03 candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`;
- repaired candidate tree: `a9cc881f50b7a6adf021ce80fce52a330e9d203d`;
- repair branch: `work/vi12r-u03-r025-repair`;
- repair changed exactly the U03 owner/proof paths:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`.

## Repair

The U03 same-occurrence discriminator now combines full observation equality with a native-record
comparison that preserves fidelity-bearing numeric distinctions. Numeric runtime type is not
collapsed by Python equality; Decimal tuple/scale is compared exactly; floats use their hexadecimal
representation. Nested provider-native mapping/list/tuple values are compared recursively.

The bounded regression covers the exact Reviewer-025 int/float and Decimal-scale escapes, confirms
separately reconstructed genuinely identical content remains idempotent, and confirms a rejected
conflict leaves the first admitted record unchanged.

No provider duplicate/retransmission equivalence, provider validity rule, U04 behaviour,
persistence/replay or downstream capability was added.

## Exact validation

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11;
- focused U01+U02+U03 proof: **368 passed**;
- strict positive public-seam mypy specimen: pass;
- strict negative specimen: rc 1 with **15 diagnostics**;
- source mypy: pass, 15 source files;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture/dependency/public-seam controls: pass;
- architecture/bootstrap: **74 passed**;
- architecture promotion: **74 passed**;
- Git diff/integrity: pass;
- worktree: clean.

U04 was not implemented or assessed.
