from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError


def _require_module(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Required module is not implemented: {module_path} ({exc})")


def _require_attr(module, attr_name: str):
    if not hasattr(module, attr_name):
        pytest.fail(f"Required attribute is not implemented: {module.__name__}.{attr_name}")
    return getattr(module, attr_name)


def test_review_contract_module_exports_preserved_review_models() -> None:
    contracts = _require_module("nvda_desk.contracts.review")
    assert contracts.__name__ == "nvda_desk.contracts.review"
    for attr_name in (
        "ReviewPacket",
        "ReviewLineage",
        "PromotionEvidence",
        "FailureTaxonomyRecord",
        "EconomicAccountabilityRecord",
        "EffectivePolicySnapshot",
        "ReviewLineagePacket",
        "PacketLineageSurface",
    ):
        assert _require_attr(contracts, attr_name) is getattr(contracts, attr_name)

    effective_policy = _require_attr(contracts, "EffectivePolicySnapshot")
    assert effective_policy is getattr(contracts, "EffectivePolicySnapshot")
    review_lineage = _require_attr(contracts, "ReviewLineagePacket")
    assert review_lineage is getattr(contracts, "ReviewLineagePacket")
    assert "resolved_coefficients" in effective_policy.model_fields
    assert "resolved_coefficients" in review_lineage.model_fields


def test_review_failure_taxonomy_carries_bounded_review_outcomes() -> None:
    contracts = _require_module("nvda_desk.contracts.review")
    assert contracts.__name__ == "nvda_desk.contracts.review"
    failure_record = _require_attr(contracts, "FailureTaxonomyRecord")
    assert failure_record is getattr(contracts, "FailureTaxonomyRecord")
    failure_class = _require_attr(contracts, "ReviewFailureClass")
    assert failure_class is getattr(contracts, "ReviewFailureClass")
    resolution_class = _require_attr(contracts, "ReviewResolutionClass")
    assert resolution_class is getattr(contracts, "ReviewResolutionClass")

    bad_read = failure_record(
        primary_failure_class=failure_class.DATA_PROVENANCE_FAILURE,
        resolution=resolution_class.NON_ACTION,
        non_action=True,
        evidence_floor={"minimum_evidence": ["source timestamp missing"]},
        rationale=["bad read blocked the decision basis"],
    )
    bad_expression = failure_record(
        primary_failure_class=failure_class.EXECUTION_EXPRESSION_FAILURE,
        resolution=resolution_class.BLOCKED_TRADE,
        blocked_trade=True,
        rationale=["expression failed at execution handoff"],
    )
    bad_sizing = failure_record(
        primary_failure_class=failure_class.SIZING_FAILURE,
        resolution=resolution_class.UNRESOLVED,
        rationale=["sizing envelope could not be reconstructed"],
    )
    bad_luck = failure_record(
        resolution=resolution_class.BAD_LUCK,
        rationale=["decision basis was reconstructable and no failure class was assigned"],
    )

    assert bad_read.model_dump(mode="json")["primary_failure_class"] == "data_provenance_failure"
    assert bad_read.model_dump(mode="json")["non_action"] is True
    assert (
        bad_expression.model_dump(mode="json")["primary_failure_class"]
        == "execution_expression_failure"
    )
    assert bad_expression.model_dump(mode="json")["blocked_trade"] is True
    assert bad_sizing.model_dump(mode="json")["primary_failure_class"] == "sizing_failure"
    assert bad_luck.model_dump(mode="json")["resolution"] == "bad_luck"

    with pytest.raises(ValidationError):
        failure_record(primary_failure_class="unbounded_failure", resolution="unknown")


def test_economic_accountability_carries_non_action_review_tag() -> None:
    contracts = _require_module("nvda_desk.contracts.review")
    assert contracts.__name__ == "nvda_desk.contracts.review"
    accountability_record = _require_attr(contracts, "EconomicAccountabilityRecord")
    assert accountability_record is getattr(contracts, "EconomicAccountabilityRecord")
    contribution_tag = _require_attr(contracts, "EconomicContributionTag")
    assert contribution_tag is getattr(contracts, "EconomicContributionTag")

    record = accountability_record(
        diagnosis=contribution_tag.VALUE_ADD,
        posture=contribution_tag.CAPITAL_PRESERVATION,
        timing=contribution_tag.NEUTRAL,
        execution=contribution_tag.VALUE_LEAK,
        sizing=contribution_tag.UNKNOWN,
        non_action=contribution_tag.CAPITAL_PRESERVATION,
    )

    payload = record.model_dump(mode="json")
    assert payload == {
        "diagnosis": "value_add",
        "posture": "capital_preservation",
        "timing": "neutral",
        "execution": "value_leak",
        "sizing": "unknown",
        "non_action": "capital_preservation",
    }

    with pytest.raises(ValidationError):
        accountability_record(non_action="unbounded_non_action_tag")
