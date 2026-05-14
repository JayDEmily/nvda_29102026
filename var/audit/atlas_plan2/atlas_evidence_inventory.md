# Atlas Plan2 evidence inventory

Status: Atlas evidence inventory regenerated from present source files in the fresh active ZIP extraction.

## Inventory boundary

| Boundary | State |
|---|---|
| Atlas import / implementation selected | No. |
| Runtime work selected | No. |
| Generated slice files modified | No. |
| Full semantic content coverage of giant source JSON claimed | No; bounded inventory uses manifest, schema, checksums, source counts, slice counts, JSON parse validation, and deterministic validate-only script output. |
| Ordinary future planning input | Present materialised slice pack plus manifest/checksums/schema. |

## Required Atlas surfaces presence

| Path | Observed state |
|---|---|
| `intent_migration/atlas_surface_slice_pack/AGENTS.override.md` | present |
| `intent_migration/atlas_tranche_roadmap/AGENTS.override.md` | present |
| `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json` | present |
| `var/audit/atlas_surface_slices/atlas_surface_slice_checksums.json` | present |
| `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json` | present |
| `var/audit/atlas_surface_slices/slices/**` | present; 18 JSON slice files |
| `var/audit/briefs/2026-04-28_ATLAS_SURFACE_SLICE_PACK_TRANCHE.md` | present |
| `var/audit/briefs/2026-04-28_ATLAS_TRANCHE_ROADMAP_PLAN.md` | present |
| `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json` | present |
| `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json` | present |
| `var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json` | present |
| `var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json` | present |
| `scripts/materialise_atlas_surface_slices.py` | present |

## Manifest validation summary

| Manifest field | Value |
|---|---:|
| `native_record_count` | `1716` |
| `raw_record_count` | `1716` |
| `slice_count` | `18` |
| `total_records_across_slices` | `1716` |
| `slice_total_matches_native_record_count` | `True` |
| `duplicate_native_atlas_record_ids` | `0` |
| `duplicate_raw_atlas_record_ids` | `0` |
| `native_records_missing_raw_atlas_record` | `0` |
| `coverage_refs_not_in_native_ledger` | `0` |
| `owner_refs_not_in_native_ledger` | `0` |

## Source JSON files

| Evidence key | Path | Count type | Count | SHA256 from manifest |
|---|---|---|---:|---|
| `native_intent_satisfaction_ledger` | `var/audit/ledgers/intent_migration/native_intent_satisfaction_ledger.json` | `record_count` | 1716 | `a1863186138db7f4ca900b4e241d900675ca1545998e0fcfc84127dd13fb223a` |
| `legacy_intent_atlas` | `var/audit/imports/atlas_bridge_inputs/legacy_intent_atlas.json` | `record_count` | 1716 | `059b728476971042910e5f2b5b4e32a8cd564f50b27eb325c118e83f4a8ccb38` |
| `legacy_file_coverage_view` | `var/audit/imports/atlas_bridge_inputs/legacy_file_coverage_view.json` | `file_count` | 128 | `822dcae2587690909cdb41ddb9eb81b2ff55a5dc02d419557c8a8e8d7aae6212` |
| `legacy_owner_map_view` | `var/audit/imports/atlas_bridge_inputs/legacy_owner_map_view.json` | `owner_count` | 82 | `105ffc4060dda873f8c13bf3835ef140a2518957d01839f476f63a0ec740335d` |

## Slice inventory from manifest

