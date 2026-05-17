"""Pure candidate audit helpers for the parallel-risk lane."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskCandidateAuditSurface,
    ParallelRiskConsequencePosture,
    ParallelRiskFragilityDimension,
)

_BLOCK_TAGS = {"vix_extreme", "hard_block", "liquidity_void"}
_CAUTION_TAGS = {
    "earnings",
    "negative_gamma",
    "scheduled_event_window_active",
    "event_gap_risk",
}


def audit_candidate(
    *,
    candidate_id: str | None,
    semantic_tags: Iterable[str] | None = None,
    fragility_dimensions: Iterable[ParallelRiskFragilityDimension] = (),
    risk_event_ids: Iterable[str] = (),
) -> ParallelRiskCandidateAuditSurface:
    """Return one bounded candidate-audit surface for lawful descriptive enrichments."""

    tags = [str(tag) for tag in list(semantic_tags or [])]
    fragility = [dimension.model_copy(deep=True) for dimension in fragility_dimensions]
    events = [str(event_id) for event_id in risk_event_ids]
    return ParallelRiskCandidateAuditSurface(
        candidate_id=candidate_id,
        semantic_tags=tags,
        audit_state="candidate_present" if candidate_id else "no_candidate",
        consequence_posture=_consequence_posture(tags=tags, fragility_dimensions=fragility),
        fragility_dimensions=fragility,
        descriptive_semantics=sorted(
            set(tags + [dimension.dimension_id for dimension in fragility])
        ),
        risk_event_ids=events,
    )


def _consequence_posture(
    *, tags: list[str], fragility_dimensions: list[ParallelRiskFragilityDimension]
) -> ParallelRiskConsequencePosture:
    tag_set = set(tags)
    max_score = max((dimension.score for dimension in fragility_dimensions), default=0.0)
    if tag_set & _BLOCK_TAGS or max_score >= 0.9:
        return "block"
    if tag_set & _CAUTION_TAGS or max_score >= 0.5:
        return "caution"
    return "observe"
