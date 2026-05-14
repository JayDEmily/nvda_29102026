from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .playbook import PlaybookMetadataReceipt
from .posture import PermissionState


class EligibilityAdmissibilitySurface(BaseModel):
    model_config = ConfigDict(extra="forbid")
    permission_state: PermissionState
    no_trade_reasons: list[str] = Field(default_factory=list)


class PlaybookEligibilityOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    admissibility_surface: EligibilityAdmissibilitySurface
    active_family_ids: list[str] = Field(default_factory=list)
    active_setup_variant_ids: list[str] = Field(default_factory=list)
    registry_id: str | None = None
    playbook_metadata_receipts: list[PlaybookMetadataReceipt] = Field(default_factory=list)
