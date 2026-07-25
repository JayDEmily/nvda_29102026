# Semantic receipt — `tests/tier_a/api/test_api_dto_boundary_surface.py`

- Sequence `132`, PM-016; SHA-256 `91af6dab97f549ed78b82fbe8e8efc4818b5d1ab776e177df195882adfc0d66e`.
- Read full test `1-90`, full `src/nvda_desk/adapters/egress/api_dto_adapter.py`, API application/dependency wiring, current API/review-export boundary law and PM-011 routes. Targeted run contribution: two tests passed inside `17 passed in 0.66s`.

## G1 — DTO adapter/dependency presence

- Locator `21-37` proves one adapter class, cached provider and three method names exist.
- The methods all accept `Any` and return untyped dictionaries through the same generic coercion. Presence does not prove explicit public DTO schemas, field allow-lists, versioning or prevention of private/domain-state leakage.
- Relation `not_proved`; strength `presence_only`.

## G2 — injected adapter call path

- Locator `40-90` proves an injected recording adapter receives the health mapping and one stub runtime mapping, and its returned dictionaries are propagated.
- This is useful composition-injection evidence, but the stub bypasses governed runtime contracts and the adapter performs no semantic field projection. The test title calls the owner admitted without an exact current proposition for these three DTO categories.
- A DTO adapter that leaks every private field satisfies all assertions.
- Relation `related_but_not_proved`; strength `behavioural_composition_specimen`.

## File decision

- Groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Preserve dependency injection and call-routing evidence. Tier-A promotion requires versioned typed runtime/review/state DTO contracts, explicit field projection/redaction and proof that API transport cannot become domain mapping or persistence authority.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
