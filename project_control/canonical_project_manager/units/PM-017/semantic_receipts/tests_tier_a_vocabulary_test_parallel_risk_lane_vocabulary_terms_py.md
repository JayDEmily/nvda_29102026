# Semantic receipt — `tests/tier_a/vocabulary/test_parallel_risk_lane_vocabulary_terms.py`

- Sequence `153`, PM-017; SHA-256 `5dda589d5486f82146f4ed4eaf25ff9421a48e0b1d8995f8bd88449bc0280797`.
- Read full test `1-25`, all seven referenced P1 decisions and the current projection. Targeted run: `1 failed` because `candidate_audit` is absent.

## G1 — seven Parallel Risk vocabulary terms are required as canonical projections

- Locator `7-25` correctly covers five admitted records: `environment_assessment`, `dependency_packet_ids`, `parallel_risk_observation_store`, `write_only_persistence`, and `append_only_observation_record`.
- It also requires `candidate_audit` and `stage_read_state`. P1 explicitly quarantines both for missing higher normative authority and removes them from the canonical projection. Requiring them reverses accepted semantic decisions; the red result is correct evidence of that contradiction, not an implementation gap.
- Relation `authority_contradictory`; strength `presence_only`.

## File decision

- Groups/relationships `1/1`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Repair must split admitted terms from the two quarantined terms or obtain new higher authority for each quarantined meaning. The current test must not force them back into canonical vocabulary.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
