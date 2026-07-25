# Semantic receipt — `tests/tier_a/persistence/test_receipt_ledger_surface.py`

- Sequence `126`, PM-015; SHA-256 `f1193c1f9702a88f0c8c23c7845a42aad6c09d9685a06a3cf38b65182e4bf624`.
- Read full test `1-104`, full `src/nvda_desk/persistence/receipt_ledger.py`, current transaction/receipt and alpha persistence authority and PM-011 routes. Targeted run contribution: five tests passed inside `25 passed in 0.26s`.

## G1 — append order, ID uniqueness and copy safety

- Locator `10-33` proves two JSON-compatible arbitrary payloads are stored in insertion order, detached from caller/readback mutation, and duplicate exact IDs are rejected.
- It does not prove a typed attestation, authorised transaction participant, atomic state-and-receipt commit, durable storage or idempotency tied to command/input/result/state.
- Relation `related_but_not_proved`; strength `behavioural`.

## G2 — point read copy safety and missing result

- Locator `36-54` proves one ID lookup returns a detached mapping and a missing ID returns `None`.
- This is local container behaviour, not proof that the receipt attests preserved authoritative evidence or is retrievable across process/runtime boundaries.
- Relation `related_but_not_proved`; strength `behavioural`.

## G3 — token and JSON-serialisability rejection

- Locator `57-65` proves blank ID/kind rejection and rejection of one non-JSON `datetime` payload.
- JSON serialisability is transport compatibility, not semantic receipt completeness, source/version identity, immutability or durability.
- Relation `related_but_not_proved`; strength `behavioural_schema`.

## G4 — whitespace normalisation and post-normalisation uniqueness

- Locator `68-79` proves ID/kind trimming and duplicate detection after trimming.
- It does not establish a governed receipt-ID namespace or replay/idempotency identity.
- Relation `related_but_not_proved`; strength `behavioural`.

## G5 — kind-filtered listing

- Locator `81-104` proves exact string-kind filtering, append order and copy detachment for two selected kinds.
- Receipt kind remains an ungoverned caller string; the test does not prove that `live_inventory_reconciliation` corresponds to a lawful transaction or evidence class.
- Relation `related_but_not_proved`; strength `behavioural_specimen`.

## File decision

- Groups/relationships `5/5`; final `BLOCKED_P3_REPAIR`.
- The implementation is an in-memory list despite its module/class durability language. Preserve local append/order/copy/validation regressions, but repair the durability claim and add typed receipt semantics, semantic owner, atomic state transaction, idempotency and retrievable replay evidence before Tier-A admission.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
