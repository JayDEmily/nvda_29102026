"""Trace imported-module review citations without promoting them to runtime authority."""

from __future__ import annotations

from collections.abc import Iterable

from nvda_desk.contracts.review_replay import (
    ImportedModuleCitation,
    ImportedModuleCitationTrace,
    ReviewReplayDecision,
)


def map_imported_module_citations(
    *,
    citations: Iterable[ImportedModuleCitation],
    decisions: Iterable[ReviewReplayDecision],
) -> list[ImportedModuleCitationTrace]:
    """Join citations to decisions in deterministic source-identifier order."""

    decision_by_source = {decision.source_identifier: decision for decision in decisions}
    traces: list[ImportedModuleCitationTrace] = []
    for citation in sorted(list(citations), key=lambda row: row.source_identifier):
        decision = decision_by_source[citation.source_identifier]
        traces.append(
            ImportedModuleCitationTrace(
                source_identifier=citation.source_identifier,
                imported_module=citation.imported_module,
                cited_claim=citation.cited_claim,
                decision_id=decision.decision_id,
                admission_class=decision.admission_class,
                rejection_or_supersession_status=decision.status,
                rejection_reason=decision.rejection_reason,
            )
        )
    return traces
