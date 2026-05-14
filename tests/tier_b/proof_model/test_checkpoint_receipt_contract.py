from __future__ import annotations

from datetime import UTC, datetime

from nvda_desk.downstream.checkpoints import PreparedIngressCheckpoint
from nvda_desk.preparation.runtime_preparer import (
    PreparedRuntimeLineage,
    PreparedRuntimeSnapshot,
)


def _snapshot(*, failed: list[str] | None = None) -> PreparedRuntimeSnapshot:
    return PreparedRuntimeSnapshot(
        snapshot_id="snapshot::prepared-ingress::001",
        payload={"source_time_utc": datetime(2026, 4, 22, 9, 31, tzinfo=UTC), "spot": 101.25},
        lineage=PreparedRuntimeLineage(
            source_kind="raw_bundle",
            transport="fixture",
            source_snapshot_id="raw::001",
            source_sections=("quote", "calendar"),
            alignment_policy="explicit_runtime_bar_time_utc",
            runtime_bar_time_utc=datetime(2026, 4, 22, 9, 31, tzinfo=UTC),
            derived_field_names=("window_count",),
        ),
        derived_fields={"window_count": 1},
        missing_optional_enrichments=["minutes_to_next_event:next_event_time_utc"],
        failed_enrichments=list(failed or []),
    )


def test_prepared_ingress_checkpoint_receipt_is_detached_and_valid_without_failures() -> None:
    snapshot = _snapshot()

    checkpoint = PreparedIngressCheckpoint.from_snapshot("prepared_ingress", snapshot)
    payload = checkpoint.as_receipt_payload(snapshot)

    assert checkpoint.status == "valid"
    assert payload["checkpoint_id"] == "prepared_ingress"
    assert payload["snapshot_id"] == "snapshot::prepared-ingress::001"
    assert payload["status"] == "valid"
    assert payload["alignment_policy"] == "explicit_runtime_bar_time_utc"
    assert payload["source_sections"] == ["quote", "calendar"]
    assert payload["missing_optional_enrichments"] == [
        "minutes_to_next_event:next_event_time_utc"
    ]
    assert payload["failed_enrichments"] == []
    assert payload["prepared_context"]["payload"]["spot"] == 101.25
    assert payload["prepared_context"]["source_kind"] == "raw_bundle"

    payload["prepared_context"]["payload"]["spot"] = 999.0
    assert snapshot.payload["spot"] == 101.25


def test_prepared_ingress_checkpoint_receipt_degrades_when_enrichment_fails() -> None:
    snapshot = _snapshot(failed=["window_count:windows_not_list"])

    checkpoint = PreparedIngressCheckpoint.from_snapshot("prepared_ingress", snapshot)
    payload = checkpoint.as_receipt_payload(snapshot)

    assert checkpoint.status == "degraded"
    assert payload["status"] == "degraded"
    assert payload["failed_enrichments"] == ["window_count:windows_not_list"]
    assert payload["prepared_context"]["failed_enrichments"] == [
        "window_count:windows_not_list"
    ]
