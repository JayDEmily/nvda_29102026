"""Pure candidate audit helpers for the parallel-risk lane."""

from __future__ import annotations

from nvda_desk.contracts.parallel_risk import ParallelRiskCandidateAuditSurface


def audit_candidate(
    *, candidate_id: str | None, semantic_tags: list[str] | None = None
) -> ParallelRiskCandidateAuditSurface:
    """Return one bounded candidate-audit surface for later lawful enrichments."""

    tags = list(semantic_tags or [])
    return ParallelRiskCandidateAuditSurface(
        candidate_id=candidate_id,
        semantic_tags=tags,
        audit_state="audited" if candidate_id else "no_candidate",
    )
