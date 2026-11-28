"""Inert D079 joint-fit proof authoring candidate; NOT installed or released.

Future physical path: tests/product/m02_completion_28_prospective/d079/test_signal.py.
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
LEGAL = ("A", "B", "RANK", "COND", "C_NONPRIOR")

SIGNAL = "D079"
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
}
CASE_HASHES = {
    "D079-CONTROLLED-SUCCESS": "34d051b8286bf1e661a4009925f04f7431fbfc7143d9c0d480d313025c2a5496",
    "D079-CONTROLLED-REACHED_REFUSAL": "eaa15b1f00aed22c9499a258b142df0408ff7a7a584a7b382f22b76806013fcc",
    "D079-MISSING-MEMBER": "41740cc9d60f398a0d1662455832899b5042bc2c7453491edd97c7b5d689cdd9",
    "D079-DUPLICATE-MEMBER": "d012eb1d13bfc6bda3990cb3972c96133dc161eb57853f7a51a0c72722b22f2d",
    "D079-PARENT-NOT-KNOWN-AT-FIT-CUTOFF": "0c58e54a4dc0335460c5724ee3be00906fb2e16243273bab1ccf05856de81689",
    "D079-MIXED-SOURCE-CORPUS": "7cd43201348673e71b755b475a8efe7bc8b6c26343c305b6c54476cfa569ada6",
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


# Proposed common fixture and exact public fit seam. No product calls at module import.


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


# Independent encoding of the pinned native public carrier representation.
# Do not import the product's private identity/codec helpers.
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


class Histories:
    """Exact case inputs only; actual sealed sources, fresh separate owners and stores."""

    def __init__(self, path, policy, manifest, case):
        self.path = path
        path.mkdir()
        self.policy, self.manifest, self.case = policy, manifest, case
        self.frames = {frame["slot"]: frame for frame in manifest["frames"]}
        self.owners, self.clocks, self.storages, self.rows = {}, {}, {}, {}
        self.source_facts, self.members = {}, {}
        self.specs, self.signals, self.slots = {}, {}, {}
        setup = case["setup_and_reached_preconditions"]
        if "history_producer_slots_by_specimen" in setup:
            by_spec = setup["history_producer_slots_by_specimen"]
        else:
            (spec,) = case["specimens"]
            by_spec = {spec["id"]: setup["history_producer_slots"]}
        self.digests = {s["id"]: s["expanded_sha256"] for s in case["specimens"]}
        for specimen, roles in by_spec.items():
            for signal, slots in roles.items():
                self._declare(specimen + "_" + signal, specimen, signal, slots)
        alt = setup.get("additional_history_producer")
        if alt:
            self._declare(alt["store"], alt["source"], alt["signal"], alt["slots"])
        for key, signal in self.signals.items():
            if signal not in ("D076", "D077"):
                self._create_underlying(key)

    def _declare(self, key, specimen, signal, slots):
        assert key not in self.signals
        self.specs[key], self.signals[key], self.slots[key] = specimen, signal, tuple(slots)
        self.rows[key] = {}
        self.clocks[key] = [
            datetime.fromisoformat(self.frames["S0"]["default_underlying_calculated_at"])
        ]
        self.storages[key] = f.SQLiteReadStorageV1(str(self.path / (key + ".sqlite")))

    def _create_underlying(self, key):
        signal, specimen = self.signals[key], self.specs[key]
        members = _expand(self.manifest, specimen, self.digests[specimen])
        source = f.create_aligned_history_source(admission=_admission(signal), specimen_id=specimen)
        self.members[key] = members
        self.source_facts[key] = _source_evidence(source, members, specimen, self.digests[specimen])
        self.owners[key] = f.create_aligned_history_owner(
            admission=_admission(signal),
            source=source,
            predecessor_read_storages=(),
            storage=f.SQLiteStorageV1(str(self.path / (key + ".sqlite")), True),
            utc_now=lambda key=key: self.clocks[key][0],
        )
        # Verify source-selected exact literal pairs and public temporal history before use.
        subject = self.policy["profiles"][signal]["subject"]
        for frame in self.frames.values():
            for role in ROLES:
                (pair,) = _pairs(members, self.source_facts[key], frame, role, subject)
                _role(pair, frame, role, subject)
                visible = _visible(
                    source,
                    members,
                    self.source_facts[key],
                    role,
                    datetime.fromisoformat(frame["as_of"]),
                    datetime.fromisoformat(frame["row_cutoff"]),
                    subject,
                )
                assert _exact(pair[1]) in tuple(_exact(item) for item in visible)

    def reader(self, key):
        return f.create_aligned_history_reader(
            admission=_admission(self.signals[key]), storage=self.storages[key]
        )

    def actual(self, key, slot):
        original = self.rows[key][slot]
        read = self.reader(key).get_derived_occurrence(original.derived_occurrence_id)
        assert type(read) is f.AlignedHistoryOccurrenceV1
        assert _parent_bytes(read) == _parent_bytes(original)
        _assert_parent_id(read)
        return read

    def _time(self, key, frame, relative):
        setup = self.case["setup_and_reached_preconditions"]
        slot, signal = frame["slot"], self.signals[key]
        delayed = setup.get("only_delayed_parent", {})
        if (signal, slot) == (delayed.get("signal"), delayed.get("slot")):
            return datetime.fromisoformat(delayed["actual_first_calculated_at"])
        alt = setup.get("additional_history_producer", {})
        if key == alt.get("store") and slot in alt["normal_first_times_except"]:
            return datetime.fromisoformat(alt["normal_first_times_except"][slot])
        name = "default_relative_calculated_at" if relative else "default_underlying_calculated_at"
        return datetime.fromisoformat(frame[name])

    def produce(self, slot, later=False):
        frame = self.frames[slot]
        # Actual chronological within-frame operation order. All five underlying
        # producers precede the relative producers; alternate D071 S3 is +3.
        for key, signal in self.signals.items():
            if signal in ("D076", "D077") or (not later and slot not in self.slots[key]):
                continue
            assert slot not in self.rows[key]
            specimen = self.specs[key]
            subject = self.policy["profiles"][signal]["subject"]
            pairs = tuple(
                _pairs(self.members[key], self.source_facts[key], frame, role, subject)[0]
                for role in ROLES
            )
            now = self._time(key, frame, False)
            self.clocks[key][0] = now
            request = _request(signal, self.policy, frame)
            result = self.owners[key].materialise(request)
            expected = _log_oracle(pairs, self.manifest, specimen, signal, slot)
            _row(result, signal, self.policy, frame, request, now, expected, pairs)
            self.rows[key][slot] = result
            self.actual(key, slot)
        for key, signal in self.signals.items():
            if signal not in ("D076", "D077") or (not later and slot not in self.slots[key]):
                continue
            assert slot not in self.rows[key]
            roles = ("D072", "D071") if signal == "D076" else ("D073", "D074", "D072")
            keys = tuple(self.specs[key] + "_" + role for role in roles)
            parents = tuple(self.actual(parent, slot) for parent in keys)
            now = self._time(key, frame, True)
            assert all(parent.calculated_at_utc <= now for parent in parents)
            self.clocks[key][0] = now
            if key not in self.owners:
                self.owners[key] = f.create_aligned_history_owner(
                    admission=_admission(signal),
                    source=None,
                    predecessor_read_storages=tuple(self.storages[p] for p in keys),
                    storage=f.SQLiteStorageV1(str(self.path / (key + ".sqlite")), True),
                    utc_now=lambda key=key: self.clocks[key][0],
                )
            request = _request(
                signal,
                self.policy,
                frame,
                tuple(parent.derived_occurrence_id for parent in parents),
            )
            result = self.owners[key].materialise(request)
            values = tuple(_ratio(parent.result) for parent in parents)
            expected = (
                values[0] - values[1]
                if signal == "D076"
                else (values[0] + values[1]) / 2 - values[2]
            )
            independent = self.manifest["oracle_only_not_inputs"]["complete_legal_row_oracles"][
                self.specs[key]
            ][slot]["exact_fraction_values_D071_through_D077"][int(signal[1:]) - 71]
            assert expected == Fraction(*independent)
            _row(result, signal, self.policy, frame, request, now, _er(expected), parents=parents)
            self.rows[key][slot] = result
            self.actual(key, slot)

    def check_all(self, later=False):
        for key, signal in self.signals.items():
            expected = (*self.slots[key], "S7") if later else self.slots[key]
            assert tuple(self.rows[key]) == expected
            reader = self.reader(key)
            _history(reader, signal, self.policy, list(self.frames.values()), self.rows[key])
            for slot in expected:
                self.actual(key, slot)


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


def _shared(row, slot, mismatch=False):
    target, spy, tech, semi = row
    assert tuple(x.derived_signal_id for x in row) == FIT_ROLES
    assert tuple(x.derived_signal_id for x in tech.predecessors) == ("D072", "D071")
    assert tuple(x.derived_signal_id for x in semi.predecessors) == ("D073", "D074", "D072")
    qqq, nested_spy = tech.predecessors
    smh, soxx, nested_qqq = semi.predecessors
    for left, right in ((spy, nested_spy), (qqq, nested_qqq)):
        assert left.derived_occurrence_id == right.derived_occurrence_id
        if mismatch and slot == "S3" and left is spy:
            assert _parent_bytes(left) != _parent_bytes(right)
            l, r = _parent_content(left), _parent_content(right)
            assert l.pop("calculated_at_utc") == datetime.fromisoformat("2026-10-16T12:40:03Z")
            assert r.pop("calculated_at_utc") == datetime.fromisoformat("2026-10-16T12:40:02Z")
            assert _envelope("AlignedHistoryOccurrenceV1", l) == _envelope(
                "AlignedHistoryOccurrenceV1", r
            )
        else:
            assert _parent_bytes(left) == _parent_bytes(right)
    return (target, spy, qqq, smh, soxx)


def _full_sample(rows, slots, histories, cutoff, *, delayed=False, mismatch=False, mixed=False):
    assert len(rows) == len(slots) == 6
    assert len({p.derived_occurrence_id for row in rows for p in row}) == 24
    memberships = {}
    seen_facts = set()
    original_ids = set()
    for slot, row in zip(slots, rows, strict=True):
        frame = histories.frames[slot]
        for sig, p in zip(FIT_ROLES, row, strict=True):
            assert p.derived_signal_id == sig and p.request.slot == slot
            assert p.request == _request(
                sig, histories.policy, frame, p.request.predecessor_occurrence_ids
            )
            assert p.definition == _definition(sig, histories.policy)
            assert p.source_profile_ref == _ref(histories.policy["profiles"][sig]["profile_ref"])
            assert p.effective_as_of_utc == datetime.fromisoformat(frame["as_of"])
            assert p.knowledge_cutoff_utc == datetime.fromisoformat(frame["row_cutoff"])
            assert (
                p.window_context == _context(frame) and p.window_seconds == frame["window_seconds"]
            )
            assert p.knowledge_cutoff_utc <= cutoff
            if delayed and (sig, slot) == ("D077", "S6"):
                assert p.calculated_at_utc == cutoff + timedelta(seconds=2)
            else:
                assert p.calculated_at_utc <= cutoff
        underlying = _shared(row, slot, mismatch)
        assert len({p.derived_occurrence_id for p in underlying}) == 5
        sets = _corpus_sets(histories.manifest, underlying, frame)
        assert len(sets) == 10
        for parent in underlying:
            for original in parent.original_observations:
                key = (
                    slot,
                    parent.request.subject_instrument,
                    str(original.raw_signal_catalogue_ids[0].value),
                )
                assert key not in seen_facts
                seen_facts.add(key)
                original_ids.add(original.observation_occurrence_id)
        memberships[slot] = set.intersection(*sets)
        assert memberships[slot]
    assert len(seen_facts) == len(original_ids) == 60
    common = set.intersection(*memberships.values())
    if mixed:
        assert not common
        assert memberships == {
            k: set(v)
            for k, v in histories.case["independent_oracle"]["actual_per_row_legal_corpora"].items()
        }
    else:
        assert common


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


def _assert_coefficient(occurrence, request, policy, frame, rows, det, condition, vector, now):
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
    p = policy["profiles"][SIGNAL]
    component = COMPONENTS[SIGNAL]
    expected = dict(
        owner_object_id="M02",
        owner_namespace="neutral_market_measurement_truth/aligned_history/v1",
        implementation_brief_sha256=PINS[SIGNAL][0],
        derived_signal_id=SIGNAL,
        derived_occurrence_id=occurrence.derived_occurrence_id,
        request=request,
        definition=_definition(SIGNAL, policy),
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


def _list_coefficients(reader, asof, cutoff):
    return reader.list_derived_history(
        derived_signal_id=SIGNAL,
        subject_instrument="NVDA",
        effective_at_or_before_utc=asof,
        knowledge_at_or_before_utc=cutoff,
        limit=10,
    )


def _run(tmp_path, case_id, stage):
    policy, manifest, case = _case(case_id)
    assert case["expected_stage"] == stage
    setup, variation = case["setup_and_reached_preconditions"], case["request_and_exact_variation"]
    assert tuple(setup["fit_row_roles"]) == FIT_ROLES
    slots = tuple(setup["requested_training_slots"])
    assert slots == tuple(f"S{i}" for i in range(1, 7))
    hist = Histories(tmp_path / "histories", policy, manifest, case)
    for slot in ("S0", *slots):
        hist.produce(slot)
    hist.check_all()
    actual_rows = []
    request_rows = []
    store_keys = None
    for row in variation["ordered_rows"]:
        slot = row["slot"]
        entries = row["member_ids"]
        assert tuple(e["signal"] for e in entries) == FIT_ROLES
        ids = []
        actual = []
        keys = []
        for e in entries:
            key = e.get("actual_read_store", case["specimens"][0]["id"] + "_" + e["signal"])
            assert hist.signals[key] == e["signal"]
            assert hist.specs[key] == e.get("actual_source_specimen", case["specimens"][0]["id"])
            keys.append(key)
            if e["identity"] == "ACTUAL_PUBLIC_GETTER_ID_AND_CANONICAL_PAYLOAD":
                p = hist.actual(key, e["slot"])
                ids.append(p.derived_occurrence_id)
                actual.append(p)
            else:
                assert stage == "PARENT_LOOKUP" and (slot, e["signal"]) == ("S3", "D077")
                assert e["identity"] == "mmtahistory1:" + "0" * 64
                assert e["slot"] not in hist.rows[key]
                assert hist.reader(key).get_derived_occurrence(e["identity"]) is None
                ids.append(e["identity"])
                actual.append(None)
        if store_keys is None:
            store_keys = tuple(keys)
        assert tuple(keys) == store_keys
        request_rows.append(f.AlignedFitRowRequestV1(slot=slot, member_occurrence_ids=tuple(ids)))
        actual_rows.append(tuple(actual))
    rows = tuple(actual_rows)
    assert tuple(row.slot for row in request_rows) == slots
    ids = tuple(identity for row in request_rows for identity in row.member_occurrence_ids)
    assert len(ids) == 24
    cutoff = datetime.fromisoformat(variation["cutoff"])
    asof = datetime.fromisoformat(variation["as_of"])
    now = datetime.fromisoformat(setup["fit_now"])
    assert variation["origin"] == "S6" and cutoff == asof + timedelta(seconds=4) and now >= cutoff
    oracle = case["independent_oracle"]
    positive = case["kind"] == "SUCCESS"
    if stage == "PARENT_LOOKUP":
        assert len(set(ids)) == 24
        assert [(i, j) for i, row in enumerate(rows) for j, p in enumerate(row) if p is None] == [
            (2, 3)
        ]
        for i, row in enumerate(rows):
            for j, parent in enumerate(row):
                if parent is not None:
                    assert (
                        parent.request.slot == slots[i] and parent.derived_signal_id == FIT_ROLES[j]
                    )
                    assert parent.calculated_at_utc <= cutoff
        # Exact absent D077 S3 has its three lawful underlying parents in the actual stores.
        for sig in ("D073", "D074", "D072"):
            assert hist.actual("A_" + sig, "S3").calculated_at_utc <= cutoff
    elif stage in ("SAMPLE_MEMBER_ID_UNIQUENESS", "PARENT_ROW_ALIGNMENT"):
        correct = tuple(tuple(hist.actual(key, slot) for key in store_keys) for slot in slots)
        _full_sample(correct, slots, hist, cutoff)
        assert [
            (i, j)
            for i, row in enumerate(rows)
            for j, p in enumerate(row)
            if _parent_bytes(p) != _parent_bytes(correct[i][j])
        ] == [(2, 3)]
        if stage == "SAMPLE_MEMBER_ID_UNIQUENESS":
            assert len(set(ids)) == 23 and ids[11] == ids[7]
            assert _parent_bytes(rows[2][3]) == _parent_bytes(correct[1][3])
        else:
            assert len(set(ids)) == 24 and rows[2][3].request.slot == "S0"
            assert rows[2][3].calculated_at_utc <= cutoff
            assert rows[2][3].derived_occurrence_id != correct[2][3].derived_occurrence_id
    else:
        _full_sample(
            rows,
            slots,
            hist,
            cutoff,
            delayed=stage == "PARENT_AVAILABILITY",
            mismatch=stage == "SHARED_PARENT_PAYLOAD_IDENTITY",
            mixed=stage == "COMPLETE_ACTUAL_SOURCE_ROSTER",
        )
        det, condition, vector = _numeric(rows)
        if stage == "RANK":
            assert all(_ratio(row[3].result) == 0 for row in rows)
            assert det == Fraction(*oracle["determinant"]) == 0 and condition is None
        elif stage == "CONDITION":
            assert det == Fraction(*oracle["determinant"]) == 9
            assert condition == Fraction(*oracle["condition"]) == Fraction(208, 3) > 50
        elif stage == "COMPLETE_ACTUAL_SOURCE_ROSTER":
            assert det == 27 and condition == 50
            assert vector == (
                _fit_a() * Fraction(8, 27),
                Fraction(-11, 54),
                Fraction(7, 27),
                Fraction(-4, 9),
            )
        elif positive:
            assert det == (27 if stage == "CONDITION_INCLUSIVE_BOUNDARY_AND_DURABLE_REOPEN" else 51)
            assert condition == Fraction(*oracle["condition_ratio"]) <= 50
            assert vector == tuple(
                Fraction(*pair) for pair in oracle["actual_intercept_and_vector"]
            )
            assert vector[1 + tuple(COMPONENTS).index(SIGNAL)] == Fraction(
                *oracle["actual_component_ratio"]
            )
        else:
            assert det == 51 and condition == Fraction(1269, 34)
    profile = policy["profiles"][SIGNAL]
    request = f.AlignedFitRequestV1(
        derived_signal_id=SIGNAL,
        subject_instrument="NVDA",
        origin_slot="S6",
        as_of_utc=asof,
        knowledge_cutoff_utc=cutoff,
        calculation_definition_version=profile["calculation_definition_version"],
        source_profile_ref=_ref(profile["profile_ref"]),
        parameter_set_ref=_ref(profile["parameter_ref"]),
        input_selection_policy_ref=_ref(profile["selection_ref"]),
        context_refs=(_context(hist.frames["S6"]).ref,),
        rows=tuple(request_rows),
    )
    db = tmp_path / "coefficient.sqlite"
    clock = [now]
    owner = f.create_aligned_coefficient_owner(
        admission=_admission(SIGNAL),
        predecessor_read_storages=tuple(hist.storages[key] for key in store_keys),
        storage=f.SQLiteStorageV1(str(db), True),
        utc_now=lambda: clock[0],
    )
    result = owner.materialise(request)
    if positive:
        _assert_coefficient(
            result, request, policy, hist.frames["S6"], rows, det, condition, vector, now
        )
        assert _ratio(result.result) == Fraction(*oracle["actual_component_ratio"])
        first = _coefficient_bytes(result)
        assert tuple(
            _coefficient_bytes(x) for x in _list_coefficients(owner.reads, asof, cutoff)
        ) == (first,)
        assert (
            _coefficient_bytes(owner.reads.get_derived_occurrence(result.derived_occurrence_id))
            == first
        )
        # S7 must not be produced until after the first target call.
        hist.produce("S7", later=True)
        hist.check_all(later=True)
        clock[0] = datetime.fromisoformat(variation["later_replay_now"])
        assert _coefficient_bytes(owner.materialise(request)) == first
        assert tuple(
            _coefficient_bytes(x) for x in _list_coefficients(owner.reads, clock[0], clock[0])
        ) == (first,)
    else:
        assert result is None
        assert _list_coefficients(owner.reads, now, now) == ()
    # Preserve actual parents while proving coefficient reopen has no live producer
    # or current-store dependency. Rename only the test's own temporary directory.
    hist.check_all(later=positive)
    hist.owners.clear()
    del owner
    detached = tmp_path / "detached-histories"
    hist.path.rename(detached)
    try:
        reader = f.create_aligned_coefficient_reader(
            admission=_admission(SIGNAL), storage=f.SQLiteReadStorageV1(str(db))
        )
        if positive:
            reread = reader.get_derived_occurrence(result.derived_occurrence_id)
            assert _coefficient_bytes(reread) == first
            _assert_coefficient(
                reread, request, policy, hist.frames["S6"], rows, det, condition, vector, now
            )
            assert tuple(
                _coefficient_bytes(x) for x in _list_coefficients(reader, clock[0], clock[0])
            ) == (first,)
        else:
            assert _list_coefficients(reader, now, now) == ()
    finally:
        detached.rename(hist.path)
    hist.check_all(later=positive)


def test_d079_joint_success(tmp_path):
    _run(tmp_path, "D079-CONTROLLED-SUCCESS", "JOINT_FIT_AND_DURABLE_REOPEN")


def test_d079_rank_deficient(tmp_path):
    _run(tmp_path, "D079-CONTROLLED-REACHED_REFUSAL", "RANK")


def test_d079_missing_member(tmp_path):
    _run(tmp_path, "D079-MISSING-MEMBER", "PARENT_LOOKUP")


def test_d079_duplicate_member(tmp_path):
    _run(tmp_path, "D079-DUPLICATE-MEMBER", "SAMPLE_MEMBER_ID_UNIQUENESS")


def test_d079_parent_unavailable_at_cutoff(tmp_path):
    _run(tmp_path, "D079-PARENT-NOT-KNOWN-AT-FIT-CUTOFF", "PARENT_AVAILABILITY")


def test_d079_mixed_source_corpus(tmp_path):
    _run(tmp_path, "D079-MIXED-SOURCE-CORPUS", "COMPLETE_ACTUAL_SOURCE_ROSTER")
