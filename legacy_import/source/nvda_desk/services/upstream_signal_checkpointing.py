"""Checkpoint helpers for the upstream signal completion tranche.

Purpose:
    Define deterministic checkpoint names, bounded observation helpers, and
    deterministic exceptions for upstream signal promotion boundaries.
Inputs:
    Stable checkpoint names plus bounded input and output snapshots.
Outputs:
    `CheckpointObservation` records or `UpstreamSignalCheckpointError`
    exceptions carrying the same structured observation.
Side Effects:
    None. Callers decide where checkpoint observations are stored.
Failure Modes:
    `UpstreamSignalCheckpointError` is raised when a checkpoint detects a
    prohibited transition or malformed boundary state.
Checkpoints:
    The helpers in this module are used by upstream signal regime promotion,
    participation-baseline reconstruction, and raw-to-cognition wiring.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from nvda_desk.schemas.checkpoints import CheckpointObservation

CHECKPOINT_REGIME_COMPLETE_REQUIRES_BREADTH_CONCENTRATION = (
    "upstream_signal.regime_packet.complete_requires_breadth_concentration"
)
CHECKPOINT_PARTICIPATION_RATIO_POSITIVE_WHEN_PRESENT = (
    "upstream_signal.participation_baseline.relative_volume_ratio_positive_when_present"
)
CHECKPOINT_PARTICIPATION_AVAILABLE_REQUIRES_BASELINE_VOLUME = (
    "upstream_signal.participation_baseline.available_requires_baseline_volume"
)
CHECKPOINT_REGIME_PACKET_CAPTURE_OBSERVED = (
    "upstream_signal.regime_packet.capture_observed"
)
CHECKPOINT_PARTICIPATION_PROXY_BASELINE_OBSERVED = (
    "upstream_signal.participation_baseline.proxy_baseline_observed"
)
CHECKPOINT_CHAIN_TO_COGNITION_REGIME_MAPPING = (
    "upstream_signal.chain_to_cognition.regime_mapping_observed"
)
CHECKPOINT_CHAIN_TO_COGNITION_PARTICIPATION_MAPPING = (
    "upstream_signal.chain_to_cognition.participation_mapping_observed"
)


class UpstreamSignalCheckpointError(RuntimeError):
    """Deterministic upstream checkpoint failure carrying structured evidence.

    Purpose:
        Expose one stable exception surface for checkpoint failures in the
        upstream signal completion tranche.
    Inputs:
        A checkpoint name, a short failure detail, and bounded input/output
        snapshots.
    Outputs:
        A RuntimeError subclass with an attached `CheckpointObservation`.
    Side Effects:
        None.
    Failure Modes:
        Always raises when instantiated through `raise_checkpoint_failure`.
    Checkpoints:
        This exception is the failure carriage for all checkpoint-enabled
        upstream signal boundaries.
    """

    def __init__(
        self,
        *,
        checkpoint_name: str,
        detail: str,
        input_snapshot: dict[str, Any],
        output_snapshot: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.checkpoint_name = checkpoint_name
        self.detail = detail
        self.observation = CheckpointObservation(
            checkpoint_name=checkpoint_name,
            timestamp=(datetime.now(UTC) if timestamp is None else timestamp),
            input_snapshot=input_snapshot,
            output_snapshot={} if output_snapshot is None else output_snapshot,
        )
        super().__init__(f"CHECKPOINT_FAILURE:{checkpoint_name}:{detail}")


def checkpoint_observation(
    *,
    checkpoint_name: str,
    input_snapshot: dict[str, Any],
    output_snapshot: dict[str, Any],
    timestamp: datetime | None = None,
) -> CheckpointObservation:
    """Build one bounded checkpoint observation record.

    Purpose:
        Give checkpoint-enabled code one stable helper for creating structured
        observations without inventing ad hoc shapes.
    Inputs:
        A checkpoint name plus bounded input/output snapshots.
    Outputs:
        `CheckpointObservation`.
    Side Effects:
        None.
    Failure Modes:
        Validation fails if the observation is malformed.
    Checkpoints:
        The emitted observation is itself the trace output required by the
        checkpoint-integrity extension.
    """

    return CheckpointObservation(
        checkpoint_name=checkpoint_name,
        timestamp=(datetime.now(UTC) if timestamp is None else timestamp),
        input_snapshot=input_snapshot,
        output_snapshot=output_snapshot,
    )


def append_unique_observation(
    observations: list[CheckpointObservation],
    observation: CheckpointObservation,
) -> None:
    """Append one checkpoint observation if the same bounded fact is absent.

    Purpose:
        Prevent repeated calls from silently duplicating identical checkpoint
        observations on mutable packets.
    Inputs:
        An observation list and one candidate observation.
    Outputs:
        The list is mutated only when the observation is new.
    Side Effects:
        May append one observation to the supplied list.
    Failure Modes:
        None.
    Checkpoints:
        Supports stable checkpoint trace carriage on mutable packets.
    """

    key = (
        observation.checkpoint_name,
        observation.timestamp,
        observation.input_snapshot,
        observation.output_snapshot,
    )
    for existing in observations:
        existing_key = (
            existing.checkpoint_name,
            existing.timestamp,
            existing.input_snapshot,
            existing.output_snapshot,
        )
        if existing_key == key:
            return
    observations.append(observation)


def raise_checkpoint_failure(
    *,
    checkpoint_name: str,
    detail: str,
    input_snapshot: dict[str, Any],
    output_snapshot: dict[str, Any] | None = None,
    timestamp: datetime | None = None,
) -> None:
    """Raise a deterministic upstream checkpoint failure.

    Purpose:
        Enforce the checkpoint-integrity rule without using Python `assert`.
    Inputs:
        A checkpoint name, a short failure detail, and bounded snapshots.
    Outputs:
        Never returns.
    Side Effects:
        Raises `UpstreamSignalCheckpointError`.
    Failure Modes:
        Always raises.
    Checkpoints:
        This helper is the standard failure path for upstream signal tranche
        checkpoints.
    """

    raise UpstreamSignalCheckpointError(
        checkpoint_name=checkpoint_name,
        detail=detail,
        input_snapshot=input_snapshot,
        output_snapshot=output_snapshot,
        timestamp=timestamp,
    )
