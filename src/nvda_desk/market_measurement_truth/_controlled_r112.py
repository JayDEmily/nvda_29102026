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
    """Read-only selector facade; neither M00 commands nor coordinator state escape."""

    __slots__ = (
        "_lock", "_actual_get", "_actual_pages", "_is_sealed",
        "_read_digest", "_read_originals", "_read_source_id",
        "_kind", "_selector",
    )

    def __init__(
        self, lock, reads, is_sealed, read_digest, read_originals,
        read_source_id, kind, selector=None,
    ):
        self._lock = lock
        self._actual_get = reads.get_raw_observation_occurrence
        self._actual_pages = reads.list_projected_raw_history
        self._is_sealed = is_sealed
        self._read_digest = read_digest
        self._read_originals = read_originals
        self._read_source_id = read_source_id
        self._kind = kind
        self._selector = selector

    def locked(self):
        return self._lock

    @property
    def sealed(self) -> bool:
        with self._lock:
            return self._is_sealed()

    @property
    def cohort_kind(self) -> str:
        return self._kind

    @property
    def cohort_digest(self) -> str:
        with self._lock:
            return self._read_digest()

    def trusted_originals(self) -> tuple[raw.RawObservationOccurrenceV1, ...]:
        with self._lock:
            return self._read_originals()

    def source_id_for_receipt(self, receipt: datetime) -> str | None:
        with self._lock:
            return self._read_source_id(receipt)

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


