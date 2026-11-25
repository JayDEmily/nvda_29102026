"""D109 exact eight owner-admitted scalar straddle cases.

Inert authoring only; never import, collect or execute as Worker.
Prospective physical path tests/product/m02_scalar_straddle_d109/test_signal.py.
Self-contained independent literal and field-comparison helpers adapted
from the accepted support source; no import or execution of that family.
Every named case directly constructs real public parents and uses the
ordinary durable readers; no injected derived records or hidden scenarios.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw

ROOT = Path(__file__).resolve().parents[3]
LEAF = "handoff/m02_completion_28_execution/L10c/"
POLICY_PATH = LEAF + "SCALAR_STRADDLE_SOURCE_POLICY_PROPOSED_20261125.json"
MANIFEST_PATH = LEAF + "SCALAR_STRADDLE_FINITE_SPECIMENS_PROPOSED_20261125.json"
BRIEF_PATH = LEAF + "SCALAR_STRADDLE_PREEDIT_DESIGN_AND_REVIEW_20261125.md"
POLICY_SHA = "279f1cd166ad0c11585c9776dc4a45b5d949946a513717c39f1dcc9a816e8561"
MANIFEST_SHA = "5e341ef9289f185d4ae9da53eaca9852735af632b17400a89a10508a114dd760"
BRIEF = "04697219c5d5057ac3884aceb09d754dc391a66f6ed4a425459c938c684b1d8d"
D087_BRIEF = "103777a517401fcb08099acb6fe7c915286499819c1f8f71da50c4bf71cc8468"
C1 = "controlled-nvda-c110-20261023"
C2 = "controlled-nvda-p110-20261023"
PROVIDER, VARIANT = "foundation-controlled-options", "option_snapshot_v1"
SCOPE = PROVIDER + "/" + VARIANT
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
ADMISSION = f.OwnerAdmissionV1("M02", BRIEF)
MID_ADMISSION = f.OwnerAdmissionV1("M02", D087_BRIEF)
META = (
    ("contract.id", ("contract", "id")),
    ("underlying.id", ("underlying", "id")),
    ("expiry.date", ("expiry", "date")),
    ("strike.key", ("strike", "key")),
    ("option.right", ("option", "right")),
    ("currency.code", ("currency", "code")),
    ("contract.multiplier", ("contract", "multiplier")),
    ("instrument.kind", ("instrument", "kind")),
    ("model.convention", ("model", "convention")),
    ("value.role", ("value", "role")),
)
MAPS = {
    rid: raw.RawSignalProjectionMappingV1(
        "mmt-" + rid.lower() + "-option", 1, raw.RawSignalCatalogueId(rid),
        PROVIDER, VARIANT, path, units, META,
    )
    for rid, path, units in (
        ("R034", ("quote", "bid"), "USD_per_share"),
        ("R035", ("quote", "ask"), "USD_per_share"),
        ("R112", ("model", "delta"), "delta_fraction"),
        ("R118", ("model", "underlying_price"), "USD_per_share"),
    )
}
ROLES = {
    "C1-bid": (C1, "R034", "option_bid"),
    "C1-ask": (C1, "R035", "option_ask"),
    "C2-bid": (C2, "R034", "option_bid"),
    "C2-ask": (C2, "R035", "option_ask"),
    "C1-delta": (C1, "R112", "model_delta"),
    "C2-delta": (C2, "R112", "model_delta"),
    "C1-spot": (C1, "R118", "model_underlying_price"),
}
MID_MAPS = (MAPS["R034"], MAPS["R035"])
MID_UNIT = f.UnitConventionVersionV1(
    "mmt-option-price", 1, "USD_per_share", "USD_per_share", Decimal("1"), Decimal("0"),
)
MID_CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-option-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
MID_DEFINITION = f.CalculationDefinitionV1(
    "D087", "D087-OPTION-SCALAR-1", "K02_ALGEBRA", "(bid+ask)/2",
    ("R034", "R035"), (), "P_BASIC", "option_premium", "exact_ratio",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
    ),
)
MID_POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d087-selection", 1,
    ("subject_instrument", "contract.id", "underlying.id", "expiry.date", "strike.key",
     "option.right", "currency.code", "contract.multiplier", "model.convention"),
    timedelta(seconds=60), timedelta(0), ("true_instant",), (),
    PROVIDER, VARIANT, SCOPE, 100, 1000,
)
DELTA_DEFINITION = f.CalculationDefinitionV1(
    "D091", "T01-D091-SCALAR-PAIR-DEF-V1", "K08_RULE_BUCKET_POLICY",
    "categorise(abs(exact signed R112 delta)) under D091-SYNTHETIC-TENTATIVE-V1",
    ("R112",), (), "P_RULE", "category", "category",
    (f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
     f.AuthorityArtifactRefV1(BRIEF_PATH, BRIEF)),
)


def _read_pinned(path: str, sha: str) -> dict:
    payload = (ROOT / path).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == sha
    return json.loads(payload)


def _digest(value: object) -> str:
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def _base_members() -> list[dict]:
    members = _read_pinned(POLICY_PATH, POLICY_SHA)["positive_source_specimen"]["members"]
    assert [member["member_id"] for member in members] == list(ROLES)
    return members


def _specimen(name: str, full_sha: str, core_sha: str) -> list[dict]:
    # Independent documentary expansion; never supply these records to the
    # source factory. It must admit its own exact authorised original facts.
    manifest = _read_pinned(MANIFEST_PATH, MANIFEST_SHA)
    rows = [row for row in manifest["specimens"] if row["specimen_id"] == name]
    assert len(rows) == 1
    spec = rows[0]
    members = copy.deepcopy(_base_members())
    for operation in spec["literal_operations"]:
        if operation["op"] == "append":
            members.append(copy.deepcopy(operation["member"]))
        else:
            indices = [
                i for i, member in enumerate(members)
                if member["member_id"] == operation["target_member_id"]
            ]
            assert len(indices) == 1
            if operation["op"] == "omit":
                members.pop(indices[0])
            else:
                assert operation["op"] == "replace"
                members[indices[0]] = copy.deepcopy(operation["member"])
    core = [
        member for member in members
        if member["observation"]["raw_signal_catalogue_ids"] != ["R118"]
    ]
    assert len(members) == spec["full_member_count"]
    assert len(core) == spec["core_member_count"]
    assert _digest(members) == spec["expanded_member_sha256"] == full_sha
    assert _digest(core) == spec["core_member_sha256"] == core_sha
    return members


def _native(value):
    if isinstance(value, dict):
        if set(value) == {"native_type", "text"}:
            assert value["native_type"] == "Decimal" and type(value["text"]) is str
            return Decimal(value["text"])
        return {key: _native(item) for key, item in value.items()}
    return value


def _exact(value):
    # Do not use Decimal equality for signed zero, exponent or NaN.
    if isinstance(value, Mapping):
        return ("mapping", tuple(sorted((key, _exact(v)) for key, v in value.items())))
    if type(value) in (tuple, list):
        return (type(value), tuple(_exact(v) for v in value))
    if type(value) is Decimal:
        return (Decimal, value.as_tuple())
    if is_dataclass(value) and not isinstance(value, type):
        return (type(value), tuple((field.name, _exact(getattr(value, field.name)))
                                   for field in fields(value)))
    return (type(value), value)


def _path(value, path):
    for key in path:
        value = value[key]
    return value


def _member(members: list[dict], label: str) -> dict:
    matches = [member for member in members if member["member_id"] == label]
    assert len(matches) == 1
    return matches[0]["observation"]


def _assert_original(actual, literal: dict) -> None:
    # Every outer field, including absent metadata, is compared against
    # independent literal content; never substitute an expected DTO for ingress.
    assert type(actual) is raw.RawObservationOccurrenceV1
    expected = {
        "concept_id": raw.concept_id(literal["concept_id"]),
        "contract_id": raw.contract_id(literal["contract_id"]),
        "observation_occurrence_id": raw.observation_occurrence_id(
            literal["observation_occurrence_id"]
        ),
        "delivery_artifact_ref": raw.delivery_artifact_ref(literal["delivery_artifact_ref"]),
        "source_provider": raw.provider_id(literal["source_provider"]),
        "native_record": _native(literal["native_record"]),
        "received_ts_utc": datetime.fromisoformat(literal["received_ts_utc"]),
        "ingestion_sequence_scope": raw.ingestion_sequence_scope(
            literal["ingestion_sequence_scope"]
        ),
        "raw_signal_catalogue_ids": tuple(
            raw.RawSignalCatalogueId(rid) for rid in literal["raw_signal_catalogue_ids"]
        ),
    }
    for field in fields(raw.RawObservationOccurrenceV1):
        value = expected.get(field.name, literal.get(field.name))
        assert _exact(getattr(actual, field.name)) == _exact(value), field.name


def _assert_projection(item, original, rid: str) -> None:
    # Compare every field of the actual M00 projection against the original
    # getter and the independently fixed mapping. In particular mapping units
    # are not taken as evidence of the original units.
    mapping = MAPS[rid]
    expected = {
        "raw_signal_catalogue_id": mapping.raw_signal_catalogue_id,
        "observation_occurrence_id": original.observation_occurrence_id,
        "projection_mapping_id": mapping.mapping_id,
        "projection_mapping_version": mapping.version,
        "source_provider": PROVIDER,
        "source_variant": VARIANT,
        "native_field_path": mapping.native_field_path,
        "native_value": _path(original.native_record, mapping.native_field_path),
        "native_units": mapping.native_units,
        "subject_instrument": original.subject_instrument,
        "source_temporal_kind": "true_instant",
        "source_timestamp_raw": "2026-10-20T12:40:00Z",
        "source_timezone_native": "UTC",
        "received_ts_utc": T,
        "ingestion_sequence": original.ingestion_sequence,
        "ingestion_sequence_scope": raw.ingestion_sequence_scope(SCOPE),
        "revision_vintage_native": None,
        "selection_identity": raw.RawSelectionIdentityV1(tuple(
            (key, _path(original.native_record, path)) for key, path in META
        )),
    }
    assert type(item) is raw.ProjectedRawValueV1
    assert {field.name for field in fields(item)} == set(expected)
    assert original.native_units == mapping.native_units
    for key, value in expected.items():
        assert _exact(getattr(item, key)) == _exact(value), key


def _source_pins(source, full_sha: str, core_sha: str) -> None:
    assert type(source) is f.ScalarStraddleSourceV1
    assert source.full_specimen_sha256 == full_sha
    assert source.core_manifest_sha256 == core_sha
    assert not hasattr(source, "commands")
    assert not hasattr(source, "admit_raw_observation_occurrence")


def _read_role(source, members, label):
    subject, rid, role = ROLES[label]
    literal = _member(members, label)
    oid = raw.observation_occurrence_id(literal["observation_occurrence_id"])
    original = source.get_raw_observation_occurrence(oid)
    _assert_original(original, literal)
    assert original.subject_instrument == subject
    assert original.native_record["value"]["role"] == role
    assert original.received_ts_utc == T
    assert original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId(rid), mappings=(MAPS[rid],),
        subject_instrument=subject, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    assert type(page) is raw.ProjectedRawHistoryPageV1
    assert page.next_cursor is None and len(page.items) == 1
    projection = page.items[0]
    _assert_projection(projection, original, rid)
    return original, projection


def _mid_parameter(contract):
    return f.CalculationParameterSetV1(
        "mmt-d087-" + ("c1" if contract == C1 else "c2") + "-controlled",
        1, "P_BASIC", contract, (contract,),
    )


def _mid_request(contract):
    param = _mid_parameter(contract)
    return f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D087", contract, T, CUTOFF, "D087-OPTION-SCALAR-1",
            f.VersionRefV1(param.context_id, 1),
            f.VersionRefV1("mmt-d087-selection", 1), (MID_CONTEXT.ref,),
            tuple(f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value, f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1("mmt-option-price", 1), contract,
            ) for mapping in MID_MAPS),
        ), MID_CONTEXT, (),
    )


def _delta_request(contract, core_sha):
    return f.ScalarD091RequestV1(
        derived_signal_id="D091", subject_instrument=contract, as_of_utc=T,
        knowledge_cutoff_utc=CUTOFF, calculation_definition_version="T01-D091-SCALAR-PAIR-DEF-V1",
        source_profile_ref=f.VersionRefV1("T01-L10C-R112-SCALAR-PAIR-V1", 1),
        rule_profile_ref=f.VersionRefV1("D091-SYNTHETIC-TENTATIVE-V1", 1),
        projection_mapping_ref=f.VersionRefV1("mmt-r112-option", 1),
        unit_convention_ref=f.VersionRefV1("mmt-option-delta", 1),
        core_manifest_sha256=core_sha,
    )


def _history_args(signal, contract):
    return dict(
        derived_signal_id=signal, subject_instrument=contract,
        effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10,
    )


def _assert_midpoint(result, request, original_pairs, expected_num):
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert type(result.result) is f.ExactRatioV1
    assert result.result == f.ExactRatioV1(expected_num, 1)
    assert result.request == request and result.definition == MID_DEFINITION
    contract = original_pairs[0][0].subject_instrument
    assert result.parameter_set == _mid_parameter(contract)
    assert result.input_selection_policy == MID_POLICY
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/window/v1"
    assert result.implementation_brief_sha256 == D087_BRIEF
    assert result.derived_signal_id == "D087" and result.derived_occurrence_id
    assert result.projection_mappings == MID_MAPS and result.unit_conventions == (MID_UNIT,)
    assert result.predecessors == () and result.window_seconds == 0
    assert result.units == "option_premium" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    expected = tuple(
        f.RawInputLineageV1(
            mapping.raw_signal_catalogue_id.value, original.observation_occurrence_id.value,
            f.VersionRefV1(mapping.mapping_id, 1), f.VersionRefV1("mmt-option-price", 1),
            projection, projection.native_value, T,
        )
        for mapping, (original, projection) in zip(MID_MAPS, original_pairs, strict=True)
    )
    assert _exact(result.raw_input_lineage) == _exact(expected)


def _assert_delta(result, request, original, projection, signed_text, label):
    assert type(result) is f.ScalarD091OccurrenceV1
    assert result.request == request and result.definition == DELTA_DEFINITION
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/d091/scalar/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.derived_signal_id == "D091" and result.derived_occurrence_id
    assert result.source_policy_sha256 == POLICY_SHA
    assert result.core_manifest_sha256 == request.core_manifest_sha256
    assert _exact(result.original_observation) == _exact(original)
    assert _exact(result.selected_projection) == _exact(projection)
    expected = Decimal(signed_text)
    assert _exact(original.native_record["model"]["delta"]) == _exact(expected)
    assert _exact(projection.native_value) == _exact(expected)
    assert _exact(result.signed_delta) == _exact(expected)
    assert type(result.result) is f.D091CategoryV1
    assert result.result == f.D091CategoryV1(label)
    assert result.units == result.result_shape == "category"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)


def _assert_readback(reader, result, signal, contract):
    assert _exact(reader.get_derived_occurrence(result.derived_occurrence_id)) == _exact(result)
    actual_history = reader.list_derived_history(**_history_args(signal, contract))
    assert _exact(actual_history) == _exact((result,))


def _assert_single_mutation(members, label, path, value):
    # Check all unaffected original facts, not just the manifest's hash or label.
    original = _base_members()
    expected = copy.deepcopy(original)
    target = _member(expected, label)
    changed = _member(members, label)
    assert target["observation_occurrence_id"] != changed["observation_occurrence_id"]
    assert target["delivery_artifact_ref"] != changed["delivery_artifact_ref"]
    target["observation_occurrence_id"] = changed["observation_occurrence_id"]
    target["delivery_artifact_ref"] = changed["delivery_artifact_ref"]
    parent = _path(target, path[:-1])
    assert parent[path[-1]] != value
    parent[path[-1]] = value
    assert expected == members


PAIR = "T01-L10C-NVDA-20261023-110"
STRADDLE_DEFINITION = f.CalculationDefinitionV1(
    "D109", "T01-D109-SCALAR-PAIR-DEF-V1", "K02_ALGEBRA",
    "call midpoint + put midpoint", (), ("D087", "D091"), "P_BASIC",
    "USD_per_share", "exact_ratio",
    (f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
     f.AuthorityArtifactRefV1(BRIEF_PATH, BRIEF)),
)


def _straddle_request(core_sha, call_mid, put_mid, call_delta, put_delta):
    return f.D109ScalarRequestV1(
        derived_signal_id="D109", subject_instrument=PAIR, as_of_utc=T,
        knowledge_cutoff_utc=CUTOFF,
        calculation_definition_version="T01-D109-SCALAR-PAIR-DEF-V1",
        core_manifest_sha256=core_sha,
        call_mid=call_mid, put_mid=put_mid, call_delta=call_delta, put_delta=put_delta,
    )


def _assert_straddle(result, request, rc, rp, sc, sp, originals):
    assert type(result) is f.D109ScalarOccurrenceV1
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/d109/scalar/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.derived_signal_id == "D109" and result.derived_occurrence_id
    assert _exact(result.request) == _exact(request)
    assert _exact(result.definition) == _exact(STRADDLE_DEFINITION)
    assert result.source_policy_sha256 == POLICY_SHA
    assert result.core_manifest_sha256 == request.core_manifest_sha256
    assert _exact(result.call_mid) == _exact(rc)
    assert _exact(result.put_mid) == _exact(rp)
    assert _exact(result.call_delta) == _exact(sc)
    assert _exact(result.put_delta) == _exact(sp)
    assert _exact(result.original_quotes) == _exact(originals)
    assert result.result == f.ExactRatioV1(5, 1)
    assert type(result.result) is f.ExactRatioV1
    assert result.units == "USD_per_share" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert {field.name for field in fields(result)} == {
        "owner_object_id", "owner_namespace", "implementation_brief_sha256",
        "derived_signal_id", "derived_occurrence_id", "request", "definition",
        "source_policy_sha256", "core_manifest_sha256", "call_mid", "put_mid",
        "call_delta", "put_delta", "original_quotes", "result", "units",
        "result_shape", "effective_as_of_utc", "knowledge_cutoff_utc", "calculated_at_utc",
    }


def _parent_only_members(members):
    rows = _read_pinned(MANIFEST_PATH, MANIFEST_SHA)["parent_only_specimens"]
    assert len(rows) == 1
    row = rows[0]
    assert row["specimen_id"] == "D087_PARENT_ONLY_FOREIGN_C1_ASK_V1"
    assert row["allowed_case_id"] == "D109-WRONG-QUOTE-LINEAGE"
    actual = row["literal_members"]
    assert row["member_count"] == len(actual) == 2
    assert _digest(actual) == row["member_sha256"] == (
        "e9643453cc84dc3c97cb6cab021f4cf5a773f8c61981d2d2ca4f7b65b81b8b53"
    )
    expected = copy.deepcopy(members[:2])
    assert [item["member_id"] for item in expected] == ["C1-bid", "C1-ask"]
    ask = expected[1]["observation"]
    ask["observation_occurrence_id"] = "T01-L10C-SCALAR-V1-FOREIGN-C1-ASK-02"
    ask["delivery_artifact_ref"] = "T01-L10C-SCALAR-D087-FOREIGN-C1-ASK-V1"
    assert actual == expected
    return actual


def _raw_ingress_literal(literal):
    # Construct the exact authorised parent-only original, never a projected
    # value or derived parent. M00 admits it through its actual public command.
    values = dict(literal)
    for key, factory in (
        ("concept_id", raw.concept_id), ("contract_id", raw.contract_id),
        ("observation_occurrence_id", raw.observation_occurrence_id),
        ("delivery_artifact_ref", raw.delivery_artifact_ref),
        ("source_provider", raw.provider_id),
        ("ingestion_sequence_scope", raw.ingestion_sequence_scope),
    ):
        values[key] = factory(values[key])
    values["native_record"] = _native(values["native_record"])
    values["received_ts_utc"] = datetime.fromisoformat(values["received_ts_utc"])
    values["raw_signal_catalogue_ids"] = tuple(
        raw.RawSignalCatalogueId(rid) for rid in values["raw_signal_catalogue_ids"]
    )
    return raw.RawObservationOccurrenceV1(**values)


def test_d109_controlled_success(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    originals = (c1_bid[0], c1_ask[0], c2_bid[0], c2_ask[0])
    clock = [NOW]
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    result = owner.materialise(request)
    _assert_straddle(result, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, result, "D109", PAIR)
    del owner
    clock[0] = NOW + timedelta(seconds=1)
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, False), utc_now=lambda: clock[0],
    )
    assert _exact(owner.materialise(request)) == _exact(result)
    del owner, mid_reader, delta_reader, source
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    reopened = reader.get_derived_occurrence(result.derived_occurrence_id)
    _assert_straddle(reopened, request, rc, rp, sc, sp, originals)
    _assert_readback(reader, result, "D109", PAIR)


def test_d109_call_same_bin_non_atm(tmp_path):
    full_sha = "26077105077381800fc66994ace01557120e68c4e6039e1d2cc69b00cd237115"
    core_sha = "34e648cd4b3b1ea8c210c5578060badcb49fc0e373fedc52f460dcc56e28ba32"
    members = _specimen("C60", full_sha, core_sha)
    _assert_single_mutation(
        members, "C1-delta", ("native_record", "model", "delta"),
        {"native_type": "Decimal", "text": "0.60"},
    )
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="C60")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.60", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )


def test_d109_put_same_bin_non_atm(tmp_path):
    full_sha = "494f1ac740e700aa3dcd998a76b1a8cdfb4c7d77dc6cf002c2990321b3866d3f"
    core_sha = "1e0e91f847f8cebf69c084ad7aa9b1e583d1e8a3fda51c2bb23e26e39ee2db3c"
    members = _specimen("P60", full_sha, core_sha)
    _assert_single_mutation(
        members, "C2-delta", ("native_record", "model", "delta"),
        {"native_type": "Decimal", "text": "-0.60"},
    )
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="P60")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.60", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )


def test_d109_missing_parent(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    missing = "mmtd091scalar1:" + "0" * 64
    assert missing != sp.derived_occurrence_id
    assert delta_reader.get_derived_occurrence(missing) is None
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, missing,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rp.derived_occurrence_id, sc.derived_occurrence_id, missing,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )


def test_d109_duplicate_parent(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rc.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rc.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert request.call_mid == request.put_mid
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 3
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )


def test_d109_wrong_slot(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    request = _straddle_request(
        core_sha, rp.derived_occurrence_id, rc.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rp.derived_occurrence_id, rc.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    assert _exact(mid_reader.get_derived_occurrence(request.call_mid)) == _exact(rp)
    assert _exact(mid_reader.get_derived_occurrence(request.put_mid)) == _exact(rc)
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )


def test_d109_wrong_core(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    # Actual C2 ATM parent from a different lawful core in the SAME delta store.
    alternate_full = "26077105077381800fc66994ace01557120e68c4e6039e1d2cc69b00cd237115"
    alternate_core = "34e648cd4b3b1ea8c210c5578060badcb49fc0e373fedc52f460dcc56e28ba32"
    alternate_members = _specimen("C60", alternate_full, alternate_core)
    _assert_single_mutation(
        alternate_members, "C1-delta", ("native_record", "model", "delta"),
        {"native_type": "Decimal", "text": "0.60"},
    )
    alternate = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="C60")
    _source_pins(alternate, alternate_full, alternate_core)
    changed_call = _read_role(alternate, alternate_members, "C1-delta")
    assert _exact(changed_call[1].native_value) == _exact(Decimal("0.60"))
    actual_put = _read_role(alternate, alternate_members, "C2-delta")
    assert _exact(actual_put) == _exact(put_original)
    del delta_reader
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=alternate,
        storage=f.SQLiteStorageV1(delta_path, False), utc_now=lambda: NOW,
    )
    alternate_request = _delta_request(C2, alternate_core)
    foreign = deltas.materialise(alternate_request)
    _assert_delta(foreign, alternate_request, *actual_put, "-0.50", "ABS_50_75")
    assert foreign.derived_occurrence_id != sp.derived_occurrence_id
    assert foreign.core_manifest_sha256 != core_sha
    for field in fields(sp):
        if field.name not in ("derived_occurrence_id", "request", "core_manifest_sha256"):
            assert _exact(getattr(foreign, field.name)) == _exact(getattr(sp, field.name))
    for field in fields(dp):
        if field.name != "core_manifest_sha256":
            assert _exact(getattr(alternate_request, field.name)) == _exact(getattr(dp, field.name))
    del deltas, alternate
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(delta_reader, sc, "D091", C1)
    assert _exact(delta_reader.get_derived_occurrence(sp.derived_occurrence_id)) == _exact(sp)
    assert _exact(delta_reader.get_derived_occurrence(foreign.derived_occurrence_id)) == (
        _exact(foreign)
    )
    put_history = delta_reader.list_derived_history(**_history_args("D091", C2))
    assert len(put_history) == 2
    assert {item.derived_occurrence_id for item in put_history} == {
        sp.derived_occurrence_id, foreign.derived_occurrence_id,
    }
    request = _straddle_request(
        core_sha, rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, foreign.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        rc.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, foreign.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )
    assert _exact(delta_reader.get_derived_occurrence(foreign.derived_occurrence_id)) == (
        _exact(foreign)
    )


def test_d109_wrong_quote_lineage(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_original = _read_role(source, members, "C1-delta")
    put_original = _read_role(source, members, "C2-delta")
    mid_path = str(tmp_path / "midpoints.sqlite")
    delta_path = str(tmp_path / "delta.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: NOW,
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: NOW,
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_original, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_original, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    del mids, deltas
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    delta_reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(delta_path),
    )
    _assert_readback(mid_reader, rc, "D087", C1)
    _assert_readback(mid_reader, rp, "D087", C2)
    _assert_readback(delta_reader, sc, "D091", C1)
    _assert_readback(delta_reader, sp, "D091", C2)
    # Exactly two separately admitted actual originals for the parent-only
    # specimen. Neither an arbitrary sealed source nor a fabricated parent.
    foreign_members = _parent_only_members(members)
    foreign_owner = raw.create_owner()
    bid_literal = _member(foreign_members, "C1-bid")
    ask_literal = _member(foreign_members, "C1-ask")
    admitted_bid = foreign_owner.commands.admit_raw_observation_occurrence(
        _raw_ingress_literal(bid_literal),
    )
    admitted_ask = foreign_owner.commands.admit_raw_observation_occurrence(
        _raw_ingress_literal(ask_literal),
    )
    _assert_original(admitted_bid, bid_literal)
    _assert_original(admitted_ask, ask_literal)
    foreign_bid = _read_role(foreign_owner.reads, foreign_members, "C1-bid")
    foreign_ask = _read_role(foreign_owner.reads, foreign_members, "C1-ask")
    assert _exact(foreign_bid) == _exact(c1_bid)
    assert _exact(foreign_ask[1].native_value) == _exact(c1_ask[1].native_value)
    assert foreign_ask[0].observation_occurrence_id != c1_ask[0].observation_occurrence_id
    assert foreign_ask[0].delivery_artifact_ref != c1_ask[0].delivery_artifact_ref
    for field in fields(c1_ask[0]):
        if field.name not in ("observation_occurrence_id", "delivery_artifact_ref"):
            assert _exact(getattr(foreign_ask[0], field.name)) == (
                _exact(getattr(c1_ask[0], field.name))
            )
    for field in fields(c1_ask[1]):
        if field.name != "observation_occurrence_id":
            assert _exact(getattr(foreign_ask[1], field.name)) == (
                _exact(getattr(c1_ask[1], field.name))
            )
    # Genuine D087 owner, same existing SQLite store and same lawful C1 request.
    del mid_reader
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=foreign_owner.reads,
        storage=f.SQLiteStorageV1(mid_path, False), utc_now=lambda: NOW,
    )
    foreign = mids.materialise(mc)
    _assert_midpoint(foreign, mc, (foreign_bid, foreign_ask), 3)
    assert foreign.derived_occurrence_id != rc.derived_occurrence_id
    assert _exact(foreign.raw_input_lineage[0]) == _exact(rc.raw_input_lineage[0])
    assert foreign.raw_input_lineage[1].observation_occurrence_id != (
        rc.raw_input_lineage[1].observation_occurrence_id
    )
    for field in fields(rc):
        if field.name not in ("derived_occurrence_id", "raw_input_lineage"):
            assert _exact(getattr(foreign, field.name)) == _exact(getattr(rc, field.name))
    del mids, foreign_owner
    mid_reader = f.create_window_reader(
        admission=MID_ADMISSION, storage=f.SQLiteReadStorageV1(mid_path),
    )
    assert _exact(mid_reader.get_derived_occurrence(rc.derived_occurrence_id)) == _exact(rc)
    assert _exact(mid_reader.get_derived_occurrence(foreign.derived_occurrence_id)) == (
        _exact(foreign)
    )
    call_history = mid_reader.list_derived_history(**_history_args("D087", C1))
    assert len(call_history) == 2
    assert {item.derived_occurrence_id for item in call_history} == {
        rc.derived_occurrence_id, foreign.derived_occurrence_id,
    }
    _assert_readback(mid_reader, rp, "D087", C2)
    # The correct BASE C1 is still available, but the selected foreign C1 is
    # a valid equal-price parent whose R035 lineage does not bind to BASE.
    request = _straddle_request(
        core_sha, foreign.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert (request.derived_signal_id, request.subject_instrument,
            request.as_of_utc, request.knowledge_cutoff_utc,
            request.calculation_definition_version, request.core_manifest_sha256) == (
        "D109", PAIR, T, CUTOFF, "T01-D109-SCALAR-PAIR-DEF-V1", core_sha,
    )
    assert (request.call_mid, request.put_mid, request.call_delta, request.put_delta) == (
        foreign.derived_occurrence_id, rp.derived_occurrence_id,
        sc.derived_occurrence_id, sp.derived_occurrence_id,
    )
    assert len({request.call_mid, request.put_mid, request.call_delta, request.put_delta}) == 4
    out_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: NOW,
    )
    assert owner.materialise(request) is None
    assert owner.reads.list_derived_history(**_history_args("D109", PAIR)) == ()
    del owner
    reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D109", PAIR)) == ()
    # Refusal must not consume, replace or mutate the actual lawful parents.
    for parent, parent_reader in (
        (rc, mid_reader), (rp, mid_reader), (sc, delta_reader), (sp, delta_reader),
    ):
        assert _exact(parent_reader.get_derived_occurrence(parent.derived_occurrence_id)) == (
            _exact(parent)
        )
    assert _exact(mid_reader.get_derived_occurrence(foreign.derived_occurrence_id)) == (
        _exact(foreign)
    )
