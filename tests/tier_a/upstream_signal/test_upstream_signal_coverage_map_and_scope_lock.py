from __future__ import annotations

import pytest

from nvda_desk.contracts.dataset_packets import build_dataset_packet_signal_view
from nvda_desk.contracts.upstream_signal import UpstreamSignalCoverageEntry
from nvda_desk.upstream.raw_signal_coverage import (
    UpstreamSignalScopeLockError,
    build_upstream_signal_coverage_map,
    validate_upstream_signal_scope,
)


def _coverage_map():
    return build_upstream_signal_coverage_map(
        [
            UpstreamSignalCoverageEntry(
                owner="parallel_risk_lane",
                signal_family_id="market_depth_imbalance",
                source_scope="sequence-gap006-upstream",
                packet_fields=["imbalance", "venue"],
                promotion_status="trace_only",
            ),
            UpstreamSignalCoverageEntry(
                owner="parallel_risk_lane",
                signal_family_id="headline_risk_marker",
                source_scope="sequence-gap006-upstream",
                packet_fields=["headline_id", "risk_tag"],
                promotion_status="quarantine_required",
            ),
        ]
    )


def test_signal_coverage_map_declares_every_admitted_upstream_signal() -> None:
    coverage_map = _coverage_map()

    assert set(coverage_map.admitted_signal_family_ids) == {
        "market_depth_imbalance",
        "headline_risk_marker",
    }
    depth_entry = coverage_map.require("market_depth_imbalance")
    assert depth_entry.owner == "parallel_risk_lane"
    assert depth_entry.packet_fields == ["imbalance", "venue"]
    assert depth_entry.promotion_status == "trace_only"


def test_scope_lock_rejects_unlisted_signal_family() -> None:
    with pytest.raises(UpstreamSignalScopeLockError, match="unlisted_signal_family"):
        validate_upstream_signal_scope(
            signal_family_id="undeclared_alpha_hint",
            coverage_map=_coverage_map(),
        )


def test_dataset_packet_contract_boundary_is_explicit() -> None:
    view = build_dataset_packet_signal_view(
        packet_id="dataset-packet-2",
        signal_family_id="market_depth_imbalance",
        payload={
            "imbalance": 0.42,
            "venue": "NASDAQ",
            "undeclared_signal_key": "must-not-cross",
        },
        coverage_map=_coverage_map(),
    )

    assert view.packet_id == "dataset-packet-2"
    assert view.signal_family_id == "market_depth_imbalance"
    assert view.exposed_fields == {"imbalance": 0.42, "venue": "NASDAQ"}
    assert view.rejected_fields == {"undeclared_signal_key": "must-not-cross"}
