"""Fixed window selection and D016 signed-volume law over actual public evidence."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, spread
from ._evaluation import decode as decode_record
from ._record_store import RecordState
from ._selection import _same_content, eligible
from ._trade_direction import POLICY as SIGN_POLICY
from ._trade_direction import validate as validate_sign

BRIEF = "bcf43f272179b7291a9851a5a1731efc7a90fb156d92de7108e41683045dae01"
NAMESPACE = "neutral_market_measurement_truth/window/v1"
DEFINITION = f.CalculationDefinitionV1(
    "D016",
    "D016-SIGNED-VOLUME-1",
    "K08_RULE_BUCKET_POLICY",
    "sum(matched_sign * size)",
    ("R121",),
    ("D015",),
    "P_RULE",
    "shares",
    "scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
POLICY = replace(
    SIGN_POLICY,
    context_id="mmt-trade-window",
    maximum_staleness=timedelta(seconds=300),
    maximum_skew=timedelta(0),
)
MAPPING = raw_api.RawSignalProjectionMappingV1(
    "mmt-trade-size",
    1,
    raw_api.RawSignalCatalogueId("R121"),
    POLICY.source_provider,
    POLICY.source_variant,
    ("trade", "size"),
    "shares",
    (),
)
UNIT = f.UnitConventionVersionV1(
    "mmt-trade-shares", 1, "shares", "shares", Decimal("1"), Decimal("0")
)
WINDOWS = {f"mmt-signed-volume-{seconds}s": seconds for seconds in (1, 5, 60, 300)}
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-trade-session", 1),
    datetime(2026, 10, 20, 11, 50, 10, tzinfo=UTC),
    datetime(2026, 10, 20, 12, 10, 10, tzinfo=UTC),
    datetime(2026, 10, 20, 11, 50, 10, tzinfo=UTC),
)


def _admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1:
        raise TypeError("exact owner admission required")
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D016 admission required")


def _request(request: f.WindowCalculationRequestV1, now: datetime) -> int:
    c = request.calculation
    seconds = WINDOWS.get(c.parameter_set_ref.context_id, 0)
    if not seconds:
        raise ValueError("unadmitted window")
    expected = f.CalculationRequestV1(
        "D016",
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(f"mmt-signed-volume-{seconds}s", 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (request.context.ref,),
        (
            f.RawInputBindingV1(
                "R121",
                f.VersionRefV1(MAPPING.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            ),
        ),
    )
    start = c.as_of_utc - timedelta(seconds=seconds)
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
        or not request.context.history_complete_from_utc <= start
        or not request.context.session_start_utc
        <= start
        < c.as_of_utc
        < request.context.session_end_utc
    ):
        raise ValueError("unsupported window/context or insufficient complete history")
    return seconds


def _identity(value: f.WindowMeasurementOccurrenceV1) -> str:
    payload = {
        item.name: getattr(value, item.name)
        for item in fields(value)
        if item.name not in {"derived_occurrence_id", "calculated_at_utc"}
    }
    return "mmtwindow1:" + hashlib.sha256(canonical(payload)).hexdigest()


def _lineage(
    item: raw_api.ProjectedRawValueV1, request: f.CalculationRequestV1
) -> f.RawInputLineageV1:
    event = eligible(item, MAPPING, POLICY, request)
    if event is None or type(item.native_value) is not Decimal or item.native_value < 0:
        raise ValueError("inadmissible selected size")
    return f.RawInputLineageV1(
        "R121",
        item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPING.mapping_id, 1),
        f.VersionRefV1(UNIT.context_id, 1),
        item,
        item.native_value,
        event,
    )


def _sizes(
    reader: f.RawProjectionReaderV1, c: f.CalculationRequestV1, seconds: int
) -> tuple[f.RawInputLineageV1, ...]:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, raw_api.ProjectedRawValueV1] = {}
    selected = []
    for _ in range(POLICY.history_page_limit):
        page = reader.list_projected_raw_history(
            MAPPING.raw_signal_catalogue_id,
            mappings=(MAPPING,),
            subject_instrument="NVDA",
            received_at_or_before_utc=c.knowledge_cutoff_utc,
            event_at_or_before_utc=c.as_of_utc,
            limit=POLICY.history_page_size,
            cursor=cursor,
        )
        if (
            type(page) is not raw_api.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple
            or len(page.items) > POLICY.history_page_size
        ):
            raise ValueError("incomplete size history")
        for item in page.items:
            if type(item) is not raw_api.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(raw_api.observation_occurrence_id("id")):
                raise ValueError("malformed projection")
            identity = item.observation_occurrence_id.value
            if identity in seen:
                if not _same_content(seen[identity], item):
                    raise ValueError("conflicting trade")
                continue
            seen[identity] = item
            event = datetime.fromisoformat(str(item.source_timestamp_raw).replace("Z", "+00:00"))
            f._utc(event)
            if c.as_of_utc - timedelta(seconds=seconds) < event <= c.as_of_utc:
                selected.append(_lineage(item, c))
        cursor = page.next_cursor
        if cursor is None:
            break
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            raise ValueError("incomplete size paging")
        cursors.add(cursor)
    else:
        raise ValueError("size history bound exhausted")
    return tuple(
        sorted(
            selected, key=lambda x: (x.event_time_utc, x.observation_occurrence_id), reverse=True
        )
    )


def _total(
    lines: tuple[f.RawInputLineageV1, ...],
    predecessors: tuple[f.TradeDirectionOccurrenceV1, ...],
    request: f.WindowCalculationRequestV1,
    now: datetime,
) -> Decimal:
    if not lines or len(lines) != len(predecessors):
        raise ValueError("empty window or incomplete trade/sign match")
    if len({x.observation_occurrence_id for x in lines}) != len(lines):
        raise ValueError("duplicate trade")
    if tuple(p.derived_occurrence_id for p in predecessors) != request.predecessor_occurrence_ids:
        raise ValueError("predecessor identity/order mismatch")
    total = Decimal("0")
    for line, p in zip(lines, predecessors, strict=True):
        validate_sign(p)
        trade = p.raw_input_lineage[0]
        a, b = line.projection, trade.projection
        if (
            p.result == 0
            or p.calculated_at_utc > now
            or p.knowledge_cutoff_utc != request.calculation.knowledge_cutoff_utc
            or p.effective_as_of_utc > request.calculation.as_of_utc
            or canonical(
                (
                    line.observation_occurrence_id,
                    line.event_time_utc,
                    a.subject_instrument,
                    a.source_provider,
                    a.source_variant,
                    a.ingestion_sequence_scope,
                    a.ingestion_sequence,
                    a.received_ts_utc,
                )
            )
            != canonical(
                (
                    trade.observation_occurrence_id,
                    trade.event_time_utc,
                    b.subject_instrument,
                    b.source_provider,
                    b.source_variant,
                    b.ingestion_sequence_scope,
                    b.ingestion_sequence,
                    b.received_ts_utc,
                )
            )
        ):
            raise ValueError("unclassified or incompatible matched trade")
        contribution = line.canonical_value if p.result > 0 else line.canonical_value.copy_negate()
        result = spread(contribution.copy_negate(), total)
        if result is None:
            raise ValueError("exact sum failed")
        total = result
    return total


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence required")
    f._Validated.__post_init__(value)
    seconds = _request(value.request, value.calculated_at_utc)
    c = value.request.calculation
    parameter = f.CalculationParameterSetV1(
        c.parameter_set_ref.context_id, 1, "P_RULE", "NVDA", ("NVDA",)
    )
    if (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D016"
        or value.window_seconds != seconds
        or value.units != "shares"
        or value.result_shape != "scalar_decimal"
        or value.effective_as_of_utc != c.as_of_utc
        or value.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or canonical(
            (
                value.definition,
                value.parameter_set,
                value.input_selection_policy,
                value.unit_conventions,
                value.projection_mappings,
            )
        )
        != canonical((DEFINITION, parameter, POLICY, (UNIT,), (MAPPING,)))
    ):
        raise ValueError("unadmitted window metadata")
    lines = value.raw_input_lineage
    if lines != tuple(
        sorted(lines, key=lambda x: (x.event_time_utc, x.observation_occurrence_id), reverse=True)
    ):
        raise ValueError("noncanonical trade ordering")
    for line in lines:
        if (
            canonical(line) != canonical(_lineage(line.projection, c))
            or not c.as_of_utc - timedelta(seconds=seconds) < line.event_time_utc <= c.as_of_utc
        ):
            raise ValueError("invalid window lineage")
    if canonical(value.result) != canonical(
        _total(
            lines,
            cast(tuple[f.TradeDirectionOccurrenceV1, ...], value.predecessors),
            value.request,
            value.calculated_at_utc,
        )
    ) or value.derived_occurrence_id != _identity(value):
        raise ValueError("window equation/identity mismatch")


def _decode(payload: bytes) -> f.WindowMeasurementOccurrenceV1:
    return cast(
        f.WindowMeasurementOccurrenceV1, decode_record(payload, f.WindowMeasurementOccurrenceV1)
    )


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str:
            raise TypeError("exact identity string required")
        if not derived_occurrence_id:
            raise ValueError("nonempty identity required")
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
    ) -> tuple[f.WindowMeasurementOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            type(limit) is not int
            or type(derived_signal_id) is not str
            or type(subject_instrument) is not str
        ):
            raise TypeError("exact history argument types required")
        if not 1 <= limit <= 1000 or not derived_signal_id or not subject_instrument:
            raise ValueError("invalid history identifiers/limit")
        return tuple(
            sorted(
                (
                    v
                    for v in self.state.all()
                    if v.derived_signal_id == derived_signal_id
                    and v.request.calculation.subject_instrument == subject_instrument
                    and v.effective_as_of_utc <= effective_at_or_before_utc
                    and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
                ),
                key=lambda v: (
                    v.effective_as_of_utc,
                    v.knowledge_cutoff_utc,
                    v.derived_occurrence_id,
                ),
                reverse=True,
            )[:limit]
        )


class _Owner:
    def __init__(
        self,
        state: RecordState,
        raw: f.RawProjectionReaderV1,
        predecessor: f.MeasurementTradeDirectionReadsV1,
        now: Callable[[], datetime],
    ) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact window request required")
        now = self.now()
        f._utc(now)
        try:
            seconds = _request(request, now)
            lines = _sizes(self.raw, request.calculation, seconds)
            predecessors = tuple(
                self.predecessor.get_derived_occurrence(i)
                for i in request.predecessor_occurrence_ids
            )
            if any(p is None for p in predecessors):
                return None
            signs = cast(tuple[f.TradeDirectionOccurrenceV1, ...], predecessors)
            total = _total(lines, signs, request, now)
            c = request.calculation
            value = f.WindowMeasurementOccurrenceV1(
                "M02",
                NAMESPACE,
                BRIEF,
                "D016",
                "pending",
                request,
                DEFINITION,
                f.CalculationParameterSetV1(
                    c.parameter_set_ref.context_id, 1, "P_RULE", "NVDA", ("NVDA",)
                ),
                POLICY,
                (UNIT,),
                (MAPPING,),
                lines,
                signs,
                seconds,
                total,
                "shares",
                "scalar_decimal",
                c.as_of_utc,
                c.knowledge_cutoff_utc,
                now,
            )
            value = replace(value, derived_occurrence_id=_identity(value))
            validate(value)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | f.MeasurementWindowReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    from . import (
        _correlation_matrix,
        _cross_section_dispersion,
        _international_returns,
        _jump_variation,
        _log_return,
        _macro_changes,
        _macro_surprise,
        _realised_volatility,
        _relative_market_return,
        _relative_sector_return,
        _return_acceleration,
        _session_range,
        _session_returns,
        _session_vwap,
        _true_range,
        _underlying_returns,
        _volatility_terms,
        _volume_baseline,
        _vwap_comparison,
        _vwap_returns,
    )

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 == _cross_section_dispersion.BRIEF
    ):
        return _cross_section_dispersion.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 == _correlation_matrix.BRIEF
    ):
        return _correlation_matrix.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 == _relative_sector_return.BRIEF
    ):
        return _relative_sector_return.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 == _relative_market_return.BRIEF
    ):
        return _relative_market_return.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 in _underlying_returns.BRIEFS.values()
    ):
        return _underlying_returns.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 in _international_returns.BRIEFS.values()
    ):
        return _international_returns.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 in _macro_surprise.BRIEFS.values()
    ):
        return _macro_surprise.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 in _volatility_terms.BRIEFS.values()
    ):
        return _volatility_terms.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.implementation_brief_sha256 in _macro_changes.BRIEFS.values()
    ):
        return _macro_changes.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _jump_variation.BRIEF
    ):
        return _jump_variation.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _true_range.BRIEF
    ):
        return _true_range.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _vwap_returns.BRIEFS.values()
    ):
        return _vwap_returns.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _volume_baseline.BRIEFS.values()
    ):
        return _volume_baseline.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _realised_volatility.BRIEFS.values()
    ):
        return _realised_volatility.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _session_range.BRIEF
    ):
        return _session_range.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _return_acceleration.BRIEF
    ):
        return _return_acceleration.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _session_returns.BRIEFS.values()
    ):
        return _session_returns.build_owner(admission, raw, predecessor, storage, now)

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _log_return.BRIEFS.values()
    ):
        return _log_return.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _vwap_comparison.BRIEF
    ):
        return _vwap_comparison.build_owner(admission, raw, predecessor, storage, now)

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _session_vwap.BRIEF
    ):
        return _session_vwap.build_owner(
            admission,
            raw,
            cast(f.MeasurementTradeDirectionReadsV1 | None, predecessor),
            storage,
            now,
        )
    _admission(admission)
    if (
        type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
        or predecessor is None
        or not callable(getattr(predecessor, "get_derived_occurrence", None))
    ):
        raise TypeError("declared window dependencies required")
    return _Owner(
        RecordState(storage, _decode, validate),
        raw,
        cast(f.MeasurementTradeDirectionReadsV1, predecessor),
        now,
    )


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1
) -> f.MeasurementWindowReadsV1:
    from . import (
        _correlation_matrix,
        _cross_section_dispersion,
        _international_returns,
        _jump_variation,
        _log_return,
        _macro_changes,
        _macro_surprise,
        _realised_volatility,
        _relative_market_return,
        _relative_sector_return,
        _return_acceleration,
        _session_range,
        _session_returns,
        _session_vwap,
        _true_range,
        _underlying_returns,
        _volatility_terms,
        _volume_baseline,
        _vwap_comparison,
        _vwap_returns,
    )

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 == _cross_section_dispersion.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _cross_section_dispersion.validate))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 == _correlation_matrix.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _correlation_matrix.validate))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 == _relative_sector_return.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _relative_sector_return.validate))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 == _relative_market_return.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _relative_market_return.validate))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _underlying_returns.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _underlying_returns.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _international_returns.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _international_returns.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _macro_surprise.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _macro_surprise.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _volatility_terms.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _volatility_terms.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _macro_changes.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _macro_changes.validator(admission)))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _jump_variation.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _jump_variation.validator(admission)))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _true_range.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _true_range.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _vwap_returns.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _vwap_returns.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _volume_baseline.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _volume_baseline.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _realised_volatility.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _realised_volatility.validator(admission)))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _session_range.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _session_range.validate))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _return_acceleration.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _return_acceleration.validate))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _session_returns.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _session_returns.validator(admission)))

    if (
        type(admission) is f.OwnerAdmissionV1
        and admission.object_id == "M02"
        and admission.implementation_brief_sha256 in _log_return.BRIEFS.values()
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _log_return.validator(admission)))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _vwap_comparison.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _vwap_comparison.validate))

    if type(admission) is f.OwnerAdmissionV1 and admission == f.OwnerAdmissionV1(
        "M02", _session_vwap.BRIEF
    ):
        if type(storage) is not f.SQLiteReadStorageV1:
            raise TypeError("exact read-only storage required")
        return _Reads(RecordState(storage, _decode, _session_vwap.validate))
    _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only storage required")
    return _Reads(RecordState(storage, _decode, validate))
