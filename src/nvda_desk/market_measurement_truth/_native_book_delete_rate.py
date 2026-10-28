"""D140 native receipt deletion rate consumes actual prior positional standing size."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _native_book_insert_rate as rate_source
from . import _native_codec as codec
from . import _native_source as source_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "91f680af16d74b589883d363242572de2dc95360f036db5ccfa5fb9b1ae269c2"
NAMESPACE = "neutral_market_measurement_truth/native-d140/v1"
PROFILE = f.VersionRefV1("native-d140-delete", 1)
T, CUTOFF, ROLES = rate_source.T, rate_source.CUTOFF, rate_source.ROLES
DEFINITION = f.CalculationDefinitionV1(
    "D140",
    "D140-NATIVE-RECEIPT-DELETE-1",
    "K08_RULE_BUCKET_POLICY",
    (
        "count and actual pre-delete standing size of native bid positions1-2 "
        "in two-second R001 receipt bucket"
    ),
    ROLES,
    (),
    "P_RULE",
    "events or size/time",
    "book_rate_pair",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (
        type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D140"
        or request.source_profile_ref != PROFILE
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int
        or request.depth_levels != 0
        or request.band is not None
        or type(request.window_seconds) is not int
        or request.window_seconds != 2
        or type(request.side) is not int
        or request.side != 1
        or request.positions != (1, 2)
        or request.predecessor_occurrence_ids
    ):
        raise ValueError("unadmitted native D140 receipt deletion request")


def _removed(
    source: f.NativeSourceSnapshotV1, request: f.NativeCalculationRequestV1
) -> tuple[tuple[str, ...], Decimal]:
    groups = rate_source._ordered_groups(source)
    start = T - timedelta(seconds=2)
    rate_source._prewindow_complete(source, groups, start)
    sides: dict[int, list[Decimal]] = {0: [], 1: []}
    selected = []
    removed = Decimal(0)
    for group in groups:
        receipt = cast(datetime, group["R001"].canonical_value)
        side = cast(int, group["R188"].canonical_value)
        position = cast(int, group["R185"].canonical_value)
        operation = cast(int, group["R187"].canonical_value)
        native_size = cast(Decimal, group["R190"].canonical_value)
        in_scope = start < receipt <= T and side == 1 and position in request.positions
        if in_scope and operation != 2:
            raise ValueError("selected native bid mutation is not a deletion")
        rows = sides[side]
        if operation == 0:
            if position > len(rows) or native_size <= 0:
                raise ValueError("invalid native positional insert")
            rows.insert(position, native_size)
        elif operation == 1:
            if position >= len(rows) or native_size <= 0:
                raise ValueError("native update lacks standing row")
            rows[position] = native_size
        elif operation == 2:
            if position >= len(rows) or native_size != 0:
                raise ValueError("native delete requires standing position and zero size")
            prior_size = rows.pop(position)
            if in_scope:
                selected.append(group["R001"].observation_occurrence_id)
                removed += prior_size
        else:
            raise ValueError("unadmitted native book operation")
    expected = tuple(
        (side, position, size) for side in (1, 0) for position, size in enumerate(sides[side])
    )
    if (
        tuple((row.side, row.position, row.size) for row in source.standing_rows) != expected
        or len(selected) != 1
    ):
        raise ValueError("exact source replay or selected deletion set incomplete")
    return tuple(selected), removed


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("derived_occurrence_id", "calculated_at_utc")
    }
    return "mmtnative-d140:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(
    request: f.NativeCalculationRequestV1, source: f.NativeSourceSnapshotV1, now: datetime
) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    f._utc(now)
    if now < CUTOFF:
        raise ValueError("calculation precedes knowledge cutoff")
    if (
        source.profile.ref != PROFILE
        or source.request != f.NativeSourceRequestV1(PROFILE, T, CUTOFF)
        or source.calculated_at_utc > now
    ):
        raise ValueError("native D140 source profile/time mismatch")
    selected, removed = _removed(source, request)
    count_rate, size_rate = Fraction(len(selected), 2), Fraction(removed) / 2
    result = f.BookRatePairV1(
        f.ExactRatioV1(count_rate.numerator, count_rate.denominator),
        f.ExactRatioV1(size_rate.numerator, size_rate.denominator),
    )
    value = f.NativeMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D140",
        "pending",
        request,
        DEFINITION,
        source,
        None,
        (),
        selected,
        result,
        DEFINITION.units,
        DEFINITION.result_shape,
        T,
        CUTOFF,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D140 occurrence required")
    f._Validated.__post_init__(value)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D140"
        or value.definition != DEFINITION
        or value.source is None
        or value.quote_assembly is not None
        or value.predecessors
        or type(value.result) is not f.BookRatePairV1
        or codec.canonical(value)
        != codec.canonical(_produce(value.request, value.source, value.calculated_at_utc))
    ):
        raise ValueError("native D140 full source/removed-size identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D140 identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id), None
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
            derived_signal_id != "D140"
            or type(subject_instrument) is not str
            or not subject_instrument
            or type(limit) is not int
            or limit <= 0
        ):
            raise ValueError("bounded native D140 history request required")
        rows = (
            v
            for v in self.state.all()
            if v.source is not None
            and v.source.profile.subject_instrument == subject_instrument
            and v.effective_as_of_utc <= effective_at_or_before_utc
            and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(
            sorted(
                rows,
                key=lambda v: (
                    v.effective_as_of_utc,
                    v.knowledge_cutoff_utc,
                    v.derived_occurrence_id,
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
        if now < CUTOFF:
            raise ValueError("calculation precedes knowledge cutoff")
        source = source_module.build_owner(
            f.OwnerAdmissionV1("M02", source_module.BRIEF),
            self.raw_reader,
            f.MemoryStorageV1(),
            lambda: now,
        ).materialise(f.NativeSourceRequestV1(PROFILE, T, CUTOFF))
        if source is None:
            return None
        try:
            value = _produce(request, source, now)
        except (ValueError, TypeError, ArithmeticError):
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
        raise ValueError("native D140 admission/public source mismatch")
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
        raise ValueError("native D140 read-only admission mismatch")
    return _Reads(_state(storage))
