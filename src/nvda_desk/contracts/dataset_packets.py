"""Dataset-packet boundary contracts for admitted upstream-signal fields."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from nvda_desk.contracts.upstream_signal import UpstreamSignalCoverageMap


class DatasetPacketSignalView(BaseModel):
    """Explicit dataset-packet view of fields admitted from one upstream signal family."""

    model_config = ConfigDict(extra="forbid")

    packet_id: str = Field(min_length=1)
    signal_family_id: str = Field(min_length=1)
    exposed_fields: dict[str, Any] = Field(default_factory=dict)
    rejected_fields: dict[str, Any] = Field(default_factory=dict)


def build_dataset_packet_signal_view(
    *,
    packet_id: str,
    signal_family_id: str,
    payload: dict[str, Any],
    coverage_map: UpstreamSignalCoverageMap,
) -> DatasetPacketSignalView:
    """Expose only fields declared by the coverage map for one signal family."""

    entry = coverage_map.require(signal_family_id)
    allowed_fields = set(entry.packet_fields)
    exposed = {key: value for key, value in payload.items() if key in allowed_fields}
    rejected = {key: value for key, value in payload.items() if key not in allowed_fields}
    return DatasetPacketSignalView(
        packet_id=packet_id,
        signal_family_id=signal_family_id,
        exposed_fields=exposed,
        rejected_fields=rejected,
    )
