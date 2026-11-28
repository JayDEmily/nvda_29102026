"""Inert relative aligned-history proof authoring candidate; NOT installed or released.

Future physical path:
tests/product/m02_completion_28_prospective/support/d077-history/test_profile.py.
Only the separately designated strict Tester may import/collect/run after release.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import datetime, timedelta
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[5]
LEAF = "handoff/m02_completion_28_execution/L01a/"
POLICY = LEAF + "ALIGNED_HISTORY_SOURCE_POLICY_PROPOSED_20261126.json"
MANIFEST = LEAF + "ALIGNED_HISTORY_FINITE_SPECIMENS_PROPOSED_20261126.json"
INVENTORY = LEAF + "ALIGNED_HISTORY_JOINT_FIT_FINITE_CASES_PROPOSED_20261126.json"
POLICY_SHA = "9ba56098c273007980c893db39931ac86e7a3185bbb665f8c3f1e14f99b72af1"
MANIFEST_SHA = "bb03481de75e1820c7aff61777a4a3aa4f676440ec03e373a05c032a0417c76d"
INVENTORY_SHA = "3be150f2998b4187a81720b424c848099edeba7a9f638ae90d9aae95d4c5d5c1"
PROVIDER = "foundation-controlled-aligned-history"
VARIANT = "prior_close_history_v1"
SCOPE = PROVIDER + "/" + VARIANT
ROLES = ("R037", "R042")
UNIT = f.UnitConventionVersionV1(
    "t01-l01a-underlying-price",
    1,
    "USD_per_share",
    "USD_per_share",
    Decimal("1"),
    Decimal("0"),
)
META = (
    ("instrument.id", ("instrument", "id")),
    ("session.id", ("session", "id")),
    ("adjustment.basis", ("adjustment", "basis")),
    ("price.kind", ("price", "kind")),
)
MAPS = {
    rid: raw.RawSignalProjectionMappingV1(
        "t01-l01a-" + rid.lower() + "-history",
        1,
        raw.RawSignalCatalogueId(rid),
        PROVIDER,
        VARIANT,
        path,
        "USD_per_share",
        META,
    )
    for rid, path in (("R037", ("trade", "last")), ("R042", ("official_close", "value")))
}
LEGAL = ("A", "B", "RANK", "COND", "C_NONPRIOR")

SIGNAL = "D077"
PARENT_SIGNALS = ("D073", "D074", "D072")
PINS = {
    "D073": (
        "a7234477d581e6cba27e470919fa092c4ed5054d5a1aa31d2019d8fa94d16f48",
        "867444cecdf23c191269b1b3856410cc1ee6e3b81b8730dafa6d6528b78d6e0a",
    ),
    "D074": (
        "524b2d2a4aa94a0c1c55ea376650d14648af67c46e73763ce3e8cc0f2e9e0c0e",
        "f2a2208a73d291e614577eaf2b81ffd13d699c4efbc2eeeb6258569ac8aa1c34",
    ),
    "D072": (
        "4f8214d1ca11eaf0769206f3f322c799f44883bd266e63748e937dea5602b739",
        "637ff9b90b916ee69ee956db28e191ef86be3764ce2004b5fc24e371fa5869df",
    ),
    "D077": (
        "88bdd385ff91432940f4d27a8cff2bce6af22a8c85b858f53ba2f674d3c30a3c",
        "7f1b9f882d815616aa8e2fe53d6069800c7524f375202bff4eea5a67bf91a735",
    ),
}
CASE_HASHES = {
    "SUP-D077-HISTORY-SUCCESS": (
        "fa8258971344733dd919dd322f9625680e7d04be98faa0b52ca216d478e4b8b5"
    ),
    "SUP-D077-HISTORY-REACHED_REFUSAL": (
        "e2318098ea40daddb82137289ad76d29d065ff7078ced39c3269f6b128c82cfa"
    ),
    "SUP-D077-HISTORY-MIXED-ORIGINAL-ROSTER": (
        "0ef5bad7b7c1a2c7e0c9874afd05630c68b4fc0aa95feec841ea95b4338e7cfe"
    ),
}
A_SHA = "ca87adff2e2aa7a509c2f1d584eda019665fd7f38b3966b8be901fbddbcb22d1"


def _pinned(path, digest):
    data = (ROOT / path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    return json.loads(data)


def _sha(value):
    data = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def _expand(manifest, name, digest):
    (spec,) = [v for v in manifest["specimens"] if v["specimen_id"] == name]
    members = copy.deepcopy(manifest["base_members"])
    for change in spec["operations"]:
        if change["op"] == "append":
            members.append(copy.deepcopy(change["member"]))
        else:
            assert change["op"] == "replace"
            (i,) = [
                i
                for i, row in enumerate(members)
                if row["observation"]["observation_occurrence_id"] == change["old_id"]
            ]
            members[i] = copy.deepcopy(change["member"])
    members.sort(
        key=lambda row: (
            datetime.fromisoformat(row["observation"]["received_ts_utc"]),
            row["observation"]["ingestion_sequence"],
            row["observation"]["observation_occurrence_id"],
        )
    )
    assert len(members) == spec["expanded_count"]
    assert _sha(members) == spec["expanded_sha256"] == digest
    for frame in manifest["frames"]:
        slot = frame["slot"]
        assert (
            _sha([row for row in members if row["slot"] == slot])
            == (spec["frame_roster_sha256"][slot])
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
        selection_identity=raw.RawSelectionIdentityV1(
            tuple((key, _path(native, path)) for key, path in META)
        ),
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
            raw.RawSignalCatalogueId(rid),
            oid,
            mappings=(MAPS[rid],),
        )
        _assert_original(original, literal)
        _assert_projection(projected, literal, rid)
        actual[key] = (original, projected)
    return actual


def _visible(source, members, actual, rid, event, cutoff, subject):
    page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId(rid),
        mappings=(MAPS[rid],),
        subject_instrument=subject,
        received_at_or_before_utc=cutoff,
        event_at_or_before_utc=event,
        limit=100,
        cursor=None,
    )
    assert type(page) is raw.ProjectedRawHistoryPageV1
    assert page.next_cursor is None
    expected = tuple(
        actual[m["observation"]["observation_occurrence_id"]][1]
        for m in members
        if m["role"] == rid
        and m["subject"] == subject
        and datetime.fromisoformat(m["observation"]["received_ts_utc"]) <= cutoff
        and datetime.fromisoformat(m["observation"]["source_timestamp_raw"]) <= event
    )
    assert _exact(page.items) == _exact(expected)
    return page.items


def _pairs(members, actual, frame, role, subject):
    return tuple(
        actual[m["observation"]["observation_occurrence_id"]]
        for m in members
        if (m["slot"], m["subject"], m["role"]) == (frame["slot"], subject, role)
    )


def _role(
    pair, frame, role, subject, *, anchor=None, kind=None, units="USD_per_share", cutoff=None
):
    original, projection = pair
    event = datetime.fromisoformat(original.source_timestamp_raw)
    expect_anchor = frame["as_of" if role == "R037" else "reference"]
    expect_kind = "current_last" if role == "R037" else "official_close"
    session = frame["session_current" if role == "R037" else "session_reference"]
    assert event == (anchor or datetime.fromisoformat(expect_anchor))
    assert (
        event <= original.received_ts_utc <= (cutoff or datetime.fromisoformat(frame["row_cutoff"]))
    )
    assert original.raw_signal_catalogue_ids == (raw.RawSignalCatalogueId(role),)
    assert original.source_provider == raw.provider_id(PROVIDER)
    assert original.source_variant == VARIANT and original.subject_instrument == subject
    assert original.source_temporal_kind == "true_instant"
    assert original.source_timezone_native == "UTC"
    assert original.native_units == units
    assert original.native_record["instrument"]["id"] == subject
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
        datetime.fromisoformat(c["start"]),
        datetime.fromisoformat(c["end"]),
        datetime.fromisoformat(c["history_complete_from"]),
    )


def _case(case_id):
    policy = _pinned(POLICY, POLICY_SHA)
    manifest = _pinned(MANIFEST, MANIFEST_SHA)
    inventory = _pinned(INVENTORY, INVENTORY_SHA)
    (case,) = [x for x in inventory["physical_cases"] if x["case_id"] == case_id]
    digest = hashlib.sha256(
        json.dumps(
            case,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()
    assert digest == CASE_HASHES[case_id]
    assert case["family"] == SIGNAL and case["execution_authorised"] is False
    assert [x["slot"] for x in manifest["frames"]] == [f"S{i}" for i in range(8)]
    for signal, (brief_sha, binding_sha) in PINS.items():
        brief = ROOT / (LEAF + f"ALIGNED_HISTORY_{signal}_IMPLEMENTATION_BRIEF.md")
        binding = (
            ROOT / f"implementation/authority/T01_ALIGNED_HISTORY_{signal}_AUTHORITY_BINDING.yaml"
        )
        assert hashlib.sha256(brief.read_bytes()).hexdigest() == brief_sha
        assert hashlib.sha256(binding.read_bytes()).hexdigest() == binding_sha
    return policy, manifest, case


def _admission(signal):
    return f.OwnerAdmissionV1("M02", PINS[signal][0])


def _ref(value):
    return f.VersionRefV1(value["id"], value["version"])


def _parameter(profile):
    ref = profile["parameter_ref"]
    return f.CalculationParameterSetV1(
        ref["id"],
        ref["version"],
        profile["parameter_profile"],
        profile["subject"],
        tuple(profile["members"]),
    )


def _selection(profile):
    ref = profile["selection_ref"]
    # Own relative selection records ordered member subjects; source conventions
    # describe the retained nested lineage, not a separately selected raw source.
    members = tuple(profile["members"]) if profile["derived_dependencies"] else ()
    return f.InputSelectionPolicyVersionV1(
        ref["id"],
        ref["version"],
        ("subject_instrument", "instrument.id", "session.id", "adjustment.basis", "price.kind"),
        timedelta(seconds=86400),
        timedelta(0),
        ("true_instant",),
        members,
        PROVIDER,
        VARIANT,
        SCOPE,
        100,
        2,
    )


def _definition(signal, policy):
    p = policy["profiles"][signal]
    refs = tuple(f.AuthorityArtifactRefV1(x["path"], x["sha256"]) for x in policy["authority_refs"])
    return f.CalculationDefinitionV1(
        signal,
        p["calculation_definition_version"],
        p["kernel"],
        p["equation"],
        tuple(p["raw_dependencies"]),
        tuple(p["derived_dependencies"]),
        p["parameter_profile"],
        p["units"],
        p["result_shape"],
        (
            *refs,
            f.AuthorityArtifactRefV1(POLICY, POLICY_SHA),
            f.AuthorityArtifactRefV1(
                LEAF + f"ALIGNED_HISTORY_{signal}_IMPLEMENTATION_BRIEF.md", PINS[signal][0]
            ),
        ),
    )


def _request(signal, policy, frame, predecessor_ids=()):
    p = policy["profiles"][signal]
    return f.AlignedHistoryRequestV1(
        derived_signal_id=signal,
        subject_instrument=p["subject"],
        slot=frame["slot"],
        as_of_utc=datetime.fromisoformat(frame["as_of"]),
        knowledge_cutoff_utc=datetime.fromisoformat(frame["row_cutoff"]),
        calculation_definition_version=p["calculation_definition_version"],
        source_profile_ref=_ref(p["profile_ref"]),
        parameter_set_ref=_ref(p["parameter_ref"]),
        input_selection_policy_ref=_ref(p["selection_ref"]),
        context_refs=(_context(frame).ref,),
        predecessor_occurrence_ids=predecessor_ids,
    )


def _row(row, signal, policy, frame, request, now, result, pairs=(), parents=()):
    p = policy["profiles"][signal]
    assert type(row) is f.AlignedHistoryOccurrenceV1
    assert re.fullmatch(r"mmtahistory1:[0-9a-f]{64}", row.derived_occurrence_id)
    expected = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/aligned_history/v1",
        implementation_brief_sha256=PINS[signal][0],
        derived_signal_id=signal,
        derived_occurrence_id=row.derived_occurrence_id,
        request=request,
        definition=_definition(signal, policy),
        source_policy_sha256=POLICY_SHA,
        source_profile_ref=_ref(p["profile_ref"]),
        parameter_set=_parameter(p),
        input_selection_policy=_selection(p),
        window_context=_context(frame),
        projection_mappings=tuple(MAPS[rid] for rid in ROLES) if pairs else (),
        unit_conventions=(UNIT,) if pairs else (),
        original_observations=tuple(pair[0] for pair in pairs),
        selected_projections=tuple(pair[1] for pair in pairs),
        predecessors=parents,
        result=result,
        units=p["units"],
        result_shape=p["result_shape"],
        window_seconds=frame["window_seconds"],
        effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        calculated_at_utc=now,
    )
    _compare_fields(row, expected, f.AlignedHistoryOccurrenceV1)


def _log_oracle(pairs, manifest, specimen, signal, slot):
    # Independently derive from literal/native price ratio; do not call product log,
    # read the product result as an oracle, or supply the expected value to the owner.
    current, reference = (pair[1].native_value for pair in pairs)
    ratio = Fraction(current) / Fraction(reference)
    assert ratio in (Fraction(100, 101), Fraction(1), Fraction(101, 100))
    with localcontext(Context(prec=80, rounding=ROUND_HALF_EVEN)) as context:
        high = context.divide(Decimal(ratio.numerator), Decimal(ratio.denominator)).ln()
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)) as context:
        result = context.plus(high) if ratio != 1 else Decimal("0")
    oracle = manifest["oracle_only_not_inputs"]["complete_legal_row_oracles"][specimen][slot]
    expected = Fraction(*oracle["exact_fraction_values_D071_through_D077"][int(signal[1:]) - 71])
    assert Fraction(result) == expected
    return result


def _history(reader, signal, policy, frames, results):
    assert len({row.derived_occurrence_id for row in results.values()}) == len(results)
    for row in results.values():
        assert _exact(reader.get_derived_occurrence(row.derived_occurrence_id)) == _exact(row)
    for effective, knowledge in ((7, 7), (6, 7), (7, 6), (3, 3)):
        actual = reader.list_derived_history(
            derived_signal_id=signal,
            subject_instrument=policy["profiles"][signal]["subject"],
            effective_at_or_before_utc=datetime.fromisoformat(frames[effective]["as_of"]),
            knowledge_at_or_before_utc=datetime.fromisoformat(frames[knowledge]["row_cutoff"]),
            limit=10,
        )
        expected = tuple(
            results[frame["slot"]]
            for frame in reversed(frames[: min(effective, knowledge) + 1])
            if frame["slot"] in results
        )
        assert _exact(actual) == _exact(expected)


def _produce_parent(tmp_path, policy, manifest, signal, specimen, slots, digest):
    # Separate genuine owner, sealed source, database and clock for each role.
    frames = manifest["frames"]
    subject = policy["profiles"][signal]["subject"]
    members = _expand(manifest, specimen, digest)
    source = f.create_aligned_history_source(admission=_admission(signal), specimen_id=specimen)
    actual = _source_evidence(source, members, specimen, digest)
    db = tmp_path / f"{specimen}-{signal}.sqlite"
    clock = [datetime.fromisoformat(frames[0]["default_underlying_calculated_at"])]
    owner = f.create_aligned_history_owner(
        admission=_admission(signal),
        source=source,
        predecessor_read_storages=(),
        storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    results = {}
    # Establish exact actual source pairs for all frames, including any deliberately
    # omitted materialisation. Omission never calls the parent producer for that slot.
    for frame in frames:
        slot = frame["slot"]
        if slot not in slots and specimen != "A":
            continue
        event = datetime.fromisoformat(frame["as_of"])
        cutoff = datetime.fromisoformat(frame["row_cutoff"])
        pairs = []
        for role in ROLES:
            (pair,) = _pairs(members, actual, frame, role, subject)
            _role(pair, frame, role, subject)
            visible = _visible(source, members, actual, role, event, cutoff, subject)
            assert _exact(pair[1]) in tuple(_exact(item) for item in visible)
            pairs.append(pair)
        if slot not in slots:
            continue
        clock[0] = datetime.fromisoformat(frame["default_underlying_calculated_at"])
        request = _request(signal, policy, frame)
        row = owner.materialise(request)
        expected = _log_oracle(pairs, manifest, specimen, signal, slot)
        _row(row, signal, policy, frame, request, clock[0], expected, tuple(pairs))
        results[slot] = row
    assert tuple(results) == tuple(slots)
    _history(owner.reads, signal, policy, frames, results)
    del owner, source
    storage = f.SQLiteReadStorageV1(str(db))
    reader = f.create_aligned_history_reader(admission=_admission(signal), storage=storage)
    _history(reader, signal, policy, frames, results)
    # Actual ordinary read-only getter output, not a synthetic parent payload.
    reopened = {
        slot: reader.get_derived_occurrence(row.derived_occurrence_id)
        for slot, row in results.items()
    }
    return storage, reader, reopened


def _corpus_sets(manifest, parents, frame):
    # Compare FULL actual original typed content, not corpus labels or prices.
    legal = {
        name: _expand(
            manifest,
            name,
            next(
                spec["expanded_sha256"]
                for spec in manifest["specimens"]
                if spec["specimen_id"] == name
            ),
        )
        for name in LEGAL
    }
    sets = []
    keys = []
    for parent in parents:
        assert len(parent.original_observations) == len(parent.selected_projections) == 2
        subject = parent.request.subject_instrument
        for role, original, projected in zip(
            ROLES, parent.original_observations, parent.selected_projections, strict=True
        ):
            key = (frame["slot"], subject, role)
            assert key not in keys
            keys.append(key)
            membership = set()
            for name, members in legal.items():
                rows = [
                    m["observation"] for m in members if (m["slot"], m["subject"], m["role"]) == key
                ]
                for literal in rows:
                    try:
                        _assert_original(original, literal)
                        _assert_projection(projected, literal, role)
                    except AssertionError:
                        continue
                    membership.add(name)
            assert membership
            sets.append(membership)
    assert len(keys) == 2 * len(parents)
    return sets


def _lawful_parents(parents, policy, frame, now, *, same_frame=True):
    assert tuple(row.derived_signal_id for row in parents) == PARENT_SIGNALS
    assert len({row.derived_occurrence_id for row in parents}) == len(parents)
    for signal, row in zip(PARENT_SIGNALS, parents, strict=True):
        assert type(row) is f.AlignedHistoryOccurrenceV1
        assert row.request.subject_instrument == policy["profiles"][signal]["subject"]
        assert row.source_profile_ref == _ref(policy["profiles"][signal]["profile_ref"])
        assert row.definition == _definition(signal, policy)
        assert row.knowledge_cutoff_utc <= now and row.calculated_at_utc <= now
        assert row.knowledge_cutoff_utc < row.calculated_at_utc
        if same_frame:
            assert row.request.slot == frame["slot"]
            assert row.effective_as_of_utc == datetime.fromisoformat(frame["as_of"])
            assert row.knowledge_cutoff_utc == datetime.fromisoformat(frame["row_cutoff"])
            assert row.window_context == _context(frame)
            assert row.window_seconds == frame["window_seconds"]


def _relative_result(parents, manifest, frame, specimen="A"):
    values = tuple(Fraction(row.result) for row in parents)
    # This arithmetic is independently derived; each parent Decimal has already
    # been established from its literal price ratio, manifest oracle and typed lineage.
    value = (values[0] + values[1]) / 2 - values[2]
    expected = Fraction(
        *manifest["oracle_only_not_inputs"]["complete_legal_row_oracles"][specimen][frame["slot"]][
            "exact_fraction_values_D071_through_D077"
        ][int(SIGNAL[1:]) - 71]
    )
    assert value == expected
    return f.ExactRatioV1(value.numerator, value.denominator)


def _relative_owner(tmp_path, storages, frame):
    db = tmp_path / f"{SIGNAL}.sqlite"
    clock = [datetime.fromisoformat(frame["default_relative_calculated_at"])]
    # Exact proposed additive API: no raw source, only concrete ordered storage per role.
    owner = f.create_aligned_history_owner(
        admission=_admission(SIGNAL),
        source=None,
        predecessor_read_storages=storages,
        storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    return owner, db, clock


def _ordinary_relative(db):
    return f.create_aligned_history_reader(
        admission=_admission(SIGNAL),
        storage=f.SQLiteReadStorageV1(str(db)),
    )


def _normal_history(tmp_path, case_id, refusal):
    policy, manifest, case = _case(case_id)
    frames = manifest["frames"]
    setup = case["setup_and_reached_preconditions"]
    assert tuple(setup["actual_parent_producer_slots"]) == PARENT_SIGNALS
    assert case["specimens"] == [{"id": "A", "expanded_sha256": A_SHA}]
    produced = tuple(
        _produce_parent(
            tmp_path, policy, manifest, sig, "A", setup["actual_parent_producer_slots"][sig], A_SHA
        )
        for sig in PARENT_SIGNALS
    )
    storages, readers, parent_rows = zip(*produced, strict=True)
    owner, db, clock = _relative_owner(tmp_path, storages, frames[0])
    results = {}
    for frame in frames:
        slot = frame["slot"]
        clock[0] = datetime.fromisoformat(frame["default_relative_calculated_at"])
        if slot == "S3" and refusal is not None:
            # Negative target sequence is explicit in the individual case function;
            # assert actual reached facts before a single refused target call.
            ids = refusal(case, policy, manifest, frame, clock[0], readers, parent_rows)
            request = _request(SIGNAL, policy, frame, ids)
            assert len(set(ids)) == len(PARENT_SIGNALS)
            assert owner.materialise(request) is None
            continue
        parents = tuple(rows[slot] for rows in parent_rows)
        _lawful_parents(parents, policy, frame, clock[0])
        assert set.intersection(*_corpus_sets(manifest, parents, frame))
        ids = tuple(parent.derived_occurrence_id for parent in parents)
        request = _request(SIGNAL, policy, frame, ids)
        expected = _relative_result(parents, manifest, frame)
        row = owner.materialise(request)
        _row(row, SIGNAL, policy, frame, request, clock[0], expected, parents=parents)
        results[slot] = row
    assert len(results) == case["independent_oracle"]["actual_history_rows"]
    if refusal is None:
        replay = case["request_and_exact_variation"]["later_replay"]
        assert replay == {"slot": "S7", "now": "2026-10-20T12:40:06Z", "same_request": True}
        clock[0] = datetime.fromisoformat(replay["now"])
        assert _exact(owner.materialise(results["S7"].request)) == _exact(results["S7"])
    else:
        assert "S3" not in results and set(results) == {f"S{i}" for i in (0, 1, 2, 4, 5, 6, 7)}
    _history(owner.reads, SIGNAL, policy, frames, results)
    del owner
    _history(_ordinary_relative(db), SIGNAL, policy, frames, results)
    for sig, reader, rows in zip(PARENT_SIGNALS, readers, parent_rows, strict=True):
        _history(reader, sig, policy, frames, rows)


def test_d077_history_success(tmp_path):
    _normal_history(tmp_path, "SUP-D077-HISTORY-SUCCESS", None)


def _missing_soxx(case, policy, manifest, frame, now, readers, rows):
    assert case["expected_stage"] == "RELATIVE_PARENT_LOOKUP"
    variation = case["request_and_exact_variation"]
    assert variation["target"] == "S3" and variation["cutoff"] == frame["row_cutoff"]
    smh, qqq = rows[0]["S3"], rows[2]["S3"]
    assert "S3" not in rows[1]  # Actual SOXX S3 raw pair was checked, not materialised.
    missing = variation["parent_ids_order"][1]["identity"]
    assert missing == "mmtahistory1:" + "0" * 64
    assert readers[1].get_derived_occurrence(missing) is None
    for sig, parent, reader in (("D073", smh, readers[0]), ("D072", qqq, readers[2])):
        assert _exact(reader.get_derived_occurrence(parent.derived_occurrence_id)) == _exact(parent)
        assert parent.derived_signal_id == sig and parent.request.slot == "S3"
        assert parent.source_profile_ref == _ref(policy["profiles"][sig]["profile_ref"])
        assert parent.effective_as_of_utc == datetime.fromisoformat(frame["as_of"])
        assert parent.knowledge_cutoff_utc == datetime.fromisoformat(frame["row_cutoff"])
        assert parent.window_context == _context(frame)
        assert parent.knowledge_cutoff_utc <= now and parent.calculated_at_utc <= now
    return smh.derived_occurrence_id, missing, qqq.derived_occurrence_id


def test_d077_missing_soxx_parent(tmp_path):
    _normal_history(tmp_path, "SUP-D077-HISTORY-REACHED_REFUSAL", _missing_soxx)


def test_d077_mixed_original_roster(tmp_path):
    policy, manifest, case = _case("SUP-D077-HISTORY-MIXED-ORIGINAL-ROSTER")
    assert case["expected_stage"] == "RELATIVE_COMPLETE_ACTUAL_SOURCE_ROSTER"
    frame = manifest["frames"][6]
    variation = case["request_and_exact_variation"]
    assert (variation["target"], variation["as_of"], variation["cutoff"], variation["now"]) == (
        "S6",
        frame["as_of"],
        frame["row_cutoff"],
        frame["default_relative_calculated_at"],
    )
    setup = case["setup_and_reached_preconditions"]["actual_parent_producers"]
    assert [(x["signal"], x["specimen"], x["slots"], x["store"]) for x in setup] == [
        ("D073", "RANK", ["S6"], "RANK_D073"),
        ("D074", "COND", ["S6"], "COND_D074"),
        ("D072", "A", ["S6"], "A_D072"),
    ]
    digests = {x["id"]: x["expanded_sha256"] for x in case["specimens"]}
    produced = tuple(
        _produce_parent(
            tmp_path,
            policy,
            manifest,
            x["signal"],
            x["specimen"],
            x["slots"],
            digests[x["specimen"]],
        )
        for x in setup
    )
    storages, readers, rows = zip(*produced, strict=True)
    parents = tuple(item["S6"] for item in rows)
    now = datetime.fromisoformat(variation["now"])
    _lawful_parents(parents, policy, frame, now)
    for parent, spec in zip(parents, setup, strict=True):
        assert parent.calculated_at_utc == datetime.fromisoformat(spec["first_calculated_at"])
        assert (
            type(parent.result) is Decimal and parent.result.as_tuple() == Decimal("0").as_tuple()
        )
        assert tuple(p.native_value for p in parent.selected_projections) == (Decimal("10100"),) * 2
    ids = sorted(
        original.observation_occurrence_id.value
        for parent in parents
        for original in parent.original_observations
    )
    oracle = case["independent_oracle"]
    assert ids == oracle["actual_required_original_ids"]
    sets = _corpus_sets(manifest, parents, frame)
    assert set.intersection(*sets[:2]) == {"RANK"}
    assert set.intersection(*sets[2:4]) == {"COND"}
    assert set.intersection(*sets[4:]) == set(LEGAL)
    assert sorted(set.intersection(*sets)) == oracle["legal_corpus_intersection"] == []
    values = tuple(Fraction(parent.result) for parent in parents)
    counterfactual = (values[0] + values[1]) / 2 - values[2]
    assert [counterfactual.numerator, counterfactual.denominator] == oracle[
        "would_be_relative_ratio"
    ]
    owner, db, clock = _relative_owner(tmp_path, storages, frame)
    assert clock[0] == now
    request = _request(SIGNAL, policy, frame, tuple(row.derived_occurrence_id for row in parents))
    # Exactly one D077 target call, all mandatory upstream facts independently lawful.
    assert owner.materialise(request) is None
    _history(owner.reads, SIGNAL, policy, manifest["frames"], {})
    del owner
    _history(_ordinary_relative(db), SIGNAL, policy, manifest["frames"], {})
    for sig, reader, result in zip(PARENT_SIGNALS, readers, rows, strict=True):
        _history(reader, sig, policy, manifest["frames"], result)
