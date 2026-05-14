"""Build review-stage packets from runtime-visible facts only."""

from __future__ import annotations

from typing import Iterable

from nvda_desk.contracts.modifiers import ResolvedCoefficientValue
from nvda_desk.contracts.review import ReviewLineage, ReviewPacket


class ReviewStageService:
    """Construct review packets and attach deterministic lineage surfaces."""

    def build_review_packet(
        self,
        *,
        packet_id: str | None = None,
        summary: str | None = None,
        sections: Iterable[str] = (),
    ) -> ReviewPacket:
        return build_review_packet(packet_id=packet_id, summary=summary, sections=sections)

    def attach_lineage(
        self,
        *,
        packet: ReviewPacket,
        event_ids: Iterable[str] = (),
        resolved_surfaces: Iterable[str] = (),
        resolved_coefficients: Iterable[ResolvedCoefficientValue] = (),
    ) -> dict:
        return attach_lineage(
            packet=packet,
            event_ids=event_ids,
            resolved_surfaces=resolved_surfaces,
            resolved_coefficients=resolved_coefficients,
        )

    def attach_imported_citations(
        self, *, packet: ReviewPacket, citations: Iterable[str] = ()
    ) -> dict:
        return attach_imported_citations(packet=packet, citations=citations)


def build_review_packet(
    *, packet_id: str | None = None, summary: str | None = None, sections: Iterable[str] = ()
) -> ReviewPacket:
    """Return one typed review packet from runtime-visible text sections."""

    return ReviewPacket(packet_id=packet_id, summary=summary, sections=list(sections))


def attach_lineage(
    *,
    packet: ReviewPacket,
    event_ids: Iterable[str] = (),
    resolved_surfaces: Iterable[str] = (),
    resolved_coefficients: Iterable[ResolvedCoefficientValue] = (),
) -> dict:
    """Attach deterministic lineage metadata to one review packet."""

    lineage = ReviewLineage(
        event_ids=list(event_ids),
        resolved_surfaces=list(resolved_surfaces),
        resolved_coefficients=list(resolved_coefficients),
    )
    return {"review_packet": packet.model_dump(), "lineage": lineage.model_dump()}


def attach_imported_citations(*, packet: ReviewPacket, citations: Iterable[str] = ()) -> dict:
    """Attach import-stage citations without changing review semantics."""

    return {"review_packet": packet.model_dump(), "imported_citations": list(citations)}
