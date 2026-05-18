from __future__ import annotations

import inspect
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import AuthorityFlags
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.stage_inputs import StageInputBundle
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.domain.parallel_risk import (
    family_aggregation,
    freshness,
    missing_signals,
    minute_profile_assembly,
    risk_atoms,
    unavailable_signals,
)
from nvda_desk.services.parallel_risk_lane_service import ParallelRiskLaneService


def test_enriched_optional_profile_keeps_every_forbidden_authority_default_false() -> None:
    result = ParallelRiskLaneService().run_bootstrap(
        stage_input_bundle=StageInputBundle(
            temporal=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
            regime=MarketRegimeContextInput(vix_level=31.0),
            options_flow=OptionsFlowContextInput(spot_price=101.0, front_dte=5, next_dte=1),
        ),
        input_packet_id="dmp::parallel_risk::bootstrap_input::authority-regression",
        output_packet_id="dmp::parallel_risk::output::authority-regression",
        include_minute_profile=True,
    )

    flags = result["minute_profile"].authority_flags
    assert flags.candidate_formation_allowed is False
    assert flags.playbook_selection_allowed is False
    assert flags.capital_sizing_allowed is False
    assert flags.broker_execution_allowed is False
    assert flags.serial_stage_mutation_allowed is False
    assert flags.review_judgement_authority is False
    assert flags.direct_workbook_runtime_read_allowed is False
    assert result["minute_profile"].lineage["forbidden_authority_keys_consumed"] == []


def test_authority_flags_still_reject_positive_authority() -> None:
    with pytest.raises(ValidationError, match="parallel_risk_authority_flags_must_remain_false"):
        AuthorityFlags(playbook_selection_allowed=True)


def test_enriched_prl_modules_do_not_open_runtime_workbook_read_surface() -> None:
    combined_source = "\n".join(
        inspect.getsource(module)
        for module in (
            family_aggregation,
            freshness,
            missing_signals,
            minute_profile_assembly,
            risk_atoms,
            unavailable_signals,
        )
    )

    forbidden_runtime_workbook_terms = ("openpyxl", "load_workbook", "read_excel", ".xlsx")
    for term in forbidden_runtime_workbook_terms:
        assert term not in combined_source
