"""Deterministic fixture contracts for cognition-runtime tests.

Gate C requires every runtime-oriented test to build from a typed fixture
contract rather than free-form dictionaries.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    TemporalContextInput,
)


class CognitionRuntimeFixture(BaseModel):
    """Typed fixture contract for one full desk-runtime test case."""

    model_config = ConfigDict(extra="forbid")

    fixture_id: str
    temporal_input: TemporalContextInput
    regime_input: MarketRegimeContextInput
    options_flow_input: OptionsFlowContextInput
    inventory_state: InventoryState
    risk_budget_remaining_pct: float = Field(ge=0.0, le=100.0)


def supportive_runtime_fixture() -> CognitionRuntimeFixture:
    """Return one supportive deterministic runtime fixture."""

    return CognitionRuntimeFixture(
        fixture_id="supportive_runtime_fixture",
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T14:15:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            next_event_at=datetime.fromisoformat("2026-03-23T15:30:00-04:00"),
            prior_session_return_pct=1.4,
            intraday_move_pct=0.8,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=0.8,
            nq_return_pct=0.5,
            es_return_pct=0.3,
            sox_return_pct=0.9,
            breadth_score=0.67,
            concentration_score=0.41,
            vix_level=18.4,
            vvix_level=84.0,
            us10y=4.22,
            us2y=4.04,
            usdjpy=148.9,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=118.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=61.0,
            next_atm_iv=60.1,
            put_call_skew=0.18,
            gamma_pressure_score=0.33,
            call_put_imbalance=-0.05,
            oi_concentration=0.44,
            atm_straddle_value=5.9,
            vix_level=18.4,
            vvix_level=84.0,
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=10.0,
            fresh_cash_pct=70.0,
            overnight_inventory_pct=0.0,
            open_orders_count=0,
            capital_lockup_pct=12.0,
            cost_basis_gap_pct=0.5,
            thesis_state_input="valid",
            adverse_excursion_pct=-1.0,
            time_stop_minutes_remaining=180,
        ),
        risk_budget_remaining_pct=68.0,
    )


def stressed_runtime_fixture() -> CognitionRuntimeFixture:
    """Return one stressed deterministic runtime fixture."""

    return CognitionRuntimeFixture(
        fixture_id="stressed_runtime_fixture",
        temporal_input=TemporalContextInput(
            ts=datetime.fromisoformat("2026-03-23T10:20:00-04:00"),
            next_expiry=datetime.fromisoformat("2026-03-27T16:00:00-04:00"),
            prior_session_return_pct=-2.0,
            intraday_move_pct=-3.5,
        ),
        regime_input=MarketRegimeContextInput(
            nvda_return_pct=-3.5,
            nq_return_pct=-1.4,
            es_return_pct=-0.9,
            sox_return_pct=-2.2,
            breadth_score=0.28,
            concentration_score=0.84,
            vix_level=31.0,
            vvix_level=122.0,
            us10y=4.6,
            us2y=4.8,
            usdjpy=143.4,
        ),
        options_flow_input=OptionsFlowContextInput(
            spot_price=105.0,
            front_dte=4,
            next_dte=11,
            front_atm_iv=78.0,
            next_atm_iv=74.0,
            put_call_skew=0.62,
            gamma_pressure_score=0.82,
            call_put_imbalance=0.22,
            oi_concentration=0.77,
            atm_straddle_value=8.4,
            vix_level=31.0,
            vvix_level=122.0,
        ),
        inventory_state=InventoryState(
            existing_inventory_pct=40.0,
            fresh_cash_pct=55.0,
            overnight_inventory_pct=15.0,
            open_orders_count=2,
            capital_lockup_pct=78.0,
            cost_basis_gap_pct=-10.0,
            thesis_state_input="fragile",
            adverse_excursion_pct=-11.0,
            time_stop_minutes_remaining=10,
        ),
        risk_budget_remaining_pct=48.0,
    )
