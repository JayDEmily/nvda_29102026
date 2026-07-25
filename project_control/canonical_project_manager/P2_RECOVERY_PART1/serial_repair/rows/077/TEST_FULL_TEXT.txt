from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskPreparationPacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput
from nvda_desk.domain.parallel_risk.environment_assessment import assess_risk_envelope


def test_front_dte_greater_than_next_dte_preserves_options_repricing_caution() -> None:
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
        regime_input=MarketRegimeContextInput(),
        options_flow_input=OptionsFlowContextInput(front_dte=5, next_dte=1),
    )

    envelope = assess_risk_envelope(packet)

    assert envelope.envelope_state == "caution"
    assert envelope.caution_flags == ["front_term_structure_backwardation"]
    assert [c.source_family for c in envelope.contributions] == ["options_repricing_context"]


def test_front_dte_not_greater_than_next_dte_does_not_create_legacy_caution() -> None:
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC)),
        regime_input=MarketRegimeContextInput(),
        options_flow_input=OptionsFlowContextInput(front_dte=1, next_dte=5),
    )

    assert assess_risk_envelope(packet).envelope_state == "tight"
