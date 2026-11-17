"""Exact R112 closed-batch coordinator using genuine private in-memory M00.

The successful source is only the SHA-verified original 15. B_TIE and B_OVER64
are test-only negative cohorts with separate file-hash and roster identities.
"""
from __future__ import annotations

import hashlib
import json
import threading
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as raw
from . import _native_codec as codec

_ROOT = Path(__file__).resolve().parents[3]
_BASE = _ROOT / "handoff/m02_completion_28_execution"
_POSITIVE = _BASE / "L01b/CONTROLLED_BATCH_INPUTS.json"
_POSITIVE_SHA = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
_B_FIXTURES = {
    "B_TIE": (
        "L04/D091_PROOF_ADMISSION_REVISION_20261116/NEGATIVE_FIXTURES/d091_controlled_top_rank_tie_refusal.json",
        "0d34b51e309db8799bd6426f1e183a80e1d9244354cda2867af2b1e7271ef0fc", 2,
    ),
    "B_OVER64": (
        "L04/D091_PROOF_ADMISSION_REVISION_20261116/NEGATIVE_FIXTURES/d091_controlled_over_64_refusal.json",
        "ba7129a821d9e6434be9fc5fcc454d8ebd78f043c090255f0c1c2cfde630caf7", 65,
    ),
}
_SUBJECT = "SYNTH-NVDA-OPT-C100-20261120"
_PROVIDER = "t01-controlled-option-delta"
_VARIANT = "controlled-option-model-delta/fraction-v1"
_UNITS = "signed_decimal_fraction"
_SCOPE = "T01-R112-CONTROL/G1"
_SOURCE = "T01-R112-CLOSED-BATCH-V1"
_EXPECTED_IDENTITY = (
    ("contract_id", "SYNTH-NVDA-OPT-C100-20261120"),
    ("underlying", "NVDA"), ("security_type", "OPT"), ("right", "C"),
    ("expiry_date", "2026-11-20"), ("strike", "100"), ("currency", "USD"),
    ("model_variant", "CONTROLLED_SIGNED_DELTA_V1"),
    ("scale", "signed_decimal_fraction"),
    ("generation", "T01-R112-CONTROL-G1"),
    ("request_id", "T01-R112-BOUNDARIES-1"),
)


class CoordinatorSourceFieldRefusal(ValueError):
    """Source field validation before roster and before M00 mutation."""

    def __init__(self, field_path: str) -> None:
        self.code = "COORDINATOR_SOURCE_FIELD_REFUSAL"
        self.field_path = field_path
        super().__init__(f"{self.code}({field_path})")


class CoordinatorSealRefusal(ValueError):
    code = "COORDINATOR_POSTSEAL_INGRESS_REFUSAL"


def _read_members(path: Path, digest: str, negative: bool) -> tuple[dict, ...]:
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != digest:
        raise ValueError("source artifact SHA256 mismatch")
    data = json.loads(content)
    result = data["input"]["members"] if negative else data["members"]
    if type(result) is not list or not result:
        raise ValueError("invalid source member document")
    return tuple(result)


def _native(value: object) -> object:
    if type(value) is dict:
        if set(value) == {"native_type", "text"}:
            if value["native_type"] != "Decimal" or type(value["text"]) is not str:
                raise ValueError("unadmitted native Decimal tag")
            return Decimal(value["text"])
        return {name: _native(item) for name, item in value.items()}
    if type(value) is list:
        return [_native(item) for item in value]
    return value


def _expected(member: dict) -> raw.RawObservationOccurrenceV1:
    item = member["observation"]
    return raw.RawObservationOccurrenceV1(
        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw.observation_occurrence_id(item["observation_occurrence_id"]),
        delivery_artifact_ref=raw.delivery_artifact_ref(_SOURCE),
        source_provider=raw.provider_id(item["source_provider"]),
        native_record=_native(item["native_record"]),
        received_ts_utc=datetime.fromisoformat(item["received_ts_utc"].replace("Z", "+00:00")),
        ingestion_sequence=item["ingestion_sequence"],
        ingestion_sequence_scope=raw.ingestion_sequence_scope(item["ingestion_sequence_scope"]),
        source_temporal_kind=item["source_temporal_kind"],
        raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(x) for x in item["raw_signal_catalogue_ids"]),
        source_variant=item["source_variant"],
        subject_instrument=item["subject_instrument"],
        native_units=item["native_units"],
        source_timestamp_raw=item["source_timestamp_raw"],
        source_timezone_native=item["source_timezone_native"],
    )


