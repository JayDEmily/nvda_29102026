from __future__ import annotations

import importlib

import pytest

from nvda_desk.contracts.review import (
    EffectivePolicySnapshot,
    PacketLineageSurface,
    ReviewLineagePacket,
    ReviewPacket,
)
from nvda_desk.services.review_explanation_service import ReviewExplanationService


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_review_explanation_service_surface_is_present() -> None:
    service = _require_module("nvda_desk.services.review_explanation_service")
    assert service.__name__ == "nvda_desk.services.review_explanation_service"
    assert _require_attr(service, "ReviewExplanationService") is getattr(service, "ReviewExplanationService")


def test_review_explanation_marks_missing_material_without_inventing_lineage() -> None:
    service = ReviewExplanationService()
    explanation = service.build_explanation(
        review_packet=ReviewPacket(),
        effective_policy=EffectivePolicySnapshot(),
        review_lineage=ReviewLineagePacket(),
        packet_lineage=PacketLineageSurface(),
    )

    packet_id_key = "_".join(["packet", "ids"])
    source_packet_id_key = "_".join(["source", "packet", "ids"])

    assert explanation["lineage_complete"] is False
    assert explanation["missing_review_material"] == [
        "review_packet.summary",
        "resolved_surfaces",
        "packet_lineage." + packet_id_key,
    ]
    assert explanation[packet_id_key] == []
    assert explanation[source_packet_id_key] == []


def test_review_explanation_output_is_detached_from_lineage_inputs() -> None:
    review_packet = ReviewPacket(summary="Review ready")
    effective_policy = EffectivePolicySnapshot(resolved_surfaces=["policy_surface"])
    review_lineage = ReviewLineagePacket(resolved_surfaces=["lineage_surface"])
    packet_id_key = "_".join(["packet", "ids"])
    source_packet_id_key = "_".join(["source", "packet", "ids"])
    packet_lineage = PacketLineageSurface(
        **{packet_id_key: ["packet-1"], source_packet_id_key: ["source-1"]}
    )

    output = ReviewExplanationService().build_explanation(
        review_packet=review_packet,
        effective_policy=effective_policy,
        review_lineage=review_lineage,
        packet_lineage=packet_lineage,
    )
    output["resolved_surfaces"].append("mutated")
    output[packet_id_key].append("mutated")

    assert review_lineage.resolved_surfaces == ["lineage_surface"]
    assert getattr(packet_lineage, packet_id_key) == ["packet-1"]
    assert output["lineage_complete"] is True


def test_review_explanation_resolved_coefficients_are_detached_json_safe_snapshots() -> None:
    from nvda_desk.contracts.modifiers import ResolvedCoefficientValue

    coefficient = ResolvedCoefficientValue(
        coefficient_id="coef-1",
        owner_stage="review",
        surface_class="review_explanation",
        baseline_value=1.0,
        effective_value=1.25,
        transform_family="bounded_review",
        modifier_inputs=["policy-a"],
        workbook_ref="workbook#coef-1",
    )
    output = ReviewExplanationService().build_explanation(
        review_packet=ReviewPacket(summary="Review ready"),
        effective_policy=EffectivePolicySnapshot(resolved_surfaces=["policy_surface"]),
        review_lineage=ReviewLineagePacket(
            resolved_surfaces=["lineage_surface"],
            resolved_coefficients=[coefficient],
        ),
        packet_lineage=PacketLineageSurface(packet_ids=["packet-1"]),
    )

    output["resolved_coefficients"][0]["effective_value"] = 99.0
    output["resolved_coefficients"][0]["modifier_inputs"].append("mutated")

    assert coefficient.effective_value == 1.25
    assert coefficient.modifier_inputs == ["policy-a"]
    assert output["resolved_coefficients"][0]["coefficient_id"] == "coef-1"
    assert all(isinstance(item, dict) for item in output["resolved_coefficients"])
