"""RSQL-P01/P03/P04/P05/P08/P12: actual file-backed public M00 contract."""

import subprocess
import sys
from collections.abc import Mapping
from dataclasses import MISSING, fields, is_dataclass, replace
from datetime import timedelta
from decimal import Decimal
from struct import pack, unpack

import pytest
from _support import T0, fresh_observation, fresh_record, observation, owner, policy

from nvda_desk.raw_signal_occurrence_truth import api


def representation(value):
    if isinstance(value, Mapping):
        return ["mapping", [[key, representation(value[key])] for key in sorted(value)]]
    if type(value) is Decimal:
        t = value.as_tuple()
        return ["decimal", t.sign, list(t.digits), str(t.exponent)]
    if type(value) is float:
        return ["float", pack("!d", value).hex()]
    if type(value) is bytes:
        return ["bytes", value.hex()]
    if type(value) in (tuple, list):
        return [type(value).__name__, [representation(item) for item in value]]
    if is_dataclass(value):
        return [
            type(value).__name__,
            {f.name: representation(getattr(value, f.name)) for f in fields(value)},
        ]
    return [type(value).__name__, str(value)]


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
    assert fresh_observation(tmp_path / "raw.db", "obs").source_temporal_kind == "receipt_only"


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
            source_product_api="api-v1",
            source_endpoint_callback="callback",
            native_identifier="native-id",
            native_tick_series_identifier="series",
            source_variant="variant",
            subject_instrument="subject",
            native_units="units",
            availability_session="availability",
            source_status_native="status",
            market_timezone_iana="Australia/Melbourne",
            market_session_native="session",
            raw_signal_catalogue_ids=(api.RawSignalCatalogueId("R034"),),
        )
        o.commands.admit_raw_observation_occurrence(raw)
        read = fresh_observation(path, kind)
        assert representation(read) == representation(raw)
        assert representation(read.native_record) == representation(native)
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
    assert representation(fresh_observation(path, "obs")) == representation(raw)
    assert representation(fresh_observation(path, "retransmit")) == representation(again)


