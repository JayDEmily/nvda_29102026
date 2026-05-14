"""Typed persistence record models for the rebuild-phase repository layer."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ExecutionRecordModel(BaseModel):
    """One persisted execution record."""

    model_config = ConfigDict(extra="forbid")
    record_id: str
    candidate_id: str | None = None
    stage: str = "execution"
    payload: dict = Field(default_factory=dict)


class PositionRecordModel(BaseModel):
    """One persisted canonical position record."""

    model_config = ConfigDict(extra="forbid")
    position_id: str
    symbol: str | None = None
    payload: dict = Field(default_factory=dict)


class CapitalStateRecordModel(BaseModel):
    """One persisted capital-state record."""

    model_config = ConfigDict(extra="forbid")
    snapshot_id: str
    payload: dict = Field(default_factory=dict)


class ReviewPacketRecordModel(BaseModel):
    """One persisted review packet record."""

    model_config = ConfigDict(extra="forbid")
    packet_id: str
    payload: dict = Field(default_factory=dict)
