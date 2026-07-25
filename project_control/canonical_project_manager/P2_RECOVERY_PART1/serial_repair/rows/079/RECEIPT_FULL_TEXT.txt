# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_scheduled_event_preservation.py`

## File evidence

- Sequence `079`, unit `PM-014`; test SHA-256 `2d0db0088b71af676f345d40506a763cba079b01955fa2ad55dd10291e83f655`.
- Full reads: test `1-37`; environment assessment `src/nvda_desk/domain/parallel_risk/environment_assessment.py:1-126`; temporal contract `src/nvda_desk/contracts/temporal.py:1-48`; calendar and Parallel Risk seams `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:188-201,254-269`.
- Raw test result: `1 passed in 0.13s`.

## G1 — `test_scheduled_event_window_active_caution_is_preserved_without_trade_authority`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_scheduled_event_preservation.py:12-37`; assertions require the free-form tag to become a same-named caution/contribution and check absence of three selected strings.
- Authority locator: `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:188-201,254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact tag vocabulary and its caution consequence.
- Authority match: calendar event context may lawfully inform the independent risk lane, but no admitted proposition defines this tag or mapping.
- Behaviour proved: one tagged event fixture produces the asserted current caution and contribution.
- Limitation: free-form tag ownership, event-type semantics, timing/materiality conditions and structural non-authority are unproved; substring absence is incomplete.
- Adversarial challenge: another tag or alias could trigger action authority, or this tag could be applied outside its valid window, without failing the test.
- Exact-surface falsifier: remove or rename the scheduled-event caution or contribution so an assertion at lines `31-33` fails; insert `buy`, `sell` or `order` into the JSON payload so the matching assertion at lines `35-37` fails.
- Assertion that must fail and why: line `31` fails if the tagged window no longer yields a caution envelope, line `32` fails if the exact tag is not retained as the sole caution flag, and line `33` fails if the contribution family changes. Lines `35-37` fail only for the literal words `buy`, `sell` or `order`; other action fields or side effects remain unobserved.
- Semantic relation: `authority_missing`.
- Proof strength: `behavioural`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after calendar-owned typed event semantics, an admitted consequence rule and structural non-authority proof.

## File decision

- Groups/relationships: `1/1`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the current tag-to-caution regression observation; do not admit its free-form vocabulary or consequence as Tier A truth.
