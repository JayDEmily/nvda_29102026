"""Deterministic Stage-1 calculation kernels for M01.

This module owns only K01-K08, K16 and K17.  It is deliberately pure: M00 reads,
version selection and persistence remain in the public owner in :mod:`api`.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, cast
from zoneinfo import ZoneInfo

from . import api
from ._catalogue import catalogue_row, catalogue_rows

STAGE1_KERNEL_IDS = frozenset(
    {
        "K01_TIME",
        "K02_ALGEBRA",
        "K03_CHANGE_RETURN",
        "K04_STANDARDISE_RANK",
        "K05_REALIZED_RISK",
        "K06_REGRESSION_DEPENDENCE",
        "K07_WEIGHTED_SCORE",
        "K08_RULE_BUCKET_POLICY",
        "K16_STRUCTURED_ASSEMBLY",
        "K17_ORDER_FLOW_IMBALANCE",
    }
)


@dataclass(frozen=True, slots=True)
class KernelValueV1:
    value: object
    occurrence_id: str
    effective_at_utc: datetime
    received_ts_utc: datetime
    subject_instrument: str
    source_temporal_kind: str
    source_timestamp_raw: str | None = None
    metadata: tuple[tuple[str, object], ...] = ()

    def __post_init__(self) -> None:
        if not self.occurrence_id:
            raise ValueError("occurrence_id must not be empty")
        if self.effective_at_utc.tzinfo is None or self.effective_at_utc.utcoffset() != timedelta(
            0
        ):
            raise ValueError("effective_at_utc must be UTC-aware")
        if self.received_ts_utc.tzinfo is None or self.received_ts_utc.utcoffset() != timedelta(0):
            raise ValueError("received_ts_utc must be UTC-aware")
        if not self.subject_instrument:
            raise ValueError("subject_instrument must not be empty")
        if self.source_temporal_kind not in {
            "true_instant",
            "receipt_only",
            "date_only",
            "derived",
        }:
            raise ValueError("unadmitted source_temporal_kind")


@dataclass(frozen=True, slots=True)
class KernelResultV1:
    value: object
    units: str
    result_shape: str
    input_occurrence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BookEventV1:
    occurrence_id: str
    event_time_utc: datetime
    position: int
    operation: str
    side: str
    price: Decimal
    size: Decimal
    venue: str = ""
    ingestion_sequence: int = 0


@dataclass(frozen=True, slots=True)
class BookMutationV1:
    event: BookEventV1
    prior_size: Decimal
    resulting_size: Decimal
    inserted_size: Decimal
    depleted_size: Decimal
    restored_size: Decimal
    removed_size: Decimal


_DEC0 = Decimal(0)
_DEC1 = Decimal(1)
_DEC100 = Decimal(100)
_DEC10000 = Decimal(10000)


def _d(value: object) -> Decimal:
    if type(value) is Decimal:
        return value
    if type(value) is int:
        return Decimal(value)
    if type(value) is str:
        return Decimal(value)
    raise TypeError(f"expected Decimal-compatible scalar, got {type(value).__name__}")


def _i(value: object) -> int:
    """Apply built-in int semantics to admitted immutable scalar parameter types."""
    if type(value) is bool:
        return int(value)
    if type(value) is int:
        return value
    if type(value) is Decimal:
        return int(value)
    if type(value) is str:
        return int(value)
    raise TypeError(f"expected int-compatible scalar, got {type(value).__name__}")


def _parameter_map(parameter_set: api.CalculationParameterSetV1) -> dict[str, object]:
    return dict(parameter_set.parameters)


def _metadata(value: KernelValueV1) -> dict[str, object]:
    return dict(value.metadata)


def _option_right(metadata: dict[str, object]) -> str:
    value = metadata.get("option_right", metadata.get("right", ""))
    return str(value).lower()


def select_d123_official_period_pair(
    raw: dict[str, tuple[KernelValueV1, ...]],
    *,
    as_of_utc: datetime,
    knowledge_cutoff_utc: datetime,
) -> tuple[str, tuple[KernelValueV1, KernelValueV1]] | None:
    """D123-only selection of two authoritative, distinct official OI periods.

    The four official-* metadata fields must be explicitly provided by an
    admitted M00 projection. They are NOT inferred from ticks or native vintage.
    Revision precedence is numeric only for the *controlled, mapped contract*;
    no particular live-provider revision ordering is asserted here.
    """
    populated = tuple(rid for rid in ("R047", "R048") if raw.get(rid))
    if len(populated) != 1:
        return None
    rid = populated[0]
    eligible = select_eligible_values(
        raw[rid],
        as_of_utc=as_of_utc,
        knowledge_cutoff_utc=knowledge_cutoff_utc,
        maximum_staleness=None,
        temporal_basis_permissions=("true_instant", "date_only", "receipt_only"),
    )
    if len(eligible) < 2:
        return None
    right = "call" if rid == "R047" else "put"
    contract_fields = (
        "contract_id",
        "underlying_instrument",
        "expiry",
        "strike",
        "option_right",
        "source_provider",
        "source_variant",
    )
    baseline = _metadata(eligible[0])
    if (
        baseline.get("option_right") != right
        or any(baseline.get(key) is None for key in contract_fields)
        or baseline.get("underlying_instrument") != eligible[0].subject_instrument
    ):
        return None
    by_period: dict[str, list[KernelValueV1]] = {}
    ordinal_by_period: dict[str, int] = {}
    period_by_ordinal: dict[int, str] = {}
    for value in eligible:
        fields = _metadata(value)
        if value.subject_instrument != eligible[0].subject_instrument:
            return None
        if any(
            type(fields.get(key)) is not type(baseline[key]) or fields[key] != baseline[key]
            for key in contract_fields
        ):
            return None
        period = fields.get("official_reporting_period_id")
        ordinal = fields.get("official_reporting_period_order")
        revision = fields.get("official_revision_id")
        precedence = fields.get("official_revision_precedence")
        if (
            type(period) is not str
            or not period
            or type(ordinal) is not int
            or ordinal < 0
            or type(revision) is not str
            or not revision
            or type(precedence) is not int
            or precedence <= 0
        ):
            return None
        if (period in ordinal_by_period and ordinal_by_period[period] != ordinal) or (
            ordinal in period_by_ordinal and period_by_ordinal[ordinal] != period
        ):
            return None
        ordinal_by_period[period] = ordinal
        period_by_ordinal[ordinal] = period
        by_period.setdefault(period, []).append(value)
    if len(by_period) < 2:
        return None
    selected: list[KernelValueV1] = []
    for ordinal in sorted(period_by_ordinal, reverse=True)[:2]:
        revisions = by_period[period_by_ordinal[ordinal]]
        by_precedence: dict[int, str] = {}
        by_revision: dict[str, int] = {}
        for revision in revisions:
            meta = _metadata(revision)
            precedence = meta["official_revision_precedence"]
            revision_id = meta["official_revision_id"]
            assert type(precedence) is int and type(revision_id) is str
            if precedence in by_precedence or revision_id in by_revision:
                # Multiple raw observations of the same revision are not an
                # invented sequence of distinct authoritative corrections.
                return None
            by_precedence[precedence] = revision_id
            by_revision[revision_id] = precedence
        selected.append(
            max(
                revisions,
                key=lambda item: cast(int, _metadata(item)["official_revision_precedence"]),
            )
        )
    return rid, (selected[0], selected[1])


def _same_option_history_selection(current: KernelValueV1, reference: KernelValueV1) -> bool:
    """Require D094/D095 history to describe the same contract or exact bucket."""

    if current.subject_instrument != reference.subject_instrument:
        return False
    current_metadata = _metadata(current)
    reference_metadata = _metadata(reference)
    current_contract = current_metadata.get("contract_id")
    reference_contract = reference_metadata.get("contract_id")
    if current_contract is not None or reference_contract is not None:
        return (
            current_contract is not None
            and reference_contract is not None
            and type(current_contract) is type(reference_contract)
            and current_contract == reference_contract
        )
    for key in ("expiry", "delta_bucket"):
        current_value = current_metadata.get(key)
        reference_value = reference_metadata.get(key)
        if (
            current_value is None
            or reference_value is None
            or type(current_value) is not type(reference_value)
            or current_value != reference_value
        ):
            return False
    current_right = _option_right(current_metadata)
    reference_right = _option_right(reference_metadata)
    return bool(current_right) and current_right == reference_right


def _named(value: object) -> dict[str, object]:
    if isinstance(value, Mapping):
        if not all(type(key) is str for key in value):
            return {}
        return dict(value)
    if type(value) is not tuple:
        return {}
    output: dict[str, object] = {}
    for item in value:
        if type(item) is not tuple or len(item) < 2 or type(item[0]) is not str:
            return {}
        output[item[0]] = item[1]
    return output


def _named_tuple(values: Iterable[tuple[str, object]]) -> tuple[tuple[str, object], ...]:
    return tuple(values)


def _all_values(
    raw_inputs: dict[str, tuple[KernelValueV1, ...]],
    derived_inputs: dict[str, tuple[KernelValueV1, ...]],
) -> tuple[KernelValueV1, ...]:
    return tuple(
        item for values in (*raw_inputs.values(), *derived_inputs.values()) for item in values
    )


def select_eligible_values(
    values: tuple[KernelValueV1, ...],
    *,
    as_of_utc: datetime,
    knowledge_cutoff_utc: datetime,
    maximum_staleness: timedelta | None,
    temporal_basis_permissions: tuple[str, ...],
) -> tuple[KernelValueV1, ...]:
    eligible: list[KernelValueV1] = []
    for item in values:
        if (
            item.source_temporal_kind not in temporal_basis_permissions
            and item.source_temporal_kind != "derived"
        ):
            continue
        if item.received_ts_utc > knowledge_cutoff_utc:
            continue
        if (
            item.source_temporal_kind in {"true_instant", "derived"}
            and item.effective_at_utc > as_of_utc
        ):
            continue
        basis = (
            item.effective_at_utc
            if item.source_temporal_kind in {"true_instant", "derived"}
            else item.received_ts_utc
        )
        if maximum_staleness is not None and as_of_utc - basis > maximum_staleness:
            continue
        eligible.append(item)
    eligible.sort(
        key=lambda item: (item.effective_at_utc, item.received_ts_utc, item.occurrence_id)
    )
    return tuple(eligible)


def _values(
    mapping: dict[str, tuple[KernelValueV1, ...]], identity: str
) -> tuple[KernelValueV1, ...]:
    return mapping.get(identity, ())


def _latest(mapping: dict[str, tuple[KernelValueV1, ...]], identity: str) -> KernelValueV1 | None:
    values = _values(mapping, identity)
    if not values:
        return None
    return max(
        values, key=lambda item: (item.effective_at_utc, item.received_ts_utc, item.occurrence_id)
    )


def _scalar(mapping: dict[str, tuple[KernelValueV1, ...]], identity: str) -> object | None:
    item = _latest(mapping, identity)
    return None if item is None else item.value


def _input_ids(*mappings: dict[str, tuple[KernelValueV1, ...]]) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                item.occurrence_id
                for mapping in mappings
                for values in mapping.values()
                for item in values
            }
        )
    )


def _result(
    identity: str,
    value: object,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
) -> KernelResultV1:
    row = catalogue_row(identity)
    shape = "structured" if type(value) is tuple else "scalar"
    return KernelResultV1(
        value=value,
        units=row.units,
        result_shape=shape,
        input_occurrence_ids=_input_ids(raw, derived),
    )


def _decimal_values(
    mapping: dict[str, tuple[KernelValueV1, ...]], identity: str
) -> tuple[Decimal, ...]:
    return tuple(_d(item.value) for item in _values(mapping, identity))


def _sample_mean(values: tuple[Decimal, ...]) -> Decimal:
    return sum(values, _DEC0) / Decimal(len(values))


def _sample_sd(values: tuple[Decimal, ...]) -> Decimal | None:
    if len(values) < 2:
        return None
    mean = _sample_mean(values)
    variance = sum(((item - mean) ** 2 for item in values), _DEC0) / Decimal(len(values) - 1)
    if variance <= 0:
        return None
    return variance.sqrt()


def _pearson(left: tuple[Decimal, ...], right: tuple[Decimal, ...]) -> Decimal | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    ml, mr = _sample_mean(left), _sample_mean(right)
    dl = tuple(item - ml for item in left)
    dr = tuple(item - mr for item in right)
    den = (
        sum((item * item for item in dl), _DEC0) * sum((item * item for item in dr), _DEC0)
    ).sqrt()
    if den == 0:
        return None
    return sum((a * b for a, b in zip(dl, dr, strict=True)), _DEC0) / den


def _solve(matrix: list[list[Decimal]], vector: list[Decimal]) -> list[Decimal] | None:
    n = len(vector)
    augmented = [[*row, vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if augmented[r][col] != 0), None)
        if pivot is None:
            return None
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        augmented[col] = [v / divisor for v in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor == 0:
                continue
            augmented[row] = [
                a - factor * b for a, b in zip(augmented[row], augmented[col], strict=True)
            ]
    return [augmented[i][-1] for i in range(n)]


def _ols(
    y: tuple[Decimal, ...], columns: tuple[tuple[Decimal, ...], ...]
) -> tuple[Decimal, ...] | None:
    if not y or any(len(column) != len(y) for column in columns):
        return None
    rows = [(Decimal(1), *(column[i] for column in columns)) for i in range(len(y))]
    ncoef = 1 + len(columns)
    xtx = [
        [sum((row[i] * row[j] for row in rows), _DEC0) for j in range(ncoef)] for i in range(ncoef)
    ]
    xty = [
        sum((row[i] * target for row, target in zip(rows, y, strict=True)), _DEC0)
        for i in range(ncoef)
    ]
    solved = _solve(xtx, xty)
    return None if solved is None else tuple(solved)


def _ols_slope(x: tuple[Decimal, ...], y: tuple[Decimal, ...]) -> Decimal | None:
    fit = _ols(y, (x,))
    return None if fit is None else fit[1]


def _history_anchor(
    values: tuple[KernelValueV1, ...],
    *,
    as_of: datetime,
    seconds: int | None = None,
    days: int | None = None,
) -> tuple[KernelValueV1, KernelValueV1] | None:
    eligible = tuple(v for v in values if v.effective_at_utc <= as_of)
    if not eligible:
        return None
    current = max(eligible, key=lambda v: (v.effective_at_utc, v.received_ts_utc, v.occurrence_id))
    anchor = current.effective_at_utc - (
        timedelta(seconds=seconds) if seconds is not None else timedelta(days=days or 0)
    )
    refs = tuple(
        v
        for v in eligible
        if v.effective_at_utc <= anchor and v.occurrence_id != current.occurrence_id
    )
    if not refs:
        return None
    reference = max(refs, key=lambda v: (v.effective_at_utc, v.received_ts_utc, v.occurrence_id))
    return current, reference


def _align_occurrence_fields(
    raw: dict[str, tuple[KernelValueV1, ...]], fields: tuple[str, ...]
) -> tuple[dict[str, KernelValueV1], ...]:
    maps = [{item.occurrence_id: item for item in raw.get(field, ())} for field in fields]
    if not maps:
        return ()
    ids = set(maps[0])
    for mapping in maps[1:]:
        ids &= set(mapping)
    rows: list[dict[str, KernelValueV1]] = []
    for occurrence_id in ids:
        rows.append(
            {field: mapping[occurrence_id] for field, mapping in zip(fields, maps, strict=True)}
        )
    rows.sort(
        key=lambda row: (
            max(v.effective_at_utc for v in row.values()),
            next(iter(row.values())).occurrence_id,
        )
    )
    return tuple(rows)


_TRADE_IDENTITY_KEYS = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")


def _source_identity_compatible(left: KernelValueV1, right: KernelValueV1) -> bool:
    if left.subject_instrument != right.subject_instrument:
        return False
    left_meta, right_meta = _metadata(left), _metadata(right)
    for key in _TRADE_IDENTITY_KEYS:
        lhs, rhs = left_meta.get(key), right_meta.get(key)
        if (lhs is not None or rhs is not None) and (
            lhs is None or rhs is None or type(lhs) is not type(rhs) or lhs != rhs
        ):
            return False
    return True


def _observation_signs(
    observations: tuple[KernelValueV1, ...],
    signed_predecessors: tuple[KernelValueV1, ...],
) -> dict[str, tuple[int, str]] | None:
    """Match D015 per-trade signs to their native M00 observation, never D IDs.

    A D015 occurrence can contain a history of trade sources. Reconstruct the
    *selected* source as the unique latest eligible native trade in its stored
    lineage at its own calculation time/cutoff. Reject missing or ambiguous
    reconstruction rather than synthesising a partial signed total.
    """
    if not observations or not signed_predecessors:
        return None
    observation_ids = {v.occurrence_id for v in observations}
    if len(observation_ids) != len(observations):
        return None
    result: dict[str, tuple[int, str]] = {}
    selected_version: dict[str, tuple[datetime, datetime, str]] = {}
    for predecessor in signed_predecessors:
        metadata = _metadata(predecessor)
        lineage = metadata.get("raw_input_lineage")
        cutoff = metadata.get("source_knowledge_cutoff_utc")
        if (
            type(lineage) is not tuple
            or type(cutoff) is not datetime
            or not all(type(item) is api.RawInputLineageV1 for item in lineage)
        ):
            return None
        source_ids = {
            item.observation_occurrence_id for item in lineage if item.raw_signal_id == "R120"
        }
        if not source_ids:
            return None
        matching = [
            item
            for item in observations
            if item.occurrence_id in source_ids
            and item.effective_at_utc <= predecessor.effective_at_utc
            and item.received_ts_utc <= cutoff
            and _source_identity_compatible(item, predecessor)
        ]
        if not matching:
            # An older D015 history item can legitimately predate the raw
            # window currently being aggregated. It contributes no trade.
            continue
        if not source_ids <= observation_ids:
            # Some native trades used by this D015 classification are absent
            # from the parent's required per-trade field. Choosing a visible
            # older source as the sign's anchor would fabricate correlation.
            return None
        latest_at = max((v.effective_at_utc, v.received_ts_utc) for v in matching)
        newest = [v for v in matching if (v.effective_at_utc, v.received_ts_utc) == latest_at]
        if len({v.occurrence_id for v in newest}) != 1:
            return None
        selected_id = newest[0].occurrence_id
        if type(predecessor.value) is not int or predecessor.value not in {-1, 1}:
            return None
        if selected_id in result and result[selected_id][0] != predecessor.value:
            # Conflicting classifications cannot be silently selected.
            return None
        priority = (predecessor.effective_at_utc, cutoff, predecessor.occurrence_id)
        if selected_id not in result or priority > selected_version[selected_id]:
            result[selected_id] = (predecessor.value, predecessor.occurrence_id)
            selected_version[selected_id] = priority
    if {item.occurrence_id for item in observations} != set(result):
        return None
    return result


def _latest_by_subject(
    mapping: dict[str, tuple[KernelValueV1, ...]], identity: str
) -> dict[str, KernelValueV1]:
    output: dict[str, KernelValueV1] = {}
    for item in mapping.get(identity, ()):
        current = output.get(item.subject_instrument)
        if current is None or (item.effective_at_utc, item.received_ts_utc, item.occurrence_id) > (
            current.effective_at_utc,
            current.received_ts_utc,
            current.occurrence_id,
        ):
            output[item.subject_instrument] = item
    return output


def _ordered_book_events(events: tuple[BookEventV1, ...]) -> tuple[BookEventV1, ...]:
    """Provider receipt/sequence order with a stable deterministic identity tie-break."""
    return tuple(
        event
        for _, event in sorted(
            enumerate(events),
            key=lambda pair: (
                pair[1].event_time_utc,
                pair[1].ingestion_sequence,
                pair[1].occurrence_id,
                pair[0],
            ),
        )
    )


def _apply_book_event(
    state: dict[tuple[str, str, int], tuple[Decimal, Decimal]], event: BookEventV1
) -> BookMutationV1:
    """Apply an admitted positional mutation, shifting rows of the same book/side.

    An event at an as-yet-unseen position may be a partial rate-only stream;
    a depth-state consumer separately rejects a non-contiguous final book.
    An update/delete without an established predecessor is never fabricated.
    """
    op, side = event.operation.lower(), event.side.lower()
    if (
        op not in {"insert", "update", "delete", "remove", "cancel"}
        or side not in {"bid", "ask"}
        or event.position < 0
        or event.size < 0
    ):
        raise ValueError("invalid provider book operation/side/position/quantity")
    key = (event.venue, side, event.position)
    present = key in state
    prior_size = state[key][1] if present else _DEC0
    inserted = depleted = restored = removed = _DEC0
    if op == "insert":
        # A positional insertion never overwrites the row it displaces.
        affected = sorted(
            (k for k in state if k[:2] == key[:2] and k[2] >= event.position),
            key=lambda k: k[2],
            reverse=True,
        )
        for old in affected:
            state[(old[0], old[1], old[2] + 1)] = state.pop(old)
        state[key] = (event.price, event.size)
        inserted = event.size
        prior_size = _DEC0  # an insert creates a row, not a size restoration
        resulting = event.size
    else:
        if not present:
            raise ValueError("book update/delete has no established row at source position")
        if op == "update":
            resulting = event.size
            depleted = max(prior_size - resulting, _DEC0)
            restored = max(resulting - prior_size, _DEC0)
            state[key] = (event.price, resulting)
        else:
            resulting = _DEC0
            removed = prior_size
            state.pop(key)
            affected = sorted(
                (k for k in state if k[:2] == key[:2] and k[2] > event.position), key=lambda k: k[2]
            )
            for old in affected:
                state[(old[0], old[1], old[2] - 1)] = state.pop(old)
    return BookMutationV1(event, prior_size, resulting, inserted, depleted, restored, removed)


def reconstruct_book(events: tuple[BookEventV1, ...]) -> tuple[BookMutationV1, ...]:
    state: dict[tuple[str, str, int], tuple[Decimal, Decimal]] = {}
    return tuple(_apply_book_event(state, event) for event in _ordered_book_events(events))


def _book_events(
    raw: dict[str, tuple[KernelValueV1, ...]], *, direct: bool = False
) -> tuple[BookEventV1, ...]:
    if direct:
        # Direct exchange depth: position, market-maker/venue, operation, side, price, size.
        position_id, venue_id, operation_id, side_id, price_id, size_id = (
            "R192",
            "R193",
            "R194",
            "R195",
            "R196",
            "R197",
        )
    else:
        position_id, operation_id, side_id, price_id, size_id, venue_id = (
            "R185",
            "R187",
            "R188",
            "R189",
            "R190",
            None,
        )
    required = tuple(field for field in (position_id, operation_id, side_id, size_id) if field)
    field_sets = [{item.occurrence_id for item in raw.get(field, ())} for field in required]
    if not field_sets[0] or any(ids != field_sets[0] for ids in field_sets[1:]):
        raise ValueError("incomplete native book-event field set")
    rows = _align_occurrence_fields(raw, required)
    if raw.get(price_id) and {v.occurrence_id for v in raw[price_id]} != field_sets[0]:
        raise ValueError("partial native price field set")
    if venue_id is not None and {v.occurrence_id for v in raw.get(venue_id, ())} != field_sets[0]:
        raise ValueError("incomplete direct venue field set")
    by_price = {item.occurrence_id: item for item in raw.get(price_id, ())}
    by_venue = (
        {} if venue_id is None else {item.occurrence_id: item for item in raw.get(venue_id, ())}
    )
    events: list[BookEventV1] = []
    source_streams: set[tuple[str, str]] = set()
    for row in rows:
        base = row[position_id]
        stream = (
            str(_metadata(base).get("source_provider", "")),
            str(_metadata(base).get("source_variant", "")),
        )
        for field in required:
            meta = _metadata(row[field])
            if (
                str(meta.get("source_provider", "")),
                str(meta.get("source_variant", "")),
            ) != stream:
                raise ValueError("book fields for one occurrence have incompatible sources")
            if row[field].subject_instrument != base.subject_instrument:
                raise ValueError("book fields for one occurrence have incompatible subjects")
        source_streams.add(stream)
        price_item = by_price.get(base.occurrence_id)
        price = _DEC0 if price_item is None else _d(price_item.value)
        venue = (
            ""
            if venue_id is None or base.occurrence_id not in by_venue
            else str(by_venue[base.occurrence_id].value)
        )
        events.append(
            BookEventV1(
                base.occurrence_id,
                max(v.effective_at_utc for v in row.values()),
                _i(row[position_id].value),
                str(row[operation_id].value).lower(),
                str(row[side_id].value).lower(),
                price,
                _d(row[size_id].value),
                venue,
                _i(_metadata(base).get("ingestion_sequence", 0)),
            )
        )
    if len(source_streams) != 1:
        raise ValueError("multiple unmatched book source streams")
    return tuple(events)


def _book_final_state(
    events: tuple[BookEventV1, ...],
) -> dict[tuple[str, str, int], tuple[Decimal, Decimal]] | None:
    state: dict[tuple[str, str, int], tuple[Decimal, Decimal]] = {}
    try:
        for event in _ordered_book_events(events):
            _apply_book_event(state, event)
    except ValueError:
        return None
    # No completeness assertion is synthesised from a hole in the observed
    # provider row indices. Both 0-based and 1-based source positions occur.
    streams = {(venue, side) for venue, side, _ in state}
    for venue, side in streams:
        positions = sorted(k[2] for k in state if k[:2] == (venue, side))
        if positions[0] not in {0, 1} or positions != list(
            range(positions[0], positions[0] + len(positions))
        ):
            return None
    return state


def _context(contexts: tuple[object, ...], kind: type[Any]) -> Any | None:
    matches = [item for item in contexts if type(item) is kind]
    return matches[0] if len(matches) == 1 else None


def supported_stage1_ids() -> tuple[str, ...]:
    return tuple(row.derived_id for row in catalogue_rows() if row.kernel_id in STAGE1_KERNEL_IDS)


def occurrence_identity(
    derived_signal_id: str,
    *,
    calculation_definition_version: str,
    subject_instrument: str,
    effective_as_of_utc: datetime,
    knowledge_cutoff_utc: datetime,
    input_occurrence_ids: tuple[str, ...],
    version_keys: tuple[tuple[str, int], ...],
) -> str:
    payload = {
        "derived_signal_id": derived_signal_id,
        "calculation_definition_version": calculation_definition_version,
        "subject_instrument": subject_instrument,
        "effective_as_of_utc": effective_as_of_utc.isoformat(),
        "knowledge_cutoff_utc": knowledge_cutoff_utc.isoformat(),
        "input_occurrence_ids": sorted(input_occurrence_ids),
        "version_keys": sorted((str(identity), int(version)) for identity, version in version_keys),
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return f"{derived_signal_id.lower()}-{digest}"


def extract_scalar(value: object, extractor: str, arguments: tuple[object, ...]) -> Decimal:
    named = _named(value)
    if extractor == "component":
        current: object = value
        for part in arguments:
            if type(current) is tuple or isinstance(current, Mapping):
                mapped = _named(current)
                if str(part) not in mapped:
                    raise ValueError("component path not present")
                current = mapped[str(part)]
            else:
                raise ValueError("component path traverses non-structured value")
        return _d(current)
    if extractor == "weighted_component_sum":
        if len(arguments) % 2:
            raise ValueError("weighted_component_sum needs name/coefficient pairs")
        total = _DEC0
        for i in range(0, len(arguments), 2):
            name, coefficient = str(arguments[i]), _d(arguments[i + 1])
            if name not in named:
                raise ValueError("weighted component missing")
            total += coefficient * _d(named[name])
        return total
    probabilities = _named(named.get("probabilities", ()))
    if extractor == "class_probability":
        label = str(arguments[0])
        if label not in probabilities:
            raise ValueError("class probability missing")
        return _d(probabilities[label])
    if extractor == "probability_margin":
        ordered = sorted((_d(item) for item in probabilities.values()), reverse=True)
        if len(ordered) < 2:
            raise ValueError("probability margin requires two classes")
        return ordered[0] - ordered[1]
    if extractor == "normalised_entropy":
        probs = tuple(_d(item) for item in probabilities.values())
        if len(probs) < 2 or any(p < 0 for p in probs) or sum(probs, _DEC0) != _DEC1:
            raise ValueError("invalid probability vector")
        entropy = -sum((p * p.ln() for p in probs if p > 0), _DEC0)
        return entropy / Decimal(len(probs)).ln()
    distribution = named.get("distribution")
    if extractor in {
        "distribution_cdf",
        "upper_tail",
        "distribution_mean",
        "distribution_variance",
    }:
        if type(distribution) is not tuple:
            raise ValueError("stored distribution missing")
        points = tuple(
            (_d(item[0]), _d(item[1]))
            for item in distribution
            if type(item) is tuple and len(item) == 2
        )
        if not points or sum((p for _, p in points), _DEC0) != _DEC1:
            raise ValueError("invalid stored distribution")
        if extractor == "distribution_cdf":
            x = _d(arguments[0])
            return sum((p for v, p in points if v <= x), _DEC0)
        if extractor == "upper_tail":
            x = _d(arguments[0])
            return _DEC1 - sum((p for v, p in points if v <= x), _DEC0)
        mean = sum((v * p for v, p in points), _DEC0)
        if extractor == "distribution_mean":
            return mean
        return sum((((v - mean) ** 2) * p for v, p in points), _DEC0)
    matrix = named.get("matrix")
    if extractor in {"matrix_entry", "row_l2", "frobenius"}:
        if type(matrix) is not tuple:
            raise ValueError("matrix missing")
        rows = tuple(tuple(_d(v) for v in row) for row in matrix)
        if extractor == "matrix_entry":
            return rows[_i(arguments[0])][_i(arguments[1])]
        if extractor == "row_l2":
            row = rows[_i(arguments[0])]
            return Decimal(str(sum(float(v) ** 2 for v in row) ** 0.5))
        return Decimal(str(sum(float(v) ** 2 for row in rows for v in row) ** 0.5))
    raise ValueError(f"unadmitted scalar extractor {extractor!r}")


def _transform(value: Decimal, feature: api.ScoreFeatureV1) -> Decimal:
    if feature.transform == "identity":
        transformed = value
    elif feature.transform == "signed_log":
        scale = feature.transform_scale
        if scale is None or scale <= 0:
            raise ValueError("signed_log requires positive transform_scale")
        transformed = (_DEC1 if value >= 0 else -_DEC1) * (_DEC1 + abs(value) / scale).ln()
    elif feature.transform == "bounded_ratio":
        scale = feature.transform_scale
        if scale is None or scale <= 0:
            raise ValueError("bounded_ratio requires positive transform_scale")
        transformed = value / (scale + abs(value))
    elif feature.transform == "z_score":
        baseline = feature.baseline_values
        sd = _sample_sd(baseline)
        if sd is None:
            raise ValueError("z_score requires non-degenerate prior baseline")
        transformed = (value - _sample_mean(baseline)) / sd
    else:
        raise ValueError(f"unadmitted score transform {feature.transform!r}")
    if feature.clip_min is not None:
        transformed = max(transformed, feature.clip_min)
    if feature.clip_max is not None:
        transformed = min(transformed, feature.clip_max)
    return Decimal(feature.orientation) * transformed


def _score(
    identity: str,
    raw_inputs: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    parameter_set: api.CalculationParameterSetV1,
) -> object | None:
    if not parameter_set.score_features:
        return None
    row = catalogue_row(identity)
    declared_dependencies = set((*row.raw_dependencies, *row.derived_dependencies))
    if any(
        feature.signal_id not in declared_dependencies for feature in parameter_set.score_features
    ):
        return None
    transformed: list[tuple[api.ScoreFeatureV1, Decimal]] = []
    for feature in parameter_set.score_features:
        occurrence = _latest(
            raw_inputs if feature.signal_id.startswith("R") else derived,
            feature.signal_id,
        )
        if occurrence is None:
            return None
        try:
            scalar = extract_scalar(
                occurrence.value, feature.extractor, tuple(feature.extractor_arguments)
            )
            transformed.append((feature, _transform(scalar, feature)))
        except (TypeError, ValueError, IndexError, KeyError, InvalidOperation):
            return None
    params = _parameter_map(parameter_set)
    if identity == "D157":
        matrix_occ = _latest(derived, "D156")
        if matrix_occ is None:
            return None
        m = _named(matrix_occ.value)
        matrix = m.get("partial_correlation_matrix", m.get("matrix"))
        if type(matrix) is not tuple or len(matrix) != len(transformed):
            return None
        u: list[Decimal] = []
        for j, (feature, _) in enumerate(transformed):
            row = matrix[j]
            if type(row) is not tuple or len(row) != len(transformed):
                return None
            duplicate = sum((abs(_d(row[k])) for k in range(len(transformed)) if k != j), _DEC0)
            u.append(feature.weight / (_DEC1 + duplicate))
        total_u = sum(u, _DEC0)
        if total_u <= 0:
            return None
        weights = tuple(item / total_u for item in u)
        mean = sum((w * z for w, (_, z) in zip(weights, transformed, strict=True)), _DEC0)
        return sum(
            (w * ((z - mean) ** 2) for w, (_, z) in zip(weights, transformed, strict=True)), _DEC0
        ).sqrt()
    raw = _d(params.get("intercept", _DEC0)) + sum(
        (feature.weight * z for feature, z in transformed), _DEC0
    )
    # D008's alignment_score is explicitly a bounded quality component.
    bounded = identity == "D008" or bool(
        params.get("bounded_output", catalogue_row(identity).units == "0-1")
    )
    if bounded:
        # Decimal has exp(); stable enough for the admitted deterministic carrier.
        return _DEC1 / (_DEC1 + (-raw).exp())
    return raw


def _eval_k07(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    parameter_set: api.CalculationParameterSetV1,
    contexts: tuple[object, ...],
) -> object | None:
    if identity == "D008":
        # Only admitted true-instants contribute to event-time skew. Receipt and
        # date-only sources contribute to missingness, never fabricated instants.
        sources = raw.get("R001", ())
        if not sources or len({source.occurrence_id for source in sources}) != len(sources):
            return None
        instants = tuple(
            source.effective_at_utc
            for source in sources
            if source.source_temporal_kind == "true_instant"
        )
        if not instants or not derived.get("D001") or not derived.get("D002"):
            return None
        score = _score(identity, raw, derived, parameter_set)
        if type(score) is not Decimal or not _DEC0 <= score <= _DEC1:
            return None
        skew = Decimal(str((max(instants) - min(instants)).total_seconds()))
        return _named_tuple(
            (
                ("max_true_instant_skew_seconds", skew),
                ("event_time_coverage_fraction", Decimal(len(instants)) / Decimal(len(sources))),
                ("missing_event_time_count", len(sources) - len(instants)),
                ("alignment_score", score),
            )
        )
    if identity != "D173":
        return _score(identity, raw, derived, parameter_set)

    # Neighbour relations are directed, versioned identities, not a proximity
    # search on available candidate results. A candidate-scoped score is valid
    # only when every configured feature has exactly one matching occurrence.
    subject = _context(contexts, api.CandidateStructureContextV1)
    candidate_set = _context(contexts, api.CandidateSetContextV1)
    if subject is None or candidate_set is None:
        return None
    candidate_id = subject.candidate_identity
    if candidate_id not in candidate_set.candidate_identities:
        return None
    neighbours = tuple(
        other for source, other in candidate_set.neighbour_relations if source == candidate_id
    )
    if not neighbours or not parameter_set.score_features:
        return None
    if any(
        feature.signal_id not in catalogue_row(identity).derived_dependencies
        for feature in parameter_set.score_features
    ):
        return None
    scores: dict[str, Decimal] = {}
    params = _parameter_map(parameter_set)
    for candidate in (candidate_id, *neighbours):
        total = _d(params.get("intercept", _DEC0))
        for feature in parameter_set.score_features:
            matching = tuple(
                item
                for item in derived.get(feature.signal_id, ())
                if _named(item.value).get("candidate") == candidate
            )
            if len(matching) != 1:
                return None
            try:
                scalar = extract_scalar(
                    matching[0].value, feature.extractor, tuple(feature.extractor_arguments)
                )
                total += feature.weight * _transform(scalar, feature)
            except (TypeError, ValueError, KeyError, ArithmeticError, IndexError):
                return None
        scores[candidate] = total
    subject_score = scores[candidate_id]
    return _named_tuple(
        (
            ("subject_candidate", candidate_id),
            ("subject_score", subject_score),
            ("comparisons", tuple((c, scores[c] - subject_score) for c in neighbours)),
            ("neighbour_scores", tuple((c, scores[c]) for c in neighbours)),
        )
    )


def _phase_for_local(local: datetime, phases: object) -> str | None:
    if type(phases) is not tuple:
        return None
    matches: list[str] = []
    local_time = local.timetz().replace(tzinfo=None)
    for specification in phases:
        if type(specification) is not str:
            return None
        try:
            name, start, end = specification.split("|")
            sh, sm = (int(v) for v in start.split(":"))
            eh, em = (int(v) for v in end.split(":"))
            start_time = time(sh, sm)
            end_time = time(eh, em)
        except Exception:
            return None
        if start_time == end_time:
            return None
        inside = (
            start_time <= local_time < end_time
            if start_time < end_time
            else local_time >= start_time or local_time < end_time
        )
        if inside:
            matches.append(name)
    return matches[0] if len(matches) == 1 else None


def _eval_k01(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    params: dict[str, object],
    as_of: datetime,
    cutoff: datetime,
) -> object | None:
    if identity == "D001":
        source = _latest(raw, "R002")
        if source is None or source.source_temporal_kind != "true_instant":
            return None
        value = source.source_timestamp_raw or source.value
        if type(value) is datetime:
            stamp = value
        elif type(value) is str:
            try:
                stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        else:
            return None
        if stamp.tzinfo is None:
            timezone_name = str(_scalar(raw, "R003") or params.get("exchange_timezone", ""))
            if not timezone_name:
                return None
            stamp = stamp.replace(tzinfo=ZoneInfo(timezone_name))
        return stamp.astimezone(UTC)
    if identity == "D002":
        source = _latest(raw, "R002")
        if source is None or source.source_temporal_kind == "date_only":
            return None
        if source.source_temporal_kind == "true_instant":
            d001 = _latest(derived, "D001")
            if d001 is None or type(d001.value) is not datetime:
                return None
            seconds = Decimal(str((cutoff - d001.value).total_seconds()))
            if seconds < 0:
                return None
            return _named_tuple((("basis", "source_event"), ("age_seconds", seconds)))
        if source.source_temporal_kind == "receipt_only":
            seconds = Decimal(str((cutoff - source.received_ts_utc).total_seconds()))
            if seconds < 0:
                return None
            return _named_tuple((("basis", "collector_receipt"), ("age_seconds", seconds)))
        return None
    if identity == "D003":
        source = _latest(derived, "D001")
        if source is None or type(source.value) is not datetime:
            return None
        timezone_name = str(_scalar(raw, "R004") or params.get("exchange_timezone", ""))
        if not timezone_name:
            return None
        try:
            return source.value.astimezone(ZoneInfo(timezone_name))
        except Exception:
            return None
    if identity == "D004":
        local = _scalar(derived, "D003")
        if type(local) is not datetime:
            return None
        # Session-date offset is explicit when an overnight session requires one.
        boundary = params.get("trading_date_boundary")
        trading_date = local.date()
        if type(boundary) is str:
            hh, mm = (int(v) for v in boundary.split(":"))
            if local.timetz().replace(tzinfo=None) < time(hh, mm):
                trading_date -= timedelta(days=1)
        return trading_date
    if identity == "D005":
        local = _scalar(derived, "D003")
        if type(local) is not datetime:
            return None
        return _phase_for_local(local, params.get("session_phases"))
    if identity == "D009":
        # A macro revision is one co-referenced native M00 occurrence with
        # all three versioning fields. Set intersection alone would silently
        # drop a newer partial revision and mislabel an older one as current.
        required_fields = ("R280", "R281", "R282")
        occurrence_sets: list[set[str]] = []
        for field in required_fields:
            values = raw.get(field, ())
            ids = {item.occurrence_id for item in values}
            if not values or len(ids) != len(values):
                return None
            occurrence_sets.append(ids)
        if any(ids != occurrence_sets[0] for ids in occurrence_sets[1:]):
            return None
        rows = _align_occurrence_fields(raw, required_fields)
        visible = tuple(
            row for row in rows if all(item.received_ts_utc <= cutoff for item in row.values())
        )
        if not visible:
            return None
        ordered = sorted(
            visible,
            key=lambda row: (
                max(item.received_ts_utc for item in row.values()),
                row["R280"].occurrence_id,
            ),
        )
        current = ordered[-1]
        category = "initial" if len(ordered) == 1 else "latest_known_at_cutoff"
        return _named_tuple(
            (
                ("status", category),
                ("realtime_start", current["R280"].value),
                ("realtime_end", current["R281"].value),
                ("last_updated", current["R282"].value),
                ("cutoff", cutoff),
            )
        )
    if identity == "D010":
        local = _scalar(derived, "D003")
        liquid = params.get("liquid_phases")
        weekdays = params.get("market_open_weekdays")
        closed_dates = params.get("market_closed_dates")
        open_dates = params.get("market_open_dates", ())
        if (
            type(local) is not datetime
            or type(liquid) is not tuple
            or type(weekdays) is not tuple
            or type(closed_dates) is not tuple
            or type(open_dates) is not tuple
        ):
            return None
        if any(type(item) is not int or not 0 <= item <= 6 for item in weekdays):
            return None
        local_date = local.date().isoformat()
        if any(type(item) is not str for item in (*closed_dates, *open_dates)):
            return None
        is_open_day = local_date in open_dates or (
            local.weekday() in weekdays and local_date not in closed_dates
        )
        if not is_open_day:
            return False
        phase = _phase_for_local(local, params.get("session_phases"))
        return False if phase is None else phase in liquid
    if identity == "D062":
        event_times: list[datetime] = []
        for event_value in raw.get("R284", ()):
            if (
                type(event_value.value) is datetime
                and event_value.value > as_of
                and event_value.received_ts_utc <= cutoff
            ):
                event_times.append(event_value.value)
        if not event_times:
            return None
        next_event_at = min(event_times)
        seconds = Decimal(str((next_event_at - as_of).total_seconds()))
        return _named_tuple((("seconds", seconds), ("minutes", seconds / Decimal(60))))
    if identity == "D085":
        expiry = _scalar(raw, "R013")
        trading = _scalar(derived, "D004")
        try:
            expiry_date = (
                expiry
                if type(expiry) is date and type(expiry) is not datetime
                else date.fromisoformat(str(expiry))
            )
            trading_date = (
                trading
                if type(trading) is date and type(trading) is not datetime
                else date.fromisoformat(str(trading))
            )
        except Exception:
            return None
        days = (expiry_date - trading_date).days
        return days if days >= 0 else None
    if identity == "D086":
        expiry = _scalar(raw, "R013")
        now = _scalar(derived, "D001")
        if type(now) is not datetime or expiry is None:
            return None
        try:
            expiry_date = (
                expiry
                if type(expiry) is date and type(expiry) is not datetime
                else date.fromisoformat(str(expiry))
            )
            expiry_time = str(params["expiry_time"])
            timezone_name = str(params["exchange_timezone"])
            hh, mm = (int(v) for v in expiry_time.split(":"))
            expiry_instant = datetime.combine(
                expiry_date, time(hh, mm), ZoneInfo(timezone_name)
            ).astimezone(UTC)
        except Exception:
            return None
        seconds = Decimal(str((expiry_instant - now).total_seconds()))
        if seconds < 0:
            return None
        return seconds / Decimal(86400) / Decimal(365)
    return None


def _eval_k02(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    params: dict[str, object],
    contexts: tuple[object, ...],
) -> object | None:
    try:
        if identity in {"D011", "D087"}:
            bid, ask = _d(_scalar(raw, "R034")), _d(_scalar(raw, "R035"))
            return (bid + ask) / Decimal(2)
        if identity == "D012":
            return _d(_scalar(raw, "R035")) - _d(_scalar(raw, "R034"))
        if identity == "D013":
            mid, spread = _d(_scalar(derived, "D011")), _d(_scalar(derived, "D012"))
            return None if mid == 0 else _DEC100 * spread / mid
        if identity == "D014":
            bid, ask = _d(_scalar(raw, "R033")), _d(_scalar(raw, "R036"))
            den = bid + ask
            return None if den == 0 else (bid - ask) / den
        if identity == "D017":
            price_ids = {v.occurrence_id for v in raw.get("R120", ())}
            size_ids = {v.occurrence_id for v in raw.get("R121", ())}
            if not price_ids or price_ids != size_ids:
                return None
            rows = _align_occurrence_fields(raw, ("R120", "R121"))
            if any(not _source_identity_compatible(row["R120"], row["R121"]) for row in rows):
                return None
            den = sum((_d(r["R121"].value) for r in rows), _DEC0)
            return (
                None
                if den == 0
                else sum((_d(r["R120"].value) * _d(r["R121"].value) for r in rows), _DEC0) / den
            )
        if identity == "D018":
            provider, calc = _d(_scalar(raw, "R137")), _d(_scalar(derived, "D017"))
            diff = provider - calc
            return (
                None
                if calc == 0
                else _named_tuple(
                    (("price_difference", diff), ("bps_difference", _DEC10000 * diff / calc))
                )
            )
        if identity == "D025":
            low, high, last = (
                _d(_scalar(raw, "R039")),
                _d(_scalar(raw, "R040")),
                _d(_scalar(raw, "R037")),
            )
            den = high - low
            return None if den == 0 else (last - low) / den
        if identity in {"D042", "D043"}:
            short = "R247" if identity == "D042" else "R246"
            return _DEC100 * (_d(_scalar(raw, "R249")) - _d(_scalar(raw, short)))
        if identity == "D047":
            return _DEC10000 * (_d(_scalar(raw, "R257")) - _d(_scalar(raw, "R256")))
        if identity in {"D057", "D058", "D059"}:
            pair = {"D057": ("R238", "R239"), "D058": ("R239", "R236"), "D059": ("R236", "R240")}[
                identity
            ]
            a, b = (_d(_scalar(raw, x)) for x in pair)
            return None if b == 0 else _named_tuple((("point_difference", a - b), ("ratio", a / b)))
        if identity == "D060":
            vix = _d(_scalar(raw, "R236"))
            return None if vix == 0 else _d(_scalar(raw, "R237")) / vix
        if identity == "D076":
            return _d(_scalar(derived, "D072")) - _d(_scalar(derived, "D071"))
        if identity == "D077":
            q = _d(_scalar(derived, "D072"))
            smh = _latest(derived, "D073")
            soxx = _latest(derived, "D074")
            if smh and soxx:
                return (_d(smh.value) + _d(soxx.value)) / Decimal(2) - q
            proxy = params.get("single_proxy")
            if proxy in {"D073", "D074"}:
                return _d(_scalar(derived, str(proxy))) - q
            return None
        if identity == "D088":
            mid = _d(_scalar(derived, "D087"))
            bid = _d(_scalar(raw, "R034"))
            ask = _d(_scalar(raw, "R035"))
            return None if mid == 0 else _DEC100 * (ask - bid) / mid
        if identity == "D089":
            spot = _d(_scalar(raw, "R118"))
            return None if spot == 0 else _d(_scalar(raw, "R014")) / spot
        if identity == "D090":
            ratio_value = _eval_k02("D089", raw, derived, params, contexts)
            if ratio_value is None:
                return None
            log_ratio = _d(ratio_value)
            return None if log_ratio <= 0 else log_ratio.ln()
        if identity == "D092":
            return (_d(_scalar(raw, "R084")) + _d(_scalar(raw, "R093"))) / Decimal(2)
        if identity == "D093":
            return _DEC100 * (_d(_scalar(raw, "R093")) - _d(_scalar(raw, "R084")))
        if identity in {"D097", "D098"}:
            term_points: list[tuple[Decimal, Decimal]] = []
            for item in derived.get("D096", ()):
                n = _named(item.value)
                day = n.get("expiry_day", _metadata(item).get("expiry_day"))
                iv = n.get(
                    "iv", n.get("value", item.value if type(item.value) is Decimal else None)
                )
                if day is not None and iv is not None:
                    term_points.append((_d(day), _d(iv)))
            term_points.sort()
            if identity == "D097" and len(term_points) >= 2:
                (d1, i1), (d2, i2) = term_points[:2]
                return None if d2 == d1 else _DEC100 * (i2 - i1) / (d2 - d1)
            if identity == "D098" and len(term_points) >= 3:
                (d1, i1), (d2, i2), (d3, i3) = term_points[:3]
                if d2 == d1 or d3 in (d2, d1):
                    return None
                return (
                    Decimal(2)
                    * (_DEC100 * (i3 - i2) / (d3 - d2) - _DEC100 * (i2 - i1) / (d2 - d1))
                    / (d3 - d1)
                )
            return None
        if identity in {"D099", "D100", "D101"}:
            # Every IV point must join its own source-native R112 delta by
            # exact option contract; copied/independently labelled IV metadata
            # is not authoritative delta truth. D099/100 also require the
            # declared R015 strike. Never silently discard a missing or
            # contradictory member of the selected expiry surface.
            raw_fields = ("R111", "R112", "R015") if identity != "D101" else ("R111", "R112")
            by_field: dict[str, dict[str, KernelValueV1]] = {}
            for field in raw_fields:
                selected: dict[str, KernelValueV1] = {}
                for item in raw.get(field, ()):
                    cid = _metadata(item).get("contract_id")
                    if type(cid) is not str or not cid or cid in selected:
                        return None
                    selected[cid] = item
                if not selected:
                    return None
                by_field[field] = selected
            contracts = set(by_field["R111"])
            if any(set(by_field[field]) != contracts for field in raw_fields[1:]):
                return None
            skew_points: list[tuple[str, str, Decimal, Decimal]] = []
            for cid in sorted(contracts):
                iv_point = by_field["R111"][cid]
                delta_point = by_field["R112"][cid]
                iv_meta = _metadata(iv_point)
                expiry = iv_meta.get("expiry")
                right = _option_right(iv_meta)
                if (
                    expiry is None
                    or right not in {"c", "call", "p", "put"}
                    or not _source_identity_compatible(iv_point, delta_point)
                    or _metadata(iv_point).get("source_provider")
                    != _metadata(delta_point).get("source_provider")
                ):
                    return None
                if identity != "D101":
                    strike_point = by_field["R015"][cid]
                    if (
                        not _source_identity_compatible(iv_point, strike_point)
                        or _metadata(iv_point).get("source_provider")
                        != _metadata(strike_point).get("source_provider")
                        or iv_meta.get("strike") is None
                        or _d(strike_point.value) != _d(iv_meta["strike"])
                    ):
                        return None
                skew_points.append(
                    (str(expiry), right, abs(_d(delta_point.value)), _d(iv_point.value))
                )
            target = Decimal("0.25") if identity in {"D099", "D101"} else Decimal("0.10")
            complete_skew_groups: list[tuple[Decimal, Decimal, tuple[Decimal, ...]]] = []
            for expiry in sorted({point[0] for point in skew_points}):
                expiry_points = tuple(point for point in skew_points if point[0] == expiry)
                calls = tuple(
                    iv
                    for _, right, delta, iv in expiry_points
                    if right in {"c", "call"} and delta == target
                )
                puts = tuple(
                    iv
                    for _, right, delta, iv in expiry_points
                    if right in {"p", "put"} and delta == target
                )
                if len(calls) != 1 or len(puts) != 1:
                    continue
                atm = tuple(iv for _, _, delta, iv in expiry_points if delta == Decimal("0.50"))
                complete_skew_groups.append((calls[0], puts[0], atm))
            if len(complete_skew_groups) != 1:
                return None
            call, put, atm_candidates = complete_skew_groups[0]
            if identity in {"D099", "D100"}:
                return _DEC100 * (put - call)
            if not atm_candidates:
                return None
            return _DEC100 * (put + call - Decimal(2) * _sample_mean(atm_candidates))
        if identity in {"D107", "D108"}:
            return _DEC100 * (
                _d(_scalar(derived, "D096"))
                - _d(_scalar(derived, "D035" if identity == "D107" else "D036"))
            )
        if identity == "D109":
            # The catalogue declares D091 (versioned delta-bucket classification)
            # as the ATM selector; a D087 midpoint does not own R112 delta.
            atm_labels: dict[str, str] = {}
            if derived.get("D091"):
                label = params.get("atm_delta_bucket")
                if type(label) is not str or not label:
                    return None
                for bucket_occurrence in derived["D091"]:
                    contract = _metadata(bucket_occurrence).get("contract_id")
                    if type(contract) is not str or contract in atm_labels:
                        return None
                    atm_labels[contract] = str(bucket_occurrence.value)
            atm_by_contract_pair: dict[tuple[str, object], dict[str, Decimal]] = {}
            for item in derived.get("D087", ()):
                metadata = _metadata(item)
                right = _option_right(metadata)
                delta = metadata.get("delta")
                contract = metadata.get("contract_id")
                expiry = metadata.get("expiry")
                strike = metadata.get("strike")
                if (
                    right not in {"call", "c", "put", "p"}
                    or (delta is None and not atm_labels)
                    or expiry is None
                    or strike is None
                ):
                    return None
                if atm_labels:
                    if type(contract) is not str or contract not in atm_labels:
                        return None
                    if atm_labels[contract] != params["atm_delta_bucket"]:
                        continue
                elif abs(_d(delta)) != Decimal("0.50"):
                    continue
                canonical_right = "call" if right in {"call", "c"} else "put"
                pair_values = atm_by_contract_pair.setdefault((str(expiry), strike), {})
                if canonical_right in pair_values:
                    return None
                pair_values[canonical_right] = _d(item.value)
            complete_straddle_groups = [
                values for values in atm_by_contract_pair.values() if set(values) == {"call", "put"}
            ]
            if len(complete_straddle_groups) != 1:
                return None
            return complete_straddle_groups[0]["call"] + complete_straddle_groups[0]["put"]
        if identity == "D110":
            spot = _d(_scalar(raw, "R118"))
            return None if spot == 0 else _DEC100 * _d(_scalar(derived, "D109")) / spot
        if identity == "D116":
            if len(raw.get("R041", ())) != 1:
                return None
            present = tuple(rid for rid in ("R047", "R048") if raw.get(rid))
            if len(present) != 1 or len(raw[present[0]]) != 1:
                return None
            volume = _d(raw["R041"][0].value)
            oi = _d(raw[present[0]][0].value)
            if not (volume.is_finite() and oi.is_finite()) or volume < 0 or oi <= 0:
                return None
            return volume / oi
        if identity in {"D118", "D119"}:
            numerator_id, denominator_id = (
                ("R049", "R050") if identity == "D118" else ("R047", "R048")
            )
            ratio_denominator = sum(_decimal_values(raw, denominator_id), _DEC0)
            return (
                None
                if ratio_denominator == 0
                else sum(_decimal_values(raw, numerator_id), _DEC0) / ratio_denominator
            )
        if identity == "D123":
            values = raw.get("R047", ()) or raw.get("R048", ())
            return _d(values[0].value) - _d(values[1].value) if len(values) == 2 else None
        if identity in {"D131", "D134", "D135"}:
            depth_events = _book_events(raw)
            depth_state = _book_final_state(depth_events)
            if depth_state is None:
                return None
            depth_side = None if identity == "D131" else ("bid" if identity == "D134" else "ask")
            depth_rows = [
                (key, value)
                for key, value in depth_state.items()
                if depth_side is None or key[1] == depth_side
            ]
            if identity == "D131":
                depth_mid = _d(_scalar(derived, "D087"))
                max_distance = params.get("depth_price_distance")
                if max_distance is None:
                    return None
                depth_rows = [
                    (key, value)
                    for key, value in depth_rows
                    if abs(value[0] - depth_mid) <= _d(max_distance)
                ]
            else:
                depth_levels = params.get("depth_levels")
                if type(depth_levels) is not int or depth_levels <= 0:
                    return None
                depth_rows = sorted(depth_rows, key=lambda item: item[0][2])[:depth_levels]
            return sum((value[1] for _, value in depth_rows), _DEC0) if depth_rows else None
        if identity == "D136":
            bid, ask = _d(_scalar(derived, "D134")), _d(_scalar(derived, "D135"))
            den = bid + ask
            return None if den == 0 else (bid - ask) / den
        if identity == "D137":
            bid, ask, bs, asz = (_d(_scalar(raw, x)) for x in ("R034", "R035", "R033", "R036"))
            den = bs + asz
            return None if den == 0 else (ask * bs + bid * asz) / den
        if identity == "D143":
            # Every direct-exchange mutation must carry its own exact native
            # venue, operation, side, level, price and quantity. Dropping a
            # missing field would alter the concentration denominator.
            direct_field_ids = ("R192", "R193", "R194", "R195", "R196", "R197")
            event_ids = [{v.occurrence_id for v in raw.get(rid, ())} for rid in direct_field_ids]
            if not event_ids[0] or any(ids != event_ids[0] for ids in event_ids[1:]):
                return None
            direct_events = _book_events(raw, direct=True)
            if len(direct_events) != len(event_ids[0]):
                return None
            direct_state = _book_final_state(direct_events)
            if direct_state is None:
                return None
            by_venue: dict[str, Decimal] = {}
            for (venue, _, _), (_, size) in direct_state.items():
                by_venue[venue] = by_venue.get(venue, _DEC0) + abs(size)
            total = sum(by_venue.values(), _DEC0)
            return None if total <= 0 else sum(((v / total) ** 2 for v in by_venue.values()), _DEC0)
        if identity == "D144":
            for field_ids in (
                ("R185", "R187", "R188", "R189", "R190"),
                ("R192", "R193", "R194", "R195", "R196", "R197"),
            ):
                event_ids = [{v.occurrence_id for v in raw.get(rid, ())} for rid in field_ids]
                if not event_ids[0] or any(ids != event_ids[0] for ids in event_ids[1:]):
                    return None
                if len(_book_events(raw, direct=field_ids[0] == "R192")) != len(event_ids[0]):
                    return None
            smart = _book_final_state(_book_events(raw))
            direct = _book_final_state(_book_events(raw, direct=True))
            if smart is None or direct is None:
                return None
            gap_rows: list[tuple[str, tuple[tuple[str, Decimal], ...]]] = []
            for (venue, side, position), (direct_price, direct_size) in sorted(direct.items()):
                smart_value = smart.get(("", side, position))
                if smart_value is None:
                    continue
                smart_price, smart_size = smart_value
                gap_rows.append(
                    (
                        f"{side}:{position}:{venue}",
                        (
                            ("price_difference", smart_price - direct_price),
                            ("depth_difference", smart_size - direct_size),
                        ),
                    )
                )
            return tuple(gap_rows) if gap_rows else None
        if identity == "D151":
            members = params.get("basket_membership")
            if type(members) is not tuple or not members:
                return None

            def by_subject(rid: str) -> dict[str, Decimal]:
                return {
                    v.subject_instrument: _d(v.value)
                    for v in raw.get(rid, ())
                    if v.subject_instrument in members
                }

            last_by_subject, open_by_subject, vwap_by_subject, prior_by_subject = (
                by_subject(x) for x in ("R037", "R043", "R137", "R042")
            )

            def fraction(reference: dict[str, Decimal]) -> Decimal | None:
                eligible_members = [
                    member
                    for member in members
                    if member in last_by_subject and member in reference
                ]
                return (
                    None
                    if not eligible_members
                    else Decimal(
                        sum(
                            last_by_subject[member] > reference[member]
                            for member in eligible_members
                        )
                    )
                    / Decimal(len(eligible_members))
                )

            positive_fraction = fraction(open_by_subject)
            above_vwap_fraction = fraction(vwap_by_subject)
            above_prior_fraction = fraction(prior_by_subject)
            if (
                positive_fraction is None
                or above_vwap_fraction is None
                or above_prior_fraction is None
            ):
                return None
            return _named_tuple(
                (
                    ("positive_return_fraction", positive_fraction),
                    ("above_vwap_fraction", above_vwap_fraction),
                    ("above_prior_close_fraction", above_prior_fraction),
                )
            )
        if identity == "D164":
            from ._financial_policy import named, number

            execution = named(_scalar(derived, "D133"))
            base = _d(execution["expected_slippage_currency"])
            if number(base) < 0:
                return None
            schedule = _context(contexts, api.ExecutionCostScheduleVersionV1)
            if schedule is None or execution["currency"] != schedule.cost_units:
                return None
            commission = sum((v for _, v in schedule.commission_rules), _DEC0)
            fees = sum((v for _, v in schedule.fee_rules), _DEC0)
            multi = sum((v for _, v in schedule.multi_leg_incremental_cost_rules), _DEC0)
            return _named_tuple(
                (
                    ("expected_spread_slippage_cost", base),
                    ("commissions", commission),
                    ("fees", fees),
                    ("multi_leg_incremental_cost", multi),
                    ("total", base + commission + fees + multi),
                    ("currency", schedule.cost_units),
                )
            )
        if identity == "D168":
            candidate = _context(contexts, api.CandidateStructureContextV1)
            if candidate is None:
                return None
            fields = {
                raw_id: _latest_by_subject(raw, raw_id)
                for raw_id in ("R112", "R115", "R116", "R117", "R016")
            }
            if any(
                contract not in field
                for contract in candidate.leg_contract_identities
                for field in fields.values()
            ):
                return None
            signed_quantities: dict[str, Decimal] = {}
            for contract, side, quantity in zip(
                candidate.leg_contract_identities,
                candidate.leg_sides,
                candidate.leg_quantities,
                strict=True,
            ):
                if quantity <= 0 or side.lower() not in {"buy", "sell"}:
                    return None
                signed_quantities[contract] = quantity if side.lower() == "buy" else -quantity
            names = ("delta", "gamma", "vega", "theta")
            raw_ids = ("R112", "R115", "R116", "R117")
            output = []
            for name, raw_id in zip(names, raw_ids, strict=True):
                total = sum(
                    (
                        signed_quantities[contract]
                        * _d(fields["R016"][contract].value)
                        * _d(fields[raw_id][contract].value)
                        for contract in candidate.leg_contract_identities
                    ),
                    _DEC0,
                )
                output.append((name, total))
            return tuple(output)
        if identity == "D170":
            candidate = _context(contexts, api.CandidateStructureContextV1)
            if candidate is None:
                return None
            strike_by_contract = {}
            right_by_contract = {}
            for item in raw.get("R014", ()):
                contract = _metadata(item).get("contract_id", item.subject_instrument)
                if type(contract) is not str:
                    return None
                if contract in strike_by_contract:
                    return None
                strike_by_contract[contract] = _d(item.value)
                right = str(
                    _metadata(item).get("option_right", _metadata(item).get("right", ""))
                ).lower()
                if right not in {"call", "c", "put", "p"}:
                    return None
                right_by_contract[contract] = "call" if right in {"call", "c"} else "put"
            premium_by_contract = {}
            for item in derived.get("D087", ()):
                contract = _metadata(item).get("contract_id", item.subject_instrument)
                if type(contract) is not str:
                    return None
                if contract in premium_by_contract:
                    return None
                premium_by_contract[contract] = _d(item.value)
            assumed = dict(candidate.premium_assumptions)
            legs = []
            for contract, side, quantity in zip(
                candidate.leg_contract_identities,
                candidate.leg_sides,
                candidate.leg_quantities,
                strict=True,
            ):
                if contract not in strike_by_contract or contract not in right_by_contract:
                    return None
                if side.lower() not in {"buy", "sell"}:
                    return None
                premium = premium_by_contract.get(contract, assumed.get(contract))
                if premium is None:
                    return None
                if (
                    contract in premium_by_contract
                    and contract in assumed
                    and premium_by_contract[contract] != assumed[contract]
                ):
                    return None
                sign = _DEC1 if side.lower() == "buy" else -_DEC1
                legs.append(
                    (
                        right_by_contract[contract],
                        strike_by_contract[contract],
                        sign * quantity,
                        _d(premium),
                    )
                )
            if len(legs) != len(candidate.leg_contract_identities):
                return None
            strikes = sorted({strike for _, strike, _, _ in legs})
            if not strikes:
                return None
            premium_constant = -sum(
                (signed_qty * premium for _, _, signed_qty, premium in legs), _DEC0
            )
            boundaries = [_DEC0, *strikes]
            roots: set[Decimal] = set()
            for i, left in enumerate(boundaries):
                segment_right = boundaries[i + 1] if i + 1 < len(boundaries) else None
                probe = (
                    (left + segment_right) / Decimal(2)
                    if segment_right is not None
                    else left + _DEC1
                )
                slope = _DEC0
                intercept = premium_constant
                for option_right, strike, signed_qty, _ in legs:
                    if option_right == "call" and probe >= strike:
                        slope += signed_qty
                        intercept -= signed_qty * strike
                    elif option_right == "put" and probe <= strike:
                        slope -= signed_qty
                        intercept += signed_qty * strike
                if slope == 0:
                    if intercept == 0:
                        return None
                    continue
                root = -intercept / slope
                if root < 0:
                    continue
                if segment_right is None:
                    if root >= left:
                        roots.add(root)
                elif left <= root <= segment_right:
                    roots.add(root)
            return tuple(sorted(roots)) if roots else None
        if identity == "D179":
            execution_fill = _d(_scalar(raw, "R229"))
            arrival_benchmark = _d(_scalar(raw, "R221"))
            execution_side = str(params.get("side", "")).lower()
            slippage_sign = (
                Decimal(1)
                if execution_side == "buy"
                else Decimal(-1)
                if execution_side == "sell"
                else None
            )
            if slippage_sign is None or arrival_benchmark == 0:
                return None
            slip = slippage_sign * (execution_fill - arrival_benchmark)
            return _named_tuple(
                (("price_slippage", slip), ("bps_slippage", _DEC10000 * slip / arrival_benchmark))
            )
        if identity == "D180":
            filled, remaining = _d(_scalar(raw, "R219")), _d(_scalar(raw, "R220"))
            den = filled + remaining
            return None if den <= 0 else filled / den
        if identity in {"D181", "D182", "D183", "D184"}:
            greek = {"D181": "R112", "D182": "R115", "D183": "R116", "D184": "R117"}[identity]
            # A live portfolio total requires every admitted position leg.
            # Intersecting the native occurrence IDs without checking their
            # equality silently drops legs with absent Greeks/multipliers.
            leg_ids = {item.occurrence_id for item in raw.get("R212", ())}
            greek_ids = {item.occurrence_id for item in raw.get(greek, ())}
            multiplier_ids = {item.occurrence_id for item in raw.get("R016", ())}
            if not leg_ids or leg_ids != greek_ids or leg_ids != multiplier_ids:
                return None
            rows = _align_occurrence_fields(raw, ("R212", greek, "R016"))
            live_contexts = [c for c in contexts if type(c) is api.LivePositionContextV1]
            if live_contexts:
                from ._financial_policy import greek_input_unit

                if len(live_contexts) != 1:
                    return None
                live = live_contexts[0]
                if len(live.m00_occurrence_refs) != len(live.leg_contract_identities):
                    return None
                source_rows = {row["R212"].occurrence_id: row for row in rows}
                if set(source_rows) != set(live.m00_occurrence_refs):
                    return None
                scopes = [c for c in contexts if type(c) is api.RiskScopeContextV1]
                if len(scopes) > 1:
                    return None
                for contract, quantity, multiplier, source in zip(
                    live.leg_contract_identities, live.signed_quantities, live.multipliers,
                    live.m00_occurrence_refs, strict=True,
                ):
                    row = source_rows[source]
                    if (
                        row["R212"].value != quantity or row["R016"].value != multiplier
                        or any(
                            dict(v.metadata).get("contract_id") != contract for v in row.values()
                        )
                        or dict(row["R212"].metadata).get("canonical_units") != "contracts"
                        or dict(row["R016"].metadata).get("canonical_units")
                        != "shares_per_contract"
                    ):
                        return None
                    if scopes:
                        scope = scopes[0]
                        if (
                            scope.live_position_ref
                            != api.VersionRefV1(live.context_id, live.version)
                            or set(scope.position_membership_source_refs)
                            != set(live.m00_occurrence_refs)
                                or dict(row[greek].metadata).get("currency") != scope.currency_code
                                or dict(row[greek].metadata).get("canonical_units")
                                != greek_input_unit(identity, scope.currency_code)
                        ):
                            return None
            return (
                sum(
                    (_d(r["R212"].value) * _d(r[greek].value) * _d(r["R016"].value) for r in rows),
                    _DEC0,
                )
                if rows
                else None
            )
        if identity == "D185":
            realised_pnl, unrealised_pnl, total_pnl = (
                _scalar(raw, x) for x in ("R214", "R215", "R216")
            )
            if realised_pnl is None or unrealised_pnl is None or total_pnl is None:
                return None
            return _named_tuple(
                (
                    ("realised", _d(realised_pnl)),
                    ("unrealised", _d(unrealised_pnl)),
                    ("total", _d(total_pnl)),
                )
            )
        if identity == "D190":
            cset = _context(contexts, api.CandidateSetContextV1)
            hold = (
                _d(_scalar(derived, "D188"))
                if type(_scalar(derived, "D188")) is Decimal
                else _d(_named(_scalar(derived, "D188")).get("utility"))
            )
            if cset is None:
                return None
            vals = {
                str(_named(v.value).get("candidate")): _d(_named(v.value).get("value"))
                for v in derived.get("D165", ())
                if _named(v.value).get("candidate") is not None
            }
            eligible = [vals[c] for c in cset.candidate_identities if c in vals]
            return None if not eligible else max(eligible) - hold
        if identity == "D191":
            fill_components = _named(_scalar(derived, "D133"))
            cost_components = _named(_scalar(derived, "D164"))
            if "currency" in params and (
                fill_components.get("currency") != params["currency"]
                or cost_components.get("currency") != params["currency"]
            ):
                return None
            expected_fill = fill_components.get("expected_fill_price")
            if expected_fill is None:
                return None
            liquidation_quantity = _d(params["liquidation_quantity"])
            contract_multiplier = _d(params["multiplier"])
            if liquidation_quantity <= 0 or contract_multiplier <= 0:
                return None
            non_slippage = (
                _d(cost_components.get("commissions", 0))
                + _d(cost_components.get("fees", 0))
                + _d(cost_components.get("multi_leg_incremental_cost", 0))
            )
            return _d(expected_fill) * liquidation_quantity * contract_multiplier - non_slippage
        if identity == "D193":
            # The signed per-fill slippage is already established by D179
            # against the admitted R221 arrival benchmark.  D087 remains a
            # declared quote predecessor but is not that execution benchmark.
            # Recomputing from D087 silently changes the cost basis.
            commission_paid = _d(_scalar(raw, "R233"))
            executed_quantity = _d(_scalar(raw, "R228"))
            contract_multiplier = _d(_scalar(raw, "R016"))
            signed_slippage = _named(_scalar(derived, "D179")).get("price_slippage")
            if signed_slippage is None:
                return None
            return commission_paid + _d(signed_slippage) * executed_quantity * contract_multiplier
        if identity == "D199":
            observed = _d(_scalar(raw, "R216"))
            explained = sum(
                (_d(_scalar(derived, d)) for d in ("D194", "D195", "D196", "D197", "D198")), _DEC0
            )
            pnl = _context(contexts, api.PnLConventionVersionV1)
            cost = (
                _d(_scalar(derived, "D193"))
                if pnl is not None and pnl.observed_total_pnl_is_gross_of_execution_costs
                else _DEC0
            )
            return observed - explained - cost
    except (TypeError, ValueError, ArithmeticError, KeyError):
        return None
    return None


def _eval_k03(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    params: dict[str, object],
    as_of: datetime,
) -> object | None:
    fixed_seconds = {"D019": 60, "D020": 300, "D021": 1800, "D027": 300, "D094": 300}
    fixed_days = {"D066": 1, "D067": 1, "D068": 1, "D069": 1, "D095": 1}
    source_map = {
        "D019": "R143",
        "D020": "R143",
        "D021": "R143",
        "D027": "R137",
        "D044": "R252",
        "D045": "R249",
        "D046": "R255",
        "D048": "R245",
        "D049": "R274",
        "D050": "R275",
        "D051": "R276",
        "D052": "R236",
        "D053": "R237",
        "D054": "R238",
        "D055": "R239",
        "D056": "R240",
        "D066": "R270",
        "D067": "R271",
        "D068": "R272",
        "D069": "R273",
        "D094": "R111",
        "D095": "R111",
    }
    try:
        if identity in {"D022", "D023"}:
            current = _d(_scalar(raw, "R037"))
            reference = _d(_scalar(raw, "R043" if identity == "D022" else "R042"))
            return None if current <= 0 or reference <= 0 else (current / reference).ln()
        if identity == "D024":
            q1 = _d(_scalar(derived, "D019"))
            q5 = _d(_scalar(derived, "D020")) / Decimal(5)
            q30 = _d(_scalar(derived, "D021")) / Decimal(30)
            return _named_tuple(
                (
                    ("q1", q1),
                    ("q5", q5),
                    ("q30", q30),
                    ("accel_1v5", q1 - q5),
                    ("accel_5v30", q5 - q30),
                )
            )
        if identity == "D026":
            current, vwap = _d(_scalar(raw, "R037")), _d(_scalar(raw, "R137"))
            return (
                None
                if vwap == 0
                else _named_tuple(
                    (
                        ("price_difference", current - vwap),
                        ("percent_difference", _DEC100 * (current / vwap - _DEC1)),
                    )
                )
            )
        if identity in {"D071", "D072", "D073", "D074", "D075"}:
            current, prior = _d(_scalar(raw, "R037")), _d(_scalar(raw, "R042"))
            return None if current <= 0 or prior <= 0 else (current / prior).ln()
        if identity == "D103":
            # A parallel surface shift compares an identical strike/expiry grid
            # across two ordered snapshots. Intersecting grids would silently
            # turn a missing contract into a valid, but different, surface.
            surfaces: dict[str, dict[str, KernelValueV1]] = {
                "prior": {},
                "current": {},
            }
            for point in raw.get("R111", ()):
                metadata = _metadata(point)
                snapshot, grid_key = metadata.get("snapshot"), metadata.get("grid_key")
                if (
                    type(snapshot) is not str
                    or snapshot not in surfaces
                    or type(grid_key) is not str
                    or not grid_key
                    or grid_key in surfaces[snapshot]
                ):
                    return None
                surfaces[snapshot][grid_key] = point
            prior_grid, current_grid = surfaces["prior"], surfaces["current"]
            if not current_grid or set(current_grid) != set(prior_grid):
                return None
            if max(v.effective_at_utc for v in prior_grid.values()) >= min(
                v.effective_at_utc for v in current_grid.values()
            ):
                return None
            return _DEC100 * _sample_mean(
                tuple(
                    _d(current_grid[key].value) - _d(prior_grid[key].value)
                    for key in sorted(current_grid)
                )
            )
        if identity == "D104":
            # Programme-owner D104-20261012-01: changes must be paired within
            # their own 25-/10-delta skew family before the relative difference.
            seconds = _i(params.get("anchor_seconds", 0))
            if seconds <= 0:
                return None
            pair25 = _history_anchor(derived.get("D099", ()), as_of=as_of, seconds=seconds)
            pair10 = _history_anchor(derived.get("D100", ()), as_of=as_of, seconds=seconds)
            if pair25 is None or pair10 is None:
                return None
            selected = (*pair25, *pair10)
            identities = tuple(
                (_metadata(value).get("underlying_instrument"), _metadata(value).get("expiry"))
                for value in selected
            )
            if (
                any(
                    type(subject) is not str or not subject or type(expiry) is not str or not expiry
                    for subject, expiry in identities
                )
                or len(set(identities)) != 1
                or len({item.subject_instrument for item in selected}) != 1
                or selected[0].effective_at_utc != selected[2].effective_at_utc
                or selected[1].effective_at_utc != selected[3].effective_at_utc
            ):
                return None
            return (
                _d(pair10[0].value)
                - _d(pair10[1].value)
                - (_d(pair25[0].value) - _d(pair25[1].value))
            )
        rid = source_map.get(identity)
        if rid is None:
            return None
        if identity in fixed_seconds:
            pair = _history_anchor(
                raw.get(rid, ()),
                as_of=as_of,
                seconds=_i(params.get("anchor_seconds", fixed_seconds[identity])),
            )
        elif identity in fixed_days:
            pair = _history_anchor(
                raw.get(rid, ()),
                as_of=as_of,
                days=_i(params.get("anchor_days", fixed_days[identity])),
            )
        else:
            if "anchor_seconds" in params:
                pair = _history_anchor(
                    raw.get(rid, ()), as_of=as_of, seconds=_i(params["anchor_seconds"])
                )
            elif "anchor_days" in params:
                pair = _history_anchor(
                    raw.get(rid, ()), as_of=as_of, days=_i(params["anchor_days"])
                )
            else:
                return None
        if pair is None:
            return None
        current_point, reference_point = pair
        if identity in {"D094", "D095"} and not _same_option_history_selection(
            current_point, reference_point
        ):
            return None
        current_value, reference_value = _d(current_point.value), _d(reference_point.value)
        if identity == "D027":
            minutes = Decimal(
                str(
                    (
                        current_point.effective_at_utc - reference_point.effective_at_utc
                    ).total_seconds()
                )
            ) / Decimal(60)
            return (
                None
                if minutes <= 0 or reference_value == 0
                else _named_tuple(
                    (
                        ("price_per_minute", (current_value - reference_value) / minutes),
                        (
                            "percent_per_minute",
                            _DEC100 * (current_value / reference_value - _DEC1) / minutes,
                        ),
                    )
                )
            )
        if identity in {"D044", "D045", "D046"}:
            return _DEC10000 * (current_value - reference_value)
        if identity in {"D048", "D049", "D050", "D051"}:
            return (
                None
                if reference_value == 0
                else _DEC100 * (current_value / reference_value - _DEC1)
            )
        if identity in {"D052", "D053", "D054", "D055", "D056"}:
            return (
                None
                if reference_value == 0
                else _named_tuple(
                    (
                        ("point_change", current_value - reference_value),
                        ("percent_change", _DEC100 * (current_value / reference_value - _DEC1)),
                    )
                )
            )
        if identity in {"D094", "D095"}:
            return _DEC100 * (current_value - reference_value)
        return (
            None
            if current_value <= 0 or reference_value <= 0
            else (current_value / reference_value).ln()
        )
    except (TypeError, ValueError, ArithmeticError):
        return None


def _eval_k04(
    identity: str, raw: dict[str, tuple[KernelValueV1, ...]], params: dict[str, object]
) -> object | None:
    try:
        if identity == "D083":
            members = params.get("basket_membership")
            if type(members) is not tuple or len(members) < 2:
                return None
            current_by_subject = {v.subject_instrument: _d(v.value) for v in raw.get("R037", ())}
            prior_by_subject = {v.subject_instrument: _d(v.value) for v in raw.get("R042", ())}
            cross_returns = tuple(
                (current_by_subject[m] / prior_by_subject[m]).ln()
                for m in members
                if m in current_by_subject
                and m in prior_by_subject
                and current_by_subject[m] > 0
                and prior_by_subject[m] > 0
            )
            return _sample_sd(cross_returns) if len(cross_returns) == len(members) else None
        rid = {
            "D028": "R041",
            "D029": "R144",
            "D030": "R062",
            "D031": "R063",
            "D105": "R183",
            "D106": "R183",
            "D117": "R041",
        }.get(identity)
        if identity == "D063":
            # Actual and consensus belong to the same native release.  An
            # intersection silently drops an incomplete newer release (or
            # selected historical sample), then standardises against stale
            # surprises.  Require complete co-referenced native membership.
            actuals = raw.get("R286", ())
            consensuses = raw.get("R285", ())
            rows = _align_occurrence_fields(raw, ("R286", "R285"))
            if (
                not actuals
                or len(rows) != len(actuals)
                or len(rows) != len(consensuses)
                or any(row["R286"].effective_at_utc != row["R285"].effective_at_utc for row in rows)
            ):
                return None
            values = tuple(
                (
                    _d(r["R286"].value) - _d(r["R285"].value),
                    max(v.effective_at_utc for v in r.values()),
                )
                for r in rows
            )
        elif identity == "D028":
            # Each volume observation must carry its own source-native elapsed
            # session fraction.  R044 is not merely a presence prerequisite:
            # historical R041 samples from other session fractions must never
            # silently enter the normalised D028 baseline.
            volumes = raw.get("R041", ())
            fractions = raw.get("R044", ())
            rows = _align_occurrence_fields(raw, ("R041", "R044"))
            if (
                not volumes
                or len(rows) != len(volumes)
                or len(rows) != len(fractions)
                or any(
                    row["R041"].effective_at_utc != row["R044"].effective_at_utc
                    or not _DEC0 <= _d(row["R044"].value) <= Decimal(1)
                    for row in rows
                )
            ):
                return None
            current_row = rows[-1]
            current_fraction = _d(current_row["R044"].value)
            values = (
                *(
                    (_d(row["R041"].value), row["R041"].effective_at_utc)
                    for row in rows[:-1]
                    if _d(row["R044"].value) == current_fraction
                ),
                (_d(current_row["R041"].value), current_row["R041"].effective_at_utc),
            )
        elif identity in {"D029", "D030", "D031"}:
            # P_BASELINE owns the source-native comparison bucket.  An
            # unrelated minute of the session must not be counted simply
            # because it was received more recently than a matching bar.
            if params.get("matching_rule") != "source_native_time_of_day_bucket":
                return None
            candidates = raw.get(rid or "", ())
            if not candidates:
                return None
            if any(
                v.source_temporal_kind != "true_instant"
                or type(_metadata(v).get("time_of_day_bucket")) is not str
                or not _metadata(v)["time_of_day_bucket"]
                for v in candidates
            ):
                return None
            current = max(
                candidates,
                key=lambda v: (v.effective_at_utc, v.received_ts_utc, v.occurrence_id),
            )
            current_bucket = _metadata(current)["time_of_day_bucket"]
            values = (
                *(
                    (_d(v.value), v.effective_at_utc)
                    for v in candidates
                    if v is not current and _metadata(v)["time_of_day_bucket"] == current_bucket
                ),
                (_d(current.value), current.effective_at_utc),
            )
        elif rid:
            values = tuple((_d(v.value), v.effective_at_utc) for v in raw.get(rid, ()))
        else:
            return None
        if not values:
            return None
        ordered_values = tuple(sorted(values, key=lambda x: x[1]))
        current_value, current_at = ordered_values[-1]
        history_values = tuple(v for v, at in ordered_values[:-1] if at < current_at)
        # A historical baseline is an exact parameterised window, never the
        # number of observations the reader happened to return today.
        if "history_count" not in params or "minimum_sample" not in params:
            return None
        count = _i(params["history_count"])
        minimum = _i(params["minimum_sample"])
        if count < minimum or minimum < 2 or len(history_values) < count:
            return None
        history_values = history_values[-count:]
        if identity == "D028":
            return (
                None
                if len(history_values) < minimum or _sample_mean(history_values) == 0
                else current_value / _sample_mean(history_values)
            )
        if identity == "D105":
            if len(history_values) < minimum:
                return None
            lo, hi = min(history_values), max(history_values)
            return None if hi == lo else _DEC100 * (current_value - lo) / (hi - lo)
        if identity == "D106":
            if len(history_values) < minimum:
                return None
            below = sum(v < current_value for v in history_values)
            equal = sum(v == current_value for v in history_values)
            return (
                _DEC100
                * (Decimal(below) + Decimal("0.5") * Decimal(equal))
                / Decimal(len(history_values))
            )
        if len(history_values) < minimum:
            return None
        sd = _sample_sd(history_values)
        return None if sd is None else (current_value - _sample_mean(history_values)) / sd
    except (TypeError, ValueError, ArithmeticError):
        return None


def _log_returns(values: tuple[Decimal, ...]) -> tuple[Decimal, ...] | None:
    if len(values) < 2 or any(v <= 0 for v in values):
        return None
    return tuple((values[i] / values[i - 1]).ln() for i in range(1, len(values)))


def _eval_k05(
    identity: str, raw: dict[str, tuple[KernelValueV1, ...]], params: dict[str, object]
) -> object | None:
    try:
        if identity == "D039":
            highs = {v.occurrence_id: _d(v.value) for v in raw.get("R141", ())}
            lows = {v.occurrence_id: _d(v.value) for v in raw.get("R142", ())}
            bars = sorted(raw.get("R143", ()), key=lambda v: v.effective_at_utc)
            bar_count = _i(params["bar_count"])
            if bar_count <= 0:
                return None
            # Select the actual latest configured bars by the close series,
            # *before* testing co-referenced highs and lows.  Filtering
            # incomplete bars first silently substitutes stale bars from
            # outside the required window and fabricates a complete ATR.
            if len(bars) < bar_count + 1:
                return None
            trs = []
            for idx in range(len(bars) - bar_count, len(bars)):
                oid = bars[idx].occurrence_id
                if (
                    oid not in highs
                    or oid not in lows
                    or bars[idx].effective_at_utc - bars[idx - 1].effective_at_utc
                    != timedelta(minutes=5)
                ):
                    return None
                prev = _d(bars[idx - 1].value)
                high, low = highs[oid], lows[oid]
                trs.append(max(high - low, abs(high - prev), abs(low - prev)))
            return _sample_mean(tuple(trs))
        # Required sample instants are supplied by the immutable versioned
        # calendar/sampling policy.  The return count alone cannot prove five
        # trading days or any other named interval was actually covered.
        required = _i(params["required_intervals"])
        expected = params.get("required_sample_instants_utc")
        if (
            required <= 0
            or type(expected) is not tuple
            or len(expected) != required + 1
            or any(
                type(instant) is not datetime
                or instant.tzinfo is None
                or instant.utcoffset() != timedelta(0)
                for instant in expected
            )
            or tuple(sorted(set(expected))) != expected
        ):
            return None
        # In the presence of revisions, the newest receipt visible at cutoff
        # wins for each declared sample instant; unknown/missing instants fail.
        by_instant: dict[datetime, KernelValueV1] = {}
        for value in raw.get("R151", ()):
            instant = value.effective_at_utc
            if instant in expected and (
                instant not in by_instant
                or (value.received_ts_utc, value.occurrence_id)
                > (by_instant[instant].received_ts_utc, by_instant[instant].occurrence_id)
            ):
                by_instant[instant] = value
        if set(by_instant) != set(expected):
            return None
        price_series = tuple(_d(by_instant[instant].value) for instant in expected)
        log_returns = _log_returns(price_series)
        if log_returns is None or len(log_returns) != required:
            return None
        selected_returns = log_returns
        if identity == "D038":
            rv = sum((r * r for r in selected_returns), _DEC0)
            bv = (
                Decimal(str(3.141592653589793))
                / Decimal(2)
                * sum(
                    (
                        abs(selected_returns[i]) * abs(selected_returns[i - 1])
                        for i in range(1, len(selected_returns))
                    ),
                    _DEC0,
                )
            )
            return max(rv - bv, _DEC0)
        dt = _d(params["trading_year_fraction_per_interval"])
        den = dt * Decimal(len(selected_returns))
        return None if den <= 0 else (sum((r * r for r in selected_returns), _DEC0) / den).sqrt()
    except (TypeError, ValueError, ArithmeticError, KeyError):
        return None


def _factor_rows(
    derived: dict[str, tuple[KernelValueV1, ...]], identities: tuple[str, ...]
) -> tuple[tuple[Decimal, ...], ...] | None:
    maps = [
        {v.effective_at_utc: _d(v.value) for v in derived.get(identity, ())}
        for identity in identities
    ]
    common = set(maps[0]) if maps else set()
    for mapping in maps[1:]:
        common &= set(mapping)
    if not common:
        return None
    ordered = sorted(common)
    return tuple(tuple(mapping[t] for t in ordered) for mapping in maps)


def _eval_k06(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    params: dict[str, object],
) -> object | None:
    try:
        if identity in {"D079", "D080", "D081", "D078"}:
            aligned = _factor_rows(derived, ("D075", "D071", "D076", "D077"))
            minimum = _i(params.get("minimum_sample", 4))
            if aligned is None:
                return None
            y, m, t, s = aligned
            # P_REGRESSION selects an immutable trailing sample subset; older
            # states cannot enter a fit simply because they remain in durable
            # predecessor history. Without an explicit count, retain the
            # accepted whole-available-history direct-kernel convention.
            count = _i(params.get("history_count", len(y) - (1 if identity == "D078" else 0)))
            if count < minimum:
                return None
            if identity == "D078":
                if len(y) < count + 1:
                    return None
                y, m, t, s = (series[-(count + 1) :] for series in (y, m, t, s))
                fit = _ols(y[:-1], (m[:-1], t[:-1], s[:-1]))
                if fit is None:
                    return None
                # The accepted D078 expression expressly consumes the three
                # predecessor coefficient occurrences of this *same* fit.
                # Reconstructing a different private model and ignoring those
                # declared inputs would make the D079-D081 graph ornamental.
                for did, expected in (("D079", fit[1]), ("D080", fit[2]), ("D081", fit[3])):
                    candidates = derived.get(did, ())
                    if len(candidates) != 1 or _d(candidates[0].value) != expected:
                        return None
                return y[-1] - (fit[0] + fit[1] * m[-1] + fit[2] * t[-1] + fit[3] * s[-1])
            if len(y) < count:
                return None
            y, m, t, s = (series[-count:] for series in (y, m, t, s))
            fit = _ols(y, (m, t, s))
            if fit is None:
                return None
            return fit[{"D079": 1, "D080": 2, "D081": 3}[identity]]
        if identity == "D082":
            # R151 supplies closes, not precomputed returns.  Pearson on
            # untransformed price levels is a different financial statistic.
            # The P_REGRESSION window selects exactly N aligned *returns*,
            # which require N+1 actual positive closing-price observations.
            minimum = _i(params["minimum_sample"])
            count = _i(params["history_count"])
            values = raw.get("R151", ())
            by_subject: dict[str, dict[datetime, Decimal]] = {}
            for item in values:
                series = by_subject.setdefault(item.subject_instrument, {})
                if item.effective_at_utc in series:
                    # Contradictory same-time native closes are not a window.
                    return None
                series[item.effective_at_utc] = _d(item.value)
            subjects = tuple(sorted(by_subject))
            if minimum < 2 or count < minimum or len(subjects) < 2:
                return None
            # A missing member of any selected native time point must not be
            # repaired by intersection: this would bridge a gap and produce
            # a materially different return interval for that subject.
            times = sorted(set().union(*(set(series) for series in by_subject.values())))
            if len(times) < count + 1:
                return None
            window = times[-(count + 1) :]
            returns: dict[str, tuple[Decimal, ...]] = {}
            for subject in subjects:
                series = by_subject[subject]
                if any(at not in series for at in window):
                    return None
                calculated = _log_returns(tuple(series[at] for at in window))
                if calculated is None:
                    return None
                returns[subject] = calculated
            matrix = []
            for a in subjects:
                row = []
                for b in subjects:
                    correlation = _pearson(returns[a], returns[b])
                    if correlation is None:
                        return None
                    row.append(correlation)
                matrix.append(tuple(row))
            return _named_tuple((("subjects", subjects), ("matrix", tuple(matrix))))
        if identity == "D138":
            midpoint = _d(_scalar(derived, "D011"))
            native_fields = ("R189", "R190", "R188")
            # Each price/size/side triple denotes one native book row.  An
            # incomplete triple may not vanish from an OLS regression by
            # intersection of projected field-occurrence IDs.
            ids_by_field = [
                {value.occurrence_id for value in raw.get(field, ())} for field in native_fields
            ]
            if not ids_by_field[0] or any(ids != ids_by_field[0] for ids in ids_by_field[1:]):
                return None
            book_rows = _align_occurrence_fields(raw, native_fields)
            for native_row in book_rows:
                base = native_row["R189"]
                source = (
                    _metadata(base).get("source_provider"),
                    _metadata(base).get("source_variant"),
                )
                if any(
                    item.subject_instrument != base.subject_instrument
                    or (
                        _metadata(item).get("source_provider"),
                        _metadata(item).get("source_variant"),
                    )
                    != source
                    for item in native_row.values()
                ):
                    return None
                if str(native_row["R188"].value).lower() not in {"bid", "ask"}:
                    return None
                price, amount = _d(native_row["R189"].value), _d(native_row["R190"].value)
                if not price.is_finite() or not amount.is_finite() or amount < 0:
                    return None
            slope_output: list[tuple[str, Decimal]] = []
            for side in ("bid", "ask"):
                side_rows = [r for r in book_rows if str(r["R188"].value).lower() == side]
                side_rows.sort(key=lambda r: abs(_d(r["R189"].value) - midpoint))
                cumulative = _DEC0
                distance_values: list[Decimal] = []
                cumulative_sizes: list[Decimal] = []
                for r in side_rows:
                    cumulative += _d(r["R190"].value)
                    distance_values.append(abs(_d(r["R189"].value) - midpoint))
                    cumulative_sizes.append(cumulative)
                slope = _ols_slope(tuple(distance_values), tuple(cumulative_sizes))
                if slope is None:
                    return None
                slope_output.append((f"{side}_slope", slope))
            return tuple(slope_output)
        if identity == "D156":
            histories = derived.get("D155", ())
            ridge = _d(params.get("ridge_coefficient"))
            if len(histories) < 2:
                return None
            state_vectors: list[tuple[Decimal, ...]] = []
            for occurrence in histories:
                raw_vector = occurrence.value
                if type(raw_vector) is not tuple:
                    return None
                vector_values = tuple(
                    _d(element[1])
                    for element in raw_vector
                    if type(element) is tuple
                    and len(element) >= 2
                    and type(element[1]) in {Decimal, int}
                )
                if not vector_values:
                    return None
                state_vectors.append(vector_values)
            n = len(state_vectors[0])
            if any(len(v) != n for v in state_vectors):
                return None
            cols = tuple(tuple(row[j] for row in state_vectors) for j in range(n))
            corr = tuple(
                tuple(_DEC1 if i == j else (_pearson(cols[i], cols[j]) or _DEC0) for j in range(n))
                for i in range(n)
            )
            cov: list[list[Decimal]] = []
            means = tuple(_sample_mean(c) for c in cols)
            for i in range(n):
                cov.append(
                    [
                        sum(
                            ((row[i] - means[i]) * (row[j] - means[j]) for row in state_vectors),
                            _DEC0,
                        )
                        / Decimal(len(state_vectors) - 1)
                        + (ridge if i == j else _DEC0)
                        for j in range(n)
                    ]
                )
            inverse_cols = []
            for j in range(n):
                solution = _solve(
                    [list(r) for r in cov], [Decimal(1) if i == j else _DEC0 for i in range(n)]
                )
                if solution is None:
                    return None
                inverse_cols.append(solution)
            precision = [[inverse_cols[j][i] for j in range(n)] for i in range(n)]
            partial = []
            for i in range(n):
                row = []
                for j in range(n):
                    row.append(
                        _DEC1
                        if i == j
                        else -precision[i][j] / (precision[i][i] * precision[j][j]).sqrt()
                    )
                partial.append(tuple(row))
            return _named_tuple(
                (("correlation_matrix", corr), ("partial_correlation_matrix", tuple(partial)))
            )
    except (TypeError, ValueError, ArithmeticError, KeyError):
        return None
    return None


def _d186_profile(
    params: dict[str, object],
) -> tuple[tuple[str, str, tuple[object, ...], Decimal, Decimal], ...] | None:
    """Resolve the explicitly authorised flat, versioned P_RULE feature schema.

    A feature is (D155 component D-id, existing K07 scalar extractor, arguments).
    Profile indices are strictly contiguous and weights/scales are exact Decimals.
    """
    feature_keys = {name for name in params if name.startswith("similarity_feature:")}
    if not feature_keys:
        return None
    n = len(feature_keys)
    if set(params) != {
        f"similarity_{kind}:{index}"
        for index in range(1, n + 1)
        for kind in ("feature", "weight", "scale")
    }:
        return None
    allowed_extractors = {
        "component",
        "weighted_component_sum",
        "class_probability",
        "probability_margin",
        "normalised_entropy",
        "distribution_cdf",
        "upper_tail",
        "distribution_mean",
        "distribution_variance",
        "matrix_entry",
        "row_l2",
        "frobenius",
    }
    argument_counts: dict[str, int] = {
        "class_probability": 1,
        "probability_margin": 0,
        "normalised_entropy": 0,
        "distribution_cdf": 1,
        "upper_tail": 1,
        "distribution_mean": 0,
        "distribution_variance": 0,
        "matrix_entry": 2,
        "row_l2": 1,
        "frobenius": 0,
    }
    output: list[tuple[str, str, tuple[object, ...], Decimal, Decimal]] = []
    for index in range(1, n + 1):
        specification = params[f"similarity_feature:{index}"]
        weight = params[f"similarity_weight:{index}"]
        scale = params[f"similarity_scale:{index}"]
        if (
            type(specification) is not tuple
            or len(specification) < 2
            or type(specification[0]) is not str
            or specification[0] not in catalogue_row("D155").derived_dependencies
            or type(specification[1]) is not str
            or specification[1] not in allowed_extractors
            or type(weight) is not Decimal
            or not weight.is_finite()
            or weight < 0
            or type(scale) is not Decimal
            or not scale.is_finite()
            or scale <= 0
        ):
            return None
        extractor = specification[1]
        arguments = specification[2:]
        if extractor in argument_counts and len(arguments) != argument_counts[extractor]:
            return None
        if extractor == "weighted_component_sum" and (not arguments or len(arguments) % 2):
            return None
        if extractor == "component" and any(type(part) not in {str, int} for part in arguments):
            return None
        output.append((specification[0], extractor, arguments, weight, scale))
    if sum((v[3] for v in output), _DEC0) != _DEC1:
        return None
    if len({(v[0], v[1], v[2]) for v in output}) != n:
        return None
    return tuple(output)


def _d186_components(value: object) -> dict[str, tuple[object, str]] | None:
    """Read actual K16 D155 components without implicit scalarisation."""
    if type(value) is not tuple:
        return None
    components: dict[str, tuple[object, str]] = {}
    for item in value:
        if (
            type(item) is not tuple
            or len(item) != 4
            or type(item[0]) is not str
            or type(item[2]) is not str
            or not item[2]
            or type(item[3]) is not tuple
        ):
            return None
        component_id, component_value, _, metadata = item
        try:
            info = dict(metadata)
        except (TypeError, ValueError):
            return None
        if (
            component_id in components
            or component_id not in catalogue_row("D155").derived_dependencies
            or info.get("units") != catalogue_row(component_id).units
        ):
            return None
        components[component_id] = (component_value, info["units"])
    if set(components) != set(catalogue_row("D155").derived_dependencies):
        return None
    return components


def _d186_selected_states(
    derived: dict[str, tuple[KernelValueV1, ...]],
    contexts: tuple[object, ...],
    as_of: datetime,
    cutoff: datetime,
) -> tuple[KernelValueV1, KernelValueV1] | None:
    entry_ref = _context(contexts, api.EntryStateContextV1)
    if entry_ref is None:
        return None
    history = derived.get("D155", ())
    anchor = tuple(v for v in history if v.occurrence_id == entry_ref.d155_occurrence_id)
    if len(anchor) != 1 or len({v.occurrence_id for v in history}) != len(history):
        return None
    eligible = tuple(
        v
        for v in history
        if v.source_temporal_kind == "derived"
        and v.effective_at_utc <= as_of
        and v.received_ts_utc <= cutoff
    )
    if not eligible or anchor[0] not in eligible:
        return None
    current = max(
        eligible,
        key=lambda v: (v.effective_at_utc, v.received_ts_utc, v.occurrence_id),
    )
    entry = anchor[0]
    if (
        entry.occurrence_id == current.occurrence_id
        or entry.effective_at_utc >= current.effective_at_utc
        or entry.subject_instrument != current.subject_instrument
        or _metadata(entry).get("result_shape") != "structured"
        or _metadata(current).get("result_shape") != "structured"
        or _metadata(entry).get("units") != catalogue_row("D155").units
        or _metadata(entry).get("units") != _metadata(current).get("units")
        or _d186_components(entry.value) is None
        or _d186_components(current.value) is None
    ):
        return None
    old = _d186_components(entry.value)
    new = _d186_components(current.value)
    if (
        old is None
        or new is None
        or tuple(old) != tuple(new)
        or any(
            old[name][1] != new[name][1] or type(old[name][0]) is not type(new[name][0])
            for name in old
        )
    ):
        return None
    return (entry, current)


def _eval_k08(
    identity: str,
    raw: dict[str, tuple[KernelValueV1, ...]],
    derived: dict[str, tuple[KernelValueV1, ...]],
    params: dict[str, object],
    contexts: tuple[object, ...],
    as_of: datetime,
    cutoff: datetime,
) -> object | None:
    if identity in {"D175", "D178", "D189", "D192"}:
        from ._financial_policy import action_decision, hedge_adjustment, limit_price, risk_budget

        try:
            if identity == "D192":
                policy_value = action_decision(derived, params, as_of, cutoff)
            elif identity == "D189":
                policy_value = hedge_adjustment(
                    derived, params, contexts, as_of, cutoff
                )
            else:
                financial_policy = risk_budget if identity == "D175" else limit_price
                policy_value = financial_policy(
                    raw, derived, params, contexts, as_of, cutoff
                )
        except (TypeError, ValueError, ArithmeticError, KeyError, AttributeError):
            return None
        return policy_value
    try:
        if identity == "D007":
            policy = _context(contexts, api.RequiredFieldPolicyV1)
            return (
                None
                if policy is None or not policy.requirements
                else Decimal(sum(bool(raw.get(req)) for req in policy.requirements))
                / Decimal(len(policy.requirements))
            )
        if identity == "D015":
            trade = _d(_scalar(raw, "R120"))
            mid = _d(_scalar(derived, "D011"))
            if trade > mid:
                return 1
            if trade < mid:
                return -1
            trade_history = sorted(raw.get("R120", ()), key=lambda v: v.effective_at_utc)
            current_trade = _latest(raw, "R120")
            if current_trade:
                prior_trade = next(
                    (
                        v
                        for v in reversed(trade_history)
                        if v.effective_at_utc < current_trade.effective_at_utc
                        and _d(v.value) != trade
                    ),
                    None,
                )
                if prior_trade:
                    return 1 if trade > _d(prior_trade.value) else -1
            return 0
        if identity == "D016":
            sizes = raw.get("R121", ())
            signs = _observation_signs(sizes, derived.get("D015", ()))
            if signs is None:
                return None
            return sum((Decimal(signs[v.occurrence_id][0]) * _d(v.value) for v in sizes), _DEC0)
        if identity == "D065":
            pre = _d(params.get("pre_window_seconds"))
            post = _d(params.get("post_window_seconds"))
            threshold = _d(params.get("importance_threshold"))
            event_candidates: list[tuple[datetime, KernelValueV1]] = []
            for event_value in raw.get("R284", ()):
                event_time = event_value.value
                if type(event_time) is datetime and as_of - timedelta(
                    seconds=float(post)
                ) <= event_time <= as_of + timedelta(seconds=float(pre)):
                    event_candidates.append((event_time, event_value))
            if not event_candidates:
                return False
            _, selected_event = min(
                event_candidates,
                key=lambda pair: (
                    abs((pair[0] - as_of).total_seconds()),
                    pair[0],
                ),
            )
            event_metadata = dict(selected_event.metadata)
            key = tuple(
                event_metadata.get(k) for k in ("event_id", "source_provider", "source_variant")
            )
            if (
                type(key[0]) is not str
                or not key[0]
                or type(key[1]) is not str
                or not key[1]
                or type(key[2]) is not str
            ):
                return None
            predecessors = tuple(
                item
                for item in derived.get("D064", ())
                if tuple(
                    dict(item.metadata).get(k)
                    for k in ("event_id", "source_provider", "source_variant")
                )
                == key
            )
            if not predecessors:
                return None
            chosen = _latest({"D064": predecessors}, "D064")
            if chosen is None:
                return None
            try:
                importance = _d(chosen.value)
            except (TypeError, ValueError):
                return None
            return importance >= threshold
        if identity == "D091":
            delta = abs(_d(_scalar(raw, "R112")))
            bounds = params.get("delta_bucket_boundaries")
            labels = params.get("delta_bucket_labels")
            if (
                type(bounds) is not tuple
                or type(labels) is not tuple
                or len(bounds) != len(labels) + 1
            ):
                return None
            for i, label in enumerate(labels):
                lo, hi = _d(bounds[i]), _d(bounds[i + 1])
                if lo <= delta < (hi if i < len(labels) - 1 else hi + Decimal("1e-40")):
                    return str(label)
            return None
        if identity == "D120":
            fields = ("R120", "R121", "R015")
            if not all(raw.get(field) for field in fields):
                return None
            input_ids = [{v.occurrence_id for v in raw[field]} for field in fields]
            if not all(ids == input_ids[0] for ids in input_ids[1:]):
                return None
            signed_rows = _align_occurrence_fields(raw, fields)
            signs = _observation_signs(
                tuple(row["R120"] for row in signed_rows), derived.get("D015", ())
            )
            if signs is None:
                return None
            signed_contracts = _DEC0
            signed_premium = _DEC0
            for signed_row in signed_rows:
                oid = signed_row["R120"].occurrence_id
                if not all(
                    _source_identity_compatible(signed_row["R120"], v) for v in signed_row.values()
                ):
                    return None
                sign = Decimal(signs[oid][0])
                size = _d(signed_row["R121"].value)
                price = _d(signed_row["R120"].value)
                mult = _d(signed_row["R015"].value)
                signed_contracts += sign * size
                signed_premium += sign * size * price * mult
            return _named_tuple(
                (
                    ("signed_contracts", signed_contracts),
                    ("signed_premium_notional", signed_premium),
                )
            )
        if identity in {"D121", "D122"}:
            # K08 exact per-contract grouping: D120, D091 and D085 live in
            # independent D-occurrence namespaces.  Contract selection must be
            # reconstructed from each child's immutable selection identity;
            # an equal UUID or a free-form `group` metadata string proves nothing.
            group_id = "D091" if identity == "D121" else "D085"
            flows = derived.get("D120", ())
            labels = derived.get(group_id, ())
            contract_keys = (
                "contract_id",
                "underlying_instrument",
                "expiry",
                "strike",
                "option_right",
            )

            def contract_key(item: KernelValueV1) -> tuple[object, ...] | None:
                meta = _metadata(item)
                values = tuple(meta.get(key) for key in contract_keys)
                if any(value is None for value in values):
                    return None
                return values

            if not flows or not labels:
                return None
            signed_by_contract: dict[tuple[object, ...], tuple[Decimal, Decimal]] = {}
            labels_by_contract: dict[tuple[object, ...], object] = {}
            for flow in flows:
                flow_key = contract_key(flow)
                parts = _named(flow.value)
                signed_qty = parts.get("signed_contracts")
                notional = parts.get("signed_premium_notional")
                if (
                    flow_key is None
                    or flow_key in signed_by_contract
                    or type(signed_qty) is not Decimal
                    or type(notional) is not Decimal
                ):
                    return None
                signed_by_contract[flow_key] = (signed_qty, notional)
            for label in labels:
                label_key = contract_key(label)
                if label_key is None or label_key in labels_by_contract:
                    return None
                labels_by_contract[label_key] = label.value
            if set(signed_by_contract) != set(labels_by_contract):
                return None
            bucket_bounds = params.get("dte_bucket_boundaries")
            bucket_labels = params.get("dte_bucket_labels")
            if identity == "D122" and (
                type(bucket_bounds) is not tuple
                or type(bucket_labels) is not tuple
                or len(bucket_bounds) != len(bucket_labels) + 1
                or not bucket_labels
                or any(
                    _d(bucket_bounds[i]) >= _d(bucket_bounds[i + 1])
                    for i in range(len(bucket_labels))
                )
            ):
                return None
            grouped: dict[tuple[str, ...], tuple[Decimal, Decimal]] = {}
            for key in sorted(signed_by_contract):
                _, _, expiry, _, right = key
                if type(expiry) is not str or not expiry or type(right) is not str or not right:
                    return None
                label = labels_by_contract[key]
                group: tuple[str, ...]
                if identity == "D121":
                    if type(label) is not str or not label:
                        return None
                    group = (expiry, right.lower(), label)
                else:
                    if type(label) is not int or label < 0:
                        return None
                    assert type(bucket_labels) is tuple and type(bucket_bounds) is tuple
                    matches = [
                        str(bucket_labels[i])
                        for i in range(len(bucket_labels))
                        if _d(bucket_bounds[i])
                        <= Decimal(label)
                        < (
                            _d(bucket_bounds[i + 1])
                            if i < len(bucket_labels) - 1
                            else _d(bucket_bounds[i + 1]) + Decimal("1e-40")
                        )
                    ]
                    if len(matches) != 1 or not matches[0]:
                        return None
                    group = (expiry, matches[0])
                old_qty, old_notional = grouped.get(group, (_DEC0, _DEC0))
                qty, premium = signed_by_contract[key]
                grouped[group] = (old_qty + qty, old_notional + premium)
            return tuple(
                (
                    key,
                    _named_tuple(
                        (
                            ("signed_contracts", value[0]),
                            ("signed_premium_notional", value[1]),
                        )
                    ),
                )
                for key, value in sorted(grouped.items())
            )
        if identity == "D124":
            # Call and put OI are separate raw observations; strike/expiry
            # concentration groups both rights by their original *contract*
            # identities.  Raw observation IDs are not buckets.  A missing
            # or duplicate contract identity would make HHI unreconstructable.
            if params.get("grouping") != "strike_expiry":
                return None
            by_strike_expiry: dict[tuple[str, Decimal], Decimal] = {}
            seen_contracts: set[tuple[object, ...]] = set()
            for raw_id, right in (("R047", "call"), ("R048", "put")):
                for item in raw.get(raw_id, ()):
                    meta = _metadata(item)
                    cid = meta.get("contract_id")
                    subject = meta.get("underlying_instrument")
                    expiry = meta.get("expiry")
                    strike = meta.get("strike")
                    if (
                        type(cid) is not str
                        or not cid
                        or type(subject) is not str
                        or not subject
                        or subject != item.subject_instrument
                        or type(expiry) is not str
                        or not expiry
                        or _option_right(meta) != right
                    ):
                        return None
                    try:
                        strike_amount = _d(strike)
                        oi = _d(item.value)
                    except (TypeError, ValueError, ArithmeticError):
                        return None
                    if (
                        not strike_amount.is_finite()
                        or strike_amount <= 0
                        or not oi.is_finite()
                        or oi < 0
                    ):
                        return None
                    contract = (subject, cid, expiry, strike_amount, right)
                    if contract in seen_contracts:
                        return None
                    seen_contracts.add(contract)
                    key = (expiry, strike_amount)
                    by_strike_expiry[key] = by_strike_expiry.get(key, _DEC0) + oi
            total = sum(by_strike_expiry.values(), _DEC0)
            if total <= 0:
                return None
            oi_shares = tuple((key, oi / total) for key, oi in sorted(by_strike_expiry.items()))
            hhi = sum((share * share for _, share in oi_shares), _DEC0)
            return _named_tuple((("shares", oi_shares), ("hhi", hhi)))
        if identity == "D128":
            bounds = params.get("spot_distance_boundaries")
            if type(bounds) is not tuple or len(bounds) < 2:
                return None
            bins = [_DEC0] * (len(bounds) - 1)
            total = _DEC0
            for item in derived.get("D125", ()):
                n = _named(item.value)
                g = abs(_d(n.get("gamma_exposure")))
                dist = abs(_d(n.get("spot_distance")))
                total += g
                for i in range(len(bins)):
                    if (
                        _d(bounds[i])
                        <= dist
                        < (
                            _d(bounds[i + 1])
                            if i < len(bins) - 1
                            else _d(bounds[i + 1]) + Decimal("1e-40")
                        )
                    ):
                        bins[i] += g
                        break
            if total <= 0:
                return None
            shares = tuple(v / total for v in bins)
            return _named_tuple((("shares", shares), ("hhi", sum((s * s for s in shares), _DEC0))))
        if identity in {"D139", "D140", "D141"}:
            # A projected native event is atomic: a missing operation/side/level/
            # quantity cannot silently remove one mutation from the history.
            native_book_fields: tuple[str, ...] = ("R185", "R187", "R188", "R190")
            if identity == "D141":
                native_book_fields = (*native_book_fields, "R189")
            native_occurrences = [
                {v.occurrence_id for v in raw.get(field, ())} for field in native_book_fields
            ]
            if not native_occurrences[0] or any(
                item != native_occurrences[0] for item in native_occurrences[1:]
            ):
                return None
            book_mutations = reconstruct_book(_book_events(raw))
            window = _d(params["window_seconds"])
            if window <= 0 or len(book_mutations) != len(native_occurrences[0]):
                return None
            if identity in {"D139", "D140"}:
                # P_RULE establishes non-overlapping positive book-level bands;
                # a source position outside the configured bands cannot be
                # silently omitted or assigned an invented fallback bucket.
                upper_bounds = params.get("level_bucket_upper_bounds")
                if (
                    type(upper_bounds) is not tuple
                    or not upper_bounds
                    or any(type(bound) is not int or bound <= 0 for bound in upper_bounds)
                    or tuple(sorted(set(upper_bounds))) != upper_bounds
                ):
                    return None
                typed_upper_bounds = cast(tuple[int, ...], upper_bounds)
                attr = "inserted_size" if identity == "D139" else "removed_size"
                selected_mutations = [m for m in book_mutations if getattr(m, attr) > 0]
                groups: dict[tuple[str, int], tuple[int, Decimal]] = {}
                for mutation in selected_mutations:
                    side = mutation.event.side.lower()
                    level = mutation.event.position
                    if side not in {"bid", "ask"} or level <= 0:
                        return None
                    bucket = next((b for b in typed_upper_bounds if level <= b), None)
                    if bucket is None:
                        return None
                    key = (side, bucket)
                    bucket_count, bucket_size = groups.get(key, (0, _DEC0))
                    groups[key] = (bucket_count + 1, bucket_size + getattr(mutation, attr))
                total_count_rate = Decimal(len(selected_mutations)) / window
                size = sum((getattr(m, attr) for m in selected_mutations), _DEC0) / window
                by_side_level = tuple(
                    (key, (Decimal(n) / window, total / window))
                    for key, (n, total) in sorted(groups.items())
                )
                return _named_tuple(
                    (
                        ("event_count_rate", total_count_rate),
                        ("size_rate", size),
                        ("by_side_level", by_side_level),
                    )
                )
            depleted = [m for m in book_mutations if m.depleted_size > 0]
            credited = _DEC0
            total = sum((m.depleted_size for m in depleted), _DEC0)
            max_dt = _d(params["replenishment_max_seconds"])
            if max_dt <= 0:
                return None
            for dep in depleted:
                restoration = next(
                    (
                        m
                        for m in book_mutations
                        if m.event.event_time_utc > dep.event.event_time_utc
                        and m.event.side == dep.event.side
                        and m.event.price == dep.event.price
                        and m.restored_size > 0
                        and Decimal(
                            str((m.event.event_time_utc - dep.event.event_time_utc).total_seconds())
                        )
                        <= max_dt
                    ),
                    None,
                )
                if restoration:
                    credited += min(dep.depleted_size, restoration.restored_size)
            return None if total <= 0 else credited / total
        if identity == "D142":
            resilience_events = _book_events(raw)
            levels = params.get("depth_levels")
            shock_depth_fraction = _d(params.get("shock_depth_fraction"))
            shock_spread_multiple = _d(params.get("shock_spread_multiple"))
            recovery_depth_fraction = _d(params.get("recovery_depth_fraction"))
            recovery_spread_multiple = _d(params.get("recovery_spread_multiple"))
            if (
                type(levels) is not int
                or levels <= 0
                or shock_depth_fraction <= 0
                or shock_spread_multiple <= 0
                or recovery_depth_fraction <= 0
                or recovery_spread_multiple <= 0
            ):
                return None
            ordered_events = _ordered_book_events(resilience_events)
            resilience_state: dict[tuple[str, str, int], tuple[Decimal, Decimal]] = {}
            snapshots: list[tuple[datetime, Decimal, Decimal]] = []
            for book_event in ordered_events:
                _apply_book_event(resilience_state, book_event)
                bids = sorted(
                    ((k, v) for k, v in resilience_state.items() if k[1] == "bid"),
                    key=lambda item: (item[0][2], -item[1][0]),
                )[:levels]
                asks = sorted(
                    ((k, v) for k, v in resilience_state.items() if k[1] == "ask"),
                    key=lambda item: (item[0][2], item[1][0]),
                )[:levels]
                if not bids or not asks:
                    continue
                best_bid = max(v[0] for _, v in bids)
                best_ask = min(v[0] for _, v in asks)
                spread = best_ask - best_bid
                if spread < 0:
                    return None
                depth = sum((v[1] for _, v in (*bids, *asks)), _DEC0)
                snapshots.append((book_event.event_time_utc, depth, spread))
            if len(snapshots) < 3:
                return None
            shock_index: int | None = None
            pre_snapshot: tuple[datetime, Decimal, Decimal] | None = None
            for i in range(1, len(snapshots)):
                prior_snapshot = snapshots[i - 1]
                current_snapshot = snapshots[i]
                if prior_snapshot[1] <= 0 or prior_snapshot[2] < 0:
                    continue
                depth_shock = current_snapshot[1] <= prior_snapshot[1] * shock_depth_fraction
                spread_shock = (
                    prior_snapshot[2] > 0
                    and current_snapshot[2] >= prior_snapshot[2] * shock_spread_multiple
                )
                if depth_shock or spread_shock:
                    shock_index = i
                    pre_snapshot = prior_snapshot
                    break
            if shock_index is None or pre_snapshot is None:
                return None
            shock_snapshot = snapshots[shock_index]
            for recovery_snapshot in snapshots[shock_index + 1 :]:
                if (
                    recovery_snapshot[1] >= pre_snapshot[1] * recovery_depth_fraction
                    and recovery_snapshot[2] <= pre_snapshot[2] * recovery_spread_multiple
                ):
                    seconds = Decimal(
                        str((recovery_snapshot[0] - shock_snapshot[0]).total_seconds())
                    )
                    if seconds < 0:
                        return None
                    return _named_tuple(
                        (
                            ("seconds", seconds),
                            ("recovered_depth", recovery_snapshot[1]),
                            ("recovered_spread", recovery_snapshot[2]),
                            ("pre_shock_depth", pre_snapshot[1]),
                            ("pre_shock_spread", pre_snapshot[2]),
                            ("shock_depth", shock_snapshot[1]),
                            ("shock_spread", shock_snapshot[2]),
                        )
                    )
            return None
        if identity == "D166":
            return _d(_scalar(derived, "D159")) >= _d(params.get("minimum_identifiability")) and _d(
                _scalar(derived, "D165")
            ) >= _d(params.get("minimum_utility"))
        if identity == "D167":
            cset = _context(contexts, api.CandidateSetContextV1)
            if cset is None:
                return None
            candidate_flags = {
                str(_named(v.value).get("candidate")): _named(v.value).get("value")
                for v in derived.get("D166", ())
            }
            candidate_values = {
                str(_named(v.value).get("candidate")): _d(_named(v.value).get("value"))
                for v in derived.get("D165", ())
                if _named(v.value).get("candidate") is not None
            }
            lawful = [
                c
                for c in cset.candidate_identities
                if c in candidate_flags and c in candidate_values
            ]
            if not lawful:
                return None
            eligible = [c for c in lawful if candidate_flags[c] is True]
            if not eligible:
                return "no_trade"
            best = max(candidate_values[c] for c in eligible)
            return next(
                c
                for c in cset.candidate_identities
                if c in eligible and candidate_values[c] == best
            )
        if identity == "D176":
            from ._financial_policy import number, one, validate_budget

            for predecessor in ("D175", "D165", "D163", "D132"):
                one(derived, predecessor, as_of, cutoff)
            budget, _, _, risk = validate_budget(derived["D175"][0].value, params, as_of, cutoff)
            if (params["risk_per_unit_currency"] != budget["currency"]
                    or params["risk_per_unit_definition"] != budget["risk_definition_id"]):
                return None
            per_unit = number(params["risk_per_unit"])
            uncertainty = number(params["uncertainty_multiplier"])
            liquidity = number(params["liquidity_multiplier"])
            if min(per_unit, uncertainty, liquidity) <= 0:
                return None
            return int(risk // (per_unit * uncertainty * liquidity))
        if identity == "D186":
            features = _d186_profile(params)
            values = derived.get("D155", ())
            if features is None or len(values) != 2:
                return None
            entry, current = values
            old = _d186_components(entry.value)
            new = _d186_components(current.value)
            if old is None or new is None:
                return None
            d2 = _DEC0
            deltas = []
            for index, (did, extractor, arguments, weight, scale) in enumerate(features, 1):
                entry_scalar = extract_scalar(old[did][0], extractor, arguments)
                current_scalar = extract_scalar(new[did][0], extractor, arguments)
                difference = current_scalar - entry_scalar
                standardised = difference / scale
                d2 += weight * standardised * standardised
                deltas.append((f"{index}:{did}:{extractor}", (difference, standardised)))
            return _named_tuple(
                (
                    ("similarity", (-Decimal("0.5") * d2).exp()),
                    ("distance_squared", d2),
                    ("deltas", tuple(deltas)),
                )
            )
        if identity == "D208":
            info = _d(_scalar(derived, "D202"))
            decay = _d(_scalar(derived, "D207"))
            thresholds = params.get("classification_thresholds")
            if type(thresholds) is not tuple:
                return None
            for spec in thresholds:
                name, min_info, max_decay = str(spec).split("|")
                if info >= _d(min_info) and decay <= _d(max_decay):
                    return name
            return "non-informative"
        if identity == "D209":
            schedule = _context(contexts, api.RecalculationScheduleV1)
            latest = _latest(raw, "R001")
            if latest is None and schedule is None:
                return None
            return _named_tuple(
                (
                    ("trigger", "m00_receipt" if latest is not None else "scheduled"),
                    ("at", latest.received_ts_utc if latest is not None else as_of),
                )
            )
    except (TypeError, ValueError, ArithmeticError, KeyError):
        return None
    return None


def _eval_k16(
    identity: str, derived: dict[str, tuple[KernelValueV1, ...]], params: dict[str, object]
) -> object | None:
    if identity != "D155":
        return None
    order = params.get("component_order")
    if type(order) is not tuple or not order or len(set(order)) != len(order):
        return None
    if set(order) != set(catalogue_row(identity).derived_dependencies):
        return None
    output = []
    for did in order:
        item = _latest(derived, str(did))
        if item is None:
            return None
        # Preserve original units/quality plus exact temporal freshness facts;
        # do not fabricate a missing quality grade.
        metadata = _metadata(item)
        if not metadata.get("units"):
            return None
        preserved = (
            *item.metadata,
            ("effective_at_utc", item.effective_at_utc),
            ("received_ts_utc", item.received_ts_utc),
        )
        output.append((str(did), item.value, item.occurrence_id, preserved))
    return tuple(output)


def _eval_k17(
    raw: dict[str, tuple[KernelValueV1, ...]], params: dict[str, object], as_of: datetime
) -> object | None:
    # The authoritative D145 raw set is R187/R188/R189/R190. Resolve
    # consecutive top-of-book states without an internal synthetic input.
    # A replacement level is explicit only with delete and insert events;
    # an update at an unseen price cannot silently erase an unknown level.
    try:
        window = _d(params["window_seconds"])
        if window <= 0:
            return None
        start = as_of - timedelta(seconds=float(window))
        required_fields = ("R187", "R188", "R189", "R190")
        # Each book mutation is one native record with four required fields.
        # Intersection-only alignment would silently drop a partially projected
        # update and calculate OFI from a fabricated shorter event sequence.
        event_ids = tuple(
            tuple(item.occurrence_id for item in raw.get(field, ())) for field in required_fields
        )
        if any(len(ids) != len(set(ids)) for ids in event_ids):
            return None
        if not event_ids or any(set(ids) != set(event_ids[0]) for ids in event_ids[1:]):
            return None
        rows = _align_occurrence_fields(raw, required_fields)
        if not rows:
            return None
        state: dict[tuple[str, Decimal], Decimal] = {}
        predecessor: tuple[Decimal, Decimal, Decimal, Decimal] | None = None
        total = _DEC0
        transitions = 0
        # Same-event-time mutations form one deterministic book-state transition.
        # Intermediate partial states are not invented as market snapshots.
        instants = sorted({max(item.effective_at_utc for item in row.values()) for row in rows})
        for timestamp in instants:
            if timestamp > as_of:
                continue
            batch = tuple(
                row
                for row in rows
                if max(item.effective_at_utc for item in row.values()) == timestamp
            )
            batch = tuple(
                sorted(
                    batch,
                    key=lambda row: (
                        _i(_metadata(row["R187"]).get("ingestion_sequence", 0)),
                        row["R187"].occurrence_id,
                    ),
                )
            )
            for row in batch:
                operation = str(row["R187"].value).lower()
                side = str(row["R188"].value).lower()
                price = _d(row["R189"].value)
                size = _d(row["R190"].value)
                if side not in {"bid", "ask"} or price <= 0 or size < 0:
                    return None
                key = (side, price)
                if operation == "insert":
                    if key in state or size <= 0:
                        return None
                    state[key] = size
                elif operation == "update":
                    if key not in state or size <= 0:
                        return None
                    state[key] = size
                elif operation in {"delete", "remove", "cancel"}:
                    if key not in state:
                        return None
                    del state[key]
                else:
                    return None
            bids = tuple((p, q) for (s, p), q in state.items() if s == "bid")
            asks = tuple((p, q) for (s, p), q in state.items() if s == "ask")
            if not bids or not asks:
                predecessor = None
                continue
            pb, qb = max(bids)
            pa, qa = min(asks)
            if pb >= pa:
                return None
            current = (pb, qb, pa, qa)
            if predecessor is not None and timestamp >= start:
                pb0, qb0, pa0, qa0 = predecessor
                total += (
                    (qb if pb >= pb0 else _DEC0)
                    - (qb0 if pb <= pb0 else _DEC0)
                    - (qa if pa <= pa0 else _DEC0)
                    + (qa0 if pa >= pa0 else _DEC0)
                )
                transitions += 1
            predecessor = current
        return total if transitions > 0 else None
    except (ValueError, TypeError, KeyError, ArithmeticError, OverflowError):
        return None


def evaluate_stage1_kernel(
    derived_signal_id: str,
    *,
    raw_inputs: dict[str, tuple[KernelValueV1, ...]],
    derived_inputs: dict[str, tuple[KernelValueV1, ...]],
    parameter_set: api.CalculationParameterSetV1,
    contexts: tuple[object, ...],
    as_of_utc: datetime,
    knowledge_cutoff_utc: datetime,
) -> KernelResultV1 | None:
    try:
        row = catalogue_row(derived_signal_id)
    except KeyError:
        return None
    if (
        row.kernel_id not in STAGE1_KERNEL_IDS
        or parameter_set.profile not in row.parameter_profiles
    ):
        return None
    if derived_signal_id == "D123" and any(raw_inputs.values()):
        pair = select_d123_official_period_pair(
            raw_inputs, as_of_utc=as_of_utc, knowledge_cutoff_utc=knowledge_cutoff_utc
        )
        if pair is None:
            return None
        raw_inputs = {pair[0]: pair[1]}
    if derived_signal_id == "D186":
        selection = _d186_selected_states(derived_inputs, contexts, as_of_utc, knowledge_cutoff_utc)
        if selection is None:
            return None
        derived_inputs = {"D155": selection}
    params = _parameter_map(parameter_set)
    value: object | None
    if row.kernel_id == "K01_TIME":
        value = _eval_k01(
            derived_signal_id, raw_inputs, derived_inputs, params, as_of_utc, knowledge_cutoff_utc
        )
    elif row.kernel_id == "K02_ALGEBRA":
        value = _eval_k02(derived_signal_id, raw_inputs, derived_inputs, params, contexts)
    elif row.kernel_id == "K03_CHANGE_RETURN":
        value = _eval_k03(derived_signal_id, raw_inputs, derived_inputs, params, as_of_utc)
    elif row.kernel_id == "K04_STANDARDISE_RANK":
        value = _eval_k04(derived_signal_id, raw_inputs, params)
    elif row.kernel_id == "K05_REALIZED_RISK":
        value = _eval_k05(derived_signal_id, raw_inputs, params)
    elif row.kernel_id == "K06_REGRESSION_DEPENDENCE":
        value = _eval_k06(derived_signal_id, raw_inputs, derived_inputs, params)
    elif row.kernel_id == "K07_WEIGHTED_SCORE":
        value = _eval_k07(derived_signal_id, raw_inputs, derived_inputs, parameter_set, contexts)
    elif row.kernel_id == "K08_RULE_BUCKET_POLICY":
        value = _eval_k08(
            derived_signal_id, raw_inputs, derived_inputs, params, contexts,
            as_of_utc, knowledge_cutoff_utc
        )
    elif row.kernel_id == "K16_STRUCTURED_ASSEMBLY":
        value = _eval_k16(derived_signal_id, derived_inputs, params)
    elif row.kernel_id == "K17_ORDER_FLOW_IMBALANCE":
        value = _eval_k17(raw_inputs, params, as_of_utc)
    else:
        value = None
    if value is not None and derived_signal_id == "D104" and any(derived_inputs.values()):
        # Only the four actually used skew occurrences belong in the kernel
        # provenance, not any older records retained in a historical view.
        seconds = _i(params.get("anchor_seconds", 0))
        selected_skews: dict[str, tuple[KernelValueV1, ...]] = {}
        if seconds <= 0:
            return None
        for skew_id in ("D099", "D100"):
            skew_selected_pair = _history_anchor(
                derived_inputs.get(skew_id, ()), as_of=as_of_utc, seconds=seconds
            )
            if skew_selected_pair is None:
                return None
            selected_skews[skew_id] = skew_selected_pair
        derived_inputs = selected_skews
    return None if value is None else _result(derived_signal_id, value, raw_inputs, derived_inputs)


__all__ = [
    "STAGE1_KERNEL_IDS",
    "BookEventV1",
    "BookMutationV1",
    "KernelResultV1",
    "KernelValueV1",
    "evaluate_stage1_kernel",
    "extract_scalar",
    "occurrence_identity",
    "reconstruct_book",
    "select_eligible_values",
    "supported_stage1_ids",
]
