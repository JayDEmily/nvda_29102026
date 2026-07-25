# Semantic receipt — `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py`

## File evidence

- Sequence `073`, unit `PM-014`; test SHA-256 `5d277b38d12979ac5014e81ca9512711b01634b0e894a2ad612f0ff9e16ee445`.
- Full reads: test `1-83`; assembler `src/nvda_desk/domain/parallel_risk/minute_profile_assembly.py:1-158`; directly invoked envelope, atom and aggregation modules and Parallel Risk contracts; Parallel Risk authority `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; P1 decisions `project_control/canonical_project_manager/units/PM-010/P1_INTEGRATED_SEMANTIC_REGISTER.tsv:121-122`.
- Raw test result: `2 passed in 0.14s`.

## G1 — `test_minute_profile_assembly_preserves_current_envelope_and_authority_flags`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py:13-67`; assertions at lines `48-67` cover profile type, caution state, false flags, three atom families, five signals, lineage and an empty forbidden-key list.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66` and `docs/11_NATIVE_ARCHITECTURE_BLUEPRINT_CORE.md:254-269`; `NO_VALID_AUTHORITY_RELATIONSHIP` for the Minute Profile, asserted atom families, signal snapshot schema and authority-flag surface.
- Authority match: an independent environment envelope and explicit lineage are normatively compatible, but the exact profile product and nested taxonomy are not established by those propositions.
- Behaviour proved: the fixture produces a caution-labelled profile containing the asserted families, signal IDs and supplied parent/dependency/source identities.
- Limitation: false flags and an empty forbidden-key list are declarations; the test does not prove no side effects or hidden reads, and it exercises one profile state only.
- Adversarial challenge: the assembler could form a candidate, call a capital service, add an unasserted action field or misclassify another input while all assertions remain green.
- Exact-surface falsifier: omit one asserted signal/family or alter an asserted lineage value so an assertion at lines `52-66` fails; this falsifies the specimen, not the missing profile authority.
- Assertion that must fail and why: lines `52-59` fail if the fixture loses any asserted atom family or signal ID, and lines `63-65` fail if parent, dependency or source-artifact lineage changes. Lines `50-51` and `66` only inspect values written into the profile; they do not fail when the assembler performs an unobserved candidate, capital or hidden-read side effect.
- Semantic relation: `authority_missing`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return after proposition-level and vocabulary admission of the profile, atom/family and snapshot semantics with behavioural authority rejection.

## G2 — `test_minute_profile_assembly_contains_no_trade_action_fields`

- Test locator: `tests/tier_a/parallel_risk/test_parallel_risk_minute_profile_assembly.py:70-83`; assertion loop at lines `81-83` checks absence of seven selected strings from one JSON payload.
- Authority locator: `docs/02_BRIEFING_AND_EXECUTION_OPERATING_MODEL_CORE.md:58-66`; `NO_VALID_AUTHORITY_RELATIONSHIP` for using finite token absence as complete proof of Parallel Risk non-authority.
- Authority match: the intended no-trade boundary aligns with normative law, but the proof method does not exercise executable authority or schema rejection.
- Behaviour proved: the seven literal strings are absent from the serialised minimal profile specimen.
- Limitation: aliases, renamed fields, nested instructions, numeric order parameters, callbacks and side effects can evade the token list.
- Adversarial challenge: add `execute_position`, `quantity` or a broker callback without any listed token; every assertion remains green.
- Exact-surface falsifier: insert one listed literal such as `brokerage_order` into the serialised fixture so the corresponding loop assertion at line `83` fails.
- Assertion that must fail and why: the loop assertion at line `83` fails only when one of the seven exact strings appears in the JSON payload. A differently named action carrier or an external broker/capital call leaves every iteration green, so the group cannot establish the title's complete no-action claim.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `token_only`.
- Disposition and return gate: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`; return with owned profile semantics and structural rejection/side-effect tests rather than selected-token absence.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve the envelope, signal and lineage observations as implementation evidence; do not admit the unowned Minute Profile and atom/family taxonomy into Tier A.
