# VI-12R U03 Reviewer-028 Repair Evidence

## Binding

- Reviewer-028 FAIL commit: `d6d58c0a45b439c262cc135b961e9c67b98ac0a8`.
- Rejected U03 candidate: `06735b3682d79387ebaa4da70002e6685d52740a` /
  tree `b73b6ba4486eba9ae3aa4c1facc626579c8b8ee5`.
- Finding repaired: `R028-U03-F001` only.
- Repaired physical candidate: `d25aedeed5de65d0a241bdce6eae22671ef2ddf8` /
  tree `21eb6bd2ba53b29ea6d80f90c01af40668f56955`.
- Physical changed paths: `src/nvda_desk/raw_signal_occurrence_truth/api.py` and
  `tests/product/raw_signal/test_u03_observation_native_temporal.py` only.

## Implemented repair

The exact-native retry comparator now handles the two remaining Reviewer-028 sequence
representations explicitly:

- `array.array`: exact typecode plus raw array bytes;
- `range`: exact start, stop and step.

This prevents ordinary equality from treating `array('b', [1])` and `array('B', [1])`, or
`range(0, 3, 2)` and `range(0, 4, 2)`, as identical same-occurrence content. Rejected retries leave
the first admitted record in place. Earlier exact runtime-type, Decimal, IEEE-754 float/complex,
mapping and nested collection handling remains unchanged.

No U04, persistence, replay, provider-validity or downstream semantics were added.

## Frozen-candidate evidence

Pinned Python 3.13.5 / pytest 9.0.3 / mypy 1.20.1 / Ruff 0.15.11 tooling was provisioned outside
the repository from a project-preserved wheelhouse after complete SHA-256 manifest verification.

On clean candidate `d25aedeed5de65d0a241bdce6eae22671ef2ddf8`:

- Reviewer-028 regressions: **2 passed**;
- U01+U02+U03: **375 passed**;
- mypy: success across 15 source files;
- Ruff: pass;
- product-proof control: PASS, six families / 13 of 13 obligations;
- architecture validation: PASS, zero dependency/public-seam violations;
- dependency and public-seam checkers: PASS;
- architecture/bootstrap: **74 passed**;
- architecture promotion: **74 passed**;
- `git diff HEAD^ HEAD --check`: pass;
- `git fsck --full --strict`: pass;
- candidate worktree: clean.

Fresh independent Reviewer 029 remains required. U03 is not accepted by this Worker evidence and U04
remains prohibited until U03 receives PASS and is lawfully promoted.
