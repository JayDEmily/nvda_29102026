"""RSQL-P01/P03/P04/P05/P08/P12: actual file-backed public M00 contract."""

from dataclasses import fields, replace
from datetime import timedelta
from decimal import Decimal
from struct import unpack

import pytest
from _support import T0, fresh_observation, observation, owner, policy, representation

from nvda_desk.raw_signal_occurrence_truth import api


def test_sqlite_public_contracts_and_typed_identity_layers(tmp_path):
    o = owner(tmp_path / "raw.db", create=True)
    p = policy()
    assert o.commands.register_capture_scope_policy(p) is p
    assert o.reads.get_capture_scope_policy(p.scope_policy_id, 1) == p
    expected = {
        api.CaptureScopePolicyV1: {
            "concept_id",
            "contract_id",
            "units",
            "scope_policy_id",
            "scope_policy_version",
            "activation_ts_utc",
            "eligibility_policy_ref",
            "deactivation_ts_utc",
        },
        api.ScheduledCaptureOccurrenceV1: {
            "concept_id",
            "contract_id",
            "units",
            "capture_occurrence_id",
            "scope_policy_ref",
            "slot_start_utc",
            "slot_end_utc",
        },
        api.CaptureReceiptEvidenceRelationV1: {
            "concept_id",
            "contract_id",
            "units",
            "observation_occurrence_ref",
            "capture_occurrence_ref",
            "scope_policy_ref",
            "received_ts_utc",
            "relation_role",
        },
        api.CaptureReceiptPresenceAssessmentV1: {
            "concept_id",
            "contract_id",
            "units",
            "assessment_occurrence_id",
            "capture_occurrence_ref",
            "outcome",
            "evidence_as_of_ts_utc",
            "supersedes_assessment_ref",
        },
        api.RawObservationOccurrenceV1: {
            "concept_id",
            "contract_id",
            "observation_occurrence_id",
            "delivery_artifact_ref",
            "source_provider",
            "native_record",
            "received_ts_utc",
            "ingestion_sequence",
            "ingestion_sequence_scope",
            "source_temporal_kind",
            "raw_signal_catalogue_ids",
            "source_product_api",
            "source_endpoint_callback",
            "native_identifier",
            "native_tick_series_identifier",
            "source_variant",
            "subject_instrument",
            "native_units",
            "availability_session",
            "source_status_native",
            "revision_vintage_native",
            "received_epoch_ns",
            "source_timestamp_raw",
            "source_timezone_native",
            "market_timezone_iana",
            "market_session_native",
        },
    }
    for record, names in expected.items():
        assert {field.name for field in fields(record)} == names
    factories = [
        api.concept_id,
        api.contract_id,
        api.scope_policy_id,
        api.eligibility_policy_ref,
        api.scope_policy_ref,
        api.capture_occurrence_id,
        api.observation_occurrence_id,
        api.assessment_occurrence_id,
        api.provider_id,
        api.delivery_artifact_ref,
        api.ingestion_sequence_scope,
    ]
    identities = [factory("opaque") for factory in factories]
    assert len({type(item) for item in identities}) == len(identities)
    for wrong in identities:
        if type(wrong) is not type(api.observation_occurrence_id("opaque")):
            with pytest.raises(TypeError):
                replace(observation(), observation_occurrence_id=wrong)
    with pytest.raises(ValueError):
        replace(observation(), received_ts_utc=T0.replace(tzinfo=None))
    with pytest.raises(TypeError):
        api.RawObservationOccurrenceV1(**{"unknown": True})
    raw = observation()
    assert o.commands.admit_raw_observation_occurrence(raw) is raw
    assert o.reads.get_raw_observation_occurrence(raw.observation_occurrence_id) == raw
    # No capture scope is required to preserve a valid observation.
    assert fresh_observation(tmp_path / "raw.db", "obs")["kind"] == "receipt_only"


def test_sqlite_native_fidelity_and_temporal_absence(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    native = {
        "bool": True,
        "int": 1,
        "large": -(10**100 + 13),
        "dec": Decimal("-0.000"),
        "trail": Decimal("1.2300"),
        "nan": Decimal("-NaN123"),
        "snan": Decimal("sNaN7"),
        "inf": Decimal("Infinity"),
        "float": -0.0,
        "floatnan": unpack("!d", bytes.fromhex("7ff8000000000009"))[0],
        "bytes": b"\x00\xff",
        "text": "原始值",
        "null": None,
        "list": [False, None, 2],
        "tuple": ("a", Decimal("2.00")),
        "nested": {"x": b"xx"},
    }
    for index, kind in enumerate(("true_instant", "date_only", "receipt_only")):
        timestamp = {
            "true_instant": "2026-09-20T11:59:59.123456+00:00",
            "date_only": "2026-09-20",
            "receipt_only": None,
        }[kind]
        raw = observation(
            kind,
            index,
            native=native,
            source_temporal_kind=kind,
            source_timestamp_raw=timestamp,
            received_epoch_ns=10**70,
            revision_vintage_native="native-revision",
        )
        o.commands.admit_raw_observation_occurrence(raw)
        read = fresh_observation(path, kind)
        assert read == {
            "native": representation(native),
            "provider": "controlled-provider",
            "delivery": "delivery",
            "kind": kind,
            "source_timestamp_raw": timestamp,
            "sequence": str(index),
            "scope": "scope-A",
            "receipt": T0.isoformat(),
            "epoch": str(10**70),
            "revision": "native-revision",
            "timezone": None,
        }
    with pytest.raises(ValueError):
        observation(source_temporal_kind="receipt_only", source_timestamp_raw="2026-09-20")
    with pytest.raises(ValueError):
        observation(source_temporal_kind="date_only", source_timestamp_raw=None)


def test_sqlite_retry_conflict_and_retransmission(tmp_path):
    path = tmp_path / "raw.db"
    o = owner(path, create=True)
    raw = observation(native={"value": Decimal("3.00")})
    o.commands.admit_raw_observation_occurrence(raw)
    reopened = owner(path, now=T0 + timedelta(days=1))
    assert reopened.commands.admit_raw_observation_occurrence(raw) == raw
    for changed in (
        replace(raw, native_record={"value": Decimal("3.0")}),
        replace(raw, received_ts_utc=T0 + timedelta(microseconds=1)),
        replace(raw, delivery_artifact_ref=api.delivery_artifact_ref("other")),
    ):
        with pytest.raises(ValueError):
            reopened.commands.admit_raw_observation_occurrence(changed)
    again = replace(raw, observation_occurrence_id=api.observation_occurrence_id("retransmit"))
    reopened.commands.admit_raw_observation_occurrence(again)
    assert fresh_observation(path, "obs")["native"] == representation(raw.native_record)
    assert fresh_observation(path, "retransmit")["native"] == representation(raw.native_record)
