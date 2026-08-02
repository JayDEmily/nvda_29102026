"""Typed ingress bundle admitted at the preparation-to-serial seam."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput


class CommonStageContext(BaseModel):
    """One bounded common authority reference shared by legacy stage carriers."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    context_id: str
    prepared_id: str
    prepared_fingerprint: str
    input_schema_versions: dict[str, str]
    preparation_policy_version: str
    temporal_reference_id: str
    completeness_state: Literal["complete", "degraded"]
    resolution_receipt_ids: tuple[str, ...] = ()


class StageInputBundle(BaseModel):
    """Typed stage-input bundle emitted by cognition ingress."""

    model_config = ConfigDict(extra="forbid")
    common_context: CommonStageContext | None = None
    temporal: TemporalContextInput
    regime: MarketRegimeContextInput
    options_flow: OptionsFlowContextInput

    @model_validator(mode="after")
    def _validate_common_context_refs(self) -> "StageInputBundle":
        references = (
            self.temporal.common_context_ref,
            self.regime.common_context_ref,
            self.options_flow.common_context_ref,
        )
        if self.common_context is None:
            if any(reference is not None for reference in references):
                raise ValueError("common_context reference requires common_context authority")
            return self
        if any(reference != self.common_context.context_id for reference in references):
            raise ValueError("common_context reference mismatch")
        return self

    def as_mapping(self) -> dict[str, object]:
        """Return a stage-name keyed mapping over the typed input carriers."""

        return {
            "temporal": self.temporal,
            "regime": self.regime,
            "options_flow": self.options_flow,
        }
