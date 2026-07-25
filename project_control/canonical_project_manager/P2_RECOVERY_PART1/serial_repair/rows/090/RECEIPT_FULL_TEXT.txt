# Semantic receipt — `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py`

## File evidence

- Sequence `090`, unit `PM-014`; test SHA-256 `a698381377a9785a6748fc183bc860f5abddfc35df8765f80f6e858e8af6746e`.
- Full reads: test `1-58`; harness `src/nvda_desk/testing/harnesses/canonical_runtime.py:1-84`; replay and trace-review contracts directly exercised; fixture law `docs/09.1_DMPV3_PROTOCOL_WORKING.md:31-37`; replay limitations `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:175,215-217`; testing proof limits `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-26,59-73`.
- Raw test result: `2 passed in 0.22s`.

## G1 — `test_canonical_runtime_specimen_surface_is_present`

- Test locator: `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py:22-31`; assertions require package/module and four exported symbols.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for symbol presence as canonical runtime proof.
- Authority match: a test-only harness may lawfully exist, but importability does not prove replay, trace or runtime semantics.
- Behaviour proved: the named module and symbols are currently importable.
- Limitation: no functional, replay, identity or isolation behaviour is exercised.
- Adversarial challenge: expose stubs that return arbitrary values while all assertions remain green.
- Exact-surface falsifier: remove one module/symbol so an assertion at lines `23-31` fails.
- Assertion that must fail and why: at test lines `23-31`, making either module unimportable triggers `_require_module`, and deleting or renaming any required export triggers `_require_attr` or breaks the identity comparison. A callable stub with no valid replay or fixture behaviour still passes this presence surface.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `presence_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as test-harness inventory evidence only.

## G2 — `test_canonical_runtime_specimen_surface_stays_test_only_and_fixture_backed`

- Test locator: `tests/tier_a/testing_harnesses/test_canonical_runtime_specimen_surface.py:34-58`; assertions cover fixture-root names, packet/scenario IDs and absence of two runtime import strings.
- Authority locator: `docs/09.1_DMPV3_PROTOCOL_WORKING.md:31-37` and `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:215-217`.
- Authority match: deterministic test-owned fixture identity is lawful, and current replay surfaces are explicitly non-authoritative comparison seams; the group fits shadow evidence, not authoritative replay.
- Behaviour proved: one built specimen uses the asserted fixture-root names and retains supplied IDs; source text lacks two selected imports.
- Limitation: no fixture content is retrieved/fingerprint-verified, no original decision is replayed, and token absence does not prove isolation from live runtime.
- Adversarial challenge: access live state through another import/helper or provide missing fixture roots while retaining all asserted names.
- Exact-surface falsifier: change an asserted root/ID or insert one listed import string so an assertion at lines `52-58` fails.
- Assertion that must fail and why: at test lines `52-58`, changing any of the three fixture-root basenames, dropping either supplied packet ID or the scenario ID, or inserting either exact prohibited import string into `canonical_runtime.py` breaks a direct assertion. The test does not open the fixture roots, verify content fingerprints or detect access through another module.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; return to Tier A only with authoritative fixture retrieval, fingerprint validation, isolated execution and complete dependency proof.

## File decision

- Groups/relationships: `2/2`.
- Final disposition: `ADMIT_TIER_B_SHADOW`.
- Retain as a bounded non-authoritative harness/specimen surface. It does not establish canonical runtime or authoritative replay.
