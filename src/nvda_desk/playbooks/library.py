"""Bounded playbook-library selection helpers."""

from __future__ import annotations

from nvda_desk.config.playbook_registry import (
    PlaybookRegistryDocument,
    build_playbook_metadata_receipts,
)
from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.playbook import PlaybookMetadataReceipt
from nvda_desk.contracts.posture import PermissionState


def select_playbook_metadata_receipts(
    *, registry: PlaybookRegistryDocument, eligibility: PlaybookEligibilityOutput
) -> list[PlaybookMetadataReceipt]:
    """Select playbook metadata receipts using only the declared eligibility carrier."""

    if eligibility.admissibility_surface.permission_state == PermissionState.BLOCK:
        return []
    return build_playbook_metadata_receipts(
        registry,
        setup_family_ids=eligibility.active_family_ids,
        setup_variant_ids=eligibility.active_setup_variant_ids,
    )
