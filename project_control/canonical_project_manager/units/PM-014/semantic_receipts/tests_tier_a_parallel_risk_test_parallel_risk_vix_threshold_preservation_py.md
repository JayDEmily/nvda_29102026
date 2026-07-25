# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py`

## File evidence

- Sequence `086`, unit `PM-014`; test SHA-256 `35dfc0957c1f288e4aa1fb3f0b3f75fa8280b875ae5e932e982cf5ecdbcf5856`.
- Full reads: test `1-40`; evaluator `src/nvda_desk/domain/parallel_risk/environment_assessment.py:1-126`; directly exercised preparation/regime contracts; current profile config `config/parallel_risk_lane_profile.v1.yaml:1-21`; coefficient authority `config/coefficient_authority.v1.yaml:8-37`; Parallel Risk and coefficient seams `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-286`.
- Raw test result: `3 passed in 0.13s`.

## G1 — `test_vix_30_caution_threshold_is_preserved_as_compatibility_mode`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:20-25`; assertions require caution, `vix_elevated` and no hard block at exactly 30.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for a Parallel Risk threshold of 30 or the exact flag; related coefficient records are posture-owned and use 24/32.
- Authority match: the group faithfully locks current implementation compatibility but does not validate an admitted policy.
- Behaviour proved: the default evaluator maps VIX 30 to the asserted current envelope.
- Limitation: provenance, units, source completeness, calibration and whether 30 is lawful are unproved.
- Adversarial challenge: feed a fabricated VIX 30 or retain a stale legacy threshold after authority changes; all assertions remain green.
- Exact-surface falsifier: change the default 30 mapping so an assertion at lines `23-25` fails.
- Assertion that must fail and why: At VIX `30`, lines `23-25` must fail if state, contribution or hard-block output differs, because those assertions define the exact compatibility specimen. Their failure would detect a changed boundary result, while the legitimacy and provenance of threshold 30 remain unproved.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact threshold and flag authority are admitted.

## G2 — `test_vix_50_block_threshold_is_preserved_as_compatibility_mode`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:28-33`; assertions require block, caution flag and one hard block at exactly 50.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for a Parallel Risk threshold of 50 or the exact block vocabulary.
- Authority match: this is current regression evidence only; the controlling proposition does not define the numeric policy.
- Behaviour proved: the default evaluator maps VIX 50 to the asserted current block envelope.
- Limitation: source validity, threshold calibration, multiple blocks and policy lifecycle remain unproved.
- Adversarial challenge: preserve the 50 mapping after authoritative coefficients change or accept invalid VIX values elsewhere.
- Exact-surface falsifier: change the default 50 mapping so an assertion at lines `31-33` fails.
- Assertion that must fail and why: At VIX `50`, lines `31-33` must fail if the evaluator stops producing the asserted block state, caution contribution and hard block. This detects the current exact mapping only; it does not validate the policy owner or the source quality of VIX.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after exact block policy and vocabulary are admitted.

## G3 — `test_subthreshold_vix_does_not_create_legacy_caution`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_vix_threshold_preservation.py:36-40`; assertions require tight/empty contributions at 29.99.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for the complete subthreshold state policy.
- Authority match: the boundary narrows current behaviour but derives from the same unowned 30 threshold.
- Behaviour proved: one value immediately below 30 produces the asserted current state.
- Limitation: missing, negative, non-finite, stale and other subthreshold values are not covered.
- Adversarial challenge: mis-handle `None`, NaN or 0 while this single fixture remains green.
- Exact-surface falsifier: emit a contribution or non-tight state at 29.99 so an assertion at lines `39-40` fails.
- Assertion that must fail and why: Lines `39-40` must fail if `29.99` produces any contribution or a non-tight state, because they are the immediate-below-threshold boundary checks. They do not cover missing, non-finite, negative or other subthreshold inputs.
- Semantic relation: `authority_missing`.
- Proof strength: `boundary`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with an admitted threshold/state table and complete invalid/missing input handling.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve exact current 30/50 regression boundaries as observation evidence only. They cannot be Tier A until a lawful Parallel Risk owner admits the policy and resolves the conflicting posture-owned 24/32 coefficient records.
