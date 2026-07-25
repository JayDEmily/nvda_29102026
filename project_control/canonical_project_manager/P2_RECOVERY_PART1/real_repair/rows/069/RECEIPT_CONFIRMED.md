# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py`

## File evidence

- Sequence `069`, unit `PM-014`; test SHA-256 `07b965aa0a7b0b7d7b2d08ac30b4fe0f5375d9cbd6f5b692873d65d61e3930a4`.
- Full reads: test `1-59`; implementation `src/nvda_desk/domain/parallel_risk/freshness.py:1-77`; exercised freshness contract; source/capture/persist separation `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:27-44,58-64`; PRL authority `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`.
- Raw test result: `3 passed in 0.13s`.

## G1 — `test_freshness_register_marks_fresh_ageing_and_stale_with_deterministic_defaults`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:8-31`; assertions at lines `27-31` fix ages `30/90/150`, default limit `60`, and states `fresh/ageing/stale`.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:27-44,58-64`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the `Freshness Register`, 60/120-second thresholds or state taxonomy.
- Authority match: temporal provenance is governed, but classification thresholds and PRL consequences are not defined by the cited authority or governed config.
- Behaviour proved: the current helper calculates non-negative age and applies its hard-coded 60-second and 2× limit branches to these fixtures.
- Limitation: it does not prove threshold suitability by signal family, timezone/clock skew policy, invalid thresholds, future timestamps, configuration ownership or downstream meaning.
- Adversarial challenge: the helper could apply the same 60-second limit to a signal requiring five minutes, or grant authority from `fresh`, while all assertions pass.
- Exact-surface falsifier: change the default limit or branch comparison so any assertion at lines `27-31` fails for the exact fixtures.
- Assertion that must fail and why: line `29` fails if the default age limit is no longer `60`; line `27` or `30` fails if the first threshold no longer separates 30 seconds from 90 seconds; and line `31` fails if the second threshold no longer classifies 150 seconds as stale. These assertions pin the hard-coded arithmetic only; they do not validate that the thresholds are lawfully owned or suitable for each signal family.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after admitted state vocabulary and per-signal governed threshold/consequence authority.

## G2 — `test_freshness_register_unknown_when_source_or_generated_time_absent`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:34-39`; assertions at lines `37-39` fix `unknown`, no observed age and one impact string.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:66-77`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact freshness-state and impact labels.
- Authority match: explicit missing/degraded state is normatively required, but the register form and exact labels are not.
- Behaviour proved: absent source/generated timestamps produce the asserted current object values.
- Limitation: missing source time and missing generation time are collapsed; no error, completeness or downstream consequence is proved.
- Adversarial challenge: a mandatory timestamp failure could be silently downgraded to `unknown`; assertions `37-39` would remain green despite fail-closed law.
- Exact-surface falsifier: emit a non-`unknown` state, numeric age or different impact string so assertion `37`, `38` or `39` fails.
- Assertion that must fail and why: line `37` fails if missing temporal inputs produce any state other than `unknown`; line `38` fails if an age is fabricated; and line `39` fails if the current unknown-impact label changes. None of those assertions requires the helper to distinguish a permitted optional absence from a mandatory preparation failure.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after the owning contract distinguishes mandatory failure from permitted unknown/degraded absence.

## G3 — `test_freshness_register_is_metadata_only_and_neutral_state_of_play`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_freshness_register.py:42-59`; assertions at lines `53-59` fix stale state, capture/persist times, source refs, impact text and absence of two substrings.
- Authority locator: `docs/04.2_PREPARED_DATA_CONTRACTS_WORKING.md:27-44,58-64` for temporal lineage; `NO_VALID_AUTHORITY_RELATIONSHIP` for the impact policy or claimed metadata-only register.
- Authority match: source/capture/persist separation and source references match governed provenance; the impact label and non-authority semantics do not have exact authority.
- Behaviour proved: the object carries the three supplied timestamps and source reference unchanged for this specimen.
- Limitation: selected substring absence does not exclude action aliases, nested authority or side effects, and the test does not validate source-time precedence or provenance completeness.
- Adversarial challenge: add `execution_allowed=True` or mutate a downstream service without using the words `trade` or `order`; assertions `53-59` remain green.
- Exact-surface falsifier: alter carried capture/persist timestamps or source refs so assertion `54`, `55` or `56` fails; this falsifies only the bounded lineage carriage.
- Assertion that must fail and why: line `54` detects a changed capture timestamp, line `55` detects a changed persistence timestamp, and line `56` detects lost or altered source references. The two substring checks at lines `58-59` would not fail for differently named authority fields or external side effects, so they cannot prove the title's complete metadata-only claim.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `identity_lineage`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after structural non-authority tests and governed impact semantics.

## File decision

- Groups/relationships: `3/3`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve age arithmetic and timestamp-carriage observations as implementation evidence only.
