"""D017 session selection and exact weighted arithmetic; shared window/store reused."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical
from ._record_store import RecordState
from ._selection import _same_content, eligible
from ._window import NAMESPACE, _decode, _identity, _Reads

BRIEF = "b3e7b29f882d4f8ae698c8450d92ada08b3625c2effa29359f59fd50f5a3cf28"
DEFINITION = f.CalculationDefinitionV1(
    "D017",
    "D017-SESSION-VWAP-1",
    "K02_ALGEBRA",
    "sum(price * size) / sum(size)",
    ("R120", "R121"),
    (),
    "P_BASIC",
    "price",
    "scalar_exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-session-vwap", 1, "P_BASIC", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-vwap-selection",
    1,
    ("subject_instrument",),
    timedelta(hours=1),
    timedelta(0),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
MAPPINGS = tuple(
    raw_api.RawSignalProjectionMappingV1(
        "mmt-trade-" + name,
        1,
        raw_api.RawSignalCatalogueId(rid),
        POLICY.source_provider,
        POLICY.source_variant,
        ("trade", name),
        units,
        (),
    )
    for name, rid, units in (("price", "R120", "price"), ("size", "R121", "shares"))
)
UNITS = (
    f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0")),
    f.UnitConventionVersionV1(
        "mmt-trade-shares", 1, "shares", "shares", Decimal("1"), Decimal("0")
    ),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-vwap-session", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
    datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)


def _request(request: f.WindowCalculationRequestV1, now: datetime) -> int:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D017",
        "NVDA",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,),
        tuple(
            f.RawInputBindingV1(
                mapping.raw_signal_catalogue_id.value,
                f.VersionRefV1(mapping.mapping_id, 1),
                f.VersionRefV1(unit.context_id, 1),
                "NVDA",
            )
            for mapping, unit in zip(MAPPINGS, UNITS, strict=True)
        ),
    )
    elapsed = c.as_of_utc - CONTEXT.session_start_utc
    if (
        canonical(c) != canonical(expected)
        or request.context != CONTEXT
        or request.predecessor_occurrence_ids
        or elapsed.microseconds
        or not CONTEXT.history_complete_from_utc
        <= CONTEXT.session_start_utc
        <= c.as_of_utc
        < CONTEXT.session_end_utc
        or not c.as_of_utc <= c.knowledge_cutoff_utc <= now
    ):
        raise ValueError("unsupported/incomplete session context")
    return elapsed.days * 86400 + elapsed.seconds


def _lineage(
    item: raw_api.ProjectedRawValueV1, index: int, c: f.CalculationRequestV1
) -> f.RawInputLineageV1:
    event = eligible(item, MAPPINGS[index], POLICY, c)
    if (
        event is None
        or not CONTEXT.session_start_utc <= event <= c.as_of_utc
        or type(item.native_value) is not Decimal
        or item.native_value < 0
    ):
        raise ValueError("inadmissible selected trade field")
    return f.RawInputLineageV1(
        MAPPINGS[index].raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(MAPPINGS[index].mapping_id, 1),
        f.VersionRefV1(UNITS[index].context_id, 1),
        item,
        item.native_value,
        event,
    )


def _history(
    reader: f.RawProjectionReaderV1, index: int, c: f.CalculationRequestV1
) -> dict[str, f.RawInputLineageV1]:
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, raw_api.ProjectedRawValueV1] = {}
    result = {}
    mapping = MAPPINGS[index]
    for _ in range(POLICY.history_page_limit):
        page = reader.list_projected_raw_history(
            mapping.raw_signal_catalogue_id,
            mappings=(mapping,),
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
            raise ValueError("incomplete session history")
        for item in page.items:
            if type(item) is not raw_api.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(raw_api.observation_occurrence_id("id")):
                raise ValueError("invalid native occurrence identity")
            identity = item.observation_occurrence_id.value
            if identity in seen:
                if not _same_content(seen[identity], item):
                    raise ValueError("conflicting native trade")
                continue
            seen[identity] = item
            if type(item.source_timestamp_raw) is not str:
                raise ValueError("source event required")
            event = datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))
            f._utc(event)
            if CONTEXT.session_start_utc <= event <= c.as_of_utc:
                result[identity] = _lineage(item, index, c)
        cursor = page.next_cursor
        if cursor is None:
            return result
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            raise ValueError("incomplete session paging")
        cursors.add(cursor)
    raise ValueError("session history bound exhausted")


def _produce(
    request: f.WindowCalculationRequestV1, lines: tuple[f.RawInputLineageV1, ...], now: datetime
) -> f.WindowMeasurementOccurrenceV1:
    seconds = _request(request, now)
    if not lines or len(lines) % 2:
        raise ValueError("nonempty complete price/size pairs required")
    numerator = Fraction(0)
    denominator = Fraction(0)
    keys = []
    for offset in range(0, len(lines), 2):
        price, size = lines[offset : offset + 2]
        for index, line in enumerate((price, size)):
            if canonical(line) != canonical(_lineage(line.projection, index, request.calculation)):
                raise ValueError("invalid selected lineage")
        a, b = price.projection, size.projection
        if canonical(
            (
                price.observation_occurrence_id,
                price.event_time_utc,
                a.subject_instrument,
                a.source_provider,
                a.source_variant,
                a.ingestion_sequence_scope,
                a.ingestion_sequence,
                a.received_ts_utc,
            )
        ) != canonical(
            (
                size.observation_occurrence_id,
                size.event_time_utc,
                b.subject_instrument,
                b.source_provider,
                b.source_variant,
                b.ingestion_sequence_scope,
                b.ingestion_sequence,
                b.received_ts_utc,
            )
        ):
            raise ValueError("incompatible native trade pair")
        keys.append((price.event_time_utc, price.observation_occurrence_id))
        numerator += Fraction(price.canonical_value) * Fraction(size.canonical_value)
        denominator += Fraction(size.canonical_value)
    if (
        denominator <= 0
        or keys != sorted(keys)
        or len({identity for _, identity in keys}) != len(keys)
    ):
        raise ValueError("invalid denominator, duplicate trade or ordering")
    result = numerator / denominator
    c = request.calculation
    value = f.WindowMeasurementOccurrenceV1(
        "M02",
        NAMESPACE,
        BRIEF,
        "D017",
        "pending",
        request,
        DEFINITION,
        PARAMETER,
        POLICY,
        UNITS,
        MAPPINGS,
        lines,
        (),
        seconds,
        f.ExactRatioV1(result.numerator, result.denominator),
        "price",
        "scalar_exact_ratio",
        c.as_of_utc,
        c.knowledge_cutoff_utc,
        now,
    )
    return replace(value, derived_occurrence_id=_identity(value))


def validate(value: f.WindowMeasurementOccurrenceV1) -> None:
    if type(value) is not f.WindowMeasurementOccurrenceV1:
        raise TypeError("exact window occurrence required")
    f._Validated.__post_init__(value)
    expected = _produce(value.request, value.raw_input_lineage, value.calculated_at_utc)
    if canonical(value) != canonical(expected):
        raise ValueError("session VWAP metadata/equation/identity mismatch")


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
            _request(request, now)
            prices, sizes = (_history(self.raw, index, request.calculation) for index in (0, 1))
            if not prices or prices.keys() != sizes.keys():
                return None
            ordered = sorted(prices, key=lambda key: (prices[key].event_time_utc, key))
            lines = tuple(line for key in ordered for line in (prices[key], sizes[key]))
            value = _produce(request, lines, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.WindowMeasurementOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1,
    raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTradeDirectionReadsV1 | None,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> f.MeasurementWindowOwnerV1:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D017 admission required")
    if (
        predecessor is not None
        or type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or not callable(getattr(raw, "list_projected_raw_history", None))
    ):
        raise TypeError("declared raw-only window dependencies required")
    return _Owner(RecordState(storage, _decode, validate), raw, now)
