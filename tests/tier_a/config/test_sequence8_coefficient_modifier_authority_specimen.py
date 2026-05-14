"""Sequence 8 tests for coefficient/modifier authority specimens before runtime code."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

SPECIMEN_PATH = Path("tests/fixtures/sequence8/coefficient_modifier_authority_specimen.json")
AUTHORITY_PATH = Path("config/coefficient_authority.v1.yaml")


def _load_specimen() -> dict[str, Any]:
    """Load the bounded Sequence 8 coefficient/modifier specimen."""

    return json.loads(SPECIMEN_PATH.read_text(encoding="utf-8"))


def _load_authority() -> dict[str, Any]:
    """Load the promoted coefficient authority configuration."""

    return yaml.safe_load(AUTHORITY_PATH.read_text(encoding="utf-8"))


def _records_by_id(authority: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index coefficient authority records by their governed coefficient id."""

    return {record["coefficient_id"]: record for record in authority["records"]}


def _policies_by_id(authority: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index state-conditioned modifier policies by their governed policy id."""

    return {policy["policy_id"]: policy for policy in authority["modifier_policies"]}


def test_sequence8_specimen_declares_only_coefficient_modifier_authority() -> None:
    """The specimen opens Sequence 8 authority only and leaves Sequence 9 closed."""

    specimen = _load_specimen()

    assert specimen["sequence"] == "8"
    assert specimen["authority_class"] == "coefficient_modifier_authority"
    assert all("sequence9" not in authority.lower() for authority in specimen["source_authorities"])
    assert (
        "sequence9_downstream_capital_pre_deployment_logic" in specimen["closed_authority_classes"]
    )


def test_sequence8_specimen_coefficients_match_config_bounds_and_owner_stage() -> None:
    """Every specimen coefficient mirrors config authority and stays inside hard bounds."""

    specimen = _load_specimen()
    records = _records_by_id(_load_authority())

    for expected in specimen["coefficient_owner_stage_map"]:
        coefficient_id = expected["coefficient_id"]
        record = records[coefficient_id]

        assert record["owner_stage"] == expected["owner_stage"]
        assert record["surface_class"] == expected["surface_class"]
        assert record["baseline_value"] == expected["baseline_value"]
        assert record["runtime_mutable"] is expected["runtime_mutable"]
        assert record["hard_floor"] == expected["hard_floor"]
        assert record["hard_cap"] == expected["hard_cap"]

        if isinstance(record["baseline_value"], bool):
            assert record["hard_floor"] == "FALSE_ONLY"
            assert record["hard_cap"] == "TRUE_ONLY"
        else:
            assert record["hard_floor"] <= record["baseline_value"] <= record["hard_cap"]


def test_sequence8_specimen_modifier_effects_are_admitted_and_bounded() -> None:
    """Modifier policies may restrict admitted surfaces but may not widen authority."""

    specimen = _load_specimen()
    authority = _load_authority()
    records = _records_by_id(authority)
    policies = _policies_by_id(authority)

    for expected_policy in specimen["state_conditioned_modifiers"]:
        policy = policies[expected_policy["policy_id"]]
        assert policy["owner_stage"] == expected_policy["owner_stage"]
        assert policy["admitted_surfaces"] == expected_policy["admitted_surfaces"]

        effects_by_id = {effect["coefficient_id"]: effect for effect in policy["effects"]}
        for expected_effect in expected_policy["effects"]:
            coefficient_id = expected_effect["coefficient_id"]
            record = records[coefficient_id]
            effect = effects_by_id[coefficient_id]

            assert coefficient_id in policy["admitted_surfaces"]
            assert effect["transform_family"] == expected_effect["transform_family"]
            assert effect["effective_value"] == expected_effect["effective_value"]

            if isinstance(record["baseline_value"], bool):
                assert effect["effective_value"] is True
                assert expected_effect["direction"] == "protective_only"
            else:
                assert record["hard_floor"] <= effect["effective_value"] <= record["hard_cap"]
                assert effect["effective_value"] <= record["baseline_value"]
                assert expected_effect["direction"] == "restrictive_only"


def test_sequence8_specimen_review_horizon_and_promotion_are_non_deploying() -> None:
    """Review and promotion doctrine stays evidence-gated and separates paper from live."""

    specimen = _load_specimen()
    horizon = specimen["review_horizons"][0]
    doctrine = specimen["promotion_doctrine"]
    separation = doctrine["live_paper_historical_evaluation_separation"]

    assert horizon["review_trigger"] == "promotion_gate_only"
    assert set(horizon["minimum_evidence_modes"]) == {
        "historical_evaluation",
        "live_paper_evaluation",
    }
    assert horizon["forbidden_trigger"] == "single_backtest_or_live_paper_excitement"
    assert doctrine["evaluation_design"] == "champion_challenger_evaluation"
    assert doctrine["current_live_authority"] == "champion"
    assert doctrine["candidate_authority"] == "challenger_requires_promotion_gate"
    assert separation["direct_live_update_allowed"] is False
    assert separation["capital_deployment_allowed"] is False


def test_sequence8_specimen_keeps_closed_authority_classes_closed() -> None:
    """The test specimen does not smuggle downstream execution or capital decisions."""

    specimen = _load_specimen()
    closed = set(specimen["closed_authority_classes"])

    assert "downstream_capital_deployment" in closed
    assert "position_sizing" in closed
    assert "brokerage_execution" in closed
    assert "serial_candidate_selection_rewrite" in closed
    assert "parallel_risk_envelope_rewrite_outside_coefficient_modifier_seams" in closed
    assert "unbounded_live_self_tuning" in closed
