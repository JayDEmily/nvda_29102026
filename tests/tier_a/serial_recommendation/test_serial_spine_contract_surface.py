from __future__ import annotations

import pytest

from nvda_desk.contracts.serial_spine import (
    SERIAL_SPINE_PROHIBITED_AUTHORITIES,
    SERIAL_SPINE_STAGE_ORDER,
    SERIAL_STAGE_DEPENDENCIES,
    copy_serial_spine_contract,
    serial_spine_contract,
    validate_serial_stage_dependencies,
    validate_serial_stage_order,
)


def test_serial_spine_contract_preserves_governed_six_stage_order() -> None:
    contract = serial_spine_contract()

    assert contract["architecture_row"] == "5.7 Serial desk-cognition spine"
    assert contract["owner"] == "serial desk-cognition authority"
    assert contract["stage_order"] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
        "execution",
    ]
    assert tuple(contract["stage_order"]) == SERIAL_SPINE_STAGE_ORDER


def test_serial_stage_order_rejects_missing_duplicate_unknown_or_reordered_stages() -> None:
    assert validate_serial_stage_order(SERIAL_SPINE_STAGE_ORDER) == SERIAL_SPINE_STAGE_ORDER

    invalid_orders = [
        ("temporal", "regime", "options_flow", "posture", "eligibility"),
        ("temporal", "regime", "options_flow", "posture", "eligibility", "eligibility"),
        ("temporal", "options_flow", "regime", "posture", "eligibility", "execution"),
        ("temporal", "regime", "options_flow", "posture", "eligibility", "capital"),
    ]
    for invalid_order in invalid_orders:
        with pytest.raises(ValueError):
            validate_serial_stage_order(invalid_order)


def test_serial_stage_dependencies_are_known_and_never_point_forward() -> None:
    dependencies = validate_serial_stage_dependencies(
        SERIAL_SPINE_STAGE_ORDER, SERIAL_STAGE_DEPENDENCIES
    )

    assert dependencies["temporal"] == ()
    assert dependencies["regime"] == ()
    assert dependencies["options_flow"] == ()
    assert dependencies["posture"] == ("regime",)
    assert dependencies["eligibility"] == ("posture",)
    assert dependencies["execution"] == (
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
    )

    with pytest.raises(ValueError, match="forward dependencies"):
        validate_serial_stage_dependencies(
            SERIAL_SPINE_STAGE_ORDER,
            {**SERIAL_STAGE_DEPENDENCIES, "regime": ("execution",)},
        )

    with pytest.raises(ValueError, match="unknown dependencies"):
        validate_serial_stage_dependencies(
            SERIAL_SPINE_STAGE_ORDER,
            {**SERIAL_STAGE_DEPENDENCIES, "posture": ("ghost_stage",)},
        )


def test_serial_spine_contract_is_trace_only_and_excludes_capital_live_inventory_authority() -> (
    None
):
    contract = serial_spine_contract()

    for authority in (
        "capital_deployment_authority",
        "live_position_management",
        "order_placement",
        "position_sizing",
    ):
        assert authority in contract["prohibited_authorities"]
        assert authority in SERIAL_SPINE_PROHIBITED_AUTHORITIES

    assert "capital" not in contract["stage_order"]
    assert "live_inventory" not in contract["stage_order"]
    assert all("parallel" not in stage_name for stage_name in contract["stage_order"])
    assert "does not allocate capital" in contract["boundary"]


def test_serial_spine_contract_readback_is_copy_safe() -> None:
    first = copy_serial_spine_contract()
    first["stage_order"].append("mutated")
    first["stage_dependencies"]["execution"].append("mutated")

    second = copy_serial_spine_contract()
    assert second["stage_order"] == list(SERIAL_SPINE_STAGE_ORDER)
    assert second["stage_dependencies"]["execution"] == [
        "temporal",
        "regime",
        "options_flow",
        "posture",
        "eligibility",
    ]


def test_serial_stage_dependencies_reject_self_dependency() -> None:
    with pytest.raises(ValueError, match="forward dependencies"):
        validate_serial_stage_dependencies(
            SERIAL_SPINE_STAGE_ORDER,
            {**SERIAL_STAGE_DEPENDENCIES, "posture": ("posture",)},
        )


def test_serial_spine_contract_copy_boundary_covers_schema_and_authority_lists() -> None:
    first = copy_serial_spine_contract()
    first["prohibited_authorities"].append("mutated_capital_authority")
    first["stage_output_schemas"]["execution"] = "CapitalDeploymentDecision"

    second = copy_serial_spine_contract()
    assert second["prohibited_authorities"] == list(SERIAL_SPINE_PROHIBITED_AUTHORITIES)
    assert second["stage_output_schemas"]["execution"] == "ExecutionExpressionOutput"
