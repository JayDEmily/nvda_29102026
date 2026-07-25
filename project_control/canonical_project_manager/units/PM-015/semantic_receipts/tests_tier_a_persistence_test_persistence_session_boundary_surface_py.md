# Semantic receipt — `tests/tier_a/persistence/test_persistence_session_boundary_surface.py`

- Sequence `124`, PM-015; SHA-256 `742003a1354fc7acb5a191e9e3d7d6591e231b01e927700932a279dd56662798`.
- Read full test `1-57`, full `src/nvda_desk/persistence/session_factory.py`, persistence package exports, current alpha persistence law and PM-011 routes. Targeted run contribution: three tests passed inside `25 passed in 0.26s`.

## G1 — fresh bounded in-memory session

- Locator `11-21` proves each context-manager call yields a distinct empty dict-backed session and does not carry one caller's inserted key into the next session.
- This aligns narrowly with the admitted alpha allowance for explicitly bounded process-memory infrastructure, but does not prove repository-contract substitution, rollback/commit semantics, owner transactions or explicit non-durable labelling at the contract boundary.
- Relation `bounded_clause_proved`; strength `behavioural`.

## G2 — package export blacklist

- Locator `24-38` proves the current package exports only `ReceiptLedger` and lacks five exact donor-style names.
- It does not prove persistence technology separation or absence of equivalent engine/schema/seed authority under renamed, indirect or composed surfaces.
- Relation `not_proved`; strength `name_blacklist`.

## G3 — session-module blacklist

- Locator `41-57` proves dict inheritance, one method presence and absence of seven exact names.
- A renamed or imported external engine/seed helper remains unobserved; a harmless same-name symbol would fail. This is API-shape evidence, not behavioural substitution or non-authority proof.
- Relation `not_proved`; strength `name_blacklist`.

## File decision

- Groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- Preserve G1 as a narrow non-authoritative in-memory-session regression. Replace G2-G3 with behavioural dependency/composition proof and add explicit non-durable, transaction and adapter-substitution semantics before Tier-A admission.
- No project surface outside this receipt and ledger row was mutated.
