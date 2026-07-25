# Semantic receipt — `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py`

## File evidence

- Sequence `097`, unit `PM-015`; test SHA-256 `964e7b27b4e76efc8639a8318390478e3031629c6629726c37e1c734cf2f308e`.
- Full reads: test `1-24`; complete service `src/nvda_desk/downstream/opening.py`; opening ownership `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:152-168`; target architecture `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`.
- Raw test result: `1 passed in 0.15s`.

## G1 — `test_downstream_opening_service_surface_is_present`

- Test locator: `tests/tier_a/downstream_runtime/test_downstream_opening_service_surface.py:21-24`; assertions import one module and require one class attribute.
- Authority locator: `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:152-168` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:322-337`.
- Authority match: the module/class name is aligned with the downstream opening owner, but the cited propositions require routed opening, placement-readiness and non-executing handoff behaviour.
- Behaviour proved: the downstream-opening module imports and exposes the exact `DownstreamOpeningService` attribute named by this presence test.
- Limitation: no capital-decision input, trace, readiness state, blocked precedence, protocol-only boundary, handoff invariant or non-execution behaviour is exercised.
- Adversarial challenge: replace the service with an empty class or a class that opens broker execution; the test remains green while the authority is violated.
- Exact-surface falsifier: remove or rename `DownstreamOpeningService`; the assertion at line `24` must fail.
- Assertion that must fail and why: at test lines `22-24`, making the module unimportable or removing/renaming `DownstreamOpeningService` triggers the helper failure or breaks the identity assertion. An empty or broker-executing class under the same name remains green because no method is called.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `RETIREMENT_RECOMMENDED_NOT_EXECUTED`; retire this Tier A presence-only file once behavioural opening/readiness/handoff tests cover the owner.

## File decision

- Groups/relationships: `1/1`.
- Final disposition: `RETIREMENT_RECOMMENDED_NOT_EXECUTED`.
- Presence is inventory evidence only and contributes no independent behavioural acceptance proof.
