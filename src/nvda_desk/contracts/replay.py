from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ReplayPacketLineage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    packet_ids: list[str] = Field(default_factory=list)
    replay_run_id: str | None = None
