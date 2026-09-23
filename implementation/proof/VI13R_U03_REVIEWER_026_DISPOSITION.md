# VI-13R U03 Reviewer 026 disposition

## Binding

- Role: fresh independent Reviewer 026.
- Scope: repaired `IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth` only.
- Frozen repaired candidate: `6316735eb22bdbe243b02637f09376bf1200e43d`.
- Candidate tree: `a9cc881f50b7a6adf021ce80fce52a330e9d203d`.
- Prior finding under repair: `R025-U03-F001`.
- U04 was not assessed and remains prohibited.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

The two Reviewer-025 example escapes are closed: same-ID `int(1)` -> `float(1.0)` and
`Decimal("1.0")` -> `Decimal("1.00")` retries are rejected and do not replace the original record.
The exact-pinned focused U01+U02+U03 suite is independently **368/368**, and current static/Ruff/
product/architecture/dependency/public-seam controls are green.

`R025-U03-F001` is nevertheless **not fully closed** because the realised comparator still violates
the accepted same-occurrence exact-content law on native numeric values admitted by the current
public contract.

### R026-U03-F001 — identical NaN retry is falsely rejected

A first admitted observation containing `float("nan")` and a separately reconstructed same-ID
observation containing a fresh `float("nan")` are genuinely reconstructed copies of the same native
value under the current U03 surface, yet the retry raises the conflicting-content `ValueError`.
`Decimal("NaN")` reproduces the same defect.

The candidate gates native comparison behind ordinary full-dataclass equality. NaN equality is
non-reflexive across separately reconstructed values, so this outer equality fails before the
native comparator can decide exact native content.

This defeats BC-010 same-ID idempotency for identical content, BC-005 native-value preservation and
the explicit Reviewer-026 identical-reconstruction obligation.

### R026-U03-F002 — complex signed-zero conflict is falsely accepted

A first observation with native `complex(-0.0, 0.0)` followed under the same occurrence identity by
`complex(0.0, 0.0)` is accepted as idempotent. Readback retains the first `(-0+0j)` representation.
The repair explicitly recognises `complex` as numeric but compares it with ordinary `==`, which
collapses the signed-zero component.

This defeats BC-005 exact native fidelity, BC-009 conflicting-payload rejection and BC-010
idempotency only for identical content.

These are realised public-seam failures, not invented provider semantics: `native_record` is
currently `Mapping[str, object]`, its snapshot does not exclude these value types, both are admitted
before retry comparison, and BC-009 prohibits inventing provider validity rules here.

## Smallest bounded repair

The owning layer is the U03 M-owner retry comparator plus its implementation-coupled U03 proof.
Remove ordinary native-record equality from the full-observation prerequisite, preserve accepted
non-native field semantics, and make the admitted native numeric comparison both representation-
sensitive where the contract already preserves representation and reflexive for separately
reconstructed identical values. Add focused regressions for the two concrete Reviewer-026 escapes.

Do not add provider validity/duplicate/retransmission semantics, U04 behaviour, persistence, replay
or downstream capability.

U03 is not promotable. U04 remains prohibited pending a repaired candidate and fresh independent
U03 review.
