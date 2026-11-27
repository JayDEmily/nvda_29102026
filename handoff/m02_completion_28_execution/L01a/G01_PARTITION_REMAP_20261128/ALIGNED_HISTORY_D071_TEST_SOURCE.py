"""Exact controlled aligned-history authoring candidate for D071.

INERT: do not import, collect or execute in the Worker.
Prospective physical path:
tests/product/m02_completion_28_prospective/support/d071-history/test_profile.py.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[5]
LEAF = "handoff/m02_completion_28_execution/L01a/"
POLICY = LEAF + "ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json"
MANIFEST = LEAF + "ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json"
BRIEF = LEAF + "ALIGNED_HISTORY_D071_IMPLEMENTATION_BRIEF.md"
POLICY_SHA = "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1"
MANIFEST_SHA = "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d"
BRIEF_SHA = "65f2d0f9135f291773ab6081ec76892a967315df3ecb9c1760a4e2687a296e5e"
SIGNAL, SUBJECT = "D071", "SPY"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF_SHA)
PROVIDER = "foundation-controlled-aligned-history"
VARIANT = "prior_close_history_v1"
SCOPE = PROVIDER + "/" + VARIANT
ROLES = ("R037", "R042")
PROFILE = f.VersionRefV1("t01-l01a-d071-history", 1)
PARAM = f.CalculationParameterSetV1(
    "t01-l01a-d071-parameters", 1, "P_WINDOW", SUBJECT, (SUBJECT,),
)
SELECTION = f.InputSelectionPolicyVersionV1(
    "t01-l01a-d071-selection", 1,
    ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
    timedelta(seconds=86400), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, SCOPE, 100, 2,
)
UNIT = f.UnitConventionVersionV1(
    "t01-l01a-underlying-price", 1, "USD_per_share", "USD_per_share",
    Decimal("1"), Decimal("0"),
)
META = (
    ("instrument.id", ("instrument", "id")),
    ("session.id", ("session", "id")),
    ("adjustment.basis", ("adjustment", "basis")),
    ("price.kind", ("price", "kind")),
)
MAPS = {
    rid: raw.RawSignalProjectionMappingV1(
        "t01-l01a-" + rid.lower() + "-history", 1, raw.RawSignalCatalogueId(rid),
        PROVIDER, VARIANT, path, "USD_per_share", META,
    )
    for rid, path in (("R037", ("trade", "last")), ("R042", ("official_close", "value")))
}


def _pinned(path, digest):
    data = (ROOT / path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    return json.loads(data)


def _sha(value):
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def _expand(manifest, name, digest):
    spec, = [v for v in manifest["specimens"] if v["specimen_id"] == name]
    members = copy.deepcopy(manifest["base_members"])
    for change in spec["operations"]:
        if change["op"] == "append":
            members.append(copy.deepcopy(change["member"]))
        else:
            assert change["op"] == "replace"
            i, = [
                i for i, row in enumerate(members)
                if row["observation"]["observation_occurrence_id"] == change["old_id"]
            ]
            members[i] = copy.deepcopy(change["member"])
    members.sort(key=lambda row: (
        datetime.fromisoformat(row["observation"]["received_ts_utc"]),
        row["observation"]["ingestion_sequence"],
        row["observation"]["observation_occurrence_id"],
    ))
    assert len(members) == spec["expanded_count"]
    assert _sha(members) == spec["expanded_sha256"] == digest
    for frame in manifest["frames"]:
        slot = frame["slot"]
        assert _sha([row for row in members if row["slot"] == slot]) == (
            spec["frame_roster_sha256"][slot]
        )
    return members


def _native(value):
    if isinstance(value, dict):
        if set(value) == {"decimal"}:
            assert type(value["decimal"]) is str
            return Decimal(value["decimal"])
        return {key: _native(item) for key, item in value.items()}
    return value


def _exact(value):
    if isinstance(value, Mapping):
        return ("mapping", tuple(sorted((key, _exact(v)) for key, v in value.items())))
    if type(value) in (tuple, list):
        return (type(value), tuple(_exact(v) for v in value))
    if type(value) is Decimal:
        return (Decimal, value.as_tuple())
    if is_dataclass(value) and not isinstance(value, type):
        return (
            type(value),
            tuple((field.name, _exact(getattr(value, field.name))) for field in fields(value)),
        )
    return (type(value), value)


def _path(value, path):
    for key in path:
        value = value[key]
    return value


def _compare_fields(actual, expected, cls):
    assert type(actual) is cls
    assert {field.name for field in fields(cls)} == set(expected)
    for field in fields(cls):
        assert _exact(getattr(actual, field.name)) == _exact(expected[field.name]), field.name


def _assert_original(actual, literal):
    expected = dict(literal)
    expected.update(
        concept_id=raw.concept_id(literal["concept_id"]),
        contract_id=raw.contract_id(literal["contract_id"]),
        observation_occurrence_id=raw.observation_occurrence_id(
            literal["observation_occurrence_id"]
        ),
        delivery_artifact_ref=raw.delivery_artifact_ref(literal["delivery_artifact_ref"]),
        source_provider=raw.provider_id(literal["source_provider"]),
        native_record=_native(literal["native_record"]),
        received_ts_utc=datetime.fromisoformat(literal["received_ts_utc"]),
        ingestion_sequence_scope=raw.ingestion_sequence_scope(literal["ingestion_sequence_scope"]),
        raw_signal_catalogue_ids=tuple(
            raw.RawSignalCatalogueId(rid) for rid in literal["raw_signal_catalogue_ids"]
        ),
    )
    _compare_fields(actual, expected, raw.RawObservationOccurrenceV1)


def _assert_projection(actual, literal, rid):
    mapping = MAPS[rid]
    native = _native(literal["native_record"])
    expected = dict(
        raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
        observation_occurrence_id=raw.observation_occurrence_id(
            literal["observation_occurrence_id"]
        ),
        projection_mapping_id=mapping.mapping_id,
        projection_mapping_version=mapping.version,
        source_provider=literal["source_provider"],
        source_variant=literal["source_variant"],
        native_field_path=mapping.native_field_path,
        native_value=_path(native, mapping.native_field_path),
        native_units=mapping.native_units,
        subject_instrument=literal["subject_instrument"],
        source_temporal_kind=literal["source_temporal_kind"],
        source_timestamp_raw=literal["source_timestamp_raw"],
        source_timezone_native=literal["source_timezone_native"],
        received_ts_utc=datetime.fromisoformat(literal["received_ts_utc"]),
        ingestion_sequence=literal["ingestion_sequence"],
        ingestion_sequence_scope=raw.ingestion_sequence_scope(literal["ingestion_sequence_scope"]),
        revision_vintage_native=literal["revision_vintage_native"],
        selection_identity=raw.RawSelectionIdentityV1(tuple(
            (key, _path(native, path)) for key, path in META
        )),
    )
    _compare_fields(actual, expected, raw.ProjectedRawValueV1)


def _source_evidence(source, members, name, digest):
    assert type(source) is f.AlignedHistorySourceV1
    assert source.specimen_id == name
    assert source.expanded_sha256 == digest
    assert source.expanded_count == len(members)
    assert not hasattr(source, "commands")
    assert not hasattr(source, "admit_raw_observation_occurrence")
    actual = {}
    for member in members:
        literal, rid = member["observation"], member["role"]
        key = literal["observation_occurrence_id"]
        assert key not in actual
        oid = raw.observation_occurrence_id(key)
        original = source.get_raw_observation_occurrence(oid)
        projected = source.project_raw_value(
            raw.RawSignalCatalogueId(rid), oid, mappings=(MAPS[rid],),
        )
        _assert_original(original, literal)
        _assert_projection(projected, literal, rid)
        actual[key] = (original, projected)
    return actual


def _visible(source, members, actual, rid, event, cutoff):
    page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId(rid), mappings=(MAPS[rid],), subject_instrument=SUBJECT,
        received_at_or_before_utc=cutoff, event_at_or_before_utc=event, limit=100, cursor=None,
    )
    assert type(page) is raw.ProjectedRawHistoryPageV1
    assert page.next_cursor is None
    expected = tuple(
        actual[m["observation"]["observation_occurrence_id"]][1]
        for m in members if m["role"] == rid and m["subject"] == SUBJECT
        and datetime.fromisoformat(m["observation"]["received_ts_utc"]) <= cutoff
        and datetime.fromisoformat(m["observation"]["source_timestamp_raw"]) <= event
    )
    assert _exact(page.items) == _exact(expected)
    return page.items


def _pairs(members, actual, frame, role):
    return tuple(
        actual[m["observation"]["observation_occurrence_id"]]
        for m in members
        if (m["slot"], m["subject"], m["role"]) == (frame["slot"], SUBJECT, role)
    )


def _role(pair, frame, role, *, anchor=None, kind=None, units="USD_per_share", cutoff=None):
    original, projection = pair
    event = datetime.fromisoformat(original.source_timestamp_raw)
    expect_anchor = frame["as_of" if role == "R037" else "reference"]
    expect_kind = "current_last" if role == "R037" else "official_close"
    session = frame["session_current" if role == "R037" else "session_reference"]
    assert event == (anchor or datetime.fromisoformat(expect_anchor))
    assert event <= original.received_ts_utc <= (
        cutoff or datetime.fromisoformat(frame["row_cutoff"])
    )
    assert original.raw_signal_catalogue_ids == (raw.RawSignalCatalogueId(role),)
    assert original.source_provider == raw.provider_id(PROVIDER)
    assert original.source_variant == VARIANT and original.subject_instrument == SUBJECT
    assert original.source_temporal_kind == "true_instant"
    assert original.source_timezone_native == "UTC"
    assert original.native_units == units
    assert original.native_record["instrument"]["id"] == SUBJECT
    assert original.native_record["session"]["id"] == session
    assert original.native_record["adjustment"]["basis"] == "controlled_unadjusted/1"
    assert original.native_record["price"]["kind"] == (kind or expect_kind)
    assert projection.native_units == "USD_per_share"
    assert type(projection.native_value) is Decimal
    assert projection.native_value > 0 and projection.native_value.as_tuple().exponent == 0


def _context(frame):
    c = frame["context"]
    return f.WindowContextV1(
        f.VersionRefV1(c["id"], c["version"]),
        datetime.fromisoformat(c["start"]), datetime.fromisoformat(c["end"]),
        datetime.fromisoformat(c["history_complete_from"]),
    )


def _request(frame):
    return f.AlignedHistoryRequestV1(
        derived_signal_id=SIGNAL, subject_instrument=SUBJECT, slot=frame["slot"],
        as_of_utc=datetime.fromisoformat(frame["as_of"]),
        knowledge_cutoff_utc=datetime.fromisoformat(frame["row_cutoff"]),
        calculation_definition_version="T01-D071-ALIGNED-HISTORY-DEF-V1",
        source_profile_ref=PROFILE, parameter_set_ref=f.VersionRefV1(PARAM.context_id, 1),
        input_selection_policy_ref=f.VersionRefV1(SELECTION.context_id, 1),
        context_refs=(_context(frame).ref,), predecessor_occurrence_ids=(),
    )


def _definition(policy):
    refs = tuple(f.AuthorityArtifactRefV1(x["path"], x["sha256"])
                 for x in policy["authority_refs"])
    return f.CalculationDefinitionV1(
        SIGNAL, "T01-D071-ALIGNED-HISTORY-DEF-V1", "K03_CHANGE_RETURN",
        "ln(current/reference)", ROLES, (), "P_WINDOW", "return", "scalar_decimal",
        (*refs, f.AuthorityArtifactRefV1(POLICY, POLICY_SHA),
         f.AuthorityArtifactRefV1(BRIEF, BRIEF_SHA)),
    )


def _assert_result(row, request, frame, pairs, manifest, policy, now):
    oracle = manifest["oracle_only_not_inputs"]
    expected = oracle["complete_legal_row_oracles"]["A"][frame["slot"]]
    n, d = expected["normalized_values_D071_through_D077"][0]
    assert d == 1 and n in (-1, 0, 1)
    text = {
        -1: oracle["negative_log_50_digit_half_even"],
        0: "0",
        1: oracle["positive_log_50_digit_half_even"],
    }[n]
    result = Decimal(text)
    assert Fraction(result) == Fraction(
        *expected["exact_fraction_values_D071_through_D077"][0]
    )
    assert type(row) is f.AlignedHistoryOccurrenceV1
    assert re.fullmatch(r"mmtahistory1:[0-9a-f]{64}", row.derived_occurrence_id)
    expected_fields = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/aligned_history/v1",
        implementation_brief_sha256=BRIEF_SHA, derived_signal_id=SIGNAL,
        derived_occurrence_id=row.derived_occurrence_id, request=request,
        definition=_definition(policy), source_policy_sha256=POLICY_SHA,
        source_profile_ref=PROFILE, parameter_set=PARAM, input_selection_policy=SELECTION,
        window_context=_context(frame), projection_mappings=tuple(MAPS[rid] for rid in ROLES),
        unit_conventions=(UNIT,), original_observations=tuple(pair[0] for pair in pairs),
        selected_projections=tuple(pair[1] for pair in pairs), predecessors=(),
        result=result, units="return", result_shape="scalar_decimal",
        window_seconds=frame["window_seconds"], effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc, calculated_at_utc=now,
    )
    _compare_fields(row, expected_fields, f.AlignedHistoryOccurrenceV1)


def _history(reader, frames, results):
    assert len({row.derived_occurrence_id for row in results.values()}) == len(results)
    for row in results.values():
        assert _exact(reader.get_derived_occurrence(row.derived_occurrence_id)) == _exact(row)
    # Independent effective and knowledge query bounds; S7 must not leak into S6.
    for effective, knowledge in ((7, 7), (6, 7), (7, 6), (3, 3)):
        actual = reader.list_derived_history(
            derived_signal_id=SIGNAL, subject_instrument=SUBJECT,
            effective_at_or_before_utc=datetime.fromisoformat(frames[effective]["as_of"]),
            knowledge_at_or_before_utc=datetime.fromisoformat(frames[knowledge]["row_cutoff"]),
            limit=10,
        )
        expected = tuple(
            results[frame["slot"]] for frame in reversed(frames[:min(effective, knowledge) + 1])
            if frame["slot"] in results
        )
        assert _exact(actual) == _exact(expected)


def test_d071_history_success(tmp_path):
    manifest = _pinned(MANIFEST, MANIFEST_SHA)
    policy = _pinned(POLICY, POLICY_SHA)
    assert hashlib.sha256((ROOT / BRIEF).read_bytes()).hexdigest() == BRIEF_SHA
    frames = manifest["frames"]
    assert [frame["slot"] for frame in frames] == [
        "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
    ]
    members = _expand(manifest, "A",
                      "ca87adff2e2aa7a509c2f1d584eda019665fd7f38b3966b8be901fbddbcb22d1")
    source = f.create_aligned_history_source(admission=ADMISSION, specimen_id="A")
    actual = _source_evidence(source, members, "A",
                              "ca87adff2e2aa7a509c2f1d584eda019665fd7f38b3966b8be901fbddbcb22d1")
    db = tmp_path / "d071-history.sqlite"
    clock = [datetime.fromisoformat(frames[0]["default_underlying_calculated_at"])]
    owner = f.create_aligned_history_owner(
        admission=ADMISSION, source=source, predecessor_read_storages=(),
        storage=f.SQLiteStorageV1(str(db), True), utc_now=lambda: clock[0],
    )
    results = {}
    for frame in frames:
        slot = frame["slot"]
        t = datetime.fromisoformat(frame["as_of"])
        cutoff = datetime.fromisoformat(frame["row_cutoff"])
        clock[0] = datetime.fromisoformat(frame["default_underlying_calculated_at"])
        request = _request(frame)
        currents = _pairs(members, actual, frame, "R037")
        references = _pairs(members, actual, frame, "R042")
        visible_current = _visible(source, members, actual, "R037", t, cutoff)
        visible_reference = _visible(source, members, actual, "R042", t, cutoff)

        current, = currents
        reference, = references
        _role(current, frame, "R037")
        _role(reference, frame, "R042")
        assert _exact(current[1]) in tuple(_exact(p) for p in visible_current)
        assert _exact(reference[1]) in tuple(_exact(p) for p in visible_reference)
        row = owner.materialise(request)
        _assert_result(
            row, request, frame, (current, reference), manifest, policy, clock[0],
        )
        results[slot] = row
    assert len(results) == 8
    clock[0] = datetime.fromisoformat("2026-10-20T12:40:06Z")
    assert _exact(owner.materialise(_request(frames[7]))) == _exact(results["S7"])
    _history(owner.reads, frames, results)
    del owner, source
    reader = f.create_aligned_history_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)),
    )
    _history(reader, frames, results)


def test_d071_missing_exact_reference(tmp_path):
    manifest = _pinned(MANIFEST, MANIFEST_SHA)
    policy = _pinned(POLICY, POLICY_SHA)
    assert hashlib.sha256((ROOT / BRIEF).read_bytes()).hexdigest() == BRIEF_SHA
    frames = manifest["frames"]
    assert [frame["slot"] for frame in frames] == [
        "S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
    ]
    members = _expand(manifest, "SPY_OFF_ANCHOR",
                      "dc062c52f5a0a6b08240411eb0290cc68d46f35b29c49cd0c6c8370af632c515")
    source = f.create_aligned_history_source(admission=ADMISSION, specimen_id="SPY_OFF_ANCHOR")
    actual = _source_evidence(source, members, "SPY_OFF_ANCHOR",
                              "dc062c52f5a0a6b08240411eb0290cc68d46f35b29c49cd0c6c8370af632c515")
    db = tmp_path / "d071-history.sqlite"
    clock = [datetime.fromisoformat(frames[0]["default_underlying_calculated_at"])]
    owner = f.create_aligned_history_owner(
        admission=ADMISSION, source=source, predecessor_read_storages=(),
        storage=f.SQLiteStorageV1(str(db), True), utc_now=lambda: clock[0],
    )
    results = {}
    for frame in frames:
        slot = frame["slot"]
        t = datetime.fromisoformat(frame["as_of"])
        cutoff = datetime.fromisoformat(frame["row_cutoff"])
        clock[0] = datetime.fromisoformat(frame["default_underlying_calculated_at"])
        request = _request(frame)
        currents = _pairs(members, actual, frame, "R037")
        references = _pairs(members, actual, frame, "R042")
        visible_current = _visible(source, members, actual, "R037", t, cutoff)
        visible_reference = _visible(source, members, actual, "R042", t, cutoff)
        if slot == "S3":
            current, = currents
            reference, = references
            _role(current, frame, "R037")
            anchor = datetime.fromisoformat(frame["reference"])
            _role(reference, frame, "R042", anchor=anchor - timedelta(minutes=1))
            assert _exact(current[1]) in tuple(_exact(p) for p in visible_current)
            assert _exact(reference[1]) in tuple(_exact(p) for p in visible_reference)
            assert not any(
                datetime.fromisoformat(p.source_timestamp_raw) == anchor
                for p in visible_reference
            )
            assert owner.materialise(request) is None
            continue
        current, = currents
        reference, = references
        _role(current, frame, "R037")
        _role(reference, frame, "R042")
        assert _exact(current[1]) in tuple(_exact(p) for p in visible_current)
        assert _exact(reference[1]) in tuple(_exact(p) for p in visible_reference)
        row = owner.materialise(request)
        _assert_result(
            row, request, frame, (current, reference), manifest, policy, clock[0],
        )
        results[slot] = row
    assert set(results) == {"S0", "S1", "S2", "S4", "S5", "S6", "S7"}
    _history(owner.reads, frames, results)
    del owner, source
    reader = f.create_aligned_history_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)),
    )
    _history(reader, frames, results)
