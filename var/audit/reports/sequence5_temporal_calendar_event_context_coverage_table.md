# Sequence 5 temporal/calendar/event context coverage table

| Slice | Total records in slice | Sequence 5 selected records |
|---|---:|---:|
| `dmpv3_packet_carriage.json` | 73 | 13 |
| `downstream_capital_deployment_authority.json` | 2 | 2 |
| `dynamic_coefficient_and_modifier_authority.json` | 193 | 12 |
| `exit_and_close_architecture.json` | 90 | 2 |
| `external_source_interfaces_and_api_ingress.json` | 234 | 19 |
| `financial_and_event_calendar_architecture.json` | 117 | 117 |
| `live_position_and_inventory_architecture.json` | 38 | 1 |
| `opening_architecture_and_placement_readiness.json` | 74 | 74 |
| `parallel_risk_lane.json` | 57 | 3 |
| `persistence_ledgers_and_receipts.json` | 97 | 4 |
| `playbook_library_architecture.json` | 95 | 1 |
| `prepared_ingress_and_runtime_context_preparation.json` | 51 | 16 |
| `raw_capture_and_source_temporal_law.json` | 108 | 108 |
| `raw_signal_families.json` | 123 | 6 |
| `review_and_explanation_layer.json` | 143 | 4 |
| `serial_desk_cognition_spine.json` | 139 | 3 |
| `testing_proof_and_checkpoint_surfaces.json` | 72 | 9 |
| `vocabulary_governance_interface.json` | 10 | 0 |

## Mandatory slice check

| Mandatory slice | Required count | Selected count | Result |
|---|---:|---:|---|
| `financial_and_event_calendar_architecture.json` | 117 | 117 | PASS |
| `opening_architecture_and_placement_readiness.json` | 74 | 74 | PASS |
| `raw_capture_and_source_temporal_law.json` | 108 | 108 | PASS |

## Posture counts

```json
{
  "selected_record_count": 394,
  "records_by_slice": {
    "dmpv3_packet_carriage.json": 13,
    "downstream_capital_deployment_authority.json": 2,
    "dynamic_coefficient_and_modifier_authority.json": 12,
    "exit_and_close_architecture.json": 2,
    "external_source_interfaces_and_api_ingress.json": 19,
    "financial_and_event_calendar_architecture.json": 117,
    "live_position_and_inventory_architecture.json": 1,
    "opening_architecture_and_placement_readiness.json": 74,
    "parallel_risk_lane.json": 3,
    "persistence_ledgers_and_receipts.json": 4,
    "playbook_library_architecture.json": 1,
    "prepared_ingress_and_runtime_context_preparation.json": 16,
    "raw_capture_and_source_temporal_law.json": 108,
    "raw_signal_families.json": 6,
    "review_and_explanation_layer.json": 4,
    "serial_desk_cognition_spine.json": 3,
    "testing_proof_and_checkpoint_surfaces.json": 9
  },
  "context_type_counts": {
    "dmpv3_temporal_context_carriage_deferral": 13,
    "explicit_deferral_downstream_capital_not_temporal_authority": 2,
    "coefficient_modifier_context_deferral": 12,
    "downstream_lifecycle_temporal_context_deferral": 3,
    "external_temporal_calendar_event_source_context": 19,
    "financial_calendar_and_scheduled_event_context": 117,
    "opening_phase_and_placement_readiness_context": 74,
    "parallel_risk_context_consumer_deferral": 3,
    "temporal_context_persistence_receipt_deferral": 4,
    "playbook_calendar_event_constraint_deferral": 1,
    "prepared_runtime_temporal_context": 16,
    "raw_capture_source_temporal_law_context": 108,
    "raw_signal_temporal_context_source_deferral": 6,
    "review_explanation_temporal_context_deferral": 4,
    "serial_context_consumer_deferral": 3,
    "testing_proof_temporal_context_deferral": 9
  },
  "event_posture_counts": {
    "context_metadata_only_not_alpha": 80,
    "scheduled_event_context_metadata_not_alpha": 13,
    "not_event_alpha; downstream capital may only consume already formed lawful context": 2,
    "scheduled_calendar_event_context_metadata_not_alpha": 117,
    "opening_context_metadata_not_alpha": 74,
    "temporal_source_context_metadata_not_alpha": 108
  },
  "scheduled_unscheduled_posture_counts": {
    "mixed_or_not_yet_separated_static_reconciliation_only": 80,
    "scheduled_or_mixed": 19,
    "not_applicable": 2,
    "scheduled": 117,
    "not_applicable_or_schedule_derived_opening_phase": 74,
    "mixed_source_temporal_context": 102
  }
}
```
