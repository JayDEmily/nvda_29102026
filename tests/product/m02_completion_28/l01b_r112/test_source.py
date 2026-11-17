"""L01b/R112: exactly 15 admitted physical source-field refusal cases.

AUTHORING ONLY. DO NOT EXECUTE on the Worker. Only a separately designated
strict Tester with an accepted claim/generation and runner may execute these.
The successful source is the immutable original fifteen-member R112 artifact;
none of the negative inputs is an additional successful-source specimen.

The source-field guard must be reached before off-roster comparison or any
public M00 write. This module deliberately uses no monkeypatch, mock M00 owner,
skipped test, xfail or parameterised expansion of the 15 physical tests.
"""
from __future__ import annotations

import copy
from collections.abc import Mapping
from dataclasses import fields
import hashlib
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.raw_signal_occurrence_truth import api as raw
from nvda_desk.market_measurement_truth import _controlled_r112 as controlled


ROOT = Path(__file__).resolve().parents[4]
SOURCE_PATH = ROOT / "handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json"
SOURCE_SHA256 = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
NEGATIVE_DIR = ROOT / "handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/NEGATIVE_FIXTURES"
FIELD_CASES = {
    "native_units": ("observation.native_units", "decimal_percent", "b337bb83a61b02fd470f5fa06cbeeb6c9bc4c22327cfb080bd1e3d0a8e594b33"),
    "source_provider": ("observation.source_provider", "t01-other-provider", "311449aecf4aa3cf92dcedb6cf50d5d04c70af10531d2a119e032f0c2755679d"),
    "source_variant": ("observation.source_variant", "other-variant/fraction-v1", "633d5c5a648fb6e9af5835cfde545f753e9d7b9570a7475ec5e6214582a4a12b"),
    "contract_id": ("observation.native_record.identity.contract_id", "SYNTH-NVDA-OPT-C101-20261120", "5707a23b542a5e6117fca02c926ffb50e8d9687bd48252696728b7bd71d75aae"),
    "underlying": ("observation.native_record.identity.underlying", "OTHER", "8f56be39fe73c6f9d33eca45a90d8ce4e638000583f5517aa989e7a5adca1c41"),
    "security_type": ("observation.native_record.identity.security_type", "STK", "3a62d4f6aeabedf87000c2c5fe1aae7957c6da2d42f78a6eecf594878182193d"),
    "right": ("observation.native_record.identity.right", "P", "cf6d3be90a5cc04ba142673e82b57b38511be1003b3548712fc3e2eda1dc122d"),
    "expiry_date": ("observation.native_record.identity.expiry_date", "2026-11-27", "ff9736a906aebf132d97a7b04c8a14018f704a41371361f3abc3eef3c401acd6"),
    "strike": ("observation.native_record.identity.strike", "105", "a4c3634f248289bff0c427dc6a66360f087a42c60efdf79048338c5b4223feaf"),
    "currency": ("observation.native_record.identity.currency", "EUR", "2fc2210a4fe21ca42a0964dd5d1cbeee11e8c98c5b08cfc838564bed4bf53fe3"),
    "model_variant": ("observation.native_record.identity.model_variant", "CONTROLLED_SIGNED_DELTA_V2", "696f8c8141d90f598850d4325ffa0d5a137290b104e28d20b49af36d97f18c62"),
    "scale": ("observation.native_record.identity.scale", "decimal_percent", "ecaf3846158cf5da5075051350b4e2af8d50e01a7a6f5c80cdf61e75243c6e2d"),
    "generation": ("observation.native_record.identity.generation", "T01-R112-CONTROL-G2", "cd1fbb5e284ba83b9219aaae4d413f9ee7c07e4b161e7d8658c96387e27d56d4"),
    "request_id": ("observation.native_record.identity.request_id", "T01-R112-OTHER-REQUEST", "d1c56064e3c5c94cd9457024ba993b85e694d58056ea449b762fc966b3f5539f"),
    "sequence_scope": ("observation.ingestion_sequence_scope", "T01-R112-CONTROL/G2", "0604d7e5c15d6de8c651cdcc3233c8d56334b97e394487b7810e5d977bc6d39e"),
}
SOURCE_DELIVERY = "T01-R112-CLOSED-BATCH-V1"


def _load_original() -> tuple[dict, ...]:
    assert hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest() == SOURCE_SHA256
    artifact = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    members = tuple(artifact["members"])
    assert len(members) == 15
    assert [m["observation"]["observation_occurrence_id"] for m in members] == [
        f"T01-R112-BATCH-{i:02d}" for i in range(15)
    ]
    return members


