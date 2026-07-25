# Semantic receipt — `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py`

## File evidence

- Sequence `104`, unit `PM-015`; test SHA-256 `6eceb47ddfa298b45bb4121a3a2a65c77118a7b2aedf769fd3c09c65d40f65ba`.
- Full reads: test `1-116`; complete implementation `src/nvda_desk/downstream/overnight_carry.py:1-203`; API construction and route methods `src/nvda_desk/api/app.py:281-360`; normative/P1 search found only vocabulary/planning mentions, not a governing overnight-carry proposition.
- Raw test result: `4 passed in 0.24s`.

## G1 — `test_carry_handoff_builds_lifecycle_limited_action_envelope_with_open_fallback`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:24-44`; a caller-built exit decision is converted to an overnight action envelope and configured-open fallback.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; current normative and P1 sources do not own an overnight carry handoff, action lattice, lifecycle ceiling, horizon vocabulary or next-session-open fallback.
- Authority match: the implementation is related to downstream lifecycle handling, but no proposition establishes this packet or its exact semantics.
- Behaviour proved: a trim decision yields `hold/trim`, the explicit/configured open uses first-truthy fallback, and the packet rejects `execution_allowed=True`.
- Limitation: horizon and open timestamp are untyped strings; decision identity is not independently authenticated; lifecycle ceiling can be caller-selected; empty/whitespace identifiers and temporal consistency are untested.
- Adversarial challenge: provide a fabricated exit decision, arbitrary horizon and malformed configured open; the tested assertions can remain green while the handoff is operationally meaningless.
- Exact-surface falsifier: change the allowed-action tuple, fallback open value or false execution flag; an assertion at lines `40-44` must fail.
- Assertion that must fail and why: at test lines `40-44`, changing the carried position/horizon, the exact `("hold", "trim")` action tuple, the configured-open fallback, or the false execution flag breaks a direct assertion. Caller-selected horizon, lifecycle ceiling and malformed timestamp text remain ungoverned.
- Semantic relation: `authority_missing`.
- Proof strength: `state_transition`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; admit an overnight-carry owner, typed horizon/open contract and action-ceiling semantics before repair.

## G2 — `test_market_carry_evaluation_applies_handoff_envelope_and_derives_vwap_distance`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:47-70`; one market mapping produces a five-percent distance and a capped trim recommendation.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; no normative proposition owns the four-percent VWAP threshold, VIX threshold `30`, market-state source, scalar context or carry recommendation.
- Authority match: session VWAP appears in planning material only; that is discovery evidence, not current runtime authority for this evaluator.
- Behaviour proved: the service computes `(close-vwap)/vwap`, derives one threshold action, applies the handoff cap, copies selected VIX/VVIX values and keeps execution false.
- Limitation: arbitrary mappings are accepted; symbol defaults to NVDA; timestamps, market sessions, source lineage, units, finite-value constraints, stale data, negative prices and the meaning of recommendation are unproved.
- Adversarial challenge: pass fabricated or stale prices and scalars with no source/time identity; a plausible recommendation is still returned.
- Exact-surface falsifier: change the five-percent calculation, recommendation, copied VIX value or execution flag; an assertion at lines `67-70` must fail.
- Assertion that must fail and why: at test lines `67-70`, changing the capped `trim` recommendation, five-percent calculation, copied `vix_close`, or false execution flag breaks a direct assertion. The service can still accept fabricated, stale or cross-symbol market mappings because no source or time identity is asserted.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; define authoritative inputs, thresholds, timing and recommendation semantics before behavioural promotion.

## G3 — `test_carry_replay_compares_market_evaluation_against_next_session_reference`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:73-92`; one evaluation is compared with caller-supplied next-session open and close values.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; no replay proposition owns this comparator, reference envelope, path labels or arithmetic base.
- Authority match: the false mutation flag is compatible with replay isolation, but compatibility does not establish complete replay identity or determinism.
- Behaviour proved: open-gap and close-to-close percentages are calculated from the evaluation close and the result reports no runtime mutation.
- Limitation: the reference is an unauthenticated mapping; evaluation/reference symbol, session and timestamp matching are absent; the false flag is declarative and no live state is observed.
- Adversarial challenge: compare an NVDA evaluation against another instrument or session; the asserted arithmetic still passes.
- Exact-surface falsifier: alter either path percentage or set the runtime flag true; an assertion at lines `90-92` must fail.
- Assertion that must fail and why: at test lines `90-92`, changing either three-percent/one-percent path value or setting `runtime_mutated` true breaks a direct assertion. The comparator never verifies that evaluation and reference belong to the same symbol, session or retained source envelope.
- Semantic relation: `authority_missing`.
- Proof strength: `replay`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; establish replay envelope completeness, identity matching and side-effect observation.

## G4 — `test_api_exposes_overnight_carry_dependency_surfaces`

- Test locator: `tests/tier_a/downstream_runtime/test_fwd017_overnight_carry_contract.py:95-116`; six route names and one market evaluation are exercised.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP`; no admitted API or overnight-carry contract owns these routes or default identifiers.
- Authority match: the API exposes the same unowned evaluator and fabricates absent upstream capital, risk, placement and policy IDs at `src/nvda_desk/api/app.py:281-304`.
- Behaviour proved: expected names exist, one mapping returns a member of the three-action set, and execution remains false.
- Limitation: route presence does not prove dependency correctness; fabricated lineage, caller-controlled lifecycle values, authentication, idempotency, persistence and error semantics are untested.
- Adversarial challenge: omit all upstream receipt IDs; the API manufactures them and the asserted result remains green.
- Exact-surface falsifier: remove one expected handler, return a recommendation outside the set or permit execution; an assertion at lines `105-116` must fail.
- Assertion that must fail and why: at test lines `97-116`, removing any expected handler breaks the subset assertion; returning a recommendation outside the three literals or setting execution true breaks a direct assertion. The API's fabricated fallback upstream IDs remain invisible to this test.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; admit the domain/API owner and prohibit fabricated upstream truth before repair.

## File decision

- Groups/relationships: `4/4`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- The file proves local calculations and non-execution defaults, but the entire overnight-carry domain, thresholds, lineage and replay envelope lack governing authority.
