"""Checkpoint helpers for preserved downstream seam boundaries.

Purpose:
    Define deterministic checkpoint names and bounded observation helpers for
    the preserved downstream seam boundaries hardened during the Gate 297
    surgery continuation.
Inputs:
    Stable checkpoint names plus bounded input and output snapshots.
Outputs:
    `CheckpointObservation` records suitable for attachment to downstream
    decisions and review-safe receipts.
Side Effects:
    None. Callers decide where checkpoint observations are stored.
Failure Modes:
    Pydantic validation raises when a checkpoint observation is malformed.
Checkpoints:
    The helpers in this module are used by capital-deployment authority,
    downstream opening shells, and review packet preserved-seam carriage.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from nvda_desk.schemas.checkpoints import CheckpointObservation

CHECKPOINT_CDA_DECISION_OBSERVED = (
    "downstream_seam.capital_deployment_authority.decision_observed"
)
CHECKPOINT_OPENING_AUTHORISATION_OBSERVED = (
    "downstream_seam.opening_authorisation.decision_observed"
)
CHECKPOINT_PLACEMENT_HANDOFF_OBSERVED = (
    "downstream_seam.placement_handoff.reservation_observed"
)
CHECKPOINT_REVIEW_PACKET_PRESERVED_SEAM_OBSERVED = (
    "downstream_seam.review_packet.preserved_seam_observed"
)


def checkpoint_observation(
    *,
    checkpoint_name: str,
    input_snapshot: dict[str, Any],
    output_snapshot: dict[str, Any],
    timestamp: datetime | None = None,
) -> CheckpointObservation:
    """Build one bounded checkpoint observation record for downstream seams."""

    return CheckpointObservation(
        checkpoint_name=checkpoint_name,
        timestamp=(datetime.now(UTC) if timestamp is None else timestamp),
        input_snapshot=input_snapshot,
        output_snapshot=output_snapshot,
    )
