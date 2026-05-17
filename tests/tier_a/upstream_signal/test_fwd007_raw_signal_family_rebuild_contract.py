from __future__ import annotations

from decimal import Decimal

from nvda_desk.contracts.market_substrate import (
    MarketSubstrateObservation,
    MarketSubstrateSnapshot,
)
from nvda_desk.contracts.strategic_ladder import (
    LadderDecision,
    LadderRungInput,
    StrategicLadderObservationContext,
    StrategicLadderValidationRequest,
)
from nvda_desk.upstream.market_substrate import build_market_substrate_snapshot
from nvda_desk.upstream.strategic_ladder import StrategicLadderMarketService


def test_market_substrate_snapshot_preserves_trace_only_rich_observation_context() -> None:
    snapshot = build_market_substrate_snapshot(
        substrate_id="substrate-1",
        observations=[
            MarketSubstrateObservation(
                observation_id="obs-price",
                signal_family_id="spot_price",
                symbol="NVDA",
                value=Decimal("121.50"),
                units="usd",
                source_ids=["quote-feed"],
                tags=["liquid"],
            ),
            MarketSubstrateObservation(
                observation_id="obs-gamma",
                signal_family_id="negative_gamma",
                symbol="NVDA",
                value=Decimal("1"),
                units="flag",
                source_ids=["options-feed"],
                tags=["risk_context"],
            ),
        ],
    )

    assert isinstance(snapshot, MarketSubstrateSnapshot)
    assert snapshot.signal_family_ids == ["negative_gamma", "spot_price"]
    assert snapshot.by_signal_family("spot_price")[0].observation_id == "obs-price"
    assert snapshot.decision_authority == "trace_only_market_substrate"
    assert snapshot.trade_decision_side_effects == []


def test_strategic_ladder_service_validates_rungs_against_observation_context_without_execution() -> (
    None
):
    service = StrategicLadderMarketService()
    request = StrategicLadderValidationRequest(
        request_id="ladder-request-1",
        rungs=[
            LadderRungInput(
                rung_id="r1", limit_price=Decimal("120.00"), notional_usd=Decimal("5000")
            ),
            LadderRungInput(
                rung_id="r2", limit_price=Decimal("124.00"), notional_usd=Decimal("2500")
            ),
        ],
        observation_context=StrategicLadderObservationContext(
            symbol="NVDA",
            spot_price=Decimal("121.50"),
            negative_gamma_active=True,
            event_risk_active=False,
            liquidity_state="normal",
        ),
    )

    output = service.validate_market_ladder(request)

    assert output.overall_decision == LadderDecision.REVISE
    assert [rung.rung_id for rung in output.rung_results] == ["r1", "r2"]
    assert output.rung_results[0].rung_decision == LadderDecision.REVISE
    assert output.rung_results[0].market_evidence.distance_from_spot == Decimal("1.50")
    assert output.strike_zone_signals[0].signal_id == "spot_distance"
    assert output.supervisory_overlay.overlay_state == "caution"
    assert output.execution_authority == "not_authorised"
