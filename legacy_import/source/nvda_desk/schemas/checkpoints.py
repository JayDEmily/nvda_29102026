"""Checkpoint observation contracts for checkpoint-enabled runtime boundaries.

Purpose:
    Provide one bounded, test-accessible observation surface for named
    checkpoints introduced after the checkpoint-integrity extension.
Inputs:
    Structured checkpoint metadata plus bounded input and output snapshots.
Outputs:
    `CheckpointObservation` records that can be attached to packets or runtime
    outputs without creating hidden logging-only behaviour.
Side Effects:
    None. This module defines typed contracts only.
Failure Modes:
    Pydantic validation raises when required checkpoint fields are missing or
    malformed.
Checkpoints:
    This module is itself the typed carriage surface for checkpoint-enabled
    boundaries and therefore does not define additional runtime checkpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CheckpointObservation(BaseModel):
    """Structured observation emitted by a named checkpoint.

    Purpose:
        Preserve bounded, test-accessible evidence that a checkpoint executed
        and what truth it observed.
    Inputs:
        A stable checkpoint name, one timestamp, and bounded input/output
        snapshots.
    Outputs:
        A typed observation record.
    Side Effects:
        None.
    Failure Modes:
        Validation fails if required fields are absent or snapshots are not
        mapping-like JSON-compatible structures.
    Checkpoints:
        This class is the canonical typed output for checkpoint-enabled
        boundaries in the upstream signal tranche.
    """

    model_config = ConfigDict(extra="forbid")

    checkpoint_name: str
    timestamp: datetime
    input_snapshot: dict[str, Any] = Field(default_factory=dict)
    output_snapshot: dict[str, Any] = Field(default_factory=dict)
