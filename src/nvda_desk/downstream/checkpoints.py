from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nvda_desk.preparation.context_packet import build_context_payload_mapping
from nvda_desk.preparation.runtime_preparer import PreparedRuntimeSnapshot


@dataclass(slots=True)
class CheckpointObservation:
    checkpoint_id: str
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PreparedIngressCheckpoint:
    """Checkpoint receipt for prepared-ingress handoff material."""

    checkpoint_id: str
    snapshot_id: str | None
    alignment_policy: str
    source_sections: tuple[str, ...] = ()
    missing_optional_enrichments: tuple[str, ...] = ()
    failed_enrichments: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        if self.failed_enrichments:
            return "degraded"
        return "valid"

    @classmethod
    def from_snapshot(
        cls, checkpoint_id: str, snapshot: PreparedRuntimeSnapshot
    ) -> "PreparedIngressCheckpoint":
        return cls(
            checkpoint_id=checkpoint_id,
            snapshot_id=snapshot.snapshot_id,
            alignment_policy=snapshot.lineage.alignment_policy,
            source_sections=tuple(snapshot.lineage.source_sections),
            missing_optional_enrichments=tuple(snapshot.missing_optional_enrichments),
            failed_enrichments=tuple(snapshot.failed_enrichments),
        )

    def as_receipt_payload(self, snapshot: PreparedRuntimeSnapshot) -> dict[str, Any]:
        """Return detached checkpoint receipt material for audit writers."""

        return {
            "checkpoint_id": self.checkpoint_id,
            "snapshot_id": self.snapshot_id,
            "status": self.status,
            "alignment_policy": self.alignment_policy,
            "source_sections": list(self.source_sections),
            "missing_optional_enrichments": list(self.missing_optional_enrichments),
            "failed_enrichments": list(self.failed_enrichments),
            "prepared_context": build_context_payload_mapping(snapshot),
        }
