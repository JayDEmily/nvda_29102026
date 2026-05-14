"""Compatibility wrapper for workbook-owned eligibility service path."""

from __future__ import annotations

from nvda_desk.contracts.eligibility import PlaybookEligibilityOutput
from nvda_desk.contracts.posture import PostureRiskOutput
from nvda_desk.services.playbook_eligibility_service import PlaybookEligibilityService


class EligibilityService(PlaybookEligibilityService):
    """Workbook-owned alias of the bounded playbook eligibility coordinator."""

    def evaluate(
        self, *, posture: PostureRiskOutput, candidate_family_ids: list[str] | None = None
    ) -> PlaybookEligibilityOutput:
        return super().evaluate(posture=posture, candidate_family_ids=candidate_family_ids)
