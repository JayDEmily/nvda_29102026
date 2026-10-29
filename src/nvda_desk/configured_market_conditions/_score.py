"""Fixed controlled K07 score law owned by P02's admitted runtime module."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from typing import cast

from nvda_desk.market_measurement_truth import api as f

from . import api as c
from ._codec import canonical, decode
from ._store import RecordState

NAMESPACE = "configured_market_conditions/score/v1"
BRIEFS = {"D040": "ce8a16e3f5c5f886b1847ce09be321477259577560e3543b4b18853b59ad3492"}
# Generated verbatim from the sole owning JSON; never reconstructed in companion docs.
PROFILE_BYTES = {
    "D040": """{
  "signal": "D040",
  "definition": "D040-TREND-INTENSITY-1",
  "profile_id": "p02-d040-controlled/1",
  "kernel": "K07_WEIGHTED_SCORE",
  "units": "score",
  "output": "exact_ratio",
  "intercept": [
    0,
    1
  ],
  "features": [
    {
      "signal": "D020",
      "path": "result",
      "units": "log_return",
      "transform": "bounded_ratio",
      "scale": [
        1,
        100
      ],
      "clip": [
        0,
        1
      ],
      "orientation": 1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D020",
      "path": "result",
      "units": "log_return",
      "transform": "bounded_ratio",
      "scale": [
        1,
        100
      ],
      "clip": [
        -1,
        0
      ],
      "orientation": -1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D021",
      "path": "result",
      "units": "log_return",
      "transform": "bounded_ratio",
      "scale": [
        3,
        100
      ],
      "clip": [
        0,
        1
      ],
      "orientation": 1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D021",
      "path": "result",
      "units": "log_return",
      "transform": "bounded_ratio",
      "scale": [
        3,
        100
      ],
      "clip": [
        -1,
        0
      ],
      "orientation": -1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D027",
      "path": "percent_per_minute",
      "units": "percent/minute",
      "transform": "bounded_ratio",
      "scale": [
        1,
        10
      ],
      "clip": [
        0,
        1
      ],
      "orientation": 1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D027",
      "path": "percent_per_minute",
      "units": "percent/minute",
      "transform": "bounded_ratio",
      "scale": [
        1,
        10
      ],
      "clip": [
        -1,
        0
      ],
      "orientation": -1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D024",
      "path": "accel_1v5",
      "units": "return/minute",
      "transform": "bounded_ratio",
      "scale": [
        1,
        1000
      ],
      "clip": [
        0,
        1
      ],
      "orientation": 1,
      "weight": [
        1,
        4
      ]
    },
    {
      "signal": "D024",
      "path": "accel_1v5",
      "units": "return/minute",
      "transform": "bounded_ratio",
      "scale": [
        1,
        1000
      ],
      "clip": [
        -1,
        0
      ],
      "orientation": -1,
      "weight": [
        1,
        4
      ]
    }
  ],
  "dependencies": [
    {
      "signal": "D020",
      "owner": "M02",
      "brief": "811906fdfb073da9b5a7ba137563953d6ff977d50bfe99b8f43adb068f20e839",
      "definition": "D020-LOG-RETURN-1",
      "parameter": "mmt-log-300s-50d-half-even/1",
      "context": "controlled-close-session/1",
      "window": 300
    },
    {
      "signal": "D021",
      "owner": "M02",
      "brief": "913ba660f583f8f3e564190390681e594a374e0fc2d66227bd8452b4d0cbb8cc",
      "definition": "D021-LOG-RETURN-1",
      "parameter": "mmt-log-1800s-50d-half-even/1",
      "context": "controlled-close-session/1",
      "window": 1800
    },
    {
      "signal": "D027",
      "owner": "M02",
      "brief": "6c4a8b6a4451ddfa6b555e9f1b02d659af269ec0788e8ebc15b8ddf9528796bf",
      "definition": "D027-VWAP-RATE-1",
      "parameter": "mmt-vwap-rate-300s/1",
      "context": "controlled-price-session/1",
      "window": 300
    },
    {
      "signal": "D024",
      "owner": "M02",
      "brief": "7776047c140ed8e6fa76af66a772b4a8ffbf1088ce4681377243ec666ddc9885",
      "definition": "D024-RETURN-ACCELERATION-1",
      "parameter": "mmt-return-acceleration/1",
      "context": "controlled-close-session/1",
      "window": 1800
    }
  ]
}
"""
}
PROFILES = {key: c.profile_from_document(json.loads(raw)) for key, raw in PROFILE_BYTES.items()}
T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)


def ratio(value: f.ExactRatioV1) -> Fraction:
    if type(value) is not f.ExactRatioV1:
        raise TypeError("exact rational required")
    return Fraction(value.numerator, value.denominator)


def carrier(value: Fraction) -> f.ExactRatioV1:
    return f.ExactRatioV1(value.numerator, value.denominator)


def request_check(request: c.ScoreRequestV1, now: datetime) -> c.ScoreProfileV1:
    if type(request) is not c.ScoreRequestV1:
        raise TypeError("exact score request required")
    c.utc(now)
    c._Record.__post_init__(request)
    profile = PROFILES.get(request.signal)
    if (
        profile is None
        or request.profile_id != profile.profile_id
        or request.subject != "NVDA"
        or request.as_of_utc != T
        or request.knowledge_cutoff_utc != T + timedelta(seconds=1)
        or now < request.knowledge_cutoff_utc
        or len(request.predecessor_ids) != len(profile.dependencies)
        or len(set(request.predecessor_ids)) != len(request.predecessor_ids)
        or any(not i for i in request.predecessor_ids)
    ):
        raise ValueError("unadmitted profile/time/input request")
    return profile


def _foundation(
    p: f.WindowMeasurementOccurrenceV1,
    dep: c.DependencyV1,
    request: c.ScoreRequestV1,
    now: datetime,
) -> None:
    pc = p.request.calculation
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
        or p.request.context.ref.context_id + "/" + str(p.request.context.ref.version)
        != dep.context
        or pc.context_refs != (p.request.context.ref,)
        or p.window_seconds != dep.window
        or pc.subject_instrument != request.subject
        or p.parameter_set.subject_instrument != request.subject
        or p.parameter_set.members != (request.subject,)
        or p.effective_as_of_utc != request.as_of_utc
        or pc.as_of_utc != request.as_of_utc
        or p.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or pc.knowledge_cutoff_utc != request.knowledge_cutoff_utc
        or not p.knowledge_cutoff_utc <= p.calculated_at_utc <= now
        or not p.derived_occurrence_id.startswith("mmtwindow1:")
    ):
        raise ValueError("incompatible actual foundation predecessor")
    expected = {
        "D020": ("return", "scalar_decimal", Decimal, "mmt-close-selection"),
        "D021": ("return", "scalar_decimal", Decimal, "mmt-close-selection"),
        "D024": (
            "return/minute",
            "named_exact_acceleration",
            f.ReturnAccelerationV1,
            "mmt-return-acceleration-selection",
        ),
        "D027": (
            "price/minute / percent/minute",
            "named_exact_vwap_rate",
            f.VwapRateV1,
            "mmt-vwap-rate-300s-selection",
        ),
    }[dep.signal]
    units, shape, cls, selection = expected
    if (
        p.units != units
        or p.result_shape != shape
        or type(p.result) is not cls
        or p.definition.units != units
        or p.definition.result_shape != shape
        or p.input_selection_policy.context_id != selection
        or p.input_selection_policy.version != 1
        or pc.input_selection_policy_ref != f.VersionRefV1(selection, 1)
        or p.request.context.session_start_utc != T.replace(minute=0)
        or p.request.context.session_end_utc != T.replace(hour=13, minute=0)
        or not p.raw_input_lineage
    ):
        raise ValueError("incompatible shape/unit/selection/session")


def produce(
    request: c.ScoreRequestV1,
    predecessors: tuple[f.WindowMeasurementOccurrenceV1, ...],
    now: datetime,
) -> c.ScoreOccurrenceV1:
    profile = request_check(request, now)
    if len(predecessors) != len(profile.dependencies):
        raise ValueError("all actual required predecessors needed")
    for p, dep, identity in zip(
        predecessors, profile.dependencies, request.predecessor_ids, strict=True
    ):
        if type(p) is not f.WindowMeasurementOccurrenceV1 or p.derived_occurrence_id != identity:
            raise ValueError("actual ordered occurrence required")
        _foundation(p, dep, request, now)
    by_signal = {p.derived_signal_id: p for p in predecessors}
    if "D024" in by_signal:
        nested = by_signal["D024"].predecessors
        if (
            len(nested) != 3
            or canonical(nested[1]) != canonical(by_signal["D020"])
            or canonical(nested[2]) != canonical(by_signal["D021"])
        ):
            raise ValueError("incoherent direct/acceleration predecessor chain")
    evidence = []
    total = ratio(profile.intercept)
    for feature in profile.features:
        p = by_signal[feature.signal]
        raw = p.result if feature.path == "result" else getattr(p.result, feature.path)
        x = (
            Fraction(raw)
            if type(raw) is Decimal and raw.is_finite()
            else ratio(cast(f.ExactRatioV1, raw))
        )
        scale = ratio(feature.scale)
        if scale <= 0 or ratio(feature.weight) < 0 or feature.orientation not in (-1, 1):
            raise ValueError("invalid immutable score coefficient")
        if feature.transform == "bounded_ratio":
            z = x / (scale + abs(x))
        elif feature.transform == "identity":
            z = x
        else:
            raise ValueError("unsupported immutable transform")
        if feature.clip[0] > feature.clip[1]:
            raise ValueError("invalid clip")
        z = min(max(z, Fraction(feature.clip[0])), Fraction(feature.clip[1]))
        oriented = z * feature.orientation
        weighted = oriented * ratio(feature.weight)
        total += weighted
        evidence.append(
            c.FeatureEvidenceV1(
                feature,
                p.derived_occurrence_id,
                carrier(x),
                carrier(z),
                carrier(oriented),
                carrier(weighted),
            )
        )
    if not 0 <= total <= 1:
        raise ValueError("controlled score range violated")
    value = c.ScoreOccurrenceV1(
        "M03",
        NAMESPACE,
        BRIEFS[request.signal],
        request.signal,
        "pending",
        request,
        profile,
        hashlib.sha256(PROFILE_BYTES[request.signal].encode()).hexdigest(),
        predecessors,
        tuple(evidence),
        carrier(total),
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
            cast(tuple[f.WindowMeasurementOccurrenceV1, ...], value.predecessors),
            value.calculated_at_utc,
        )
    ):
        raise ValueError("score metadata/lineage/result/identity mismatch")


def _decode(payload: bytes) -> c.ScoreOccurrenceV1:
    return cast(c.ScoreOccurrenceV1, decode(payload, c.ScoreOccurrenceV1))


class _Reads:
    def __init__(self, state: RecordState) -> None:
        self.state = state

    def get_derived_occurrence(self, derived_occurrence_id: str) -> c.ScoreOccurrenceV1 | None:
        if type(derived_occurrence_id) is not str:
            raise TypeError("exact identity string required")
        if not re.fullmatch(r"cmcscore1:[0-9a-f]{64}", derived_occurrence_id):
            raise ValueError("score identity required")
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
    ) -> tuple[c.ScoreOccurrenceV1, ...]:
        c.utc(effective_at_or_before_utc)
        c.utc(knowledge_at_or_before_utc)
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("bounded exact history limit required")
        if type(derived_signal_id) is not str or type(subject_instrument) is not str:
            raise TypeError("exact history identifiers required")
        if derived_signal_id not in BRIEFS or subject_instrument != "NVDA":
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


def _admission(admission: f.OwnerAdmissionV1) -> str:
    if type(admission) is not f.OwnerAdmissionV1 or admission.object_id != "M03":
        raise ValueError("exact configured-owner admission required")
    matches = [s for s, h in BRIEFS.items() if admission.implementation_brief_sha256 == h]
    if len(matches) != 1:
        raise ValueError("unsupported owning authority")
    return matches[0]


def _validator(signal: str) -> Callable[[c.ScoreOccurrenceV1], None]:
    def check(value: c.ScoreOccurrenceV1) -> None:
        validate(value)
        if value.derived_signal_id != signal:
            raise ValueError("wrong admitted score file")

    return check


class _Owner:
    def __init__(
        self,
        state: RecordState,
        reader: f.MeasurementWindowReadsV1,
        now: Callable[[], datetime],
        signal: str,
    ) -> None:
        self.state, self.reader, self.now, self.signal = state, reader, now, signal
        self.reads = _Reads(state)

    def materialise(self, request: c.ScoreRequestV1) -> c.ScoreOccurrenceV1 | None:
        now = self.now()
        c.utc(now)
        try:
            request_check(request, now)
            if request.signal != self.signal:
                return None
            facts = tuple(self.reader.get_derived_occurrence(i) for i in request.predecessor_ids)
            if any(type(p) is not f.WindowMeasurementOccurrenceV1 for p in facts):
                return None
            value = produce(request, cast(tuple[f.WindowMeasurementOccurrenceV1, ...], facts), now)
        except (TypeError, ValueError, ArithmeticError, AttributeError, KeyError):
            return None
        return cast(c.ScoreOccurrenceV1, self.state.append(value))


def build_owner(
    admission: f.OwnerAdmissionV1,
    predecessor: f.MeasurementWindowReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    now: Callable[[], datetime],
) -> c.ScoreOwnerV1:
    signal = _admission(admission)
    if type(storage) not in (f.MemoryStorageV1, f.SQLiteStorageV1) or not callable(now):
        raise TypeError("exact storage and clock required")
    if not callable(getattr(predecessor, "get_derived_occurrence", None)):
        raise TypeError("actual public predecessor reader required")
    return _Owner(RecordState(storage, _decode, _validator(signal)), predecessor, now, signal)


def build_reader(admission: f.OwnerAdmissionV1, storage: f.SQLiteReadStorageV1) -> c.ScoreReadsV1:
    signal = _admission(admission)
    if type(storage) is not f.SQLiteReadStorageV1:
        raise TypeError("exact read-only score storage required")
    return _Reads(RecordState(storage, _decode, _validator(signal)))
