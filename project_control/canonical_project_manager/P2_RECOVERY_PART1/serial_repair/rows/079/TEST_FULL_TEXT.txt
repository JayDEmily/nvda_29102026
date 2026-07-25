from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.parallel_risk import ParallelRiskPreparationPacket
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.domain.parallel_risk.environment_assessment import assess_risk_envelope


def test_scheduled_event_window_active_caution_is_preserved_without_trade_authority() -> None:
    packet = ParallelRiskPreparationPacket(
        temporal_input=TemporalContextInput(
            source_time_utc=datetime(2026, 5, 18, 14, 30, tzinfo=UTC),
            windows=[
                TemporalEventWindow(
                    event_id="event-1",
                    window_start_utc=datetime(2026, 5, 18, 14, 25, tzinfo=UTC),
                    window_end_utc=datetime(2026, 5, 18, 14, 45, tzinfo=UTC),
                    tags=["scheduled_event_window_active"],
                )
            ],
        ),
        regime_input=MarketRegimeContextInput(),
        options_flow_input=OptionsFlowContextInput(),
    )

    envelope = assess_risk_envelope(packet)

    assert envelope.envelope_state == "caution"
    assert envelope.caution_flags == ["scheduled_event_window_active"]
    assert [c.source_family for c in envelope.contributions] == ["temporal_event_context"]
    payload = envelope.model_dump_json()
    assert "buy" not in payload
    assert "sell" not in payload
    assert "order" not in payload
