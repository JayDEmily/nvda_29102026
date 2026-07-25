# Semantic receipt — `tests/tier_a/normative_authority/test_gate_c_outputs_replay_and_api.py`

- Sequence `147`, PM-017; SHA-256 `077dc7678df61c0319c20e3eaa38d6ec5a2257d9b98ced0f48ff941f5e65b991`.
- Read full test `1-67`, directly exercised API, Daily P&L and replay-harness surfaces, propositions `C-021;C-041;C-043;C-047;C-048`, and Gate C admission evidence. Targeted run: `1 passed, 3 failed`, within the expected-red pack.

## G1 — API does not own untyped veto/risk-block state
- Locator `8-13` requires two private stores and two route handlers to be absent. This exact surface is proved; renamed/nested equivalents remain outside the assertion.
- Relation `bounded_separable_clause`; strength `boundary`.
## G2 — API exit/close path fails closed without upstream authority
- Locator `16-24` requires a minimal hold request to raise rather than fabricate identifiers.
- Relation `bounded_separable_clause`; strength `boundary`.
## G3 — Daily P&L report identity is idempotent and evidence IDs persist
- Locator `27-49` requires duplicate report ID rejection, one stored report, exact evidence IDs and false decision-mutation flag.
- Relation `bounded_separable_clause`; strength `state_transition`.
## G4 — replay evaluation carries dataset/window identity and cannot promote runtime authority
- Locator `52-67` requires dataset identity/fingerprint, windows and review/research-only default mode. Contract shape/default only; execution isolation is not proved here.
- Relation `bounded_separable_clause`; strength `presence_only`.

## File decision

- Groups/relationships `4/4`; final `ADMIT_TIER_A_CURRENT` under the Gate C admission receipt.
- Three current failures remain implementation obligations. The admission does not expand absence checks beyond the exact API members or treat a mode default as full behavioural isolation.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
