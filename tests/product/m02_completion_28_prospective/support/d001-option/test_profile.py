"""INERT D001 option-time proof authoring candidate; never import or collect as Worker.
Prospective physical path: tests/product/m02_completion_28_prospective/support/d001-option/test_profile.py.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw


def _pinned(path, digest):
    content = (ROOT / path).read_bytes()
    assert hashlib.sha256(content).hexdigest() == digest
    return json.loads(content)


def _native(value):
    if isinstance(value, dict):
        if value.get("native_type") == "Decimal":
            assert set(value) == {"native_type", "text"}
            assert type(value["text"]) is str
            return Decimal(value["text"])
        return {k: _native(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_native(v) for v in value]
    return value


def _exact(value):
    if isinstance(value, Mapping):
        return ("mapping", tuple(sorted((k, _exact(v)) for k, v in value.items())))
    if type(value) in (tuple, list):
        return (type(value), tuple(_exact(v) for v in value))
    if type(value) is Decimal:
        return (Decimal, value.as_tuple())
    if type(value) is datetime:
        return (datetime, value.isoformat(), value.fold, type(value.tzinfo))
    if is_dataclass(value) and not isinstance(value, type):
        return (type(value), tuple((x.name, _exact(getattr(value, x.name))) for x in fields(value)))
    return (type(value), value)


def _compare(actual, expected, cls):
    assert type(actual) is cls
    assert {x.name for x in fields(cls)} == set(expected)
    for k, v in expected.items():
        assert _exact(getattr(actual, k)) == _exact(v), k


def _path(value, path):
    for key in path:
        value = value[key]
    return value


def _mapping(literal):
    return raw.RawSignalProjectionMappingV1(
        mapping_id=literal["mapping_id"], version=literal["version"],
        raw_signal_catalogue_id=raw.RawSignalCatalogueId(literal["raw_signal_catalogue_id"]),
        source_provider=literal["source_provider"], source_variant=literal["source_variant"],
        native_field_path=tuple(literal["native_field_path"]), native_units=literal["native_units"],
        selection_identity_field_paths=tuple(
            (name, tuple(path)) for name, path in literal["selection_identity_field_paths"]
        ),
    )


def _original(actual, literal):
    names = {x.name for x in fields(raw.RawObservationOccurrenceV1)}
    assert set(literal) <= names
    expected = dict.fromkeys(names)  # omitted optional native metadata must be absent
    expected.update(literal)
    expected.update(
        concept_id=raw.concept_id(literal["concept_id"]),
        contract_id=raw.contract_id(literal["contract_id"]),
        observation_occurrence_id=raw.observation_occurrence_id(literal["observation_occurrence_id"]),
        delivery_artifact_ref=raw.delivery_artifact_ref(literal["delivery_artifact_ref"]),
        source_provider=raw.provider_id(literal["source_provider"]),
        native_record=_native(literal["native_record"]),
        received_ts_utc=datetime.fromisoformat(literal["received_ts_utc"]),
        ingestion_sequence_scope=raw.ingestion_sequence_scope(literal["ingestion_sequence_scope"]),
        raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(r) for r in literal["raw_signal_catalogue_ids"]),
    )
    _compare(actual, expected, raw.RawObservationOccurrenceV1)


def _projection(actual, literal, mapping):
    native = _native(literal["native_record"])
    _compare(actual, dict(
        raw_signal_catalogue_id=mapping.raw_signal_catalogue_id,
        observation_occurrence_id=raw.observation_occurrence_id(literal["observation_occurrence_id"]),
        projection_mapping_id=mapping.mapping_id, projection_mapping_version=mapping.version,
        source_provider=literal["source_provider"], source_variant=literal["source_variant"],
        native_field_path=mapping.native_field_path, native_value=_path(native, mapping.native_field_path),
        native_units=mapping.native_units, subject_instrument=literal["subject_instrument"],
        source_temporal_kind=literal["source_temporal_kind"],
        source_timestamp_raw=literal["source_timestamp_raw"],
        source_timezone_native=literal["source_timezone_native"],
        received_ts_utc=datetime.fromisoformat(literal["received_ts_utc"]),
        ingestion_sequence=literal["ingestion_sequence"],
        ingestion_sequence_scope=raw.ingestion_sequence_scope(literal["ingestion_sequence_scope"]),
        revision_vintage_native=literal["revision_vintage_native"],
        selection_identity=raw.RawSelectionIdentityV1(tuple(
            (key, _path(native, path)) for key, path in mapping.selection_identity_field_paths
        )),
    ), raw.ProjectedRawValueV1)


def _case(case_id):
    policy = _pinned(POLICY, POLICY_SHA)["source"]
    inventory = _pinned(INVENTORY, INVENTORY_SHA)
    assert hashlib.sha256((ROOT / BRIEF).read_bytes()).hexdigest() == BRIEF_SHA
    assert hashlib.sha256((ROOT / BINDING).read_bytes()).hexdigest() == BINDING_SHA
    case, = [c for c in inventory["physical_cases"] if c["case_id"] == case_id]
    specimen, = [s for s in policy["exact_specimens"] if s["id"] == case["specimen"]]
    members = specimen["members"]
    packed = json.dumps(members, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                        allow_nan=False).encode("ascii")
    assert len(members) == specimen["member_count"]
    assert hashlib.sha256(packed).hexdigest() == specimen["expanded_member_sha256"] == case["specimen_sha256"]
    assert len({m["observation_occurrence_id"] for m in members}) == len(members)
    return policy, case, members


def _ordered(pairs):
    return tuple(sorted(pairs, key=lambda pair: (
        pair[1].received_ts_utc, pair[1].ingestion_sequence_scope.value,
        pair[1].ingestion_sequence, pair[1].observation_occurrence_id.value,
    )))


def _source_evidence(source, policy, case, members):
    # The proposed narrow source factory must internally admit the literal corpus
    # through actual public M00 commands then seal them. No test fake/raw adapter.
    assert source.specimen_id == case["specimen"]
    assert source.expanded_sha256 == case["specimen_sha256"]
    assert source.expanded_count == len(members)
    assert not hasattr(source, "commands")
    assert not hasattr(source, "admit_raw_observation_occurrence")
    mappings = {role: _mapping(spec) for role, spec in policy["role_mappings"].items()}
    actual = {}
    for literal in members:
        role, = literal["raw_signal_catalogue_ids"]
        oid = raw.observation_occurrence_id(literal["observation_occurrence_id"])
        original = source.get_raw_observation_occurrence(oid)
        projected = source.project_raw_value(raw.RawSignalCatalogueId(role), oid,
                                             mappings=(mappings[role],))
        _original(original, literal)
        _projection(projected, literal, mappings[role])
        actual[literal["observation_occurrence_id"]] = (original, projected)

    cutoff = datetime.fromisoformat(case["request_clock"]["knowledge_cutoff_utc"])
    visible = []
    for role, mapping in mappings.items():
        expected = _ordered(
            pair for pair in actual.values()
            if pair[1].raw_signal_catalogue_id == raw.RawSignalCatalogueId(role)
            and pair[0].received_ts_utc <= cutoff
        )
        cursor = None
        cursors = set()
        items = []
        for _ in range(20):
            page = source.list_projected_raw_history(
                raw.RawSignalCatalogueId(role), mappings=(mapping,), subject_instrument=SUBJECT,
                received_at_or_before_utc=cutoff, event_at_or_before_utc=None, limit=2, cursor=cursor,
            )
            assert type(page) is raw.ProjectedRawHistoryPageV1
            assert len(page.items) <= 2
            items.extend(page.items)
            if page.next_cursor is None:
                break
            assert page.items and page.next_cursor != cursor and page.next_cursor not in cursors
            cursors.add(page.next_cursor)
            cursor = page.next_cursor
        else:
            raise AssertionError("incomplete bounded history")
        assert len({p.observation_occurrence_id for p in items}) == len(items)
        assert _exact(tuple(items)) == _exact(tuple(p[1] for p in expected))
        visible.extend(expected)
    return mappings, actual, _ordered(visible)


def _history(reader, request):
    return reader.list_derived_history(
        derived_signal_id=SIGNAL, subject_instrument=SUBJECT,
        effective_at_or_before_utc=request.as_of_utc,
        knowledge_at_or_before_utc=request.knowledge_cutoff_utc, limit=10,
    )


def _assert_history(reader, request, expected):
    assert _exact(_history(reader, request)) == _exact(expected)
    # An unbounded-in-time check via the declared public seam catches extra rows.
    assert _exact(reader.list_derived_history(
        derived_signal_id=SIGNAL, subject_instrument=SUBJECT,
        effective_at_or_before_utc=datetime.max.replace(tzinfo=UTC),
        knowledge_at_or_before_utc=datetime.max.replace(tzinfo=UTC), limit=10,
    )) == _exact(expected)
    for row in expected:
        assert _exact(reader.get_derived_occurrence(row.derived_occurrence_id)) == _exact(row)

ROOT = Path(__file__).resolve().parents[5]
LEAF = "handoff/m02_completion_28_execution/L07a/"
POLICY = LEAF + "OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json"
INVENTORY = LEAF + "OPTION_TIME_FINITE_CASES_PROPOSED_20261127.json"
BRIEF = LEAF + "D001_IMPLEMENTATION_BRIEF.md"
BINDING = "implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml"
POLICY_SHA = "14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a"
INVENTORY_SHA = "638f8703e75c15b10c2e3772ef7a8ceb0a105a6845140d0e409d50c9a1f01c7f"
BRIEF_SHA = "222d0919c67c05f6436f985b8262ace985ab11dea30fc045333ee13fa10a8d8d"
BINDING_SHA = "ff80ea7dd3aa7674723b758dda9173356bda75119ba996ece5bf4c1a9ff2cf35"
SIGNAL = "D001"
SUBJECT = "controlled-nvda-c110-20261023"
PROFILE = f.VersionRefV1("t01-option-time-d001", 1)
DEFINITION = "T01-D001-OPTION-TIME-DEF-V1"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF_SHA)


def _definition():
    return f.CalculationDefinitionV1(
        'D001', DEFINITION, 'K01_TIME', 'Same actual true instant converted to aware UTC, preserving microseconds.',
        ('R002', 'R003'), (), 'P_TIME', 'UTC_datetime', 'aware_utc_datetime',
        (
            f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv', '67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549'),
            f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md', '603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c'),
            f.AuthorityArtifactRefV1('handoff/m02_completion_28_execution/L07a/OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json', '14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a'),
            f.AuthorityArtifactRefV1('handoff/m02_completion_28_execution/L07a/D001_IMPLEMENTATION_BRIEF.md', '222d0919c67c05f6436f985b8262ace985ab11dea30fc045333ee13fa10a8d8d'),
        ),
    )


def _prepare(tmp_path, case_id):
    policy, case, members = _case(case_id)
    assert case["request_frame"] == "MAIN" and case["actual_parent"] is None
    source = f.create_option_time_source(admission=ADMISSION, specimen_id=case["specimen"])
    assert type(source) is f.OptionTimeSourceV1
    maps, actual, visible = _source_evidence(source, policy, case, members)
    assert len(actual) == len(visible) == 7
    assert set(maps) == {"R001", "R002", "R003", "R004", "R013", "R023", "R024"}
    roles = {p[1].raw_signal_catalogue_id.value: p for p in visible}
    assert len(roles) == 7
    r2, r3 = roles["R002"], roles["R003"]
    for original, projection in (r2, r3):
        assert original.subject_instrument == SUBJECT
        assert original.native_record["contract"]["id"] == SUBJECT
        assert original.native_record["sample"]["id"] == "MAIN"
        assert original.received_ts_utc == datetime.fromisoformat("2026-10-22T19:59:59.250000Z")
    assert r2[0].native_units == "native_time" and r3[0].native_units == "native_timezone"
    assert r3[0].source_temporal_kind == "true_instant"
    assert r3[0].source_timestamp_raw == "2026-10-22T19:59:59.125000Z"
    assert r3[0].source_timezone_native == "UTC"
    assert r2[0].native_record["value"]["role"] == "source_timestamp"
    assert r3[0].native_record["value"]["role"] == "source_offset"
    clocks = case["request_clock"]
    request = f.OptionTimeRequestV1(
        derived_signal_id=SIGNAL, subject_instrument=SUBJECT, frame_id="MAIN",
        as_of_utc=datetime.fromisoformat(clocks["as_of_utc"]),
        knowledge_cutoff_utc=datetime.fromisoformat(clocks["knowledge_cutoff_utc"]),
        calculation_definition_version=DEFINITION, source_profile_ref=PROFILE,
        predecessor_occurrence_ids=(),
    )
    clock = [datetime.fromisoformat(clocks["calculated_at_utc"])]
    db = tmp_path / "d001-option.sqlite"
    owner = f.create_option_time_owner(
        admission=ADMISSION, source=source, storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    return source, owner, db, request, clock, case, maps, r2, r3


def _empty_reopen(request, db):
    # Reader is constructed independently from the ordinary on-disk store.
    reader = f.create_option_time_reader(admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)))
    _assert_history(reader, request, ())


def test_d001_success(tmp_path):
    source, owner, db, request, clock, case, maps, r2, r3 = _prepare(tmp_path, "SUP-D001-OPTION-SUCCESS")
    assert r2[0].source_temporal_kind == "true_instant"
    assert r2[0].source_timestamp_raw == r2[1].native_value
    assert r2[0].source_timezone_native == r3[1].native_value == "-04:00"
    event = datetime.fromisoformat(r2[0].source_timestamp_raw)
    assert event.strftime("%z") == "-0400"
    expected = event.astimezone(UTC)
    assert expected == datetime.fromisoformat(r3[0].source_timestamp_raw)
    assert expected == datetime.fromisoformat(case["oracle_only"]["result"])
    assert expected == request.as_of_utc < r2[0].received_ts_utc <= request.knowledge_cutoff_utc
    assert expected.microsecond == 125000
    row = owner.materialise(request)
    assert type(row) is f.OptionTimeOccurrenceV1
    assert re.fullmatch(r"mmtoptiontime1:[0-9a-f]{64}", row.derived_occurrence_id)
    _compare(row, dict(
        owner_object_id="M02", owner_namespace="neutral_market_measurement_truth/option_time/v1",
        implementation_brief_sha256=BRIEF_SHA, derived_signal_id=SIGNAL,
        derived_occurrence_id=row.derived_occurrence_id, request=request,
        definition=_definition(), source_policy_sha256=POLICY_SHA,
        source_profile_ref=PROFILE, projection_mappings=(maps["R002"], maps["R003"]),
        original_observations=(r2[0], r3[0]), selected_projections=(r2[1], r3[1]),
        predecessor_occurrence_ids=(), result=expected, units="UTC_datetime",
        result_shape="aware_utc_datetime", effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc, calculated_at_utc=clock[0],
    ), f.OptionTimeOccurrenceV1)
    assert row.result.tzinfo is UTC
    clock[0] = datetime.fromisoformat(case["oracle_only"]["replay_at"])
    assert _exact(owner.materialise(request)) == _exact(row)
    _assert_history(owner.reads, request, (row,))
    del owner, source
    reader = f.create_option_time_reader(admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)))
    _assert_history(reader, request, (row,))


def test_d001_date_only(tmp_path):
    source, owner, db, request, clock, case, maps, r2, r3 = _prepare(tmp_path, "SUP-D001-OPTION-REACHED_REFUSAL")
    assert case["expected_stage"] == "ACTUAL_R002_TEMPORAL_KIND"
    assert r2[0].source_temporal_kind == r2[1].source_temporal_kind == "date_only"
    assert r2[0].source_timestamp_raw == r2[1].native_value == "2026-10-22"
    assert r2[0].source_timezone_native is None and r3[1].native_value == "-04:00"
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d001_receipt_only(tmp_path):
    source, owner, db, request, clock, case, maps, r2, r3 = _prepare(tmp_path, "SUP-D001-OPTION-RECEIPT-ONLY")
    assert case["expected_stage"] == "ACTUAL_R002_TEMPORAL_KIND"
    assert r2[0].source_temporal_kind == r2[1].source_temporal_kind == "receipt_only"
    assert r2[0].source_timestamp_raw is None and r2[0].source_timezone_native is None
    assert datetime.fromisoformat(r2[1].native_value) == r2[0].received_ts_utc
    assert r3[1].native_value == "-04:00"
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d001_offset_mismatch(tmp_path):
    source, owner, db, request, clock, case, maps, r2, r3 = _prepare(tmp_path, "SUP-D001-OPTION-OFFSET-MISMATCH")
    assert case["expected_stage"] == "ACTUAL_R002_R003_OFFSET_AGREEMENT"
    assert r2[0].source_temporal_kind == r3[0].source_temporal_kind == "true_instant"
    assert r2[0].source_timestamp_raw == r2[1].native_value
    assert datetime.fromisoformat(r2[0].source_timestamp_raw).astimezone(UTC) == request.as_of_utc
    assert datetime.fromisoformat(r3[0].source_timestamp_raw) == request.as_of_utc
    assert r2[0].source_timezone_native == "-04:00" and r3[1].native_value == "-05:00"
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)