def _validate_first(value: raw.RawObservationOccurrenceV1) -> None:
    if type(value) is not raw.RawObservationOccurrenceV1:
        raise TypeError("exact M00 observation required")
    checks = (
        ("observation.native_units", value.native_units, _UNITS),
        ("observation.source_provider", value.source_provider.value, _PROVIDER),
        ("observation.source_variant", value.source_variant, _VARIANT),
        ("observation.ingestion_sequence_scope", value.ingestion_sequence_scope.value, _SCOPE),
        ("observation.subject_instrument", value.subject_instrument, _SUBJECT),
        ("observation.source_temporal_kind", value.source_temporal_kind, "receipt_only"),
        ("observation.source_timestamp_raw", value.source_timestamp_raw, None),
        ("observation.source_timezone_native", value.source_timezone_native, None),
        ("observation.raw_signal_catalogue_ids", value.raw_signal_catalogue_ids,
         (raw.RawSignalCatalogueId("R112"),)),
    )
    for path, observed, expected in checks:
        if observed != expected:
            raise CoordinatorSourceFieldRefusal(path)
    record = value.native_record
    identity = record.get("identity") if isinstance(record, Mapping) else None
    for name, required in _EXPECTED_IDENTITY:
        observed = identity.get(name) if isinstance(identity, Mapping) else None
        if observed != required:
            raise CoordinatorSourceFieldRefusal(f"observation.native_record.identity.{name}")


class _ReadOnly:
    """Public read-only wrapper: no commands, writable M00 or mutable roster."""

    __slots__ = ("_lock", "_actual_get", "_actual_pages", "_state", "_expected",
                 "_digest", "_kind", "_selector")

    def __init__(self, lock, reads, state, expected, digest, kind, selector=None):
        self._lock = lock
        self._actual_get = reads.get_raw_observation_occurrence
        self._actual_pages = reads.list_projected_raw_history
        self._state, self._expected = state, expected
        self._digest, self._kind, self._selector = digest, kind, selector

    def locked(self):
        return self._lock

    @property
    def sealed(self) -> bool:
        with self._lock:
            return self._state["phase"] == "SEALED"

    @property
    def cohort_kind(self) -> str:
        return self._kind

    @property
    def cohort_digest(self) -> str:
        with self._lock:
            if not self.sealed:
                raise CoordinatorSealRefusal("unsealed has no identity")
            return self._digest["sha256"]

    def trusted_originals(self) -> tuple[raw.RawObservationOccurrenceV1, ...]:
        with self._lock:
            if not self.sealed:
                raise CoordinatorSealRefusal("trusted roster not yet sealed")
            actual = tuple(self._actual_get(x.observation_occurrence_id) for x in self._expected)
            if codec.canonical(actual) != codec.canonical(self._expected):
                raise ValueError("trusted M00 original getter diverged")
            if hashlib.sha256(codec.canonical(actual)).hexdigest() != self._digest["sha256"]:
                raise ValueError("trusted actual M00 digest diverged")
            return actual

    def source_id_for_receipt(self, receipt: datetime) -> str | None:
        # Read-only original-member lookup, including the legitimate preseal
        # diagnostic. Never enumerates pages or provides M00 command access.
        with self._lock:
            for expected in self._expected:
                if expected.received_ts_utc == receipt and self._actual_get(
                    expected.observation_occurrence_id
                ) is not None:
                    return expected.observation_occurrence_id.value
            return None

    def get_raw_observation_occurrence(self, occurrence_id):
        with self._lock:
            if self._selector is None:
                return self._actual_get(occurrence_id)
            return self._selector.get_raw_observation_occurrence(occurrence_id)

    def list_projected_raw_history(self, *args, **kwargs):
        with self._lock:
            if self._selector is None:
                return self._actual_pages(*args, **kwargs)
            return self._selector.list_projected_raw_history(*args, **kwargs)


