# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received Reviewer-027 FAIL TAR SHA-256:
  `06b2922be039dc2199195d064698091cdd3f46d03f2bc69038b09289172989f5`;
- received filename: `NVDA_G03_TESTER_VI13R_U03_R027_FAIL_FULL_GIT_20260923.tar(2).gz`;
- received/routed Worker continuity before repair: `8f04fb9276b812198daa9cfc22541acf00656991`;
- Reviewer-027 disposition commit: `31b76489b1ec32fa38921bd3f5e97e40f544e23e`;
- rejected repaired U03 candidate: `758060930b015c23bf63a5de4d71c4d318760393`;
- repaired U03 candidate: `06735b3682d79387ebaa4da70002e6685d52740a`;
- repaired candidate tree: `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`;
- repair branch: `work/vi12r-u03-r027-repair`;
- physical repair changed exactly the U03 owner/proof paths:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
- repair binary diff SHA-256 over those two paths from rejected candidate to repaired candidate:
  `e1dbcf371f893f75decea7701bc43415a4cdd2488fefa74221531ad1fb5c6c4d`.

## Repair

The U03 native retry comparator now fails closed on a runtime-type change before generic equality can
collapse distinct representations. Decimal remains compared by exact tuple/sign/scale, float by
exact IEEE-754 bytes, and complex by exact real/imaginary IEEE-754 bytes.

Nested mappings no longer use ordinary set/key equality or ordinary lookup. Keys and values are
matched recursively with the same exact native comparator, so `int(1)` and `float(1.0)` cannot be
silently treated as the same nested key. List/tuple and set/frozenset native values are likewise
compared recursively after exact runtime-type agreement, preventing their nested elements from
reintroducing the same Python-equality collapse.

The bounded implementation-coupled regressions add only the two concrete Reviewer-027 witnesses:

- same-ID `b"abc"` -> `bytearray(b"abc")` is rejected and readback remains the first `bytes` value;
- same-ID nested mapping key `{1: "x"}` -> `{1.0: "x"}` is rejected and readback retains the first
  `int` key.

The complete U01+U02+U03 proof retains the already-closed int/float, Decimal-scale, reconstructed
NaN-idempotency and complex signed-zero behaviours. No provider validity, duplicate/retransmission
equivalence, U04 behaviour, persistence/replay or downstream capability was added.

## Exact validation

Pinned execution tooling, provisioned outside the repository from preserved project wheels after
successful SHA-256 manifest verification:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact clean candidate `06735b3682d79387ebaa4da70002e6685d52740a` / tree
`b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`:

- focused Reviewer-027 regressions: **2 passed**;
- focused U01+U02+U03 proof: **373 passed**;
- source mypy: success, 15 source files;
- Ruff `src tests tools`: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- candidate diff check: pass;
- `git fsck --full --strict`: pass;
- candidate worktree after validation: clean.

The first development U01+U02+U03 run used the base sandbox's pytest 9.0.2 and lacked mypy, so its
two mypy-invoking U01 proof cases failed for missing tooling. That run is not candidate evidence. A
validator invocation without `PYTHONPATH=src` likewise failed import and was rerun correctly. Neither
was treated as semantic failure or as frozen-candidate proof.

U04 was not implemented or assessed.
