"""Pure playbook admissibility compilation."""

from __future__ import annotations

from nvda_desk.config.playbook_registry import (
    PlaybookRegistryDocument,
    build_playbook_metadata_receipts,
)
from nvda_desk.contracts.eligibility import (
    EligibilityAdmissibilitySurface,
    PlaybookEligibilityOutput,
)
from nvda_desk.contracts.posture import PermissionState


def _unique_in_order(values: list[str] | tuple[str, ...]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def compile_playbook_eligibility(
    *,
    permission_state: PermissionState,
    candidate_family_ids: list[str] | None = None,
    registry: PlaybookRegistryDocument | None = None,
) -> PlaybookEligibilityOutput:
    """Return one bounded eligibility surface from permission state and playbook inputs."""

    families = _unique_in_order(candidate_family_ids or [])
    no_trade_reasons: list[str] = []
    registry_id = registry.registry_id if registry is not None else None

    if registry is not None and not families:
        families = _unique_in_order(
            [playbook.setup_family for playbook in registry.enabled_playbooks()]
        )

    if permission_state == PermissionState.BLOCK:
        no_trade_reasons.append("permission_block")
        return PlaybookEligibilityOutput(
            admissibility_surface=EligibilityAdmissibilitySurface(
                permission_state=permission_state,
                no_trade_reasons=no_trade_reasons,
            ),
            active_family_ids=[],
            active_setup_variant_ids=[],
            registry_id=registry_id,
            playbook_metadata_receipts=[],
        )

    active_setup_variant_ids: list[str]
    if registry is None:
        active_setup_variant_ids = [f"{family}.baseline" for family in families]
        receipts = []
    else:
        receipts = build_playbook_metadata_receipts(registry, setup_family_ids=families)
        active_setup_variant_ids = _unique_in_order(
            [receipt.setup_variant_id for receipt in receipts]
        )
        families = _unique_in_order([receipt.setup_family for receipt in receipts])

    return PlaybookEligibilityOutput(
        admissibility_surface=EligibilityAdmissibilitySurface(
            permission_state=permission_state,
            no_trade_reasons=no_trade_reasons,
        ),
        active_family_ids=families,
        active_setup_variant_ids=active_setup_variant_ids,
        registry_id=registry_id,
        playbook_metadata_receipts=receipts,
    )
