"""D131 coherent CALL depth band over the actual native D087 public predecessor."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime
from decimal import Decimal
from typing import cast

from . import api as f
from . import _native_codec as codec
from . import _native_option as option
from . import _native_source as source_module
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "0ac16b9eb4859665807a86739293a196e63916062c3db7c522ab6303eabcfbe8"
NAMESPACE = "neutral_market_measurement_truth/native-d131/v1"
CALL = f.VersionRefV1("native-a2-call", 1)
BOOK = f.VersionRefV1("native-c1-call", 1)
CONTEXT = f.VersionRefV1("native-coherent-call-reference", 1)
BAND = Decimal("0.50")
DEFINITION = f.CalculationDefinitionV1(
    "D131", "D131-NATIVE-CALL-BAND-1", "K02_ALGEBRA",
    "sum(standing size where abs(price - actual D087 midpoint) <= band)",
    ("R185", "R187", "R188", "R189", "R190"), ("D087",), "P_BASIC",
    "contracts", "decimal",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D131" or request.source_profile_ref != BOOK
        or type(request.depth_levels) is not int or request.depth_levels != 0
        or type(request.band) is not Decimal or request.band.as_tuple() != BAND.as_tuple()
        or request.window_seconds is not None or request.side is not None
        or request.positions or len(request.predecessor_occurrence_ids) != 1
        or type(request.predecessor_occurrence_ids[0]) is not str
        or not request.predecessor_occurrence_ids[0]
        or request.as_of_utc > request.knowledge_cutoff_utc):
        raise ValueError("unadmitted native D131 band request")


def _compatible(request: f.NativeCalculationRequestV1,
                source: f.NativeSourceSnapshotV1,
                predecessor: f.NativeMeasurementOccurrenceV1) -> None:
    source_module._validate(source)
    option._validate(predecessor)
    quote_source = predecessor.source
    if quote_source is None:
        raise ValueError("native D087 lacks quote source")
    # This exact synthetic cross-provider A2/C1 relation was commissioned in
    # L01. It is not an inference that two provider traces share a generation.
    if (source.request != f.NativeSourceRequestV1(
            BOOK, request.as_of_utc, request.knowledge_cutoff_utc)
        or source.profile.ref != BOOK or quote_source.profile.ref != CALL
        or source.profile.source_context_ref != CONTEXT
        or quote_source.profile.source_context_ref != CONTEXT
        or source.profile.subject_instrument != quote_source.profile.subject_instrument
        or source.profile.contract_identity != quote_source.profile.contract_identity
        or source.profile.security_type != "OPT"
        or source.profile.option_right != quote_source.profile.option_right
        or source.profile.option_right != "C"
        or source.profile.request != "COH-CALL-R1"
        or quote_source.profile.request != "OPT-C100-R1"
        or source.profile.generation != "OPT-C100-SMART-COHERENT-V2"
        or quote_source.profile.generation != "OPT-L1-G1"
        or predecessor.request.source_profile_ref != CALL
        or predecessor.request.as_of_utc != request.as_of_utc
        or predecessor.request.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or predecessor.derived_occurrence_id != request.predecessor_occurrence_ids[0]
        or predecessor.definition != option.DEFINITION
        or type(predecessor.result) is not Decimal
        or predecessor.quote_assembly is None):
        raise ValueError("D087 does not match the exact coherent CALL reference")


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return "mmtnative-d131:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(request: f.NativeCalculationRequestV1,
             source: f.NativeSourceSnapshotV1,
             predecessor: f.NativeMeasurementOccurrenceV1,
             now: datetime) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    _compatible(request, source, predecessor)
    midpoint = cast(Decimal, predecessor.result)
    selected = tuple(row for row in source.standing_rows
                     if row.price is not None and abs(row.price - midpoint) <= BAND)
    if (not source.standing_rows or any(row.price is None for row in source.standing_rows)
        or not selected):
        raise ValueError("complete priced coherent CALL book required")
    total = sum((row.size for row in selected), Decimal(0))
    value = f.NativeMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D131", "pending", request, DEFINITION,
        source, None, (predecessor,), tuple(row.observation_occurrence_id for row in selected),
        total, DEFINITION.units, DEFINITION.result_shape, request.as_of_utc,
        request.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D131 occurrence required")
    f._Validated.__post_init__(value)
    if (value.owner_object_id != "M02" or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF or value.derived_signal_id != "D131"
        or value.definition != DEFINITION or value.source is None
        or value.quote_assembly is not None or len(value.predecessors) != 1
        or type(value.predecessors[0]) is not f.NativeMeasurementOccurrenceV1
        or type(value.result) is not Decimal
        or codec.canonical(value) != codec.canonical(_produce(
            value.request, value.source, value.predecessors[0],
            value.calculated_at_utc))):
        raise ValueError("native D131 result or full provenance mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived occurrence identity required")
        return next((v for v in self.state.all()
                     if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str,
        subject_instrument: str, effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime, limit: int
        ) -> tuple[f.NativeMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (derived_signal_id != "D131" or type(subject_instrument) is not str
            or not subject_instrument or type(limit) is not int or limit <= 0):
            raise ValueError("bounded native D131 history request required")
        rows = (v for v in self.state.all() if v.source is not None
                and v.source.profile.subject_instrument == subject_instrument
                and v.effective_as_of_utc <= effective_at_or_before_utc
                and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc)
        return tuple(sorted(rows, key=lambda v: (
            v.effective_as_of_utc, v.knowledge_cutoff_utc,
            v.derived_occurrence_id), reverse=True))[:limit]


class _Owner:
    def __init__(self, raw_reader: f.NativeRawReaderV1,
                 predecessor_reader: f.NativeMeasurementReadsV1,
                 state: RecordState, utc_now: Callable[[], datetime]) -> None:
        self.raw_reader, self.predecessor_reader = raw_reader, predecessor_reader
        self.state, self.utc_now = state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.NativeCalculationRequestV1
                    ) -> f.NativeMeasurementOccurrenceV1 | None:
        _request_check(request)
        now = self.utc_now()
        f._utc(now)
        if now < request.knowledge_cutoff_utc:
            raise ValueError("calculation cannot precede knowledge cutoff")
        predecessor = self.predecessor_reader.get_derived_occurrence(
            request.predecessor_occurrence_ids[0])
        if predecessor is None:
            return None
        source_owner = source_module.build_owner(
            f.OwnerAdmissionV1("M02", source_module.BRIEF), self.raw_reader,
            f.MemoryStorageV1(), lambda: now)
        source = source_owner.materialise(f.NativeSourceRequestV1(
            BOOK, request.as_of_utc, request.knowledge_cutoff_utc))
        if source is None:
            return None
        try:
            value = _produce(request, source, predecessor, now)
        except (ValueError, TypeError):
            return None
        return cast(f.NativeMeasurementOccurrenceV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1
           ) -> RecordState:
    return RecordState(storage,
                       lambda payload: codec.decode(payload, f.NativeMeasurementOccurrenceV1),
                       _validate, encode=codec.canonical)


def build_owner(admission: f.OwnerAdmissionV1, raw_reader: f.NativeRawReaderV1,
                predecessor_reader: f.NativeMeasurementReadsV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                utc_now: Callable[[], datetime]) -> f.NativeMeasurementOwnerV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(utc_now)
        or not callable(getattr(raw_reader, "list_projected_raw_history", None))
        or not callable(getattr(raw_reader, "list_raw_observation_history", None))
        or not callable(getattr(predecessor_reader, "get_derived_occurrence", None))):
        raise ValueError("native D131 admission or public predecessors mismatch")
    return _Owner(raw_reader, predecessor_reader, _state(storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.NativeMeasurementReadsV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1):
        raise ValueError("native D131 read-only admission mismatch")
    return _Reads(_state(storage))
