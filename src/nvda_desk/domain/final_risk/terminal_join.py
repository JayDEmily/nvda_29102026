"""Pure terminal-risk join helpers."""

from __future__ import annotations

from typing import Any

from nvda_desk.contracts.execution import ExecutionExpressionOutput
from nvda_desk.contracts.risk import (
    FinalRiskBranchJoinReceipt,
    FinalRiskJoinPolicy,
    FinalRiskJoinReceipt,
    ParallelRiskFinalRiskBranch,
    SerialFinalRiskBranch,
)


def _apply_legacy_expression_join(
    *, expression: ExecutionExpressionOutput, overlay_result: dict
) -> FinalRiskJoinReceipt:
    reasons = list(overlay_result.get("reasons", []))
    if overlay_result.get("action") == "stand_down":
        return FinalRiskJoinReceipt(
            action="stand_down", confidence_scalar=0.0, reasons=reasons
        )
    confidence = 1.0 if expression.lead_playbook_id else 0.0
    return FinalRiskJoinReceipt(
        action="proceed", confidence_scalar=confidence, reasons=reasons
    )


def _apply_branch_compatibility_join(
    *,
    serial_branch: SerialFinalRiskBranch | None,
    parallel_branch: ParallelRiskFinalRiskBranch | None,
    policy: FinalRiskJoinPolicy,
    receipt_id: str,
) -> FinalRiskBranchJoinReceipt:
    policy = FinalRiskJoinPolicy.model_validate(policy.model_dump(mode="python"))
    serial = (
        SerialFinalRiskBranch.model_validate(serial_branch.model_dump(mode="python"))
        if serial_branch is not None
        else None
    )
    parallel = (
        ParallelRiskFinalRiskBranch.model_validate(parallel_branch.model_dump(mode="python"))
        if parallel_branch is not None
        else None
    )
    missing: list[str] = []
    reasons: list[str] = []
    hard_blocks: list[str] = []
    cautions: list[str] = []
    if serial is None:
        missing.append("missing_serial_risk_authority")
    else:
        hard_blocks.extend(serial.hard_blocks)
        cautions.extend(serial.cautions)
        if serial.permission_state != "allow":
            reasons.append("serial_permission_blocked")
    if parallel is None:
        missing.append("missing_parallel_risk_authority")
    else:
        hard_blocks.extend(parallel.hard_blocks)
        cautions.extend(parallel.cautions)
    candidate_id: str | None = None
    if serial is not None and parallel is not None:
        if serial.candidate_id != parallel.candidate_id:
            reasons.append("candidate_identity_conflict")
        else:
            candidate_id = serial.candidate_id
    if hard_blocks:
        reasons.append("hard_block_present")
    if cautions and policy.cautions_prohibit:
        reasons.append("caution_prohibited")
    action = (
        "eligible_for_capital_assessment"
        if not (missing or reasons or hard_blocks)
        else "stand_down"
    )
    return FinalRiskBranchJoinReceipt(
        receipt_id=receipt_id,
        action=action,
        serial_branch_id=serial.branch_id if serial else None,
        parallel_branch_id=parallel.branch_id if parallel else None,
        candidate_id=candidate_id,
        hard_blocks=tuple(sorted(set(hard_blocks))),
        cautions=tuple(sorted(set(cautions))),
        missing_authority_reasons=tuple(sorted(set(missing))),
        reasons=tuple(sorted(set(reasons))),
        capital_authority_granted=False,
        execution_authority_granted=False,
    )


def apply_terminal_join(
    *,
    expression: ExecutionExpressionOutput | None = None,
    overlay_result: dict | None = None,
    serial_branch: SerialFinalRiskBranch | None = None,
    parallel_branch: ParallelRiskFinalRiskBranch | None = None,
    policy: FinalRiskJoinPolicy | None = None,
    receipt_id: str | None = None,
) -> FinalRiskJoinReceipt | FinalRiskBranchJoinReceipt:
    """Run either the retained expression adapter or the bounded branch adapter.

    The branch adapter is compatibility-only and does not fabricate canonical M05/M06
    lineage. Canonical K11/K14 authority remains in ``m09_capital_authority``.
    """

    branch_mode = any(
        value is not None
        for value in (serial_branch, parallel_branch, policy, receipt_id)
    )
    if branch_mode:
        if policy is None or receipt_id is None:
            raise TypeError("branch_join_policy_and_receipt_id_required")
        return _apply_branch_compatibility_join(
            serial_branch=serial_branch,
            parallel_branch=parallel_branch,
            policy=policy,
            receipt_id=receipt_id,
        )
    if expression is None or overlay_result is None:
        raise TypeError("legacy_expression_and_overlay_required")
    return _apply_legacy_expression_join(
        expression=expression,
        overlay_result=overlay_result,
    )