def test_sqlite_requiredness_time_layers_and_static_public_facets(tmp_path):
    o = owner(tmp_path / "raw.db", create=True)
    p = policy(deactivation_ts_utc=T0 + timedelta(minutes=1))
    c = api.ScheduledCaptureOccurrenceV1(
        api.concept_id("raw_signal.scheduled_capture_occurrence"),
        api.contract_id("nvda.raw_signal.ScheduledCaptureOccurrence.v1"),
        "not_applicable",
        api.capture_occurrence_id("c"),
        api.scope_policy_ref("policy@1"),
        T0,
        T0 + timedelta(seconds=30),
    )
    r = api.CaptureReceiptEvidenceRelationV1(
        api.concept_id("raw_signal.capture_receipt_evidence_relation"),
        api.contract_id("nvda.raw_signal.CaptureReceiptEvidenceRelation.v1"),
        "not_applicable",
        api.observation_occurrence_id("obs"),
        c.capture_occurrence_id,
        c.scope_policy_ref,
        T0,
        "evidences_receipt_presence_only",
    )
    a = api.CaptureReceiptPresenceAssessmentV1(
        api.concept_id("raw_signal.capture_receipt_presence_assessment"),
        api.contract_id("nvda.raw_signal.CaptureReceiptPresenceAssessment.v1"),
        "not_applicable",
        api.assessment_occurrence_id("a"),
        c.capture_occurrence_id,
        "zero_received",
        T0,
    )
    identities = [
        f("same")
        for f in (
            api.concept_id,
            api.contract_id,
            api.scope_policy_id,
            api.scope_policy_ref,
            api.eligibility_policy_ref,
            api.capture_occurrence_id,
            api.observation_occurrence_id,
            api.assessment_occurrence_id,
            api.provider_id,
            api.delivery_artifact_ref,
            api.ingestion_sequence_scope,
        )
    ]
    identities.append(api.RawSignalCatalogueId("R034"))
    optional = {
        api.CaptureScopePolicyV1: {"deactivation_ts_utc"},
        api.ScheduledCaptureOccurrenceV1: set(),
        api.CaptureReceiptEvidenceRelationV1: set(),
        api.CaptureReceiptPresenceAssessmentV1: {"supersedes_assessment_ref"},
        api.RawObservationOccurrenceV1: {
            f.name
            for f in fields(observation())
            if f.name
            not in {
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
            }
        },
    }
    for value in (p, c, r, a, observation()):
        cls = type(value)
        assert {f.name for f in fields(value) if f.default is not MISSING} == optional[cls]
        for field in fields(value):
            item = getattr(value, field.name)
            if field.default is MISSING:
                args = {
                    f.name: getattr(value, f.name) for f in fields(value) if f.name != field.name
                }
                with pytest.raises(TypeError):
                    cls(**args)
            if hasattr(item, "value"):
                for wrong in identities:
                    if type(wrong) is not type(item):
                        with pytest.raises((TypeError, ValueError)):
                            replace(value, **{field.name: wrong})
            if field.name.endswith("_utc"):
                with pytest.raises(ValueError):
                    replace(value, **{field.name: T0.replace(tzinfo=None)})
        if hasattr(value, "units"):
            with pytest.raises(ValueError):
                replace(value, units="price")
    for invalid in (None, "", "contains", "final", "two_received"):
        with pytest.raises(ValueError):
            replace(a, outcome=invalid)
    with pytest.raises(ValueError):
        replace(r, relation_role="contains")
    # Two provider logical records in one delivery remain distinct original facts.
    first, second = observation("first"), observation("second", 2)
    o.commands.admit_raw_observation_occurrence(first)
    o.commands.admit_raw_observation_occurrence(second)
    assert fresh_record(tmp_path / "raw.db", "observation", "first") == first
    assert fresh_record(tmp_path / "raw.db", "observation", "second") == second
    assert first.delivery_artifact_ref == second.delivery_artifact_ref
    # Actual pinned checker verifies command/read returns, not annotation spelling alone.
    specimen = """
from typing import assert_type, reveal_type
from collections.abc import Sequence
from datetime import datetime
from nvda_desk.raw_signal_occurrence_truth import api
o = api.create_owner()
reveal_type(o.commands.register_capture_scope_policy)
reveal_type(o.commands.realise_scheduled_capture_occurrence)
reveal_type(o.commands.admit_raw_observation_occurrence)
reveal_type(o.commands.derive_capture_receipt_evidence_relation)
reveal_type(o.commands.append_capture_receipt_presence_assessment)
reveal_type(o.commands.reconcile_owed_slots)
reveal_type(o.reads.get_capture_scope_policy)
reveal_type(o.reads.get_scheduled_capture_occurrence)
reveal_type(o.reads.get_raw_observation_occurrence)
reveal_type(o.reads.get_receipt_presence_assessment)
reveal_type(o.reads.list_receipt_presence_assessments)
reveal_type(o.reads.project_raw_value)
reveal_type(o.reads.list_projected_raw_history)
assert_type(o.reads.get_raw_observation_occurrence(api.observation_occurrence_id("o")),
            api.RawObservationOccurrenceV1 | None)
assert_type(o.reads.get_scheduled_capture_occurrence(api.capture_occurrence_id("c")),
            api.ScheduledCaptureOccurrenceV1 | None)
assert_type(o.reads.get_capture_scope_policy(api.scope_policy_id("p"), 1),
            api.CaptureScopePolicyV1 | None)
assert_type(o.reads.get_receipt_presence_assessment(api.assessment_occurrence_id("a")),
            api.CaptureReceiptPresenceAssessmentV1 | None)
assert_type(o.reads.list_receipt_presence_assessments(api.capture_occurrence_id("c")),
            Sequence[api.CaptureReceiptPresenceAssessmentV1])
def commands(p: api.CaptureScopePolicyV1, raw: api.RawObservationOccurrenceV1,
             when: datetime) -> None:
    assert_type(o.commands.register_capture_scope_policy(p), api.CaptureScopePolicyV1)
    assert_type(o.commands.admit_raw_observation_occurrence(raw), api.RawObservationOccurrenceV1)
    assert_type(o.commands.realise_scheduled_capture_occurrence(
        scope_policy_ref=api.scope_policy_ref("p@1"), slot_start_utc=when,
        capture_occurrence_id=api.capture_occurrence_id("c")), api.ScheduledCaptureOccurrenceV1)
    assert_type(o.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=raw.observation_occurrence_id,
        capture_occurrence_ref=api.capture_occurrence_id("c"),
        scope_policy_ref=api.scope_policy_ref("p@1")), api.CaptureReceiptEvidenceRelationV1 | None)
    assert_type(o.commands.append_capture_receipt_presence_assessment(
        assessment_occurrence_id=api.assessment_occurrence_id("a"),
        capture_occurrence_ref=api.capture_occurrence_id("c"), evidence_as_of_ts_utc=when,
        supersedes_assessment_ref=None), api.CaptureReceiptPresenceAssessmentV1)
    assert_type(o.commands.reconcile_owed_slots(scope_policy_ref=api.scope_policy_ref("p@1"),
        slot_starts_utc=(when,), capture_occurrence_ids=(api.capture_occurrence_id("c"),),
        assessment_occurrence_ids=(api.assessment_occurrence_id("a"),)),
        Sequence[api.CaptureReceiptPresenceAssessmentV1])
"""
    checked = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--disallow-any-expr", "-c", specimen],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert checked.stdout.count("Revealed type is") == 13
    assert "Any" not in checked.stdout
    negative = (
        specimen
        + """
o.reads.get_raw_observation_occurrence(api.capture_occurrence_id("wrong-layer"))
"""
    )
    refused = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--disallow-any-expr", "-c", negative],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert refused.returncode == 1
    assert refused.stdout.count("error:") == 1 and "[arg-type]" in refused.stdout
