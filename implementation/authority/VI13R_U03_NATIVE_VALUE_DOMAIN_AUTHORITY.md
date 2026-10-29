# Programme Owner Authority — U03 Native-Value Carrier Domain and Exact-Content Relation

**Date:** 2026-09-24  
**Status:** `ACCEPTED — current human/programme authority`  
**Scope:** `IWO-U03` only; RawObservationOccurrence.v1 native-record carrier and same-occurrence retry exact-content discrimination  
**Supersedes:** the unresolved blocker in `VI13R_REVIEW_LINEAGE_AND_U03_BLOCKER_CORRECTION.md` section 4  
**Does not authorise:** U04, provider validity/quarantine policy, provider duplicate equivalence, provider retransmission equivalence, persistence design, D001+, downstream consumer semantics, or any change to BC-005/BC-009/BC-010 meaning

## 1. Authority basis

The current Programme Owner explicitly authorised this Tester thread to resolve the U03 native-value-domain / exact-content decision and proceed. Under repository authority precedence, that current human/programme instruction supplies the missing authority identified by Reviewer 029 and the later blocker correction.

The Tester recurrence rule remains unchanged: reviewers detect recurrence and stop on an authority gap; they do not normally invent semantic law. This document exists only because current higher programme authority has now been supplied for this specific gap.

## 2. Governing interpretation

BC-005 requires preservation of admitted provider-logical field names and values unchanged, but it does not make arbitrary Python object graphs part of the semantic contract. The realised annotation `Mapping[str, object]` was therefore too mechanically broad to serve as the exact-content domain for BC-009/BC-010.

For the current provider-neutral tranche, the public implementation carrier for `native_record` is a closed recursive **NativeValueV1 carrier algebra**. It carries provider-logical content without asserting wire-byte/header-order/serialization archival and without defining provider business validity.

### NativeValueV1 carrier algebra

A carried native value is exactly one of:

- `None`;
- exact built-in `bool`;
- exact built-in `int`;
- exact built-in `float`;
- exact `decimal.Decimal`;
- exact built-in `str`;
- exact built-in `bytes`;
- exact built-in `list` whose items are NativeValueV1 values;
- exact built-in `tuple` whose items are NativeValueV1 values; or
- a mapping whose logical field names are exact built-in `str` values and whose values are NativeValueV1 values. Mapping implementation identity and iteration order are not provider content and are not preserved as semantic distinctions.

Top-level `native_record` remains a provider-logical mapping with string field names. A mapping may be accepted from any lawful `Mapping` implementation at ingress, but the owner snapshot must not preserve or depend on custom mapping equality/behaviour; only the logical string-key/value content is admitted.

Provider-supplied null remains the NativeValueV1 `None` value. Structural absence outside `native_record` remains governed separately by BC-009.

## 3. Exact-content relation

Same-occurrence retry exactness under BC-010 is defined over the admitted carrier algebra, not Python's generic `==` fallback.

- Different carrier branches/types are different content. In particular, `bool` is not `int`, and `list` is not `tuple`.
- `None`, `bool`, `int`, `str` and `bytes` compare by exact type plus value.
- `float` compares by exact IEEE-754 binary64 representation, preserving NaN bit-pattern/sign and signed zero distinctions.
- `Decimal` compares by exact `Decimal.as_tuple()` representation, preserving sign/digits/exponent and NaN representation carried by that tuple.
- `list` and `tuple` compare by exact container kind, length, order and recursive item exactness.
- mappings compare by the same logical string-key set and recursive value exactness; mapping iteration/insertion order is not content because BC-005 expressly does not claim universal header-order/serialization archival.
- there is **no generic object-equality fallback** for values outside this carrier algebra.

Two separately reconstructed carrier values are identical content when this relation says they are identical. Object identity is not required.

## 4. Values outside the carrier algebra

A value outside NativeValueV1 is **not admitted by the current generic carrier** and must fail closed before owner state is created or replaced. The implementation must not sanitise, coerce, stringify or silently normalise it.

This rejection is not a judgement that a provider tick is bad, duplicated or quarantined. It means only that no currently admitted provider mapping has supplied a lossless carrier rule for that runtime representation.

If a future admitted provider mapping genuinely requires another native runtime representation, that mapping must first supply explicit current authority for a lossless carrier/codec and exact-content rule for that representation. Such an extension must not reintroduce generic Python `__eq__` as the semantic fallback.

## 5. Disposition of Reviewer-025..029 witness types

The preserved Git history remains valid evidence of why the open `object` surface was unsafe. Under this authority, however, witness types outside NativeValueV1 are no longer lawful admitted-content specimens for the current generic carrier.

Tests that currently treat unsupported values such as arbitrary custom objects, `array.array`, `range`, `datetime`, `bytearray`, `complex`, sets/frozensets or nested non-string mapping keys as admitted native content must not be silently deleted for green. Their active proof role must be explicitly reclassified to the new proposition: **unsupported carrier representations fail closed without mutating the previously admitted occurrence**. History remains preserved in Git.

## 6. Required class-level closure proposition

A Worker may return U03 to Reviewer 030 only when all of the following are true on one frozen candidate:

1. the public/static carrier declaration and runtime admission boundary agree on the finite NativeValueV1 carrier above;
2. allowed values preserve BC-005 native fidelity and alias-safe readback;
3. same-ID independently reconstructed identical content is idempotent under the exact-content relation;
4. same-ID conflicting content is rejected without replacing the first occurrence;
5. unsupported carrier values fail closed before semantic state mutation;
6. no comparator path can fall through to arbitrary user-defined `__eq__` or another unbounded object-equivalence mechanism;
7. existing U01/U02 semantics and all still-valid U03 proof remain intact; and
8. U04 remains untouched and prohibited.

Reviewer 030 must challenge this **class-level closure**, not search for another arbitrary Python type outside the authorised carrier and call that a new admitted-value defect.
