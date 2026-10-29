"""D136 exact imbalance from two actual, same-book public SMART depths."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import fields, replace
from datetime import datetime
from fractions import Fraction
from typing import cast

from . import _smart_ask, _smart_depth
from . import api as f
from ._catalogue import _AUTHORITY
from ._evaluation import canonical, decode
from ._record_store import RecordState

BRIEF = "0e8b8a7152e1a92c6aaafcacd8f6df5133ad3ce242ba0a905e2ad1194e2cfa57"
NAMESPACE = "neutral_market_measurement_truth/smart-imbalance/v1"
DEFINITION = f.CalculationDefinitionV1(
    "D136", "D136-SMART-DEPTH-IMBALANCE-1", "K02_ALGEBRA",
    "(bid_depth-ask_depth)/(bid_depth+ask_depth)", (), ("D134", "D135"),
    "P_BASIC", "-1_to_1", "exact_ratio",
    tuple(f.AuthorityArtifactRefV1(*item) for item in _AUTHORITY),
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d136-same-book-top-levels", 1, "P_BASIC", _smart_depth.SUBJECT,
    (_smart_depth.SUBJECT,),
)
SELECTION = f.VersionRefV1("mmt-d136-same-book-selection", 1)


def request(bid_id: str, ask_id: str) -> f.SmartImbalanceRequestV1:
    return f.SmartImbalanceRequestV1(
        f.CalculationRequestV1(
            "D136", _smart_depth.SUBJECT, _smart_depth.T, _smart_depth.CUTOFF,
            DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), SELECTION, (SELECTION,), (),
        ), (bid_id, ask_id), f.SmartDepthPairV1(2, 2),
    )


def _request(req: f.SmartImbalanceRequestV1, now: datetime) -> None:
    f._utc(now)
    if (type(req) is not f.SmartImbalanceRequestV1
        or any(type(item) is not str or not item for item in req.predecessor_occurrence_ids)
        or req.predecessor_occurrence_ids[0] == req.predecessor_occurrence_ids[1]
        or canonical(req) != canonical(request(*req.predecessor_occurrence_ids))
        or now < _smart_depth.CUTOFF):
        raise ValueError("unadmitted D136 selection or predecessor IDs")


def _produce(req: f.SmartImbalanceRequestV1,
             parents: tuple[f.SmartDepthOccurrenceV1, f.SmartDepthOccurrenceV1],
             now: datetime) -> f.SmartImbalanceOccurrenceV1:
    _request(req, now)
    bid, ask = parents
    _smart_depth._validate(bid)
    _smart_ask._validate(ask)
    if (bid.derived_occurrence_id != req.predecessor_occurrence_ids[0]
        or ask.derived_occurrence_id != req.predecessor_occurrence_ids[1]
        or bid.derived_signal_id != "D134" or ask.derived_signal_id != "D135"
        or bid.implementation_brief_sha256 != _smart_depth.BRIEF
        or ask.implementation_brief_sha256 != _smart_ask.BRIEF
        or bid.request.calculation.subject_instrument != _smart_depth.SUBJECT
        or ask.request.calculation.subject_instrument != _smart_depth.SUBJECT
        or bid.request.calculation.as_of_utc != ask.request.calculation.as_of_utc
        or bid.request.calculation.knowledge_cutoff_utc
        != ask.request.calculation.knowledge_cutoff_utc
        or bid.request.selection.provider != ask.request.selection.provider
        or bid.request.selection.variant != ask.request.selection.variant
        or bid.request.selection.generation != ask.request.selection.generation
        or bid.request.selection.history_complete_from_utc
        != ask.request.selection.history_complete_from_utc
        or bid.projection_mappings != ask.projection_mappings
        or bid.unit_conventions != ask.unit_conventions
        or bid.raw_input_lineage != ask.raw_input_lineage
        or bid.standing_rows != ask.standing_rows
        or bid.request.depth_levels != req.requested_depth_levels.bid_levels
        or ask.request.depth_levels != req.requested_depth_levels.ask_levels
        or (bid.request.depth_levels == ask.request.depth_levels
            and bid.request.selection != ask.request.selection)
        or bid.effective_as_of_utc != _smart_depth.T
        or ask.effective_as_of_utc != _smart_depth.T
        or bid.knowledge_cutoff_utc != _smart_depth.CUTOFF
        or ask.knowledge_cutoff_utc != _smart_depth.CUTOFF
        or bid.calculated_at_utc > now or ask.calculated_at_utc > now):
        raise ValueError("actual depths differ in source/book/levels/time")
    b, a = Fraction(bid.result), Fraction(ask.result)
    if b < 0 or a < 0 or b + a == 0:
        raise ValueError("nonzero compatible displayed depth required")
    ratio = (b - a) / (b + a)
    value = f.SmartImbalanceOccurrenceV1(
        "M02", NAMESPACE, BRIEF, "D136", "pending", req, DEFINITION, PARAMETER,
        parents, f.ExactRatioV1(ratio.numerator, ratio.denominator), "-1_to_1",
        "exact_ratio", _smart_depth.T, _smart_depth.CUTOFF, now,
    )
    payload = {field.name: getattr(value, field.name) for field in fields(value)
               if field.name not in ("derived_occurrence_id", "calculated_at_utc")}
    return replace(value, derived_occurrence_id="mmtimbalance1:" +
                   hashlib.sha256(canonical(payload)).hexdigest())


def _validate(value: f.SmartImbalanceOccurrenceV1) -> None:
    if type(value) is not f.SmartImbalanceOccurrenceV1:
        raise TypeError("exact D136 occurrence required")
    f._Validated.__post_init__(value)
    if canonical(value) != canonical(_produce(value.request, value.predecessors,
                                              value.calculated_at_utc)):
        raise ValueError("D136 predecessors/result/identity mismatch")


def _decode(payload: bytes) -> f.SmartImbalanceOccurrenceV1:
    return cast(f.SmartImbalanceOccurrenceV1, decode(payload, f.SmartImbalanceOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str
                               ) -> f.SmartImbalanceOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str or not derived_occurrence_id:
            raise ValueError("nonempty imbalance occurrence identity required")
        return next((v for v in self.state.all()
                     if v.derived_occurrence_id == derived_occurrence_id), None)

    def list_derived_history(self, *, derived_signal_id: str, subject_instrument: str,
                             effective_at_or_before_utc: datetime,
                             knowledge_at_or_before_utc: datetime, limit: int
                             ) -> tuple[f.SmartImbalanceOccurrenceV1, ...]:
        f._utc(effective_at_or_before_utc)
        f._utc(knowledge_at_or_before_utc)
        if (type(limit) is not int or not 1 <= limit <= 1000
            or type(derived_signal_id) is not str or not derived_signal_id
            or type(subject_instrument) is not str or not subject_instrument):
            raise ValueError("invalid imbalance history query")
        return tuple(sorted((v for v in self.state.all()
                             if v.derived_signal_id == derived_signal_id
                             and v.request.calculation.subject_instrument == subject_instrument
                             and v.effective_as_of_utc <= effective_at_or_before_utc
                             and v.knowledge_cutoff_utc <= knowledge_at_or_before_utc),
                            key=lambda v: (v.effective_as_of_utc, v.knowledge_cutoff_utc,
                                           v.derived_occurrence_id), reverse=True)[:limit])


class _Owner:
    def __init__(self, state: RecordState, bid_reader: f.MeasurementSmartDepthReadsV1,
                 ask_reader: f.MeasurementSmartDepthReadsV1,
                 now: Callable[[], datetime]) -> None:
        self.state, self.bid_reader, self.ask_reader, self.now = (
            state, bid_reader, ask_reader, now
        )
        self.reads = _Reads(state)

    def materialise(self, req: f.SmartImbalanceRequestV1
                    ) -> f.SmartImbalanceOccurrenceV1 | None:
        now = self.now()
        f._utc(now)
        try:
            _request(req, now)
            bid = self.bid_reader.get_derived_occurrence(req.predecessor_occurrence_ids[0])
            ask = self.ask_reader.get_derived_occurrence(req.predecessor_occurrence_ids[1])
            if type(bid) is not f.SmartDepthOccurrenceV1 \
                    or type(ask) is not f.SmartDepthOccurrenceV1:
                return None
            value = _produce(req, (bid, ask), now)
        except (TypeError, ValueError, ArithmeticError):
            return None
        return cast(f.SmartImbalanceOccurrenceV1, self.state.append(value))


def build_owner(admission: f.OwnerAdmissionV1,
                bid_reader: f.MeasurementSmartDepthReadsV1,
                ask_reader: f.MeasurementSmartDepthReadsV1,
                storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
                now: Callable[[], datetime]) -> f.MeasurementSmartImbalanceOwnerV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF):
        raise ValueError("unadmitted D136 owner")
    if (type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now)
        or not callable(getattr(bid_reader, "get_derived_occurrence", None))
        or not callable(getattr(ask_reader, "get_derived_occurrence", None))):
        raise TypeError("actual public predecessor readers and storage/clock required")
    return _Owner(RecordState(storage, _decode, _validate), bid_reader, ask_reader, now)


def build_reader(admission: f.OwnerAdmissionV1,
                 storage: f.SQLiteReadStorageV1) -> f.MeasurementSmartImbalanceReadsV1:
    if admission != f.OwnerAdmissionV1("M02", BRIEF) or type(storage) is not f.SQLiteReadStorageV1:
        raise ValueError("unadmitted D136 reader")
    return _Reads(RecordState(storage, _decode, _validate))
