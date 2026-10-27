"""Independent authority-derived public depth/error/restart discovery sequence."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from dataclasses import fields
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

T = datetime(2026, 10, 20, 12, 39, 59, tzinfo=UTC)
SUBJECT = "independent-L04-STK"
PROVIDER = "independent-L04-synthetic"
VARIANT = "independent-depth-controls/1"


def native(value):
    if isinstance(value, Mapping):
        return {key: native(item) for key, item in value.items()}
    if type(value) is Decimal:
        return {"native_type": "Decimal", "value": str(value)}
    if type(value) is datetime:
        return {"native_type": "datetime", "value": value.isoformat()}
    return {"native_type": type(value).__name__, "value": value}


def record(value):
    result = {}
    for field in fields(value):
        item = getattr(value, field.name)
        if field.name == "native_record":
            item = native(item)
        elif field.name == "received_ts_utc":
            item = item.isoformat()
        elif field.name == "raw_signal_catalogue_ids":
            item = [key.value for key in item] if item is not None else None
        elif hasattr(item, "value"):
            item = item.value
        result[field.name] = item
    return result


def owner(path, create=False):
    return r.create_owner(durability_port=create_sqlite_persistence(str(path), create=create))


def discover(raw, cutoff, generation="G1", after=False):
    path = ("_collector", "control", "generation_after") if after else ("_collector", "generation")
    selected = []
    cursor = None
    seen = set()
    for _ in range(100):
        page = raw.reads.list_raw_observation_history(
            subject_instrument=SUBJECT,
            source_provider=PROVIDER,
            source_variant=VARIANT,
            received_at_or_before_utc=cutoff,
            native_identity_selectors=((('_collector', 'request'), 'REQUEST-7'), (path, generation)),
            limit=1,
            cursor=cursor,
        )
        assert len(page.items) <= 1
        selected.extend(record(value) for value in page.items)
        cursor = page.next_cursor
        if cursor is None:
            return selected
        assert cursor not in seen
        seen.add(cursor)
    raise AssertionError("non-exhausting public cursor")


def read(path):
    raw = owner(path)
    return {
        "all": discover(raw, T + timedelta(seconds=1)),
        "before_error": discover(raw, T),
        "at_error": discover(raw, T + timedelta(milliseconds=100)),
        "before_restart": discover(raw, T + timedelta(milliseconds=199)),
        "g2_ordinary": discover(raw, T + timedelta(seconds=1), "G2"),
        "g2_incoming": discover(raw, T + timedelta(seconds=1), "G2", True),
    }


def occurrence(identifier, offset, sequence, callback, control=None):
    collector = {"schema_version": "collector-control-transport/1", "origin": "synthetic",
                 "subject": SUBJECT, "request": "REQUEST-7", "generation": "G1",
                 "requested_exchange": "SMART"}
    if control is not None:
        collector["control"] = control
    return r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(identifier),
        delivery_artifact_ref=r.delivery_artifact_ref("independent-delivery:" + identifier),
        source_provider=r.provider_id(PROVIDER),
        native_record={**callback, "_collector": collector},
        received_ts_utc=T + timedelta(milliseconds=offset),
        ingestion_sequence=sequence,
        ingestion_sequence_scope=r.ingestion_sequence_scope("independent-L04-scope"),
        source_temporal_kind="receipt_only",
        raw_signal_catalogue_ids=None if control is not None else (r.RawSignalCatalogueId("R187"),),
        source_variant=VARIANT,
        subject_instrument=SUBJECT,
        source_endpoint_callback="updateMktDepthL2" if control is None else (
            "error" if control["origin"] == "provider_callback" else "collectorControl"
        ),
    )


def main():
    path = Path(tempfile.mkdtemp(prefix="l04-independent-")) / "observations.db"
    raw = owner(path, True)
    depth = occurrence("review-depth", 0, 1, {
        "operation": 0, "side": 1, "position": 0,
        "price": Decimal("99.00"), "size": Decimal("5.00"),
    })
    base_control = {"schema_version": "m00-control-envelope/1", "request": "REQUEST-7",
                    "generation_before": "G1", "generation_after": "G1", "invalidates": True}
    error = occurrence("review-error", 100, 2,
                       {"reqId": 7, "errorCode": 317, "errorString": "synthetic reset"},
                       {**base_control, "kind": "error317", "origin": "provider_callback"})
    restart = occurrence("review-restart", 200, 3, {}, {
        **base_control, "kind": "restart", "origin": "collector_control", "generation_after": "G2",
    })
    raw.commands.admit_raw_observation_occurrence(depth)
    assert discover(raw, T + timedelta(seconds=1)) == [record(depth)]
    raw.commands.admit_raw_observation_occurrence(error)
    assert discover(raw, T + timedelta(seconds=1)) == [record(depth), record(error)]
    mapping = r.RawSignalProjectionMappingV1("independent-operation", 1,
        r.RawSignalCatalogueId("R187"), PROVIDER, VARIANT, ("operation",), "operation")
    assert raw.reads.project_raw_value(r.RawSignalCatalogueId("R187"),
        error.observation_occurrence_id, mappings=(mapping,)) is None
    raw.commands.admit_raw_observation_occurrence(restart)
    # One noticed contract edge: any valid ASCII digit cursor beyond this
    # population is empty, even beyond CPython's decimal int conversion limit.
    beyond = raw.reads.list_raw_observation_history(
        subject_instrument=SUBJECT, source_provider=PROVIDER, source_variant=VARIANT,
        received_at_or_before_utc=T + timedelta(seconds=1),
        native_identity_selectors=(), limit=1, cursor="9" * 5000,
    )
    assert beyond.items == () and beyond.next_cursor is None
    expected = {"all": [record(depth), record(error), record(restart)],
                "before_error": [record(depth)], "at_error": [record(depth), record(error)],
                "before_restart": [record(depth), record(error)], "g2_ordinary": [],
                "g2_incoming": [record(restart)]}
    del raw
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    assert read(path) == expected
    env = dict(os.environ)
    child = subprocess.run([sys.executable, __file__, "read", str(path)],
                           env=env, capture_output=True, text=True, check=True)
    assert json.loads(child.stdout) == expected
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    print("DIRECT_SEQUENCE_PASS", json.dumps({"observation_count": 3,
        "provider_error": 317, "restart": "G1->G2", "incoming_boundary_discovered": True,
        "long_valid_cursor_digits": 5000, "long_valid_cursor_result": "EMPTY",
        "known_control_ids_in_queries": False, "fresh_readonly_bytes_unchanged": True}, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "read":
        print(json.dumps(read(Path(sys.argv[2])), sort_keys=True))
    else:
        main()
