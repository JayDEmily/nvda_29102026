# Semantic receipt — `tests/tier_a/adapters_egress/test_broker_boundary_surface.py`

- Sequence `128`, PM-016; SHA-256 `3f929592bb82bf058bc93360e4b814f544755f44bb7bd7dc81d1e2af99b8abf8`.
- Read full test `1-42`, full `src/nvda_desk/adapters/egress/broker_protocol.py`, current Broker Protocol vocabulary authority, opening/placement boundary and PM-011 routes. Targeted run contribution: two tests passed inside `17 passed in 0.66s`.

## G1 — protocol surface and four method names

- Locator `21-34` proves the module exports one protocol under two aliases and declares four callable method attributes.
- This aligns with the canonical `Broker Protocol` as a protocol-only boundary, but the methods use open `Mapping[str, Any]`/`Sequence[Mapping]` shapes and do not prove governed message schemas, credentials isolation, submission mode, receipt identity or separation from concrete execution.
- Relation `bounded_clause_partially_proved`; strength `structural_contract`.

## G2 — absence of two concrete adapter names

- Locator `37-42` proves only `PaperBrokerAdapter` and `LiveBrokerAdapter` are absent from that module.
- Renamed, imported, indirect or composed concrete execution remains unobserved; a harmless class with either name would fail. This is lexical absence, not behavioural closure of broker execution authority.
- Relation `not_proved`; strength `name_blacklist`.

## File decision

- Groups/relationships `2/2`; final `BLOCKED_P3_REPAIR`.
- Preserve the protocol alias/method-shape regression. Tier-A promotion requires typed broker-boundary messages and behavioural proof that concrete adapter selection, credentials, submission and receipts remain separately owned; replace exact-name absence with dependency/composition instrumentation.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