def _native(value: object) -> object:
    if isinstance(value, dict):
        if set(value) == {"native_type", "text"}:
            assert value["native_type"] == "Decimal" and type(value["text"]) is str
            return Decimal(value["text"])
        return {k: _native(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_native(v) for v in value]
    return value


def _utc(value: str) -> datetime:
    v = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert v.utcoffset().total_seconds() == 0
    return v


def _observation(member: dict, *, delivery_ref: str) -> raw.RawObservationOccurrenceV1:
    o = member["observation"]
    return raw.RawObservationOccurrenceV1(
        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw.observation_occurrence_id(o["observation_occurrence_id"]),
        delivery_artifact_ref=raw.delivery_artifact_ref(delivery_ref),
        source_provider=raw.provider_id(o["source_provider"]),
        native_record=_native(o["native_record"]),
        received_ts_utc=_utc(o["received_ts_utc"]),
        ingestion_sequence=o["ingestion_sequence"],
        ingestion_sequence_scope=raw.ingestion_sequence_scope(o["ingestion_sequence_scope"]),
        source_temporal_kind=o["source_temporal_kind"],
        raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(r) for r in o["raw_signal_catalogue_ids"]),
        source_variant=o["source_variant"],
        subject_instrument=o["subject_instrument"],
        native_units=o["native_units"],
        source_timestamp_raw=o["source_timestamp_raw"],
        source_timezone_native=o["source_timezone_native"],
    )


def _path_value(value: dict, path: str) -> object:
    current: object = value
    for key in path.split("."):
        assert isinstance(current, dict)
        current = current[key]
    return current


def _set_path(value: dict, path: str, replacement: str) -> None:
    parts = path.split(".")
    cur = value
    for key in parts[:-1]:
        cur = cur[key]
    cur[parts[-1]] = replacement


def _fixture(name: str) -> tuple[dict, str]:
    expected_path, malformed_value, expected_sha = FIELD_CASES[name]
    source = NEGATIVE_DIR / f"l01b_r112_controlled_{name}_refusal.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_sha
    fixture = json.loads(source.read_text(encoding="utf-8"))
    assert fixture["case_id"] == f"L01B-R112-CONTROLLED-{name.replace('_','-').upper()}-REFUSAL"
    assert fixture["original_source_sha256"] == SOURCE_SHA256
    assert fixture["single_mutation"] == {expected_path: malformed_value}
    assert fixture["required_public_seam"] == "COORDINATOR_INGRESS"
    return fixture, expected_path


def _assert_one_bad_field_only(original: dict, negative: dict, field: str) -> None:
    # Independent of the fixture's own 'single_mutation' explanatory label:
    # compare the full original t00 observation with a precisely reconstructed
    # one-field mutation, aside from its intentionally new opaque observation ID.
    expected = copy.deepcopy(original["observation"])
    expected["observation_occurrence_id"] = negative["observation_occurrence_id"]
    assert _path_value({"observation": original["observation"]}, field) != _path_value(
        {"observation": negative}, field
    )
    _set_path({"observation": expected}, field, _path_value({"observation": negative}, field))
    assert negative == expected


def _canonical_native_value(value: object) -> object:
    # Compare complete provider-native payloads by exact content, not
    # Mapping object's identity or Decimal('NaN') == Decimal('NaN').
    if isinstance(value, Mapping):
        return ("mapping", tuple(sorted((key, _canonical_native_value(item))
                                        for key, item in value.items())))
    if type(value) in (tuple, list):
        return (type(value).__name__, tuple(_canonical_native_value(x) for x in value))
    if type(value) is Decimal:
        return ("decimal_as_tuple", value.as_tuple())
    return (type(value).__name__, value)


def _assert_exact_original(actual: object, expected: raw.RawObservationOccurrenceV1) -> None:
    assert type(actual) is raw.RawObservationOccurrenceV1
    for f in fields(raw.RawObservationOccurrenceV1):
        assert _canonical_native_value(getattr(actual, f.name)) == _canonical_native_value(
            getattr(expected, f.name)
        ), f"original raw field mutated: {f.name}"


