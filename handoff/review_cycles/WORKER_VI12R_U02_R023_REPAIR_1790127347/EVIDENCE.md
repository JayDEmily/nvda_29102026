# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received Tester-023 FAIL TAR SHA-256:
  `a9965d345de8ef5ab70e5fe5d1a6cdcd0cd65c1c816549fa02deeb114ad90893`;
- received filename: `NVDA_G03_TESTER_VI13R_U02_R023_FAIL_FULL_GIT_20260923.tar(1).gz`;
- Reviewer-023 FAIL continuity before repair: `8649a9e`;
- rejected U02 candidate: `a77dc596b7cbc3f248097df94d8dd0bef4491bec`;
- repaired U02 candidate: `5c62ec5147da718297b251b5a287405ebf3b4755`;
- repaired candidate tree: `dc1293d2c3d7e234e53a8d663f25eac51f7086ab`;
- repair branch: `work/vi12r-u02-r023-repair`;
- repair changed paths relative to the routed FAIL continuity:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u02_capture_schedule.py` only.

## Repair

`_CommandsV1` and `_ReadsV1` no longer store `_U02State` (or another directly reachable mutable
state wrapper). `create_owner()` constructs validated command/read capabilities over owner-local U02
state. The public facet objects retain only those callables. Existing U01/U02 public method shapes
and policy/slot/idempotency/read semantics are preserved.

Two bounded regressions were added:

1. the exact Reviewer-023 direct `_state` access/mutation path is absent and the rejected overlapping
   policy remains absent from referential readback;
2. ordinary direct facet attribute traversal exposes no mutable `dict`, `list` or `set` state,
   preventing a trivial `_state` rename/wrapper repair from satisfying the regression.

This is not a claim against arbitrary function-closure introspection, `eval`/`exec`, monkey-patching
or unrestricted Python metaprogramming; those were explicitly outside the authorised repair claim.

## Exact validation

Toolchain recovered from preserved project artefacts outside the repository:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact clean candidate `5c62ec5147da718297b251b5a287405ebf3b4755`:

- focused U01+U02 proof: **328 passed**;
- focused Reviewer-023 bypass regressions: **2 passed**;
- Ruff `src tests tools`: pass;
- mypy `src`: success, 15 source files;
- product-proof control: PASS, six families / 13 of 13 obligations;
- structural architecture validation: PASS, zero dependency/public-seam violations;
- dependency checker: PASS;
- public-seam checker: PASS;
- architecture/bootstrap: **74 passed**;
- `architecture_kernel` promotion: **74 passed**;
- `git diff --check`: pass;
- `git fsck --full --strict`: pass;
- worktree: clean.

U03 was not implemented or assessed.
