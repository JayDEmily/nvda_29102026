# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received source TAR SHA-256:
  `5b730936a1a6588d0f023398c55ad2b27e6728bc752a96e28eb0e007f0b2a457`;
- received filename: `NVDA_G03_U03_NATIVE_DOMAIN_WORKER_HANDOFF_FULL_GIT_20260924.tar(1).gz`;
- received repository HEAD before repair: `4c196dfad6c128c04815b167c1a6bbcd5c0145e0`;
- authority-resolution parent: `65716819fd24cc7d5941cace83e5883d8e0e76f9`;
- Reviewer-029 FAIL: `9b2ff603517c7fa5e063a4ad08790bb9fddd28c3`;
- rejected U03 candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8` /
  tree `21eb6bd2ba53b29ea6d80f90c01af40668f56955`;
- accepted/promoted U02 forward `main`: `a78ae7b5515c2e482a2656cebeebae3fa5a6d584`;
- governing class-level authority:
  `implementation/authority/VI13R_U03_NATIVE_VALUE_DOMAIN_AUTHORITY.md`;
- frozen Worker candidate: `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` /
  tree `81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`;
- branch: `work/vi12r-u03-native-domain-closure`;
- candidate changed exactly:
  - `src/nvda_desk/raw_signal_occurrence_truth/api.py`;
  - `tests/product/raw_signal/_support.py`;
  - `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
  - `tests/product/raw_signal/typecheck/native_value_negative.py`;
  - `tests/product/raw_signal/typecheck/public_seam_positive.py`;
- candidate diff SHA-256 over those five paths:
  `33bebefa1d8e8028f03f32c29c63fef62290cc17c052b7f87764126d0d06f798`.

## Class-level closure implemented

The public/static seam now exports recursive `NativeValueV1` with exactly the authorised branches:
`None`, exact built-in `bool`, `int`, `float`, exact `Decimal`, exact built-in `str`, `bytes`,
recursive exact built-in list/tuple, and string-key recursive `Mapping` values.
`RawObservationOccurrenceV1.native_record` is `Mapping[str, NativeValueV1]`.

Runtime admission/snapshot is recursive and fail-closed. Scalar branches require the authorised
exact runtime type. List and tuple require exact built-in container type. Mapping ingress may use a
lawful `Mapping` implementation, but the owner copies only exact built-in string keys and recursively
validated values into ordinary dictionaries. Cyclic composite values are rejected. Unsupported
values are rejected with `TypeError` before the owner creates or replaces semantic state; no
stringification, coercion or generic deepcopy admission remains.

Readback stays alias-safe: mutable ingress structures are recursively snapshotted and mutable values
returned through `_NativeRecordSnapshot` are recursively resnapshotted. Mapping implementation and
insertion order therefore do not become semantic content while logical string-key/value content is
preserved.

Same-occurrence native exactness is total over the authorised carrier without arbitrary equality
fallback. Mappings compare logical key sets and recursive values. Scalar branch type must match.
Float compares packed IEEE-754 binary64 bytes, preserving NaN representation and signed zero;
`Decimal` compares `as_tuple()`; list/tuple compare exact kind, length, order and recursive content.
An unsupported value reaching the internal comparator raises rather than falling through to
user-defined `__eq__`.

## Proof disposition

Still-valid U03 proof is retained. The former Reviewer-026..029 implementation-coupled specimens
that current authority places outside NativeValueV1 are not deleted; they are reclassified into
fail-closed unsupported-representation proof. The active cases include complex, bytearray, nested
non-string mapping keys, `array.array`, `range`, aware `datetime`, set and frozenset. Each proves
that an unsupported retry raises and the first admitted occurrence remains unchanged.

A separate custom object with an explosive `__eq__` proves runtime rejection occurs without
invoking arbitrary equality. Static negative proof covers datetime, complex, array and non-string
mapping-key specimens against the public `NativeValueV1` alias. Allowed recursive proof covers
custom mapping ingress, reconstruction through ordinary dictionaries with different insertion
order, ingress alias mutation, readback alias mutation, Decimal and signed-zero content. Existing
NaN reconstruction and Decimal representation cases remain active; a list/tuple kind change remains
an admitted-carrier conflict and preserves the first occurrence.

No datetime special case, open-ended type catalogue, provider validity policy, U04, persistence or
replay behaviour was added.

## Exact committed-candidate validation

Tooling used outside the repository:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact candidate `45ca4b8dcca6fdb5001e1754fd81bdba37ce05bf` / tree
`81ef8edc93c9b322b29cdec6b9ab76b731d8e9a5`:

- complete U03 proof: **56 passed**;
- U01+U02+U03: **384 passed**;
- `python -m mypy src`: success, 15 source files;
- strict `--disallow-any-expr` mypy on modified `api.py`: success;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion set: **74 passed**;
- `git diff HEAD^ HEAD --check`: pass;
- `git fsck --full --strict`: exit 0, with one dangling blob diagnostic
  (`895775b2d27b6006f3f245b6742d5d021fed089b`);
- candidate worktree after validation: clean.

During development, one first validation attempt stopped at two Ruff issues in the new proof
(import ordering and a regex-literal warning); both were corrected before candidate freeze. An
over-broad development-only `mypy --strict --disallow-any-expr src` invocation also reported
pre-existing Any use outside this U03 change; the repository-required `python -m mypy src` and the
strict modified-API check above are the committed-candidate evidence. A pre-commit promotion-gate
run correctly rejected the then-dirty worktree; the committed clean candidate passed 74/74.

U03 remains unaccepted pending fresh independent Reviewer 030. U04 remains prohibited.
