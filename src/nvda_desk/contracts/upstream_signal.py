"""Contracts for bounded upstream signal traceability and scope-lock repair surfaces."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

UpstreamSignalDisposition = Literal["admitted_trace_only", "rejected_quarantined"]
UpstreamPromotionStatus = Literal["trace_only", "quarantine_required", "rejected", "reserved"]


class RawUpstreamSignalInput(BaseModel):
    """One raw upstream signal input before native scope-lock admission."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    signal_family_id: str = Field(min_length=1)
    scope_id: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("payload", mode="before")
    @classmethod
    def _detach_payload_from_caller(cls, value: Any) -> Any:
        """Detach caller-owned payload containers before scope admission."""

        return deepcopy(value)


class UpstreamSanityTrace(BaseModel):
    """Deterministic trace emitted for every upstream signal admission attempt."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    signal_family_id: str = Field(min_length=1)
    scope_id: str = Field(min_length=1)
    disposition: UpstreamSignalDisposition
    rejection_reason: str | None = None


class UpstreamIngressResult(BaseModel):
    """Result of raw-signal ingestion without mutating downstream packet payloads."""

    model_config = ConfigDict(extra="forbid")

    dataset_packet_payload: dict[str, Any] = Field(default_factory=dict)
    sanity_trace: UpstreamSanityTrace
    trace_envelope: dict[str, Any] = Field(default_factory=dict)
    quarantined: bool = False
    trade_decision_side_effects: list[str] = Field(default_factory=list)


class UpstreamSignalCoverageEntry(BaseModel):
    """One admitted upstream signal family entry in the native coverage map."""

    model_config = ConfigDict(extra="forbid")

    owner: str = Field(min_length=1)
    signal_family_id: str = Field(min_length=1)
    source_scope: str = Field(min_length=1)
    packet_fields: list[str] = Field(default_factory=list)
    promotion_status: UpstreamPromotionStatus = "trace_only"


class UpstreamSignalCoverageMap(BaseModel):
    """Native coverage map for upstream signals admitted to packet-facing boundaries."""

    model_config = ConfigDict(extra="forbid")

    entries: list[UpstreamSignalCoverageEntry] = Field(default_factory=list)

    @property
    def admitted_signal_family_ids(self) -> list[str]:
        """Return deterministic admitted signal-family ids."""

        return sorted(entry.signal_family_id for entry in self.entries)

    def require(self, signal_family_id: str) -> UpstreamSignalCoverageEntry:
        """Return the coverage entry for one signal family or raise ``KeyError``."""

        for entry in self.entries:
            if entry.signal_family_id == signal_family_id:
                return entry
        raise KeyError(signal_family_id)
