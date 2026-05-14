from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BoundedTraceRunResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario_id: str
    permission_state: str = "unknown"
    active_playbook_ids: list[str] = Field(default_factory=list)
    final_risk_action: str = "unknown"
    capital_deployment_action: str = "unknown"
    summary: str | None = None


class BoundedTraceReviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    runs: list[BoundedTraceRunResult] = Field(default_factory=list)
    narrative_summary: str | None = None


class BoundedTraceScenario(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario_id: str
    description: str | None = None


class BoundedTraceFixturePack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario_ids: list[str] = Field(default_factory=list)
    scenarios: list[BoundedTraceScenario] = Field(default_factory=list)
