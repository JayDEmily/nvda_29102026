"""Exact session range over three explicitly mapped fields of one native snapshot."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._log_return import UNIT
from ._record_store import RecordState
from ._session_returns import CONTEXT, S, configuration, lineage, mapping, select_line
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "ceb90718b21be71fd55a8ecb3f5e6eb15d27ca8eb3f357b68a0f809606652227"
MAPPINGS = (
    mapping("R039", "mmt-session-high", ("session", "high")),
    mapping("R040", "mmt-session-low", ("session", "low")),
    mapping("R037", "mmt-current-last", ("trade", "last")),
)
POLICY = replace(
    configuration("D022")[2],
    context_id="mmt-session-range-selection",
    maximum_staleness=timedelta(seconds=60),
)
DEFINITION = f.CalculationDefinitionV1(
    "D025",
    "D025-SESSION-RANGE-1",
    "K02_ALGEBRA",
    "(last - session_low) / (session_high - session_low)",
    ("R039", "R040", "R037"),
    (),
    "P_BASIC",
    "dimensionless",
    "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*x) for x in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-session-range", 1, "P_BASIC", "NVDA", ("NVDA",))
SESSION = r.RawSelectionIdentityV1((("session", S),))


def request_check(request: f.WindowCalculationRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D025",
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1(UNIT.context_id, 1),
                "NVDA",
            )
            for m in MAPPINGS
        ),
    )
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or not CONTEXT.history_complete_from_utc
        <= CONTEXT.session_start_utc
        <= c.as_of_utc
        < CONTEXT.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("incompatible session range request")


def produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    request_check(request, now)
    c = request.calculation
    if len(lines) != 3:
        raise ValueError("three native fields required")
    for line, m in zip(lines, MAPPINGS, strict=True):
        if canonical(line) != canonical(
            lineage(line.projection, c, m, POLICY, SESSION, c.as_of_utc)
        ):
            raise ValueError("invalid range role")
    names = (
        "observation_occurrence_id",
        "source_provider",
        "source_variant",
        "subject_instrument",
        "received_ts_utc",
        "ingestion_sequence",
        "ingestion_sequence_scope",
        "source_timestamp_raw",
        "source_timezone_native",
        "source_temporal_kind",
        "selection_identity",
    )
    snapshot = tuple(getattr(lines[0].projection, n) for n in names)
    if any(tuple(getattr(line.projection, n) for n in names) != snapshot for line in lines[1:]):
        raise ValueError("incompatible native snapshots")
    high, low, last = (Fraction(line.canonical_value) for line in lines)
    if high <= low or not low <= last <= high:
        raise ValueError("zero/reversed range or incompatible last")
    ratio = (last - low) / (high - low)
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D025",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        (UNIT,),
        MAPPINGS,
        lines,
        (),
        int((c.as_of_utc - CONTEXT.session_start_utc).total_seconds()),
        f.ExactRatioV1(ratio.numerator, ratio.denominator),
        "dimensionless",
        "exact_ratio",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(
        produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    ):
        raise ValueError("session range metadata/equation/identity mismatch")


class _Owner:
    def __init__(
        self, state: RecordState, raw: f.RawProjectionReaderV1, now: Callable[[], datetime]
    ) -> None:
        self.state, self.raw, self.now = state, raw, now
        self.reads = _Reads(state)

    def materialise(
        self, request: f.WindowCalculationRequestV1
    ) -> f.WindowMeasurementOccurrenceV1 | None:
        if type(request) is not f.WindowCalculationRequestV1:
            raise TypeError("exact window request required")
        now = self.now()
        f._utc(now)
        try:
            request_check(request, now)
            c = request.calculation
            lines = tuple(
                select_line(self.raw, c, m, POLICY, SESSION, c.as_of_utc) for m in MAPPINGS
            )
            value = produce(request, lines, now)
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
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D025 admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only session dependencies required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
