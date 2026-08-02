"""Serial desk-cognition spine contract and validation helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from types import MappingProxyType
from typing import Any

SERIAL_SPINE_STAGE_ORDER: tuple[str, ...] = (
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
)

SERIAL_STAGE_DEPENDENCIES: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {
        "temporal": (),
        "regime": (),
        "options_flow": (),
        "posture": ("regime",),
        "eligibility": ("posture",),
        "execution": ("temporal", "regime", "options_flow", "posture", "eligibility"),
    }
)

SERIAL_STAGE_OUTPUT_SCHEMAS: Mapping[str, str] = MappingProxyType(
    {
        "temporal": "TemporalContextOutput",
        "regime": "MarketRegimeContextOutput",
        "options_flow": "OptionsFlowContextOutput",
        "posture": "PostureRiskOutput",
        "eligibility": "PlaybookEligibilityOutput",
        "execution": "ExecutionExpressionOutput",
    }
)

SERIAL_SPINE_PROHIBITED_AUTHORITIES: tuple[str, ...] = (
    "parallel_risk_lane",
    "capital_deployment_authority",
    "live_position_management",
    "order_placement",
    "position_sizing",
)

SERIAL_STAGE_LINEAGE_TAGS: tuple[str, ...] = (
    "serial_spine_candidate_formation",
    "before_independent_lane",
    "pre_capital_deployment",
    "no_live_inventory_authority",
)


def validate_serial_stage_order(stage_order: Sequence[str]) -> tuple[str, ...]:
    """Return the stage order after rejecting missing, duplicate, or reordered stages."""

    observed = tuple(stage_order)
    if len(set(observed)) != len(observed):
        raise ValueError("serial stage order contains duplicate stages")
    expected = SERIAL_SPINE_STAGE_ORDER
    if observed != expected:
        raise ValueError(
            "serial stage order must be " + ",".join(expected) + "; observed " + ",".join(observed)
        )
    return observed


def validate_serial_stage_dependencies(
    stage_order: Sequence[str], dependencies: Mapping[str, Sequence[str]]
) -> dict[str, tuple[str, ...]]:
    """Validate that stage dependencies are known and never point forward."""

    ordered = validate_serial_stage_order(stage_order)
    dependency_keys = set(dependencies)
    expected_keys = set(ordered)
    if dependency_keys != expected_keys:
        missing = sorted(expected_keys - dependency_keys)
        extra = sorted(dependency_keys - expected_keys)
        raise ValueError(f"serial dependencies mismatch missing={missing} extra={extra}")

    index = {stage_name: pos for pos, stage_name in enumerate(ordered)}
    normalised: dict[str, tuple[str, ...]] = {}
    for stage_name in ordered:
        stage_dependencies = tuple(dependencies[stage_name])
        unknown = [name for name in stage_dependencies if name not in index]
        if unknown:
            raise ValueError(f"serial stage {stage_name} has unknown dependencies {unknown}")
        forward = [name for name in stage_dependencies if index[name] >= index[stage_name]]
        if forward:
            raise ValueError(f"serial stage {stage_name} has forward dependencies {forward}")
        normalised[stage_name] = stage_dependencies
    return normalised


def serial_spine_contract() -> dict[str, Any]:
    """Return a copy-safe trace contract for the serial candidate-formation spine."""

    dependencies = validate_serial_stage_dependencies(
        SERIAL_SPINE_STAGE_ORDER, SERIAL_STAGE_DEPENDENCIES
    )
    return {
        "architecture_row": "5.7 Serial desk-cognition spine",
        "owner": "serial desk-cognition authority",
        "purpose": "ordered candidate formation through six serial runtime stages",
        "stage_order": list(SERIAL_SPINE_STAGE_ORDER),
        "stage_dependencies": {
            stage_name: list(stage_dependencies)
            for stage_name, stage_dependencies in dependencies.items()
        },
        "stage_output_schemas": dict(SERIAL_STAGE_OUTPUT_SCHEMAS),
        "lineage_tags": list(SERIAL_STAGE_LINEAGE_TAGS),
        "prohibited_authorities": list(SERIAL_SPINE_PROHIBITED_AUTHORITIES),
        "boundary": "forms candidate material only; does not allocate capital, place orders, or manage live inventory",
    }


def copy_serial_spine_contract() -> dict[str, Any]:
    """Return a defensive copy of the serial spine trace contract."""

    return deepcopy(serial_spine_contract())
