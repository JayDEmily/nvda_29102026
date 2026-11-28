"""INERT D095 prior-session IV proof authoring candidate; never import or collect as Worker.
Prospective physical path: tests/product/m02_completion_28_prospective/d095/test_signal.py.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from fractions import Fraction
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

ROOT = Path(__file__).resolve().parents[4]
LEAF = "handoff/m02_completion_28_execution/L10a/"
POLICY = LEAF + "OPTION_IV_PRIOR_SESSION_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json"
INVENTORY = LEAF + "OPTION_IV_PRIOR_SESSION_FINITE_CASES_PROPOSED_20261127.json"
BRIEF = LEAF + "D095_IMPLEMENTATION_BRIEF.md"
BINDING = "implementation/authority/T01_D095_PRIOR_SESSION_IV_AUTHORITY_BINDING.yaml"
POLICY_SHA = "050d167a6f15ae210f3a0b7a776957e6ebb00ce8f674ad9d417e7082951b6a39"
INVENTORY_SHA = "7a3b85138291ee50396157850502854f79b8c5c6b2b20d9f0e4c56933b4fca74"
BRIEF_SHA = "4885ee1efe9f5832f33a8bf0552caf288990f9f992542c26f535bf378bcbc703"
BINDING_SHA = "2a4530490537b2552b320db240ac09eb24508ccc9d9347316e517463c4548f32"
SIGNAL = "D095"
SUBJECT = "controlled-nvda-c110-20261023"
PROFILE = f.VersionRefV1("t01-option-iv-prior-session-d095", 1)
CALENDAR = f.VersionRefV1("t01-option-iv-session-calendar", 1)
DEFINITION = "T01-D095-OPTION-IV-PRIOR-SESSION-DEF-V1"
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF_SHA)
UNITS = "annualised_iv_decimal"


def _definition():
    return f.CalculationDefinitionV1(
        'D095', DEFINITION, 'K03_CHANGE_RETURN', '100*(current IV - unique highest eligible final prior trading-session IV).',
        ('R111', 'R183'), (), 'P_WINDOW', 'volatility_points', 'exact_ratio',
        (
            f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv', '67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549'),
            f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md', '603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c'),
            f.AuthorityArtifactRefV1('handoff/m02_completion_28_execution/L10a/OPTION_IV_PRIOR_SESSION_SOURCE_POLICY_AND_SPECIMENS_PROPOSED_20261127.json', '050d167a6f15ae210f3a0b7a776957e6ebb00ce8f674ad9d417e7082951b6a39'),
            f.AuthorityArtifactRefV1('handoff/m02_completion_28_execution/L10a/D095_IMPLEMENTATION_BRIEF.md', '4885ee1efe9f5832f33a8bf0552caf288990f9f992542c26f535bf378bcbc703'),
        ),
    )


def _prepare(tmp_path, case_id):
    policy, case, members = _case(case_id)
    assert case["actual_parent"] is None
    source = f.create_option_iv_prior_session_source(admission=ADMISSION, specimen_id=case["specimen"])
    assert type(source) is f.OptionIVPriorSessionSourceV1
    maps, actual, visible = _source_evidence(source, policy, case, members)
    assert [o.observation_occurrence_id.value for o, p in visible] == case["actual_visible_original_ids"]
    current, = [pair for pair in visible if pair[1].raw_signal_catalogue_id.value == "R111"]
    refs = tuple(pair for pair in visible if pair[1].raw_signal_catalogue_id.value == "R183")
    o, p = current
    assert o.observation_occurrence_id.value == "T01-OIV-CURRENT"
    assert o.source_temporal_kind == p.source_temporal_kind == "receipt_only"
    assert o.source_timestamp_raw is None and p.source_timestamp_raw is None
    assert o.native_record["contract"]["id"] == SUBJECT
    assert o.native_record["instrument"]["kind"] == "option"
    assert o.native_record["model"]["convention"] == "controlled-model/1"
    assert o.native_units == p.native_units == UNITS
    assert type(p.native_value) is Decimal and p.native_value.as_tuple() == Decimal("0.3575").as_tuple()
    clocks = case["request_clock"]
    request = f.OptionIVPriorSessionRequestV1(
        derived_signal_id=SIGNAL, subject_instrument=SUBJECT,
        as_of_utc=datetime.fromisoformat(clocks["as_of_utc"]),
        knowledge_cutoff_utc=datetime.fromisoformat(clocks["knowledge_cutoff_utc"]),
        calculation_definition_version=DEFINITION, source_profile_ref=PROFILE,
        calendar_ref=CALENDAR, predecessor_occurrence_ids=(),
    )
    assert o.received_ts_utc == request.as_of_utc <= request.knowledge_cutoff_utc
    model = o.native_record["model"]
    assert datetime.fromisoformat(model["quote_receipt_utc"]) < o.received_ts_utc
    assert datetime.fromisoformat(model["underlying_receipt_utc"]) < o.received_ts_utc
    intervals = [v for v in policy["calendar"]["intervals"] if v["trading_date"] is not None]
    now_session, = [v for v in intervals if datetime.fromisoformat(v["start_utc"]) <=
                    request.as_of_utc < datetime.fromisoformat(v["end_utc"])]
    prior = max((v for v in intervals if v["trading_date"] < now_session["trading_date"]),
                key=lambda v: v["trading_date"])
    assert now_session["trading_date"] == "2026-10-19"
    assert prior["trading_date"] == "2026-10-16"  # not Sunday calendar-yesterday
    assert prior["end_utc"] == "2026-10-16T20:00:00Z"
    for orig, proj in refs:
        bar = orig.native_record["bar"]
        assert orig.source_temporal_kind == proj.source_temporal_kind == "date_only"
        assert orig.source_timestamp_raw == bar["date"]
        assert bar["bar_size"] == "1 day" and bar["what_to_show"] == "OPTION_IMPLIED_VOLATILITY"
        assert bar["session_calendar_ref"] == "t01-option-iv-session-calendar/1" and bar["final"] is True
        assert type(bar["revision"]) is int and bar["revision"] > 0
        assert orig.revision_vintage_native == f"controlled-final/{bar['revision']}"
        assert type(proj.native_value) is Decimal and proj.native_value >= 0
    clock = [datetime.fromisoformat(clocks["calculated_at_utc"])]
    db = tmp_path / "d095.sqlite"
    owner = f.create_option_iv_prior_session_owner(
        admission=ADMISSION, source=source, storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    return source, owner, db, request, clock, case, maps, actual, visible, current, refs


def _empty_reopen(request, db):
    reader = f.create_option_iv_prior_session_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)),
    )
    _assert_history(reader, request, ())


def _late(actual, visible, request):
    late, projection = actual["T01-OIV-FRI-V3-LATE"]
    assert late.native_record["bar"]["date"] == "2026-10-16"
    assert late.native_record["bar"]["revision"] == 3
    assert late.received_ts_utc > request.knowledge_cutoff_utc
    assert projection.observation_occurrence_id == late.observation_occurrence_id
    assert all(o.observation_occurrence_id != late.observation_occurrence_id for o, p in visible)


def test_d095_success(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-SUCCESS",
    )
    _late(actual, visible, request)
    assert [o.native_record["bar"]["date"] for o, p in refs] == ["2026-10-15", "2026-10-16", "2026-10-16"]
    friday = [pair for pair in refs if pair[0].native_record["bar"]["date"] == "2026-10-16"]
    assert [o.native_record["bar"]["revision"] for o, p in friday] == [1, 2]
    for o, p in friday:
        assert o.native_record["contract"]["id"] == SUBJECT
        assert o.native_record["model"]["convention"] == current[0].native_record["model"]["convention"]
        assert o.native_units == p.native_units == UNITS
        assert datetime.fromisoformat("2026-10-16T20:00:00Z") <= o.received_ts_utc <= request.knowledge_cutoff_utc
    reference = friday[1]
    assert reference[0].observation_occurrence_id.value == "T01-OIV-FRI-V2"
    ratio = 100 * (Fraction(current[1].native_value) - Fraction(reference[1].native_value))
    assert ratio == Fraction(9, 2) == Fraction(*case["oracle_only"]["result_ratio"])
    row = owner.materialise(request)
    assert type(row) is f.OptionIVPriorSessionOccurrenceV1
    assert re.fullmatch(r"mmtoptionivprior1:[0-9a-f]{64}", row.derived_occurrence_id)
    _compare(row, dict(
        owner_object_id="M02", owner_namespace="neutral_market_measurement_truth/option_iv_prior_session/v1",
        implementation_brief_sha256=BRIEF_SHA, derived_signal_id=SIGNAL,
        derived_occurrence_id=row.derived_occurrence_id, request=request,
        definition=_definition(), source_policy_sha256=POLICY_SHA,
        source_profile_ref=PROFILE, calendar_ref=CALENDAR,
        projection_mappings=(maps["R111"], maps["R183"]),
        visible_originals=tuple(o for o, p in visible), visible_projections=tuple(p for o, p in visible),
        selected_current_id=current[0].observation_occurrence_id,
        selected_reference_id=reference[0].observation_occurrence_id,
        prior_trading_date=date(2026, 10, 16),
        configured_reference_close_utc=datetime.fromisoformat("2026-10-16T20:00:00Z"),
        predecessor_occurrence_ids=(), result=f.ExactRatioV1(9, 2),
        units="volatility_points", result_shape="exact_ratio",
        effective_as_of_utc=request.as_of_utc, knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        calculated_at_utc=clock[0],
    ), f.OptionIVPriorSessionOccurrenceV1)
    clock[0] = datetime.fromisoformat(case["oracle_only"]["replay_at"])
    assert _exact(owner.materialise(request)) == _exact(row)
    _assert_history(owner.reads, request, (row,))
    del owner, source
    reader = f.create_option_iv_prior_session_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(str(db)),
    )
    _assert_history(reader, request, (row,))


def test_d095_wrong_session(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-REACHED_REFUSAL",
    )
    assert case["expected_stage"] == "EXACT_PRIOR_SESSION_REFERENCE"
    ref, = refs
    assert ref[0].source_timestamp_raw == "2026-10-15"
    assert ref[0].native_record["contract"]["id"] == SUBJECT
    assert ref[0].native_record["model"]["convention"] == "controlled-model/1"
    assert ref[0].native_units == UNITS
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d095_late_reference(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-LATE-REFERENCE",
    )
    assert case["expected_stage"] == "ACTUAL_REFERENCE_KNOWLEDGE_CUTOFF"
    _late(actual, visible, request)
    assert refs == ()
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d095_wrong_contract(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-WRONG-CONTRACT",
    )
    assert case["expected_stage"] == "ACTUAL_NATIVE_CONTRACT_COMPATIBILITY"
    ref, = refs
    assert ref[0].source_timestamp_raw == "2026-10-16"
    assert ref[0].subject_instrument == SUBJECT and ref[0].native_record["contract"]["id"] == "NVDA"
    assert ref[0].native_record["model"]["convention"] == "controlled-model/1"
    assert ref[0].native_units == UNITS
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d095_wrong_model(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-WRONG-MODEL",
    )
    assert case["expected_stage"] == "ACTUAL_MODEL_CONVENTION_COMPATIBILITY"
    ref, = refs
    assert ref[0].source_timestamp_raw == "2026-10-16" and ref[0].native_record["contract"]["id"] == SUBJECT
    assert ref[0].native_record["model"]["convention"] == "controlled-different-model/1"
    assert ref[0].native_units == UNITS
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d095_wrong_units(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-WRONG-UNITS",
    )
    assert case["expected_stage"] == "ACTUAL_NATIVE_IV_UNITS"
    ref, = refs
    assert ref[0].source_timestamp_raw == "2026-10-16" and ref[0].native_record["contract"]["id"] == SUBJECT
    assert ref[0].native_record["model"]["convention"] == "controlled-model/1"
    assert ref[0].native_units == "volatility_points" and ref[1].native_units == UNITS
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)


def test_d095_duplicate_vintage(tmp_path):
    source, owner, db, request, clock, case, maps, actual, visible, current, refs = _prepare(
        tmp_path, "D095-CONTROLLED-DUPLICATE-VINTAGE",
    )
    assert case["expected_stage"] == "UNIQUE_HIGHEST_VISIBLE_FINAL_VINTAGE"
    assert [o.native_record["bar"]["revision"] for o, p in refs] == [1, 2, 2]
    assert all(o.source_timestamp_raw == "2026-10-16" and o.native_record["contract"]["id"] == SUBJECT
               and o.native_record["model"]["convention"] == "controlled-model/1"
               and o.native_units == UNITS for o, p in refs)
    a, b = refs[1:]
    assert a[0].observation_occurrence_id != b[0].observation_occurrence_id
    assert a[0].received_ts_utc == b[0].received_ts_utc
    assert a[0].ingestion_sequence != b[0].ingestion_sequence
    assert _exact(a[1].native_value) == _exact(b[1].native_value)
    assert owner.materialise(request) is None
    _assert_history(owner.reads, request, ())
    del owner, source
    _empty_reopen(request, db)
