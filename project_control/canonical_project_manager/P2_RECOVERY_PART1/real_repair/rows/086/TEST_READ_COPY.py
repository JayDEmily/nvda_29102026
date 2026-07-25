from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskPreparationPacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.domain.parallel_risk.environment_assessment import assess_risk_envelope


def _packet(vix_level: float) -> ParallelRiskPreparationPacket:
    return ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
        regime_input=MarketRegimeContextInput(vix_level=vix_level),
        options_flow_input=OptionsFlowContextInput(),
    )


def test_vix_30_caution_threshold_is_preserved_as_compatibility_mode() -> None:
    envelope = assess_risk_envelope(_packet(30.0))

    assert envelope.envelope_state == "caution"
    assert "vix_elevated" in envelope.caution_flags
    assert envelope.hard_blocks == []


def test_vix_50_block_threshold_is_preserved_as_compatibility_mode() -> None:
    envelope = assess_risk_envelope(_packet(50.0))

    assert envelope.envelope_state == "block"
    assert "vix_elevated" in envelope.caution_flags
    assert envelope.hard_blocks == ["vix_extreme"]


def test_subthreshold_vix_does_not_create_legacy_caution() -> None:
    envelope = assess_risk_envelope(_packet(29.99))

    assert envelope.envelope_state == "tight"
    assert envelope.contributions == []
