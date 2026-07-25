# Semantic receipt — `tests/tier_a/persistence/test_position_repository_surface.py`

- Sequence `125`, PM-015; SHA-256 `0d3fd39f7fc0a0444721fe90742b89618f457b4d9255f41d848ac0bd2506c7b5`.
- Read full test `1-92`, full `src/nvda_desk/repositories/position_repository.py`, current live-position and persistence/transaction authority and PM-011 routes. Targeted run contribution: five tests passed inside `25 passed in 0.26s`.

## G1 — duplicate rejection and write/read copy boundary

- Locator `8-25` proves one ID cannot be written twice and nested caller/readback mutation does not alter the stored arbitrary mapping.
- It does not prove typed position identity, authorised writer, inventory invariants, transaction/receipt atomicity, durability or idempotency.
- Relation `related_but_not_proved`; strength `behavioural`.

## G2 — insertion-order snapshot listing

- Locator `28-36` proves two arbitrary mappings are listed in insertion order and list mutation is detached.
- Ordering and copy safety are local repository behaviour, not proof of canonical live inventory or replay sequence.
- Relation `related_but_not_proved`; strength `behavioural`.

## G3 — identifier-bearing record read/list copy safety

- Locator `39-56` proves one stored mapping can be returned with its normalised ID and detached nested content.
- The repository still accepts any mapping and does not bind source fill, command, receipt, version or state transition identity.
- Relation `related_but_not_proved`; strength `behavioural`.

## G4 — ID normalisation and duplicate rejection

- Locator `59-69` proves whitespace normalisation, empty-ID rejection and duplicate detection after normalisation.
- This is a bounded identifier regression only; it does not establish globally governed position identity or replay/idempotency semantics.
- Relation `related_but_not_proved`; strength `behavioural`.

## G5 — replacement copy boundary

- Locator `72-92` proves an existing mapping is replaced by ID and detached from caller/readback mutation.
- It does not prove that replacement is an authorised state transition, atomically attested, sequence-safe or replayable. Unvalidated exposure and provenance fields are accepted directly from the caller.
- Relation `related_but_not_proved`; strength `behavioural`.

## File decision

- Groups/relationships `5/5`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Preserve the exact process-memory ID, order and copy regressions. Current authority explicitly classifies live-position persistence as a thin, non-durable seam; promotion requires typed state, semantic owner/writer, transition, transaction, receipt, durability and replay evidence.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
