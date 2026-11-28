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


LOCAL_SIGNAL = "D003"
LOCAL_PROFILE = f.VersionRefV1("t01-option-time-d003", 1)
LOCAL_NAMESPACE = "neutral_market_measurement_truth/option_time_local/v1"
LOCAL_ZONE_REF = f.VersionRefV1("t01-option-session-calendar", 1)
LOCAL_DEFINITION = f.CalculationDefinitionV1(
    LOCAL_SIGNAL,
    "T01-D003-OPTION-TIME-DEF-V1",
    "K01_TIME",
    "Convert actual D001 UTC to the admitted R004 IANA exchange zone, preserving the same instant.",
    ("R004",),
    ("D001",),
    "P_TIME",
    "IANA_datetime",
    "aware_iana_datetime",
    (
        *DEFINITION.authority_refs[:3],
        f.AuthorityArtifactRefV1(source.LOCAL_BRIEF_PATH, source.LOCAL_BRIEF),
    ),
)


def _local_request_check(request: f.OptionTimeRequestV1) -> None:
    if type(request) is not f.OptionTimeRequestV1:
        raise TypeError("exact D003 option-time request required")
    f._Validated.__post_init__(request)
    policy = source.local_policy()
    if request.frame_id not in policy["frames"]:
        raise ValueError("unadmitted D003 option-time frame")
    clocks = policy["frames"][request.frame_id]["calculation_clocks"][LOCAL_SIGNAL]
    if (
        request.derived_signal_id != LOCAL_SIGNAL
        or request.subject_instrument != source.SUBJECT
        or request.source_profile_ref != LOCAL_PROFILE
        or request.calculation_definition_version != LOCAL_DEFINITION.calculation_definition_version
        or len(request.predecessor_occurrence_ids) != 1
        or request.as_of_utc != datetime.fromisoformat(clocks["as_of_utc"])
        or request.knowledge_cutoff_utc != datetime.fromisoformat(clocks["knowledge_cutoff_utc"])
    ):
        raise ValueError("unadmitted D003 option-time frame/clock/profile")


def _local_calculate(
    request: f.OptionTimeRequestV1,
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
    parent: f.OptionTimeOccurrenceV1,
) -> datetime:
    from zoneinfo import ZoneInfo

    _local_request_check(request)
    _validate(parent)
    if (
        len(originals) != 1 or len(projections) != 1
        or request.predecessor_occurrence_ids != (parent.derived_occurrence_id,)
        or parent.request.subject_instrument != request.subject_instrument
        or parent.request.frame_id != request.frame_id
        or parent.effective_as_of_utc != request.as_of_utc
        or parent.result != request.as_of_utc
        or not (
            parent.knowledge_cutoff_utc <= parent.calculated_at_utc <= request.knowledge_cutoff_utc
        )
    ):
        raise ValueError("D003 actual parent alignment or visibility mismatch")
    source.validate_local_roles(
        parent.original_observations + originals, parent.selected_projections + projections,
    )
    original, = originals
    projection, = projections
    policy = source.local_policy()
    zone = policy["calendar"]["iana_zone"]
    record = original.native_record
    if (
        original.subject_instrument != source.SUBJECT
        or original.native_units != "IANA_timezone"
        or original.source_temporal_kind != "receipt_only"
        or original.source_timestamp_raw is not None
        or original.source_timezone_native is not None
        or original.received_ts_utc > request.knowledge_cutoff_utc
        or source._path(record, ("sample", "id")) != request.frame_id
        or source._path(record, ("value", "role")) != "exchange_iana"
        or any(record[key] != value for key, value in policy["contract_identity"].items())
        or type(projection.native_value) is not str
        or projection.native_value != zone or zone != "America/New_York"
        or policy["calendar"]["ref"] != "t01-option-session-calendar/1"
    ):
        raise ValueError("D003 actual R004 zone/role/contract/receipt invariant")
    return parent.result.astimezone(ZoneInfo(zone))


