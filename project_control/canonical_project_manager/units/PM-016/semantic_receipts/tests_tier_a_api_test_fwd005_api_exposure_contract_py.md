# Semantic receipt — `tests/tier_a/api/test_fwd005_api_exposure_contract.py`

- Sequence `133`, PM-016; SHA-256 `7d170762e8b2c3357ed5bb567645beb99a460c347b8dd5657aaec122495f2f9f`.
- Read full test `1-95`, full `src/nvda_desk/api/app.py` and `src/nvda_desk/api/deps.py`, directly exposed repositories/services, current API composition/ownership law and PM-011 route. Targeted run contribution: three tests passed inside `17 passed in 0.66s`.

## G1 — cached dependency objects and classifier specimen

- Locator `16-30` proves selected providers return process-global cached instances and one classifier returns one of five labels.
- Object identity does not prove lawful composition or absence of domain logic. The API dependency module directly constructs persistence, risk, paper-broker, carry and review services; several are mutable/global or operationally ungoverned.
- Relation `contradictory_composition`; strength `behavioural_identity`.

## G2 — route inventory and stateful CRUD

- Locator `33-73` proves twenty-three named handlers are registered and three caller-authored mappings can be created/listed through the app.
- Current architecture states API routes own transport/composition only. These handlers create session, event and module identities/state directly from untyped mappings, exposing semantic and persistence behaviour through the API shell.
- Route-name coverage does not prove lawful contracts or ownership.
- Relation `contradicts_api_ownership`; strength `behavioural`.

## G3 — configuration, authority-event and replay endpoints

- Locator `76-95` proves selected config/strategy reads, caller-authored veto/risk events, score ranking, evaluation record creation and phase-list echoing.
- The API shell exposes unversioned policy/config, creates authority-labelled events from strings, and labels score sorting/phase echo as replay. It does not prove typed ownership, authorised writers, preserved evidence, isolated execution or side-effect boundaries.
- Relation `contradicts_api_ownership_and_replay`; strength `behavioural_specimen`.

## File decision

- Groups/relationships `3/3`; final `BLOCKED_P3_REPAIR`.
- This file proves broad internal exposure, not the required bounded API boundary. Repair requires typed DTOs, lawful composition roots and owner services; API routes must not create domain identity/persistence truth or relabel CRUD/score sorting as authority/replay behaviour.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
