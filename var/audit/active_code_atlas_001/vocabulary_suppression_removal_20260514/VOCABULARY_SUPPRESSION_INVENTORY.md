# Vocabulary Suppression Inventory — pre-mutation

Scope: PM-authorised removal of source-code vocabulary synonym suppression logic.

This inventory was created before modifying source/test/config/vocabulary data. Line ranges refer to the pre-mutation file state at HEAD c8c7825.

## Summary

- Source suppression constants/tables found: 1 (`FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS`, lines 28-137).
- Source path/surface-specific suppression predicate functions found: 20 (lines 235-971, excluding generic identifier/protocol/function-declaration parsing predicates at lines 193-232).
- `score = 0` suppression branches inspected: 21 at lines 1060-1113; 19 are hard-coded/path-bound suppression branches to remove, 2 are generic parsing filters to retain.
- Tests whose purpose is to prove path-bound suppression: 34 function-level tests in `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` from lines 382-2103.

## Source-code suppression patterns

| ID | File path | Line range | Function / branch | What candidate it hides | Why previously added | Hard-coded source suppression | Required decision | Required mutation | Required tests |
|---|---|---:|---|---|---|---|---|---|---|
| VSUP-001 | src/nvda_desk/vocabulary_synonym_audit.py | 28-137, 963-971, 1112-1113 | FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS / _is_fwd001_governance_candidate_fragment | FWD-001 table of coefficient/source/playbook/calendar/risk/packet synonym candidates by exact path/raw phrase/slug | Prior FWD-001 adjudication made clean-check pass by path-bound suppression | yes | REJECT_WITH_GOVERNED_EVIDENCE or KEEP_AS_UNRESOLVED_CANDIDATE per candidate | remove table, predicate, branch; route phrases to governed vocabulary data/evidence | replace path-bound tests with governed handling tests |
| VSUP-002 | src/nvda_desk/vocabulary_synonym_audit.py | 235-248, 1060-1061 | _is_vocabulary_seed_note_relationship_fragment | `Source Temporal Standard field` in vocabulary builder notes | prior local exception for seed note wording | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase globally if false positive | test governed rejection/admission path |
| VSUP-003 | src/nvda_desk/vocabulary_synonym_audit.py | 251-261, 1062-1063 | _is_dmp_v3_fixture_root_descriptor_fragment | `DMP V3 root` in canonical runtime fixture descriptor | prior local exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-004 | src/nvda_desk/vocabulary_synonym_audit.py | 264-282, 1064-1067 | _is_baseline_only_surface_error_text_fragment | `baseline only` / baseline-only surface error text | prior error-text exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-005 | src/nvda_desk/vocabulary_synonym_audit.py | 285-300, 1068-1069 | _is_coefficient_authority_import_descriptor_fragment | `Coefficient Authority import` descriptors | prior import-descriptor exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-006 | src/nvda_desk/vocabulary_synonym_audit.py | 303-316, 1070-1073 | _is_downstream_stage_read_service_method_fragment | `read state` method name near Stage-read State | prior method-name exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test unresolved/clean-check behaviour |
| VSUP-007 | src/nvda_desk/vocabulary_synonym_audit.py | 319-338, 1074-1077 | _is_coefficient_authority_service_accessor_fragment | `coefficient_authority_service` path-bound accessor fragments | prior service-accessor exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection/admission path |
| VSUP-008 | src/nvda_desk/vocabulary_synonym_audit.py | 341-369, 1088-1089 | _is_parallel_risk_lane_contract_descriptor_fragment | parallel-risk contract descriptors/dataschema/packet/service | prior contract descriptor exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase(s) | test governed rejection path |
| VSUP-009 | src/nvda_desk/vocabulary_synonym_audit.py | 372-391, 1078-1081 | _is_dependency_packet_ids_replay_review_fragment | `packet_ids` replay/review identifiers | prior replay/review identifier exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-010 | src/nvda_desk/vocabulary_synonym_audit.py | 394-423, 1082-1085 | _is_testing_harness_specimen_artifact_descriptor_fragment | append-only/stage-input specimen artefact descriptors | prior fixture descriptor exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase(s) | test governed rejection path |
| VSUP-011 | src/nvda_desk/vocabulary_synonym_audit.py | 426-461, 1086-1087 | _is_pr_stage_environment_descriptor_fragment | bootstrap/bounded/environment-assessment/stage-read fragments | prior path-bound exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase(s) | test governed rejection path |
| VSUP-012 | src/nvda_desk/vocabulary_synonym_audit.py | 464-477, 1090-1093 | _is_coefficient_authority_path_field_fragment | `coefficient_authority_path` field fragment | prior config field exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-013 | src/nvda_desk/vocabulary_synonym_audit.py | 480-575, 1094-1095 | _is_sequence8_coefficient_modifier_descriptor_fragment | Sequence 8 coefficient/modifier descriptors by exact path | prior Sequence 8 exception table | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch/table; govern phrases | test governed rejection path |
| VSUP-014 | src/nvda_desk/vocabulary_synonym_audit.py | 578-639, 1096-1097 | _is_sequence7_parallel_risk_descriptor_fragment | Sequence 7 parallel-risk/environment/stage-input descriptors | prior Sequence 7 exception table | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch/table; govern phrases | test governed rejection path |
| VSUP-015 | src/nvda_desk/vocabulary_synonym_audit.py | 642-693, 1098-1099 | _is_sequence11_registry_identifier_fragment | Sequence 11 retained-test registry identifiers | prior registry identifier exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch/table; govern phrases | test governed rejection path |
| VSUP-016 | src/nvda_desk/vocabulary_synonym_audit.py | 696-714, 1100-1103 | _is_sequence9_capital_consumed_input_identifier_fragment | Sequence 9 coefficient_modifier_authority identifiers | prior consumed-input identifier exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-017 | src/nvda_desk/vocabulary_synonym_audit.py | 717-743, 1104-1107 | _is_session_clock_source_timezone_local_identifier_fragment | `source_timezone` local variable near source_timezone_raw | prior local variable exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch; govern phrase | test governed rejection path |
| VSUP-018 | src/nvda_desk/vocabulary_synonym_audit.py | 746-816, 1108-1109 | _is_sequence9_dependency_lineage_identifier_fragment | Sequence-tagged lineage identifiers like coefficient-authority-seq8 | prior sequence-anchor exception | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch/table; govern phrases | test governed rejection path |
| VSUP-019 | src/nvda_desk/vocabulary_synonym_audit.py | 819-960, 1110-1111 | _is_roadmap_control_surface_identifier_fragment | exact roadmap-control identifiers by path/phrase/slug | prior mutable roadmap-control exception table | yes | REJECT_WITH_GOVERNED_EVIDENCE | remove branch/table; govern phrases | test governed handling not path suppression |

