"""Deterministic review-replay comparison services."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.review_replay import (
    ImportedModuleCitation,
    ReviewReplayComparisonResult,
    ReviewReplayDecision,
)
from nvda_desk.review.imported_module_citations import map_imported_module_citations


def compare_imported_module_review_replay(
    *,
    citations: Iterable[ImportedModuleCitation],
    decisions: Iterable[ReviewReplayDecision],
) -> ReviewReplayComparisonResult:
    """Compare imported-module citation claims against review decisions without runtime promotion."""

    citation_list = sorted(list(citations), key=lambda row: row.source_identifier)
    decision_sources = {decision.source_identifier for decision in decisions}
    compared_sources = [citation.source_identifier for citation in citation_list]
    missing_sources = sorted(set(compared_sources) - decision_sources)
    traces = []
    if not missing_sources:
        traces = map_imported_module_citations(citations=citation_list, decisions=decisions)
    return ReviewReplayComparisonResult(
        compared_source_identifiers=compared_sources,
        missing_decision_source_identifiers=missing_sources,
        citation_traces=traces,
        promoted_to_runtime=False,
        runtime_side_effects=[],
    )
