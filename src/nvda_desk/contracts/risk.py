from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FinalRiskJoinReceipt(BaseModel):
    """Legacy confidence-bearing receipt retained for pre-M09 callers only."""

    model_config = ConfigDict(extra="forbid")
    action: str
    confidence_scalar: float = 0.0
    reasons: list[str] = Field(default_factory=list)


class SerialFinalRiskBranch(BaseModel):
    """Bounded compatibility carrier for the legacy C-036 serial branch."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    branch_id: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)
    execution_expression_id: str = Field(min_length=1)
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    permission_state: Literal["allow", "blocked"]
    hard_blocks: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    policy_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_branch(self) -> "SerialFinalRiskBranch":
        if self.hard_blocks != tuple(sorted(set(self.hard_blocks))):
            raise ValueError("serial_hard_blocks_must_be_canonical")
        if self.cautions != tuple(sorted(set(self.cautions))):
            raise ValueError("serial_cautions_must_be_canonical")
        if self.permission_state == "blocked" and not self.hard_blocks:
            raise ValueError("blocked_serial_branch_requires_hard_block")
        if self.permission_state == "allow" and self.hard_blocks:
            raise ValueError("allowed_serial_branch_cannot_carry_hard_block")
        return self


class ParallelRiskFinalRiskBranch(BaseModel):
    """Bounded compatibility carrier for the legacy C-036 parallel branch."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    branch_id: str = Field(min_length=1)
    candidate_id: str = Field(min_length=1)
    packet_id: str = Field(min_length=1)
    semantic_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    hard_blocks: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    evidence_limitations: tuple[str, ...] = ()
    policy_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_branch(self) -> "ParallelRiskFinalRiskBranch":
        for field_name in ("hard_blocks", "cautions", "evidence_limitations"):
            value = getattr(self, field_name)
            if value != tuple(sorted(set(value))):
                raise ValueError(f"parallel_{field_name}_must_be_canonical")
        return self


class FinalRiskJoinPolicy(BaseModel):
    """Closed compatibility policy for the legacy C-036 branch join."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    policy_version: Literal["final-join-v1"] = "final-join-v1"
    cautions_prohibit: bool = False


class FinalRiskBranchJoinReceipt(BaseModel):
    """Non-canonical compatibility result; it grants no capital or execution authority."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str = Field(min_length=1)
    action: Literal["eligible_for_capital_assessment", "stand_down"]
    serial_branch_id: str | None
    parallel_branch_id: str | None
    candidate_id: str | None
    hard_blocks: tuple[str, ...] = ()
    cautions: tuple[str, ...] = ()
    missing_authority_reasons: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    capital_authority_granted: Literal[False] = False
    execution_authority_granted: Literal[False] = False

    @model_validator(mode="after")
    def _validate_receipt(self) -> "FinalRiskBranchJoinReceipt":
        for field_name in (
            "hard_blocks",
            "cautions",
            "missing_authority_reasons",
            "reasons",
        ):
            value = getattr(self, field_name)
            if value != tuple(sorted(set(value))):
                raise ValueError(f"{field_name}_must_be_canonical")
        if self.action == "eligible_for_capital_assessment" and (
            self.hard_blocks or self.missing_authority_reasons or self.reasons
        ):
            raise ValueError("eligible_compatibility_join_cannot_carry_prohibiting_evidence")
        if self.action == "stand_down" and not (
            self.hard_blocks or self.missing_authority_reasons or self.reasons
        ):
            raise ValueError("stand_down_compatibility_join_requires_reason")
        return self
