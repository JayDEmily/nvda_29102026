"""Configuration-surface contracts.

These payloads expose coefficient groups, strategy variants, and the Gate 60/61
authority packets that fence lawful mutable surfaces away from prohibited or
review-only policy language.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from nvda_desk.schemas.calibration import WalkForwardHarnessAuthorityPacket
from nvda_desk.schemas.events import (
    EventIngestionAuthorityPacket,
    EventStoreAuthorityPacket,
    LiveEventRichnessAuthorityPacket,
)
from nvda_desk.schemas.market import (
    PrecursorStitchingAuthorityPacket,
    PrecursorUniverseAuthorityPacket,
)
from nvda_desk.schemas.risk import PhaseCarryoverPolicyAuthorityPacket
from nvda_desk.schemas.session_clock import DeskCalendarAuthorityPacket
from nvda_desk.schemas.state_policy import (
    CandidateGovernanceAuthorityPacket,
    EventOptionsStressAuthorityPacket,
    ModifierControlLawAuthorityPacket,
    NonActionAuthorityPacket,
    ReviewEligibilityAuthorityPacket,
    StabilityAuthorityPacket,
    StatePolicyAuthorityPacket,
)
from nvda_desk.schemas.temporal_surface import EventWindowAuthorityPacket


class CoefficientGroupParameterPayload(BaseModel):
    """One parameter inside a coefficient group."""

    name: str = Field(min_length=1)
    value: float | int | str | bool
    test_min: float | int | None = None
    test_max: float | int | None = None
    step: float | int | None = None
    notes: str | None = None


class CoefficientGroupPayload(BaseModel):
    """One configurable coefficient group and its supported sandbox overrides."""

    key: str = Field(min_length=1)
    layer: str = Field(min_length=1)
    module: str = Field(min_length=1)
    weight: float = Field(ge=0)
    enabled: bool
    parameters: list[CoefficientGroupParameterPayload] = Field(default_factory=list)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)


class CoefficientGroupListResponse(BaseModel):
    """Response wrapper for configured coefficient groups."""

    groups: list[CoefficientGroupPayload]


class StrategyVariantSummaryPayload(BaseModel):
    """Compact summary for one named strategy variant."""

    name: str = Field(min_length=1)
    description: str
    weight_override_keys: list[str] = Field(default_factory=list)
    coefficient_override_keys: list[str] = Field(default_factory=list)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)


class StrategyVariantListResponse(BaseModel):
    """Response wrapper for strategy-variant summaries."""

    variants: list[StrategyVariantSummaryPayload]


class StrategyVariantPayload(BaseModel):
    """Detailed strategy-variant surface including explicit override buckets."""

    name: str = Field(min_length=1)
    description: str
    enabled_module_counts: dict[str, int] = Field(default_factory=dict)
    weight_overrides: dict[str, float] = Field(default_factory=dict)
    coefficient_overrides: dict[str, dict[str, float | int | str | bool]] = Field(
        default_factory=dict
    )
    runtime_overrides: dict[str, object] = Field(default_factory=dict)
    supported_sandbox_overrides: list[str] = Field(default_factory=list)


class DeskCalendarAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 66 desk-calendar packet."""

    authority: DeskCalendarAuthorityPacket


class PrecursorUniverseAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 68 precursor-universe packet."""

    authority: PrecursorUniverseAuthorityPacket


class PrecursorStitchingAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 75 precursor-stitching packet."""

    authority: PrecursorStitchingAuthorityPacket


class PhaseCarryoverPolicyAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 69 phase/carry packet."""

    authority: PhaseCarryoverPolicyAuthorityPacket


class EventWindowAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 67 event-window packet."""

    authority: EventWindowAuthorityPacket


class StatePolicyAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 60 state-policy packet."""

    authority: StatePolicyAuthorityPacket


class NonActionAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 61 non-action authority packet."""

    authority: NonActionAuthorityPacket


class StabilityAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 62 stability authority packet."""

    authority: StabilityAuthorityPacket


class ReviewEligibilityAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 63 review-eligibility packet."""

    authority: ReviewEligibilityAuthorityPacket


class EventOptionsStressAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 70 event/options-stress packet."""

    authority: EventOptionsStressAuthorityPacket


class ModifierControlLawAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 71 modifier-control-law packet."""

    authority: ModifierControlLawAuthorityPacket


class EventIngestionAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 72 event-ingestion packet."""

    authority: EventIngestionAuthorityPacket


class EventStoreAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 73 event-store/query packet."""

    authority: EventStoreAuthorityPacket


class LiveEventRichnessAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 74 live-event-richness packet."""

    authority: LiveEventRichnessAuthorityPacket


class CandidateGovernanceAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 64 candidate-governance packet."""

    authority: CandidateGovernanceAuthorityPacket


class WalkForwardHarnessAuthorityResponse(BaseModel):
    """Future config/API hook for the frozen Gate 79 walk-forward harness packet."""

    authority: WalkForwardHarnessAuthorityPacket
