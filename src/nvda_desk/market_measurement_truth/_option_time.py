"""D001 controlled option true-instant calculation and durable readback."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw

from . import _native_codec as native
from . import _option_time_codec as codec
from . import _option_time_source as source
from . import api as f
from ._record_store import RecordState

SIGNAL = "D001"
PROFILE = f.VersionRefV1("t01-option-time-d001", 1)
NAMESPACE = "neutral_market_measurement_truth/option_time/v1"
DEFINITION = f.CalculationDefinitionV1(
    SIGNAL,
    "T01-D001-OPTION-TIME-DEF-V1",
    "K01_TIME",
    "Same actual true instant converted to aware UTC, preserving microseconds.",
    ("R002", "R003"),
    (),
    "P_TIME",
    "UTC_datetime",
    "aware_utc_datetime",
    (
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
            "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
        ),
        f.AuthorityArtifactRefV1(
            "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
            "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
        ),
        f.AuthorityArtifactRefV1(source.POLICY_PATH, source.POLICY_SHA),
        f.AuthorityArtifactRefV1(source.BRIEF_PATH, source.BRIEF),
    ),
)


def _request_check(request: f.OptionTimeRequestV1) -> None:
    if type(request) is not f.OptionTimeRequestV1:
        raise TypeError("exact D001 option-time request required")
    f._Validated.__post_init__(request)
    if request.frame_id not in ("EARLIER", "MAIN", "CROSS_CLOSE", "SAME_DAY", "AT_EXPIRY", "AFTER"):
        raise ValueError("unadmitted D001 option-time frame/clock/profile")
    clocks = source.policy()["frames"][request.frame_id]["calculation_clocks"]["D001"]
    if (
        request.derived_signal_id != SIGNAL
        or request.subject_instrument != source.SUBJECT
        or request.source_profile_ref != PROFILE
        or request.calculation_definition_version != DEFINITION.calculation_definition_version
        or request.predecessor_occurrence_ids != ()
        or request.as_of_utc != datetime.fromisoformat(clocks["as_of_utc"])
        or request.knowledge_cutoff_utc != datetime.fromisoformat(clocks["knowledge_cutoff_utc"])
    ):
        raise ValueError("unadmitted D001 option-time frame/clock/profile")


def _calculate(
    request: f.OptionTimeRequestV1,
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
) -> datetime:
    _request_check(request)
    source.validate_pair(originals, projections)
    r2, r3 = originals
    p2, p3 = projections
    policy = source.policy()
    for original, role, units in (
        (r2, "source_timestamp", "native_time"),
        (r3, "source_offset", "native_timezone"),
    ):
        record = original.native_record
        if (
            original.subject_instrument != source.SUBJECT
            or original.native_units != units
            or source._path(record, ("sample", "id")) != request.frame_id
            or source._path(record, ("value", "role")) != role
            or any(record[key] != value for key, value in policy["contract_identity"].items())
            or original.source_temporal_kind != "true_instant"
        ):
            raise ValueError("D001 actual role/contract/true-instant invariant")
    stamp, offset = p2.native_value, p3.native_value
    if (
        type(stamp) is not str
        or type(offset) is not str
        or r2.source_timestamp_raw != stamp
        or r2.source_timezone_native != offset
        or type(r3.source_timestamp_raw) is not str
        or r3.source_timezone_native != "UTC"
    ):
        raise ValueError("D001 actual supplied offset/text mismatch")
    event = datetime.fromisoformat(stamp)
    other = datetime.fromisoformat(r3.source_timestamp_raw)
    f._utc(other)
    if event.tzinfo is None or event.strftime("%z") != offset.replace(":", ""):
        raise ValueError("D001 actual native offset mismatch")
    result = event.astimezone(UTC)
    if (
        result != other
        or result != request.as_of_utc
        or not result <= r2.received_ts_utc == r3.received_ts_utc <= request.knowledge_cutoff_utc
    ):
        raise ValueError("D001 actual event and receipt chronology mismatch")
    return result


def _validate(value: f.OptionTimeOccurrenceV1) -> None:
    if type(value) is not f.OptionTimeOccurrenceV1:
        raise TypeError("exact D001 option-time occurrence required")
    f._Validated.__post_init__(value)
    result = _calculate(value.request, value.original_observations, value.selected_projections)
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != source.BRIEF
        or value.derived_signal_id != SIGNAL
        or value.definition != DEFINITION
        or value.source_policy_sha256 != source.POLICY_SHA
        or value.source_profile_ref != PROFILE
        or value.predecessor_occurrence_ids != ()
        or native.canonical(value.projection_mappings)
        != native.canonical(tuple(source.mapping_for(rid) for rid in ("R002", "R003")))
        or value.result != result
        or value.result.tzinfo is not UTC
        or value.units != "UTC_datetime"
        or value.result_shape != "aware_utc_datetime"
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.derived_occurrence_id != codec.identity(value)
    ):
        raise ValueError("D001 option-time durable semantic or identity mismatch")


def _store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, codec.decode, _validate, encode=codec.encode)


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> f.OptionTimeOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty D001 occurrence identity required")
        return next(
            (
                value
                for value in self._state.all()
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
    ) -> tuple[f.OptionTimeOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != SIGNAL
            or subject_instrument != source.SUBJECT
            or type(limit) is not int
            or not 1 <= limit <= 64
        ):
            raise ValueError("bounded option-time history required")
        rows = (
            value
            for value in self._state.all()
            if value.effective_as_of_utc <= effective_at_or_before_utc
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
            )
        )[:limit]


class _Owner:
    def __init__(
        self,
        raw_source: f.OptionTimeSourceV1,
        state: RecordState,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._state, self._utc_now = raw_source, state, utc_now
        self.reads = _Reads(state)

    def materialise(self, request: f.OptionTimeRequestV1) -> f.OptionTimeOccurrenceV1 | None:
        if type(request) is not f.OptionTimeRequestV1:
            raise TypeError("exact D001 option-time request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _request_check(request)
            if now < request.knowledge_cutoff_utc:
                return None
            originals, projections = source.live_pair(self._source, request.knowledge_cutoff_utc)
            result = _calculate(request, originals, projections)
            row = f.OptionTimeOccurrenceV1(
                "M02",
                NAMESPACE,
                source.BRIEF,
                SIGNAL,
                "pending",
                request,
                DEFINITION,
                source.POLICY_SHA,
                PROFILE,
                tuple(source.mapping_for(r) for r in ("R002", "R003")),
                originals,
                projections,
                (),
                result,
                "UTC_datetime",
                "aware_utc_datetime",
                request.as_of_utc,
                request.knowledge_cutoff_utc,
                now,
            )
            row = replace(row, derived_occurrence_id=codec.identity(row))
        except (TypeError, ValueError, ArithmeticError, KeyError):
            return None
        return cast(f.OptionTimeOccurrenceV1, self._state.append(row))


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw_source: f.OptionTimeSourceV1,
    storage: f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.OptionTimeOwnerV1:
    source.check_admission(admission)
    if (
        type(raw_source) is not f.OptionTimeSourceV1
        or not raw_source._matches_admission(admission)
        or type(storage) is not f.SQLiteStorageV1
        or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("unadmitted D001 source/storage/clock")
    return _Owner(raw_source, _store(storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteReadStorageV1,
) -> f.OptionTimeReadsV1:
    source.check_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D001 read-only storage")
    return _Reads(_store(storage))
