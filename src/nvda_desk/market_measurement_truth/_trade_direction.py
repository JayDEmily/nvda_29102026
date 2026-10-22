"""Fixed controlled D015; unchanged public M00 and actual D011 evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field, fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Protocol, get_type_hints

from nvda_desk.raw_signal_occurrence_truth import api as raw_api

from . import api as f
from ._catalogue import _AUTHORITY
from ._rational import canonical, capture, untagged, validate_evidence
from ._selection import _same_content, eligible, select

BRIEF = "84baa16665db5f8543eba3b1770dafcfb36cc5e8064b2f1837beb924713acb0d"
NAMESPACE = "neutral_market_measurement_truth/trade_direction/v1"
DEFINITION = f.CalculationDefinitionV1(
    "D015",
    "D015-TRADE-DIRECTION-1",
    "K08_RULE_BUCKET_POLICY",
    "quote_first_then_last_different_trade_else_0",
    ("R120", "R126", "R127"),
    ("D011",),
    "P_RULE",
    "sign",
    "enum_trade_sign",
    tuple(f.AuthorityArtifactRefV1(*r) for r in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1("mmt-trade-rule", 1, "P_RULE", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-pilot-selection",
    1,
    ("subject_instrument",),
    timedelta(seconds=60),
    timedelta(seconds=10),
    ("true_instant",),
    (),
    "foundation-pilot-fixture",
    "cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",
    100,
    1000,
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price", 1, "price", "price", Decimal("1"), Decimal("0"))
MAPPINGS = tuple(
    raw_api.RawSignalProjectionMappingV1(
        "mmt-trade-" + label,
        1,
        raw_api.RawSignalCatalogueId(rid),
        "foundation-pilot-fixture",
        "cash_quote_v1",
        path,
        "price",
        (),
    )
    for rid, label, path in (
        ("R120", "price", ("trade", "price")),
        ("R126", "bid", ("quote", "bid")),
        ("R127", "ask", ("quote", "ask")),
    )
)


def _admission(value: f.OwnerAdmissionV1) -> None:
    if type(value) is not f.OwnerAdmissionV1:
        raise TypeError("exact owner admission required")
    if value != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("exact D015 admission required")


def _decode(value: Any, hint: Any) -> Any:
    if hint in (f.TradeDirectionRequestV1, f.TradeDirectionOccurrenceV1):
        hints = get_type_hints(hint)
        if type(value) is not dict or set(value) != set(hints):
            raise ValueError("complete trade-direction record required")
        return hint(**{key: _decode(value[key], cls) for key, cls in hints.items()})
    return untagged(value, hint)


def decode(payload: bytes) -> f.TradeDirectionOccurrenceV1:
    value: f.TradeDirectionOccurrenceV1 = _decode(json.loads(payload), f.TradeDirectionOccurrenceV1)
    if canonical(value) != payload:
        raise ValueError("noncanonical trade-direction payload")
    validate(value)
    return value


def _logical(value: f.TradeDirectionOccurrenceV1) -> bytes:
    return canonical(
        {
            item.name: getattr(value, item.name)
            for item in fields(value)
            if item.name not in {"derived_occurrence_id", "calculated_at_utc"}
        }
    )


def _identity(value: f.TradeDirectionOccurrenceV1) -> str:
    return "mmtsign1:" + hashlib.sha256(_logical(value)).hexdigest()


def _request(calculation: f.CalculationRequestV1, now: datetime) -> bool:
    expected = f.CalculationRequestV1(
        "D015",
        "NVDA",
        calculation.as_of_utc,
        calculation.knowledge_cutoff_utc,
        "D015-TRADE-DIRECTION-1",
        f.VersionRefV1("mmt-trade-rule", 1),
        f.VersionRefV1("mmt-pilot-selection", 1),
        (),
        tuple(
            f.RawInputBindingV1(
                m.raw_signal_catalogue_id.value,
                f.VersionRefV1(m.mapping_id, 1),
                f.VersionRefV1("mmt-pilot-price", 1),
                "NVDA",
            )
            for m in MAPPINGS
        ),
    )
    return canonical(calculation) == canonical(expected) and (
        calculation.as_of_utc <= calculation.knowledge_cutoff_utc <= now
    )


def _lineage(pair: tuple[raw_api.ProjectedRawValueV1, datetime], index: int) -> f.RawInputLineageV1:
    item, when = pair
    mapping = MAPPINGS[index]
    if type(item.native_value) is not Decimal:
        raise ValueError("exact native Decimal required")
    return f.RawInputLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1("mmt-pilot-price", 1),
        item,
        item.native_value,
        when,
    )


def _event(item: raw_api.ProjectedRawValueV1) -> datetime:
    if type(item.source_timestamp_raw) is not str:
        raise ValueError("native event string required")
    return datetime.fromisoformat(item.source_timestamp_raw.replace("Z", "+00:00"))


def _prior(
    reader: f.RawProjectionReaderV1,
    request: f.CalculationRequestV1,
    trade: f.RawInputLineageV1,
) -> f.RawInputLineageV1 | None:
    """Complete finite prior history; current-price freshness is not a history bound."""
    cursor: str | None = None
    cursors: set[str] = set()
    seen: dict[str, raw_api.ProjectedRawValueV1] = {}
    candidates: list[tuple[raw_api.ProjectedRawValueV1, datetime]] = []
    for _ in range(POLICY.history_page_limit):
        page = reader.list_projected_raw_history(
            MAPPINGS[0].raw_signal_catalogue_id,
            mappings=(MAPPINGS[0],),
            subject_instrument="NVDA",
            received_at_or_before_utc=request.knowledge_cutoff_utc,
            event_at_or_before_utc=trade.event_time_utc,
            limit=POLICY.history_page_size,
            cursor=cursor,
        )
        if (
            type(page) is not raw_api.ProjectedRawHistoryPageV1
            or type(page.items) is not tuple
            or len(page.items) > POLICY.history_page_size
        ):
            raise ValueError("incomplete prior trade history")
        for item in page.items:
            if type(item) is not raw_api.ProjectedRawValueV1 or type(
                item.observation_occurrence_id
            ) is not type(raw_api.observation_occurrence_id("id")):
                raise ValueError("malformed prior trade identity")
            identity = item.observation_occurrence_id.value
            if identity in seen:
                if not _same_content(seen[identity], item):
                    raise ValueError("conflicting prior trade identity")
                continue
            seen[identity] = item
            try:
                event = _event(item)
                # Reuse every inherited eligibility check at its own event. This
                # removes only rolling staleness from the earlier-price search.
                when = eligible(item, MAPPINGS[0], POLICY, replace(request, as_of_utc=event))
            except (TypeError, ValueError, AttributeError):
                continue
            if (
                when is not None
                and when < trade.event_time_utc
                and item.native_value != trade.canonical_value
            ):
                candidates.append((item, when))
        cursor = page.next_cursor
        if cursor is None:
            break
        if (
            type(cursor) is not str
            or not re.fullmatch(r"[1-9][0-9]*", cursor)
            or cursor in cursors
            or not page.items
        ):
            raise ValueError("incomplete prior trade paging")
        cursors.add(cursor)
    else:
        raise ValueError("prior trade paging exhausted")
    if not candidates:
        return None
    chosen = max(candidates, key=lambda p: (p[1], p[0].received_ts_utc, p[0].ingestion_sequence))
    if sum(pair[1] == chosen[1] for pair in candidates) != 1:
        raise ValueError("ambiguous latest different trade event")
    return _lineage(chosen, 0)


def _sign(lineage: tuple[f.RawInputLineageV1, ...], midpoint: Decimal) -> int:
    price = lineage[0].canonical_value
    if price != midpoint:
        return 1 if price > midpoint else -1
    if len(lineage) == 3:
        return 0
    return 1 if price > lineage[3].canonical_value else -1


def validate(value: f.TradeDirectionOccurrenceV1) -> None:
    """Validate complete stored snapshots without source or predecessor readers."""
    f._Validated.__post_init__(value)
    c = value.request.calculation
    if not _request(c, value.calculated_at_utc) or (
        value.owner_object_id != "M02"
        or value.owner_namespace != NAMESPACE
        or value.implementation_brief_sha256 != BRIEF
        or value.derived_signal_id != "D015"
        or value.units != "sign"
        or value.result_shape != "enum_trade_sign"
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
        != canonical((DEFINITION, PARAMETER, POLICY, (UNIT,), MAPPINGS))
        or len(value.raw_input_lineage) not in (3, 4)
        or type(value.result) is not int
        or value.result not in (-1, 0, 1)
    ):
        raise ValueError("unadmitted trade-direction configuration or metadata")
    lines = value.raw_input_lineage
    trade = lines[0]
    anchor = replace(c, as_of_utc=trade.event_time_utc)
    for index, line in enumerate(lines):
        position = index if index < 3 else 0
        scoped = c if index == 0 else anchor
        if index == 3:
            scoped = replace(c, as_of_utc=line.event_time_utc)
        when = eligible(line.projection, MAPPINGS[position], POLICY, scoped)
        if when is None or canonical(line) != canonical(
            _lineage((line.projection, when), position)
        ):
            raise ValueError("invalid selected trade-direction raw lineage")
    if abs(lines[1].event_time_utc - lines[2].event_time_utc) > POLICY.maximum_skew:
        raise ValueError("trade-time quote skew")
    evidence = value.predecessor
    validate_evidence(evidence, value.calculated_at_utc)
    p = evidence.occurrence
    if (
        p.derived_signal_id != "D011"
        or p.calculation_definition_version != "D011-MIDPOINT-1"
        or p.derived_occurrence_id != value.request.midpoint_occurrence_id
        or p.effective_as_of_utc != trade.event_time_utc
        or p.knowledge_cutoff_utc != c.knowledge_cutoff_utc
        or any(
            version != 1
            for version in (
                evidence.parameter_set.version,
                evidence.input_selection_policy.version,
                *(unit.version for unit in evidence.unit_conventions),
                *(mapping.version for mapping in evidence.projection_mappings),
            )
        )
    ):
        raise ValueError("incompatible actual D011 predecessor")
    for new, old in zip(lines[1:3], p.raw_input_lineage, strict=True):
        a, b = new.projection, old.projection
        # Distinct fixture observations are correspondence, not aliases/native joins.
        if new.observation_occurrence_id == old.observation_occurrence_id or canonical(
            (
                a.subject_instrument,
                a.source_provider,
                a.source_variant,
                a.ingestion_sequence_scope,
                new.event_time_utc,
                a.received_ts_utc,
                a.native_value,
            )
        ) != canonical(
            (
                b.subject_instrument,
                b.source_provider,
                b.source_variant,
                b.ingestion_sequence_scope,
                old.event_time_utc,
                b.received_ts_utc,
                b.native_value,
            )
        ):
            raise ValueError("incompatible controlled quote correspondence")
    if len(lines) == 4 and (
        trade.canonical_value != p.result
        or lines[3].event_time_utc >= trade.event_time_utc
        or lines[3].canonical_value == trade.canonical_value
    ):
        raise ValueError("invalid last-different trade evidence")
    if value.result != _sign(lines, p.result) or value.derived_occurrence_id != _identity(value):
        raise ValueError("trade-direction equation or identity mismatch")


class _State(Protocol):
    def all(self) -> tuple[f.TradeDirectionOccurrenceV1, ...]: ...
    def append(self, value: f.TradeDirectionOccurrenceV1) -> f.TradeDirectionOccurrenceV1: ...


@dataclass
class _Memory:
    occurrences: dict[str, f.TradeDirectionOccurrenceV1] = field(default_factory=dict)

    def all(self) -> tuple[f.TradeDirectionOccurrenceV1, ...]:
        return tuple(self.occurrences.values())

    def append(self, value: f.TradeDirectionOccurrenceV1) -> f.TradeDirectionOccurrenceV1:
        validate(value)
        old = self.occurrences.get(value.derived_occurrence_id)
        if old is not None:
            if canonical(old) != canonical(replace(value, calculated_at_utc=old.calculated_at_utc)):
                raise f.PersistenceFailureV1("immutable trade-direction identity conflict")
            return old
        self.occurrences[value.derived_occurrence_id] = value
        return value


class _Reads:
    def __init__(self, state: _State) -> None:
        self._state = state

    def get_derived_occurrence(
        self, derived_occurrence_id: str
    ) -> f.TradeDirectionOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str:
            raise TypeError("occurrence ID must be a string")
        if not derived_occurrence_id:
            raise ValueError("occurrence ID must be nonempty")
        return next(
            (v for v in self._state.all() if v.derived_occurrence_id == derived_occurrence_id), None
        )

    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[f.TradeDirectionOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (
            type(limit) is not int
            or type(derived_signal_id) is not str
            or type(subject_instrument) is not str
        ):
            raise TypeError("exact history argument types required")
        if not 1 <= limit <= 1000 or not derived_signal_id or not subject_instrument:
            raise ValueError("nonempty history IDs and limit1..1000 required")
        return tuple(
            sorted(
                (
                    v
                    for v in self._state.all()
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
        state: _State,
        raw: f.RawProjectionReaderV1,
        predecessor: f.MeasurementReadsV1,
        now: Callable[[], datetime],
    ) -> None:
        self._state, self._raw, self._predecessor, self._now = state, raw, predecessor, now
        self._reads = _Reads(state)

    @property
    def reads(self) -> f.MeasurementTradeDirectionReadsV1:
        return self._reads

    def materialise(
        self, request: f.TradeDirectionRequestV1
    ) -> f.TradeDirectionOccurrenceV1 | None:
        if type(request) is not f.TradeDirectionRequestV1:
            raise TypeError("exact trade-direction request required")
        now = self._now()
        f._utc(now)
        if not _request(request.calculation, now):
            return None
        try:
            current = select(self._raw, MAPPINGS[0], POLICY, request.calculation)
            if current is None:
                return None
            trade = _lineage(current, 0)
            anchor = replace(request.calculation, as_of_utc=trade.event_time_utc)
            lines = [trade]
            for index in (1, 2):
                pair = select(self._raw, MAPPINGS[index], POLICY, anchor)
                if pair is None:
                    return None
                lines.append(_lineage(pair, index))
            predecessor = capture(self._predecessor, request.midpoint_occurrence_id)
            if predecessor is None:
                return None
            if trade.canonical_value == predecessor.occurrence.result:
                prior = _prior(self._raw, request.calculation, trade)
                if prior is not None:
                    lines.append(prior)
            value = f.TradeDirectionOccurrenceV1(
                "M02",
                NAMESPACE,
                BRIEF,
                "D015",
                "pending",
                request,
                DEFINITION,
                PARAMETER,
                POLICY,
                (UNIT,),
                MAPPINGS,
                tuple(lines),
                predecessor,
                _sign(tuple(lines), predecessor.occurrence.result),
                "sign",
                "enum_trade_sign",
                request.calculation.as_of_utc,
                request.calculation.knowledge_cutoff_utc,
                now,
            )
            value = replace(value, derived_occurrence_id=_identity(value))
            validate(value)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return self._state.append(value)


def build_owner(
    *,
    admission: f.OwnerAdmissionV1,
    raw_projection_reader: f.RawProjectionReaderV1,
    predecessor_reader: f.MeasurementReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> f.MeasurementTradeDirectionOwnerV1:
    _admission(admission)
    if not callable(utc_now):
        raise TypeError("clock must be callable")
    if type(storage) is f.MemoryStorageV1:
        state: _State = _Memory()
    elif type(storage) is f.SQLiteStorageV1:
        from ._trade_direction_sqlite import create_state

        state = create_state(storage)
    else:
        raise TypeError("exact trade-direction storage required")
    return _Owner(state, raw_projection_reader, predecessor_reader, utc_now)


def build_reader(
    *,
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteReadStorageV1,
) -> f.MeasurementTradeDirectionReadsV1:
    _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only storage required")
    from ._trade_direction_sqlite import _SQLiteState

    state = _SQLiteState(storage.database_path)
    state.all()
    return _Reads(state)
