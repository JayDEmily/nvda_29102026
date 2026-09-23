# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received Reviewer-026 FAIL TAR SHA-256:
  `e3ab1c014e4c46298a5d50ee67a5536e6979d7c8e95963ebc4b1d591588d0577`;
- received filename: `NVDA_G03_TESTER_VI13R_U03_R026_FAIL_FULL_GIT_20260923.tar(1).gz`;
- received/routed Worker continuity before repair: `4415c74ca74d816bbe7088ce17e37c1f55f2a32a`;
- Reviewer-026 disposition commit: `f58aa8b9cd21f1ebd9b01b80a71213bd5d16c63b`;
- rejected repaired U03 candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`;
- repaired U03 candidate: `758060930b015c23bf63a5de4d71c4d318760393`;
- repaired candidate tree: `b819ffa1795e97e40374a59cedd42834233d2225`;
- repair branch: `work/vi12r-u03-r026-repair`;
- physical repair changed exactly the U03 owner/proof paths:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
- repair binary diff SHA-256 over those two paths from rejected candidate to repaired candidate:
  `357742537ccb3d13d80d2beb5c31fdff892e45cd743602b6cee405c1f3014504`.

## Repair

`_observations_exactly_equal` now compares every accepted non-native observation field with its
existing equality semantics and delegates `native_record` to the fidelity-aware native comparator,
so NaN non-reflexivity can no longer short-circuit native comparison.

Native float comparison uses exact IEEE-754 bytes, making separately reconstructed identical NaNs
reflexive while retaining signed-zero and other representation distinctions. Complex values compare
the exact IEEE-754 representation of both real and imaginary components. Decimal values retain
exact tuple/sign/scale comparison. The already-correct int/float and Decimal-scale conflict
rejection remains in place.

The bounded implementation-coupled regressions cover only the two Reviewer-026 escapes:

- separately reconstructed same-ID `float("nan")` and `Decimal("NaN")` payloads remain idempotent;
- same-ID `complex(-0.0, 0.0)` -> `complex(0.0, 0.0)` is rejected and readback remains the first
  signed-zero representation.

No provider validity, duplicate/retransmission equivalence, U04 behaviour, persistence/replay or
downstream capability was added.

## Exact validation

Pinned execution tooling, provisioned outside the repository from preserved project wheels:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact clean candidate `758060930b015c23bf63a5de4d71c4d318760393`:

- focused Reviewer-026 regressions: **3 passed**;
- focused U01+U02+U03 proof: **371 passed**;
- source mypy: success, 15 source files;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- candidate diff check: pass;
- `git fsck --full --strict`: pass;
- candidate worktree after validation: clean.

Pre-freeze development checks also exposed and corrected strict-mypy `Any` leakage in the initial
generic comparator traversal. One pre-freeze promotion invocation correctly refused a dirty
worktree, and one validator invocation used an incomplete `PYTHONPATH`; both were rerun on the
frozen candidate with the exact commands/results above. Neither was treated as candidate proof.

U04 was not implemented or assessed.
