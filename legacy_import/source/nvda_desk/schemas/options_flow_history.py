from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.schemas.cognition import OptionsFlowContextOutput
from nvda_desk.schemas.options import OptionSnapshotPayload

RawSourceAuthority = Literal["persisted_option_snapshot"]
PartialityState = Literal[
    "complete",
    "front_expiry_missing",
    "next_expiry_missing",
    "raw_subset_missing",
]
WriteStatus = Literal["disabled", "persisted", "write_failed", "build_failed"]


class OptionsFlowHistoryLineage(BaseModel):
    """Deterministic lineage for one options-flow observation record."""

    model_config = ConfigDict(extra="forbid")

    capture_trigger: str = "options_flow_context_output"
    raw_source_authority: RawSourceAuthority
    observed_at: datetime
    chain_ts: datetime
    raw_source_as_of_date: date
    source_identity: str


class OptionsFlowHistoryObservationRecord(BaseModel):
    """Observational record captured at the Options and Flow Context boundary."""

    model_config = ConfigDict(extra="forbid")

    symbol: str = Field(min_length=1)
    observed_at: datetime
    chain_ts: datetime
    front_expiry: date
    next_expiry: date
    derived_state: OptionsFlowContextOutput
    front_expiry_rows: list[OptionSnapshotPayload] = Field(default_factory=list)
    next_expiry_rows: list[OptionSnapshotPayload] = Field(default_factory=list)
    partiality_state: PartialityState
    record_completeness_flag: bool
    lineage: OptionsFlowHistoryLineage


class OptionsFlowHistoryObservationStorePayload(BaseModel):
    """Stored observational record with database identity."""

    model_config = ConfigDict(extra="forbid")

    observation_id: int
    created_at: datetime
    record: OptionsFlowHistoryObservationRecord


class OptionsFlowHistoryWriteResult(BaseModel):
    """Outcome for one bounded observational-lane write attempt."""

    model_config = ConfigDict(extra="forbid")

    status: WriteStatus
    note: str | None = None
    persisted: OptionsFlowHistoryObservationStorePayload | None = None
