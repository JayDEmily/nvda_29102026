# Semantic receipt — `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py`

## File evidence

- Sequence `089`, unit `PM-014`; test SHA-256 `f037de5d9a1116e1e5cbe3ba0a8850c1be9281b003e0cb8a2d37e3884898fbe7`.
- Full reads: test `1-33`; complete specimen `var/audit/specimens/parallel_risk_envelope/sequence7_parallel_risk_envelope_expected_packet.json`; DMPV3 carriage law `docs/09_DMPV3_PROTOCOL_CORE.md:31-129`; Parallel Risk output law `docs/07_RUNTIME_OWNERSHIP_AND_CONSUMER_LEDGER_CORE.md:106-119`; testing proof limits `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-36,59-73`.
- Raw test result: `1 passed in 0.03s`.

## G1 — `test_sequence7_expected_parallel_risk_envelope_specimen_is_bounded`

- Test locator: `tests/tier_a/parallel_risk/test_sequence7_parallel_risk_envelope_specimen.py:14-33`; assertions inspect packet role/producer, state ladder, authority string, three families and token absence driven by the specimen itself.
- Authority locator: `docs/09_DMPV3_PROTOCOL_CORE.md:31-93` for packet role/producer; `NO_VALID_AUTHORITY_RELATIONSHIP` for the exact envelope taxonomy/families and specimen-authored forbidden-field list.
- Authority match: packet carriage fields align with DMPV3, but the file validates a hand-authored expected specimen rather than executing the implementation or an authoritative source.
- Behaviour proved: the checked-in JSON currently contains the asserted shape and omits its own listed strings.
- Limitation: specimen and test can agree while runtime diverges; the forbidden list is self-authored and the semantic taxonomies remain unadmitted.
- Adversarial challenge: change runtime output without updating the specimen, or omit a forbidden alias from the specimen list; the test remains green.
- Exact-surface falsifier: alter one asserted JSON field or insert a specimen-listed token so an assertion at lines `21-33` fails.
- Assertion that must fail and why: at test lines `21-33`, changing the packet role, producer role, ordered ladder, authority string or exact three-family set breaks a direct assertion; placing any string listed by the specimen itself into the serialised envelope breaks the loop. Runtime behaviour can diverge completely because this test reads only the checked-in JSON.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `NON_AUTHORITATIVE_OBSERVATIONAL`; retain as expected-shape documentation only, not blocking proof.

## File decision

- Groups/relationships: `1/1`.
- Final disposition: `NON_AUTHORITATIVE_OBSERVATIONAL`.
- The specimen is useful documentation of intended packet shape but is self-referential, non-executing and semantically dependent on unadmitted envelope taxonomies.