def _validate_local(value: f.OptionTimeLocalOccurrenceV1) -> None:
    if type(value) is not f.OptionTimeLocalOccurrenceV1:
        raise TypeError("exact D003 option-time occurrence required")
    value.__post_init__()
    expected = _local_calculate(
        value.request, value.original_observations, value.selected_projections, value.predecessor,
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != LOCAL_NAMESPACE
        or value.implementation_brief_sha256 != source.LOCAL_BRIEF
        or value.derived_signal_id != LOCAL_SIGNAL
        or value.definition != LOCAL_DEFINITION
        or value.source_policy_sha256 != source.POLICY_SHA
        or value.source_profile_ref != LOCAL_PROFILE
        or value.predecessor_occurrence_ids != value.request.predecessor_occurrence_ids
        or native.canonical(value.projection_mappings)
        != native.canonical((source.mapping_for("R004"),))
        or value.zone_policy_ref != LOCAL_ZONE_REF
        or codec.local_datetime_facts(value.result) != codec.local_datetime_facts(expected)
        or value.units != LOCAL_DEFINITION.units
        or value.result_shape != LOCAL_DEFINITION.result_shape
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.derived_occurrence_id != codec.local_identity(value)
    ):
        raise ValueError("D003 option-time durable semantic or identity mismatch")


def _local_store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, codec.decode_local, _validate_local, encode=codec.encode_local)


class _LocalReads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str,
    ) -> f.OptionTimeLocalOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty D003 occurrence identity required")
        return next(
            (value for value in self._state.all()
             if value.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.OptionTimeLocalOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != LOCAL_SIGNAL or subject_instrument != source.SUBJECT
            or type(limit) is not int or not 1 <= limit <= 64
        ):
            raise ValueError("bounded D003 option-time history required")
        rows = (
            value for value in self._state.all()
            if value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda value: (
            value.effective_as_of_utc, value.knowledge_cutoff_utc, value.derived_occurrence_id,
        )))[:limit]


