from __future__ import annotations

from nvda_desk.contracts.upstream_signal import RawUpstreamSignalInput
from nvda_desk.domain.parallel_risk.missing_signals import (
    build_missing_signal_register_entry,
    signal_snapshot_from_upstream_ingress_result,
)
from nvda_desk.upstream.raw_signal_ingress import ingest_raw_upstream_signal


def test_missing_signal_register_entry_is_metadata_only_and_lowers_confidence() -> None:
    entry = build_missing_signal_register_entry(
        signal_id="vwap_distance",
        signal_family="market_microstructure",
        expected_reason="expected after typed workbook inventory promotion",
        missing_reason="not_projected_into_prl_input",
        expected_signal_inventory_ref="workbook#Parallel Risk Lane Signal Inventory",
        workbook_lineage_refs=["Raw_Primitives_Catalog!A1:H49"],
    )

    assert entry.impact_on_profile == "lowers_confidence"
    assert entry.expected_signal_inventory_ref == "workbook#Parallel Risk Lane Signal Inventory"
    assert entry.workbook_lineage_refs == ["Raw_Primitives_Catalog!A1:H49"]
    assert "trade" not in entry.model_dump_json()
    assert "order" not in entry.model_dump_json()


def test_quarantined_upstream_signal_becomes_snapshot_absence_not_runtime_signal_value() -> None:
    result = ingest_raw_upstream_signal(
        raw_signal=RawUpstreamSignalInput(
            source_id="source-1",
            signal_family_id="headline_feed",
            scope_id="NVDA",
            payload={"headline": "placeholder"},
        ),
        dataset_packet_payload={},
        admitted_signal_families={"vix_level"},
    )

    entry = signal_snapshot_from_upstream_ingress_result(result, raw_or_derived="raw")

    assert result.quarantined is True
    assert entry.signal_id == "headline_feed"
    assert entry.signal_family == "headline_feed"
    assert entry.value is None
    assert entry.missing_or_quarantined == "quarantined"
    assert entry.rejection_reason == "signal_family_not_admitted"
    assert entry.lawful_prl_use_allowed is False


def test_admitted_trace_only_signal_snapshot_does_not_strip_trace_lineage() -> None:
    result = ingest_raw_upstream_signal(
        raw_signal=RawUpstreamSignalInput(
            source_id="source-2",
            signal_family_id="vix_level",
            scope_id="NVDA",
            payload={"value": 31.0, "units": "index_level", "trade_allowed": True},
        ),
        dataset_packet_payload={},
        admitted_signal_families={"vix_level"},
    )

    entry = signal_snapshot_from_upstream_ingress_result(result, raw_or_derived="raw")

    assert result.quarantined is False
    assert entry.missing_or_quarantined == "present"
    assert entry.value == {"value": 31.0, "units": "index_level"}
    assert entry.source_ids == ["source-2"]
    assert entry.lawful_prl_use_allowed is True
    assert "trade_allowed" not in str(entry.value)
