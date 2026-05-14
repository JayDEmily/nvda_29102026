"""Build deterministic explanation surfaces for downstream review consumers."""

from __future__ import annotations

from nvda_desk.contracts.review import (
    EffectivePolicySnapshot,
    PacketLineageSurface,
    ReviewLineagePacket,
    ReviewPacket,
)


class ReviewExplanationService:
    """Translate review-lineage facts into deterministic explanation text."""

    def build_explanation(
        self,
        *,
        review_packet: ReviewPacket,
        effective_policy: EffectivePolicySnapshot,
        review_lineage: ReviewLineagePacket,
        packet_lineage: PacketLineageSurface,
    ) -> dict:
        summary = review_packet.summary or ""
        resolved_surfaces = list(
            review_lineage.resolved_surfaces or effective_policy.resolved_surfaces
        )
        packet_ids = list(packet_lineage.packet_ids)
        source_packet_ids = list(packet_lineage.source_packet_ids)
        missing_material = []
        if not summary:
            missing_material.append("review_packet.summary")
        if not resolved_surfaces:
            missing_material.append("resolved_surfaces")
        if not packet_ids:
            missing_material.append("packet_lineage.packet_ids")

        surfaces_text = ", ".join(resolved_surfaces)
        packet_ids_text = ", ".join(packet_ids)
        resolved_coefficients = [
            coefficient.model_dump()
            for coefficient in (
                review_lineage.resolved_coefficients or effective_policy.resolved_coefficients
            )
        ]
        return {
            "summary": summary,
            "resolved_surfaces": resolved_surfaces,
            "packet_ids": packet_ids,
            "source_packet_ids": source_packet_ids,
            "resolved_coefficients": resolved_coefficients,
            "missing_review_material": missing_material,
            "lineage_complete": not missing_material,
            "explanation": f"{summary} | surfaces={surfaces_text} | packets={packet_ids_text}".strip(),
        }