| Blueprint surface | Slice name | Records | Satisfaction-status counts | Leaf-type counts |
|---|---|---:|---|---|
| DMPV3 packet carriage | `dmpv3_packet_carriage` | 73 | `{"missing": 21, "partially_satisfied": 28, "transform_required": 24}` | `{"later_blueprint_leaf": 24, "later_test_first_leaf": 49}` |
| Downstream capital deployment authority | `downstream_capital_deployment_authority` | 2 | `{"partially_satisfied": 1, "transform_required": 1}` | `{"later_blueprint_leaf": 1, "later_test_first_leaf": 1}` |
| Dynamic coefficient and modifier authority | `dynamic_coefficient_and_modifier_authority` | 193 | `{"missing": 84, "partially_satisfied": 66, "transform_required": 43}` | `{"later_blueprint_leaf": 43, "later_test_first_leaf": 150}` |
| Exit and close architecture | `exit_and_close_architecture` | 90 | `{"missing": 47, "transform_required": 43}` | `{"later_blueprint_leaf": 90}` |
| External source interfaces and API ingress | `external_source_interfaces_and_api_ingress` | 234 | `{"missing": 110, "partially_satisfied": 48, "transform_required": 76}` | `{"later_blueprint_leaf": 76, "later_test_first_leaf": 158}` |
| Financial and event calendar architecture | `financial_and_event_calendar_architecture` | 117 | `{"partially_satisfied": 102, "transform_required": 15}` | `{"later_blueprint_leaf": 15, "later_test_first_leaf": 102}` |
| Live position and inventory architecture | `live_position_and_inventory_architecture` | 38 | `{"already_satisfied": 2, "missing": 5, "partially_satisfied": 14, "transform_required": 17}` | `{"later_blueprint_leaf": 17, "later_test_first_leaf": 19, "none": 2}` |
| Opening architecture and placement readiness | `opening_architecture_and_placement_readiness` | 74 | `{"missing": 7, "partially_satisfied": 6, "transform_required": 61}` | `{"later_blueprint_leaf": 61, "later_test_first_leaf": 13}` |
| Parallel risk lane | `parallel_risk_lane` | 57 | `{"partially_satisfied": 32, "transform_required": 25}` | `{"later_blueprint_leaf": 25, "later_test_first_leaf": 32}` |
| Persistence, ledgers, and receipts | `persistence_ledgers_and_receipts` | 97 | `{"missing": 18, "partially_satisfied": 56, "transform_required": 23}` | `{"later_blueprint_leaf": 23, "later_test_first_leaf": 74}` |
| Playbook library architecture | `playbook_library_architecture` | 95 | `{"partially_satisfied": 31, "transform_required": 64}` | `{"later_blueprint_leaf": 95}` |
| Prepared ingress and runtime context preparation | `prepared_ingress_and_runtime_context_preparation` | 51 | `{"missing": 31, "partially_satisfied": 18, "transform_required": 2}` | `{"later_blueprint_leaf": 2, "later_test_first_leaf": 49}` |
| Raw capture and source temporal law | `raw_capture_and_source_temporal_law` | 108 | `{"missing": 11, "partially_satisfied": 31, "transform_required": 66}` | `{"later_blueprint_leaf": 66, "later_test_first_leaf": 42}` |
| Raw signal families | `raw_signal_families` | 123 | `{"missing": 22, "partially_satisfied": 33, "transform_required": 68}` | `{"later_blueprint_leaf": 68, "later_test_first_leaf": 55}` |
| Review and explanation layer | `review_and_explanation_layer` | 143 | `{"missing": 45, "partially_satisfied": 52, "transform_required": 46}` | `{"later_blueprint_leaf": 46, "later_test_first_leaf": 97}` |
| Serial desk-cognition spine | `serial_desk_cognition_spine` | 139 | `{"partially_satisfied": 30, "transform_required": 109}` | `{"later_blueprint_leaf": 109, "later_test_first_leaf": 30}` |
| Testing, proof, and checkpoint surfaces | `testing_proof_and_checkpoint_surfaces` | 72 | `{"partially_satisfied": 44, "transform_required": 28}` | `{"later_blueprint_leaf": 28, "later_test_first_leaf": 44}` |
| Vocabulary governance interface | `vocabulary_governance_interface` | 10 | `{"already_satisfied": 1, "missing": 3, "partially_satisfied": 3, "transform_required": 3}` | `{"later_blueprint_leaf": 3, "later_test_first_leaf": 6, "none": 1}` |

## Checksum evidence

