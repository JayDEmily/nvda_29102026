# Semantic receipt — `tests/tier_a/persistence/test_parallel_risk_observation_store_surface.py`

- Sequence `123`, PM-015; SHA-256 `089c269a5244a1532328fab9a49ec245f9b629e91bd42975e1be6329e28bb928`.
- Read full test `1-116`, full `src/nvda_desk/persistence/parallel_risk_observations.py`, directly exercised serial/Parallel Risk packet construction, current transaction/replay authority and PM-011 routes. Targeted run contribution: four tests passed inside `25 passed in 0.26s`.

## G1 — observation construction and private append state

- Locator `39-67` proves one record builder carries selected input/output packet IDs, source time, persisted time and a bounded output summary into one in-memory append.
- The test reads `store.__dict__["_records"]` directly. It does not prove a public retrievable evidence contract, typed persisted schema, durability, atomic command/state/receipt commit, idempotency binding or authoritative replay availability required by `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:17-76,145-217`.
- Relation `related_but_not_proved`; strength `behavioural_private_state`.

## G2 — no public readback by exact method names

- Locator `70-76` proves `append_observation` exists and three exact readback names do not.
- This conflicts with authoritative replay's retrievable-evidence requirement rather than proving a lawful persistence boundary. Renamed/private readback remains possible, while the test itself bypasses the public surface through `__dict__`.
- Relation `contradictory_boundary`; strength `name_blacklist`.

## G3 — duplicate observation-ID rejection

- Locator `79-96` proves the second append of the same record raises for one normalised ID path.
- It does not bind idempotency to source input/result/state or prove atomicity with any owner transaction; a duplicate semantic observation with a new ID remains accepted.
- Relation `related_but_not_proved`; strength `behavioural`.

## G4 — receipt packet-ID list detachment

- Locator `99-116` proves caller mutation of the record's packet-ID lists does not mutate the returned receipt lists.
- This is a useful copy-boundary regression, but does not establish preserved packet availability, content integrity, version identity or replay completeness.
- Relation `related_but_not_proved`; strength `behavioural`.

## File decision

- Groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Preserve selected temporal/packet carriage, duplicate-ID and copy-detachment clauses. Repair requires a public typed evidence-retrieval contract, explicit non-durable status or durable implementation, transaction/idempotency semantics and proof that the exact branch products are retrievable for replay without private-state inspection.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
