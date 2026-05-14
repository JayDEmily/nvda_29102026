"""Shared contract primitives used across bounded runtime families."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RuntimeStage(StrEnum):
    """Governed runtime stage identifiers."""

    TEMPORAL = "temporal"
    REGIME = "regime"
    OPTIONS_FLOW = "options_flow"
    POSTURE = "posture"
    ELIGIBILITY = "eligibility"
    EXECUTION = "execution"
    FINAL_RISK = "final_risk"
    CAPITAL = "capital"
    DOWNSTREAM = "downstream"
    REVIEW = "review"


class PacketMetadata(BaseModel):
    """Shared packet metadata carried across native packet surfaces."""

    model_config = ConfigDict(extra="forbid")
    packet_id: str
    stage: RuntimeStage
    schema_name: str


class ReceiptMetadata(BaseModel):
    """Shared receipt metadata carried across native review and persistence surfaces."""

    model_config = ConfigDict(extra="forbid")
    receipt_id: str
    stage: RuntimeStage
    lineage_tags: list[str] = Field(default_factory=list)
