"""Parallel-risk-owned write-only persistence helpers for Module 8."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime

from nvda_desk.contracts.packets import DeskModulePacketV3
from nvda_desk.contracts.parallel_risk import (
    PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA,
    PARALLEL_RISK_LANE_DATASCHEMA,
    ParallelRiskObservationAppendReceipt,
    ParallelRiskObservationRecord,
)
from nvda_desk.contracts.temporal import build_source_temporal_payload


class ParallelRiskObservationStore:
    """Append-only write-only store for bounded parallel-risk observation records."""

    def __init__(self):
        self._records: list[dict] = []
        self._observation_ids: set[str] = set()

    def append_observation(
        self, record: ParallelRiskObservationRecord
    ) -> ParallelRiskObservationAppendReceipt:
        """Append one observation record and return a bounded receipt."""

        if record.observation_id in self._observation_ids:
            raise ValueError(f"duplicate observation_id: {record.observation_id}")
        stored = deepcopy(record.model_dump(mode="python"))
        self._records.append(stored)
        self._observation_ids.add(record.observation_id)
        return ParallelRiskObservationAppendReceipt(
            observation_id=record.observation_id,
            stored_input_packet_ids=list(record.input_packet_ids),
            stored_output_packet_ids=list(record.output_packet_ids),
        )


def build_parallel_risk_observation_record(
    *,
    observation_id: str,
    input_packet: DeskModulePacketV3,
    output_packet: DeskModulePacketV3,
    persisted_at_utc: datetime | None = None,
) -> ParallelRiskObservationRecord:
    """Build one append-only observation record from the lawful Module 8 packet pair."""

    if input_packet.dataschema != PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA:
        raise ValueError(
            f"parallel risk observation input packet requires dataschema {PARALLEL_RISK_BOOTSTRAP_INPUT_DATASCHEMA}, got {input_packet.dataschema}"
        )
    if output_packet.dataschema != PARALLEL_RISK_LANE_DATASCHEMA:
        raise ValueError(
            f"parallel risk observation output packet requires dataschema {PARALLEL_RISK_LANE_DATASCHEMA}, got {output_packet.dataschema}"
        )

    persisted_at_utc = persisted_at_utc or datetime.now(UTC)
    temporal_input = input_packet.data.temporal_input
    return ParallelRiskObservationRecord(
        **build_source_temporal_payload(
            source_time_utc=temporal_input.source_time_utc,
            source_date=temporal_input.source_date,
            source_time_raw=temporal_input.source_time_raw,
            source_time_kind=temporal_input.source_time_kind,
            source_timezone_raw=temporal_input.source_timezone_raw,
            captured_at_utc=temporal_input.captured_at_utc,
            persisted_at_utc=persisted_at_utc,
            source_provider=temporal_input.source_provider,
            source_channel=temporal_input.source_channel,
            time_granularity=temporal_input.time_granularity,
        ),
        observation_id=observation_id,
        input_packet_ids=[input_packet.packet_id],
        output_packet_ids=[output_packet.packet_id],
        traceid=output_packet.traceid,
        runid=output_packet.runid,
        scenarioid=output_packet.scenarioid,
        parentids=list(output_packet.lineage.parentids),
        dependencyids=list(output_packet.lineage.dependencyids),
        bounded_observation_payload={
            "lane_packet_role": output_packet.packetrole,
            "lane_dataschema": output_packet.dataschema,
            "input_dataschema": input_packet.dataschema,
            "summary_headline": output_packet.summary.headline,
            "summary_humanstate": output_packet.summary.humanstate,
            "summary_keyflags": list(output_packet.summary.keyflags),
        },
    )
