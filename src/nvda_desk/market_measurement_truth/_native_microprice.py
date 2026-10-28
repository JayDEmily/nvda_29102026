"""D137 exact microprice over the commissioned four-callback option assembly."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import api as f
from . import _native_codec as codec
from . import _native_source as source_module
from ._catalogue import _AUTHORITY
from ._native_option import _assemble
from ._record_store import RecordState

BRIEF = "e245fb52e9cdb2d09e88a5d4ad4b298049840e07a1a70288311ff6c651ff82a5"
NAMESPACE = "neutral_market_measurement_truth/native-d137/v1"
PROFILES = {
    f.VersionRefV1("native-a2-call", 1),
    f.VersionRefV1("native-a3-put", 1),
}
DEFINITION = f.CalculationDefinitionV1(
    "D137", "D137-NATIVE-OPTION-MICROPRICE-1", "K02_ALGEBRA",
    "(ask_price*bid_size+bid_price*ask_size)/(bid_size+ask_size)",
    ("R033", "R034", "R035", "R036"), (), "P_BASIC", "USD/underlying share premium", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D137"
        or request.source_profile_ref not in PROFILES
        or request.depth_levels != 0 or request.band is not None
        or request.window_seconds is not None or request.side is not None
        or request.positions or request.predecessor_occurrence_ids
        or request.as_of_utc > request.knowledge_cutoff_utc):
        raise ValueError("unadmitted native option microprice request")


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return "mmtnative-d137:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(request: f.NativeCalculationRequestV1,
             source: f.NativeSourceSnapshotV1, now: datetime
             ) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    assembly, lines = _assemble(source, request)
    bid_size, bid_price, ask_price, ask_size = (
        Fraction(cast(Decimal, line.canonical_value)) for line in lines)
    denominator = bid_size + ask_size
    if denominator == 0:
        raise ValueError("nonzero microprice size denominator required")
    ratio = (ask_price * bid_size + bid_price * ask_size) / denominator
    result = f.ExactRatioV1(ratio.numerator, ratio.denominator)
    value = f.NativeMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D137", "pending", request, DEFINITION,
        source, assembly, (), assembly.constituent_occurrence_ids, result,
        DEFINITION.units, DEFINITION.result_shape, request.as_of_utc,
        request.knowledge_cutoff_utc, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D137 occurrence required")
    f._Validated.__post_init__(value)
    if (value.owner_object_id != "M02" or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF or value.derived_signal_id != "D137"
        or value.definition != DEFINITION or value.source is None
        or value.predecessors or type(value.result) is not f.ExactRatioV1
        or value.quote_assembly is None
        or value != _produce(value.request, value.source, value.calculated_at_utc)):
        raise ValueError("native D137 result or complete provenance mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived occurrence identity required")
        return next((value for value in self.state.all()
                     if value.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str,
        subject_instrument: str, effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime, limit: int
        ) -> tuple[f.NativeMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (derived_signal_id != "D137" or type(subject_instrument) is not str
            or not subject_instrument or type(limit) is not int or limit <= 0):
            raise ValueError("bounded native D137 history request required")
        values = (value for value in self.state.all() if value.source is not None
                  and value.source.profile.subject_instrument == subject_instrument
                  and value.effective_as_of_utc <= effective_at_or_before_utc
                  and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc)
        return tuple(sorted(values, key=lambda value: (
            value.effective_as_of_utc, value.knowledge_cutoff_utc,
            value.derived_occurrence_id), reverse=True))[:limit]


class _Owner:
    def __init__(self, raw_reader: f.NativeRawReaderV1, state: RecordState,
                 utc_now: Callable[[], datetime]) -> None:
        self.raw_reader, self.state, self.utc_now = raw_reader, state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.NativeCalculationRequestV1
                    ) -> f.NativeMeasurementOccurrenceV1 | None:
        _request_check(request)
        now = self.utc_now()
        f._utc(now)
        if now < request.knowledge_cutoff_utc:
            raise ValueError("calculation cannot precede knowledge cutoff")
        source_owner = source_module.build_owner(
            f.OwnerAdmissionV1("M02", source_module.BRIEF), self.raw_reader,
            f.MemoryStorageV1(), lambda: now,
        )
        snapshot = source_owner.materialise(f.NativeSourceRequestV1(
            request.source_profile_ref, request.as_of_utc, request.knowledge_cutoff_utc))
        if snapshot is None:
            return None
        try:
            value = _produce(request, snapshot, now)
        except (ValueError, TypeError):
            return None
        return cast(f.NativeMeasurementOccurrenceV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1
           ) -> RecordState:
    return RecordState(storage, lambda payload: codec.decode(payload, f.NativeMeasurementOccurrenceV1),
                       _validate, encode=codec.canonical)


def build_owner(admission: f.OwnerAdmissionV1, raw_reader: f.NativeRawReaderV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                utc_now: Callable[[], datetime]) -> f.NativeMeasurementOwnerV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(utc_now)
        or not callable(getattr(raw_reader, "list_projected_raw_history", None))
        or not callable(getattr(raw_reader, "list_raw_observation_history", None))):
        raise ValueError("native D137 owner admission mismatch")
    return _Owner(raw_reader, _state(storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.NativeMeasurementReadsV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1):
        raise ValueError("native D137 read-only admission mismatch")
    return _Reads(_state(storage))
