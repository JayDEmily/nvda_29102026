"""Underlying aligned histories and the bounded D076 relative route."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from typing import cast

from . import _aligned_history_codec as codec
from . import _aligned_history_source as source
from . import _log_return
from . import api as f
from ._record_store import RecordState

NAMESPACE = "neutral_market_measurement_truth/aligned_history/v1"


def _request_frame(
    authority: source.Authority, request: f.AlignedHistoryRequestV1, now: datetime,
) -> source.Frame:
    if type(request) is not f.AlignedHistoryRequestV1:
        raise TypeError("exact aligned history request required")
    f._Validated.__post_init__(request)
    f._utc(now)
    cfg = authority.config
    frame = authority.frames.get(request.slot)
    if frame is None:
        raise ValueError("unadmitted aligned history slot")
    expected = f.AlignedHistoryRequestV1(
        cfg.signal, cfg.subject, frame.slot, frame.as_of, frame.cutoff,
        cfg.definition.calculation_definition_version, cfg.profile,
        f.VersionRefV1(cfg.parameter.context_id, cfg.parameter.version),
        f.VersionRefV1(cfg.selection.context_id, cfg.selection.version),
        (frame.context.ref,), (),
    )
    if request != expected or now < frame.cutoff:
        raise ValueError("unadmitted request, metadata, or calculation clock")
    return frame


def _produce(
    authority: source.Authority, request: f.AlignedHistoryRequestV1,
    pairs: tuple[source.Pair, ...], now: datetime,
) -> f.AlignedHistoryOccurrenceV1:
    frame = _request_frame(authority, request, now)
    cfg = authority.config
    if (
        len(pairs) != 2
        or pairs[0][0].observation_occurrence_id == pairs[1][0].observation_occurrence_id
    ):
        raise ValueError("two distinct ordered original facts required")
    prices: list[Decimal] = []
    for pair, mapping in zip(pairs, source.MAPS, strict=True):
        price = source.role_price(pair, frame, cfg.subject, mapping)
        if price is None:
            raise ValueError("selected original is ineligible for its role")
        prices.append(price)
    keys = tuple((frame.slot, cfg.subject, role) for role in source.ROLES)
    authority.check_corpus(
        keys, tuple((key, pair[0]) for key, pair in zip(keys, pairs, strict=True)),
    )
    result = _log_return._logarithm(prices[0], prices[1])
    value = f.AlignedHistoryOccurrenceV1(
        "M02", NAMESPACE, cfg.brief, cfg.signal, "pending", request, cfg.definition,
        source.POLICY_SHA, cfg.profile, cfg.parameter, cfg.selection, frame.context,
        source.MAPS, (source.UNIT,), tuple(pair[0] for pair in pairs),
        tuple(pair[1] for pair in pairs), (), result, "return", "scalar_decimal",
        frame.seconds, frame.as_of, frame.cutoff, now,
    )
    return replace(value, derived_occurrence_id=codec.identity(value))


def _store(
    authority: source.Authority, storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1,
) -> RecordState:
    def validate(value: f.AlignedHistoryOccurrenceV1) -> None:
        if type(value) is not f.AlignedHistoryOccurrenceV1:
            raise TypeError("exact aligned history occurrence required")
        f._Validated.__post_init__(value)
        expected = _produce(
            authority, value.request,
            tuple(zip(value.original_observations, value.selected_projections, strict=True)),
            value.calculated_at_utc,
        )
        if codec.encode(value) != codec.encode(expected):
            raise ValueError("aligned history semantic, metadata or identity mismatch")

    return RecordState(storage, codec.decode, validate, encode=codec.encode)


class _Reads:
    def __init__(self, authority: source.Authority, state: RecordState) -> None:
        self._authority, self._state = authority, state

    def get_derived_occurrence(
        self, derived_occurrence_id: str,
    ) -> f.AlignedHistoryOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty aligned history occurrence identity required")
        rows = cast(tuple[f.AlignedHistoryOccurrenceV1, ...], self._state.all())
        return next(
            (row for row in rows if row.derived_occurrence_id == derived_occurrence_id), None,
        )

    def list_derived_history(
        self, *, derived_signal_id: str, subject_instrument: str,
        effective_at_or_before_utc: datetime, knowledge_at_or_before_utc: datetime, limit: int,
    ) -> tuple[f.AlignedHistoryOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        cfg = self._authority.config
        if (
            derived_signal_id != cfg.signal or subject_instrument != cfg.subject
            or type(limit) is not int or not 1 <= limit <= 1000
        ):
            raise ValueError("bounded own-jurisdiction history required")
        rows = (
            row for row in cast(tuple[f.AlignedHistoryOccurrenceV1, ...], self._state.all())
            if row.effective_as_of_utc <= effective_at_or_before_utc
            and row.knowledge_cutoff_utc <= knowledge_at_or_before_utc
        )
        return tuple(sorted(rows, key=lambda row: (
            row.effective_as_of_utc, row.knowledge_cutoff_utc, row.derived_occurrence_id,
        ), reverse=True))[:limit]


class _Owner:
    def __init__(
        self, authority: source.Authority, sealed: f.AlignedHistorySourceV1,
        state: RecordState, utc_now: Callable[[], datetime],
    ) -> None:
        self._authority, self._source, self._state = authority, sealed, state
        self._utc_now = utc_now
        self.reads = _Reads(authority, state)

    def materialise(
        self, request: f.AlignedHistoryRequestV1,
    ) -> f.AlignedHistoryOccurrenceV1 | None:
        if type(request) is not f.AlignedHistoryRequestV1:
            raise TypeError("exact aligned history request required")
        now = self._utc_now()
        f._utc(now)
        try:
            frame = _request_frame(self._authority, request, now)
            pairs = tuple(
                source.select_role(self._source, frame, self._authority.config.subject, mapping)
                for mapping in source.MAPS
            )
            value = _produce(self._authority, request, pairs, now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        # Persistence failures remain technical failures, never business refusals.
        return cast(f.AlignedHistoryOccurrenceV1, self._state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1, sealed: f.AlignedHistorySourceV1 | None,
    predecessor_read_storages: tuple[f.SQLiteReadStorageV1, ...],
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.AlignedHistoryOwnerV1:
    authority = source.Authority(admission)
    if authority.config.signal == "D076":
        return _build_relative_owner(authority, sealed, predecessor_read_storages, storage, utc_now)
    if (
        type(sealed) is not f.AlignedHistorySourceV1 or not sealed._matches_admission(admission)
        or type(predecessor_read_storages) is not tuple or predecessor_read_storages
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("exact sealed source and fresh owner-local SQLite storage required")
    return _Owner(authority, sealed, _store(authority, storage), utc_now)


def build_reader(
    admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1,
) -> f.AlignedHistoryReadsV1:
    authority = source.Authority(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only SQLite storage required")
    if authority.config.signal == "D076":
        return _Reads(authority, _relative_store(authority, _parent_authorities(), storage))
    return _Reads(authority, _store(authority, storage))


def _parent_admissions() -> tuple[f.OwnerAdmissionV1, ...]:
    return tuple(f.OwnerAdmissionV1("M02", source.BRIEFS[signal]) for signal in source.D076_PARENTS)


def _parent_authorities() -> tuple[source.Authority, ...]:
    return tuple(source.Authority(admission) for admission in _parent_admissions())


def _relative_frame(
    authority: source.Authority, request: f.AlignedHistoryRequestV1, now: datetime,
) -> source.Frame:
    if type(request) is not f.AlignedHistoryRequestV1:
        raise TypeError("exact aligned history request required")
    f._Validated.__post_init__(request)
    f._utc(now)
    cfg = authority.config
    frame = authority.frames.get(request.slot)
    ids = request.predecessor_occurrence_ids
    if frame is None or len(ids) != len(source.D076_PARENTS) or len(set(ids)) != len(ids):
        raise ValueError("D076 exact slot and distinct ordered parent IDs required")
    expected = f.AlignedHistoryRequestV1(
        cfg.signal, cfg.subject, frame.slot, frame.as_of, frame.cutoff,
        cfg.definition.calculation_definition_version, cfg.profile,
        f.VersionRefV1(cfg.parameter.context_id, cfg.parameter.version),
        f.VersionRefV1(cfg.selection.context_id, cfg.selection.version),
        (frame.context.ref,), ids,
    )
    if request != expected or now < frame.cutoff:
        raise ValueError("unadmitted relative request, metadata or calculation clock")
    return frame


def _relative_produce(
    authority: source.Authority, parent_authorities: tuple[source.Authority, ...],
    request: f.AlignedHistoryRequestV1, parents: tuple[f.AlignedHistoryOccurrenceV1, ...],
    now: datetime,
) -> f.AlignedHistoryOccurrenceV1:
    frame = _relative_frame(authority, request, now)
    cfg = authority.config
    if (
        tuple(a.config.signal for a in parent_authorities) != source.D076_PARENTS
        or len(parents) != len(parent_authorities)
        or any(type(parent) is not f.AlignedHistoryOccurrenceV1 for parent in parents)
        or tuple(p.derived_occurrence_id for p in parents) != request.predecessor_occurrence_ids
    ):
        raise ValueError("D076 exact ordered parent identities required")
    keys: list[source.Key] = []
    actual: list[tuple[source.Key, source.raw.RawObservationOccurrenceV1]] = []
    values: list[Fraction] = []
    for parent, parent_authority in zip(parents, parent_authorities, strict=True):
        # The same underlying producer validates every retained typed original,
        # projection, profile, frame, calculation, metadata and complete identity.
        f._Validated.__post_init__(parent)
        expected = _produce(
            parent_authority, parent.request,
            tuple(zip(parent.original_observations, parent.selected_projections, strict=True)),
            parent.calculated_at_utc,
        )
        if codec.encode(parent) != codec.encode(expected):
            raise ValueError("relative parent semantic, identity or metadata mismatch")
        if (
            parent.request.slot != frame.slot or parent.effective_as_of_utc != frame.as_of
            or parent.knowledge_cutoff_utc != frame.cutoff
            or parent.window_context != frame.context or parent.window_seconds != frame.seconds
        ):
            raise ValueError("relative parent frame alignment mismatch")
        if parent.knowledge_cutoff_utc > now or parent.calculated_at_utc > now:
            raise ValueError("relative parent unavailable at decision ceiling")
        if type(parent.result) is not Decimal:
            raise ValueError("exact canonical Decimal parent return required")
        values.append(Fraction(parent.result))
        for role, original in zip(source.ROLES, parent.original_observations, strict=True):
            key = (frame.slot, parent_authority.config.subject, role)
            keys.append(key)
            actual.append((key, original))
    if len({item[1].observation_occurrence_id for item in actual}) != len(actual):
        raise ValueError("distinct selected originals required across relative roles")
    # One whole-union predicate after complete actual parent validation, in both
    # live production and ordinary durable read-only reconstruction.
    authority.check_corpus(tuple(keys), tuple(actual))
    ratio = values[0] - values[1]
    value = f.AlignedHistoryOccurrenceV1(
        "M02", NAMESPACE, cfg.brief, cfg.signal, "pending", request, cfg.definition,
        source.POLICY_SHA, cfg.profile, cfg.parameter, cfg.selection, frame.context,
        (), (), (), (), parents, f.ExactRatioV1(ratio.numerator, ratio.denominator),
        cfg.definition.units, cfg.definition.result_shape, frame.seconds, frame.as_of,
        frame.cutoff, now,
    )
    return replace(value, derived_occurrence_id=codec.identity(value))


def _relative_store(
    authority: source.Authority, parent_authorities: tuple[source.Authority, ...],
    storage: f.SQLiteStorageV1 | f.SQLiteReadStorageV1,
) -> RecordState:
    def validate(value: f.AlignedHistoryOccurrenceV1) -> None:
        if type(value) is not f.AlignedHistoryOccurrenceV1:
            raise TypeError("exact relative history occurrence required")
        f._Validated.__post_init__(value)
        expected = _relative_produce(
            authority, parent_authorities, value.request, value.predecessors, value.calculated_at_utc,
        )
        if codec.encode(value) != codec.encode(expected):
            raise ValueError("relative history semantic, metadata or identity mismatch")

    return RecordState(storage, codec.decode, validate, encode=codec.encode)


class _RelativeOwner:
    def __init__(
        self, authority: source.Authority, parent_authorities: tuple[source.Authority, ...],
        readers: tuple[f.AlignedHistoryReadsV1, ...], state: RecordState,
        utc_now: Callable[[], datetime],
    ) -> None:
        self._authority, self._parent_authorities = authority, parent_authorities
        self._readers, self._state, self._utc_now = readers, state, utc_now
        self.reads = _Reads(authority, state)

    def materialise(
        self, request: f.AlignedHistoryRequestV1,
    ) -> f.AlignedHistoryOccurrenceV1 | None:
        if type(request) is not f.AlignedHistoryRequestV1:
            raise TypeError("exact aligned history request required")
        now = self._utc_now()
        f._utc(now)
        try:
            _relative_frame(self._authority, request, now)
            parents = []
            for reader, identity in zip(self._readers, request.predecessor_occurrence_ids, strict=True):
                parent = reader.get_derived_occurrence(identity)
                if type(parent) is not f.AlignedHistoryOccurrenceV1:
                    raise ValueError("actual relative parent not found")
                parents.append(parent)
            value = _relative_produce(
                self._authority, self._parent_authorities, request, tuple(parents), now,
            )
        except (TypeError, ValueError, ArithmeticError):
            return None
        # Persistence failures (including from actual parent reads) are technical.
        return cast(f.AlignedHistoryOccurrenceV1, self._state.append(value))


def _build_relative_owner(
    authority: source.Authority, sealed: f.AlignedHistorySourceV1 | None,
    predecessor_read_storages: tuple[f.SQLiteReadStorageV1, ...],
    storage: f.SQLiteStorageV1, utc_now: Callable[[], datetime],
) -> f.AlignedHistoryOwnerV1:
    if (
        sealed is not None or type(predecessor_read_storages) is not tuple
        or len(predecessor_read_storages) != len(source.D076_PARENTS)
        or any(type(s) is not f.SQLiteReadStorageV1 for s in predecessor_read_storages)
        or len({s.database_path for s in predecessor_read_storages}) != len(source.D076_PARENTS)
        or type(storage) is not f.SQLiteStorageV1 or storage.create is not True
        or not callable(utc_now)
    ):
        raise ValueError("D076 requires ordered concrete parent reads and fresh own SQLite storage")
    readers = tuple(
        f.create_aligned_history_reader(admission=admission, storage=parent_storage)
        for admission, parent_storage in zip(_parent_admissions(), predecessor_read_storages, strict=True)
    )
    parent_authorities = _parent_authorities()
    return _RelativeOwner(
        authority, parent_authorities, readers,
        _relative_store(authority, parent_authorities, storage), utc_now,
    )
