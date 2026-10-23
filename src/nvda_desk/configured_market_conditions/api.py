"""Typed controlled P02 score boundary; no acquisition or trading side effects."""

from __future__ import annotations

import types
from collections.abc import Callable
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from typing import Protocol, get_args, get_origin, get_type_hints

from nvda_desk.market_measurement_truth import api as f


def utc(value: datetime) -> None:
    if type(value) is not datetime:
        raise TypeError("exact datetime required")
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError("UTC-aware instant required")


def _matches(value: object, hint: object) -> bool:
    origin, args = get_origin(hint), get_args(hint)
    if origin is types.UnionType:
        return any(_matches(value, h) for h in args)
    if origin is tuple:
        if type(value) is not tuple:
            return False
        if len(args) == 2 and args[1] is Ellipsis:
            return all(_matches(v, args[0]) for v in value)
        return len(value) == len(args) and all(
            _matches(v, h) for v, h in zip(value, args, strict=True)
        )
    return type(value) is hint


class _Record:
    __slots__ = ()

    def __post_init__(self) -> None:
        hints = get_type_hints(type(self))
        for field in fields(self):  # type: ignore[arg-type]
            value = getattr(self, field.name)
            if not _matches(value, hints[field.name]):
                raise TypeError(field.name + " has wrong exact type")
            if type(value) is str and not value:
                raise ValueError("nonempty identity required")
            if type(value) is datetime:
                utc(value)


@dataclass(frozen=True, slots=True)
class FeatureV1(_Record):
    signal: str
    path: str
    units: str
    transform: str
    scale: f.ExactRatioV1
    clip: tuple[int, int]
    orientation: int
    weight: f.ExactRatioV1


@dataclass(frozen=True, slots=True)
class DependencyV1(_Record):
    signal: str
    owner: str
    brief: str
    definition: str
    parameter: str
    context: str
    window: int


@dataclass(frozen=True, slots=True)
class ScoreProfileV1(_Record):
    signal: str
    definition: str
    profile_id: str
    kernel: str
    units: str
    output: str
    intercept: f.ExactRatioV1
    features: tuple[FeatureV1, ...]
    dependencies: tuple[DependencyV1, ...]


@dataclass(frozen=True, slots=True)
class ScoreRequestV1(_Record):
    signal: str
    subject: str
    as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    profile_id: str
    predecessor_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FeatureEvidenceV1(_Record):
    feature: FeatureV1
    source_occurrence_id: str
    extracted: f.ExactRatioV1
    transformed: f.ExactRatioV1
    oriented: f.ExactRatioV1
    weighted: f.ExactRatioV1


@dataclass(frozen=True, slots=True)
class ScoreOccurrenceV1(_Record):
    owner_object_id: str
    owner_namespace: str
    implementation_brief_sha256: str
    derived_signal_id: str
    derived_occurrence_id: str
    request: ScoreRequestV1
    profile: ScoreProfileV1
    profile_sha256: str
    predecessors: tuple[f.WindowMeasurementOccurrenceV1 | ScoreOccurrenceV1, ...]
    features: tuple[FeatureEvidenceV1, ...]
    result: f.ExactRatioV1
    units: str
    result_shape: str
    effective_as_of_utc: datetime
    knowledge_cutoff_utc: datetime
    calculated_at_utc: datetime


class ScoreReadsV1(Protocol):
    def get_derived_occurrence(self, derived_occurrence_id: str) -> ScoreOccurrenceV1 | None: ...
    def list_derived_history(
        self,
        *,
        derived_signal_id: str,
        subject_instrument: str,
        effective_at_or_before_utc: datetime,
        knowledge_at_or_before_utc: datetime,
        limit: int,
    ) -> tuple[ScoreOccurrenceV1, ...]: ...


class ScoreOwnerV1(Protocol):
    @property
    def reads(self) -> ScoreReadsV1: ...
    def materialise(self, request: ScoreRequestV1) -> ScoreOccurrenceV1 | None: ...


def profile_from_document(document: dict) -> ScoreProfileV1:
    """Lossless exact profile construction; construction does not authorise arbitrary profiles."""

    def ratio(pair: list) -> f.ExactRatioV1:
        if type(pair) is not list or len(pair) != 2:
            raise TypeError("rational pair required")
        return f.ExactRatioV1(*pair)

    return ScoreProfileV1(
        **{k: v for k, v in document.items() if k not in ("intercept", "features", "dependencies")},
        intercept=ratio(document["intercept"]),
        features=tuple(
            FeatureV1(
                **{k: v for k, v in item.items() if k not in ("scale", "clip", "weight")},
                scale=ratio(item["scale"]),
                clip=tuple(item["clip"]),
                weight=ratio(item["weight"]),
            )
            for item in document["features"]
        ),
        dependencies=tuple(DependencyV1(**item) for item in document["dependencies"]),
    )


def create_owner(
    *,
    admission: f.OwnerAdmissionV1,
    predecessor_reader: f.MeasurementWindowReadsV1,
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    utc_now: Callable[[], datetime],
) -> ScoreOwnerV1:
    from ._score import build_owner

    return build_owner(admission, predecessor_reader, storage, utc_now)


def create_reader(
    *,
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteReadStorageV1,
) -> ScoreReadsV1:
    from ._score import build_reader

    return build_reader(admission, storage)
