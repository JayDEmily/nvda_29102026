# Vocabulary Suppression Removal Decisions

Scope: PM-authorised FWD-001 / 5.18 remediation to remove source-code synonym suppression.

Allowed decision labels only: `ADMIT_VOCABULARY_ENTRY`, `ADMIT_ALLOWED_ALIAS`, `ADD_DISALLOWED_PHRASE`, `REJECT_WITH_GOVERNED_EVIDENCE`, `KEEP_AS_UNRESOLVED_CANDIDATE`, `BLOCKED_REQUIRES_PM_AUTHORITY`, `BLOCKED_REQUIRES_ABSENT_SOURCE`.

## Source suppression mechanisms removed

| ID | Removed mechanism | Decision | Replacement evidence |
|---|---|---|---|
| VSUP-001 | `FWD001_GOVERNANCE_CANDIDATE_FRAGMENTS` table, `_is_fwd001_governance_candidate_fragment`, and its `score = 0` branch | REJECT_WITH_GOVERNED_EVIDENCE | Removed from source; candidates below routed to builder-governed aliases/disallowed phrases. |
| VSUP-002..VSUP-019 | Path/surface-specific predicate functions from `_is_vocabulary_seed_note_relationship_fragment` through `_is_roadmap_control_surface_identifier_fragment` and their `score = 0` branches | REJECT_WITH_GOVERNED_EVIDENCE | Removed from source; only generic protocol-identifier and Python function-declaration parsing filters remain. |

## Candidate decisions

