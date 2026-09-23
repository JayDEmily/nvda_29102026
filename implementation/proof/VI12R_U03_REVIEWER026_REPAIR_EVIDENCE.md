# VI-12R U03 Reviewer-026 repair evidence

## Status

**WORKER REPAIR CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

Reviewer 026 returned `FAIL / RETURN_TO_WORKER` because the repaired U03 retry comparator still
falsely rejected separately reconstructed identical NaN content and falsely accepted a complex
signed-zero representation change. The authorised repair is only `R026-U03-F001` and
`R026-U03-F002`; U04 remains prohibited.

## Exact repaired candidate

- branch: `work/vi12r-u03-r026-repair`;
- rejected repaired U03 candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`;
- Reviewer-026 FAIL commit: `f58aa8b9cd21f1ebd9b01b80a71213bd5d16c63b`;
- routed Worker continuity: `4415c74ca74d816bbe7088ce17e37c1f55f2a32a`;
- repaired candidate: `758060930b015c23bf63a5de4d71c4d318760393`;
- tree: `b819ffa1795e97e40374a59cedd42834233d2225`;
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
- repair binary diff SHA-256: `357742537ccb3d13d80d2beb5c31fdff892e45cd743602b6cee405c1f3014504`.

## Repair proposition

Same-occurrence retry comparison now preserves the existing equality law for all non-native
observation fields without invoking ordinary equality on `native_record`. Native numeric
comparison is exact for the representations already preserved by U03: float values compare by
IEEE-754 bytes, Decimal values by tuple/sign/scale, and complex values by the exact bytes of both
components.

This makes separately reconstructed canonical NaN values reflexive for retry identity while
retaining representation-sensitive conflict rejection, including signed zero. The already-closed
Reviewer-025 int/float and Decimal-scale conflicts remain rejected.

The focused regression proves the two concrete Reviewer-026 escapes only: reconstructed
`float("nan")`/`Decimal("NaN")` retries are idempotent, and complex signed-zero change is rejected
without replacing the original record.

## Exact validation

Pinned environment:

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
- architecture/dependency/public-seam controls: pass;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- Git diff/integrity: pass;
- candidate worktree: clean.

Fresh Reviewer 027 must independently disposition the repaired U03 candidate. U04 remains
prohibited until U03 receives `PASS` and is lawfully promoted to forward `main`.
