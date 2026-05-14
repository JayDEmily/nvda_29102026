from __future__ import annotations

import json
from pathlib import Path


def test_required_parallel_risk_protocol_and_calendar_terms_are_present() -> None:
    vocab_path = Path("data/vocabulary/canonical_vocabulary.json")
    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    entries = {entry["canonical_slug"]: entry for entry in vocab["entries"]}

    assert "parallel_risk_lane" in entries
    assert entries["parallel_risk_lane"]["maps_to_contract"] == "ParallelRiskLanePacket"

    assert "dmp_v3" in entries
    assert entries["dmp_v3"]["maps_to_contract"] == "DmpV3Envelope"

    assert "financial_calendar_reference_bundle" in entries
    assert (
        entries["financial_calendar_reference_bundle"]["maps_to_contract"]
        == "ImportedReferenceBundle"
    )

    assert "financial_calendar_crosswalk" in entries
    assert (
        entries["financial_calendar_crosswalk"]["maps_to_contract"]
        == "FinancialCalendarCrosswalkRecord"
    )

    assert "financial_calendar_import_record" in entries
    assert (
        entries["financial_calendar_import_record"]["maps_to_contract"]
        == "FinancialCalendarImportRecord"
    )

    assert "coefficient_authority" in entries
    assert entries["coefficient_authority"]["maps_to_contract"] == "CoefficientAuthorityDocument"

    assert "mutable_runtime_surface" in entries
    assert entries["mutable_runtime_surface"]["maps_to_contract"] == "CoefficientAuthorityRecord"

    assert "baseline_only_surface" in entries
    assert entries["baseline_only_surface"]["maps_to_contract"] == "CoefficientAuthorityRecord"

    assert "effective_coefficient_lineage" in entries
    assert (
        entries["effective_coefficient_lineage"]["maps_to_contract"] == "ResolvedCoefficientValue"
    )

    assert "state_conditioned_modifier" in entries
    assert entries["state_conditioned_modifier"]["maps_to_contract"] == "ModifierPolicyRecord"

    assert "bounded_dynamic_coefficient" in entries
    assert (
        entries["bounded_dynamic_coefficient"]["maps_to_contract"] == "CoefficientAuthorityRecord"
    )

    assert "review_horizon" in entries
    assert entries["review_horizon"]["maps_to_contract"] == "CoefficientReviewHorizon"

    assert "champion_challenger_evaluation" in entries
    assert (
        entries["champion_challenger_evaluation"]["maps_to_contract"]
        == "CoefficientPromotionEvaluation"
    )

    assert "live_paper_historical_evaluation_separation" in entries
    assert (
        entries["live_paper_historical_evaluation_separation"]["maps_to_contract"]
        == "CoefficientEvaluationSeparationRule"
    )

    assert "source_temporal_standard" in entries
    assert entries["source_temporal_standard"]["maps_to_contract"] == "SourceTemporalStandard"

    assert "source_time_raw" in entries
    assert (
        entries["source_time_raw"]["maps_to_contract"] == "SourceTemporalStandard.source_time_raw"
    )

    assert "source_time_kind" in entries
    assert (
        entries["source_time_kind"]["maps_to_contract"] == "SourceTemporalStandard.source_time_kind"
    )

    assert "source_timezone_raw" in entries
    assert (
        entries["source_timezone_raw"]["maps_to_contract"]
        == "SourceTemporalStandard.source_timezone_raw"
    )

    assert "source_time_utc" in entries
    assert (
        entries["source_time_utc"]["maps_to_contract"] == "SourceTemporalStandard.source_time_utc"
    )

    assert "source_date" in entries
    assert entries["source_date"]["maps_to_contract"] == "SourceTemporalStandard.source_date"

    assert "captured_at_utc" in entries
    assert (
        entries["captured_at_utc"]["maps_to_contract"] == "SourceTemporalStandard.captured_at_utc"
    )

    assert "persisted_at_utc" in entries
    assert (
        entries["persisted_at_utc"]["maps_to_contract"] == "SourceTemporalStandard.persisted_at_utc"
    )

    assert "source_provider" in entries
    assert (
        entries["source_provider"]["maps_to_contract"] == "SourceTemporalStandard.source_provider"
    )

    assert "source_channel" in entries
    assert entries["source_channel"]["maps_to_contract"] == "SourceTemporalStandard.source_channel"

    assert "time_granularity" in entries
    assert (
        entries["time_granularity"]["maps_to_contract"] == "SourceTemporalStandard.time_granularity"
    )

    assert "workbook_temporal_provenance" in entries
    assert (
        entries["workbook_temporal_provenance"]["maps_to_contract"]
        == "SignalWorkbookTemporalProvenanceRule"
    )

    assert "field_level_provenance" in entries
    assert (
        entries["field_level_provenance"]["maps_to_contract"]
        == "SignalWorkbookTemporalProvenanceRule.field_level_provenance"
    )

    assert "temporal_conformance_inventory" in entries
    assert (
        entries["temporal_conformance_inventory"]["maps_to_contract"]
        == "TemporalConformanceInventory"
    )

    assert "already_conformant" in entries
    assert (
        entries["already_conformant"]["maps_to_contract"]
        == "TemporalConformanceClassification.already_conformant"
    )

    assert "needs_proof_test_remediation_only" in entries
    assert (
        entries["needs_proof_test_remediation_only"]["maps_to_contract"]
        == "TemporalConformanceClassification.needs_proof_test_remediation_only"
    )

    assert "needs_code_persistence_remediation_in_tranche_3" in entries
    assert (
        entries["needs_code_persistence_remediation_in_tranche_3"]["maps_to_contract"]
        == "TemporalConformanceClassification.needs_code_persistence_remediation_in_tranche_3"
    )

    assert "reserved_blocked" in entries
    assert (
        entries["reserved_blocked"]["maps_to_contract"]
        == "TemporalConformanceClassification.reserved_blocked"
    )
