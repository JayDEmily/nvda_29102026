#!/usr/bin/env bash
set +e
cd /mnt/data/work_nvda10/repo
report=var/audit/active_code_atlas_001/fwd003_fwd009_continuation_20260514/reports
run_block(){ id="$1"; python scripts/run_proof_block.py --block "$id" > "$report/${id}.stdout" 2> "$report/${id}.stderr"; st=$?; printf '%s\n' "$st" > "$report/${id}.status"; printf '%s status=%s\n' "$id" "$st" >> "$report/run_fwd003_fwd009_targeted.progress"; }
for id in \
  persistence_ledgers_receipts_surface \
  persistence_session_boundary_surface \
  module_registry_repository_surface \
  support_spine_prepared_packet_review_surface \
  dmpv3_extension_canonical_leaf_surface \
  dmpv3_transform_boundary_surface \
  roadmap_external_source_api_ingress_authority_surface \
  external_source_contract_surface \
  external_source_transform_boundary_surface \
  raw_capture_source_temporal_law_surface \
  raw_capture_transform_boundary_surface \
  source_temporal_standard_surface \
  raw_signal_contract_copy_boundary_surface \
  raw_signal_transform_boundary_surface \
  financial_event_calendar_authority_surface \
  financial_event_calendar_transform_boundary_surface \
  prepared_runtime_snapshot_contract_surface \
  prepared_runtime_transform_boundary_surface; do
  run_block "$id"
done
printf 'done\n' > "$report/run_fwd003_fwd009_targeted.done"
