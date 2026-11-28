"""Inert D078 same-fit residual proof authoring candidate; NOT installed or released.

Future path: tests/product/m02_completion_28_prospective/d078/test_signal.py.
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
from itertools import permutations
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[4]
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

SIGNAL = "D078"
PINS = {
    "D071": (
        "65f2d0f9135f291773ab6081ec76892a967315df3ecb9c1760a4e2687a296e5e",
        "30cbb5fe2f8a1b720bc58b55b05f3c88b736401f03d03199404444b60330dc03",
    ),
    "D072": (
        "4f8214d1ca11eaf0769206f3f322c799f44883bd266e63748e937dea5602b739",
        "637ff9b90b916ee69ee956db28e191ef86be3764ce2004b5fc24e371fa5869df",
    ),
    "D073": (
        "a7234477d581e6cba27e470919fa092c4ed5054d5a1aa31d2019d8fa94d16f48",
        "867444cecdf23c191269b1b3856410cc1ee6e3b81b8730dafa6d6528b78d6e0a",
    ),
    "D074": (
        "524b2d2a4aa94a0c1c55ea376650d14648af67c46e73763ce3e8cc0f2e9e0c0e",
        "f2a2208a73d291e614577eaf2b81ffd13d699c4efbc2eeeb6258569ac8aa1c34",
    ),
    "D075": (
        "24ec8f08faf1a61059cee69b8c675767345809ae6a0dd90ab852a2fc30977750",
        "50120c02327ed212e8821ac3795d4f64daa3e38d77ecd5c92c7b20f6a2ba8c3f",
    ),
    "D076": (
        "c2b30721c0f535d00bb09cb801461ddf875966a93049c47fe572856f43fde480",
        "6f1324ab9922a1cd8b9994da931ee8f946d7d8666a758f8554269d092d006a80",
    ),
    "D077": (
        "88bdd385ff91432940f4d27a8cff2bce6af22a8c85b858f53ba2f674d3c30a3c",
        "7f1b9f882d815616aa8e2fe53d6069800c7524f375202bff4eea5a67bf91a735",
    ),
    "D079": (
        "47b4c5d27d7ffc57710d70973825500524e3d9bbc179cc59df0d356381612127",
        "c90aec925d606bcf9537ffad014338a579ab856884d659a85dd4ecd10050cf54",
    ),
    "D080": (
        "69f38747173cd464ae8586f919caa23f8ae754fbb1190b001675cae05e5a709e",
        "dcc6589fe36f091f4ea68da97b011ec67ea416e706e1ba9089da8223e1cd84d7",
    ),
    "D081": (
        "cf2bf8c51611b8b5baf8a98d1f42fcecd63f069dd45b20dc9135844b99b6e90f",
        "a2dfca758a22fbe7898d7534a86d094457333ad74ef5022ffd0d968334183eae",
    ),
    "D078": (
        "b1fc6fe2b84f53d59b47c72c01f6265bb9a7c668a4e7f89fd7b963b0b11aa792",
        "d09915e073f9faf1f7c8a3b6371025ab3aee95d0cf25577420c8b934b136f194",
    ),
}
CASE_HASHES = {
    "D078-CONTROLLED-SUCCESS": "b442c3215ea653bea9e3de82707478235390c7a11c8a122204273933a8409255",
    "D078-CONTROLLED-REACHED_REFUSAL": "c0c2b4a5b0bca115e808c210bdbb58bf27085bdab61e9d112714a2945bf2f4a7",
    "D078-CURRENT-ROW-MISALIGNMENT": "a3c118f8dda3ea0eef2c5a2ac727369a82efb665de19b3125a75fc0de7405650",
    "D078-NONPRIOR-FIT": "dbf4c920d04de834f9f572503318f711f02c259086d98bc71e89c83b5e4476b9",
    "D078-COEFFICIENT-NOT-KNOWN-AT-RESIDUAL-CUTOFF": "57c268e9d79e7ed8c0a7bc8f1decae1ab9768d48bf842499ae89f3e224b71dd4",
}


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


def _ratio(value):
    if type(value) is Decimal:
        return Fraction(value)
    assert type(value) is f.ExactRatioV1
    result = Fraction(value.numerator, value.denominator)
    assert (value.numerator, value.denominator) == (result.numerator, result.denominator)
    return result


def _er(value):
    return f.ExactRatioV1(value.numerator, value.denominator)


def _sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def _tag(value):
    identities = (
        ("RawSignalCatalogueId", raw.RawSignalCatalogueId("R001")),
        ("observation_occurrence_id", raw.observation_occurrence_id("id")),
        ("ingestion_sequence_scope", raw.ingestion_sequence_scope("id")),
        ("concept_id", raw.concept_id("id")),
        ("contract_id", raw.contract_id("id")),
        ("delivery_artifact_ref", raw.delivery_artifact_ref("id")),
        ("provider_id", raw.provider_id("id")),
    )
    for name, example in identities:
        if type(value) is type(example):
            return {"t": "identity", "n": name, "v": value.value}
    if value is None:
        return {"t": "none"}
    if type(value) is Decimal:
        sign, digits, exponent = value.as_tuple()
        return {"t": "decimal", "s": sign, "d": list(digits), "e": exponent}
    if type(value) is datetime:
        assert value.utcoffset() == timedelta(0)
        return {"t": "datetime", "v": value.isoformat()}
    if type(value) is timedelta:
        return {"t": "duration", "v": value // timedelta(microseconds=1)}
    if type(value) is bytes:
        return {"t": "bytes", "v": value.hex()}
    if type(value) is bool:
        return {"t": "bool", "v": value}
    if type(value) is int:
        return {"t": "int", "v": str(value)}
    if type(value) is str:
        return {"t": "str", "v": value}
    if type(value) in (tuple, list):
        return {"t": type(value).__name__, "v": [_tag(item) for item in value]}
    if isinstance(value, Mapping):
        assert all(type(k) is str for k in value)
        return {"t": "mapping", "v": {k: _tag(v) for k, v in value.items()}}
    permitted = (
        raw.RawObservationOccurrenceV1,
        raw.ProjectedRawValueV1,
        raw.RawSelectionIdentityV1,
        raw.RawSignalProjectionMappingV1,
        f.VersionRefV1,
        f.AuthorityArtifactRefV1,
        f.CalculationDefinitionV1,
        f.ExactRatioV1,
    )
    assert type(value) in permitted, type(value)
    return {
        "t": "record",
        "n": type(value).__name__,
        "v": {k: _tag(v) for k, v in _fields(value).items()},
    }


def _fields(record):
    return {field.name: getattr(record, field.name) for field in fields(record)}


def _envelope(name, content):
    return json.dumps(
        _tag({"record": name, "version": 1, "content": content}),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _parent_content(row):
    content = _fields(row)
    for name in ("request", "parameter_set", "input_selection_policy", "window_context"):
        content[name] = _fields(content[name])
    content["unit_conventions"] = tuple(_fields(x) for x in row.unit_conventions)
    content["predecessors"] = tuple(_parent_bytes(x) for x in row.predecessors)
    return content


def _parent_bytes(row):
    assert type(row) is f.AlignedHistoryOccurrenceV1
    return _envelope("AlignedHistoryOccurrenceV1", _parent_content(row))


def _assert_parent_id(row):
    content = _parent_content(row)
    content.pop("derived_occurrence_id")
    content.pop("calculated_at_utc")
    assert row.derived_occurrence_id == "mmtahistory1:" + _sha_bytes(
        _envelope("AlignedHistoryOccurrenceV1", content)
    )


def _fit_a():
    with localcontext(Context(prec=90, rounding=ROUND_HALF_EVEN)) as context:
        precise = context.divide(Decimal(101), Decimal(100)).ln()
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)) as context:
        return Fraction(context.plus(precise))


def _det(matrix):
    # Independent Leibniz formula, not the future product Gauss-Jordan solver.
    total = Fraction(0)
    for order in permutations(range(len(matrix))):
        parity = sum(
            order[i] > order[j] for i in range(len(order)) for j in range(i + 1, len(order))
        )
        term = Fraction(-1 if parity % 2 else 1)
        for i, j in enumerate(order):
            term *= matrix[i][j]
        total += term
    return total


def _minor(matrix, i, j):
    return tuple(
        tuple(x for c, x in enumerate(row) if c != j) for r, row in enumerate(matrix) if r != i
    )


def _numeric(actual_rows):
    a = _fit_a()
    x = tuple((Fraction(1), *(_ratio(row.result) / a for row in rows[1:])) for rows in actual_rows)
    y = tuple(_ratio(rows[0].result) / a for rows in actual_rows)
    assert len(x) == 6 and all(len(row) == 4 for row in x)
    assert all(abs(v) <= 2 and v.denominator <= 2 for row in x for v in row)
    assert all(abs(v) <= 1 and v.denominator <= 2 for v in y)
    gram = tuple(tuple(sum(row[i] * row[j] for row in x) for j in range(4)) for i in range(4))
    h = tuple(sum(row[i] * target for row, target in zip(x, y, strict=True)) for i in range(4))
    det = _det(gram)
    if det == 0:
        return det, None, None
    inverse = tuple(
        tuple(Fraction((-1) ** (i + j)) * _det(_minor(gram, j, i)) / det for j in range(4))
        for i in range(4)
    )
    condition = max(sum(abs(v) for v in row) for row in gram) * max(
        sum(abs(v) for v in row) for row in inverse
    )
    # Cramer's rule independent of production elimination.
    vector = tuple(
        _det(tuple(tuple(h[i] if j == col else gram[i][j] for j in range(4)) for i in range(4)))
        / det
        for col in range(4)
    )
    return det, condition, (a * vector[0], *vector[1:])


FIT_ROLES = ("D075", "D071", "D076", "D077")
COMPONENTS = {"D079": "beta_market", "D080": "beta_tech", "D081": "beta_semi"}
MODEL_VERSION = "T01-L01A-JOINT-OLS-WITH-INTERCEPT-V1"
NUMERIC_VERSION = "T01-L01A-EXACT-FRACTION-GRAM-INF-V1"
HISTORY_SIGNALS = tuple(f"D{i}" for i in range(71, 78))
IDENTITY = "ACTUAL_PUBLIC_GETTER_ID_AND_CANONICAL_PAYLOAD"


def _shared(row, slot):
    target, spy, tech, semi = row
    assert tuple(x.derived_signal_id for x in row) == FIT_ROLES
    assert all(x.request.slot == slot for x in row)
    assert tuple(x.derived_signal_id for x in tech.predecessors) == ("D072", "D071")
    assert tuple(x.derived_signal_id for x in semi.predecessors) == ("D073", "D074", "D072")
    qqq, nested_spy = tech.predecessors
    smh, soxx, nested_qqq = semi.predecessors
    for left, right in ((spy, nested_spy), (qqq, nested_qqq)):
        assert left.derived_occurrence_id == right.derived_occurrence_id
        assert _parent_bytes(left) == _parent_bytes(right)
    return (target, spy, qqq, smh, soxx)


def _request_content(request):
    content = _fields(request)
    content["rows"] = tuple(_fields(row) for row in request.rows)
    return content


def _fit_content(manifest):
    content = _fields(manifest)
    content["rows"] = tuple(tuple(_parent_bytes(parent) for parent in row) for row in manifest.rows)
    return content


def _fit_bytes(manifest):
    return _envelope("AlignedFitManifestV1", _fit_content(manifest))


def _coefficient_content(occurrence):
    content = _fields(occurrence)
    content["request"] = _request_content(occurrence.request)
    content["fit"] = _fit_bytes(occurrence.fit)
    for key in ("parameter_set", "input_selection_policy", "window_context"):
        content[key] = _fields(content[key])
    return content


def _coefficient_bytes(occurrence):
    return _envelope("AlignedCoefficientOccurrenceV1", _coefficient_content(occurrence))


def _assert_coefficient(
    signal, occurrence, request, policy, frame, rows, det, condition, vector, now
):
    assert type(occurrence) is f.AlignedCoefficientOccurrenceV1
    fit = occurrence.fit
    assert type(fit) is f.AlignedFitManifestV1
    expected_fit = dict(
        fit_id=fit.fit_id,
        fit_profile_ref=f.VersionRefV1("t01-l01a-shared-joint-ols", 1),
        source_policy_sha256=POLICY_SHA,
        model_version=MODEL_VERSION,
        numeric_version=NUMERIC_VERSION,
        origin_slot=request.origin_slot,
        effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        row_slots=tuple(row.slot for row in request.rows),
        rows=rows,
        member_occurrence_ids=tuple(tuple(p.derived_occurrence_id for p in row) for row in rows),
        member_payload_sha256=tuple(
            tuple(_sha_bytes(_parent_bytes(p)) for p in row) for row in rows
        ),
        determinant=_er(det),
        condition=_er(condition),
        intercept=_er(vector[0]),
        beta_market=_er(vector[1]),
        beta_tech=_er(vector[2]),
        beta_semi=_er(vector[3]),
    )
    _compare_fields(fit, expected_fit, f.AlignedFitManifestV1)
    # The independently encoded fit digest includes the exact full retained evidence.
    content = _fit_content(fit)
    content.pop("fit_id")
    assert fit.fit_id == "mmtafit1:" + _sha_bytes(_envelope("AlignedFitManifestV1", content))
    p = policy["profiles"][signal]
    component = COMPONENTS[signal]
    expected = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/aligned_history/v1",
        implementation_brief_sha256=PINS[signal][0],
        derived_signal_id=signal,
        derived_occurrence_id=occurrence.derived_occurrence_id,
        request=request,
        definition=_definition(signal, policy),
        source_policy_sha256=POLICY_SHA,
        source_profile_ref=_ref(p["profile_ref"]),
        parameter_set=_parameter(p),
        input_selection_policy=_selection(p),
        window_context=_context(frame),
        component=component,
        fit=fit,
        result=getattr(fit, component),
        units=p["units"],
        result_shape=p["result_shape"],
        effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        calculated_at_utc=now,
    )
    _compare_fields(occurrence, expected, f.AlignedCoefficientOccurrenceV1)
    content = _coefficient_content(occurrence)
    content.pop("derived_occurrence_id")
    content.pop("calculated_at_utc")
    assert occurrence.derived_occurrence_id == "mmtacoef1:" + _sha_bytes(
        _envelope("AlignedCoefficientOccurrenceV1", content)
    )


def _dt(value):
    return datetime.fromisoformat(value)


class Witness:
    """Fresh real public owners/stores for one exact admitted specimen.

    History and coefficient production are distinct operations; test bodies
    explicitly order prior, current, and delayed first coefficient calculation.
    """

    def __init__(self, path, policy, manifest, specimen, setup):
        self.path = path
        path.mkdir()
        self.policy, self.manifest, self.setup = policy, manifest, setup
        self.specimen = specimen["id"]
        self.members = _expand(manifest, self.specimen, specimen["expanded_sha256"])
        self.frames = {frame["slot"]: frame for frame in manifest["frames"]}
        self.declared = setup["history_producer_slots"]
        assert tuple(self.declared) == HISTORY_SIGNALS
        assert all(slots == self.declared["D071"] for slots in self.declared.values())
        self.clock = [_dt(self.frames["S0"]["default_underlying_calculated_at"])]
        self.storages = {
            sig: f.SQLiteReadStorageV1(str(path / (sig + ".sqlite")))
            for sig in (*HISTORY_SIGNALS, *COMPONENTS)
        }
        self.rows = {sig: {} for sig in HISTORY_SIGNALS}
        self.owners, self.sources, self.facts = {}, {}, {}
        self.coefficients, self.coefficient_owners = {}, {}
        for sig in HISTORY_SIGNALS[:5]:
            source = f.create_aligned_history_source(
                admission=_admission(sig), specimen_id=self.specimen
            )
            self.sources[sig] = source
            self.facts[sig] = _source_evidence(
                source, self.members, self.specimen, specimen["expanded_sha256"]
            )
            self.owners[sig] = f.create_aligned_history_owner(
                admission=_admission(sig),
                source=source,
                predecessor_read_storages=(),
                storage=f.SQLiteStorageV1(str(path / (sig + ".sqlite")), True),
                utc_now=lambda: self.clock[0],
            )

    def reader(self, signal):
        return f.create_aligned_history_reader(
            admission=_admission(signal), storage=self.storages[signal]
        )

    def actual(self, signal, slot):
        written = self.rows[signal][slot]
        actual = self.reader(signal).get_derived_occurrence(written.derived_occurrence_id)
        assert type(actual) is f.AlignedHistoryOccurrenceV1
        assert _parent_bytes(actual) == _parent_bytes(written)
        _assert_parent_id(actual)
        return actual

    def row(self, slot):
        return tuple(self.actual(sig, slot) for sig in FIT_ROLES)

    def produce(self, slot):
        frame = self.frames[slot]
        underlying_now = _dt(frame["default_underlying_calculated_at"])
        relative_now = _dt(frame["default_relative_calculated_at"])
        assert self.clock[0] <= underlying_now < relative_now
        self.clock[0] = underlying_now
        for sig in HISTORY_SIGNALS[:5]:
            assert slot not in self.rows[sig]
            subject = self.policy["profiles"][sig]["subject"]
            pairs = []
            for role in ROLES:
                (pair,) = _pairs(self.members, self.facts[sig], frame, role, subject)
                _role(pair, frame, role, subject)
                visible = _visible(
                    self.sources[sig],
                    self.members,
                    self.facts[sig],
                    role,
                    _dt(frame["as_of"]),
                    _dt(frame["row_cutoff"]),
                    subject,
                )
                assert _exact(pair[1]) in tuple(_exact(item) for item in visible)
                pairs.append(pair)
            pairs = tuple(pairs)
            request = _request(sig, self.policy, frame)
            record = self.owners[sig].materialise(request)
            expected = _log_oracle(pairs, self.manifest, self.specimen, sig, slot)
            _row(record, sig, self.policy, frame, request, underlying_now, expected, pairs)
            self.rows[sig][slot] = record
            self.actual(sig, slot)
        self.clock[0] = relative_now
        for sig, roles in (
            ("D076", ("D072", "D071")),
            ("D077", ("D073", "D074", "D072")),
        ):
            assert slot not in self.rows[sig]
            parents = tuple(self.actual(role, slot) for role in roles)
            assert all(parent.calculated_at_utc <= relative_now for parent in parents)
            if sig not in self.owners:
                self.owners[sig] = f.create_aligned_history_owner(
                    admission=_admission(sig),
                    source=None,
                    predecessor_read_storages=tuple(self.storages[role] for role in roles),
                    storage=f.SQLiteStorageV1(str(self.path / (sig + ".sqlite")), True),
                    utc_now=lambda: self.clock[0],
                )
            request = _request(
                sig, self.policy, frame, tuple(parent.derived_occurrence_id for parent in parents)
            )
            record = self.owners[sig].materialise(request)
            values = tuple(_ratio(parent.result) for parent in parents)
            expected = (
                values[0] - values[1] if sig == "D076" else (values[0] + values[1]) / 2 - values[2]
            )
            literal = self.manifest["oracle_only_not_inputs"]["complete_legal_row_oracles"][
                self.specimen
            ][slot]["exact_fraction_values_D071_through_D077"][int(sig[1:]) - 71]
            assert expected == Fraction(*literal)
            _row(
                record,
                sig,
                self.policy,
                frame,
                request,
                relative_now,
                _er(expected),
                parents=parents,
            )
            self.rows[sig][slot] = record
            self.actual(sig, slot)

    def produce_declared(self):
        slots = tuple(self.declared["D071"])
        assert slots == tuple(f"S{i}" for i in range(8 if self.setup["fit_origin"] == "S7" else 7))
        for slot in slots:
            self.produce(slot)
        self.check_histories(slots)

    def produce_current(self):
        assert self.setup["fit_origin"] == "S6"
        self.produce("S7")
        self.check_histories(tuple(f"S{i}" for i in range(8)))

    def check_histories(self, slots):
        for sig in HISTORY_SIGNALS:
            assert tuple(self.rows[sig]) == slots
            _history(self.reader(sig), sig, self.policy, list(self.frames.values()), self.rows[sig])
            for slot in slots:
                self.actual(sig, slot)

    def coefficient_reader(self, signal):
        return f.create_aligned_coefficient_reader(
            admission=_admission(signal), storage=self.storages[signal]
        )

    def actual_coefficient(self, signal):
        original = self.coefficients[signal]
        reader = self.coefficient_reader(signal)
        record = reader.get_derived_occurrence(original.derived_occurrence_id)
        assert type(record) is f.AlignedCoefficientOccurrenceV1
        assert _coefficient_bytes(record) == _coefficient_bytes(original)
        rows = reader.list_derived_history(
            derived_signal_id=signal,
            subject_instrument="NVDA",
            effective_at_or_before_utc=record.effective_as_of_utc,
            knowledge_at_or_before_utc=max(record.calculated_at_utc, record.knowledge_cutoff_utc),
            limit=10,
        )
        assert tuple(_coefficient_bytes(x) for x in rows) == (_coefficient_bytes(original),)
        return record

    def produce_coefficient(self, signal):
        assert signal not in self.coefficients and signal not in self.coefficient_owners
        producer = self.setup["actual_coefficient_producers"][signal]
        spec = producer["request"]
        assert spec["derived_signal_id"] == signal
        origin = self.setup["fit_origin"]
        assert spec["origin"] == producer["origin"] == origin
        slots = tuple(self.setup["requested_training_slots"])
        assert tuple(row["slot"] for row in spec["ordered_rows"]) == slots
        assert slots == tuple(
            f"S{i}" for i in range(1 if origin == "S6" else 2, 7 if origin == "S6" else 8)
        )
        assert tuple(self.setup["fit_row_roles"]) == FIT_ROLES
        rows, request_rows = [], []
        for row in spec["ordered_rows"]:
            slot = row["slot"]
            entries = row["member_ids"]
            assert tuple(entry["signal"] for entry in entries) == FIT_ROLES
            assert all(entry["slot"] == slot and entry["identity"] == IDENTITY for entry in entries)
            actual = self.row(slot)
            rows.append(actual)
            request_rows.append(
                f.AlignedFitRowRequestV1(
                    slot=slot, member_occurrence_ids=tuple(x.derived_occurrence_id for x in actual)
                )
            )
        rows = tuple(rows)
        cutoff, asof = _dt(spec["cutoff"]), _dt(spec["as_of"])
        assert len({parent.derived_occurrence_id for row in rows for parent in row}) == 24
        assert cutoff == asof + timedelta(seconds=4)
        assert asof == _dt(self.frames[origin]["as_of"])
        for slot, row in zip(slots, rows, strict=True):
            self.assert_row(slot, row, cutoff)
        self.assert_corpus(dict(zip(slots, rows, strict=True)))
        det, condition, vector = _numeric(rows)
        expected = {
            "A": (
                51,
                Fraction(1269, 34),
                (Fraction(4, 17), Fraction(-11, 34), Fraction(3, 34), Fraction(-14, 17)),
            ),
            "B": (
                51,
                Fraction(1269, 34),
                (Fraction(8, 17), Fraction(-151, 102), Fraction(-25, 51), Fraction(-28, 17)),
            ),
            "C_NONPRIOR": (
                164,
                Fraction(1664, 41),
                (Fraction(2, 41), Fraction(243, 164), Fraction(67, 82), Fraction(31, 41)),
            ),
        }[self.specimen]
        assert (det, condition, (vector[0] / _fit_a(), *vector[1:])) == expected
        assert 0 < condition <= 50
        p = self.policy["profiles"][signal]
        request = f.AlignedFitRequestV1(
            derived_signal_id=signal,
            subject_instrument=p["subject"],
            origin_slot=origin,
            as_of_utc=asof,
            knowledge_cutoff_utc=cutoff,
            calculation_definition_version=p["calculation_definition_version"],
            source_profile_ref=_ref(p["profile_ref"]),
            parameter_set_ref=_ref(p["parameter_ref"]),
            input_selection_policy_ref=_ref(p["selection_ref"]),
            context_refs=(_context(self.frames[origin]).ref,),
            rows=tuple(request_rows),
        )
        now = _dt(producer.get("first_calculated_at", self.setup["fit_now"]))
        assert self.clock[0] <= now and now >= cutoff
        self.clock[0] = now
        owner = f.create_aligned_coefficient_owner(
            admission=_admission(signal),
            predecessor_read_storages=tuple(self.storages[role] for role in FIT_ROLES),
            storage=f.SQLiteStorageV1(str(self.path / (signal + ".sqlite")), True),
            utc_now=lambda: self.clock[0],
        )
        self.coefficient_owners[signal] = owner
        record = owner.materialise(request)
        _assert_coefficient(
            signal,
            record,
            request,
            self.policy,
            self.frames[origin],
            rows,
            det,
            condition,
            vector,
            now,
        )
        self.coefficients[signal] = record
        return self.actual_coefficient(signal)

    def produce_triplet(self):
        for sig in COMPONENTS:
            self.produce_coefficient(sig)
        return self.triplet()

    def triplet(self):
        values = tuple(self.actual_coefficient(sig) for sig in COMPONENTS)
        assert tuple(x.derived_signal_id for x in values) == tuple(COMPONENTS)
        assert len({x.derived_occurrence_id for x in values}) == 3
        assert len({x.fit.fit_id for x in values}) == 1
        assert len({_fit_bytes(x.fit) for x in values}) == 1
        assert tuple(x.component for x in values) == tuple(COMPONENTS.values())
        assert all(x.result == getattr(x.fit, x.component) for x in values)
        return values

    def assert_row(self, slot, row, ceiling):
        frame = self.frames[slot]
        assert len({x.derived_occurrence_id for x in row}) == 4
        assert tuple(x.derived_signal_id for x in row) == FIT_ROLES
        for signal, parent in zip(FIT_ROLES, row, strict=True):
            assert parent.request == _request(
                signal, self.policy, frame, parent.request.predecessor_occurrence_ids
            )
            assert parent.effective_as_of_utc == _dt(frame["as_of"])
            assert parent.knowledge_cutoff_utc == _dt(frame["row_cutoff"])
            assert parent.window_context == _context(frame)
            assert parent.window_seconds == frame["window_seconds"]
            assert parent.knowledge_cutoff_utc <= ceiling and parent.calculated_at_utc <= ceiling
            assert _parent_bytes(parent) == _parent_bytes(self.actual(signal, slot))
        _shared(row, slot)

    def assert_corpus(self, rows):
        # Establish one whole admitted corpus using every full actual original
        # and projection, not label/hash-only or per-row independent membership.
        literal = {(m["slot"], m["subject"], m["role"]): m["observation"] for m in self.members}
        seen, ids = set(), set()
        for slot, row in rows.items():
            for parent in _shared(row, slot):
                subject = parent.request.subject_instrument
                assert len(parent.original_observations) == len(parent.selected_projections) == 2
                for role, original, projection in zip(
                    ROLES, parent.original_observations, parent.selected_projections, strict=True
                ):
                    key = (slot, subject, role)
                    assert key not in seen and original.observation_occurrence_id not in ids
                    seen.add(key)
                    ids.add(original.observation_occurrence_id)
                    _assert_original(original, literal[key])
                    _assert_projection(projection, literal[key], role)
        expected = {key for key in literal if key[0] in rows}
        assert seen == expected and len(seen) == len(ids) == 10 * len(rows)

    def assert_applicable(self, triplet, current, cutoff):
        self.assert_row("S7", current, cutoff)
        fit = triplet[0].fit
        full = dict(zip(fit.row_slots, fit.rows, strict=True))
        if "S7" in full:
            assert tuple(map(_parent_bytes, full["S7"])) == tuple(map(_parent_bytes, current))
        full["S7"] = current
        assert tuple(full) == tuple(f"S{i}" for i in range(1 if fit.origin_slot == "S6" else 2, 8))
        self.assert_corpus(full)

    def check_all(self):
        self.check_histories(tuple(f"S{i}" for i in range(8)))
        self.triplet()

    def drop_live(self):
        self.owners.clear()
        self.sources.clear()
        self.coefficient_owners.clear()


def _witness(path, policy, manifest, case, name):
    (specimen,) = [x for x in case["specimens"] if x["id"] == name]
    setup = case["setup_and_reached_preconditions"]
    if len(case["specimens"]) == 2:
        setup = setup["actual_" + name]
    return Witness(path, policy, manifest, specimen, setup)


def _residual_content(record):
    content = _fields(record)
    for key in ("request", "parameter_set", "input_selection_policy", "window_context"):
        content[key] = _fields(content[key])
    content["current_histories"] = tuple(_parent_bytes(x) for x in record.current_histories)
    content["coefficients"] = tuple(_coefficient_bytes(x) for x in record.coefficients)
    return content


def _residual_bytes(record):
    return _envelope("AlignedResidualOccurrenceV1", _residual_content(record))


def _assert_residual(record, request, policy, frame, current, coeffs, expected, now):
    p = policy["profiles"]["D078"]
    fields_expected = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/aligned_history/v1",
        implementation_brief_sha256=PINS["D078"][0],
        derived_signal_id="D078",
        derived_occurrence_id=record.derived_occurrence_id,
        request=request,
        definition=_definition("D078", policy),
        source_policy_sha256=POLICY_SHA,
        source_profile_ref=_ref(p["profile_ref"]),
        parameter_set=_parameter(p),
        input_selection_policy=_selection(p),
        window_context=_context(frame),
        current_histories=current,
        coefficients=coeffs,
        result=_er(expected),
        units="return",
        result_shape="exact_ratio",
        effective_as_of_utc=request.as_of_utc,
        knowledge_cutoff_utc=request.knowledge_cutoff_utc,
        calculated_at_utc=now,
    )
    _compare_fields(record, fields_expected, f.AlignedResidualOccurrenceV1)
    assert tuple(map(_parent_bytes, record.current_histories)) == tuple(map(_parent_bytes, current))
    assert tuple(map(_coefficient_bytes, record.coefficients)) == tuple(
        map(_coefficient_bytes, coeffs)
    )
    content = _residual_content(record)
    content.pop("derived_occurrence_id")
    content.pop("calculated_at_utc")
    assert record.derived_occurrence_id == "mmtaresidual1:" + _sha_bytes(
        _envelope("AlignedResidualOccurrenceV1", content)
    )


def _list_residual(reader, now):
    return reader.list_derived_history(
        derived_signal_id="D078",
        subject_instrument="NVDA",
        effective_at_or_before_utc=now,
        knowledge_at_or_before_utc=now,
        limit=10,
    )


def _execute_residual(tmp_path, policy, case, witnesses, current_witness, current, coeffs):
    # Request data consists only of actual read-back IDs and admitted metadata.
    # The five tests supply their exact distinct current and coefficient choices.
    variation = case["request_and_exact_variation"]
    frame = current_witness.frames["S7"]
    cutoff, asof, now = (_dt(variation[k]) for k in ("knowledge_cutoff", "as_of", "now"))
    assert variation["derived_signal_id"] == "D078" and variation["current_slot"] == "S7"
    assert asof == _dt(frame["as_of"]) and now >= cutoff
    assert tuple(x.derived_signal_id for x in current) == FIT_ROLES
    assert tuple(x.derived_signal_id for x in coeffs) == tuple(COMPONENTS)
    for entry, row in zip(variation["current_ids"], current, strict=True):
        assert entry["identity"] == IDENTITY and entry["signal"] == row.derived_signal_id
        assert entry["slot"] == row.request.slot
        assert _parent_bytes(row) == _parent_bytes(
            current_witness.actual(entry["signal"], entry["slot"])
        )
    coefficient_storages = []
    for entry, record in zip(variation["coefficient_ids"], coeffs, strict=True):
        assert entry["identity"] == IDENTITY and entry["signal"] == record.derived_signal_id
        assert entry["fit_origin"] == record.fit.origin_slot
        source = witnesses[entry["actual_fit_specimen"]]
        assert _coefficient_bytes(record) == _coefficient_bytes(
            source.actual_coefficient(entry["signal"])
        )
        coefficient_storages.append(source.storages[entry["signal"]])
    assert all(record.knowledge_cutoff_utc <= cutoff for record in coeffs)
    assert all(record.calculated_at_utc <= now for record in coeffs)
    ids = tuple(x.derived_occurrence_id for x in (*current, *coeffs))
    assert len(ids) == len(set(ids)) == 7
    stores = (*tuple(current_witness.storages[sig] for sig in FIT_ROLES), *coefficient_storages)
    assert len(stores) == 7 and len(set(stores)) == 7
    p = policy["profiles"]["D078"]
    request = f.AlignedResidualRequestV1(
        derived_signal_id="D078",
        subject_instrument=p["subject"],
        slot="S7",
        as_of_utc=asof,
        knowledge_cutoff_utc=cutoff,
        calculation_definition_version=p["calculation_definition_version"],
        source_profile_ref=_ref(p["profile_ref"]),
        parameter_set_ref=_ref(p["parameter_ref"]),
        input_selection_policy_ref=_ref(p["selection_ref"]),
        context_refs=(_context(frame).ref,),
        predecessor_occurrence_ids=ids,
    )
    for witness in witnesses.values():
        witness.check_all()
    db = tmp_path / "residual.sqlite"
    clock = [now]
    owner = f.create_aligned_residual_owner(
        admission=_admission("D078"),
        predecessor_read_storages=stores,
        storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    assert _list_residual(owner.reads, now) == ()
    record = owner.materialise(request)
    oracle = case["independent_oracle"]
    if case["kind"] == "SUCCESS":
        # Independently evaluate actual named coefficient results and common
        # intercept against actual current row; compare pinned independent ratio.
        target, market, tech, semi = (_ratio(x.result) for x in current)
        alpha = _ratio(coeffs[0].fit.intercept)
        beta = tuple(_ratio(x.result) for x in coeffs)
        expected = target - (alpha + beta[0] * market + beta[1] * tech + beta[2] * semi)
        assert expected == Fraction(*oracle["actual_residual_ratio"])
        assert expected / _fit_a() == Fraction(*oracle["normalized_residual"]) == Fraction(5, 2)
        assert expected != 0 and oracle["actual_rows"] == 1
        assert type(record) is f.AlignedResidualOccurrenceV1
        _assert_residual(record, request, policy, frame, current, coeffs, expected, now)
        first = _residual_bytes(record)
        assert (
            _residual_bytes(owner.reads.get_derived_occurrence(record.derived_occurrence_id))
            == first
        )
        assert tuple(map(_residual_bytes, _list_residual(owner.reads, now))) == (first,)
        clock[0] = _dt(variation["later_replay_now"])
        assert clock[0] > now
        assert _residual_bytes(owner.materialise(request)) == first
        assert tuple(map(_residual_bytes, _list_residual(owner.reads, clock[0]))) == (first,)
    else:
        assert oracle["actual_rows"] == 0
        assert record is None
        assert _list_residual(owner.reads, now) == ()
    # No live residual/parent writers, sources or original store locations are
    # available to the ordinary reopened residual reader. Restore only test-owned
    # temporary directories to verify every parent remains byte-identical.
    del owner
    detached = []
    for witness in witnesses.values():
        witness.check_all()
        witness.drop_live()
        moved = witness.path.with_name(witness.path.name + "-detached")
        witness.path.rename(moved)
        detached.append((moved, witness.path))
    try:
        reader = f.create_aligned_residual_reader(
            admission=_admission("D078"), storage=f.SQLiteReadStorageV1(str(db))
        )
        if case["kind"] == "SUCCESS":
            reread = reader.get_derived_occurrence(record.derived_occurrence_id)
            assert _residual_bytes(reread) == first
            _assert_residual(reread, request, policy, frame, current, coeffs, expected, now)
            assert tuple(map(_residual_bytes, _list_residual(reader, clock[0]))) == (first,)
        else:
            assert _list_residual(reader, now) == ()
    finally:
        for moved, original in detached:
            moved.rename(original)
    for witness in witnesses.values():
        witness.check_all()


def _cutoff(case):
    return _dt(case["request_and_exact_variation"]["knowledge_cutoff"])


def _prior_available(triplet, current, cutoff):
    assert all(
        x.fit.origin_slot == "S6" and x.fit.effective_as_of_utc < current[0].effective_as_of_utc
        for x in triplet
    )
    assert all(
        x.fit.knowledge_cutoff_utc <= cutoff
        and x.knowledge_cutoff_utc <= cutoff
        and x.calculated_at_utc <= cutoff
        for x in triplet
    )


def test_d078_same_fit_residual(tmp_path):
    policy, manifest, case = _case("D078-CONTROLLED-SUCCESS")
    assert case["expected_stage"] == "SAME_PRIOR_FIT_RESIDUAL_AND_DURABLE_REOPEN"
    a = _witness(tmp_path / "A", policy, manifest, case, "A")
    a.produce_declared()
    triplet = a.produce_triplet()
    a.produce_current()
    current = a.row("S7")
    _prior_available(triplet, current, _cutoff(case))
    a.assert_applicable(triplet, current, _cutoff(case))
    _execute_residual(tmp_path, policy, case, {"A": a}, a, current, triplet)


def test_d078_mixed_fit(tmp_path):
    policy, manifest, case = _case("D078-CONTROLLED-REACHED_REFUSAL")
    assert case["expected_stage"] == "SAME_FIT_ID_AND_EXACT_MANIFEST"
    a = _witness(tmp_path / "A", policy, manifest, case, "A")
    b = _witness(tmp_path / "B", policy, manifest, case, "B")
    a.produce_declared()
    triplet_a = a.produce_triplet()
    b.produce_declared()
    triplet_b = b.produce_triplet()
    a.produce_current()
    b.produce_current()
    current = a.row("S7")
    current_b = b.row("S7")
    assert tuple(map(_parent_bytes, current)) == tuple(map(_parent_bytes, current_b))
    for sig in HISTORY_SIGNALS:
        assert _parent_bytes(a.actual(sig, "S7")) == _parent_bytes(b.actual(sig, "S7"))
    la = {(x["slot"], x["subject"], x["role"]): x for x in a.members}
    lb = {(x["slot"], x["subject"], x["role"]): x for x in b.members}
    assert set(la) == set(lb)
    assert [key for key in la if la[key] != lb[key]] == [("S1", "NVDA", "R037")]
    assert (
        la[("S1", "NVDA", "R037")]["observation"]["observation_occurrence_id"]
        != lb[("S1", "NVDA", "R037")]["observation"]["observation_occurrence_id"]
    )
    for triplet, witness in ((triplet_a, a), (triplet_b, b)):
        _prior_available(triplet, current, _cutoff(case))
        witness.assert_applicable(triplet, current, _cutoff(case))
    fa, fb = triplet_a[0].fit, triplet_b[0].fit
    assert fa.fit_id != fb.fit_id and _fit_bytes(fa) != _fit_bytes(fb)
    assert (
        fa.origin_slot,
        fa.effective_as_of_utc,
        fa.knowledge_cutoff_utc,
        fa.condition,
        fa.fit_profile_ref,
        fa.source_policy_sha256,
        fa.model_version,
        fa.numeric_version,
    ) == (
        fb.origin_slot,
        fb.effective_as_of_utc,
        fb.knowledge_cutoff_utc,
        fb.condition,
        fb.fit_profile_ref,
        fb.source_policy_sha256,
        fb.model_version,
        fb.numeric_version,
    )
    mixed = (*triplet_a[:2], triplet_b[2])
    assert tuple(x.fit.fit_id for x in mixed) == (fa.fit_id, fa.fit_id, fb.fit_id)
    assert mixed[2].derived_occurrence_id != triplet_a[2].derived_occurrence_id
    _execute_residual(tmp_path, policy, case, {"A": a, "B": b}, a, current, mixed)


def test_d078_wrong_current_row(tmp_path):
    policy, manifest, case = _case("D078-CURRENT-ROW-MISALIGNMENT")
    assert case["expected_stage"] == "CURRENT_ROW_ALIGNMENT_AND_AVAILABILITY"
    a = _witness(tmp_path / "A", policy, manifest, case, "A")
    a.produce_declared()
    triplet = a.produce_triplet()
    a.produce_current()
    current = a.row("S7")
    _prior_available(triplet, current, _cutoff(case))
    a.assert_applicable(triplet, current, _cutoff(case))
    wrong = a.actual("D076", "S6")
    assert wrong.derived_occurrence_id != current[2].derived_occurrence_id
    assert wrong.derived_signal_id == "D076" and wrong.request.slot == "S6"
    assert wrong.knowledge_cutoff_utc <= _cutoff(case) and wrong.calculated_at_utc <= _cutoff(case)
    actual = (*current[:2], wrong, current[3])
    assert tuple(
        i
        for i, (x, y) in enumerate(zip(actual, current, strict=True))
        if _parent_bytes(x) != _parent_bytes(y)
    ) == (2,)
    _execute_residual(tmp_path, policy, case, {"A": a}, a, actual, triplet)


def test_d078_nonprior_fit(tmp_path):
    policy, manifest, case = _case("D078-NONPRIOR-FIT")
    assert case["expected_stage"] == "FIT_ORIGIN_STRICT_PRIOR"
    c = _witness(tmp_path / "C", policy, manifest, case, "C_NONPRIOR")
    c.produce_declared()  # includes the current S7 before the fit
    current = c.row("S7")
    triplet = c.produce_triplet()
    fit = triplet[0].fit
    assert fit.origin_slot == "S7" and fit.effective_as_of_utc == current[0].effective_as_of_utc
    assert fit.row_slots == tuple(f"S{i}" for i in range(2, 8))
    assert (
        _ratio(fit.determinant) == 164
        and _ratio(fit.condition)
        == Fraction(*case["independent_oracle"]["condition"])
        == Fraction(1664, 41)
        <= 50
    )
    assert all(
        x.knowledge_cutoff_utc <= _cutoff(case) and x.calculated_at_utc <= _cutoff(case)
        for x in triplet
    )
    assert fit.knowledge_cutoff_utc <= _cutoff(case)
    c.assert_applicable(triplet, current, _cutoff(case))
    _execute_residual(tmp_path, policy, case, {"C_NONPRIOR": c}, c, current, triplet)


def test_d078_coefficient_unavailable_at_cutoff(tmp_path):
    policy, manifest, case = _case("D078-COEFFICIENT-NOT-KNOWN-AT-RESIDUAL-CUTOFF")
    assert case["expected_stage"] == "COEFFICIENT_AVAILABILITY"
    a = _witness(tmp_path / "A", policy, manifest, case, "A")
    a.produce_declared()
    a.produce_coefficient("D079")
    a.produce_coefficient("D080")
    assert "D081" not in a.coefficients and "D081" not in a.coefficient_owners
    a.produce_current()
    current = a.row("S7")
    a.produce_coefficient("D081")  # actual first calculation, no earlier call/replay
    triplet = a.triplet()
    cutoff = _cutoff(case)
    now = _dt(case["request_and_exact_variation"]["now"])
    oracle = case["independent_oracle"]
    assert all(
        x.fit.origin_slot == "S6" and x.fit.effective_as_of_utc < current[0].effective_as_of_utc
        for x in triplet
    )
    assert all(
        x.fit.knowledge_cutoff_utc <= cutoff and x.knowledge_cutoff_utc <= cutoff for x in triplet
    )
    assert all(x.calculated_at_utc <= now for x in triplet)
    assert (
        tuple(x.derived_signal_id for x in triplet if x.calculated_at_utc > cutoff)
        == (oracle["actual_late_component"],)
        == ("D081",)
    )
    assert (
        triplet[2].calculated_at_utc == _dt(oracle["actual_component_first_calculated_at"]) == now
    )
    assert cutoff == _dt(oracle["actual_residual_cutoff"]) < now
    a.assert_applicable(triplet, current, cutoff)
    _execute_residual(tmp_path, policy, case, {"A": a}, a, current, triplet)
