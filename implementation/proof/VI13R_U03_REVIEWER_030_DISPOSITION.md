# VI-13R Reviewer 030 — IWO-U03 Class-Level NativeValueV1 Disposition

**Date:** 2026-09-24
**Role:** fresh independent `TESTER` / Reviewer 030
**Reviewed candidate:** `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`
**Candidate tree:** `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`
**Disposition:** `PASS`

## 1. Scope and lineage

Reviewer 030 reviewed only IWO-U03 class-level closure under the active request. U04 was not assessed or implemented.

The relevant U03 lineage was inspected through Reviewer 025-029 and their corresponding Worker repairs. That lineage establishes one recurrent defect class: open-ended Python equality/representation was repeatedly used to decide BC-009/BC-010 same-occurrence content identity. Reviewer 029 closed the prior `array`/`range` witness and exposed the aware-`datetime` witness; current Programme Owner authority then replaced witness-by-witness repair with the finite recursive NativeValueV1 carrier and total exact-content relation.

The reviewed Worker candidate is the first candidate against that class-level authority. No new witness outside the authorised carrier was used as a rejection basis.

## 2. Authority clarification found during review

Reviewer 030 found one inconsistency in the Tester-authored authority wording, not in the Worker runtime implementation: `VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md` requires exact built-in runtime branches while also requiring the public/static declaration and runtime boundary to "agree". Python nominal class annotations include subclasses, so an ordinary annotation such as `int` or `str` cannot itself prove the stricter runtime predicate `type(value) is int/str`.

The current Programme Owner delegation to this Tester to resolve the U03 native-value-domain decision was therefore applied at the authority layer in `implementation/authority/VI13R_U03_NATIVE_VALUE_STATIC_TYPING_CLARIFICATION.md` at authority commit `c4caa78a2d13c5dc115c83fedcdf44648efe6d78`. Runtime semantics are unchanged. The static alias is the finite nominal envelope with no `Any`/`object` escape; exact built-in/subclass exclusion remains a runtime admission obligation. The official Python typing specification was inspected as primary language authority for this representability point.

This correction is not a relaxation made to obtain green: unsupported subclasses remain runtime-invalid and were independently challenged as such.

## 3. Class-level closure result

The candidate satisfies the authorised class-level proposition:

- `RawObservationOccurrenceV1.native_record` is statically exposed as `Mapping[str, NativeValueV1]`; the exported recursive alias contains the authorised carrier categories and no generic `object`/`Any` branch.
- Runtime snapshot/admission requires exact scalar/list/tuple runtime types, exact string mapping keys and recursively admitted values; unsupported values fail before owner admission state is created or replaced.
- Mapping implementation identity and insertion order are canonicalised away while logical string-key/value content remains semantic.
- Ingress and readback are recursively snapshotted, preserving mutable-container alias safety.
- Same-ID comparison is total over admitted snapshots: exact carrier branch/type, IEEE-754 float bytes, `Decimal.as_tuple()`, ordered recursive list/tuple content and order-insensitive mapping key/value content.
- No admitted comparison path falls through to arbitrary user-defined `__eq__`.
- Historical `complex`, `bytearray`, non-string-key mapping, `array.array`, `range`, aware-`datetime`, set/frozenset and arbitrary custom-object witnesses remain active as fail-closed unsupported-carrier proof rather than being deleted for green.
- Existing U01/U02 behaviour and still-valid U03 proof remain intact on the independently executable axes.
- Candidate-to-handoff production/test bytes are unchanged and U04 remains untouched.

Independent runtime challenge additionally verified bit-exact NaN payload/sign discrimination, Decimal representation discrimination, preservation of the first occurrence after conflicts, and fail-closed rejection of subclasses of authorised nominal scalar categories.

## 4. Validation actually obtained

The receiving sandbox provides Python 3.13.5 and pytest but does not provide the repository-pinned `mypy` module. That exact typechecker executable axis could therefore not be independently rerun here and is not claimed as independently green.

Independent Reviewer-030 evidence obtained on exact candidate `45ca4b8...` includes:

- U01+U02+U03 excluding the three tests whose bodies invoke `python -m mypy`: **381 passed / 3 deselected**;
- class-level runtime challenge: **PASS**;
- independent public alias-structure inspection: **PASS**, with `Mapping[str, NativeValueV1]` and no recursive `Any`/`object` escape;
- product-proof structural control: **PASS**, six families / 13 of 13 obligations;
- structural architecture validation: **PASS**;
- dependency validation: **PASS**;
- public-seam validation: **PASS**;
- candidate diff check: **PASS**;
- `git fsck --full --strict`: exit 0 with the pre-existing unreachable dangling blob `895775b2d27b6006f3f245b6742d5d021fed089b` diagnostic.

The Worker cycle separately records exact pinned Python 3.13.5 / pytest 9.0.3 / mypy 1.20.1 / Ruff 0.15.11 candidate evidence: U03 56/56, U01+U02+U03 384/384, source and strict modified-API mypy green, Ruff green, architecture/bootstrap 74/74 and architecture promotion 74/74. Those are preserved Worker observations, not relabelled as independently executed Tester results.

The inability to rerun mypy in this sandbox does not leave the semantic/static proposition unknown: Reviewer 030 independently inspected the exact exported alias and the official Python nominal-typing rule, while the candidate's runtime exact-type boundary was directly executed. No material U03 defect was established.

## 5. Disposition

`PASS`.

The Reviewer-025..029 recurrent equality class is closed for the authorised NativeValueV1 carrier on candidate `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf`.

U03 may now be lawfully promoted together with this Reviewer-030 disposition/evidence. U04 is authorised only after that promotion reaches forward `main` with preserved ancestry and integrity.
