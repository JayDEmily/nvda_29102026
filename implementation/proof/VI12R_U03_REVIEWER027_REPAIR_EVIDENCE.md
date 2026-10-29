# VI-12R U03 Reviewer-027 repair evidence

## Binding

- Reviewer-027 disposition: `FAIL / RETURN_TO_WORKER` at
  `31b76489b1ec32fa38921bd3f5e97e40f544e23e`.
- Rejected repaired U03 candidate: `758060930b015c23bf63a5de4d71c4d318760393` / tree
  `b819ffa1795e97e40374a59cedd42834233d2225`.
- Finding under repair: `R027-U03-F001` only.
- Repaired candidate: `06735b3682d79387ebaa4da70002e6685d52740a` / tree
  `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`.
- Physical changed paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py` only.
- Binary diff SHA-256 over those paths from rejected to repaired candidate:
  `e1dbcf371f893f75decea7701bc43415a4cdd2488fefa74221531ad1fb5c6c4d`.

## Repair proposition

Accepted BC-005/BC-009/BC-010 require native content to remain fidelity-bearing and same-occurrence
retry to be idempotent only for identical content. The realised generic comparator previously used
ordinary Python equality for non-numeric native values and ordinary mapping key equality/lookup,
which collapsed the Reviewer-027 `bytes`/`bytearray` and nested `int`/`float` key witnesses.

The repaired comparator first requires exact runtime-type agreement, preserves specialised Decimal
and IEEE-754 float/complex comparison, recursively matches nested mapping keys and values without
ordinary key lookup, and recursively compares list/tuple and set/frozenset members. The two concrete
Reviewer-027 conflicts are now rejected without replacing the first record.

## Frozen-candidate evidence

Pinned tooling: Python 3.13.5, pytest 9.0.3, mypy 1.20.1 compiled, Ruff 0.15.11.

Observed on the clean repaired candidate:

- Reviewer-027 regressions: 2/2 passed;
- U01+U02+U03: 373/373 passed;
- mypy source check: success, 15 files;
- Ruff: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture/dependency/public-seam controls: PASS;
- architecture/bootstrap: 74/74 passed;
- architecture promotion: 74/74 passed;
- diff check and strict Git integrity: pass;
- worktree: clean.

This is Worker evidence only. It does not independently accept U03. Fresh VI-13R Reviewer 028 is
required, and U04 remains prohibited pending Reviewer PASS and lawful U03 promotion.
