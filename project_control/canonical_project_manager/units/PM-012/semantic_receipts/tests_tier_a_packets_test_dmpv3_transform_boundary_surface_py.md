# Semantic receipt — `tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py`

## 1. Process record
- Sequence: `018`
- Unit: `PM-012`
- Test SHA-256: `40acde2f80b7e2d69b3d5c62f65105e48fe1449eec92f2686c67f2b79a76b699`
- Test read in full: lines `1-52`.
- Exercised compatibility wrappers read in full: `src/nvda_desk/schemas/dmp.py` and `src/nvda_desk/schemas/dmp_envelope.py`; canonical packet contracts/builders reread.
- Current retained-registry and proof-block routes inspected.
- Validation: `PYTHONPATH=src python -m pytest tests/tier_a/packets/test_dmpv3_transform_boundary_surface.py -q` returned `3 passed in 0.19s`, exit `0`.

## 2. Complete file restatement
The file first proves that two named compatibility modules re-export the exact canonical packet classes and builder objects. It then checks that five specifically named donor-style service modules cannot be imported and that three specifically named local-envelope attributes are absent from four packet modules.

## 3. Authority context
`docs/09_DMPV3_PROTOCOL_CORE.md:155-165` requires live packet builders to use the canonical shell and expressly permits the two named schema modules only as compatibility wrappers. No current normative proposition establishes the five service-module strings or three class-name strings as a complete forbidden set.

## 4. Assertion group 1 — compatibility wrappers are exact aliases (`11-25`)
1. **Behaviour:** identity-compares every exported wrapper object with its canonical owner.
2. **Authority meaning:** the permitted compatibility modules must not create parallel packet grammars.
3. **Fit:** direct bounded canonical-builder/wrapper clause.
4. **Proved:** all ten tested exports are the same Python objects as their canonical definitions/builders.
5. **Not proved:** all imports across the repository use them, or every packet emission is canonical.
6. **Falsifier:** define or wrap one object independently.
7. **Required failure:** identity assertions `12-25`.
8. **Authority-violating implementation that passes:** add a different parallel grammar under another module/export.
9. **Semantic relation:** `bounded_separable_clause`.
10. **Proof strength:** `identity_lineage`.
11. **Disposition/gate:** admissible narrow alias proof.

## 5. Assertion group 2 — five donor-style module names are absent (`28-38`)
1. **Behaviour:** requires `find_spec` to return `None` for five literal module names.
2. **Authority meaning:** donor packet services should not become native authority.
3. **Fit:** related intent, but the exact blacklist is not normatively complete or admitted.
4. **Proved:** those five names are not importable in the test environment.
5. **Not proved:** absence of equivalent donor authority under renamed, indirect, dynamic or external modules.
6. **Falsifier:** create one listed module.
7. **Required failure:** assertion `38`.
8. **Authority-violating implementation that passes:** implement identical donor authority under any unlisted name.
9. **Semantic relation:** `authority_missing`.
10. **Proof strength:** `token_only`.
11. **Disposition/gate:** P3 repair required; replace blacklist inference with governed ownership/dependency behaviour.

## 6. Assertion group 3 — three donor-style class names are absent (`41-52`)
1. **Behaviour:** checks three literal attributes are absent from four modules.
2. **Authority meaning:** local envelopes must not form parallel packet classes.
3. **Fit:** related boundary intent, but exact names are not a normative exhaustive set.
4. **Proved:** the twelve name/module combinations are absent.
5. **Not proved:** no parallel packet class exists under another name or location.
6. **Falsifier:** expose one listed attribute.
7. **Required failure:** assertions `49-52`.
8. **Authority-violating implementation that passes:** add a semantically equivalent local envelope with a different name.
9. **Semantic relation:** `authority_missing`.
10. **Proof strength:** `token_only`.
11. **Disposition/gate:** P3 repair required.

## 7. File-level disposition
- Assertion groups: `3`.
- Explicit proposition relationships: `3`.
- Final disposition: `BLOCKED_P3_REPAIR`.
- Preserved proof: exact alias identity for the two normatively named compatibility wrappers.
- Blocking defect: two materially broader no-parallel-authority claims rely on non-exhaustive name blacklists and can pass renamed unlawful implementations.
- No implementation or test mutation executed.
