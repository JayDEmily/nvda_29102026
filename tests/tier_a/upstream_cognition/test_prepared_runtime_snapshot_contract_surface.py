from __future__ import annotations

from datetime import datetime

from nvda_desk.preparation.runtime_preparer import prepare_runtime_snapshot


def test_prepared_runtime_snapshot_as_mapping_detaches_nested_payload() -> None:
    snapshot = prepare_runtime_snapshot(
        snapshot_id="prepared-copy-boundary",
        payload={
            "source_time_utc": datetime(2026, 4, 21, 9, 31, 45),
            "raw_context": {"windows": [{"event_id": "earnings"}]},
        },
    )

    exported = snapshot.as_mapping()
    exported["raw_context"]["windows"][0]["event_id"] = "mutated"

    assert snapshot.payload["raw_context"]["windows"][0]["event_id"] == "earnings"