def _build_closed_coordinator(members: tuple[dict, ...], kind: str):
    """Private source ownership; the returned facade has no writer/owner slot.

    The only M00 command is held lexically in this factory. All lawful source
    ingress passes through checked_admit under the same lock as seal and D091
    reads. No raw command object is returned or attached to any facade.
    """
    owner = raw.create_owner()
    write_original = owner.commands.admit_raw_observation_occurrence
    reads = owner.reads
    lock = threading.RLock()
    phase = "NEW"
    admitted: set[object] = set()
    expected = tuple(_expected(item) for item in members)
    roster = {item.observation_occurrence_id: item for item in expected}
    if len(roster) != len(expected):
        raise ValueError("duplicate controlled original roster member")
    digest: str | None = None

    def actual_originals() -> tuple[raw.RawObservationOccurrenceV1, ...]:
        return tuple(
            reads.get_raw_observation_occurrence(item.observation_occurrence_id)
            for item in expected
        )

    def checked_admit(observation: raw.RawObservationOccurrenceV1):
        nonlocal phase
        with lock:
            if phase == "SEALED":
                raise CoordinatorSealRefusal("postseal source ingress refused")
            _validate_first(observation)
            original = roster.get(observation.observation_occurrence_id)
            if original is None:
                raise CoordinatorSourceFieldRefusal("observation.observation_occurrence_id")
            if codec.canonical(observation) != codec.canonical(original):
                raise CoordinatorSourceFieldRefusal("observation.original_roster_content")
            if observation.observation_occurrence_id in admitted:
                raise CoordinatorSourceFieldRefusal("observation.duplicate_roster_id")
            result = write_original(observation)
            if codec.canonical(result) != codec.canonical(original):
                raise ValueError("actual M00 admission changed the original")
            admitted.add(observation.observation_occurrence_id)
            phase = "ADMITTING"
            return result

    def whole_source_history() -> tuple[raw.RawObservationOccurrenceV1, ...]:
        """Genuine raw M00 history includes original t14 lacking a projection.

        The actual M00 public read API is scoped by source and subject. That
        scope is exhaustive for this coordinator because its sole admissible
        writer path enforces these exact identities before M00 invocation.
        """
        from datetime import UTC, timedelta

        cursor: str | None = None
        seen_cursors: set[str] = set()
        found: list[raw.RawObservationOccurrenceV1] = []
        while True:
            page = reads.list_raw_observation_history(
                subject_instrument=_SUBJECT,
                source_provider=_PROVIDER,
                source_variant=_VARIANT,
                received_at_or_before_utc=(
                    datetime.max.replace(tzinfo=UTC) - timedelta(microseconds=1)
                ),
                native_identity_selectors=(),
                limit=8,
                cursor=cursor,
            )
            if (
                type(page) is not raw.RawObservationHistoryPageV1
                or type(page.items) is not tuple
                or not 1 <= len(page.items) <= 8
            ):
                raise CoordinatorSealRefusal("incomplete actual M00 source page")
            found.extend(page.items)
            if len(found) > len(expected):
                raise CoordinatorSealRefusal("unlisted actual M00 source observation")
            next_cursor = page.next_cursor
            if next_cursor is None:
                break
            if (
                type(next_cursor) is not str
                or next_cursor == cursor
                or next_cursor in seen_cursors
            ):
                raise CoordinatorSealRefusal("nonprogress actual M00 source cursor")
            seen_cursors.add(next_cursor)
            cursor = next_cursor
        return tuple(found)

    def seal() -> str:
        nonlocal phase, digest
        with lock:
            if phase != "ADMITTING" or admitted != set(roster):
                raise CoordinatorSealRefusal("incomplete original admissions")
            actual = actual_originals()
            if codec.canonical(actual) != codec.canonical(expected):
                raise CoordinatorSealRefusal("actual original getter content mismatch")
            all_actual = whole_source_history()
            by_id = {item.observation_occurrence_id: item for item in all_actual}
            if (
                len(all_actual) != len(expected)
                or set(by_id) != set(roster)
                or any(
                    codec.canonical(by_id[identity]) != codec.canonical(original)
                    for identity, original in roster.items()
                )
            ):
                raise CoordinatorSealRefusal("unlisted or altered actual M00 cohort")
            digest = hashlib.sha256(codec.canonical(actual)).hexdigest()
            phase = "SEALED"
            return digest

    def is_sealed() -> bool:
        return phase == "SEALED"

    def read_digest() -> str:
        if phase != "SEALED" or digest is None:
            raise CoordinatorSealRefusal("unsealed cohort has no digest")
        return digest

    def trusted_originals() -> tuple[raw.RawObservationOccurrenceV1, ...]:
        if phase != "SEALED" or digest is None:
            raise CoordinatorSealRefusal("trusted source not sealed")
        actual = actual_originals()
        if (
            codec.canonical(actual) != codec.canonical(expected)
            or hashlib.sha256(codec.canonical(actual)).hexdigest() != digest
        ):
            raise ValueError("actual sealed M00 original getter diverged")
        return actual

    def source_id_for_receipt(receipt: datetime) -> str | None:
        # Before sealing this only observes actually admitted original M00 IDs.
        for item in expected:
            if (
                item.received_ts_utc == receipt
                and reads.get_raw_observation_occurrence(
                    item.observation_occurrence_id
                ) is not None
            ):
                return item.observation_occurrence_id.value
        return None

    def read_only_capability(selector=None) -> _ReadOnly:
        with lock:
            return _ReadOnly(
                lock, reads, is_sealed, read_digest, trusted_originals,
                source_id_for_receipt, kind, selector=selector,
            )

    class _Coordinator:
        """Non-mutable facade: no M00 writer, owner or mutable seal-state field."""

        __slots__ = ()

        def checked_admit(self, observation: raw.RawObservationOccurrenceV1):
            return checked_admit(observation)

        def seal(self) -> str:
            return seal()

        def read_only_capability(self) -> _ReadOnly:
            return read_only_capability()

        def test_only_selector_capability(self, adapter) -> _ReadOnly:
            if (
                not callable(getattr(adapter, "get_raw_observation_occurrence", None))
                or not callable(getattr(adapter, "list_projected_raw_history", None))
            ):
                raise TypeError("selector adapter requires exact read methods")
            return read_only_capability(selector=adapter)

    return _Coordinator()


def create_controlled_coordinator():
    members = _read_members(_POSITIVE, _POSITIVE_SHA, False)
    if len(members) != 15:
        raise ValueError("only the exact 15-member R112 positive source is admitted")
    return _build_closed_coordinator(members, "SUCCESS_15")


def _create_negative_only_coordinator(mode: str):
    if mode not in _B_FIXTURES:
        raise ValueError("unadmitted B negative-only source")
    relative, checksum, count = _B_FIXTURES[mode]
    members = _read_members(_BASE / relative, checksum, True)
    if len(members) != count:
        raise ValueError("negative-only raw source count mismatch")
    return _build_closed_coordinator(members, mode)