class _Coordinator:
    __slots__ = ("_lock", "_writer", "_reads", "_state", "_expected", "_roster", "_digest", "_kind")

    def __init__(self, members: tuple[dict, ...], kind: str) -> None:
        owner = raw.create_owner()
        self._lock = threading.RLock()
        self._writer = owner.commands.admit_raw_observation_occurrence
        self._reads = owner.reads
        self._state = {"phase": "NEW", "admitted": set()}
        self._expected = tuple(_expected(x) for x in members)
        self._roster = {x.observation_occurrence_id: x for x in self._expected}
        if len(self._roster) != len(self._expected):
            raise ValueError("duplicate controlled source members")
        self._digest = {"sha256": None}
        self._kind = kind

    def checked_admit(self, observation: raw.RawObservationOccurrenceV1):
        with self._lock:
            if self._state["phase"] == "SEALED":
                raise CoordinatorSealRefusal("postseal source ingress refused")
            _validate_first(observation)
            expected = self._roster.get(observation.observation_occurrence_id)
            if expected is None:
                raise CoordinatorSourceFieldRefusal("observation.observation_occurrence_id")
            if codec.canonical(observation) != codec.canonical(expected):
                raise CoordinatorSourceFieldRefusal("observation.original_roster_content")
            if observation.observation_occurrence_id in self._state["admitted"]:
                raise CoordinatorSourceFieldRefusal("observation.duplicate_roster_id")
            admitted = self._writer(observation)
            if codec.canonical(admitted) != codec.canonical(observation):
                raise ValueError("M00 public admission returned a different member")
            self._state["admitted"].add(observation.observation_occurrence_id)
            self._state["phase"] = "ADMITTING"
            return admitted

    def seal(self) -> str:
        with self._lock:
            if self._state["phase"] != "ADMITTING":
                raise CoordinatorSealRefusal("source is not admitting")
            if self._state["admitted"] != set(self._roster):
                raise CoordinatorSealRefusal("incomplete exact original roster")
            actual = tuple(self._reads.get_raw_observation_occurrence(x.observation_occurrence_id)
                           for x in self._expected)
            if codec.canonical(actual) != codec.canonical(self._expected):
                raise CoordinatorSealRefusal("M00 trusted original readback mismatched")
            self._digest["sha256"] = hashlib.sha256(codec.canonical(actual)).hexdigest()
            self._state["phase"] = "SEALED"
            return self._digest["sha256"]

    def read_only_capability(self) -> _ReadOnly:
        with self._lock:
            return _ReadOnly(self._lock, self._reads, self._state, self._expected,
                             self._digest, self._kind)

    def test_only_selector_capability(self, adapter) -> _ReadOnly:
        if (not callable(getattr(adapter, "get_raw_observation_occurrence", None))
                or not callable(getattr(adapter, "list_projected_raw_history", None))):
            raise TypeError("test selector must have read-only M00 port")
        with self._lock:
            return _ReadOnly(self._lock, self._reads, self._state, self._expected,
                             self._digest, self._kind, selector=adapter)


def create_controlled_coordinator() -> _Coordinator:
    members = _read_members(_POSITIVE, _POSITIVE_SHA, False)
    if len(members) != 15:
        raise ValueError("only original 15-source successful R112 cohort supported")
    return _Coordinator(members, "SUCCESS_15")


def _create_negative_only_coordinator(mode: str) -> _Coordinator:
    if mode not in _B_FIXTURES:
        raise ValueError("unadmitted negative-only B cohort")
    path, checksum, count = _B_FIXTURES[mode]
    members = _read_members(_BASE / path, checksum, True)
    if len(members) != count:
        raise ValueError("negative-only cohort count mismatch")
    return _Coordinator(members, mode)
