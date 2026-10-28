"""L02 fixed source/control pair; authored for independent L14 execution only."""

import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "support"))
from native_reconciliation import PublicDtoReader, typed_tree

BRIEF = "5b777c5842b091f6dc4bef148970c4cf81b68864bd24f5a1633d392f38d96ead"
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF)
A4 = f.VersionRefV1("native-a4-stock", 1)
G2 = f.VersionRefV1("native-receipt-controls", 1)


def _request(ref, offset_ms):
    return f.NativeSourceRequestV1(
        ref, T + timedelta(milliseconds=offset_ms), T + timedelta(seconds=1)
    )


def _control(
    source, *, kind, receipt, identity, before="STK-SMART-G1", after="STK-SMART-G1", sequence=25
):
    template = next(
        o
        for o in source.observations
        if o.observation_occurrence_id.value == "NVDA-M00-A-V1-A4-SEQ21"
    )
    native = dict(template.native_record)
    collector = dict(native["_collector"])
    collector["control"] = {
        "schema_version": "m00-control-envelope/1",
        "kind": kind,
        "origin": "collector_control" if kind == "restart" else "provider_callback",
        "request": "STK-SMART-R1",
        "generation_before": before,
        "generation_after": after,
        "invalidates": True,
    }
    native = {"_collector": collector, "errorCode": 317 if kind == "error317" else 0}
    return replace(
        template,
        observation_occurrence_id=raw.observation_occurrence_id(identity),
        native_record=native,
        received_ts_utc=receipt,
        ingestion_sequence=sequence,
        raw_signal_catalogue_ids=None,
        source_endpoint_callback="error" if kind == "error317" else "collectorControl",
    )


def _g2_callback(source, original, identity, side, size, receipt, sequence):
    template = next(o for o in source.observations if o.observation_occurrence_id.value == original)
    native = dict(template.native_record)
    collector = dict(native["_collector"])
    collector["generation"] = "STK-SMART-G2"
    native["_collector"] = collector
    native.update(position=0, operation=0, side=side, size=size)
    changed = replace(
        template,
        observation_occurrence_id=raw.observation_occurrence_id(identity),
        native_record=native,
        received_ts_utc=receipt,
        ingestion_sequence=sequence,
        ingestion_sequence_scope=raw.ingestion_sequence_scope("STK1/SMART/G2"),
    )
    return changed


def _append_g2(source):
    # Exact L01 recipe: one outgoing/incoming boundary and two fresh contiguous rows.
    source.observations.append(
        _control(
            source,
            kind="restart",
            receipt=T - timedelta(milliseconds=100),
            identity="REC-HELPER-RESTART",
            after="STK-SMART-G2",
            sequence=29,
        )
    )
    selected = (
        (
            "NVDA-M00-A-V1-A4-SEQ21",
            "REC-HELPER-G2-B0",
            1,
            Decimal(5),
            T + timedelta(milliseconds=100),
            30,
        ),
        (
            "NVDA-M00-A-V1-A4-SEQ23",
            "REC-HELPER-G2-A0",
            0,
            Decimal(2),
            T + timedelta(milliseconds=200),
            31,
        ),
    )
    for original, identity, side, size, receipt, sequence in selected:
        source.observations.append(
            _g2_callback(source, original, identity, side, size, receipt, sequence)
        )
        for old in tuple(source.projections):
            if old.observation_occurrence_id.value != original:
                continue
            native_value = (
                size
                if old.raw_signal_catalogue_id.value == "R190"
                else 0
                if old.raw_signal_catalogue_id.value == "R185"
                else side
                if old.raw_signal_catalogue_id.value == "R188"
                else old.native_value
            )
            identity_values = tuple(
                (key, "STK-SMART-G2" if key == "generation" else value)
                for key, value in old.selection_identity.values
            )
            source.projections.append(
                replace(
                    old,
                    observation_occurrence_id=raw.observation_occurrence_id(identity),
                    received_ts_utc=receipt,
                    ingestion_sequence=sequence,
                    ingestion_sequence_scope=raw.ingestion_sequence_scope("STK1/SMART/G2"),
                    native_value=native_value,
                    selection_identity=raw.RawSelectionIdentityV1(identity_values),
                )
            )


