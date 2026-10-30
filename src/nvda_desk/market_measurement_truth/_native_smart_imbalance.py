"""D136 exact imbalance from actual compatible native D134/D135 public facts."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _native_codec as codec
from . import _native_smart_ask as ask_module
from . import _native_smart_depth as bid_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "8510a6e722300d06993ed8a66a8b1b808488913a48625f31183fd2ef9442c7ec"
NAMESPACE = "neutral_market_measurement_truth/native-d136/v1"
PROFILE = f.VersionRefV1("native-a4-stock", 1)
T = datetime.fromisoformat("2026-10-20T12:40:00+00:00")
CUTOFF = T + timedelta(seconds=1)
DEFINITION = f.CalculationDefinitionV1(
    "D136",
    "D136-NATIVE-COMMON-TOP2-IMBALANCE-1",
    "K02_ALGEBRA",
    "(bid_depth-ask_depth)/(bid_depth+ask_depth)",
    (),
    ("D134", "D135"),
    "P_BASIC",
    "-1_to_1",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (
        type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D136"
        or request.source_profile_ref != PROFILE
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int
        or request.depth_levels != 2
        or request.band is not None
        or request.window_seconds is not None
        or request.side is not None
        or request.positions
        or len(request.predecessor_occurrence_ids) != 2
        or any(type(x) is not str or not x for x in request.predecessor_occurrence_ids)
        or len(set(request.predecessor_occurrence_ids)) != 2
    ):
        raise ValueError("unadmitted native D136 common-top-two request")


def _compatible(
    request: f.NativeCalculationRequestV1,
    bid: f.NativeMeasurementOccurrenceV1,
    ask: f.NativeMeasurementOccurrenceV1,
    now: datetime,
) -> None:
    bid_module._validate(bid)
    ask_module._validate(ask)
    b_source, a_source = bid.source, ask.source
    if b_source is None or a_source is None:
        raise ValueError("actual native depth source snapshots required")
    if (
        bid.derived_occurrence_id != request.predecessor_occurrence_ids[0]
        or ask.derived_occurrence_id != request.predecessor_occurrence_ids[1]
        or bid.definition != bid_module.DEFINITION
        or ask.definition != ask_module.DEFINITION
        or bid.request.source_profile_ref != PROFILE
        or ask.request.source_profile_ref != PROFILE
        or bid.request.depth_levels != request.depth_levels
        or ask.request.depth_levels != request.depth_levels
        or bid.request.side != 1
        or ask.request.side != 0
        or bid.request.as_of_utc != request.as_of_utc
        or ask.request.as_of_utc != request.as_of_utc
        or bid.request.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or ask.request.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or b_source.profile.ref != PROFILE
        or a_source.profile.ref != PROFILE
        or codec.canonical(replace(b_source, calculated_at_utc=a_source.calculated_at_utc))
        != codec.canonical(a_source)
        or bid.calculated_at_utc > now
        or ask.calculated_at_utc > now
        or b_source.calculated_at_utc > bid.calculated_at_utc
        or a_source.calculated_at_utc > ask.calculated_at_utc
    ):
        raise ValueError("actual depths differ in exact source, profiles, levels or time")
    # Both validated profile snapshots include the exact provider/variant,
    # generation, contract/right, request/exchange, mappings, rows, raw lineage
    # and controls. Only calculation timestamps may differ between producers.


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("derived_occurrence_id", "calculated_at_utc")
    }
    return "mmtnative-d136:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(
    request: f.NativeCalculationRequestV1,
    bid: f.NativeMeasurementOccurrenceV1,
    ask: f.NativeMeasurementOccurrenceV1,
    now: datetime,
) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    f._utc(now)
    if now < CUTOFF:
        raise ValueError("calculation cannot precede knowledge cutoff")
    _compatible(request, bid, ask, now)
    b, a = Fraction(cast(Decimal, bid.result)), Fraction(cast(Decimal, ask.result))
    if b < 0 or a < 0 or b + a == 0:
        raise ValueError("nonzero compatible displayed depth required")
    ratio = (b - a) / (b + a)
    value = f.NativeMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D136",
        "pending",
        request,
        DEFINITION,
        None,
        None,
        (bid, ask),
        (),
        f.ExactRatioV1(ratio.numerator, ratio.denominator),
        DEFINITION.units,
        DEFINITION.result_shape,
        T,
        CUTOFF,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def _validate(value: f.NativeMeasurementOccurrenceV1) -> None:
    if type(value) is not f.NativeMeasurementOccurrenceV1:
        raise TypeError("exact native D136 occurrence required")
    f._Validated.__post_init__(value)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D136"
        or value.definition != DEFINITION
        or value.source is not None
        or value.quote_assembly is not None
        or value.selected_event_ids
        or len(value.predecessors) != 2
        or any(type(x) is not f.NativeMeasurementOccurrenceV1 for x in value.predecessors)
        or type(value.result) is not f.ExactRatioV1
    ):
        raise ValueError("native D136 predecessor/result shape mismatch")
    bid, ask = cast(
        tuple[f.NativeMeasurementOccurrenceV1, f.NativeMeasurementOccurrenceV1], value.predecessors
    )
    if codec.canonical(value) != codec.canonical(
        _produce(value.request, bid, ask, value.calculated_at_utc)
    ):
        raise ValueError("native D136 full provenance or identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty native D136 occurrence identity required")
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
            derived_signal_id != "D136"
            or type(subject_instrument) is not str
            or not subject_instrument
            or type(limit) is not int
            or limit <= 0
        ):
            raise ValueError("bounded native D136 history request required")
        rows = (
            v
            for v in self.state.all()
            if v.predecessors[0].source.profile.subject_instrument == subject_instrument
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
        self,
        bid_reader: f.NativeMeasurementReadsV1,
        ask_reader: f.NativeMeasurementReadsV1,
        state: RecordState,
        utc_now: Callable[[], datetime],
    ) -> None:
        self.bid_reader, self.ask_reader = bid_reader, ask_reader
        self.state, self.utc_now = state, utc_now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.NativeCalculationRequestV1
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        _request_check(request)
        now = self.utc_now()
        f._utc(now)
        if now < request.knowledge_cutoff_utc:
            raise ValueError("calculation cannot precede knowledge cutoff")
        bid = self.bid_reader.get_derived_occurrence(request.predecessor_occurrence_ids[0])
        ask = self.ask_reader.get_derived_occurrence(request.predecessor_occurrence_ids[1])
        if (
            type(bid) is not f.NativeMeasurementOccurrenceV1
            or type(ask) is not f.NativeMeasurementOccurrenceV1
        ):
            return None
        try:
            value = _produce(request, bid, ask, now)
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
    bid_reader: f.NativeMeasurementReadsV1,
    ask_reader: f.NativeMeasurementReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.NativeMeasurementOwnerV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(utc_now)
        or not callable(getattr(bid_reader, "get_derived_occurrence", None))
        or not callable(getattr(ask_reader, "get_derived_occurrence", None))
    ):
        raise ValueError("native D136 admission or two public predecessor readers mismatch")
    return _Owner(bid_reader, ask_reader, _state(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.NativeMeasurementReadsV1:
    if (
        type(admission) is not f.OwnerAdmissionV1
        or admission.object_id != "M02"
        or admission.implementation_brief_sha256 != BRIEF
        or type(storage) is not f.SQLiteReadStorageV1
    ):
        raise ValueError("native D136 read-only admission mismatch")
    return _Reads(_state(storage))
