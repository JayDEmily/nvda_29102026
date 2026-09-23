# VI-13R U03 Reviewer 027 disposition

## Binding

- Role: fresh independent Reviewer 027.
- Scope: repaired `IWO-U03 — Raw observation admission, native fidelity and temporal-kind truth` only.
- Frozen repaired candidate: `758060930b015c23bf63a5de4d71c4d318760393`.
- Candidate tree: `b819ffa1795e97e40374a59cedd42834233d2225`.
- Prior findings under repair: `R026-U03-F001`, `R026-U03-F002`.
- U04 was not assessed and remains prohibited.

## Disposition

**`FAIL / RETURN_TO_WORKER`**.

The two Reviewer-026 findings are **closed**. Fresh same-ID `float("nan")` and `Decimal("NaN")`
reconstructions are idempotent, and complex signed-zero content change is rejected without replacing
the original record. The earlier int/float and Decimal-scale conflict cases remain closed. Exact
pinned U01+U02+U03 proof is independently **371/371** and current static/Ruff/product/architecture/
dependency/public-seam controls are green.

A bounded challenge finds one new material U03 defect.

### R027-U03-F001 — generic native equality still collapses distinct admitted content

A same-observation-ID retry from native `b"abc"` to `bytearray(b"abc")` is accepted as idempotent,
although the runtime representation/type changed. A second canary reproduces the same root defect
inside a nested native mapping: key `1` changed to `1.0` is accepted as identical. The original
record remains stored in both cases, but the conflicting retry is not rejected.

The implementation's numeric branches are now representation-sensitive, but the generic native-value
fallback remains ordinary `==`; the mapping branch also relies on ordinary set/key equality and
lookup. Python therefore collapses admitted representations that the U03 retry law requires to remain
distinct.

These are realised public-seam inputs, not invented provider semantics. `native_record` remains
`Mapping[str, object]`; production restricts only top-level native field names to exact strings and
successfully admits both witness families. No accepted provider-validity rule excludes them, and
BC-009 prohibits inventing one here.

This defeats BC-005 exact native-value fidelity, BC-009 conflicting-payload rejection, BC-010
idempotency only for identical same-occurrence content, and the IWO-U03 native-fidelity/retry law.

## Smallest bounded repair

The owning layer is the U03 M-owner native retry comparator plus bounded implementation-coupled U03
proof. Make native comparison exact/runtime-type-sensitive for all values admitted by the current U03
surface, including nested mapping keys, while retaining specialised reflexive NaN and exact
float/complex/Decimal handling and preserving existing non-native field equality semantics. Add only
the focused `bytes` vs `bytearray` and nested `int` vs `float` mapping-key regressions required to
close this finding.

Do not add provider validity, duplicate/retransmission equivalence, U04 behaviour, persistence,
replay or downstream capability.

U03 is not promotable. U04 remains prohibited pending a repaired candidate and fresh independent U03
review.