## Score-zero branch classification

| Branch lines | Predicate | Classification | Action |
|---:|---|---|---|
| 1054-1055 | _is_protocol_identifier_fragment | true tokenisation/protocol identifier parsing | retain |
| 1056-1059 | _is_python_function_declaration_identifier_fragment | true function-declaration parsing | retain |
| 1060-1113 | all other path/surface specific predicates above | hard-coded suppression / legacy false-positive bypass | remove or convert to governed data/evidence |

## Tests to remove or replace

The following test names in `tests/tier_a/vocabulary/test_vocabulary_synonym_candidate_audit.py` prove path-bound source-code suppression and must not remain as suppression-blessing tests: all tests named `*_fragment_is_not_escalated`, `*_fragment_is_path_bounded`, `*_fragments_are_path_bounded`, `*_fragments_do_not_globally_hide_synonyms`, including the FWD-001 tests at lines 1882-2103.

## Config/receipt/manifests inspected for suppression

No hard-coded candidate-hiding predicate was found in `scripts/vocabulary_synonym_audit.py`; it only re-exports the runtime audit CLI. `config/proof_blocks.yaml` and `config/retained_test_registry.yaml` contain proof/test commands and vocabulary-owned paths, not Python suppression predicates, but they are candidate source paths whose exact phrases were previously hidden by source-code logic. Prior receipts under `var/audit/...vocabulary...` record `vocabulary_synonym_audit=PASS candidates=0`; those prior clean claims are superseded unless this remediation proves clean-check without source suppression.
