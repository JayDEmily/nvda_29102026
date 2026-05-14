from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

WriteStatus = Literal["disabled", "persisted", "write_failed", "build_failed"]


class OptionsFlowHistoryObservationRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    symbol: str
    observed_at: datetime
    chain_ts: datetime
    derived_state: dict = Field(default_factory=dict)
    partiality_state: str = "complete"
    lineage: dict = Field(default_factory=dict)
    lineage_keys: list[str] = Field(default_factory=list)


class OptionsFlowHistoryWriteResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: WriteStatus
    note: str | None = None
    persisted: dict | None = None
    persisted_id: int | None = None
