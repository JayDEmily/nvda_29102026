from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from nvda_desk.domain.session_clock import SessionClockPhase


class AllocationCandidateInput(BaseModel):
    module_id: str = Field(min_length=1)
    module_name: str = Field(min_length=1)
    config_key: str | None = Field(default=None, min_length=1)
    base_weight: float = Field(default=1.0, gt=0, le=10)
    min_allocation_pct: float = Field(default=0.0, ge=0, le=100)
    max_allocation_pct: float = Field(default=100.0, ge=0, le=100)


class ModuleRegimeCapitalAllocationInput(BaseModel):
    requested_at: datetime
    total_capital: float = Field(gt=0)
    session_phase: SessionClockPhase
    vix_level: float = Field(ge=0, le=200)
    vvix_level: float = Field(ge=0, le=500)
    strategy_variant_name: str | None = Field(default=None, min_length=1)
    coefficient_group_name: str | None = Field(default=None, min_length=1)
    candidates: list[AllocationCandidateInput] = Field(min_length=1, max_length=24)


class ModuleCapitalAllocation(BaseModel):
    module_id: str
    module_name: str
    allocation_pct: float = Field(ge=0, le=100)
    allocated_capital: float = Field(ge=0)
    quality_score: float = Field(ge=0, le=1)
    regime_fit_score: float = Field(ge=0, le=1)
    reasons: list[str] = Field(default_factory=list)


class ModuleRegimeCapitalAllocationOutput(BaseModel):
    requested_at: datetime
    total_capital: float = Field(gt=0)
    cash_reserve_pct: float = Field(ge=0, le=100)
    cash_reserve_capital: float = Field(ge=0)
    allocations: list[ModuleCapitalAllocation]
