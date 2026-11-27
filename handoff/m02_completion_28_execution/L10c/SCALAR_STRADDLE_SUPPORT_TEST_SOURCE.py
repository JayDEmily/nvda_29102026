"""L10c exact 16 owner-admitted scalar source-support cases.

AUTHORING ONLY: do not import, collect or execute on the Worker.
Prospective exact physical path: tests/product/m02_scalar_straddle_support/test_source.py.
The inert authored bytes remain outside tests/product until independently
cleared candidate and claim installation. No alternate runtime, mock source,
injected projection, private owner helper, or parametrised case expansion.
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

import pytest

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


def _assert_refusal(error, members, name, full_sha, stage, field):
    assert type(error) is f.ScalarStraddleSourceRefusalV1
    assert (error.manifest_id, error.digest, error.stage, error.field) == (
        name, full_sha, stage, field,
    )
    assert not hasattr(error, "source") and not hasattr(error, "commands")
    assert type(error.observed_originals) is tuple
    if stage == "MANIFEST_ID_UNIQUENESS":
        assert error.observed_originals == ()
        return
    assert len(error.observed_originals) == len(members)
    actual_ids = [item.observation_occurrence_id.value for item in error.observed_originals]
    expected_ids = [member["observation"]["observation_occurrence_id"] for member in members]
    assert actual_ids == expected_ids and len(actual_ids) == len(set(actual_ids))
    for item, member in zip(error.observed_originals, members, strict=True):
        _assert_original(item, member["observation"])


# Each of the following is a separately owner-admitted physical case.


def test_l10c_scalar_pair(tmp_path):
    full_sha = "9486f9a4cd45756c167837b67a0626b8e232403d55fa07ac42cae3671b969358"
    core_sha = "477028e777fbcb43c46c3752c14176a1b524f90084635106e45f56d0540929ce"
    members = _specimen("BASE", full_sha, core_sha)
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BASE")
    _source_pins(source, full_sha, core_sha)
    # A direct independent sequence, using the complete lawful seven-role
    # roster; no setup helper creates either source or product parent.
    c1_bid = _read_role(source, members, "C1-bid")
    c1_ask = _read_role(source, members, "C1-ask")
    c2_bid = _read_role(source, members, "C2-bid")
    c2_ask = _read_role(source, members, "C2-ask")
    call_literal = _member(members, "C1-delta")
    call_original = source.get_raw_observation_occurrence(
        raw.observation_occurrence_id(call_literal["observation_occurrence_id"]),
    )
    _assert_original(call_original, call_literal)
    assert call_original.subject_instrument == C1
    assert call_original.native_record["value"]["role"] == "model_delta"
    call_page = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R112"), mappings=(MAPS["R112"],),
        subject_instrument=C1, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    assert type(call_page) is raw.ProjectedRawHistoryPageV1
    assert call_page.next_cursor is None and len(call_page.items) == 1
    call_projection = call_page.items[0]
    _assert_projection(call_projection, call_original, "R112")
    call_delta = (call_original, call_projection)
    put_delta = _read_role(source, members, "C2-delta")
    spot = _read_role(source, members, "C1-spot")
    assert tuple(pair[1].native_value for pair in (c1_bid, c1_ask, c2_bid, c2_ask)) == (
        Decimal("2"), Decimal("4"), Decimal("1"), Decimal("3"),
    )
    assert spot[1].native_value == Decimal("111")
    # Spot is a raw source readback only. There is no spot-derived result.
    absent = source.list_projected_raw_history(
        raw.RawSignalCatalogueId("R118"), mappings=(MAPS["R118"],),
        subject_instrument=C2, received_at_or_before_utc=CUTOFF,
        event_at_or_before_utc=T, limit=100, cursor=None,
    )
    assert absent.items == () and absent.next_cursor is None
    clock = [NOW]
    mid_path = str(tmp_path / "midpoints.sqlite")
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, True), utc_now=lambda: clock[0],
    )
    mc, mp = _mid_request(C1), _mid_request(C2)
    rc, rp = mids.materialise(mc), mids.materialise(mp)
    _assert_midpoint(rc, mc, (c1_bid, c1_ask), 3)
    _assert_midpoint(rp, mp, (c2_bid, c2_ask), 2)
    assert rc.derived_occurrence_id != rp.derived_occurrence_id
    _assert_readback(mids.reads, rc, "D087", C1)
    _assert_readback(mids.reads, rp, "D087", C2)
    delta_path = str(tmp_path / "d091.sqlite")
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, True), utc_now=lambda: clock[0],
    )
    dc, dp = _delta_request(C1, core_sha), _delta_request(C2, core_sha)
    sc, sp = deltas.materialise(dc), deltas.materialise(dp)
    _assert_delta(sc, dc, *call_delta, "0.50", "ABS_50_75")
    _assert_delta(sp, dp, *put_delta, "-0.50", "ABS_50_75")
    assert len({rc.derived_occurrence_id, rp.derived_occurrence_id,
                sc.derived_occurrence_id, sp.derived_occurrence_id}) == 4
    _assert_readback(deltas.reads, sc, "D091", C1)
    _assert_readback(deltas.reads, sp, "D091", C2)
    # Reopen writable owners with the same source but a later calculation
    # clock. Exact immutable retry retains the first committed timestamp.
    del mids, deltas
    clock[0] = NOW + timedelta(seconds=1)
    mids = f.create_window_owner(
        admission=MID_ADMISSION, raw_projection_reader=source,
        storage=f.SQLiteStorageV1(mid_path, False), utc_now=lambda: clock[0],
    )
    deltas = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(delta_path, False), utc_now=lambda: clock[0],
    )
    assert _exact(mids.materialise(mc)) == _exact(rc)
    assert _exact(mids.materialise(mp)) == _exact(rp)
    assert _exact(deltas.materialise(dc)) == _exact(sc)
    assert _exact(deltas.materialise(dp)) == _exact(sp)
    del mids, deltas, source
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


def test_l10c_scalar_call_non_atm(tmp_path):
    full_sha = "26077105077381800fc66994ace01557120e68c4e6039e1d2cc69b00cd237115"
    core_sha = "34e648cd4b3b1ea8c210c5578060badcb49fc0e373fedc52f460dcc56e28ba32"
    members = _specimen("C60", full_sha, core_sha)
    _assert_single_mutation(members, "C1-delta", ("native_record", "model", "delta"),
                            {"native_type": "Decimal", "text": "0.60"})
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="C60")
    _source_pins(source, full_sha, core_sha)
    # Establish the unchanged actual quote/spot originals of this same
    # specimen, not an additional product scenario or midpoint execution.
    for role in ("C1-bid", "C1-ask", "C2-bid", "C2-ask", "C1-spot"):
        _read_role(source, members, role)
    call_original, call_projection = _read_role(source, members, "C1-delta")
    put_original, put_projection = _read_role(source, members, "C2-delta")
    path = str(tmp_path / "d091.sqlite")
    owner = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    call_request = _delta_request(C1, core_sha)
    put_request = _delta_request(C2, core_sha)
    call = owner.materialise(call_request)
    put = owner.materialise(put_request)
    _assert_delta(call, call_request, call_original, call_projection, "0.60", "ABS_50_75")
    _assert_delta(put, put_request, put_original, put_projection, "-0.50", "ABS_50_75")
    assert call.derived_occurrence_id != put.derived_occurrence_id
    _assert_readback(owner.reads, call, "D091", C1)
    _assert_readback(owner.reads, put, "D091", C2)
    del source, owner
    reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(path),
    )
    _assert_readback(reader, call, "D091", C1)
    _assert_readback(reader, put, "D091", C2)


def test_l10c_scalar_put_non_atm(tmp_path):
    full_sha = "494f1ac740e700aa3dcd998a76b1a8cdfb4c7d77dc6cf002c2990321b3866d3f"
    core_sha = "1e0e91f847f8cebf69c084ad7aa9b1e583d1e8a3fda51c2bb23e26e39ee2db3c"
    members = _specimen("P60", full_sha, core_sha)
    _assert_single_mutation(members, "C2-delta", ("native_record", "model", "delta"),
                            {"native_type": "Decimal", "text": "-0.60"})
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="P60")
    _source_pins(source, full_sha, core_sha)
    # Establish the unchanged actual quote/spot originals of this same
    # specimen, not an additional product scenario or midpoint execution.
    for role in ("C1-bid", "C1-ask", "C2-bid", "C2-ask", "C1-spot"):
        _read_role(source, members, role)
    call_original, call_projection = _read_role(source, members, "C1-delta")
    put_original, put_projection = _read_role(source, members, "C2-delta")
    path = str(tmp_path / "d091.sqlite")
    owner = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    call_request = _delta_request(C1, core_sha)
    put_request = _delta_request(C2, core_sha)
    call = owner.materialise(call_request)
    put = owner.materialise(put_request)
    _assert_delta(call, call_request, call_original, call_projection, "0.50", "ABS_50_75")
    _assert_delta(put, put_request, put_original, put_projection, "-0.60", "ABS_50_75")
    assert call.derived_occurrence_id != put.derived_occurrence_id
    _assert_readback(owner.reads, call, "D091", C1)
    _assert_readback(owner.reads, put, "D091", C2)
    del source, owner
    reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(path),
    )
    _assert_readback(reader, call, "D091", C1)
    _assert_readback(reader, put, "D091", C2)


def test_l10c_scalar_zero_pair(tmp_path):
    full_sha = "4149473bc2079961425993f2304e26bfea3697b334e5bb79c3783516adfc98f0"
    core_sha = "3a75798c092ac312280a4b793e386a5f16e7d454dcbb9009e72693ce4ae59ba8"
    members = _specimen("ZERO_PAIR", full_sha, core_sha)
    expected = copy.deepcopy(_base_members())
    for member_id, text in (("C1-delta", "0.00"), ("C2-delta", "-0.00")):
        original = _member(expected, member_id)
        actual = _member(members, member_id)
        for key in ("observation_occurrence_id", "delivery_artifact_ref"):
            assert original[key] != actual[key]
            original[key] = actual[key]
        original["native_record"]["model"]["delta"] = {"native_type": "Decimal", "text": text}
    assert members == expected
    source = f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="ZERO_PAIR")
    _source_pins(source, full_sha, core_sha)
    # Establish the unchanged actual quote/spot originals of this same
    # specimen, not an additional product scenario or midpoint execution.
    for role in ("C1-bid", "C1-ask", "C2-bid", "C2-ask", "C1-spot"):
        _read_role(source, members, role)
    call_original, call_projection = _read_role(source, members, "C1-delta")
    put_original, put_projection = _read_role(source, members, "C2-delta")
    path = str(tmp_path / "d091.sqlite")
    owner = f.create_scalar_d091_owner(
        admission=ADMISSION, source=source,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    call_request = _delta_request(C1, core_sha)
    put_request = _delta_request(C2, core_sha)
    call = owner.materialise(call_request)
    put = owner.materialise(put_request)
    _assert_delta(call, call_request, call_original, call_projection, "0.00", "ABS_00_10")
    _assert_delta(put, put_request, put_original, put_projection, "-0.00", "ABS_00_10")
    assert call.derived_occurrence_id != put.derived_occurrence_id
    _assert_readback(owner.reads, call, "D091", C1)
    _assert_readback(owner.reads, put, "D091", C2)
    del source, owner
    reader = f.create_scalar_d091_reader(
        admission=ADMISSION, storage=f.SQLiteReadStorageV1(path),
    )
    _assert_readback(reader, call, "D091", C1)
    _assert_readback(reader, put, "D091", C2)


def test_l10c_scalar_call_sign():
    full_sha = "4f862e0fdc1ed0631d2bb4bf63cbddd9bf8d3a49901b18be5e348754eaed5090"
    core_sha = "75976e66803d975f2b95d22e98a18ccfe71c7fece984b0fd60655b38c21efa70"
    members = _specimen("BAD_CALL_SIGN", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-delta', ('native_record', 'model', 'delta'),
                            {'native_type': 'Decimal', 'text': '-0.50'})
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BAD_CALL_SIGN")
    _assert_refusal(caught.value, members, "BAD_CALL_SIGN", full_sha,
                    "CORE_DOMAIN_RIGHT_SIGN", "observation.native_record.model.delta")
    oid = _member(members, "C1-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    delta = actual.native_record["model"]["delta"]
    assert type(delta) is Decimal and delta.is_finite() and delta.copy_abs() <= 1
    assert delta < 0 and actual.native_record["option"]["right"] == "C"


def test_l10c_scalar_put_sign():
    full_sha = "c688b0a9a3345dc75086785e47fdb0f42e8473dc11b1aa5dcadb9db18518766e"
    core_sha = "2f63a2688364c449d14165b0ae4987c89a798e7710da30cbf3ad9855b92feeb0"
    members = _specimen("BAD_PUT_SIGN", full_sha, core_sha)
    _assert_single_mutation(members, 'C2-delta', ('native_record', 'model', 'delta'),
                            {'native_type': 'Decimal', 'text': '0.50'})
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="BAD_PUT_SIGN")
    _assert_refusal(caught.value, members, "BAD_PUT_SIGN", full_sha,
                    "CORE_DOMAIN_RIGHT_SIGN", "observation.native_record.model.delta")
    oid = _member(members, "C2-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    delta = actual.native_record["model"]["delta"]
    assert type(delta) is Decimal and delta.is_finite() and delta.copy_abs() <= 1
    assert delta > 0 and actual.native_record["option"]["right"] == "P"


def test_l10c_scalar_delta_range():
    full_sha = "fa94d017169ff3a13e2dd29ebd5bea2011db447f4ec1e97962c917c21aa08a4a"
    core_sha = "3910479a1ce667edf450349ee3ca555ee6f9c7e5797cfa249e0d7782b271af21"
    members = _specimen("DELTA_RANGE", full_sha, core_sha)
    _assert_single_mutation(members, 'C2-delta', ('native_record', 'model', 'delta'),
                            {'native_type': 'Decimal', 'text': '-1.01'})
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_RANGE")
    _assert_refusal(caught.value, members, "DELTA_RANGE", full_sha,
                    "CORE_DOMAIN_RANGE", "observation.native_record.model.delta")
    oid = _member(members, "C2-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    delta = actual.native_record["model"]["delta"]
    assert type(delta) is Decimal and delta.is_finite() and delta == Decimal("-1.01")
    assert delta < 0 and delta.copy_abs() > 1
    assert actual.native_record["option"]["right"] == "P"


def test_l10c_scalar_delta_nonfinite():
    full_sha = "f0dd31f5a4c3ba23bbd6b528557fbe82f9dfe183d2d28bb0ad4ac4446d7ecebd"
    core_sha = "412b2454de642e879efcf6fb1158e0ee04508c3a56c8f50336eb68c0db7015e7"
    members = _specimen("DELTA_NONFINITE", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-delta', ('native_record', 'model', 'delta'),
                            {'native_type': 'Decimal', 'text': 'NaN'})
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_NONFINITE")
    _assert_refusal(caught.value, members, "DELTA_NONFINITE", full_sha,
                    "CORE_DOMAIN_FINITE", "observation.native_record.model.delta")
    oid = _member(members, "C1-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    delta = actual.native_record["model"]["delta"]
    assert type(delta) is Decimal and delta.is_nan()
    assert delta.as_tuple() == Decimal("NaN").as_tuple()


def test_l10c_scalar_delta_type():
    full_sha = "3923fe5c1802fb8966b9b023ad45e14359790bff336c12edd9d539f005c58048"
    core_sha = "3db6cc44628bc81dc9c1c6a0beac1c271d2c75d33c13d098763b868a6f7e3626"
    members = _specimen("DELTA_TYPE", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-delta', ('native_record', 'model', 'delta'),
                            '0.50')
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_TYPE")
    _assert_refusal(caught.value, members, "DELTA_TYPE", full_sha,
                    "CORE_DOMAIN_TYPE", "observation.native_record.model.delta")
    oid = _member(members, "C1-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    delta = actual.native_record["model"]["delta"]
    assert type(delta) is str and delta == "0.50"


def test_l10c_scalar_quote_units():
    full_sha = "7c50ccc44a7f9cc4407d892fa63490d7ec73a87d891db0f4dc189cc41a95cf39"
    core_sha = "cbd0585c9cccbf5e9083976a222aa5c5abc01ceda164031945421dac4a104620"
    members = _specimen("QUOTE_UNITS", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-bid', ('native_units',),
                            'USD_per_contract')
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="QUOTE_UNITS")
    _assert_refusal(caught.value, members, "QUOTE_UNITS", full_sha,
                    "CORE_ORIGINAL_METADATA", "observation.native_units")
    oid = _member(members, "C1-bid")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    assert actual.native_units == "USD_per_contract"
    assert MAPS["R034"].native_units == "USD_per_share"
    assert actual.native_record["quote"]["bid"] == Decimal("2")


def test_l10c_scalar_delta_units():
    full_sha = "fd460141fb51b04c29415b651da562eab6f51456397ab44192c56c8c6788e426"
    core_sha = "cf6c7cff980177c936ad9a1c6fa6b95c4d1b4ebe5154ab6fdaad786cd387aee7"
    members = _specimen("DELTA_UNITS", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-delta', ('native_units',),
                            'percent')
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_UNITS")
    _assert_refusal(caught.value, members, "DELTA_UNITS", full_sha,
                    "CORE_ORIGINAL_METADATA", "observation.native_units")
    oid = _member(members, "C1-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    assert actual.native_units == "percent" and MAPS["R112"].native_units == "delta_fraction"
    assert actual.native_record["model"]["delta"] == Decimal("0.50")


def test_l10c_scalar_delta_event():
    full_sha = "a16b3462191802db3146e9ae36c02dd1a0afe1a7d48980e773dce94bce2109d7"
    core_sha = "7b5b6360a50aa73277771b61e61bf66308f4d0d281354199ed624fc67d38d6eb"
    members = _specimen("DELTA_EVENT", full_sha, core_sha)
    _assert_single_mutation(members, 'C2-delta', ('source_timestamp_raw',),
                            '2026-10-20T12:39:59Z')
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_EVENT")
    _assert_refusal(caught.value, members, "DELTA_EVENT", full_sha,
                    "CORE_ORIGINAL_CLOCK", "observation.source_timestamp_raw")
    oid = _member(members, "C2-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    assert datetime.fromisoformat(actual.source_timestamp_raw) == T - timedelta(seconds=1)
    assert actual.received_ts_utc == T and actual.received_ts_utc <= CUTOFF


def test_l10c_scalar_delta_role():
    full_sha = "fef7cbf7d6217f6d7cd95d2fc39fdf986366318b1ff0cd1f1afa6083ae29ea82"
    core_sha = "ee257b68f8d3a51d1b3b016973e7f90652f07aa29e472ea396e562b560499d12"
    members = _specimen("DELTA_ROLE", full_sha, core_sha)
    _assert_single_mutation(members, 'C1-delta', ('native_record', 'value', 'role'),
                            'model_iv')
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DELTA_ROLE")
    _assert_refusal(caught.value, members, "DELTA_ROLE", full_sha,
                    "CORE_ORIGINAL_IDENTITY", "observation.native_record.value.role")
    oid = _member(members, "C1-delta")["observation_occurrence_id"]
    actual = next(item for item in caught.value.observed_originals
                  if item.observation_occurrence_id.value == oid)
    assert actual.native_record["value"]["role"] == "model_iv"
    assert actual.native_record["model"]["delta"] == Decimal("0.50")


def test_l10c_scalar_missing_core():
    full_sha = "2ea27b1dd3d376641c5870127287ce37e8451863ae1e447e0dd64a303d128013"
    core_sha = "bffc10b4e3b4109691388056a0641e8955b65b20a42b2bd8fe72aa16c7edf0ac"
    members = _specimen("MISSING_CORE", full_sha, core_sha)
    assert members == [member for member in _base_members()
                       if member["member_id"] != "C2-delta"]
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="MISSING_CORE")
    _assert_refusal(caught.value, members, "MISSING_CORE", full_sha,
                    "CORE_ROLE_CARDINALITY", "C2/R112")
    assert all(not (item.subject_instrument == C2
                   and item.raw_signal_catalogue_ids == (raw.RawSignalCatalogueId("R112"),))
               for item in caught.value.observed_originals)


def test_l10c_scalar_extra_core():
    full_sha = "99c09e303931507d1a19f7e30c041d7eeaa2213e06b3189c5ee33a82f7eb518a"
    core_sha = "b232ed9329a9f60948cd869394b4d47d51b4134964e84f12fefc3ed89af263ed"
    members = _specimen("EXTRA_CORE", full_sha, core_sha)
    assert members[:-1] == _base_members()
    extra = members[-1]
    assert extra["member_id"] == "C1-delta-extra"
    expected = copy.deepcopy(_member(_base_members(), "C1-delta"))
    changed = extra["observation"]
    for key in ("observation_occurrence_id", "delivery_artifact_ref", "ingestion_sequence"):
        assert expected[key] != changed[key]
        expected[key] = changed[key]
    assert changed["ingestion_sequence"] == 8
    expected["native_record"]["model"]["delta"] = {"native_type": "Decimal", "text": "0.55"}
    assert expected == changed
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="EXTRA_CORE")
    _assert_refusal(caught.value, members, "EXTRA_CORE", full_sha,
                    "CORE_ROLE_CARDINALITY", "C1/R112")
    actual = tuple(item for item in caught.value.observed_originals
                   if item.subject_instrument == C1
                   and item.raw_signal_catalogue_ids == (raw.RawSignalCatalogueId("R112"),))
    assert len(actual) == 2
    assert actual[0].observation_occurrence_id != actual[1].observation_occurrence_id
    assert tuple(item.native_record["model"]["delta"] for item in actual) == (
        Decimal("0.50"), Decimal("0.55"),
    )


def test_l10c_scalar_duplicate_id():
    full_sha = "2235250a655d528ff56331d30a4e387e5f945bfdf5c9e80d9f40885a258f9264"
    core_sha = "d07dec004650810d5fc66194e6586289542aef512503fb8c61db2745375e5053"
    members = _specimen("DUP_ID", full_sha, core_sha)
    assert members[:-1] == _base_members()
    assert members[-1] == members[4] and members[-1]["member_id"] == "C1-delta"
    with pytest.raises(f.ScalarStraddleSourceRefusalV1) as caught:
        f.create_scalar_straddle_source(admission=ADMISSION, specimen_id="DUP_ID")
    _assert_refusal(caught.value, members, "DUP_ID", full_sha,
                    "MANIFEST_ID_UNIQUENESS", "observation.observation_occurrence_id")
    assert caught.value.observed_originals == ()
