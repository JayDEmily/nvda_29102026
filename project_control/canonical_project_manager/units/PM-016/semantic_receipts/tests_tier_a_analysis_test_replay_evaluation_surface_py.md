# Semantic receipt — `tests/tier_a/analysis/test_replay_evaluation_surface.py`

- Sequence `130`, PM-016; SHA-256 `20fcdf7e9c520d486e29199022762cca06dde9f412f63e1f4f50be82465e2410`.
- Read full test `1-80`, full `src/nvda_desk/analysis/replay/service.py`, replay contracts, current authoritative replay/comparison authority and PM-011 routes. Targeted run contribution: two tests passed inside `17 passed in 0.66s`.

## G1 — package/service symbol presence

- Locator `43-52` proves the current import paths and four exact exported symbols exist.
- Presence and naming do not establish replay authority, source availability, controlled execution, comparison subordination or side-effect isolation.
- Relation `not_proved`; strength `presence_only`.

## G2 — fixture-path description, dictionary comparison and lineage container

- Locator `55-80` proves a fixed fixture-root description, top-level dictionary key comparison, caller-supplied packet-ID/run-ID carriage, absence of one `analysis/scenarios` path and no direct imports of that exact package.
- These are valid comparison/helper observations. They do not retrieve or validate packet content, versions, state, executable meaning or outputs; `ReplayPacketLineage` accepts caller IDs without availability proof. Path/import absence does not prove analysis-only behaviour or no live effects.
- Current authority explicitly keeps comparison subordinate and labels present mapping/review analysis surfaces non-authoritative.
- Relation `comparison_only_observation`; strength `behavioural_plus_structural`.

## File decision

- Groups/relationships `2/2`; final `NON_AUTHORITATIVE_OBSERVATIONAL`.
- Preserve deterministic key comparison, copy behaviour and lineage-container regressions as comparison-only evidence. Do not use this file to prove authoritative replay or analysis isolation without retrievable evidence, exact executable re-execution, controlled time and side-effect instrumentation.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
