# Worker cycle evidence

**Status:** `COMPLETE`

## Binding

- received Reviewer-028 FAIL TAR SHA-256:
  `5c020b2e9eb7ccbd9badf7368d8b17e9d61b3825744d2ab04e826cb1edfeaf24`;
- received filename: `NVDA_G03_TESTER_VI13R_U03_R028_FAIL_FULL_GIT_20260924.tar(1).gz`;
- received/routed Worker continuity before repair: `e968a3eaea65644fed087f3a4a4b86aa1df8247a`;
- Reviewer-028 disposition commit: `d6d58c0a45b439c262cc135b961e9c67b98ac0a8`;
- rejected repaired U03 candidate: `06735b3682d79387ebaa4da70002e6685d52740a`;
- repaired U03 candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`;
- repaired candidate tree: `21eb6bd2ba53b29ea6d80f90c01af40668f56955`;
- repair branch: `work/vi12r-u03-r028-repair`;
- physical repair changed exactly the U03 owner/proof paths:
  `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py`;
- repair diff SHA-256 over those two paths from rejected candidate to repaired candidate:
  `7f7ec1119976c668ac9a4a4ab77a78bc9341e376e57a625af2eb41c8f6e34bf6`.

## Repair

The U03 native retry comparator now preserves the two representation-bearing standard-sequence
facts proven missing by Reviewer 028. For `array.array`, retry identity compares the exact `typecode`
and the array's raw element bytes, so equal numeric contents with different signed/unsigned typecodes
cannot collapse through Python equality. For `range`, retry identity compares exact `start`, `stop`
and `step`, so two ranges that iterate to equal values but carry different bounds cannot collapse.

All earlier comparator law remains in place: exact runtime type is checked first; Decimal uses exact
tuple/sign/scale; float and complex preserve IEEE-754 representation; nested mappings and
list/tuple/set/frozenset values use recursive exact comparison. Existing non-native observation-field
retry equality is unchanged.

The bounded implementation-coupled regressions add only the two concrete Reviewer-028 witnesses:

- same-ID `array('b', [1])` -> `array('B', [1])` rejects and preserves the first typecode/content;
- same-ID `range(0, 3, 2)` -> `range(0, 4, 2)` rejects and preserves the first bounds.

No provider validity, duplicate/retransmission equivalence, U04 behaviour, persistence/replay or
downstream capability was added.

## Exact validation

The preserved BUILD-001 offline wheelhouse was extracted from the project artefact
`NVDA_IMPLEMENTATION_ADMISSION_PM_HANDOVER_FULL_GIT_20260913.tar(1).gz`; every wheel passed its
preserved `SHA256SUMS` manifest before tooling was provisioned outside the repository.

Pinned execution tooling:

- Python 3.13.5;
- pytest 9.0.3;
- mypy 1.20.1 (compiled);
- Ruff 0.15.11.

On exact clean candidate `d25aedeed5de65d0a241bdce6eae22671ef2ddf8` / tree
`21eb6bd2ba53b29ea6d80f90c01af40668f56955`:

- focused Reviewer-028 regressions: **2 passed**;
- focused U01+U02+U03 proof: **375 passed**;
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

During development, an initial array implementation failed the strict static proof because iterating
`array[Any]` introduced `Any`; it was replaced before freeze by `typecode` + `tobytes()` comparison.
An initial architecture/bootstrap invocation also omitted the exported repository `PYTHONPATH` needed
by a subprocess; the correctly bound run is the 74/74 result above. Neither failed development run
is candidate evidence.

U04 was not implemented or assessed.
