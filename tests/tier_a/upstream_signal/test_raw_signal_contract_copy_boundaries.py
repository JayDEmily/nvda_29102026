from __future__ import annotations

import pytest
from pydantic import ValidationError

from nvda_desk.contracts.upstream_signal import RawUpstreamSignalInput


def test_raw_signal_input_rejects_extra_contract_authority() -> None:
    with pytest.raises(ValidationError):
        RawUpstreamSignalInput(
            source_id="signal-feed-contract",
            signal_family_id="market_depth_imbalance",
            scope_id="sequence-gap006-upstream",
            payload={"imbalance": 0.42},
            trade_allowed=True,
        )


def test_raw_signal_input_detaches_payload_from_caller_mutation() -> None:
    caller_payload = {
        "imbalance": 0.42,
        "nested": {"venue": "NASDAQ", "depth": [10, 12]},
    }

    raw_signal = RawUpstreamSignalInput(
        source_id="signal-feed-contract",
        signal_family_id="market_depth_imbalance",
        scope_id="sequence-gap006-upstream",
        payload=caller_payload,
    )

    caller_payload["imbalance"] = 0.99
    caller_payload["nested"]["venue"] = "MUTATED"
    caller_payload["nested"]["depth"].append(99)

    assert raw_signal.payload == {
        "imbalance": 0.42,
        "nested": {"venue": "NASDAQ", "depth": [10, 12]},
    }
