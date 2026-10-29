"""D139 collector-receipt insertion rate over complete native positional source."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _native_codec as codec
from . import _native_source as source_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "6bf69e7b0283f5098b29c2182a736ffc7aa051af8fb7bbf8a100f2e531f50502"
NAMESPACE = "neutral_market_measurement_truth/native-d139/v1"
PROFILE = f.VersionRefV1("native-d139-insert", 1)
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
ROLES = ("R001", "R185", "R187", "R188", "R190")
DEFINITION = f.CalculationDefinitionV1(
    "D139",
    "D139-NATIVE-RECEIPT-INSERT-1",
    "K08_RULE_BUCKET_POLICY",
    (
        "count and inserted standing size of native bid positions1-2 "
        "in four-second R001 receipt bucket"
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
        or request.derived_signal_id != "D139"
        or request.source_profile_ref != PROFILE
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int
        or request.depth_levels != 0
        or request.band is not None
        or type(request.window_seconds) is not int
        or request.window_seconds != 4
        or type(request.side) is not int
        or request.side != 1
        or request.positions != (1, 2)
        or request.predecessor_occurrence_ids
    ):
        raise ValueError("unadmitted native D139 receipt insertion request")


def _ordered_groups(
    source: f.NativeSourceSnapshotV1,
) -> tuple[dict[str, f.NativeRawLineageV1], ...]:
    """Exact five-role receipt groups, after the owning source replay validates."""
    source_module._validate(source)
    groups: dict[str, dict[str, f.NativeRawLineageV1]] = {}
    for line in source.raw_input_lineage:
        group = groups.setdefault(line.observation_occurrence_id, {})
        if line.raw_signal_id in group:
            raise ValueError("duplicate receipt-book role")
        group[line.raw_signal_id] = line
    for group in groups.values():
        if set(group) != set(ROLES):
            raise ValueError("five complete receipt-book roles required")
        receipt = group["R001"].canonical_value
        if type(receipt) is not datetime:
            raise TypeError("R001 must retain exact UTC datetime")
        f._utc(receipt)
        for rid, line in group.items():
            expected = datetime if rid == "R001" else Decimal if rid == "R190" else int
            if (
                type(line.canonical_value) is not expected
                or line.time_basis != "collector_receipt"
                or line.event_time_utc is not None
                or line.received_ts_utc != receipt
                or line.projection.received_ts_utc != receipt
                or line.projection.source_temporal_kind != "receipt_only"
                or line.projection.source_timestamp_raw is not None
                or line.projection.source_timezone_native is not None
            ):
                raise ValueError("receipt role or native clock provenance mismatch")
    return tuple(
        sorted(
            groups.values(),
            key=lambda group: (
                cast(datetime, group["R001"].canonical_value),
                group["R001"].projection.ingestion_sequence,
            ),
        )
    )


def _prewindow_complete(
    source: f.NativeSourceSnapshotV1,
    groups: tuple[dict[str, f.NativeRawLineageV1], ...],
    start: datetime,
) -> None:
    by_id = {group["R001"].observation_occurrence_id: group for group in groups}
    warmup = source.profile.warmup_observation_ids
    if not warmup or any(
        oid not in by_id or cast(datetime, by_id[oid]["R001"].canonical_value) > start
        for oid in warmup
    ):
        raise ValueError("complete bound warm-up must precede the receipt window")
    # The source validator establishes known-empty epoch, exact ordered prefix,
    # subscribed-side coverage and positional mutations including controls.


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("derived_occurrence_id", "calculated_at_utc")
    }
    return "mmtnative-d139:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


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
        raise ValueError("native D139 source profile/time mismatch")
    groups = _ordered_groups(source)
    start = T - timedelta(seconds=4)
    _prewindow_complete(source, groups, start)
    selected = []
    size = Decimal(0)
    for group in groups:
        receipt = cast(datetime, group["R001"].canonical_value)
        if (
            start < receipt <= T
            and group["R188"].canonical_value == 1
            and group["R185"].canonical_value in request.positions
        ):
            if group["R187"].canonical_value != 0:
                raise ValueError("selected native bid mutation is not an insert")
            selected.append(group["R001"].observation_occurrence_id)
            size += cast(Decimal, group["R190"].canonical_value)
    if len(selected) != 2:
        raise ValueError("complete admitted selected insert set required")
    count_rate, size_rate = Fraction(len(selected), 4), Fraction(size) / 4
    result = f.BookRatePairV1(
        f.ExactRatioV1(count_rate.numerator, count_rate.denominator),
        f.ExactRatioV1(size_rate.numerator, size_rate.denominator),
    )
    value = f.NativeMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D139",
        "pending",
        request,
        DEFINITION,
        source,
        None,
        (),
        tuple(selected),
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
        raise TypeError("exact native D139 occurrence required")
    f._Validated.__post_init__(value)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D139"
        or value.definition != DEFINITION
        or value.source is None
        or value.quote_assembly is not None
        or value.predecessors
        or type(value.result) is not f.BookRatePairV1
        or codec.canonical(value)
        != codec.canonical(_produce(value.request, value.source, value.calculated_at_utc))
    ):
        raise ValueError("native D139 full source/result identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty D139 identity required")
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
            derived_signal_id != "D139"
            or type(subject_instrument) is not str
            or not subject_instrument
            or type(limit) is not int
            or limit <= 0
        ):
            raise ValueError("bounded native D139 history request required")
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
        raise ValueError("native D139 admission/public source mismatch")
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
        raise ValueError("native D139 read-only admission mismatch")
    return _Reads(_state(storage))
