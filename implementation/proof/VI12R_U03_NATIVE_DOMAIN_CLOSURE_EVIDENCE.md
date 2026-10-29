# VI-12R U03 NativeValueV1 Class-Level Closure Evidence

## Binding

- Programme Owner authority:
  `implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`.
- Reviewer-029 FAIL: `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`.
- Rejected U03 candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8` /
  tree `21eb6bd2ba53b29ea6d80f90c01af40668f56955`.
- Class-level closure candidate: `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` /
  tree `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`.
- Branch: `work/vi12r-u03-native-domain-closure`.
- U04 remains prohibited.

## Implemented closure

The public U03 seam now declares and exports the exact finite recursive `NativeValueV1` carrier
required by current authority. Runtime snapshot/admission recursively validates that carrier,
canonicalises mapping implementations to logical string-key/value dictionaries, rejects cycles and
unsupported representations, and keeps ingress/readback alias-safe.

Same-occurrence native retry exactness is defined only over this carrier. Float comparison uses
IEEE-754 binary64 representation, `Decimal` uses `as_tuple()`, list/tuple retain exact kind/order and
recursive content, and mappings compare logical key sets plus recursive values without treating
mapping implementation or order as semantic. No arbitrary-object `__eq__` fallback remains.

The Reviewer-026..029 witnesses that current authority places outside the carrier remain active as
unsupported fail-closed proof rather than being deleted. A custom explosive `__eq__` specimen proves
unsupported admission does not invoke user equality. Rejected unsupported or conflicting retries
preserve the first stored occurrence.

No U04, provider-validity, persistence or replay behaviour was added.

## Frozen-candidate evidence

Pinned tooling: Python 3.13.5, pytest 9.0.3, mypy 1.20.1 (compiled), Ruff 0.15.11.

On exact candidate `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` / tree
`81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`:

- U03: **56/56 passed**;
- U01+U02+U03: **384/384 passed**;
- source mypy: success across 15 source files;
- strict/disallow-Any mypy on modified production `api.py`: success;
- Ruff: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture validation: PASS, zero dependency/public-seam violations;
- dependency/public-seam checks: PASS;
- architecture/bootstrap: **74/74 passed**;
- architecture promotion: **74/74 passed**;
- diff check: pass;
- strict Git fsck: exit 0 with one dangling-blob diagnostic;
- candidate worktree: clean.

Fresh independent Reviewer 030 remains required. These Worker results do not constitute U03
acceptance or promotion.
