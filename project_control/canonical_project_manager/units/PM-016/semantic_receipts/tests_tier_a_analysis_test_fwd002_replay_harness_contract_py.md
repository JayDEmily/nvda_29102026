# Semantic receipt — `tests/tier_a/analysis/test_fwd002_replay_harness_contract.py`

- Sequence `129`, PM-016; SHA-256 `e404806a62a4b7925556da800bafdf89e308dd1bbf3977f6e8a1643705261d4c`.
- Read full test `1-138`, full `src/nvda_desk/analysis/replay/walk_forward.py`, current review/replay authority and PM-011 route. Targeted run contribution: four tests passed inside `17 passed in 0.66s`.

## G1 — window vocabularies and overlap rejection

- Locator `32-64` proves selected enum values, ordered windows, reversed-index rejection and pairwise overlap rejection for one caller-authored packet.
- Current replay authority does not establish this walk-forward taxonomy or make `WalkForwardHarnessAuthorityPacket` authoritative. It does not test strict role ordering, gaps, duplicate window IDs, dataset identity or controlled-time execution.
- Relation `unsupported_policy_taxonomy`; strength `behavioural_schema`.

## G2 — stability, horizon and comparison arithmetic

- Locator `67-95` proves one degradation calculation, threshold result, minimum-count result, ordering preservation and highest-score selection.
- Thresholds, metric meaning, baseline identity and acceptance semantics are caller-authored; no current proposition governs these policies. A fabricated score row can be accepted without source/version/state evidence.
- Relation `unsupported_policy`; strength `behavioural_specimen`.

## G3 — bucket/failure/variant helper arithmetic

- Locator `98-121` proves arithmetic and counting for in-memory helpers plus fixed default scenario and variant payload literals.
- The test name asserts absence of runtime side effects, but no runtime owner, persistence owner or mutation instrumentation is observed. Default fragility scenarios and failure labels lack current normative authority.
- Relation `not_proved`; strength `behavioural_helpers_plus_label`.

## G4 — market-row entrypoints labelled review-only

- Locator `124-138` proves three helpers convert arbitrary `candidate_id`/`score` mappings into reports and one sorts scores descending; two reports carry a `REVIEW_ONLY` enum.
- A mode label does not prove non-authority or isolation. The functions perform no governed replay: they do not retrieve source material, re-execute exact executable meaning, control time, preserve state/output evidence or assess side effects as required by `docs/07.2_STATE_RISK_AND_REPLAY_WORKING.md:145-217`.
- Relation `not_replay_proof`; strength `behavioural_specimen`.

## File decision

- Groups/relationships `4/4`; final `BLOCKED_MISSING_NORMATIVE_AUTHORITY`.
- Preserve basic chronology/arithmetic regressions as research-code evidence. Tier-A admission requires explicit authority for the walk-forward/stability/fragility policies and a test that exercises governed replay inputs, isolated execution, source/version/state/output evidence and behavioural no-side-effect assessment.
- No source, test, configuration, normative document, registry or proof-block mutation was executed.
