from __future__ import annotations

from copy import deepcopy

from nvda_desk.contracts.upstream_signal import RawUpstreamSignalInput
from nvda_desk.upstream.raw_signal_ingress import ingest_raw_upstream_signal


def _dataset_packet_payload() -> dict:
    return {
        "packet_id": "dataset-packet-1",
        "symbol": "NVDA",
        "features": {"spot_price": 101.0, "front_dte": 5},
        "decision": {"trade_allowed": False},
    }


def test_raw_signal_ingress_does_not_mutate_dataset_packet_payload() -> None:
    dataset_packet = _dataset_packet_payload()
    before = deepcopy(dataset_packet)
    raw_signal = RawUpstreamSignalInput(
        source_id="signal-feed-1",
        signal_family_id="market_depth_imbalance",
        scope_id="sequence-gap006-upstream",
        payload={"imbalance": 0.42},
    )

    result = ingest_raw_upstream_signal(
        raw_signal=raw_signal,
        dataset_packet_payload=dataset_packet,
        admitted_signal_families={"market_depth_imbalance"},
    )

    assert dataset_packet == before
    assert result.dataset_packet_payload == before
    assert result.sanity_trace.source_id == "signal-feed-1"
    assert result.sanity_trace.scope_id == "sequence-gap006-upstream"
    assert result.sanity_trace.signal_family_id == "market_depth_imbalance"
    assert result.sanity_trace.disposition == "admitted_trace_only"
    assert result.trade_decision_side_effects == []


def test_upstream_sanity_trace_records_source_scope_and_rejection_reason() -> None:
    raw_signal = RawUpstreamSignalInput(
        source_id="unknown-feed",
        signal_family_id="undeclared_alpha_hint",
        scope_id="sequence-gap006-upstream",
        payload={"hint": "buy now"},
    )

    result = ingest_raw_upstream_signal(
        raw_signal=raw_signal,
        dataset_packet_payload=_dataset_packet_payload(),
        admitted_signal_families={"market_depth_imbalance"},
    )

    assert result.quarantined is True
    assert result.sanity_trace.source_id == "unknown-feed"
    assert result.sanity_trace.scope_id == "sequence-gap006-upstream"
    assert result.sanity_trace.signal_family_id == "undeclared_alpha_hint"
    assert result.sanity_trace.rejection_reason == "signal_family_not_admitted"
    assert result.sanity_trace.disposition == "rejected_quarantined"


def test_non_interference_boundary_prevents_trade_decision_side_effects() -> None:
    raw_signal = RawUpstreamSignalInput(
        source_id="signal-feed-2",
        signal_family_id="market_depth_imbalance",
        scope_id="sequence-gap006-upstream",
        payload={"trade_allowed": True, "order_qty": 1000},
    )

    result = ingest_raw_upstream_signal(
        raw_signal=raw_signal,
        dataset_packet_payload=_dataset_packet_payload(),
        admitted_signal_families={"market_depth_imbalance"},
    )

    assert result.quarantined is False
    assert result.trade_decision_side_effects == []
    assert "trade_allowed" not in result.trace_envelope
    assert "order_qty" not in result.trace_envelope


def test_non_interference_boundary_strips_forbidden_runtime_keys_from_trace_payload() -> None:
    raw_signal = RawUpstreamSignalInput(
        source_id="signal-feed-3",
        signal_family_id="market_depth_imbalance",
        scope_id="sequence-gap006-upstream",
        payload={
            "imbalance": 0.51,
            "trade_allowed": True,
            "authorised_notional_usd": 1_000_000,
            "brokerage_order": {"side": "BUY"},
        },
    )

    result = ingest_raw_upstream_signal(
        raw_signal=raw_signal,
        dataset_packet_payload=_dataset_packet_payload(),
        admitted_signal_families={"market_depth_imbalance"},
    )

    assert result.quarantined is False
    assert result.trace_envelope["payload"] == {"imbalance": 0.51}
    assert result.trade_decision_side_effects == []


def test_non_interference_boundary_strips_nested_forbidden_runtime_keys_from_trace_payload() -> None:
    raw_signal = RawUpstreamSignalInput(
        source_id="signal-feed-4",
        signal_family_id="market_depth_imbalance",
        scope_id="sequence-gap006-upstream",
        payload={
            "imbalance": 0.63,
            "metadata": {
                "venue": "NASDAQ",
                "trade_allowed": True,
                "nested": {"authorised_notional_usd": 2_000_000, "lot_count": 7},
            },
            "observations": [
                {"depth": 10, "order_qty": 500},
                {"depth": 12, "venue": "ARCA"},
            ],
        },
    )

    result = ingest_raw_upstream_signal(
        raw_signal=raw_signal,
        dataset_packet_payload=_dataset_packet_payload(),
        admitted_signal_families={"market_depth_imbalance"},
    )

    assert result.quarantined is False
    assert result.trace_envelope["payload"] == {
        "imbalance": 0.63,
        "metadata": {"venue": "NASDAQ", "nested": {"lot_count": 7}},
        "observations": [{"depth": 10}, {"depth": 12, "venue": "ARCA"}],
    }
    assert result.trade_decision_side_effects == []
