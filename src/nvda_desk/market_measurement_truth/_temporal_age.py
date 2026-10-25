"""D002 exact age with actual public D001 or actual collector receipt."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import cast

from nvda_desk.raw_signal_occurrence_truth import api as r

from . import _temporal
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState
from ._selection import _same_content

BRIEF = "1d7a4621010e87c6fe44254aeb88712ae2d3b61bf6d739a4ef3ef7c8b3a8477f"
NAMESPACE = "neutral_market_measurement_truth/temporal-age/v1"
T = _temporal.T
PROVIDER, VARIANT = _temporal.PROVIDER, _temporal.VARIANT
META = _temporal.META
MAPS = (
    r.RawSignalProjectionMappingV1(
        "mmt-d002-r001", 1, r.RawSignalCatalogueId("R001"), PROVIDER,
        VARIANT, ("time", "receipt"), "UTC_datetime", META,
    ),
    _temporal.MAPS[0],
)
UNITS = (
    f.UnitConventionVersionV1(
        "mmt-d002-receipt", 1, "UTC_datetime", "UTC_datetime", Decimal(1), Decimal(0),
    ),
    _temporal.UNITS[0],
)
DEFINITION = f.CalculationDefinitionV1(
    "D002", "D002-SOURCE-AGE-1", "K01_TIME",
    "cutoff minus true source event or actual collector receipt",
    ("R001", "R002"), ("D001",), "P_TIME", "seconds", "age_basis_seconds",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d002-controlled", 1, "P_TIME", "NVDA", ("NVDA",),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d002-selection", 1, ("subject_instrument", "sample.id"),
    timedelta(seconds=60), timedelta(0),
    ("true_instant", "receipt_only", "date_only"), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def _utc_text(value: datetime) -> str:
    f._utc(value)
    return value.isoformat().replace("+00:00", "Z")


def _request(request: f.TemporalAgeRequestV1, now: datetime) -> None:
    c = request.calculation
    expected = f.CalculationRequestV1(
        "D002", "NVDA", T, T, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1),
        f.VersionRefV1(POLICY.context_id, 1), (),
        tuple(f.RawInputBindingV1(
            mapping.raw_signal_catalogue_id.value,
            f.VersionRefV1(mapping.mapping_id, 1),
            f.VersionRefV1(unit.context_id, 1), "NVDA",
        ) for mapping, unit in zip(MAPS, UNITS, strict=True)),
    )
    f._utc(now)
    if (
        type(request) is not f.TemporalAgeRequestV1
        or canonical(c) != canonical(expected)
        or len(request.predecessor_occurrence_ids) > 1
        or now < T
    ):
        raise ValueError("unadmitted D002 source-age request")


def _line(item: r.ProjectedRawValueV1, role: int, c: f.CalculationRequestV1
          ) -> f.TemporalAgeRawLineageV1:
    mapping, unit = MAPS[role], UNITS[role]
    identity = r.RawSelectionIdentityV1((
        ("sample.id", "controlled-temporal-sample/1"),
        ("value.role", ("collector_receipt", "source_timestamp")[role]),
    ))
    if (
        type(item) is not r.ProjectedRawValueV1
        or item.raw_signal_catalogue_id != mapping.raw_signal_catalogue_id
        or item.projection_mapping_id != mapping.mapping_id
        or item.projection_mapping_version != mapping.version
        or item.native_field_path != mapping.native_field_path
        or item.native_units != mapping.native_units
        or item.source_provider != PROVIDER or item.source_variant != VARIANT
        or item.subject_instrument != "NVDA" or item.selection_identity != identity
        or item.ingestion_sequence_scope.value != POLICY.ingestion_sequence_scope
        or type(item.ingestion_sequence) is not int or item.ingestion_sequence <= 0
        or item.revision_vintage_native is not None
        or type(item.native_value) is not str
        or item.received_ts_utc > c.knowledge_cutoff_utc
    ):
        raise ValueError("unadmitted actual D002 source")
    f._utc(item.received_ts_utc)
    if role == 0:
        if (
            item.source_temporal_kind != "receipt_only"
            or item.source_timestamp_raw is not None
            or item.source_timezone_native is not None
            or item.native_value != _utc_text(item.received_ts_utc)
        ):
            raise ValueError("R001 must preserve actual collector receipt, not event")
        selected, basis = item.received_ts_utc, "collector_receipt"
    elif item.source_temporal_kind == "true_instant":
        if item.source_timestamp_raw != item.native_value:
            raise ValueError("R002 native true-instant mismatch")
        selected = _temporal._stamp(item.native_value).astimezone(UTC)
        if (
            selected > c.as_of_utc
            or selected > item.received_ts_utc
            or c.as_of_utc - selected > POLICY.maximum_staleness
        ):
            raise ValueError("R002 future or stale true instant")
        basis = "source_event"
    elif item.source_temporal_kind == "receipt_only":
        if item.source_timestamp_raw is not None or item.source_timezone_native is not None:
            raise ValueError("R002 receipt-only cannot claim an event timestamp")
        selected, basis = item.received_ts_utc, "collector_receipt"
    elif item.source_temporal_kind == "date_only":
        raise ValueError("date-only R002 has no age-producing instant")
    else:
        raise ValueError("unknown temporal kind")
    return f.TemporalAgeRawLineageV1(
        mapping.raw_signal_catalogue_id.value,
        item.observation_occurrence_id.value,
        f.VersionRefV1(mapping.mapping_id, 1),
        f.VersionRefV1(unit.context_id, 1),
        item, item.native_value, selected, basis,
    )


def _produce(
    request: f.TemporalAgeRequestV1, lines: tuple[f.TemporalAgeRawLineageV1, ...],
    predecessors: tuple[f.TemporalOccurrenceV1, ...], now: datetime,
) -> f.TemporalAgeOccurrenceV1:
    _request(request, now)
    c = request.calculation
    if len(lines) != 2 or any(
        canonical(line) != canonical(_line(line.projection, role, c))
        for role, line in enumerate(lines)
    ):
        raise ValueError("complete exact R001/R002 source required")
    receipt, temporal = lines
    if (
        receipt.projection.selection_identity is None
        or temporal.projection.selection_identity is None
        or receipt.projection.selection_identity.value_for("sample.id")
        != temporal.projection.selection_identity.value_for("sample.id")
        or receipt.projection.received_ts_utc != temporal.projection.received_ts_utc
    ):
        raise ValueError("incompatible collector and temporal sample")
    if temporal.time_basis == "source_event":
        if len(predecessors) != 1:
            raise ValueError("true instant needs actual D001")
        parent = predecessors[0]
        _temporal._validate(parent)
        if (
            parent.implementation_brief_sha256 != _temporal.BRIEF
            or parent.derived_signal_id != "D001"
            or parent.request.as_of_utc != c.as_of_utc
            or parent.knowledge_cutoff_utc != c.knowledge_cutoff_utc
            or parent.calculated_at_utc > now
            or parent.result != temporal.selected_time_utc
            or parent.raw_input_lineage[0].projection != temporal.projection
            or parent.raw_input_lineage[0].observation_occurrence_id
            != temporal.observation_occurrence_id
            or parent.raw_input_lineage[0].event_time_utc != temporal.selected_time_utc
        ):
            raise ValueError("D001 must be the same actual selected R002 event")
        selected = parent.result
    else:
        if predecessors or request.predecessor_occurrence_ids:
            raise ValueError("receipt-only must not fabricate D001")
        if (
            temporal.projection.source_temporal_kind != "receipt_only"
            or temporal.selected_time_utc != receipt.selected_time_utc
        ):
            raise ValueError("receipt-only source must use matching actual R001 receipt")
        selected = receipt.selected_time_utc
    if (
        tuple(p.derived_occurrence_id for p in predecessors)
        != request.predecessor_occurrence_ids
        or selected > c.knowledge_cutoff_utc
    ):
        raise ValueError("wrong predecessor or negative age")
    age = Decimal(
        (c.knowledge_cutoff_utc - selected).days * 86400
        + (c.knowledge_cutoff_utc - selected).seconds
    ) + Decimal((c.knowledge_cutoff_utc - selected).microseconds) / Decimal(1000000)
    value = f.TemporalAgeOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D002", "pending", request, DEFINITION,
        PARAMETER, POLICY, UNITS, MAPS, lines, predecessors,
        f.TemporalAgeV1(temporal.time_basis, age), "seconds", "age_basis_seconds",
        c.as_of_utc, c.knowledge_cutoff_utc, now,
    )
    payload = {
        field.name: getattr(value, field.name) for field in fields(value)
        if field.name not in {"derived_occurrence_id", "calculated_at_utc"}
    }
    return replace(value, derived_occurrence_id="mmtage1:" + hashlib.sha256(
        canonical(payload)
    ).hexdigest())


def _validate(value: f.TemporalAgeOccurrenceV1) -> None:
    if type(value) is not f.TemporalAgeOccurrenceV1:
        raise TypeError("exact D002 age record required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(
        value.request, value.raw_input_lineage, value.predecessors, value.calculated_at_utc,
    )):
        raise ValueError("D002 age source/predecessor/result mismatch")


def _decode(payload: bytes) -> f.TemporalAgeOccurrenceV1:
    return cast(f.TemporalAgeOccurrenceV1, decode(payload, f.TemporalAgeOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.TemporalAgeOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("exact nonempty derived identity required")
        return next(
            (v for v in self.state.all() if v.derived_occurrence_id == derived_occurrence_id),
            None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.TemporalAgeOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid D002 history query")
        return tuple(sorted(
            (
                v for v in self.state.all()
                if v.derived_signal_id == derived_signal_id
                and v.request.calculation.subject_instrument == subject_instrument
                and v.effective_as_of_utc <= effective_at_or_before_utc
                and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc
            ),
            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc, v.derived_occurrence_id),
            reverse=True,
        )[:limit])


class _Owner:
    def __init__(
        self, state: RecordState, raw: f.RawProjectionReaderV1,
        predecessor: f.MeasurementTemporalReadsV1, now: Callable[[], datetime],
    ) -> None:
        self.state, self.raw, self.predecessor, self.now = state, raw, predecessor, now
        self.reads = _Reads(state)

    def materialise(self, request: f.TemporalAgeRequestV1
                    ) -> f.TemporalAgeOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(request, now)
            selected = []
            for role, mapping in enumerate(MAPS):
                cursor: str | None = None
                cursors: set[str] = set()
                items: dict[str, r.ProjectedRawValueV1] = {}
                for _ in range(POLICY.history_page_limit):
                    page = self.raw.list_projected_raw_history(
                        mapping.raw_signal_catalogue_id, mappings=(mapping,),
                        subject_instrument="NVDA", received_at_or_before_utc=T,
                        event_at_or_before_utc=None, limit=POLICY.history_page_size,
                        cursor=cursor,
                    )
                    if (
                        type(page) is not r.ProjectedRawHistoryPageV1
                        or type(page.items) is not tuple
                    ):
                        raise ValueError("invalid D002 source page")
                    for item in page.items:
                        key = item.observation_occurrence_id.value
                        if key in items and not _same_content(items[key], item):
                            raise ValueError("conflicting D002 source identity")
                        items[key] = item
                    cursor = page.next_cursor
                    if cursor is None:
                        break
                    if type(cursor) is not str or cursor in cursors or not page.items:
                        raise ValueError("invalid D002 source cursor")
                    cursors.add(cursor)
                else:
                    raise ValueError("incomplete D002 source history")
                identity = r.RawSelectionIdentityV1((
                    ("sample.id", "controlled-temporal-sample/1"),
                    ("value.role", ("collector_receipt", "source_timestamp")[role]),
                ))
                candidates = tuple(i for i in items.values() if i.selection_identity == identity)
                if not candidates:
                    raise ValueError("missing D002 source")
                def rank(item: r.ProjectedRawValueV1) -> tuple[datetime, int]:
                    return item.received_ts_utc, item.ingestion_sequence
                chosen = max(candidates, key=rank)
                if sum(rank(item) == rank(chosen) for item in candidates) != 1:
                    raise ValueError("ambiguous D002 source")
                selected.append(_line(chosen, role, request.calculation))
            parents = tuple(
                self.predecessor.get_derived_occurrence(i)
                for i in request.predecessor_occurrence_ids
            )
            if any(type(p) is not f.TemporalOccurrenceV1 for p in parents):
                raise ValueError("absent actual D001 predecessor")
            value = _produce(
                request, tuple(selected), cast(tuple[f.TemporalOccurrenceV1, ...], parents), now,
            )
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.TemporalAgeOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, raw: f.RawProjectionReaderV1,
    predecessor: f.MeasurementTemporalReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1, now: Callable[[], datetime],
) -> f.MeasurementTemporalAgeOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D002 owner")
    if (
        type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1)
        or not callable(now)
        or any(not callable(getattr(predecessor, method, None))
               for method in ("get_derived_occurrence", "list_derived_history"))
    ):
        raise TypeError("actual D001 public reader and exact storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), raw, predecessor, now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.MeasurementTemporalAgeReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D002 reader")
    return _Reads(RecordState(storage, _decode, _validate))
