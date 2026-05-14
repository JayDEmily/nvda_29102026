# Atlas Plan2 testing and proof classification

Status: Stage 1 proof classification regenerated from present Atlas JSON surfaces.

## Touched surface proof classification

| Touched surface type | Files touched by this reset | Expected proof tier | Docstring rule | Checkpoint rule | JSON validation | Runtime / pytest proof |
|---|---|---|---|---|---|---|
| Audit/control Markdown receipts | `var/audit/atlas_plan2/*.md` | Control-surface evidence only; no runtime proof tier claimed. | Not applicable; Markdown only. | Not applicable; no proof artefact or Python boundary changed. | Not applicable to changed files. | Prohibited in Stage 1. |
| Planning Markdown | `docs/planning/2026-05-01_ATLAS_PLANNING_COMPILER_ROUTE_SETUP_PLAN.md` | Control-surface evidence only; no runtime proof tier claimed. | Not applicable; Markdown only. | Not applicable; no proof artefact or Python boundary changed. | Not applicable to changed file. | Prohibited in Stage 1. |

## Relied-on JSON proof classification

| JSON group | Paths | Validation requirement | Stage 1 use | Prohibited interpretation |
|---|---|---|---|---|
| Atlas source evidence | `native_intent_satisfaction_ledger.json`; `legacy_intent_atlas.json`; coverage view; owner map view | `jq -e .`; manifest source hashes and counts | Source evidence for future planning. | Full semantic implementation authority. |
| Atlas derived inventory | manifest, checksum manifest, schema, and 18 slice JSON files | `jq -e .`; checksum comparison; `materialise_atlas_surface_slices.py --validate-only` | Bounded inventory and future ordinary planning input. | Generated implementation leaves or runtime proof. |
| Planning-compiler reference | Reference ZIP docs only | No JSON imported or modified. | Conceptual planning discipline. | Code import or executable compiler dependency. |

## `jq` validation output for present JSON files

```text
jq OK var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json
jq OK var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json
jq OK var/audit/atlas_surface_slices/atlas_surface_slice.schema.json
jq OK var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json
jq OK var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json
jq OK var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json
jq OK var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json
jq OK var/audit/atlas_surface_slices/slices/dmpv3_packet_carriage.json
jq OK var/audit/atlas_surface_slices/slices/downstream_capital_deployment_authority.json
jq OK var/audit/atlas_surface_slices/slices/dynamic_coefficient_and_modifier_authority.json
jq OK var/audit/atlas_surface_slices/slices/exit_and_close_architecture.json
jq OK var/audit/atlas_surface_slices/slices/external_source_interfaces_and_api_ingress.json
jq OK var/audit/atlas_surface_slices/slices/financial_and_event_calendar_architecture.json
jq OK var/audit/atlas_surface_slices/slices/live_position_and_inventory_architecture.json
jq OK var/audit/atlas_surface_slices/slices/opening_architecture_and_placement_readiness.json
jq OK var/audit/atlas_surface_slices/slices/parallel_risk_lane.json
jq OK var/audit/atlas_surface_slices/slices/persistence_ledgers_and_receipts.json
jq OK var/audit/atlas_surface_slices/slices/playbook_library_architecture.json
jq OK var/audit/atlas_surface_slices/slices/prepared_ingress_and_runtime_context_preparation.json
jq OK var/audit/atlas_surface_slices/slices/raw_capture_and_source_temporal_law.json
jq OK var/audit/atlas_surface_slices/slices/raw_signal_families.json
jq OK var/audit/atlas_surface_slices/slices/review_and_explanation_layer.json
jq OK var/audit/atlas_surface_slices/slices/serial_desk_cognition_spine.json
jq OK var/audit/atlas_surface_slices/slices/testing_proof_and_checkpoint_surfaces.json
jq OK var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json

TOTAL_JSON_FILES=25
```

## Slice-pack validate-only output

```text
{
  "result": "passed",
  "failures": [],
  "slice_count": 18,
  "total_records_across_slices": 1716,
  "unique_atlas_record_ids_across_slices": 1716
}
```

## Proof boundary

The manifest and validate-only script show present derived Atlas evidence with 18 slices and 1716 unique records. This is evidence for planning-control setup only. It does not prove active code/test alignment and does not authorise runtime implementation, pytest implementation changes, generated-slice rewrites, planning-compiler code changes, vocabulary admission, or `READY_TO_CONSIDER_ATLAS = true`.
