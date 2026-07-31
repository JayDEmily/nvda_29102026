"""Contracts for prepared runtime context handoff surfaces."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

PREPARED_CONTEXT_DATASCHEMA = "nvda.preparation.PreparedRuntimeContext.v1"


class PreparedContextPayload(BaseModel):
    """Copy-safe payload emitted from preparation into packet/review seams."""

    model_config = ConfigDict(extra="forbid")

    snapshot_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    derived_fields: dict[str, Any] = Field(default_factory=dict)
    missing_optional_enrichments: list[str] = Field(default_factory=list)
    failed_enrichments: list[str] = Field(default_factory=list)
    source_kind: str = Field(min_length=1)
    transport: str = Field(min_length=1)
    source_snapshot_id: str | None = None
    source_sections: list[str] = Field(default_factory=list)
    alignment_policy: str = Field(min_length=1)
    runtime_bar_time_utc: datetime | None = None
    derived_field_names: list[str] = Field(default_factory=list)
    source_artifact_ids: list[str] = Field(default_factory=list)
    capture_ids: list[str] = Field(default_factory=list)
    input_fingerprint: str | None = None
    input_schema_version: str | None = None
    input_schema_versions: dict[str, str] = Field(default_factory=dict)
    preparation_policy_version: str | None = None
    derivation_versions: dict[str, str] = Field(default_factory=dict)
    prepared_id: str | None = None
    prepared_fingerprint: str | None = None
    payload_kind: str | None = None
    source_time_utc: datetime | None = None
    source_date: date | None = None

    @property
    def has_failed_enrichments(self) -> bool:
        """Return whether preparation observed any failed enrichment."""

        return bool(self.failed_enrichments)

    @property
    def has_missing_optional_enrichments(self) -> bool:
        """Return whether optional enrichment inputs were absent."""

        return bool(self.missing_optional_enrichments)
