# Semantic receipt — `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py`

- Sequence `165`, PM-017; SHA-256 `af6a20aae994bd8f1cc06d4b03d4c78791e53739b1c3db726d7142c342f6e992`.
- Read full test `1-422`, full `src/nvda_desk/vocabulary_synonym_audit.py`, candidate schema/helpers, accepted occurrence-scoped PM-010 register and docs 10.1 sections 10.3-10.6. Targeted run: `3 passed, 14 failed in 5.34s`.
- The current implementation emits occurrence mappings with path, line, column, context hash and kind. Fourteen tests monkeypatch the old two-tuple `(path, phrase)` shape, so they fail before reaching their claimed assertion.

## G1 — CLI bootstrap and check-clean read-only behaviour (58-78)
Proves the script imports without external `PYTHONPATH`, reports candidate count, returns count-dependent status and leaves the governed report unchanged. It does not prove semantic cleanliness. Relation `bounded_separable_clause`; strength `boundary`.

## G2 — touched report write and quarantine projection (81-121)
Intended to prove report creation, touched fingerprint and mechanical quarantine output. It is currently unexercised because the stale tuple fixture fails at the occurrence-mapping boundary. Relation `related_but_not_proved`; strength `behavioural`.

## G3 — stamp refuses unresolved candidates (124-146)
Intended to protect the clean-stamp gate, but the expected RuntimeError is never reached under the stale fixture. Relation `related_but_not_proved`; strength `state_transition`.

## G4 — clean stamp advancement (149-166)
Proves a zero-candidate report may write the current fingerprint. It does not prove semantic completion; docs 10.1 states a fingerprint is byte agreement only. Relation `bounded_separable_clause`; strength `state_transition`.

## G5 — near match is mechanically quarantined (169-209)
The expected occurrence-independent payload is obsolete: current authority requires occurrence ID, line and context evidence. The assertion never executes. Relation `related_but_not_proved`; strength `specimen_only`.

## G6 — compact exact token is not escalated (212-225)
Intended to prove exact compact-token suppression, but the stale tuple fixture prevents observation. Relation `related_but_not_proved`; strength `boundary`.

## G7 — similar phrase is not globally suppressed (228-246)
Matches occurrence-scoped governance in meaning, but the expected result omits required occurrence identity fields and never executes. Relation `related_but_not_proved`; strength `boundary`.

## G8 — protocol identifier fragment is ignored (249-265)
Intended heuristic-boundary proof; stale fixture prevents execution. Even when repaired, it proves only configured lexical rules, not semantic absence. Relation `related_but_not_proved`; strength `token_only`.

## G9 — protocol prose variant escalates (268-288)
Intended heuristic specimen; stale fixture and obsolete output shape prevent proof. Relation `related_but_not_proved`; strength `token_only`.

## G10 — Python declaration identifier fragment is ignored (291-301)
Intended lexical filter proof; stale fixture prevents execution. Relation `related_but_not_proved`; strength `token_only`.

## G11 — Python declaration prose variant escalates (304-322)
Intended lexical specimen; stale fixture and obsolete expected payload prevent proof. Relation `related_but_not_proved`; strength `token_only`.

## G12 — admitted aliases suppress exact occurrences globally (325-339)
This is consistent with docs 10.1 section 10.6, but the stale fixture prevents observation. Relation `related_but_not_proved`; strength `boundary`.

## G13 — governed disallowed phrase specimen is suppressed (342-358)
The test describes disallowed phrases as globally governed suppressors, contrary to current docs 10.1: disallowed phrases are not phrase-global exact tokens; only exact resolved occurrences may be suppressed. It is both stale and authority-contradictory. Relation `authority_contradictory`; strength `token_only`.

## G14 — unresolved candidate remains visible (361-379)
Meaning aligns with escalation law, but obsolete fixtures omit exact occurrence evidence and fail before assertion. Relation `related_but_not_proved`; strength `boundary`.

## G15 — check-clean blocks unresolved candidates (382-393)
Intended CLI boundary is valid, but the stale fixture prevents the return-code/output assertion. Relation `related_but_not_proved`; strength `boundary`.

## G16 — check-clean passes when candidates are governed (396-409)
The fixture again treats a disallowed phrase as globally suppressing, contradicting occurrence-scoped law, and fails before the assertion. Relation `authority_contradictory`; strength `token_only`.

## G17 — source contains no named path-bound suppression table (412-422)
Proves only absence of four source tokens. A renamed or indirect path-bound suppressor would pass; lawful code using one phrase would fail. Relation `related_but_not_proved`; strength `token_only`.

## File decision
- Groups/relationships `17/17`; final `BLOCKED_P3_REPAIR`.
- Re-author fixtures and expected payloads to the occurrence-scoped mapping contract; remove global disallowed-phrase suppression expectations; replace source-token absence with behavioural occurrence tests. Preserve G1 and G4 as narrow current evidence.
- No protected source, test, configuration, normative, registry or proof-block file was changed.
