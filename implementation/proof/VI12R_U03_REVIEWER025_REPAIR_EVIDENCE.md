# VI-12R U03 Reviewer-025 repair evidence

## Status

**WORKER REPAIR CANDIDATE — NOT INDEPENDENTLY ACCEPTED.**

Reviewer 025 returned `FAIL / RETURN_TO_WORKER` on U03 because same-occurrence retry comparison
used ordinary Python/dataclass equality and therefore collapsed fidelity-bearing native numeric
content. The authorised repair is only `R025-U03-F001`; U04 remains prohibited.

## Exact repaired candidate

- branch: `work/vi12r-u03-r025-repair`;
- rejected U03 candidate: `7cf8936f854fbed952a468ce06c2f2a0320d9291`;
- Reviewer-025 FAIL commit: `04daa3c20773680bfab97a747e88778f276e188e`;
- repaired candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`;
- tree: `a9cc881f50b7a6adf021ce80fce52a330e9d203d`;
- repair paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
- repair binary diff SHA-256: `5af39d80702380726633d379b719d99093dc8b7af46224ff7de06a40a9134cad`.

## Repair proposition

Same-occurrence retry comparison now retains ordinary payload equality for the full observation and
adds an exact native-value discriminator for fidelity-bearing numeric content. Numeric runtime type
is part of retry identity; `Decimal` tuple/scale is preserved; float representation uses
`float.hex()`. Nested mappings and list/tuple content are compared recursively without creating
provider retransmission equivalence or provider validity rules.

The focused regression proves both concrete Reviewer-025 escapes are rejected:

- `int(1)` versus `float(1.0)` under the same observation identity;
- `Decimal("1.0")` versus `Decimal("1.00")` under the same observation identity.

The same regression also reconstructs genuinely identical native content independently and confirms
that the retry remains idempotent and returns the originally admitted occurrence. After a rejected
conflict, referential readback retains the original numeric runtime type/representation.

## Exact validation

Pinned environment:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact clean candidate `6316735eb22bdbe243b02637f09376bf1200e43d`:

- focused U01+U02+U03 proof: **368 passed**;
- focused same-occurrence numeric retry regression: **2 parameter cases passed**;
- strict positive public-seam mypy specimen: pass;
- strict negative public-seam mypy specimen: expected rc 1 with **15 diagnostics**;
- source mypy: success, 15 source files;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- `git diff --check`: pass;
- `git fsck --full --strict`: pass;
- worktree: clean.

Fresh Reviewer 026 must independently disposition the repaired U03 candidate. U04 remains
prohibited until U03 receives `PASS` and is lawfully promoted to forward `main`.
