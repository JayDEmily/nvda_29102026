"""Evaluate bounded playbook eligibility."""

from __future__ import annotations

from nvda_desk.config.playbook_registry import PlaybookRegistryDocument
from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.posture import PostureRiskOutput
from nvda_desk.domain.eligibility.playbook_compilation import compile_playbook_eligibility


def evaluate_playbook_eligibility(
    *,
    posture: PostureRiskOutput,
    candidate_family_ids: list[str] | None = None,
    registry: PlaybookRegistryDocument | None = None,
) -> PlaybookEligibilityOutput:
    """Return one bounded playbook eligibility output."""
    return compile_playbook_eligibility(
        permission_state=posture.permission_state,
        candidate_family_ids=candidate_family_ids,
        registry=registry,
    )
