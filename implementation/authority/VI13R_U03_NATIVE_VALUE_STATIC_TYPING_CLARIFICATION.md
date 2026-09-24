# Programme Owner Clarification — U03 NativeValueV1 Static Envelope versus Runtime Exact-Type Admission

**Date:** 2026-09-24
**Status:** `ACCEPTED — current human/programme authority clarification`
**Scope:** only the static-representation wording of `VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md` section 6.1; U03 runtime carrier semantics are unchanged
**Authority basis:** the Programme Owner's current delegation to this Tester to resolve the U03 native-value-domain / exact-content decision and proceed

## 1. Why clarification is required

`VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md` correctly makes the runtime NativeValueV1 carrier exact-type-sensitive for scalar and list/tuple branches. It also requires the public/static declaration and runtime admission boundary to "agree" on that carrier.

Python's standard static type system is nominal for ordinary class types. The Python typing specification states that a class type such as `str` represents instances whose class is `str` **or a direct or indirect subclass**, and that nominal subtyping follows subclassing. Consequently an ordinary annotation containing `int`, `float`, `Decimal`, `str`, `bytes`, `list[...]` or `tuple[...]` cannot itself express the stricter runtime predicate `type(value) is <exact class>` while still accepting ordinary instances of that class directly.

Primary language/type-system reference inspected for this decision:

- Python Typing Specification, **Type system concepts — Nominal and structural types / assignability**, <https://typing.python.org/en/latest/spec/concepts.html> (read 2026-09-24).

This is a representability limit of the static annotation system, not authority to widen the runtime carrier and not a Worker implementation defect.

## 2. Authoritative interpretation of "agree"

For U03 NativeValueV1 closure, static/runtime agreement means:

1. the exported static `NativeValueV1` alias enumerates the same authorised nominal carrier categories and recursive shape, with no `Any` or generic `object` escape;
2. the static surface rejects types that are not assignable to any authorised carrier category, including the currently reclassified outside-carrier witness families;
3. the runtime boundary is authoritative for the stricter exact-built-in/exact-`Decimal` admission rule and must reject subclasses of exact-type branches before semantic owner state is created or replaced;
4. static acceptance of a subclass solely because Python nominal subtyping makes it assignable to its authorised base class does **not** admit that subclass at runtime and does not weaken the exact-content relation;
5. no wrapper, coercion, nominal surrogate type or schema-version change is required merely to make Python static typing encode an exact-runtime-class predicate it does not natively represent.

## 3. Unchanged semantic obligations

This clarification does **not** change the NativeValueV1 runtime algebra, BC-005 native fidelity, BC-009 conflicting-payload rejection, BC-010 retry/idempotency law, or the fail-closed rule outside the carrier. In particular:

- exact runtime `bool`, `int`, `float`, `Decimal`, `str`, `bytes`, `list` and `tuple` restrictions remain mandatory;
- mapping ingress remains governed by the accepted mapping rule;
- unsupported subclasses must fail closed without mutation;
- there is still no generic `__eq__` fallback;
- U04 remains prohibited until U03 is independently accepted and lawfully promoted.

## 4. Reviewer-030 effect

Reviewer 030 must not fail the Worker because ordinary Python nominal annotations cannot statically exclude subclasses of an otherwise authorised carrier class. The review must instead establish both sides separately:

- static surface: finite recursive nominal envelope, no `Any`/`object` escape, unrelated outside-carrier categories rejected by the configured typechecker;
- runtime surface: exact-type admission and fail-closed subclass rejection.

A defect in either side remains a valid U03 failure. This clarification only removes the impossible requirement that the static type checker itself prove exact runtime class identity.
