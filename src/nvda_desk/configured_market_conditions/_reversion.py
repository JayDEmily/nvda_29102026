"""D041's own exact controlled reversion profile; D040 calculation stays unchanged."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from itertools import pairwise
from typing import cast

from nvda_desk.market_measurement_truth import api as f

from . import _score
from . import api as c
from ._codec import canonical
from ._store import RecordState

BRIEF = "b9699956358b59300cac8927a3b209e4c295828084273fe7cdb6b11e3016917a"
PROFILE_BYTES = """{
  "signal": "D041",
  "definition": "D041-REVERSION-CONDITIONS-1",
  "profile_id": "p02-d041-controlled/1",
  "kernel": "K07_WEIGHTED_SCORE",
  "units": "score",
  "output": "exact_ratio",
  "intercept": [
    2,
    3
  ],
  "features": [
    {
      "signal": "D026",
      "path": "percent_difference",
      "units": "percent",
      "transform": "bounded_ratio",
      "scale": [
        1,
        1
      ],
      "clip": [
        0,
        1
      ],
      "orientation": 1,
      "weight": [
        1,
        3
      ]
    },
    {
      "signal": "D026",
      "path": "percent_difference",
      "units": "percent",
      "transform": "bounded_ratio",
      "scale": [
        1,
        1
      ],
      "clip": [
        -1,
        0
      ],
      "orientation": -1,
      "weight": [
        1,
        3
      ]
    },
    {
      "signal": "D040",
      "path": "result",
      "units": "score",
      "transform": "identity",
      "scale": [
        1,
        1
      ],
      "clip": [
        0,
        1
      ],
      "orientation": -1,
      "weight": [
        1,
        3
      ]
    },
    {
      "signal": "D033",
      "path": "result",
      "units": "annualised_volatility",
      "transform": "bounded_ratio",
      "scale": [
        1,
        1
      ],
      "clip": [
        0,
        1
      ],
      "orientation": -1,
      "weight": [
        1,
        3
      ]
    }
  ],
  "dependencies": [
    {
      "signal": "D026",
      "owner": "M02",
      "brief": "a2f3fc76cd2cc846fd4885d4f3d3df7a1a3e5c7370700a613ecb0706c853412f",
      "definition": "D026-VWAP-DEVIATION-1",
      "parameter": "mmt-vwap-deviation/1",
      "context": "controlled-price-session/1",
      "window": 2400
    },
    {
      "signal": "D040",
      "owner": "M03",
      "brief": "ce8a16e3f5c5f886b1847ce09be321477259577560e3543b4b18853b59ad3492",
      "definition": "D040-TREND-INTENSITY-1",
      "parameter": "p02-d040-controlled/1",
      "context": "p02-d040-controlled/1",
      "window": 1800
    },
    {
      "signal": "D033",
      "owner": "M02",
      "brief": "302845c64e6c2b9098e7f6806b41356a269ce1e79f14c026cfb85760d70c18cd",
      "definition": "D033-REALISED-VOL-1",
      "parameter": "mmt-realised-vol-30m-50d/1",
      "context": "controlled-risk-calendar/1",
      "window": 1800
    }
  ]
}
"""
PROFILE = c.profile_from_document(json.loads(PROFILE_BYTES))
PROFILE_HASH = hashlib.sha256(PROFILE_BYTES.encode()).hexdigest()
T = _score.T
SAMPLES = tuple(T - timedelta(minutes=30 - i) for i in range(31))
RISK_CONTEXT = f.RealisedRiskWindowContextV1(
    f.VersionRefV1("controlled-risk-calendar", 1),
    SAMPLES[0],
    SAMPLES[-1],
    datetime(2026, 10, 10, 12, tzinfo=UTC),
    tuple(
        f.SessionFrameV1(
            f.VersionRefV1("controlled-risk-" + day.strftime("%Y%m%d"), 1),
            "controlled_cash",
            day,
            day + timedelta(hours=1),
        )
        for day in (datetime(2026, 10, 10, 12, tzinfo=UTC) + timedelta(days=i) for i in range(11))
    ),
    SAMPLES,
    tuple(
        f.TradingReturnIntervalV1(a, b, f.ExactRatioV1(1, 15120))
        for a, b in pairwise(SAMPLES)
    ),
)
PRICE_CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-price-session", 1),
    T.replace(minute=0),
    T.replace(hour=13, minute=0),
    T.replace(minute=0),
)


def _request(request: c.ScoreRequestV1, now: datetime) -> None:
    if type(request) is not c.ScoreRequestV1:
        raise TypeError("exact score request required")
    c.utc(now)
    c._Record.__post_init__(request)
    if (
        request.signal != "D041"
        or request.profile_id != PROFILE.profile_id
        or request.subject != "NVDA"
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc not in (T + timedelta(seconds=1), T + timedelta(seconds=2))
        or now < request.knowledge_cutoff_utc
        or len(request.predecessor_ids) != 3
        or len(set(request.predecessor_ids)) != 3
        or any(not i for i in request.predecessor_ids)
    ):
        raise ValueError("unadmitted D041 request")


def _foundation(
    p: f.WindowMeasurementOccurrenceV1,
    dep: c.DependencyV1,
    request: c.ScoreRequestV1,
    now: datetime,
) -> None:
    pc = p.request.calculation
    expected = {
        "D026": (
            "price / percent",
            "named_exact_vwap_deviation",
            f.VwapDeviationV1,
            "mmt-vwap-deviation-selection",
            PRICE_CONTEXT,
        ),
        "D033": (
            "annualised_volatility",
            "scalar_decimal",
            Decimal,
            "mmt-realised-vol-30m-selection",
            RISK_CONTEXT,
        ),
    }[dep.signal]
    units, shape, cls, selection, context = expected
    if (
        p.owner_object_id != dep.owner
        or p.owner_namespace != "neutral_market_measurement_truth/window/v1"
        or p.implementation_brief_sha256 != dep.brief
        or p.derived_signal_id != dep.signal
        or p.definition.derived_signal_id != dep.signal
        or pc.derived_signal_id != dep.signal
        or p.definition.calculation_definition_version != dep.definition
        or pc.calculation_definition_version != dep.definition
        or p.parameter_set.context_id + "/" + str(p.parameter_set.version) != dep.parameter
        or pc.parameter_set_ref
        != f.VersionRefV1(p.parameter_set.context_id, p.parameter_set.version)
        or p.parameter_set.subject_instrument != request.subject
        or p.parameter_set.members != (request.subject,)
        or p.request.context != context
        or pc.context_refs != (context.ref,)
        or context.ref.context_id + "/" + str(context.ref.version) != dep.context
        or p.window_seconds != dep.window
        or pc.subject_instrument != request.subject
        or pc.as_of_utc != request.as_of_utc
        or p.effective_as_of_utc != request.as_of_utc
        or pc.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or p.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or not p.knowledge_cutoff_utc <= p.calculated_at_utc <= now
        or p.units != units
        or p.definition.units != units
        or p.result_shape != shape
        or p.definition.result_shape != shape
        or type(p.result) is not cls
        or p.input_selection_policy.context_id != selection
        or p.input_selection_policy.version != 1
        or pc.input_selection_policy_ref != f.VersionRefV1(selection, 1)
        or not p.derived_occurrence_id.startswith("mmtwindow1:")
        or not p.raw_input_lineage
    ):
        raise ValueError("incompatible D041 foundation predecessor")


def _trend(
    p: c.ScoreOccurrenceV1, dep: c.DependencyV1, request: c.ScoreRequestV1, now: datetime
) -> None:
    _score.validate(p)
    if (
        p.owner_object_id != dep.owner
        or p.owner_namespace != _score.NAMESPACE
        or p.implementation_brief_sha256 != dep.brief
        or p.derived_signal_id != dep.signal
        or p.profile.definition != dep.definition
        or p.profile.profile_id != dep.parameter
        or p.request.profile_id != dep.context
        or max(
            x.window_seconds for x in p.predecessors if type(x) is f.WindowMeasurementOccurrenceV1
        )
        != dep.window
        or p.request.subject != request.subject
        or p.effective_as_of_utc != request.as_of_utc
        or p.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or p.calculated_at_utc > now
        or not 0 <= _score.ratio(p.result) <= 1
    ):
        raise ValueError("incompatible actual D040 snapshot")


def produce(
    request: c.ScoreRequestV1,
    predecessors: tuple[f.WindowMeasurementOccurrenceV1 | c.ScoreOccurrenceV1, ...],
    now: datetime,
) -> c.ScoreOccurrenceV1:
    _request(request, now)
    if (
        len(predecessors) != 3
        or tuple(p.derived_occurrence_id for p in predecessors) != request.predecessor_ids
        or type(predecessors[0]) is not f.WindowMeasurementOccurrenceV1
        or type(predecessors[1]) is not c.ScoreOccurrenceV1
        or type(predecessors[2]) is not f.WindowMeasurementOccurrenceV1
    ):
        raise ValueError("three actual ordered typed predecessors required")
    for i in (0, 2):
        _foundation(
            cast(f.WindowMeasurementOccurrenceV1, predecessors[i]),
            PROFILE.dependencies[i],
            request,
            now,
        )
    _trend(cast(c.ScoreOccurrenceV1, predecessors[1]), PROFILE.dependencies[1], request, now)
    by_signal = {p.derived_signal_id: p for p in predecessors}
    evidence = []
    total = _score.ratio(PROFILE.intercept)
    for feature in PROFILE.features:
        p = by_signal[feature.signal]
        raw = p.result if feature.path == "result" else getattr(p.result, feature.path)
        x = (
            Fraction(raw)
            if type(raw) is Decimal and raw.is_finite()
            else _score.ratio(cast(f.ExactRatioV1, raw))
        )
        if feature.signal == "D033" and x < 0:
            raise ValueError("nonnegative annualised volatility required")
        scale = _score.ratio(feature.scale)
        if scale <= 0 or _score.ratio(feature.weight) < 0 or feature.orientation not in (-1, 1):
            raise ValueError("invalid immutable coefficient")
        z = x if feature.transform == "identity" else x / (scale + abs(x))
        if feature.transform not in ("identity", "bounded_ratio"):
            raise ValueError("unsupported transform")
        z = min(max(z, Fraction(feature.clip[0])), Fraction(feature.clip[1]))
        oriented = z * feature.orientation
        weighted = oriented * _score.ratio(feature.weight)
        evidence.append(
            c.FeatureEvidenceV1(
                feature,
                p.derived_occurrence_id,
                _score.carrier(x),
                _score.carrier(z),
                _score.carrier(oriented),
                _score.carrier(weighted),
            )
        )
        total += weighted
    if not 0 <= total <= 1:
        raise ValueError("controlled reversion range violated")
    value = c.ScoreOccurrenceV1(
        "M03",
        _score.NAMESPACE,
        BRIEF,
        "D041",
        "pending",
        request,
        PROFILE,
        PROFILE_HASH,
        predecessors,
        tuple(evidence),
        _score.carrier(total),
        "score",
        "exact_ratio",
        request.as_of_utc,
        request.knowledge_cutoff_utc,
        now,
    )
    identity = (
        "cmcscore1:"
        + hashlib.sha256(
            canonical(
                replace(
                    value,
                    derived_occurrence_id="pending",
                    calculated_at_utc=request.knowledge_cutoff_utc,
                )
            )
        ).hexdigest()
    )
    return replace(value, derived_occurrence_id=identity)


def validate(value: c.ScoreOccurrenceV1) -> None:
    if type(value) is not c.ScoreOccurrenceV1:
        raise TypeError("exact score occurrence required")
    c._Record.__post_init__(value)
    if canonical(value) != canonical(
        produce(
            value.request,
            value.predecessors,
            value.calculated_at_utc,
        )
    ):
        raise ValueError("D041 metadata/result/lineage/identity mismatch")


class _Reads(_score._Reads):
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[c.ScoreOccurrenceV1, ...]:
        c.utc(effective_at_or_before_utc)
        c.utc(knowledge_at_or_before_utc)
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("bounded exact history limit required")
        if type(derived_signal_id) is not str or type(subject_instrument) is not str:
            raise TypeError("exact history identifiers required")
        if derived_signal_id != "D041" or subject_instrument != "NVDA":
            raise ValueError("admitted signal/subject required")
        return tuple(
            sorted(
                (
                    v
                    for v in self.state.all()
                    if v.derived_signal_id == derived_signal_id
                    and v.request.subject == subject_instrument
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
        foundation: f.MeasurementWindowReadsV1,
        scores: c.ScoreReadsV1,
        now: Callable[[], datetime],
    ) -> None:
        self.state, self.foundation, self.scores, self.now = state, foundation, scores, now
        self.reads = _Reads(state)

    def materialise(self, request: c.ScoreRequestV1) -> c.ScoreOccurrenceV1 | None:
        now = self.now()
        c.utc(now)
        try:
            _request(request, now)
            facts = (
                self.foundation.get_derived_occurrence(request.predecessor_ids[0]),
                self.scores.get_derived_occurrence(request.predecessor_ids[1]),
                self.foundation.get_derived_occurrence(request.predecessor_ids[2]),
            )
            if any(p is None for p in facts):
                return None
            value = produce(
                request,
                cast(tuple[f.WindowMeasurementOccurrenceV1 | c.ScoreOccurrenceV1, ...], facts),
                now,
            )
        except (TypeError, ValueError, ArithmeticError, AttributeError, KeyError):
            return None
        return cast(c.ScoreOccurrenceV1, self.state.append(value))


def _admission(admission: f.OwnerAdmissionV1) -> None:
    if type(admission) is not f.OwnerAdmissionV1 or admission != f.OwnerAdmissionV1("M03", BRIEF):
        raise ValueError("exact D041 owning authority required")


def build_owner(
    admission: f.OwnerAdmissionV1,
    foundation: f.MeasurementWindowReadsV1,
    scores: c.ScoreReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> c.ScoreOwnerV1:
    _admission(admission)
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    if any(
        not callable(getattr(rd, "get_derived_occurrence", None)) for rd in (foundation, scores)
    ):
        raise TypeError("actual foundation and score reader facets required")
    return _Owner(RecordState(storage, _score._decode, validate), foundation, scores, now)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1) -> c.ScoreReadsV1:
    _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only storage required")
    return _Reads(RecordState(storage, _score._decode, validate))