class _LocalOwner:
    def __init__(
        self, raw_source: f.OptionTimeSourceV1, parent_reads: f.OptionTimeReadsV1,
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._parent_reads = raw_source, parent_reads
        self._state, self._utc_now = state, utc_now
        self.reads = _LocalReads(state)

    def materialise(self, request: f.OptionTimeRequestV1) -> f.OptionTimeLocalOccurrenceV1 | None:
        if type(request) is not f.OptionTimeRequestV1:
            raise TypeError("exact D003 option-time request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _local_request_check(request)
            if now < request.knowledge_cutoff_utc:
                return None
            parent = self._parent_reads.get_derived_occurrence(
                request.predecessor_occurrence_ids[0],
            )
            if type(parent) is not f.OptionTimeOccurrenceV1:
                return None
            selected = source.live_local_roles(self._source, request.knowledge_cutoff_utc)
            if (
                native.canonical(parent.original_observations)
                != native.canonical(tuple(selected[r][0] for r in ("R002", "R003")))
                or native.canonical(parent.selected_projections)
                != native.canonical(tuple(selected[r][1] for r in ("R002", "R003")))
            ):
                return None
            originals, projections = (selected["R004"][0],), (selected["R004"][1],)
            result = _local_calculate(request, originals, projections, parent)
            row = f.OptionTimeLocalOccurrenceV1(
                owner_object_id="M02",
                owner_namespace=LOCAL_NAMESPACE,
                implementation_brief_sha256=source.LOCAL_BRIEF,
                derived_signal_id=LOCAL_SIGNAL,
                derived_occurrence_id="pending",
                request=request,
                definition=LOCAL_DEFINITION,
                source_policy_sha256=source.POLICY_SHA,
                source_profile_ref=LOCAL_PROFILE,
                projection_mappings=(source.mapping_for("R004"),),
                original_observations=originals,
                selected_projections=projections,
                predecessor_occurrence_ids=request.predecessor_occurrence_ids,
                predecessor=parent,
                zone_policy_ref=LOCAL_ZONE_REF,
                result=result,
                units=LOCAL_DEFINITION.units,
                result_shape=LOCAL_DEFINITION.result_shape,
                effective_as_of_utc=request.as_of_utc,
                knowledge_cutoff_utc=request.knowledge_cutoff_utc,
                calculated_at_utc=now,
            )
            row = replace(row, derived_occurrence_id=codec.local_identity(row))
        except (TypeError, ValueError, ArithmeticError, KeyError):
            return None
        return cast(f.OptionTimeLocalOccurrenceV1, self._state.append(row))


def build_local_owner(
    admission: f.OwnerAdmissionV1, raw_source: f.OptionTimeSourceV1,
    parent_storage: f.SQLiteReadStorageV1, storage: f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.OptionTimeLocalOwnerV1:
    source.check_local_admission(admission)
    if (
        type(raw_source) is not f.OptionTimeSourceV1
        or not raw_source._matches_admission(admission)
        or type(parent_storage) is not f.SQLiteReadStorageV1
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("unadmitted D003 source/parent/storage/clock")
    parent_reads = f.create_option_time_reader(
        admission=f.OwnerAdmissionV1("M02", source.BRIEF), storage=parent_storage,
    )
    return _LocalOwner(raw_source, parent_reads, _local_store(storage), utc_now)


def build_local_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.OptionTimeLocalReadsV1:
    source.check_local_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D003 read-only storage")
    return _LocalReads(_local_store(storage))


EXPIRY_SIGNAL = "D086"
EXPIRY_PROFILE = f.VersionRefV1("t01-option-time-d086", 1)
EXPIRY_NAMESPACE = "neutral_market_measurement_truth/option_time_expiry/v1"
EXPIRY_CLOCK_REF = f.VersionRefV1("t01-option-expiry-clock", 1)
EXPIRY_DEFINITION = f.CalculationDefinitionV1(
    EXPIRY_SIGNAL,
    "T01-D086-OPTION-TIME-DEF-V1",
    "K01_TIME",
    ("Exact elapsed microseconds from actual D001 UTC to configured expiry instant "
     "divided by 31536000000000; negative refuses."),
    ("R013",),
    ("D001",),
    "P_TIME",
    "years",
    "exact_ratio",
    (
        *DEFINITION.authority_refs[:3],
        f.AuthorityArtifactRefV1(source.EXPIRY_BRIEF_PATH, source.EXPIRY_BRIEF),
    ),
)


def _expiry_request_check(request: f.OptionTimeRequestV1) -> None:
    if type(request) is not f.OptionTimeRequestV1:
        raise TypeError("exact D086 option-time request required")
    f._Validated.__post_init__(request)
    policy = source.expiry_policy()
    if request.frame_id not in policy["frames"]:
        raise ValueError("unadmitted D086 option-time frame")
    clocks = policy["frames"][request.frame_id]["calculation_clocks"][EXPIRY_SIGNAL]
    if (
        request.derived_signal_id != EXPIRY_SIGNAL
        or request.subject_instrument != source.SUBJECT
        or request.source_profile_ref != EXPIRY_PROFILE
        or request.calculation_definition_version
        != EXPIRY_DEFINITION.calculation_definition_version
        or len(request.predecessor_occurrence_ids) != 1
        or request.as_of_utc != datetime.fromisoformat(clocks["as_of_utc"])
        or request.knowledge_cutoff_utc != datetime.fromisoformat(clocks["knowledge_cutoff_utc"])
    ):
        raise ValueError("unadmitted D086 option-time frame/clock/profile")


def _expiry_calculate(
    request: f.OptionTimeRequestV1,
    originals: tuple[raw.RawObservationOccurrenceV1, ...],
    projections: tuple[raw.ProjectedRawValueV1, ...],
    parent: f.OptionTimeOccurrenceV1,
) -> f.ExactRatioV1:
    from fractions import Fraction
    from zoneinfo import ZoneInfo

    _expiry_request_check(request)
    _validate(parent)
    if (
        len(originals) != 1 or len(projections) != 1
        or request.predecessor_occurrence_ids != (parent.derived_occurrence_id,)
        or parent.request.subject_instrument != request.subject_instrument
        or parent.request.frame_id != request.frame_id
        or parent.effective_as_of_utc != request.as_of_utc
        or parent.result != request.as_of_utc
        or not (
            parent.knowledge_cutoff_utc <= parent.calculated_at_utc <= request.knowledge_cutoff_utc
        )
    ):
        raise ValueError("D086 actual parent alignment or visibility mismatch")
    source.validate_expiry_roles(
        parent.original_observations + originals, parent.selected_projections + projections,
    )
    original, = originals
    projection, = projections
    policy = source.expiry_policy()
    clock = policy["expiry_policy"]
    record = original.native_record
    expected_contract = policy["contract_identity"]["contract"]
    if (
        original.subject_instrument != source.SUBJECT
        or original.native_units != "date_string"
        or original.source_temporal_kind != "receipt_only"
        or original.source_timestamp_raw is not None
        or original.source_timezone_native is not None
        or original.received_ts_utc > request.knowledge_cutoff_utc
        or original.native_identifier != "Contract.lastTradeDateOrContractMonth"
        or source._path(record, ("sample", "id")) != request.frame_id
        or source._path(record, ("value", "role")) != "expiry_date"
        or any(
            record[key] != value for key, value in policy["contract_identity"].items()
            if key != "contract"
        )
        or any(
            source._path(record, ("contract", key)) != value
            for key, value in expected_contract.items()
        )
        or type(projection.native_value) is not str
        or projection.native_field_path != ("contract", "lastTradeDateOrContractMonth")
        or projection.native_value
        != source._path(record, ("contract", "lastTradeDateOrContractMonth"))
    ):
        raise ValueError("D086 actual R013 role/contract/receipt invariant")
    date_text = projection.native_value
    actual_date = datetime.strptime(date_text, "%Y%m%d").date()
    if (
        actual_date.strftime("%Y%m%d") != date_text
        or actual_date.isoformat() != clock["expiry_date"]
        or source._path(record, ("expiry", "date")) != clock["expiry_date"]
        or clock["subject"] != source.SUBJECT
        or clock["ref"] != "t01-option-expiry-clock/1"
        or clock["iana_zone"] != "America/New_York"
        or clock["day_count"] != "ACT/365F"
        or clock["seconds_per_year"] != 31536000
        or clock["status"] != "CONTROLLED_SYNTHETIC_NOT_OFFICIAL"
    ):
        raise ValueError("D086 actual R013 expiry date/configuration mismatch")
    local = datetime.fromisoformat(clock["local_time"])
    instant = datetime.fromisoformat(clock["expiry_instant_utc"])
    f._utc(instant)
    zoned = instant.astimezone(ZoneInfo(clock["iana_zone"]))
    if (
        local.tzinfo is None or local.date() != actual_date
        or zoned.isoformat() != clock["local_time"]
        or local.astimezone(UTC) != instant
    ):
        raise ValueError("D086 inconsistent expiry date/zone/local/UTC policy")
    delta = instant - parent.result
    micros = (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds
    if micros < 0:
        raise ValueError("D086 negative elapsed maturity")
    ratio = Fraction(micros, 31536000000000)
    return f.ExactRatioV1(ratio.numerator, ratio.denominator)


def _validate_expiry(value: f.OptionTimeExpiryOccurrenceV1) -> None:
    if type(value) is not f.OptionTimeExpiryOccurrenceV1:
        raise TypeError("exact D086 option-time occurrence required")
    value.__post_init__()
    expected = _expiry_calculate(
        value.request, value.original_observations, value.selected_projections, value.predecessor,
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != EXPIRY_NAMESPACE
        or value.implementation_brief_sha256 != source.EXPIRY_BRIEF
        or value.derived_signal_id != EXPIRY_SIGNAL
        or value.definition != EXPIRY_DEFINITION
        or value.source_policy_sha256 != source.POLICY_SHA
        or value.source_profile_ref != EXPIRY_PROFILE
        or value.predecessor_occurrence_ids != value.request.predecessor_occurrence_ids
        or native.canonical(value.projection_mappings)
        != native.canonical((source.mapping_for("R013"),))
        or value.expiry_policy_ref != EXPIRY_CLOCK_REF
        or value.result != expected
        or value.units != EXPIRY_DEFINITION.units
        or value.result_shape != EXPIRY_DEFINITION.result_shape
        or value.effective_as_of_utc != value.request.as_of_utc
        or value.knowledge_cutoff_utc != value.request.knowledge_cutoff_utc
        or value.calculated_at_utc < value.knowledge_cutoff_utc
        or value.derived_occurrence_id != codec.expiry_identity(value)
    ):
        raise ValueError("D086 option-time durable semantic or identity mismatch")


def _expiry_store(storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1) -> RecordState:
    return RecordState(storage, codec.decode_expiry, _validate_expiry, encode=codec.encode_expiry)


class _ExpiryReads:
    def __init__(self, state: RecordState) -> None:
        self._state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str,
    ) -> f.OptionTimeExpiryOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty D086 occurrence identity required")
        return next(
            (value for value in self._state.all()
             if value.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.OptionTimeExpiryOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            derived_signal_id != EXPIRY_SIGNAL or subject_instrument != source.SUBJECT
            or type(limit) is not int or not 1 <= limit <= 64
        ):
            raise ValueError("bounded D086 option-time history required")
        rows = (
            value for value in self._state.all()
            if value.effective_as_of_utc <= effective_at_or_before_utc
            and value.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda value: (
            value.effective_as_of_utc, value.knowledge_cutoff_utc, value.derived_occurrence_id,
        )))[:limit]


class _ExpiryOwner:
    def __init__(
        self, raw_source: f.OptionTimeSourceV1, parent_reads: f.OptionTimeReadsV1,
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._source, self._parent_reads = raw_source, parent_reads
        self._state, self._utc_now = state, utc_now
        self.reads = _ExpiryReads(state)

    def materialise(self, request: f.OptionTimeRequestV1) -> f.OptionTimeExpiryOccurrenceV1 | None:
        if type(request) is not f.OptionTimeRequestV1:
            raise TypeError("exact D086 option-time request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _expiry_request_check(request)
            if now < request.knowledge_cutoff_utc:
                return None
            parent = self._parent_reads.get_derived_occurrence(
                request.predecessor_occurrence_ids[0],
            )
            if type(parent) is not f.OptionTimeOccurrenceV1:
                return None
            selected = source.live_expiry_roles(self._source, request.knowledge_cutoff_utc)
            if (
                native.canonical(parent.original_observations)
                != native.canonical(tuple(selected[r][0] for r in ("R002", "R003")))
                or native.canonical(parent.selected_projections)
                != native.canonical(tuple(selected[r][1] for r in ("R002", "R003")))
            ):
                return None
            originals, projections = (selected["R013"][0],), (selected["R013"][1],)
            result = _expiry_calculate(request, originals, projections, parent)
            row = f.OptionTimeExpiryOccurrenceV1(
                owner_object_id="M02",
                owner_namespace=EXPIRY_NAMESPACE,
                implementation_brief_sha256=source.EXPIRY_BRIEF,
                derived_signal_id=EXPIRY_SIGNAL,
                derived_occurrence_id="pending",
                request=request,
                definition=EXPIRY_DEFINITION,
                source_policy_sha256=source.POLICY_SHA,
                source_profile_ref=EXPIRY_PROFILE,
                projection_mappings=(source.mapping_for("R013"),),
                original_observations=originals,
                selected_projections=projections,
                predecessor_occurrence_ids=request.predecessor_occurrence_ids,
                predecessor=parent,
                expiry_policy_ref=EXPIRY_CLOCK_REF,
                result=result,
                units=EXPIRY_DEFINITION.units,
                result_shape=EXPIRY_DEFINITION.result_shape,
                effective_as_of_utc=request.as_of_utc,
                knowledge_cutoff_utc=request.knowledge_cutoff_utc,
                calculated_at_utc=now,
            )
            row = replace(row, derived_occurrence_id=codec.expiry_identity(row))
        except (TypeError, ValueError, ArithmeticError, KeyError):
            return None
        return cast(f.OptionTimeExpiryOccurrenceV1, self._state.append(row))


def build_expiry_owner(
    admission: f.OwnerAdmissionV1, raw_source: f.OptionTimeSourceV1,
    parent_storage: f.SQLiteReadStorageV1, storage: f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.OptionTimeExpiryOwnerV1:
    source.check_expiry_admission(admission)
    if (
        type(raw_source) is not f.OptionTimeSourceV1
        or not raw_source._matches_admission(admission)
        or type(parent_storage) is not f.SQLiteReadStorageV1
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("unadmitted D086 source/parent/storage/clock")
    parent_reads = f.create_option_time_reader(
        admission=f.OwnerAdmissionV1("M02", source.BRIEF), storage=parent_storage,
    )
    return _ExpiryOwner(raw_source, parent_reads, _expiry_store(storage), utc_now)


def build_expiry_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.OptionTimeExpiryReadsV1:
    source.check_expiry_admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D086 read-only storage")
    return _ExpiryReads(_expiry_store(storage))
