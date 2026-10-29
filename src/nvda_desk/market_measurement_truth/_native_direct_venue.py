"""D143 qualified MPID concentration over one native subscribed book per side."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from fractions import Fraction
from typing import cast

from . import _native_codec as codec
from . import _native_source as source_module
from . import api as f
from ._catalogue import _AUTHORITY
from ._record_store import RecordState

BRIEF = "b69227f2fbb9cc29702a9bf43ea2b88168757948074675eb48e756c143a40886"
NAMESPACE = "neutral_market_measurement_truth/native-d143/v1"
PROFILE = f.VersionRefV1("native-c2-stock", 1)
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF = T + timedelta(seconds=1)
VENUES = ("ALPHA", "BETA")
DEFINITION = f.CalculationDefinitionV1(
    "D143",
    "D143-NATIVE-SUBSCRIBED-ALL-ROWS-MPID-HHI-1",
    "K02_ALGEBRA",
    (
        "group all standing rows of both native subscribed sides by qualified MPID; "
        "sum squared depth shares"
    ),
    ("R192", "R193", "R194", "R195", "R196", "R197"),
    (),
    "P_BASIC",
    "normalised MPID concentration",
    "venue_concentration",
    tuple(f.AuthorityArtifactRefV1(*value) for value in _AUTHORITY),
)


def _request_check(request: f.NativeCalculationRequestV1) -> None:
    if (
        type(request) is not f.NativeCalculationRequestV1
        or request.derived_signal_id != "D143"
        or request.source_profile_ref != PROFILE
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc != CUTOFF
        or type(request.depth_levels) is not int
        or request.depth_levels != 2
        or request.band is not None
        or request.window_seconds is not None
        or request.side is not None
        or request.positions
        or request.predecessor_occurrence_ids
    ):
        raise ValueError("unadmitted native D143 subscribed all-row request")


def _identity(value: f.NativeMeasurementOccurrenceV1) -> str:
    payload = {
        field.name: getattr(value, field.name)
        for field in fields(value)
        if field.name not in ("derived_occurrence_id", "calculated_at_utc")
    }
    return "mmtnative-d143:" + hashlib.sha256(codec.canonical(payload)).hexdigest()


def _produce(
    request: f.NativeCalculationRequestV1, source: f.NativeSourceSnapshotV1, now: datetime
) -> f.NativeMeasurementOccurrenceV1:
    _request_check(request)
    f._utc(now)
    if now < CUTOFF:
        raise ValueError("calculation precedes knowledge cutoff")
    source_module._validate(source)
    if (
        source.profile.ref != PROFILE
        or source.request != f.NativeSourceRequestV1(PROFILE, T, CUTOFF)
        or source.calculated_at_utc > now
    ):
        raise ValueError("native D143 exact source profile/time mismatch")
    # Source owns positional replay across all MPIDs on a subscribed side.
    # depth_levels describes the bound warm-up, never a per-MPID truncation.
    rows = source.standing_rows
    for side in (1, 0):
        positions = tuple(row.position for row in rows if row.side == side)
        if not positions or positions != tuple(range(len(positions))):
            raise ValueError("complete subscribed-side standing rows required")
    if any(
        type(row.mpid) is not str
        or row.mpid not in VENUES
        or row.requested_exchange != source.profile.requested_exchange
        or row.mpid == row.requested_exchange
        or row.size <= 0
        for row in rows
    ):
        raise ValueError("unqualified or incomplete native MPID source")
    depths = tuple(
        sum((Fraction(row.size) for row in rows if row.mpid == venue), Fraction(0))
        for venue in VENUES
    )
    total = sum(depths, Fraction(0))
    if total <= 0 or any(depth <= 0 for depth in depths):
        raise ValueError("positive complete native MPID grouping required")
    shares = tuple(depth / total for depth in depths)
    hhi = sum((share * share for share in shares), Fraction(0))
    result = f.VenueConcentrationV1(
        VENUES,
        tuple(f.ExactRatioV1(share.numerator, share.denominator) for share in shares),
        f.ExactRatioV1(hhi.numerator, hhi.denominator),
    )
    value = f.NativeMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D143",
        "pending",
        request,
        DEFINITION,
        source,
        None,
        (),
        tuple(row.observation_occurrence_id for row in rows),
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
        raise TypeError("exact native D143 occurrence required")
    f._Validated.__post_init__(value)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D143"
        or value.definition != DEFINITION
        or value.source is None
        or value.quote_assembly is not None
        or value.predecessors
        or type(value.result) is not f.VenueConcentrationV1
        or codec.canonical(value)
        != codec.canonical(_produce(value.request, value.source, value.calculated_at_utc))
    ):
        raise ValueError("native D143 full source/grouping/result identity mismatch")


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.NativeMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty native D143 occurrence identity required")
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
            derived_signal_id != "D143"
            or type(subject_instrument) is not str
            or not subject_instrument
            or type(limit) is not int
            or limit <= 0
        ):
            raise ValueError("bounded native D143 history request required")
        rows = (
            value
            for value in self.state.all()
            if value.source is not None
            and value.source.profile.subject_instrument == subject_instrument
            and value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(
            sorted(
                rows,
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
        raise ValueError("native D143 admission or public source mismatch")
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
        raise ValueError("native D143 read-only admission mismatch")
    return _Reads(_state(storage))
