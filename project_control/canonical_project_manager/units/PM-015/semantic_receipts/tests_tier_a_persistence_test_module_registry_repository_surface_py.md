# Semantic receipt — `tests/tier_a/persistence/test_module_registry_repository_surface.py`

- Sequence `122`, PM-015; SHA-256 `ccefabc591bae5336a03bf4257e89f75a793d1f6f9974c76d7b0c094a666d47f`.
- Read full test `1-48`, full `src/nvda_desk/repositories/module_registry.py`, current repository/persistence authority and PM-011 routes. Targeted run contribution: all three tests passed inside `25 passed in 0.26s`.

## G1 — identifier validation and duplicate rejection

- Locator `8-17` proves empty-ID rejection and duplicate rejection for the exercised in-memory store.
- It does not prove a governed module identity model, typed record schema, authorised writer, durability, transaction or idempotency semantics.
- Relation `related_but_not_proved`; strength `behavioural`.

## G2 — deep-copy storage and readback

- Locator `20-41` proves nested caller mutation and readback mutation do not alter one stored mapping.
- This is useful process-memory copy-boundary evidence only. Arbitrary mappings remain accepted, and no current proposition makes this repository authoritative module-registry state.
- Relation `related_but_not_proved`; strength `behavioural`.

## G3 — absence of four named promotion methods

- Locator `44-48` proves only that four exact attributes are absent.
- Renamed, indirect or externally composed promotion authority remains unobserved; a harmless same-name method would fail. This is lexical API-shape checking, not behavioural non-authority proof.
- Relation `not_proved`; strength `name_blacklist`.

## File decision

- Groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Preserve G1-G2 as non-authoritative repository regressions. Replace the finite method-name blacklist with behavioural ownership/instrumentation proof, and add typed identity, owner, durability and transaction clauses before Tier-A promotion.
- No project surface outside this receipt and ledger row was mutated.
