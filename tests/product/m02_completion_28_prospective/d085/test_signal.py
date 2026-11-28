"""INERT D085 documentary proof candidate; do not import or collect as Worker.
Prospective physical path: tests/product/m02_completion_28_prospective/d085/test_signal.py.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "GUARDRAILS.md").is_file())
LEAF = "handoff/m02_completion_28_execution/L07a/"
POLICY = LEAF + "OPTION_TIME_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json"
INVENTORY = LEAF + "OPTION_TIME_FINITE_CASES_PROPOSED_20261127.json"
POLICY_SHA = "14a3ba2308f519d90d11eb450ac484a2c922507b7e04041c740297527a1d847a"
INVENTORY_SHA = "638f8703e75c15b10c2e3772ef7a8ceb0a105a6845140d0e409d50c9a1f01c7f"
PARENT_BRIEF = LEAF + "D001_IMPLEMENTATION_BRIEF.md"
PARENT_BRIEF_SHA = "222d0919c67c05f6436f985b8262ace985ab11dea30fc045333ee13fa10a8d8d"
PARENT_BINDING = "implementation/authority/T01_D001_OPTION_TIME_AUTHORITY_BINDING.yaml"
PARENT_BINDING_SHA = "ff80ea7dd3aa7674723b758dda9173356bda75119ba996ece5bf4c1a9ff2cf35"
PARENT_DEFINITION = "T01-D001-OPTION-TIME-DEF-V1"
PARENT_PROFILE = f.VersionRefV1("t01-option-time-d001", 1)
PARENT_ADMISSION = f.OwnerAdmissionV1("M02", PARENT_BRIEF_SHA)
LOCAL_BRIEF = LEAF + "D003_IMPLEMENTATION_BRIEF.md"
LOCAL_BRIEF_SHA = "0c588c6d06690f2e8fd23898cb4c219263dfc9b0924b071b40c2f92098ee5344"
LOCAL_BINDING = "implementation/authority/T01_D003_OPTION_TIME_AUTHORITY_BINDING.yaml"
LOCAL_BINDING_SHA = "a26f84b5ea86e6b5899b303ac4fe0f79d0915f5d2106392f4cf3ba40cbd48637"
LOCAL_ADMISSION = f.OwnerAdmissionV1("M02", LOCAL_BRIEF_SHA)
LOCAL_PROFILE = f.VersionRefV1("t01-option-time-d003", 1)
LOCAL_DEFINITION = "T01-D003-OPTION-TIME-DEF-V1"
BRIEF = LEAF + "D004_IMPLEMENTATION_BRIEF.md"
BRIEF_SHA = "77f81c72a9fac1aafebda94a8ab97f3b4f0f9f0e089f4367f221f57aac9c775a"
BINDING = "implementation/authority/T01_D004_OPTION_TIME_AUTHORITY_BINDING.yaml"
BINDING_SHA = "50f49638a7202d2b10f7b89b6076971445b033bd74bf66f8ea17a0c6862123aa"
SIGNAL = "D004"
SUBJECT = "controlled-nvda-c110-20261023"
PROFILE = f.VersionRefV1("t01-option-time-d004", 1)
DEFINITION = "T01-D004-OPTION-TIME-DEF-V1"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF_SHA)
NAMESPACE = "neutral_market_measurement_truth/option_time_session/v1"
CALENDAR = f.VersionRefV1("t01-option-session-calendar", 1)
UNITS = "date"
SHAPE = "exchange_trading_date"
EQUATION = "Select the open half-open UTC calendar interval containing actual D003 event; return its trading date after both full schedules match."
ID_PATTERN = r"mmtoptiontimesession1:[0-9a-f]{64}"
ROLES = ("R023", "R024")


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
        return (datetime, value.isoformat(), value.fold, type(value.tzinfo), getattr(value.tzinfo, "key", None), value.astimezone(UTC).isoformat())
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


def _ordered(pairs):
    return tuple(sorted(pairs, key=lambda pair: (
        pair[1].received_ts_utc, pair[1].ingestion_sequence_scope.value,
        pair[1].ingestion_sequence, pair[1].observation_occurrence_id.value,
    )))


def _source_evidence(source, policy, case, members, cutoff):
    # The proposed narrow source factory must internally admit the literal corpus
    # through actual public M00 commands then seal them. No test fake/raw adapter.
    assert type(source) is f.OptionTimeSourceV1
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



def _specimen(policy, spec):
    specimen, = [s for s in policy["exact_specimens"] if s["id"] == spec["specimen"]]
    members = specimen["members"]
    packed = json.dumps(members, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                        allow_nan=False).encode("ascii")
    assert len(members) == specimen["member_count"] == 7
    assert hashlib.sha256(packed).hexdigest() == specimen["expanded_member_sha256"] == spec["specimen_sha256"]
    assert len({m["observation_occurrence_id"] for m in members}) == 7
    return members


def _request(signal, frame, clocks, definition, profile, predecessors):
    return f.OptionTimeRequestV1(
        derived_signal_id=signal, subject_instrument=SUBJECT, frame_id=frame,
        as_of_utc=datetime.fromisoformat(clocks["as_of_utc"]),
        knowledge_cutoff_utc=datetime.fromisoformat(clocks["knowledge_cutoff_utc"]),
        calculation_definition_version=definition, source_profile_ref=profile,
        predecessor_occurrence_ids=predecessors,
    )


def _history(reader, request, expected):
    # Exact scoped and complete bounded ordinary public history.
    for as_of, cutoff in (
        (request.as_of_utc, request.knowledge_cutoff_utc),
        (datetime.max.replace(tzinfo=UTC), datetime.max.replace(tzinfo=UTC)),
    ):
        assert _exact(reader.list_derived_history(
            derived_signal_id=request.derived_signal_id, subject_instrument=SUBJECT,
            effective_at_or_before_utc=as_of, knowledge_at_or_before_utc=cutoff, limit=10,
        )) == _exact(expected)
    for row in expected:
        assert _exact(reader.get_derived_occurrence(row.derived_occurrence_id)) == _exact(row)


def _roles(source, policy, spec, cutoff):
    # All seven actual getter/projection and receipt-history entries; never filter by event.
    maps, actual, visible = _source_evidence(source, policy, spec, _specimen(policy, spec), cutoff)
    assert len(actual) == len(visible) == 7
    roles = {p[1].raw_signal_catalogue_id.value: p for p in visible}
    assert set(roles) == set(maps) == {"R001", "R002", "R003", "R004", "R013", "R023", "R024"}
    return maps, roles


def _authority_refs(brief, digest):
    return (
        f.AuthorityArtifactRefV1("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
                                 "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549"),
        f.AuthorityArtifactRefV1("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
                                 "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c"),
        f.AuthorityArtifactRefV1(POLICY, POLICY_SHA), f.AuthorityArtifactRefV1(brief, digest),
    )


def _d001(tmp_path, policy, spec):
    # Materialise the admitted actual D001, then obtain its ID from a separately
    # constructed ordinary reader. Neither a test DTO nor a callback supplies it.
    assert spec["jurisdiction"] == "D003"
    assert spec["use_actual_public_producer_and_ordinary_SQLite_reader"] is True
    frame = policy["frames"][spec["frame"]]
    clocks = frame["calculation_clocks"]["D001"]
    req = _request("D001", spec["frame"], clocks, PARENT_DEFINITION, PARENT_PROFILE, ())
    now = datetime.fromisoformat(clocks["calculated_at_utc"])
    source = f.create_option_time_source(admission=PARENT_ADMISSION, specimen_id=spec["specimen"])
    maps, roles = _roles(source, policy, spec, req.knowledge_cutoff_utc)
    r2, r3 = roles["R002"], roles["R003"]
    for original, projection in (r2, r3):
        assert original.subject_instrument == SUBJECT
        assert original.native_record["contract"]["id"] == SUBJECT
        assert original.native_record["sample"]["id"] == spec["frame"]
        assert original.source_temporal_kind == projection.source_temporal_kind == "true_instant"
        assert original.received_ts_utc == datetime.fromisoformat(frame["receipt_utc"])
    assert r2[0].native_units == "native_time" and r3[0].native_units == "native_timezone"
    assert r2[0].source_timestamp_raw == r2[1].native_value
    assert r2[0].source_timezone_native == r3[1].native_value
    assert r2[0].native_record["value"]["role"] == "source_timestamp"
    assert r3[0].native_record["value"]["role"] == "source_offset"
    event = datetime.fromisoformat(r2[0].source_timestamp_raw).astimezone(UTC)
    assert event == datetime.fromisoformat(r3[0].source_timestamp_raw)
    assert event == datetime.fromisoformat(frame["event_utc"]) == req.as_of_utc
    assert event < r2[0].received_ts_utc <= req.knowledge_cutoff_utc <= now
    db = tmp_path / "actual-parent-d001.sqlite"
    owner = f.create_option_time_owner(
        admission=PARENT_ADMISSION, source=source, storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: now,
    )
    produced = owner.materialise(req)
    assert type(produced) is f.OptionTimeOccurrenceV1
    assert re.fullmatch(r"mmtoptiontime1:[0-9a-f]{64}", produced.derived_occurrence_id)
    _compare(produced, dict(
        owner_object_id="M02", owner_namespace="neutral_market_measurement_truth/option_time/v1",
        implementation_brief_sha256=PARENT_BRIEF_SHA, derived_signal_id="D001",
        derived_occurrence_id=produced.derived_occurrence_id, request=req,
        definition=f.CalculationDefinitionV1(
            "D001", PARENT_DEFINITION, "K01_TIME",
            "Same actual true instant converted to aware UTC, preserving microseconds.",
            ("R002", "R003"), (), "P_TIME", "UTC_datetime", "aware_utc_datetime",
            _authority_refs(PARENT_BRIEF, PARENT_BRIEF_SHA),
        ),
        source_policy_sha256=POLICY_SHA, source_profile_ref=PARENT_PROFILE,
        projection_mappings=(maps["R002"], maps["R003"]),
        original_observations=(r2[0], r3[0]), selected_projections=(r2[1], r3[1]),
        predecessor_occurrence_ids=(), result=event, units="UTC_datetime",
        result_shape="aware_utc_datetime", effective_as_of_utc=req.as_of_utc,
        knowledge_cutoff_utc=req.knowledge_cutoff_utc, calculated_at_utc=now,
    ), f.OptionTimeOccurrenceV1)
    _history(owner.reads, req, (produced,))
    del owner, source
    reader = f.create_option_time_reader(admission=PARENT_ADMISSION, storage=f.SQLiteReadStorageV1(str(db)))
    row, = reader.list_derived_history(
        derived_signal_id="D001", subject_instrument=SUBJECT,
        effective_at_or_before_utc=req.as_of_utc, knowledge_at_or_before_utc=req.knowledge_cutoff_utc, limit=10,
    )
    assert _exact(row) == _exact(produced)
    _history(reader, req, (row,))
    return row, req, db


def _d003(tmp_path, policy, spec):
    assert spec["recursive_prerequisites_same_source_and_frame"] is True
    d001, req1, db1 = _d001(tmp_path, policy, spec)
    frame = policy["frames"][spec["frame"]]
    clocks = frame["calculation_clocks"]["D003"]
    req = _request("D003", spec["frame"], clocks, LOCAL_DEFINITION, LOCAL_PROFILE,
                   (d001.derived_occurrence_id,))
    now = datetime.fromisoformat(clocks["calculated_at_utc"])
    assert req.as_of_utc == d001.result
    assert d001.knowledge_cutoff_utc <= d001.calculated_at_utc <= req.knowledge_cutoff_utc <= now
    source = f.create_option_time_local_source(admission=LOCAL_ADMISSION, specimen_id=spec["specimen"])
    maps, roles = _roles(source, policy, spec, req.knowledge_cutoff_utc)
    assert _exact(d001.original_observations) == _exact(tuple(roles[r][0] for r in ("R002", "R003")))
    assert _exact(d001.selected_projections) == _exact(tuple(roles[r][1] for r in ("R002", "R003")))
    assert _exact(d001.projection_mappings) == _exact(tuple(maps[r] for r in ("R002", "R003")))
    original, projection = roles["R004"]
    assert original.source_temporal_kind == projection.source_temporal_kind == "receipt_only"
    assert original.source_timestamp_raw is None and original.source_timezone_native is None
    assert original.native_units == projection.native_units == "IANA_timezone"
    assert original.native_record["value"]["role"] == "exchange_iana"
    assert original.native_record["time"]["iana"] == projection.native_value == "America/New_York"
    assert projection.native_field_path == ("time", "iana")
    assert original.native_record["contract"]["id"] == SUBJECT
    assert original.native_record["sample"]["id"] == req.frame_id
    assert original.received_ts_utc <= req.knowledge_cutoff_utc
    assert policy["calendar"]["iana_zone"] == "America/New_York"
    assert policy["calendar"]["ref"] == "t01-option-session-calendar/1"
    local = d001.result.astimezone(ZoneInfo("America/New_York"))
    assert local.astimezone(UTC) == req.as_of_utc
    db = tmp_path / "actual-parent-d003.sqlite"
    assert db != db1 and not db.exists()
    owner = f.create_option_time_local_owner(
        admission=LOCAL_ADMISSION, source=source, parent_storage=f.SQLiteReadStorageV1(str(db1)),
        storage=f.SQLiteStorageV1(str(db), True), utc_now=lambda: now,
    )
    _history(owner.reads, req, ())
    produced = owner.materialise(req)
    assert type(produced) is f.OptionTimeLocalOccurrenceV1
    assert re.fullmatch(r"mmtoptiontimelocal1:[0-9a-f]{64}", produced.derived_occurrence_id)
    _compare(produced, dict(
        owner_object_id="M02", owner_namespace="neutral_market_measurement_truth/option_time_local/v1",
        implementation_brief_sha256=LOCAL_BRIEF_SHA, derived_signal_id="D003",
        derived_occurrence_id=produced.derived_occurrence_id, request=req,
        definition=f.CalculationDefinitionV1(
            "D003", LOCAL_DEFINITION, "K01_TIME",
            "Convert actual D001 UTC to the admitted R004 IANA exchange zone, preserving the same instant.",
            ("R004",), ("D001",), "P_TIME", "IANA_datetime", "aware_iana_datetime",
            _authority_refs(LOCAL_BRIEF, LOCAL_BRIEF_SHA),
        ),
        source_policy_sha256=POLICY_SHA, source_profile_ref=LOCAL_PROFILE,
        projection_mappings=(maps["R004"],), original_observations=(original,), selected_projections=(projection,),
        predecessor_occurrence_ids=(d001.derived_occurrence_id,), predecessor=d001,
        zone_policy_ref=CALENDAR, result=local, units="IANA_datetime", result_shape="aware_iana_datetime",
        effective_as_of_utc=req.as_of_utc, knowledge_cutoff_utc=req.knowledge_cutoff_utc, calculated_at_utc=now,
    ), f.OptionTimeLocalOccurrenceV1)
    _history(owner.reads, req, (produced,))
    del owner, source
    reader = f.create_option_time_local_reader(admission=LOCAL_ADMISSION, storage=f.SQLiteReadStorageV1(str(db)))
    row, = reader.list_derived_history(
        derived_signal_id="D003", subject_instrument=SUBJECT,
        effective_at_or_before_utc=req.as_of_utc, knowledge_at_or_before_utc=req.knowledge_cutoff_utc, limit=10,
    )
    assert _exact(row) == _exact(produced)
    _history(reader, req, (row,))
    return row, req, db, d001, req1, db1


# D085 own proposed fixed interface; preceding helpers retain exact D004/D003/D001
# admissions and independently compare full native and typed parent payloads.
DTE_BRIEF = LEAF + "D085_IMPLEMENTATION_BRIEF.md"
DTE_BRIEF_SHA = "d9d142c25c7d77dfa82c7181ec4ef0d0990216b77139d6a2811cd6a871e0a1a1"
DTE_BINDING = "implementation/authority/T01_D085_OPTION_TIME_AUTHORITY_BINDING.yaml"
DTE_BINDING_SHA = "b28156683fd15f4a685ceac7ff66e0db0782d21319c242a4afd1b8fbb965ee21"
DTE_ADMISSION = f.OwnerAdmissionV1("M02", DTE_BRIEF_SHA)
DTE_PROFILE = f.VersionRefV1("t01-option-time-d085", 1)
DTE_DEFINITION = "T01-D085-OPTION-TIME-DEF-V1"
DTE_NAMESPACE = "neutral_market_measurement_truth/option_time_dte/v1"
DTE_ROLES = ("R013", "R001")
DTE_EQUATION = "Actual expiry date minus actual D004 trading date in whole calendar days after collector receipt and open-session alignment."
DTE_CASE_SHA = {
    "D085-CONTROLLED-SUCCESS": "6b52f16650a9feb2e8d61232a698fdafe01b966908ad4f44c350b7036f445ba6",
    "D085-CONTROLLED-ZERO": "13044c91bef0c74781e6c052b320e85817c9168e3e6d34131fb6fff05649cf28",
    "D085-CONTROLLED-REACHED_REFUSAL": "2bd72781a1c18b65dff2a95b4f6fd2e4a1cf7bcf003da077a2d93076cf3791b7",
    "D085-CONTROLLED-WRONG-PARENT": "ed0c7a541b9a7ab2d95e53cc638996d5e80900ed47b5c66d2565ca2e1f173e1e",
    "D085-CONTROLLED-RECEIPT-MISMATCH": "92ad19232ff81b5aeb0d52e8f028257a8567c94d34916a1c2655fb3109a0920d",
    "D085-CONTROLLED-ORIGINAL-UNITS": "a83677710fa8623520ee9a2c58d31d79f46faabbea660214401ef7060c369831",
    "D085-CONTROLLED-CLOSED-RECEIPT": "cd89cf32ee247a5bce571639503c09e292fe934907641ff939a82b2954261eed",
}


def _interval(policy, instant):
    interval, = [i for i in policy["calendar"]["intervals"]
                 if datetime.fromisoformat(i["start_utc"]) <= instant < datetime.fromisoformat(i["end_utc"])]
    return interval


def _exact_roles(row, mappings, roles, names):
    assert _exact(row.original_observations) == _exact(tuple(roles[r][0] for r in names))
    assert _exact(row.selected_projections) == _exact(tuple(roles[r][1] for r in names))
    assert _exact(row.projection_mappings) == _exact(tuple(mappings[r] for r in names))


def _d004(tmp_path, policy, spec):
    assert spec["jurisdiction"] == "D004"
    assert spec["use_actual_public_producer_and_ordinary_SQLite_reader"] is True
    assert spec["recursive_prerequisites_same_source_and_frame"] is True
    # D003 consumes its own actual D001 with the same literal roster and frame.
    local_spec = dict(spec, jurisdiction="D003")
    local, req3, db3, d001, req1, db1 = _d003(tmp_path, policy, local_spec)
    clocks = policy["frames"][spec["frame"]]["calculation_clocks"]["D004"]
    req = _request("D004", spec["frame"], clocks, DEFINITION, PROFILE,
                   (local.derived_occurrence_id,))
    now = datetime.fromisoformat(clocks["calculated_at_utc"])
    assert req.as_of_utc == d001.result == local.result.astimezone(UTC)
    assert local.knowledge_cutoff_utc <= local.calculated_at_utc <= req.knowledge_cutoff_utc <= now
    source = f.create_option_time_session_source(admission=ADMISSION, specimen_id=spec["specimen"])
    maps, roles = _roles(source, policy, spec, req.knowledge_cutoff_utc)
    _exact_roles(d001, maps, roles, ("R002", "R003"))
    _exact_roles(local, maps, roles, ("R004",))
    assert _exact(local.predecessor) == _exact(d001)
    for role, field, native_role in (
        ("R023", "tradingHours", "trading_schedule"),
        ("R024", "liquidHours", "liquid_schedule"),
    ):
        original, projection = roles[role]
        assert original.source_temporal_kind == projection.source_temporal_kind == "receipt_only"
        assert original.source_timestamp_raw is None and original.source_timezone_native is None
        assert original.native_units == projection.native_units == "schedule"
        assert original.native_record["value"]["role"] == native_role
        assert original.native_record["sample"]["id"] == req.frame_id
        assert original.native_record["calendar"]["policy_ref"] == policy["calendar"]["ref"]
        assert projection.native_field_path == ("calendar", field)
        assert original.native_record["calendar"][field] == projection.native_value == policy["calendar"]["literal_schedule"]
        assert original.received_ts_utc <= req.knowledge_cutoff_utc
    interval = _interval(policy, d001.result)
    assert interval["session_id"] != "closed" and interval["trading_date"] is not None
    expected = date.fromisoformat(interval["trading_date"])
    db = tmp_path / "actual-parent-d004.sqlite"
    assert db not in (db1, db3) and not db.exists()
    owner = f.create_option_time_session_owner(
        admission=ADMISSION, source=source, parent_storage=f.SQLiteReadStorageV1(str(db3)),
        storage=f.SQLiteStorageV1(str(db), True), utc_now=lambda: now,
    )
    _history(owner.reads, req, ())
    produced = owner.materialise(req)
    assert type(produced) is f.OptionTimeSessionOccurrenceV1
    assert re.fullmatch(ID_PATTERN, produced.derived_occurrence_id)
    _compare(produced, dict(
        owner_object_id="M02", owner_namespace=NAMESPACE, implementation_brief_sha256=BRIEF_SHA,
        derived_signal_id=SIGNAL, derived_occurrence_id=produced.derived_occurrence_id, request=req,
        definition=f.CalculationDefinitionV1(
            SIGNAL, DEFINITION, "K01_TIME", EQUATION, ROLES, ("D003",), "P_TIME",
            UNITS, SHAPE, _authority_refs(BRIEF, BRIEF_SHA),
        ),
        source_policy_sha256=POLICY_SHA, source_profile_ref=PROFILE,
        projection_mappings=tuple(maps[r] for r in ROLES),
        original_observations=tuple(roles[r][0] for r in ROLES),
        selected_projections=tuple(roles[r][1] for r in ROLES),
        predecessor_occurrence_ids=(local.derived_occurrence_id,), predecessor=local,
        calendar_policy_ref=CALENDAR, session_id=interval["session_id"], result=expected,
        units=UNITS, result_shape=SHAPE, effective_as_of_utc=req.as_of_utc,
        knowledge_cutoff_utc=req.knowledge_cutoff_utc, calculated_at_utc=now,
    ), f.OptionTimeSessionOccurrenceV1)
    assert type(produced.result) is date
    _history(owner.reads, req, (produced,))
    del owner, source
    reader = f.create_option_time_session_reader(admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)))
    row, = reader.list_derived_history(
        derived_signal_id="D004", subject_instrument=SUBJECT,
        effective_at_or_before_utc=req.as_of_utc, knowledge_at_or_before_utc=req.knowledge_cutoff_utc, limit=10,
    )
    assert _exact(row) == _exact(produced)
    _history(reader, req, (row,))
    return row, req, db, local, req3, db3, d001, req1, db1


@dataclass
class _DteContext:
    case: dict
    policy: dict
    request: object
    clock: list
    owner: object
    db: Path
    parents: tuple
    mappings: dict
    roles: dict


def _prepare(tmp_path, case_id):
    policy = _pinned(POLICY, POLICY_SHA)["source"]
    inventory = _pinned(INVENTORY, INVENTORY_SHA)
    for path, digest in ((DTE_BRIEF, DTE_BRIEF_SHA), (DTE_BINDING, DTE_BINDING_SHA),
                         (BRIEF, BRIEF_SHA), (BINDING, BINDING_SHA),
                         (PARENT_BRIEF, PARENT_BRIEF_SHA), (PARENT_BINDING, PARENT_BINDING_SHA),
                         (LOCAL_BRIEF, LOCAL_BRIEF_SHA), (LOCAL_BINDING, LOCAL_BINDING_SHA)):
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    case, = [c for c in inventory["physical_cases"] if c["case_id"] == case_id]
    assert case["family"] == "D085" and case["proof_id"] == "M02-C28-D085" and case["leaf"] == "L08"
    packed = json.dumps(case, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                        allow_nan=False).encode("ascii")
    assert hashlib.sha256(packed).hexdigest() == DTE_CASE_SHA[case_id]
    spec = case["actual_parent"]
    parent, parent_req, parent_db, local, req3, db3, d001, req1, db1 = _d004(tmp_path, policy, spec)
    clocks = case["request_clock"]
    assert clocks == policy["frames"][case["request_frame"]]["calculation_clocks"]["D085"]
    req = _request("D085", case["request_frame"], clocks, DTE_DEFINITION, DTE_PROFILE,
                   (parent.derived_occurrence_id,))
    assert parent.request.frame_id == local.request.frame_id == d001.request.frame_id == spec["frame"]
    assert _exact(parent.predecessor) == _exact(local) and _exact(local.predecessor) == _exact(d001)
    assert d001.knowledge_cutoff_utc <= d001.calculated_at_utc <= local.knowledge_cutoff_utc
    assert local.knowledge_cutoff_utc <= local.calculated_at_utc <= parent.knowledge_cutoff_utc
    assert parent.knowledge_cutoff_utc <= parent.calculated_at_utc <= req.knowledge_cutoff_utc
    source = f.create_option_time_dte_source(admission=DTE_ADMISSION, specimen_id=case["specimen"])
    maps, roles = _roles(source, policy, case, req.knowledge_cutoff_utc)
    for original, projection in roles.values():
        assert original.subject_instrument == projection.subject_instrument == SUBJECT
        assert original.native_record["sample"]["id"] == req.frame_id
        for key, fields_ in policy["contract_identity"].items():
            for field, value in fields_.items():
                assert _exact(original.native_record[key][field]) == _exact(_native(value))
        assert original.received_ts_utc <= req.knowledge_cutoff_utc
    clock = [datetime.fromisoformat(clocks["calculated_at_utc"])]
    assert req.knowledge_cutoff_utc <= clock[0]
    db = tmp_path / "d085.sqlite"
    assert db not in (parent_db, db3, db1) and not db.exists()
    owner = f.create_option_time_dte_owner(
        admission=DTE_ADMISSION, source=source, parent_storage=f.SQLiteReadStorageV1(str(parent_db)),
        storage=f.SQLiteStorageV1(str(db), True), utc_now=lambda: clock[0],
    )
    _history(owner.reads, req, ())
    parents = ((parent, parent_req, parent_db, f.create_option_time_session_reader, ADMISSION),
               (local, req3, db3, f.create_option_time_local_reader, LOCAL_ADMISSION),
               (d001, req1, db1, f.create_option_time_reader, PARENT_ADMISSION))
    return _DteContext(case, policy, req, clock, owner, db, parents, maps, roles)


def _facts(c):
    # Independent raw/date/receipt/calendar witnesses. Invalid native units and
    # receipt agreement are deliberately recorded as predicates, not prerequisites.
    parent, local, d001 = (p[0] for p in c.parents)
    expiry_original, expiry_projection = c.roles["R013"]
    receipt_original, receipt_projection = c.roles["R001"]
    for original, projection, role, identifier, path in (
        (expiry_original, expiry_projection, "expiry_date", "Contract.lastTradeDateOrContractMonth",
         ("contract", "lastTradeDateOrContractMonth")),
        (receipt_original, receipt_projection, "collector_receipt", "collector.received_ts_utc",
         ("collector", "received_ts_utc")),
    ):
        assert original.source_temporal_kind == projection.source_temporal_kind == "receipt_only"
        assert original.source_timestamp_raw is projection.source_timestamp_raw is None
        assert original.source_timezone_native is projection.source_timezone_native is None
        assert original.native_record["value"]["role"] == role and original.native_identifier == identifier
        assert projection.native_field_path == path
        assert projection.native_value == _path(original.native_record, path)
        assert type(projection.native_value) is str
    text = expiry_projection.native_value
    assert re.fullmatch(r"[0-9]{8}", text)
    expiry = datetime.strptime(text, "%Y%m%d").date()
    assert expiry.strftime("%Y%m%d") == text
    assert expiry.isoformat() == expiry_original.native_record["expiry"]["date"] == c.policy["contract_identity"]["expiry"]["date"]
    assert expiry_projection.native_units == "date_string"
    assert receipt_original.native_units == receipt_projection.native_units == "UTC_datetime_text"
    claimed = datetime.fromisoformat(receipt_projection.native_value)
    assert claimed.tzinfo is UTC
    receipt = receipt_original.received_ts_utc
    assert receipt == c.roles["R002"][0].received_ts_utc == c.roles["R003"][0].received_ts_utc == c.request.as_of_utc
    event = datetime.fromisoformat(c.roles["R002"][0].source_timestamp_raw).astimezone(UTC)
    assert event == datetime.fromisoformat(c.roles["R003"][0].source_timestamp_raw)
    assert event <= receipt <= c.request.knowledge_cutoff_utc
    assert expiry_original.received_ts_utc <= c.request.knowledge_cutoff_utc
    parent_interval = _interval(c.policy, d001.result)
    event_interval = _interval(c.policy, event)
    receipt_interval = _interval(c.policy, receipt)
    assert parent.session_id == parent_interval["session_id"] != "closed"
    assert parent.calendar_policy_ref == CALENDAR
    assert type(parent.result) is date and parent.result == date.fromisoformat(parent_interval["trading_date"])
    assert event_interval["session_id"] != "closed"
    assert d001.result <= receipt <= c.request.knowledge_cutoff_utc
    align = parent.request.frame_id == local.request.frame_id == d001.request.frame_id == c.request.frame_id
    for prior, names in ((d001, ("R002", "R003")), (local, ("R004",)), (parent, ("R023", "R024"))):
        align = align and (
            _exact(prior.original_observations) == _exact(tuple(c.roles[r][0] for r in names))
            and _exact(prior.selected_projections) == _exact(tuple(c.roles[r][1] for r in names))
            and _exact(prior.projection_mappings) == _exact(tuple(c.mappings[r] for r in names))
        )
    for role, field in (("R023", "tradingHours"), ("R024", "liquidHours")):
        original, projection = c.roles[role]
        assert original.native_record["calendar"][field] == projection.native_value == c.policy["calendar"]["literal_schedule"]
    return (expiry, claimed, receipt, event, parent_interval, event_interval, receipt_interval,
            align, expiry_original.native_units, (expiry - parent.result).days)


def _positive(c, row, days, session_id):
    parent = c.parents[0][0]
    assert type(row) is f.OptionTimeDteOccurrenceV1
    assert re.fullmatch(r"mmtoptiontimedte1:[0-9a-f]{64}", row.derived_occurrence_id)
    assert type(days) is int and type(row.result) is int
    _compare(row, dict(
        owner_object_id="M02", owner_namespace=DTE_NAMESPACE, implementation_brief_sha256=DTE_BRIEF_SHA,
        derived_signal_id="D085", derived_occurrence_id=row.derived_occurrence_id, request=c.request,
        definition=f.CalculationDefinitionV1(
            "D085", DTE_DEFINITION, "K01_TIME", DTE_EQUATION, DTE_ROLES, ("D004",), "P_TIME",
            "days", "integer_calendar_days", _authority_refs(DTE_BRIEF, DTE_BRIEF_SHA),
        ),
        source_policy_sha256=POLICY_SHA, source_profile_ref=DTE_PROFILE,
        projection_mappings=tuple(c.mappings[r] for r in DTE_ROLES),
        original_observations=tuple(c.roles[r][0] for r in DTE_ROLES),
        selected_projections=tuple(c.roles[r][1] for r in DTE_ROLES),
        predecessor_occurrence_ids=(parent.derived_occurrence_id,), predecessor=parent,
        calendar_policy_ref=CALENDAR, session_id=session_id, result=days,
        units="days", result_shape="integer_calendar_days", effective_as_of_utc=c.request.as_of_utc,
        knowledge_cutoff_utc=c.request.knowledge_cutoff_utc, calculated_at_utc=c.clock[0],
    ), f.OptionTimeDteOccurrenceV1)
    assert c.case["oracle_only"]["result"] == days and c.case["oracle_only"]["expected_target_rows"] == 1


def _finish(c, expected):
    _history(c.owner.reads, c.request, expected)
    c.owner = None
    reader = f.create_option_time_dte_reader(admission=DTE_ADMISSION, storage=f.SQLiteReadStorageV1(str(c.db)))
    _history(reader, c.request, expected)
    for row, req, db, reader_factory, admission in c.parents:
        parent_reader = reader_factory(admission=admission, storage=f.SQLiteReadStorageV1(str(db)))
        _history(parent_reader, req, (row,))


def _refusal_expected(c, stage):
    assert c.case["expected_stage"] == stage
    assert c.case["oracle_only"]["result"] is None and c.case["oracle_only"]["expected_target_rows"] == 0
    assert c.case["oracle_only"]["replay_at"] is None


def test_d085_success(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-SUCCESS")
    expiry, claimed, receipt, event, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and units == "date_string" and claimed == receipt and event_i == receipt_i == parent
    assert expiry == date(2026, 10, 23) and c.parents[0][0].result == date(2026, 10, 22)
    assert event == datetime.fromisoformat("2026-10-22T19:59:59.125000Z")
    assert receipt == datetime.fromisoformat("2026-10-22T19:59:59.250000Z")
    assert days == 1 and c.case["expected_stage"] == "CALENDAR_DATE_DIFFERENCE"
    row = c.owner.materialise(c.request)
    _positive(c, row, days, parent["session_id"])
    _history(c.owner.reads, c.request, (row,))
    c.clock[0] = datetime.fromisoformat("2026-10-22T20:00:05Z")
    assert c.clock[0] == datetime.fromisoformat(c.case["oracle_only"]["replay_at"])
    assert _exact(c.owner.materialise(c.request)) == _exact(row)
    _finish(c, (row,))


def test_d085_zero(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-ZERO")
    expiry, claimed, receipt, _, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and units == "date_string" and claimed == receipt and event_i == receipt_i == parent
    assert expiry == c.parents[0][0].result == date(2026, 10, 23)
    assert days == 0 and c.case["expected_stage"] == "ZERO_CALENDAR_DAY_BOUNDARY"
    assert c.case["oracle_only"]["replay_at"] is None
    row = c.owner.materialise(c.request)
    _positive(c, row, days, parent["session_id"])
    _finish(c, (row,))


def test_d085_expired(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-REACHED_REFUSAL")
    expiry, claimed, receipt, _, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and units == "date_string" and claimed == receipt and event_i == receipt_i == parent
    assert expiry == date(2026, 10, 23) and c.parents[0][0].result == date(2026, 10, 26)
    assert days == -3
    _refusal_expected(c, "NEGATIVE_LIVE_DTE")
    assert c.owner.materialise(c.request) is None
    _finish(c, ())


def test_d085_wrong_parent(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-WRONG-PARENT")
    expiry, claimed, receipt, _, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert c.request.frame_id == "MAIN" and c.parents[0][0].request.frame_id == "EARLIER"
    assert not aligned and units == "date_string" and claimed == receipt and event_i == receipt_i != parent
    assert days == 2 and (expiry - date.fromisoformat(event_i["trading_date"])).days == 1
    assert c.request.predecessor_occurrence_ids == (c.parents[0][0].derived_occurrence_id,)
    _refusal_expected(c, "ACTUAL_D004_FRAME_ALIGNMENT")
    assert c.owner.materialise(c.request) is None
    _finish(c, ())


def test_d085_receipt_mismatch(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-RECEIPT-MISMATCH")
    _, claimed, receipt, event, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and units == "date_string" and event_i == receipt_i == parent and days == 1
    assert claimed == event == datetime.fromisoformat("2026-10-22T19:59:59.125000Z")
    assert receipt == datetime.fromisoformat("2026-10-22T19:59:59.250000Z") != claimed
    assert _interval(c.policy, claimed) == receipt_i
    _refusal_expected(c, "ACTUAL_COLLECTOR_RECEIPT_AGREEMENT")
    assert c.owner.materialise(c.request) is None
    _finish(c, ())


def test_d085_original_units(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-ORIGINAL-UNITS")
    _, claimed, receipt, _, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and claimed == receipt and event_i == receipt_i == parent and days == 1
    assert units == "UTC_datetime_text" and c.roles["R013"][1].native_units == "date_string"
    _refusal_expected(c, "ACTUAL_R013_NATIVE_UNITS")
    assert c.owner.materialise(c.request) is None
    _finish(c, ())


def test_d085_closed_receipt(tmp_path):
    c = _prepare(tmp_path, "D085-CONTROLLED-CLOSED-RECEIPT")
    _, claimed, receipt, event, parent, event_i, receipt_i, aligned, units, days = _facts(c)
    assert aligned and units == "date_string" and claimed == receipt and event_i == parent and days == 1
    assert event == datetime.fromisoformat("2026-10-22T19:59:59.875000Z")
    assert receipt == datetime.fromisoformat("2026-10-22T20:00:00.125000Z")
    assert event < datetime.fromisoformat(parent["end_utc"]) <= receipt
    assert receipt_i["session_id"] == "closed" and receipt_i["trading_date"] is None
    _refusal_expected(c, "ACTUAL_RECEIPT_SESSION_ALIGNMENT")
    assert c.owner.materialise(c.request) is None
    _finish(c, ())
