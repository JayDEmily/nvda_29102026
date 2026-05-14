"""Coordinate bounded playbook eligibility evaluation."""

from __future__ import annotations

from nvda_desk.cognition.serial.eligibility import evaluate_playbook_eligibility
from nvda_desk.config.playbook_registry import PlaybookRegistryDocument
from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.posture import PostureRiskOutput


class PlaybookEligibilityService:
    """Coordinate eligibility evaluation without absorbing domain logic."""

    def evaluate(
        self,
        *,
        posture: PostureRiskOutput,
        candidate_family_ids: list[str] | None = None,
        registry: PlaybookRegistryDocument | None = None,
    ) -> PlaybookEligibilityOutput:
        return evaluate_playbook_eligibility(
            posture=posture,
            candidate_family_ids=candidate_family_ids,
            registry=registry,
        )
