# Semantic receipt — `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py`

## File evidence

- Sequence `091`, unit `PM-014`; test SHA-256 `f5a479dafd1fbbd624bc1690cd9af865b5b264f1b911ea9491ccd80078d2ecb9`.
- Full reads: test `1-107`; fixture corpus `src/nvda_desk/testing/fixture_corpus.py:1-114`; cognition fixtures `src/nvda_desk/testing/cognition_fixtures.py:1-30`; replay sidecars `src/nvda_desk/analysis/replay/sidecar.py:1-81`; proof block `config/proof_blocks.yaml:809-820`; testing limits `docs/08.1_TESTING_AND_PROMOTION_WORKING.md:13-36,59-73`; replay limitations `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:215-217`.
- Raw test result: `4 passed in 0.16s`.

## G1 — `test_fixture_parsers_are_strict_and_optional_where_named`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:30-40`; assertions cover five parse results and two missing-required failures.
- Authority locator: `config/proof_blocks.yaml:809-820`; no higher proposition assigns runtime semantic authority to these test parsers.
- Authority match: strict deterministic fixture parsing is useful proof infrastructure, not trading/runtime authority.
- Behaviour proved: the exercised date/decimal/integer values parse as asserted and required empty date/price values fail.
- Limitation: malformed formats, ranges, precision, locale and every optional/required combination are not covered.
- Adversarial challenge: accept an invalid but non-empty date or lossy decimal elsewhere while all assertions remain green.
- Exact-surface falsifier: change one asserted parse result or permit a required empty value so an assertion at lines `31-40` fails.
- Assertion that must fail and why: at test lines `31-40`, returning a different date, decimal or integer, returning a value for either optional blank, or accepting either required blank without a matching `ValueError` breaks an exact assertion. Non-empty malformed values outside these two required examples are not comprehensively covered.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `boundary`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as deterministic fixture-parser evidence only.

## G2 — `test_legacy_fixture_loaders_parse_csv_and_jsonl`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:43-77`; assertions compare one CSV row and one JSONL row to typed test fixtures.
- Authority locator: `NO_VALID_AUTHORITY_RELATIONSHIP` for legacy fixture content as current domain/runtime truth.
- Authority match: the loaders are test-only historical evidence surfaces.
- Behaviour proved: the two temporary fixture files parse into the asserted dataclass values.
- Limitation: donor semantics, source authenticity, duplicate handling, headers and broader corpus completeness are unproved.
- Adversarial challenge: misinterpret an unsupported option type or extra column while this single row remains green.
- Exact-surface falsifier: alter one parsed field so the equality assertion at lines `59-77` fails.
- Assertion that must fail and why: at test lines `59-77`, changing any parsed field in the single CSV option row or single JSONL VWAP case makes the list-to-dataclass equality fail. Extra records, unsupported headers and other option types remain outside this specimen.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `historical_observational`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as legacy-fixture parsing evidence, never as live authority.

## G3 — `test_cognition_fixtures_are_named_test_only_specimens`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:80-88`; assertions check object type and four fixture labels.
- Authority locator: `docs/09.1_DMPV3_PROTOCOL_WORKING.md:31-37` for explicitly test-owned deterministic specimen identities.
- Authority match: named test-only fixtures are lawful, but their regime/posture labels do not establish domain policy.
- Behaviour proved: the two helper functions return the asserted fixture IDs and labels.
- Limitation: no serial cognition behaviour, input validity or expected output is exercised.
- Adversarial challenge: return arbitrary payloads under the same labels while all assertions remain green.
- Exact-surface falsifier: change one asserted fixture ID/label so an assertion at lines `84-88` fails.
- Assertion that must fail and why: at test lines `84-88`, returning a non-`CognitionRuntimeFixture`, changing either asserted fixture ID, changing the supportive regime label, or changing the stressed posture label breaks a direct assertion. The unasserted payload and actual cognition behaviour may still be arbitrary.
- Semantic relation: `bounded_separable_clause`.
- Proof strength: `specimen_only`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; retain as test-owned specimen inventory only.

## G4 — `test_research_promotion_and_evaluation_sidecars_are_append_only_and_copy_safe`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:91-107`; assertions test one research-note copy boundary and presence of one promotion, evaluation and experiment record.
- Authority locator: `config/proof_blocks.yaml:809-820`; `NO_VALID_AUTHORITY_RELATIONSHIP` for these in-memory sidecars as durable promotion/evaluation authority.
- Authority match: append/copy-safe analysis sidecars are useful partial proof, but current replay surfaces are explicitly non-authoritative and this group does not exercise persistence/restart.
- Behaviour proved: mutating a listed research-note copy does not alter stored state, and the three other records can be appended/read in process.
- Limitation: duplicate rejection, copy safety for every service, ordering, transactions, persistence, restart and authoritative promotion meaning are unproved.
- Adversarial challenge: lose all rows on restart or return mutable promotion payloads while the current assertions remain green.
- Exact-surface falsifier: expose the stored research note to mutation or fail to return one asserted record so an assertion at lines `95-107` fails.
- Assertion that must fail and why: at test lines `95-107`, returning the stored research-note object by reference changes the second title read and fails; not returning the asserted promotion decision, evaluation run or experiment run breaks its equality. Duplicate handling, restart durability and copy safety for the other record types are not exercised here.
- Semantic relation: `related_but_not_proved`.
- Proof strength: `state_transition`.
- Disposition and return gate: `ADMIT_TIER_B_SHADOW`; return to Tier A only with full duplicate/copy/order and durable state proof under owned contracts.

## File decision

- Groups/relationships: `4/4`.
- Final disposition: `ADMIT_TIER_B_SHADOW`.
- Retain this FWD002 file as partial test-infrastructure/analysis evidence. It does not establish live cognition, authoritative promotion or durable replay state.
