# Reconstructed semantic receipt — `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py`

- Sequence `091`, PM-014; test SHA-256 `f5a479dafd1fbbd624bc1690cd9af865b5b264f1b911ea9491ccd80078d2ecb9`.
- Reconstruction status: the original untracked receipt was unavailable after runtime turnover. This replacement was recreated from the surviving sequence-120 ledger decision, mechanical full-file extraction of the current test and its direct imports, the retained prior progress record, and the retained reconstruction validation run `RECONSTRUCTION_PYTEST_SEQ067_120.txt` (`227 passed in 1.43s`). It is not represented as byte-identical to the lost original receipt.
- Mechanically enumerated direct imports/surfaces: nvda_desk.analysis.replay.sidecar: EvaluationRunService, PromotionDecisionService, ResearchNoteService; nvda_desk.testing.cognition_fixtures: CognitionRuntimeFixture, stressed_runtime_fixture, supportive_runtime_fixture; nvda_desk.testing.fixture_corpus: LegacyOptionFixtureRow, LegacyVwapCase, load_legacy_option_fixture_rows, load_legacy_vwap_cases, parse_date_optional, parse_date_required, parse_decimal_optional, parse_decimal_required, parse_int_optional.
- Surviving decision summary: Parser/loaders and named fixtures are bounded specimens. The material sidecar claim is underproved: only one research list-copy mutation is tested; duplicate rejection, ordering, copy-on-write/read across other services, serialisability and explicit process-memory non-durability are absent.

## Complete test restatement

- Lines `30-40` `test_fixture_parsers_are_strict_and_optional_where_named`: executes the named specimen/boundary and observes checks at lines `31, 32, 33, 34, 35, 37, 39`. The exact assertions are enumerated in the relationship sections below.
- Lines `43-77` `test_legacy_fixture_loaders_parse_csv_and_jsonl`: executes the named specimen/boundary and observes checks at lines `59, 70`. The exact assertions are enumerated in the relationship sections below.
- Lines `80-88` `test_cognition_fixtures_are_named_test_only_specimens`: executes the named specimen/boundary and observes checks at lines `84, 85, 86, 87, 88`. The exact assertions are enumerated in the relationship sections below.
- Lines `91-107` `test_research_promotion_and_evaluation_sidecars_are_append_only_and_copy_safe`: executes the named specimen/boundary and observes checks at lines `95, 101, 106, 107`. The exact assertions are enumerated in the relationship sections below.
- Surfaces not established by the file are those identified in the surviving decision summary: exact current authority for promoted policy/taxonomy where missing, unobserved aliases or indirect paths, complete lineage/replay/transaction semantics, and any behavioural non-authority claim represented only by labels, flags, names, paths or token absence.

## G1 — `test_fixture_parsers_are_strict_and_optional_where_named`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:30-40`. Checks: L31 assert `parse_date_required("2026-05-15").isoformat() == "2026-05-15"`; L32 assert `parse_date_optional("") is None`; L33 assert `parse_decimal_required("1.25") == Decimal("1.25")`; L34 assert `parse_decimal_optional(None) is None`; L35 assert `parse_int_optional("7") == 7`; L37 raises `pytest.raises(ValueError, match="trade_date")`; L39 raises `pytest.raises(ValueError, match="price")`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Parser/loaders and named fixtures are bounded specimens. The material sidecar claim is underproved: only one research list-copy mutation is tested; duplicate rejection, ordering, copy-on-write/read across other services, serialisability and explicit process-memory non-durability are absent.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `boundary`; file disposition `BLOCKED_P3_REPAIR`.

## G2 — `test_legacy_fixture_loaders_parse_csv_and_jsonl`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:43-77`. Checks: L59 assert `option_rows == [ LegacyOptionFixtureRow( trade_date=parse_date_required("2026-05-15"), expiry=parse_date_required("2026-06-19"), strike=Decimal("120.5"), option_type="call", bid=Decimal("1.10"), ask=Decimal("1.20"), volume=100, ) ]`; L70 assert `vwap_cases == [ LegacyVwapCase( case_id="v1", trade_date=parse_date_required("2026-05-15"), vwap=Decimal("125.50"), volume=1000, ) ]`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Parser/loaders and named fixtures are bounded specimens. The material sidecar claim is underproved: only one research list-copy mutation is tested; duplicate rejection, ordering, copy-on-write/read across other services, serialisability and explicit process-memory non-durability are absent.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G3 — `test_cognition_fixtures_are_named_test_only_specimens`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:80-88`. Checks: L84 assert `isinstance(supportive, CognitionRuntimeFixture)`; L85 assert `supportive.fixture_id == "supportive_runtime"`; L86 assert `supportive.market_regime_context == "supportive"`; L87 assert `stressed.fixture_id == "stressed_runtime"`; L88 assert `stressed.risk_posture == "stressed"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Parser/loaders and named fixtures are bounded specimens. The material sidecar claim is underproved: only one research list-copy mutation is tested; duplicate rejection, ordering, copy-on-write/read across other services, serialisability and explicit process-memory non-durability are absent.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `behavioural`; file disposition `BLOCKED_P3_REPAIR`.

## G4 — `test_research_promotion_and_evaluation_sidecars_are_append_only_and_copy_safe`

- Test locator: `tests/tier_a/testing_harnesses/test_fwd002_fixture_and_sidecar_contract.py:91-107`. Checks: L95 assert `research.list_research_notes()[0]["title"] == "Observed"`; L101 assert `promotions.list_promotion_decisions()[0]["decision"] == "promote"`; L106 assert `runs.list_evaluation_runs()[0]["run_id"] == "eval-1"`; L107 assert `runs.list_experiment_runs()[0]["run_id"] == "exp-1"`
- Observed behaviour: the test fixes the exact values, exception, structure, path, field, copy/order result or token condition named above. This is bounded evidence for the exercised specimen only.
- Authority assessment: a related current boundary exists, but this group under-observes it or preserves a contradictory implementation detail. Exact fields or exceptions may be useful, while renamed, indirect, nested, transactional, lineage or side-effect violations remain outside the asserted surface.
- What is not proved: Parser/loaders and named fixtures are bounded specimens. The material sidecar claim is underproved: only one research list-copy mutation is tested; duplicate rejection, ordering, copy-on-write/read across other services, serialisability and explicit process-memory non-durability are absent.
- Adversarial challenge: an implementation can preserve these exact asserted literals, fields, paths, exceptions or selected state while violating the unobserved authority boundary identified above. Only the named exact assertion would necessarily fail; a semantically equivalent alias, indirect dependency, hidden mutation, fabricated identity, incomplete policy or omitted lifecycle condition could remain green.
- Semantic relation `related_but_not_proved`; proof strength `state_transition`; file disposition `BLOCKED_P3_REPAIR`.

## File decision

- Assertion groups/relationships `4/4`; final `BLOCKED_P3_REPAIR`.
- Return gate: preserve only the exact bounded clauses described by the checks. Tier-A promotion requires the missing current proposition or P3 repair that makes the test observe the actual behavioural, identity, lineage, replay, transaction or non-authority boundary rather than a specimen, name, flag or token proxy.
- No source, test, configuration, normative document, registry or proof-block mutation was executed during reconstruction.
