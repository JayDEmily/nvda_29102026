"""D135 native side0 SMART ask top-two/top-one depth, preserving the legacy profile."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import cast

from . import api as f
from . import _native_codec as codec
from . import _native_source as source_module
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "419afb2f5b0d27d72159587c9b9ad323afcb4dc49242257f9a83fa4317aa5653"
NAMESPACE = "neutral_market_measurement_truth/native-d135/v1"
PROFILE = f.VersionRefV1("native-a4-stock", 1)
T = datetime.fromisoformat("2026-10-20T12:40:00+00:00")
CUTOFF = T + timedelta(seconds=1)
DEFINITION = f.CalculationDefinitionV1(
    "D135", "D135-NATIVE-ASK-TOP2-1", "K02_ALGEBRA",
    "sum(top two standing native SMART side0 ask sizes after positional replay)",
    ("R185", "R187", "R188", "R190"), (), "P_BASIC", "shares", "decimal",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)

DEFINITION_TOP_ONE = f.CalculationDefinitionV1(
    "D135", "D135-NATIVE-ASK-TOP1-1", "K02_ALGEBRA",
    "sum(top one standing native SMART side0 ask size after positional replay)",
    ("R185", "R187", "R188", "R190"), (), "P_BASIC", "shares", "decimal",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D135" or request.source_profile_ref != PROFILE
        or request.as_of_utc != T or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int or request.depth_levels not in (1, 2)
        or request.band is not None or request.window_seconds is not None
        or type(request.side) is not int or request.side != 0
        or request.positions or request.predecessor_occurrence_ids):
        raise ValueError("unadmitted native D135 SMART ask depth request")


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return "mmtnative-d135:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(request: f.NativeCalculationRequestV1,
             source: f.NativeSourceSnapshotV1,
             now: datetime) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    f._utc(now)
    if now < CUTOFF:
        raise ValueError("calculation cannot precede knowledge cutoff")
    source_module._validate(source)
    if (source.profile.ref != PROFILE
        or source.request != f.NativeSourceRequestV1(PROFILE, T, CUTOFF)):
        raise ValueError("native D135 exact source context mismatch")
    selected = tuple(row for row in source.standing_rows
                     if row.side == 0 and row.position < request.depth_levels)
    if tuple(row.position for row in selected) != tuple(range(request.depth_levels)):
        raise ValueError("complete native ask depth selection required")
    # Source replay requires the four declared roles. Price may be retained as
    # provenance when projected, but no R189 input is needed for a size sum.
    total = sum((row.size for row in selected), Decimal(0))
    definition = DEFINITION_TOP_ONE if request.depth_levels == 1 else DEFINITION
    value = f.NativeMeasurementOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D135", "pending", request, definition,
        source, None, (), tuple(row.observation_occurrence_id for row in selected),
        total, definition.units, definition.result_shape, T, CUTOFF, now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D135 occurrence required")
    f._Validated.__post_init__(value)
    if (value.owner_object_id != "M02" or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF or value.derived_signal_id != "D135"
        or value.definition not in (DEFINITION, DEFINITION_TOP_ONE) or value.source is None
        or value.quote_assembly is not None or value.predecessors
        or type(value.result) is not Decimal
        or codec.canonical(value) != codec.canonical(_produce(
            value.request, value.source, value.calculated_at_utc))):
        raise ValueError("native D135 source, definition, result or identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty native D135 occurrence identity required")
        return next((v for v in self.state.all()
                     if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str,
        subject_instrument: str, effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime, limit: int
        ) -> tuple[f.NativeMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (derived_signal_id != "D135" or type(subject_instrument) is not str
            or not subject_instrument or type(limit) is not int or limit <= 0):
            raise ValueError("bounded native D135 history request required")
        rows = (v for v in self.state.all() if v.source is not None
                and v.source.profile.subject_instrument == subject_instrument
                and v.effective_as_of_utc <= effective_at_or_before_utc
                and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc)
        return tuple(sorted(rows, key=lambda v: (
            v.effective_as_of_utc, v.knowledge_cutoff_utc,
            v.derived_occurrence_id), reverse=True))[:limit]


class _Owner:
    def __init__(self, raw_reader: f.NativeRawReaderV1,
                 state: RecordState, utc_now: Callable[[], datetime]) -> None:
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
            f.MemoryStorageV1(), lambda: now)
        source = source_owner.materialise(f.NativeSourceRequestV1(PROFILE, T, CUTOFF))
        if source is None:
            return None
        try:
            value = _produce(request, source, now)
        except (ValueError, TypeError):
            return None
        return cast(f.NativeMeasurementOccurrenceV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1
           ) -> RecordState:
    return RecordState(storage,
                       lambda payload: codec.decode(payload, f.NativeMeasurementOccurrenceV1),
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
        raise ValueError("native D135 admission or public source mismatch")
    return _Owner(raw_reader, _state(storage), utc_now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.NativeMeasurementReadsV1:
    if (type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1):
        raise ValueError("native D135 read-only admission mismatch")
    return _Reads(_state(storage))
