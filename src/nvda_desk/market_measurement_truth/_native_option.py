"""D087: four asynchronous receipt-only option callbacks under the L01 profile."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import cast

from . import _native_codec as codec
from . import _native_source as source_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "0bb079166417c42d3ed2c5f8e363e771c88ba44934cda01184d43be2bc960a76"
NAMESPACE = "neutral_market_measurement_truth/native-d087/v1"
ROLES = ("R033", "R034", "R035", "R036")
POLICY = f.VersionRefV1("native-option-receipt-assembly", 1)
SKEW = timedelta(milliseconds=250)
AGE = timedelta(milliseconds=1000)
PROFILES = {
    f.VersionRefV1("native-a2-call", 1),
    f.VersionRefV1("native-a3-put", 1),
}
DEFINITION = f.CalculationDefinitionV1(
    "D087",
    "D087-NATIVE-OPTION-MIDPOINT-1",
    "K02_ALGEBRA",
    "(bid+ask)/2",
    ("R034", "R035"),
    (),
    "P_BASIC",
    "USD/underlying share premium",
    "decimal",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (
        type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D087"
        or request.source_profile_ref not in PROFILES
        or request.depth_levels != 0
        or request.band is not None
        or request.window_seconds is not None
        or request.side is not None
        or request.positions
        or request.predecessor_occurrence_ids
        or request.as_of_utc > request.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted native option midpoint request")


def _assemble(
    source: f.NativeSourceSnapshotV1, request: f.NativeCalculationRequestV1
) -> tuple[f.NativeQuoteAssemblyV1, tuple[f.NativeRawLineageV1, ...]]:
    source_module._validate(source)
    if (
        source.request
        != f.NativeSourceRequestV1(
            request.source_profile_ref, request.as_of_utc, request.knowledge_cutoff_utc
        )
        or source.profile.ref not in PROFILES
        or source.profile.security_type != "OPT"
        or source.profile.option_right not in {"C", "P"}
        or source.standing_rows
    ):
        raise ValueError("source is not this exact receipt-only option profile")
    last_control = max(
        (control.observation.received_ts_utc for control in source.controls if control.invalidates),
        default=None,
    )
    selected = []
    for role in ROLES:
        candidates = [
            line
            for line in source.raw_input_lineage
            if line.raw_signal_id == role
            and line.received_ts_utc <= request.as_of_utc
            and line.received_ts_utc <= request.knowledge_cutoff_utc
            and (last_control is None or line.received_ts_utc > last_control)
        ]
        if not candidates:
            raise ValueError("missing current quote constituent")
        chosen = max(
            candidates, key=lambda line: (line.received_ts_utc, line.projection.ingestion_sequence)
        )
        if (
            type(chosen.canonical_value) is not Decimal
            or not chosen.canonical_value.is_finite()
            or chosen.canonical_value < 0
        ):
            raise ValueError("invalid exact option quote constituent")
        selected.append(chosen)
    lines = cast(tuple[f.NativeRawLineageV1, ...], tuple(selected))
    ids = tuple(line.observation_occurrence_id for line in lines)
    receipts = tuple(line.received_ts_utc for line in lines)
    if (
        len(set(ids)) != 4
        or max(receipts) - min(receipts) > SKEW
        or request.as_of_utc - max(receipts) > AGE
        or cast(Decimal, lines[1].canonical_value) > cast(Decimal, lines[2].canonical_value)
    ):
        raise ValueError("incomplete, stale, skewed or crossed option assembly")
    return (
        f.NativeQuoteAssemblyV1(
            POLICY, ids, receipts, SKEW, AGE, source.profile.source_context_ref
        ),
        lines,
    )


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("derived_occurrence_id", "calculated_at_utc")
    }
    return "mmtnative-d087:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(
    request: f.NativeCalculationRequestV1, source: f.NativeSourceSnapshotV1, now: datetime
) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    assembly, lines = _assemble(source, request)
    midpoint = (
        cast(Decimal, lines[1].canonical_value) + cast(Decimal, lines[2].canonical_value)
    ) / Decimal(2)
    value = f.NativeMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D087",
        "pending",
        request,
        DEFINITION,
        source,
        assembly,
        (),
        assembly.constituent_occurrence_ids,
        midpoint,
        DEFINITION.units,
        DEFINITION.result_shape,
        request.as_of_utc,
        request.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D087 occurrence required")
    f._Validated.__post_init__(value)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D087"
        or value.definition != DEFINITION
        or value.source is None
        or value.predecessors
        or type(value.result) is not Decimal
        or value.quote_assembly is None
        or value != _produce(value.request, value.source, value.calculated_at_utc)
    ):
        raise ValueError("native D087 result or complete provenance mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty derived occurrence identity required")
        return next(
            (
                value
                for value in self.state.all()
                if value.derived_occurrence_id == derived_occurrence_id
            ),
            None,
        )

    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.NativeMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != "D087"
            or type(subject_instrument) is not str
            or not subject_instrument
            or type(limit) is not int
            or limit <= 0
        ):
            raise ValueError("bounded native D087 history request required")
        values = (
            value
            for value in self.state.all()
            if value.source is not None
            and value.source.profile.subject_instrument == subject_instrument
            and value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(
            sorted(
                values,
                key=lambda value: (
                    value.effective_as_of_utc,
                    value.knowledge_cutoff_utc,
                    value.derived_occurrence_id,
                ),
                reverse=True,
            )
        )[:limit]


class _Owner:
    def __init__(
        self, raw_reader: f.NativeRawReaderV1, state: RecordState, utc_now: Callable[[], datetime]
    ) -> None:
        self.raw_reader, self.state, self.utc_now = raw_reader, state, utc_now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.NativeCalculationRequestV1
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        _request_check(request)
        now = self.utc_now()
        f._utc(now)
        if now < request.knowledge_cutoff_utc:
            raise ValueError("calculation cannot precede knowledge cutoff")
        source_owner = source_module.build_owner(
            f.OwnerAdmissionV1("M02", source_module.BRIEF),
            self.raw_reader,
            f.MemoryStorageV1(),
            lambda: now,
        )
        snapshot = source_owner.materialise(
            f.NativeSourceRequestV1(
                request.source_profile_ref, request.as_of_utc, request.knowledge_cutoff_utc
            )
        )
        if snapshot is None:
            return None
        try:
            value = _produce(request, snapshot, now)
        except (ValueError, TypeError):
            return None
        return cast(f.NativeMeasurementOccurrenceV1, self.state.append(value))


def _state(storage: f.MemoryStorageV1 | f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(
        storage,
        lambda payload: codec.decode(payload, f.NativeMeasurementOccurrenceV1),
        _validate,
        encode=codec.canonical,
    )


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw_reader: f.NativeRawReaderV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.NativeMeasurementOwnerV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(utc_now)
        or not callable(getattr(raw_reader, "list_projected_raw_history", None))
        or not callable(getattr(raw_reader, "list_raw_observation_history", None))
    ):
        raise ValueError("native D087 owner admission mismatch")
    return _Owner(raw_reader, _state(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.NativeMeasurementReadsV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1
    ):
        raise ValueError("native D087 read-only admission mismatch")
    return _Reads(_state(storage))