| Candidate phrase | Nearest slug | Candidate occurrences observed after source suppression removal | Decision | Governed mutation |
|---|---|---:|---|---|
| append only observation record json | append_only_observation_record | 1 | ADD_DISALLOWED_PHRASE | Added to `append_only_observation_record.disallowed_phrases`. |
| baseline only | baseline_only_surface | 1 | ADD_DISALLOWED_PHRASE | Added to `baseline_only_surface.disallowed_phrases`. |
| bounded coefficient | bounded_dynamic_coefficient | 3 | ADMIT_ALLOWED_ALIAS | Added to `bounded_dynamic_coefficient.allowed_aliases`. |
| dynamic coefficient | bounded_dynamic_coefficient | 2 | ADMIT_ALLOWED_ALIAS | Added to `bounded_dynamic_coefficient.allowed_aliases`. |
| coefficient authority import | coefficient_authority | 3 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| coefficient authority marker | coefficient_authority | 1 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| coefficient authority path | coefficient_authority | 1 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| coefficient authority seq8 | coefficient_authority | 2 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| coefficient authority service | coefficient_authority | 8 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| coefficient modifier authority | coefficient_authority | 6 | ADD_DISALLOWED_PHRASE | Added to `coefficient_authority.disallowed_phrases`. |
| packet ids | dependency_packet_ids | 7 | ADMIT_ALLOWED_ALIAS | Added to `dependency_packet_ids.allowed_aliases`. |
| dmp v3 root | dmp_v3 | 1 | ADD_DISALLOWED_PHRASE | Added to `dmp_v3.disallowed_phrases`. |
| bounded environment assessment | environment_assessment | 1 | ADD_DISALLOWED_PHRASE | Added to `environment_assessment.disallowed_phrases`. |
| environment assessment import | environment_assessment | 1 | ADD_DISALLOWED_PHRASE | Added to `environment_assessment.disallowed_phrases`. |
| environment assessment only | environment_assessment | 2 | ADD_DISALLOWED_PHRASE | Added to `environment_assessment.disallowed_phrases`. |
| financial calendar | financial_calendar_crosswalk | 4 | ADMIT_ALLOWED_ALIAS | Added to `financial_calendar_crosswalk.allowed_aliases`. |
| parallel risk | parallel_risk_lane | 12 | ADMIT_ALLOWED_ALIAS | Added to `parallel_risk_lane.allowed_aliases`. |
| parallel risk lane dataschema | parallel_risk_lane | 2 | ADD_DISALLOWED_PHRASE | Added to `parallel_risk_lane.disallowed_phrases`. |
| parallel risk lane packet | parallel_risk_lane | 1 | ADD_DISALLOWED_PHRASE | Added to `parallel_risk_lane.disallowed_phrases`. |
| parallel risk lane service | parallel_risk_lane | 6 | ADD_DISALLOWED_PHRASE | Added to `parallel_risk_lane.disallowed_phrases`. |
| risk lane | parallel_risk_lane | 1 | ADMIT_ALLOWED_ALIAS | Added to `parallel_risk_lane.allowed_aliases`. |
| roadmap parallel risk lane | parallel_risk_lane | 4 | ADD_DISALLOWED_PHRASE | Added to `parallel_risk_lane.disallowed_phrases`. |
| playbook eligibility service | playbook_eligibility | 4 | ADD_DISALLOWED_PHRASE | Added to `playbook_eligibility.disallowed_phrases`. |
| source temporal standard field | source_temporal_standard | 1 | ADD_DISALLOWED_PHRASE | Added to `source_temporal_standard.disallowed_phrases`. |
| source temporal standard surface | source_temporal_standard | 2 | ADD_DISALLOWED_PHRASE | Added to `source_temporal_standard.disallowed_phrases`. |
| raw source | source_time_raw | 1 | ADD_DISALLOWED_PHRASE | Added to `source_time_raw.disallowed_phrases`. |
| source timezone | source_timezone_raw | 2 | ADMIT_ALLOWED_ALIAS | Added to `source_timezone_raw.allowed_aliases`. |
| sequence7 stage input bundle | stage_input_bundle | 2 | ADD_DISALLOWED_PHRASE | Added to `stage_input_bundle.disallowed_phrases`. |
| specimen stage input bundle | stage_input_bundle | 1 | ADD_DISALLOWED_PHRASE | Added to `stage_input_bundle.disallowed_phrases`. |
| stage input bundle json | stage_input_bundle | 1 | ADD_DISALLOWED_PHRASE | Added to `stage_input_bundle.disallowed_phrases`. |
| bootstrap stage read state | stage_read_state | 1 | ADD_DISALLOWED_PHRASE | Added to `stage_read_state.disallowed_phrases`. |
| read state | stage_read_state | 1 | ADD_DISALLOWED_PHRASE | Added to `stage_read_state.disallowed_phrases`. |
| state conditioned | state_conditioned_modifier | 6 | ADMIT_ALLOWED_ALIAS | Added to `state_conditioned_modifier.allowed_aliases`. |
| state conditioned modifier surface | state_conditioned_modifier | 1 | ADD_DISALLOWED_PHRASE | Added to `state_conditioned_modifier.disallowed_phrases`. |
| state conditioned modifier tests | state_conditioned_modifier | 1 | ADD_DISALLOWED_PHRASE | Added to `state_conditioned_modifier.disallowed_phrases`. |
| temporal context seq5 | temporal_context | 2 | ADD_DISALLOWED_PHRASE | Added to `temporal_context.disallowed_phrases`. |
| temporal event context | temporal_context | 3 | ADMIT_ALLOWED_ALIAS | Added to `temporal_context.allowed_aliases`. |

## Decision counts

- Candidate phrases adjudicated: 37.
- `ADMIT_ALLOWED_ALIAS`: 9.
- `ADD_DISALLOWED_PHRASE`: 28.
- `KEEP_AS_UNRESOLVED_CANDIDATE`: 0.
- `BLOCKED_REQUIRES_PM_AUTHORITY`: 0.
- `BLOCKED_REQUIRES_ABSENT_SOURCE`: 0.
- `ADMIT_VOCABULARY_ENTRY`: 0.
- `REJECT_WITH_GOVERNED_EVIDENCE`: recorded for removed source-suppression mechanism class; concrete phrase replacement uses `ADD_DISALLOWED_PHRASE` where rejection is the governed data action.