| Generated file | Checksum status | SHA256 from checksum manifest |
|---|---|---|
| `var/audit/atlas_surface_slices/atlas_surface_slice.schema.json` | matches current file | `fb857c021ac5113218702879cb8f4ae1186310dd5de8439f042216d83c79240b` |
| `var/audit/atlas_surface_slices/atlas_surface_slice_manifest.json` | matches current file | `9d1ded6cf6c9d00f41f9ee4fc48857937a9cf4a13ad1705aeff19dd8a31051f1` |
| `var/audit/atlas_surface_slices/slices/dmpv3_packet_carriage.json` | matches current file | `dbbfc30be1328c75514a21be9306085808e3f97677bf9729aa6ba571cd83f388` |
| `var/audit/atlas_surface_slices/slices/downstream_capital_deployment_authority.json` | matches current file | `4a794fd73519fa12bbe3c8d7f98ab7674327c7db4694b54fe45fe2e88bddc83a` |
| `var/audit/atlas_surface_slices/slices/dynamic_coefficient_and_modifier_authority.json` | matches current file | `5cc79428f54d26b9ab7caf0c1cc1a5aff53945480085ed5eaa7bab82816361be` |
| `var/audit/atlas_surface_slices/slices/exit_and_close_architecture.json` | matches current file | `a0005a9d225f5c31ee137cb40a9a4d706b7c803d2d600a03d0b1f7310c0320c0` |
| `var/audit/atlas_surface_slices/slices/external_source_interfaces_and_api_ingress.json` | matches current file | `69eae22954653455797c6ad9973a476f1ba9ab486aa636ba9f9175f1f5159447` |
| `var/audit/atlas_surface_slices/slices/financial_and_event_calendar_architecture.json` | matches current file | `14d5f58f2012ac18f2c844a0c3a14abe54a7ee0ba9a6c1ba757c9d0b9c7b2ed9` |
| `var/audit/atlas_surface_slices/slices/live_position_and_inventory_architecture.json` | matches current file | `a411d91276806ee3fc6e0bf17598d459e6e532459339a95b7f70f21a3cfa00ef` |
| `var/audit/atlas_surface_slices/slices/opening_architecture_and_placement_readiness.json` | matches current file | `922dc71e8adae63865e46c82d3641d4a21611b78927fdd73f5c39aafc61f9490` |
| `var/audit/atlas_surface_slices/slices/parallel_risk_lane.json` | matches current file | `2fb2d7b8e39af5469f3c0836f5334f3c9d8792ed1e7610c01ede25a33f4a8aa1` |
| `var/audit/atlas_surface_slices/slices/persistence_ledgers_and_receipts.json` | matches current file | `ff78f9bec189c7d3f177786fec108412ca3ee591882dca7885cf5b4a6f8e787e` |
| `var/audit/atlas_surface_slices/slices/playbook_library_architecture.json` | matches current file | `fc4285a84ace46a19c894266658f143caa603826f4715318107e97db0f59703d` |
| `var/audit/atlas_surface_slices/slices/prepared_ingress_and_runtime_context_preparation.json` | matches current file | `0773e185697b82f4f2ee0ae012096b52b2c3938e8eeff569473f5f6d7b894bf2` |
| `var/audit/atlas_surface_slices/slices/raw_capture_and_source_temporal_law.json` | matches current file | `6ff386c4e7b49cb453f45806950698e1a21fc9707d969279a5243ef87f99f2ac` |
| `var/audit/atlas_surface_slices/slices/raw_signal_families.json` | matches current file | `f19fa1712b054b26f63337ca711628f6f7f33d697281c34f8c693f96eed1c4eb` |
| `var/audit/atlas_surface_slices/slices/review_and_explanation_layer.json` | matches current file | `198aa49b3ee838d3e3a01241434bc4625fa636595e8b7d3f1e82f4fc13e4f99c` |
| `var/audit/atlas_surface_slices/slices/serial_desk_cognition_spine.json` | matches current file | `f100c235435bd876464d7a130ecd6f25a7a0153dbb10ed7f3c125c4f09e4e188` |
| `var/audit/atlas_surface_slices/slices/testing_proof_and_checkpoint_surfaces.json` | matches current file | `ad5bafe50e50012f6b6078453a652c080d8386d46944130944d8f50e922866c1` |
| `var/audit/atlas_surface_slices/slices/vocabulary_governance_interface.json` | matches current file | `53bc14565af44fa0eb9f57f27c37ee57bd3b43dc2e0a8e92658c2ffbefdd7203` |

## Deterministic validate-only output

```text
{
  "result": "passed",
  "failures": [],
  "slice_count": 18,
  "total_records_across_slices": 1716,
  "unique_atlas_record_ids_across_slices": 1716
}
```

## Evidence role classification

| Surface | Role | Meaning in Stage 1 |
|---|---|---|
| `native_intent_satisfaction_ledger.json`; `legacy_intent_atlas.json`; coverage and owner-map views | source evidence | Original Atlas/Bridge and native-satisfaction evidence; read through bounded counts/checksums unless future semantic claims require deeper reading. |
| Manifest, checksum manifest, schema, and 18 slice files | derived inventory | Materialised evidence package for bounded future planning; not implementation authority. |
| Atlas roadmap plan and roadmap AGENTS surface | planning candidate | Coarse future roadmap planning inputs only. |
| Slice records with `implementation_leaf_required` or future leaf type fields | implementation candidate | Quarantined until a later implementation route opens one tranche. |
| Durable names seen in Atlas/compiler planning language | vocabulary candidate | Must be classified by vocabulary law before canonical use. |
| Record counts, joins, checksums, schema/JSON parse, losslessness and no-implementation boundaries | proof obligation | Required future proof or closeout evidence; does not authorise runtime/test changes in Stage 1. |

## Content limits

- The two large source record files contain 1716 records each. Their full semantic payload was not claimed as read.

- The 18 generated slices were inventoried through manifest rows, per-file JSON parse, checksums, record counts, and validate-only script output. Full semantic coverage of every record is not claimed.

- No source JSON, generated slice, schema, checksum, runtime, test, planning-compiler code, or vocabulary file was modified.
