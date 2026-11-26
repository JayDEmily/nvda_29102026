"""D110 exact ten owner-admitted scalar straddle percentage cases.

Inert authoring only; no Worker product import, collection or execution.
Prospective path tests/product/m02_scalar_straddle_d110/test_signal.py.
Self-contained expectation helpers copied from accepted D109 proof text.
Each named case directly creates actual public parents and ordinary readers.
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
    assert result.derived_occurrence_id == (
        "mmtd109scalar1:78ceaa4d2084967b17facca8638204816762c557a5c49a5564cd5b796482523b"
    )
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

MOVE_DEFINITION = f.CalculationDefinitionV1(
    "D110", "T01-D110-SCALAR-PAIR-DEF-V1", "K02_ALGEBRA",
    "100 * D109 / R118", ("R118",), ("D109",), "P_BASIC",
    "percent", "exact_ratio",
    (f.AuthorityArtifactRefV1(POLICY_PATH, POLICY_SHA),
     f.AuthorityArtifactRefV1(BRIEF_PATH, BRIEF)),
)


def _spot_page(source, members, subject, page):
    # Compare the actual public history population to independently expanded
    # originals. A projection's mapping units are NOT original native units.
    expected = [
        member["observation"] for member in members
        if member["observation"]["raw_signal_catalogue_ids"] == ["R118"]
        and member["observation"]["subject_instrument"] == subject
    ]
    assert type(page) is raw.ProjectedRawHistoryPageV1
    assert page.next_cursor is None and len(page.items) == len(expected)
    assert len({item.observation_occurrence_id for item in page.items}) == len(expected)
    actual = {}
    mapping = MAPS["R118"]
    for literal in expected:
        oid = raw.observation_occurrence_id(literal["observation_occurrence_id"])
        original = source.get_raw_observation_occurrence(oid)
        _assert_original(original, literal)
        matches = [item for item in page.items if item.observation_occurrence_id == oid]
        assert len(matches) == 1
        item = matches[0]
        assert type(item) is raw.ProjectedRawValueV1
        expected_fields = {
            "raw_signal_catalogue_id": mapping.raw_signal_catalogue_id,
            "observation_occurrence_id": oid,
            "projection_mapping_id": mapping.mapping_id,
            "projection_mapping_version": mapping.version,
            "source_provider": PROVIDER,
            "source_variant": VARIANT,
            "native_field_path": mapping.native_field_path,
            "native_value": _path(original.native_record, mapping.native_field_path),
            "native_units": mapping.native_units,
            "subject_instrument": subject,
            "source_temporal_kind": literal["source_temporal_kind"],
            "source_timestamp_raw": literal["source_timestamp_raw"],
            "source_timezone_native": literal["source_timezone_native"],
            "received_ts_utc": datetime.fromisoformat(literal["received_ts_utc"]),
            "ingestion_sequence": literal["ingestion_sequence"],
            "ingestion_sequence_scope": raw.ingestion_sequence_scope(SCOPE),
            "revision_vintage_native": literal.get("revision_vintage_native"),
            "selection_identity": raw.RawSelectionIdentityV1(tuple(
                (key, _path(original.native_record, path)) for key, path in META
            )),
        }
        assert {field.name for field in fields(item)} == set(expected_fields)
        for key, value in expected_fields.items():
            assert _exact(getattr(item, key)) == _exact(value), key
        actual[literal["observation_occurrence_id"]] = (original, item)
    return actual


def _move_request(core_sha, full_sha, straddle_id):
    return f.D110ScalarRequestV1(
        derived_signal_id="D110", subject_instrument=PAIR, as_of_utc=T,
        knowledge_cutoff_utc=CUTOFF,
        calculation_definition_version="T01-D110-SCALAR-PAIR-DEF-V1",
        core_manifest_sha256=core_sha, full_specimen_sha256=full_sha,
        straddle=straddle_id,
    )


def _assert_move(result, request, straddle, spot_original, spot_projection):
    assert type(result) is f.D110ScalarOccurrenceV1
    assert result.owner_object_id == "M02"
    assert result.owner_namespace == "neutral_market_measurement_truth/d110/scalar/v1"
    assert result.implementation_brief_sha256 == BRIEF
    assert result.derived_signal_id == "D110" and result.derived_occurrence_id
    assert _exact(result.request) == _exact(request)
    assert _exact(result.definition) == _exact(MOVE_DEFINITION)
    assert result.source_policy_sha256 == POLICY_SHA
    assert result.core_manifest_sha256 == request.core_manifest_sha256
    assert result.full_specimen_sha256 == request.full_specimen_sha256
    assert _exact(result.straddle) == _exact(straddle)
    assert _exact(result.original_observation) == _exact(spot_original)
    assert _exact(result.selected_projection) == _exact(spot_projection)
    assert type(result.result) is f.ExactRatioV1
    assert result.result == f.ExactRatioV1(500, 111)
    assert result.units == "percent" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert {field.name for field in fields(result)} == {
        "owner_object_id", "owner_namespace", "implementation_brief_sha256",
        "derived_signal_id", "derived_occurrence_id", "request", "definition",
        "source_policy_sha256", "core_manifest_sha256", "full_specimen_sha256",
        "straddle", "original_observation", "selected_projection", "result", "units",
        "result_shape", "effective_as_of_utc", "knowledge_cutoff_utc", "calculated_at_utc",
    }


def test_d110_controlled_success(tmp_path):
    specimen = "BASE"
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    result = move.materialise(move_request)
    _assert_move(result, move_request, straddle, spot_original, spot_projection)
    _assert_readback(move.reads, result, "D110", PAIR)
    del move
    clock[0] = NOW + timedelta(seconds=1)
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, False), utc_now=lambda: clock[0],
    )
    assert _exact(move.materialise(move_request)) == _exact(result)
    del move, source, straddle_reader, mid_reader, delta_reader
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    reopened = reader.get_derived_occurrence(result.derived_occurrence_id)
    _assert_move(reopened, move_request, straddle, spot_original, spot_projection)
    _assert_readback(reader, result, "D110", PAIR)


def test_d110_zero_spot(tmp_path):
    specimen = "SPOT_ZERO"
    full_sha = "523da45e8b4da12b314f20c492cf00214b50154b2eef4e5c2624591de4671199"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    _assert_single_mutation(
        members, "C1-spot", ("native_record", "model", "underlying_price"),
        {"native_type": "Decimal", "text": "0"},
    )
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("0"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_negative_spot(tmp_path):
    specimen = "SPOT_NEGATIVE"
    full_sha = "828a7cae565216c21a7e2d49c04c7cdd2e57bff292bbf91fa6fe20a9c4109b59"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    _assert_single_mutation(
        members, "C1-spot", ("native_record", "model", "underlying_price"),
        {"native_type": "Decimal", "text": "-1"},
    )
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("-1"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_missing_spot(tmp_path):
    specimen = "SPOT_MISSING"
    full_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert members == _base_members()[:6]
    assert not c1_spots and not c2_spots
    assert source.get_raw_observation_occurrence(
        raw.observation_occurrence_id("T01-L10C-SCALAR-V1-07")
    ) is None
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_wrong_spot_right(tmp_path):
    specimen = "SPOT_WRONG_RIGHT"
    full_sha = "e42fd8d7545f6615c50e70a49a582b0da61d5b8cac5a59c18c7375977eeae5ba"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert not c1_spots and len(c2_spots) == 1
    spot_original, spot_projection = next(iter(c2_spots.values()))
    expected = copy.deepcopy(_base_members()[-1])
    expected["member_id"] = "C2-spot"
    observation = expected["observation"]
    changed = _member(members, "C2-spot")
    for field in ("observation_occurrence_id", "delivery_artifact_ref"):
        assert observation[field] != changed[field]
        observation[field] = changed[field]
    observation["subject_instrument"] = C2
    observation["native_record"]["contract"]["id"] = C2
    observation["native_record"]["option"]["right"] = "P"
    assert members == [*_base_members()[:6], expected]
    assert spot_original.subject_instrument == C2
    assert spot_original.native_record["option"]["right"] == "P"
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_spot_original_units(tmp_path):
    specimen = "SPOT_UNITS"
    full_sha = "0e5e860514fe8f8d2d070921dd651c512a1f70d9c1144490f450e5792a3cce9f"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    _assert_single_mutation(members, "C1-spot", ("native_units",), "USD_per_contract")
    assert spot_original.native_units == "USD_per_contract"
    assert spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_spot_wrong_event(tmp_path):
    specimen = "SPOT_EVENT"
    full_sha = "0e32c1ec5ce2f4f67e9cd81bfe9a4ff078263a99cc6e1da2685b389f7000a147"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    _assert_single_mutation(
        members, "C1-spot", ("source_timestamp_raw",), "2026-10-20T12:39:59Z",
    )
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert datetime.fromisoformat(spot_original.source_timestamp_raw) == T - timedelta(seconds=1)
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_spot_ambiguous(tmp_path):
    specimen = "SPOT_AMBIGUOUS"
    full_sha = "a286d269efd84cddda2142a34fd04d02b9b5317f37566eb7adb2980c4600213c"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 2 and not c2_spots
    assert members[:7] == _base_members()
    extra = copy.deepcopy(_base_members()[-1])
    extra["member_id"] = "C1-spot-extra"
    observation = extra["observation"]
    changed = _member(members, "C1-spot-extra")
    for field in ("observation_occurrence_id", "delivery_artifact_ref"):
        assert observation[field] != changed[field]
        observation[field] = changed[field]
    observation["ingestion_sequence"] = 8
    observation["native_record"]["model"]["underlying_price"] = {
        "native_type": "Decimal", "text": "112",
    }
    assert members == [*_base_members(), extra]
    assert set(c1_spots) == {
        "T01-L10C-SCALAR-V1-07", "T01-L10C-SCALAR-V1-SPOT_AMBIGUOUS-08",
    }
    assert {projection.native_value for _, projection in c1_spots.values()} == {
        Decimal("111"), Decimal("112"),
    }
    for original, projection in c1_spots.values():
        assert original.native_units == projection.native_units == "USD_per_share"
        assert original.source_timestamp_raw == "2026-10-20T12:40:00Z"
        assert original.received_ts_utc == T
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_missing_parent(tmp_path):
    specimen = "BASE"
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    assert straddle.core_manifest_sha256 == core_sha
    assert [m for m in members if m["observation"]["raw_signal_catalogue_ids"] != ["R118"]] == (
        _base_members()[:6]
    )
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = "mmtd109scalar1:" + "0" * 64
    assert chosen_id != straddle.derived_occurrence_id
    assert straddle_reader.get_derived_occurrence(chosen_id) is None
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)


def test_d110_wrong_core(tmp_path):
    specimen = "BASE"
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen(specimen, full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id=specimen)
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
    straddle_path = str(tmp_path / "d109.sqlite")
    owner = f.create_d109_scalar_owner(
        admission=ADMISSION, source=source,
        midpoint_read_storage=f.SQLiteReadStorageV1(mid_path),
        delta_read_storage=f.SQLiteReadStorageV1(delta_path),
        storage=f.SQLiteStorageV1(straddle_path, True), utc_now=lambda: NOW,
    )
    straddle = owner.materialise(request)
    _assert_straddle(straddle, request, rc, rp, sc, sp, originals)
    _assert_readback(owner.reads, straddle, "D109", PAIR)
    del owner
    straddle_reader = f.create_d109_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(straddle_path),
    )
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
    assert _exact(straddle_reader.get_derived_occurrence(
        straddle.derived_occurrence_id
    )) == _exact(straddle)
    # C60 is a real sealed different core with a lawful spot. The selected
    # actual BASE D109 remains present and valid, but its core differs.
    full_sha = "26077105077381800fc66994ace01557120e68c4e6039e1d2cc69b00cd237115"
    core_sha = "34e648cd4b3b1ea8c210c5578060badcb49fc0e373fedc52f460dcc56e28ba32"
    members = _specimen("C60", full_sha, core_sha)
    _assert_single_mutation(
        members, "C1-delta", ("native_record", "model", "delta"),
        {"native_type": "Decimal", "text": "0.60"},
    )
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="C60")
    _source_pins(source, full_sha, core_sha)
    for label in ("C1-bid", "C1-ask", "C2-bid", "C2-ask", "C1-delta", "C2-delta"):
        _read_role(source, members, label)
    assert straddle.core_manifest_sha256 != core_sha
    c1_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c2_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    c1_spots = _spot_page(source, members, C1, c1_page)
    c2_spots = _spot_page(source, members, C2, c2_page)
    assert len(c1_spots) == 1 and not c2_spots
    spot_original, spot_projection = next(iter(c1_spots.values()))
    assert spot_original.subject_instrument == C1
    assert spot_original.native_record["value"]["role"] == "model_underlying_price"
    assert spot_original.native_record["option"]["right"] == "C"
    assert spot_original.native_record["model"]["convention"] == "controlled-model/1"
    assert type(spot_projection.native_value) is Decimal
    assert spot_projection.native_value.is_finite()
    assert spot_original.native_units == spot_projection.native_units == "USD_per_share"
    assert spot_original.source_timestamp_raw == "2026-10-20T12:40:00Z"
    assert spot_original.received_ts_utc == T
    assert _exact(spot_projection.native_value) == _exact(Decimal("111"))
    chosen_id = straddle.derived_occurrence_id
    move_request = _move_request(core_sha, full_sha, chosen_id)
    assert (move_request.derived_signal_id, move_request.subject_instrument,
            move_request.as_of_utc, move_request.knowledge_cutoff_utc,
            move_request.calculation_definition_version, move_request.core_manifest_sha256,
            move_request.full_specimen_sha256, move_request.straddle) == (
        "D110", PAIR, T, CUTOFF, "T01-D110-SCALAR-PAIR-DEF-V1",
        core_sha, full_sha, chosen_id,
    )
    out_path = str(tmp_path / "d110.sqlite")
    clock = [NOW]
    move = f.create_d110_scalar_owner(
        admission=ADMISSION, source=source,
        straddle_read_storage=f.SQLiteReadStorageV1(straddle_path),
        storage=f.SQLiteStorageV1(out_path, True), utc_now=lambda: clock[0],
    )
    assert move.materialise(move_request) is None
    assert move.reads.list_derived_history(**_history_args("D110", PAIR)) == ()
    del move
    reader = f.create_d110_scalar_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(out_path),
    )
    assert reader.list_derived_history(**_history_args("D110", PAIR)) == ()
    _assert_readback(straddle_reader, straddle, "D109", PAIR)