def _post_refusal_original_seal(coordinator: object, members: tuple[dict, ...]) -> None:
    # Fifteen actual checked-ingress calls after the refusal, not a
    # convenience fixture constructing a pre-populated M00 owner.
    for member in members:
        expected = _observation(member, delivery_ref=SOURCE_DELIVERY)
        admitted = coordinator.checked_admit(expected)
        _assert_exact_original(admitted, expected)
    receipt = coordinator.seal()
    assert receipt is not None
    reads = coordinator.read_only_capability()
    assert not hasattr(reads, "commands")
    for member in members:
        raw_id = raw.observation_occurrence_id(member["observation"]["observation_occurrence_id"])
        original = reads.get_raw_observation_occurrence(raw_id)
        _assert_exact_original(original, _observation(member, delivery_ref=SOURCE_DELIVERY))
    # A rejected negative may not poison the subsequent exact original roster.
    assert reads.get_raw_observation_occurrence(
        raw.observation_occurrence_id("T01-R112-BATCH-14")
    ) is not None


def _exercise_refusal(name: str) -> None:
    originals = _load_original()
    fixture, field = _fixture(name)
    negative = fixture["input"]
    _assert_one_bad_field_only(originals[0], negative["observation"], field)
    coordinator = controlled.create_controlled_coordinator()
    submitted = _observation(
        negative,
        delivery_ref=fixture["proposed_m00_constructor"]["delivery_artifact_ref"],
    )
    with pytest.raises(controlled.CoordinatorSourceFieldRefusal) as caught:
        coordinator.checked_admit(submitted)
    assert caught.value.code == "COORDINATOR_SOURCE_FIELD_REFUSAL"
    assert caught.value.field_path == field
    assert field != "observation.observation_occurrence_id"
    # Exact field-level refusal comes before roster mismatch. A new negative ID
    # was not admitted into M00, and the ORIGINAL fifteen still admit/seal.
    _post_refusal_original_seal(coordinator, originals)
    assert coordinator.read_only_capability().get_raw_observation_occurrence(
        submitted.observation_occurrence_id
    ) is None


# Every named function below is one separately admitted L01b physical case.
# No parameterisation, derived test ids or additional product cases.
def test_l01b_r112_controlled_native_units_refusal() -> None:
    # Direct independent sequence: wrong units even with novel off-roster ID.
    originals = _load_original()
    fixture, field = _fixture("native_units")
    negative = fixture["input"]
    assert field == "observation.native_units"
    assert negative["observation"]["native_units"] == "decimal_percent"
    _assert_one_bad_field_only(originals[0], negative["observation"], field)
    coordinator = controlled.create_controlled_coordinator()
    candidate = _observation(negative, delivery_ref=fixture["proposed_m00_constructor"]["delivery_artifact_ref"])
    with pytest.raises(controlled.CoordinatorSourceFieldRefusal) as caught:
        coordinator.checked_admit(candidate)
    assert caught.value.code == "COORDINATOR_SOURCE_FIELD_REFUSAL"
    assert caught.value.field_path == "observation.native_units"
    _post_refusal_original_seal(coordinator, originals)
    assert coordinator.read_only_capability().get_raw_observation_occurrence(candidate.observation_occurrence_id) is None


def test_l01b_r112_controlled_source_provider_refusal() -> None:
    _exercise_refusal("source_provider")


def test_l01b_r112_controlled_source_variant_refusal() -> None:
    _exercise_refusal("source_variant")


def test_l01b_r112_controlled_contract_id_refusal() -> None:
    _exercise_refusal("contract_id")


def test_l01b_r112_controlled_underlying_refusal() -> None:
    _exercise_refusal("underlying")


def test_l01b_r112_controlled_security_type_refusal() -> None:
    _exercise_refusal("security_type")


def test_l01b_r112_controlled_right_refusal() -> None:
    _exercise_refusal("right")


def test_l01b_r112_controlled_expiry_date_refusal() -> None:
    _exercise_refusal("expiry_date")


def test_l01b_r112_controlled_strike_refusal() -> None:
    _exercise_refusal("strike")


def test_l01b_r112_controlled_currency_refusal() -> None:
    _exercise_refusal("currency")


def test_l01b_r112_controlled_model_variant_refusal() -> None:
    _exercise_refusal("model_variant")


def test_l01b_r112_controlled_scale_refusal() -> None:
    _exercise_refusal("scale")


def test_l01b_r112_controlled_generation_refusal() -> None:
    _exercise_refusal("generation")


def test_l01b_r112_controlled_request_id_refusal() -> None:
    _exercise_refusal("request_id")


def test_l01b_r112_controlled_sequence_scope_refusal() -> None:
    _exercise_refusal("sequence_scope")