def test_native_source_success(tmp_path):
    source = PublicDtoReader(scenarios=("A4", "A3"))  # A3 is an unrelated option source.
    path = tmp_path / "native-source.sqlite"
    owner = f.create_native_source_owner(
        admission=ADMISSION,
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(path), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    prefix = owner.materialise(_request(A4, -600))
    assert prefix is not None
    assert tuple((x.side, x.position, x.size) for x in prefix.standing_rows) == (
        (1, 0, Decimal(5)),
        (1, 1, Decimal(3)),
        (0, 0, Decimal(2)),
        (0, 1, Decimal(4)),
    )
    assert all(
        x.time_basis == "collector_receipt"
        and x.event_time_utc is None
        and x.received_ts_utc == x.projection.received_ts_utc
        for x in prefix.raw_input_lineage
    )
    assert all(value is None for value in source.event_filters)
    _append_g2(source)
    # The G1 query sees the outgoing boundary; G2 sees the same immutable ID by
    # generation_after without the caller supplying its ID or relabelling it.
    assert owner.materialise(_request(A4, 0)) is None
    new = owner.materialise(_request(G2, 300))
    assert new is not None
    assert len(new.controls) == 1
    assert new.controls[0].observation.observation_occurrence_id.value == "REC-HELPER-RESTART"
    assert (new.controls[0].generation_before, new.controls[0].generation_after) == (
        "STK-SMART-G1",
        "STK-SMART-G2",
    )
    assert tuple((x.side, x.position, x.size) for x in new.standing_rows) == (
        (1, 0, Decimal(5)),
        (0, 0, Decimal(2)),
    )
    assert source.control_queries >= 3
    before = path.read_bytes()
    reader = f.create_native_source_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(path))
    )
    old_read = reader.get_source_snapshot(prefix.source_snapshot_id)
    new_read = reader.get_source_snapshot(new.source_snapshot_id)
    assert type(old_read) is f.NativeSourceSnapshotV1
    assert type(new_read) is f.NativeSourceSnapshotV1
    assert typed_tree(old_read) == typed_tree(prefix)
    assert typed_tree(new_read) == typed_tree(new)
    history = reader.list_source_history(
        source_profile_ref=G2,
        effective_at_or_before_utc=T + timedelta(milliseconds=300),
        knowledge_at_or_before_utc=T + timedelta(seconds=1),
        limit=1,
    )
    assert len(history) == 1 and typed_tree(history[0]) == typed_tree(new)
    assert path.read_bytes() == before


def test_native_source_refusal(tmp_path):
    source = PublicDtoReader(scenarios=("A4",))
    owner = f.create_native_source_owner(
        admission=ADMISSION,
        raw_reader=source,
        storage=f.SQLiteStorageV1(str(tmp_path / "refusal.sqlite"), True),
        utc_now=lambda: T + timedelta(seconds=2),
    )
    source.observations.append(
        _control(
            source,
            kind="error317",
            receipt=T - timedelta(milliseconds=500),
            identity="REC-HELPER-ERROR317",
        )
    )
    assert owner.materialise(_request(A4, -400)) is None
    assert (
        owner.reads.list_source_history(
            source_profile_ref=A4,
            effective_at_or_before_utc=T,
            knowledge_at_or_before_utc=T + timedelta(seconds=1),
            limit=10,
        )
        == ()
    )
    # Distinct relevant callbacks at one exact receipt, scope and sequence are
    # unorderable. Their lexicographic occurrence IDs cannot break the tie.
    source.observations = [
        o for o in source.observations if o.observation_occurrence_id.value != "REC-HELPER-ERROR317"
    ]
    source.observations.append(
        _control(
            source,
            kind="restart",
            receipt=T - timedelta(milliseconds=100),
            identity="REC-HELPER-RESTART",
            after="STK-SMART-G2",
            sequence=29,
        )
    )
    original = "NVDA-M00-A-V1-A4-SEQ21"
    first = _g2_callback(
        source, original, "REC-TIE-A", 1, Decimal(5), T + timedelta(milliseconds=100), 30
    )
    second = _g2_callback(
        source, original, "REC-TIE-B", 1, Decimal(3), T + timedelta(milliseconds=100), 30
    )
    source.observations.extend((first, second))
    for item, amount in ((first, Decimal(5)), (second, Decimal(3))):
        for old in tuple(source.projections):
            if old.observation_occurrence_id.value == original:
                identity_values = tuple(
                    (key, "STK-SMART-G2" if key == "generation" else value)
                    for key, value in old.selection_identity.values
                )
                source.projections.append(
                    replace(
                        old,
                        observation_occurrence_id=item.observation_occurrence_id,
                        received_ts_utc=item.received_ts_utc,
                        ingestion_sequence=30,
                        ingestion_sequence_scope=item.ingestion_sequence_scope,
                        native_value=amount
                        if old.raw_signal_catalogue_id.value == "R190"
                        else old.native_value,
                        selection_identity=raw.RawSelectionIdentityV1(identity_values),
                    )
                )
    # Keep the exact authority-bound pair. Both callbacks are present with all
    # five required roles and identical causal coordinates. Public None also
    # covers absent fixed warm-up; independent source review verifies that the
    # complete causal-order preflight now runs before that warm-up refusal.
    assert {first.observation_occurrence_id.value, second.observation_occurrence_id.value} == {
        "REC-TIE-A",
        "REC-TIE-B",
    }
    assert (first.received_ts_utc, first.ingestion_sequence_scope, first.ingestion_sequence) == (
        second.received_ts_utc,
        second.ingestion_sequence_scope,
        second.ingestion_sequence,
    )
    assert first.received_ts_utc == T + timedelta(milliseconds=100)
    assert first.ingestion_sequence == 30
    for tied in (first, second):
        assert {
            x.raw_signal_catalogue_id.value
            for x in source.projections
            if x.observation_occurrence_id == tied.observation_occurrence_id
        } == {"R185", "R187", "R188", "R189", "R190"}
    assert owner.materialise(_request(G2, 300)) is None
    assert (
        owner.reads.list_source_history(
            source_profile_ref=G2,
            effective_at_or_before_utc=T + timedelta(milliseconds=300),
            knowledge_at_or_before_utc=T + timedelta(seconds=1),
            limit=10,
        )
        == ()
    )
