"""Sequence 7 tests-first proof for the expected envelope specimen shape."""

from __future__ import annotations

import json
from pathlib import Path

_SPECIMEN = Path(
    "var/audit/specimens/parallel_risk_envelope/"
    "sequence7_parallel_risk_envelope_expected_packet.json"
)


def test_sequence7_expected_parallel_risk_envelope_specimen_is_bounded() -> None:
    """Validate the tests-first specimen stays inside independent risk-envelope authority."""

    specimen = json.loads(_SPECIMEN.read_text(encoding="utf-8"))
    packet = specimen["expected_packet"]
    envelope = packet["data"]["risk_envelope"]

    assert packet["packetrole"] == "parallel_risk_packet"
    assert packet["producer"]["grammar_role"] == "parallel_risk_lane"
    assert envelope["state_ladder"] == ["tight", "broad", "caution", "block"]
    assert envelope["decision_authority"] == "independent_risk_envelope_only"
    assert {item["source_family"] for item in envelope["contributions"]} == {
        "temporal_event_context",
        "options_repricing_context",
        "market_volatility_context",
    }

    forbidden_text = json.dumps(envelope, sort_keys=True)
    for token in specimen["forbidden_fields"]:
        assert token not in forbidden_text
