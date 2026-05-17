from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


class WalkForwardWindowMode(str, Enum):
    ROLLING = "rolling"
    EXPANDING = "expanding"


class WalkForwardWindowRole(str, Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"


class ChronologyRule(str, Enum):
    NO_OVERLAP = "no_overlap"
    STRICT_ASCENDING = "strict_ascending"


class DownstreamConsumerMode(str, Enum):
    REVIEW_ONLY = "review_only"
    RESEARCH_ONLY = "research_only"


@dataclass(frozen=True, slots=True)
class WalkForwardSliceDefinition:
    slice_id: str
    start_index: int
    end_index: int
    role: WalkForwardWindowRole

    def __post_init__(self) -> None:
        _require_non_empty(self.slice_id, "slice_id")
        _require_ordered(self.start_index, self.end_index)


@dataclass(frozen=True, slots=True)
class WalkForwardStartOffset:
    offset_id: str
    start_index: int = 0

    def __post_init__(self) -> None:
        _require_non_empty(self.offset_id, "offset_id")
        if self.start_index < 0:
            raise ValueError("start_index must be non-negative")


@dataclass(frozen=True, slots=True)
class StabilityComparisonRule:
    metric_name: str
    maximum_degradation: Decimal

    def __post_init__(self) -> None:
        _require_non_empty(self.metric_name, "metric_name")
        if self.maximum_degradation < Decimal("0"):
            raise ValueError("maximum_degradation must be non-negative")


@dataclass(frozen=True, slots=True)
class WalkForwardWindow:
    window_id: str
    role: WalkForwardWindowRole
    start_index: int
    end_index: int
    mode: WalkForwardWindowMode = WalkForwardWindowMode.ROLLING

    def __post_init__(self) -> None:
        _require_non_empty(self.window_id, "window_id")
        _require_ordered(self.start_index, self.end_index)

    def precedes(self, other: "WalkForwardWindow") -> bool:
        return self.end_index < other.start_index


@dataclass(frozen=True, slots=True)
class OffsetComparisonOutcome:
    offset_id: str
    baseline_metric: Decimal
    candidate_metric: Decimal
    rule: StabilityComparisonRule

    @property
    def degradation(self) -> Decimal:
        return self.baseline_metric - self.candidate_metric

    @property
    def is_stable(self) -> bool:
        return self.degradation <= self.rule.maximum_degradation


@dataclass(frozen=True, slots=True)
class HorizonDiscoveryOutcome:
    horizon_id: str
    offset_outcomes: tuple[OffsetComparisonOutcome, ...]
    minimum_stable_offsets: int = 1

    @property
    def stable_offset_count(self) -> int:
        return sum(1 for outcome in self.offset_outcomes if outcome.is_stable)

    @property
    def is_accepted(self) -> bool:
        return self.stable_offset_count >= self.minimum_stable_offsets


@dataclass(frozen=True, slots=True)
class ContextSliceReport:
    slice_id: str
    event_tags: tuple[str, ...] = ()
    row_count: int = 0


@dataclass(frozen=True, slots=True)
class FragilitySignalReport:
    signal_id: str
    fragility_score: Decimal
    scenario_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AblationSignalReport:
    signal_id: str
    removed_feature_ids: tuple[str, ...] = ()
    pruning_hint: str | None = None


@dataclass(frozen=True, slots=True)
class HorizonDiscoveryBinding:
    review_packet_id: str
    candidate_id: str
    research_log_id: str | None = None


@dataclass(frozen=True, slots=True)
class GroupReviewHorizonResult:
    group_id: str
    horizon_outcome: HorizonDiscoveryOutcome
    bindings: HorizonDiscoveryBinding


@dataclass(frozen=True, slots=True)
class WalkForwardHarnessAuthorityPacket:
    packet_id: str
    windows: tuple[WalkForwardWindow, ...] = ()
    chronology_rule: ChronologyRule = ChronologyRule.NO_OVERLAP
    consumer_mode: DownstreamConsumerMode = DownstreamConsumerMode.REVIEW_ONLY

    def __post_init__(self) -> None:
        _require_non_empty(self.packet_id, "packet_id")
        ordered = sorted(self.windows, key=lambda window: (window.start_index, window.end_index))
        for prior, current in zip(ordered, ordered[1:]):
            if prior.end_index >= current.start_index:
                raise ValueError("chronology leakage: walk-forward windows overlap")


@dataclass(frozen=True, slots=True)
class StackComparisonSummary:
    stack_id: str
    score: Decimal
    baseline_score: Decimal = Decimal("0")

    @property
    def delta(self) -> Decimal:
        return self.score - self.baseline_score


@dataclass(frozen=True, slots=True)
class ComparisonReport:
    report_id: str
    stack_summaries: tuple[StackComparisonSummary, ...]
    consumer_mode: DownstreamConsumerMode = DownstreamConsumerMode.REVIEW_ONLY

    @property
    def best_stack_id(self) -> str | None:
        if not self.stack_summaries:
            return None
        return max(self.stack_summaries, key=lambda summary: summary.score).stack_id


@dataclass(frozen=True, slots=True)
class FragilityScenario:
    scenario_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BucketSummary:
    bucket_id: str
    count: int
    mean_score: Decimal


class BucketAccumulator:
    def __init__(self, bucket_id: str) -> None:
        self.bucket_id = _require_non_empty(bucket_id, "bucket_id")
        self._scores: list[Decimal] = []
        self._candidate_ids: list[str] = []

    def add(self, candidate_id: str, score: Decimal) -> None:
        self._candidate_ids.append(_require_non_empty(candidate_id, "candidate_id"))
        self._scores.append(Decimal(score))

    def summary(self) -> BucketSummary:
        if not self._scores:
            return BucketSummary(bucket_id=self.bucket_id, count=0, mean_score=Decimal("0"))
        return BucketSummary(
            bucket_id=self.bucket_id,
            count=len(self._scores),
            mean_score=sum(self._scores, Decimal("0")) / Decimal(len(self._scores)),
        )


class FailureCollector:
    def __init__(self, kind: str) -> None:
        self.kind = _require_non_empty(kind, "kind")
        self._records: list[tuple[str, str]] = []

    def add(self, failure_mode: str, detail: str) -> None:
        self._records.append(
            (_require_non_empty(failure_mode, "failure_mode"), _require_non_empty(detail, "detail"))
        )

    @property
    def records(self) -> tuple[tuple[str, str], ...]:
        return tuple(self._records)


@dataclass(frozen=True, slots=True)
class FailureModeSummary:
    count_by_mode: dict[str, int]


class StrategicLadderExperimentService:
    def run_walk_forward(
        self, rows: Iterable[Mapping[str, Any]], *, report_id: str
    ) -> ComparisonReport:
        return run_slv_walk_forward_from_market(rows, report_id=report_id)

    def run_fragility(
        self, rows: Iterable[Mapping[str, Any]], *, report_id: str
    ) -> ComparisonReport:
        return run_slv_fragility_from_market(rows, report_id=report_id)

    def run_batch_rank(
        self, rows: Iterable[Mapping[str, Any]], *, report_id: str
    ) -> ComparisonReport:
        return run_slv_batch_rank_from_market(rows, report_id=report_id)


def build_default_walk_forward_authority_packet(
    *,
    packet_id: str = "walk_forward_authority_default",
    row_count: int = 9,
) -> WalkForwardHarnessAuthorityPacket:
    third = max(row_count // 3, 1)
    return WalkForwardHarnessAuthorityPacket(
        packet_id=packet_id,
        windows=(
            WalkForwardWindow("train", WalkForwardWindowRole.TRAIN, 0, third - 1),
            WalkForwardWindow("validation", WalkForwardWindowRole.VALIDATION, third, third * 2 - 1),
            WalkForwardWindow("test", WalkForwardWindowRole.TEST, third * 2, row_count - 1),
        ),
    )


def build_comparison_report(
    *, report_id: str, stack_summaries: Sequence[Mapping[str, Any] | StackComparisonSummary]
) -> ComparisonReport:
    summaries = tuple(_coerce_stack_summary(summary) for summary in stack_summaries)
    return ComparisonReport(report_id=report_id, stack_summaries=summaries)


def rank_stack_summary(summary: StackComparisonSummary) -> Decimal:
    return summary.delta


def build_variant_payload(variant_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {"variant_id": _require_non_empty(variant_id, "variant_id"), "payload": dict(payload)}


def build_default_fragility_scenarios() -> tuple[FragilityScenario, ...]:
    return (
        FragilityScenario("baseline", {"shock": "none"}),
        FragilityScenario("liquidity_thin", {"shock": "spread_widening"}),
        FragilityScenario("volatility_jump", {"shock": "iv_expansion"}),
    )


def build_bucket_summaries(accumulators: Iterable[BucketAccumulator]) -> tuple[BucketSummary, ...]:
    return tuple(accumulator.summary() for accumulator in accumulators)


def build_failure_mode_summary(collector: FailureCollector) -> FailureModeSummary:
    counter = Counter(f"{mode}:{detail}" for mode, detail in collector.records)
    return FailureModeSummary(count_by_mode=dict(sorted(counter.items())))


def merge_failure_modes(summaries: Iterable[FailureModeSummary]) -> FailureModeSummary:
    counter: Counter[str] = Counter()
    for summary in summaries:
        counter.update(summary.count_by_mode)
    return FailureModeSummary(count_by_mode=dict(sorted(counter.items())))


def run_slv_walk_forward_from_market(
    rows: Iterable[Mapping[str, Any]], *, report_id: str = "slv_walk_forward"
) -> ComparisonReport:
    return _market_rows_to_report(rows, report_id=report_id)


def run_slv_fragility_from_market(
    rows: Iterable[Mapping[str, Any]], *, report_id: str = "slv_fragility"
) -> ComparisonReport:
    return _market_rows_to_report(rows, report_id=report_id)


def run_slv_batch_rank_from_market(
    rows: Iterable[Mapping[str, Any]], *, report_id: str = "slv_batch_rank"
) -> ComparisonReport:
    report = _market_rows_to_report(rows, report_id=report_id)
    ranked = tuple(sorted(report.stack_summaries, key=lambda summary: summary.score, reverse=True))
    return ComparisonReport(report_id=report.report_id, stack_summaries=ranked)


def _market_rows_to_report(
    rows: Iterable[Mapping[str, Any]], *, report_id: str
) -> ComparisonReport:
    summaries = []
    for row in rows:
        stack_id = str(row.get("candidate_id") or row.get("stack_id") or "candidate").strip()
        score = Decimal(str(row.get("score", "0")))
        baseline = Decimal(str(row.get("baseline_score", "0")))
        summaries.append(
            StackComparisonSummary(stack_id=stack_id, score=score, baseline_score=baseline)
        )
    return ComparisonReport(report_id=report_id, stack_summaries=tuple(summaries))


def _coerce_stack_summary(
    value: Mapping[str, Any] | StackComparisonSummary,
) -> StackComparisonSummary:
    if isinstance(value, StackComparisonSummary):
        return value
    return StackComparisonSummary(
        stack_id=str(value["stack_id"]),
        score=Decimal(str(value.get("score", "0"))),
        baseline_score=Decimal(str(value.get("baseline_score", "0"))),
    )


def _require_non_empty(value: str, field_name: str) -> str:
    token = str(value).strip()
    if not token:
        raise ValueError(f"{field_name} must be non-empty")
    return token


def _require_ordered(start_index: int, end_index: int) -> None:
    if start_index < 0 or end_index < 0:
        raise ValueError("window indices must be non-negative")
    if start_index > end_index:
        raise ValueError("start_index must be <= end_index")
