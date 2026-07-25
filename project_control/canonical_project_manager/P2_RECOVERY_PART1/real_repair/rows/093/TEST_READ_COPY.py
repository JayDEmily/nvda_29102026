from __future__ import annotations

from datetime import date
from pathlib import Path

from nvda_desk.testing.harnesses import (
    Module8ParallelRiskWorkbookMapping,
    build_module_8_parallel_risk_workbook_mapping,
)


def test_module_8_parallel_risk_workbook_mapping_surface_is_present() -> None:
    mapping = build_module_8_parallel_risk_workbook_mapping()

    assert isinstance(mapping, Module8ParallelRiskWorkbookMapping)
    assert mapping.workbook_path == Path(
        "data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx"
    )
    assert mapping.stage_input_bundle.temporal.source_date == date(2026, 3, 1)
    assert mapping.stage_input_bundle.temporal.source_time_raw is None
    assert mapping.stage_input_bundle.temporal.next_event_time_utc is None
    assert mapping.stage_input_bundle.regime.vix_level == 25.09
    assert mapping.stage_input_bundle.regime.missing_fields == ["nvda_return_pct", "nq_return_pct"]
    assert mapping.stage_input_bundle.options_flow.spot_price == 186.03
    assert mapping.stage_input_bundle.options_flow.missing_fields == ["front_dte", "next_dte"]
    assert mapping.mapping_metadata["anchor_row_ref"] == "Anchor_Data!A7:AE7"
    assert (
        mapping.mapping_metadata["field_seed_dates"]["options_flow.spot_price"]["seed_ref"]
        == "Live_Web_Baseline!B6:C6"
    )
    assert (
        mapping.mapping_metadata["field_seed_dates"]["regime.vix_level"]["seed_ref"]
        == "Live_Web_Baseline!B9:C9"
    )
    assert (
        mapping.mapping_metadata["field_seed_dates"]["temporal.source_date"]["anchor_ref"]
        == "Anchor_Data!A7"
    )
    assert mapping.derivedfrom == "reference-ledger::Anchor_Data!A7:AE7"
    assert mapping.inputfingerprint.startswith("sha256:")
