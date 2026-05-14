"""Load workbook-derived coefficient authority from typed YAML under the config home."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path

import yaml

from nvda_desk.contracts.coefficient_authority import (
    CoefficientAuthorityDocument,
    CoefficientAuthorityRecord,
    ModifierPolicyRecord,
    coefficient_authority_document_from_dict,
)
from nvda_desk.contracts.modifiers import (
    ModifierReplayReceipt,
    ModifierRuntimePacket,
    ResolvedCoefficientValue,
)

DEFAULT_COEFFICIENT_AUTHORITY_PATH = Path("config/coefficient_authority.v1.yaml")


class CoefficientAuthorityService:
    """Provide typed coefficient authority and bounded modifier resolution."""

    def __init__(self, authority_path: Path | str = DEFAULT_COEFFICIENT_AUTHORITY_PATH) -> None:
        """Initialise the service with one governed coefficient-authority YAML path."""

        self.authority_path = Path(authority_path)

    def load_document(self) -> CoefficientAuthorityDocument:
        """Load and validate the governed coefficient-authority document."""

        payload = yaml.safe_load(self.authority_path.read_text(encoding="utf-8")) or {}
        return coefficient_authority_document_from_dict(payload)

    def record_map(
        self, *, owner_stage: str | None = None
    ) -> dict[str, CoefficientAuthorityRecord]:
        """Return coefficient records keyed by id, optionally restricted to one owner stage."""

        return self.load_document().record_map(owner_stage=owner_stage)

    def baseline_value_map(self, *, owner_stage: str | None = None) -> dict[str, float | bool]:
        """Return baseline coefficient values keyed by governed coefficient id."""

        return {
            coefficient_id: record.baseline_value
            for coefficient_id, record in self.record_map(owner_stage=owner_stage).items()
        }

    def build_replay_receipt(
        self, *, active_modifier_ids: Iterable[str] = (), owner_stage: str = "posture"
    ) -> ModifierReplayReceipt:
        """Return a deterministic replay receipt without widening runtime authority."""

        document = self.load_document()
        packet = self.build_modifier_packet(
            active_modifier_ids=active_modifier_ids,
            owner_stage=owner_stage,
        )
        closed_authority_classes = [
            "capital_deployment_decision",
            "source_data_ingestion",
            "hidden_strategy_change",
            "unbounded_runtime_mutation",
        ]
        resolved = sorted(
            packet.resolved_coefficients,
            key=lambda coefficient: coefficient.coefficient_id,
        )
        fingerprint_payload = {
            "authority_id": document.authority_id,
            "schema_version": document.schema_version,
            "owner_stage": owner_stage,
            "active_modifier_ids": list(packet.active_modifier_ids),
            "resolved_coefficients": [
                coefficient.model_dump(mode="json") for coefficient in resolved
            ],
            "closed_authority_classes": closed_authority_classes,
        }
        fingerprint = hashlib.sha256(
            json.dumps(
                fingerprint_payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        return ModifierReplayReceipt(
            authority_id=document.authority_id,
            schema_version=document.schema_version,
            owner_stage=owner_stage,
            active_modifier_ids=list(packet.active_modifier_ids),
            resolved_coefficients=resolved,
            replay_fingerprint=fingerprint,
            closed_authority_classes=closed_authority_classes,
        )

    def build_modifier_packet(
        self, *, active_modifier_ids: Iterable[str] = (), owner_stage: str = "posture"
    ) -> ModifierRuntimePacket:
        """Resolve one bounded modifier packet for explicitly requested policies only."""

        document = self.load_document()
        record_map = document.record_map(owner_stage=owner_stage)
        policy_map = {
            policy.policy_id: policy
            for policy in document.modifier_policies
            if policy.owner_stage == owner_stage
        }
        requested_ids = list(active_modifier_ids)
        duplicate_ids = sorted(
            {policy_id for policy_id in requested_ids if requested_ids.count(policy_id) > 1}
        )
        if duplicate_ids:
            raise ValueError(f"duplicate modifier policies requested: {duplicate_ids}")
        unknown_ids = sorted(set(requested_ids) - set(policy_map))
        if unknown_ids:
            raise ValueError(
                f"unknown modifier policies for owner_stage={owner_stage}: {unknown_ids}"
            )

        resolved = {
            coefficient_id: self._baseline_snapshot(record)
            for coefficient_id, record in record_map.items()
        }
        resolved_surfaces = list(record_map)
        for policy_id in requested_ids:
            policy = policy_map[policy_id]
            self._apply_policy(policy=policy, record_map=record_map, resolved=resolved)
        return ModifierRuntimePacket(
            packet_id=f"coefficient_authority::{owner_stage}",
            active_modifier_ids=requested_ids,
            policy_ids=requested_ids,
            resolved_surfaces=resolved_surfaces,
            resolved_coefficients=[resolved[key] for key in sorted(resolved)],
        )

    @staticmethod
    def _baseline_snapshot(record: CoefficientAuthorityRecord) -> ResolvedCoefficientValue:
        """Build one immutable baseline/effective snapshot before policy effects apply."""

        return ResolvedCoefficientValue(
            coefficient_id=record.coefficient_id,
            owner_stage=record.owner_stage,
            surface_class=record.surface_class.value,
            baseline_value=record.baseline_value,
            effective_value=record.baseline_value,
            transform_family=record.transform_family,
            modifier_inputs=[],
            workbook_ref=f"{record.workbook_ref.sheet_name}!{record.workbook_ref.cell_range}",
            runtime_mutable=record.runtime_mutable,
        )

    @staticmethod
    def _apply_policy(
        *,
        policy: ModifierPolicyRecord,
        record_map: dict[str, CoefficientAuthorityRecord],
        resolved: dict[str, ResolvedCoefficientValue],
    ) -> None:
        """Apply one pre-validated modifier policy to admitted runtime-mutable surfaces."""

        for effect in policy.effects:
            record = record_map[effect.coefficient_id]
            resolved[effect.coefficient_id] = ResolvedCoefficientValue(
                coefficient_id=record.coefficient_id,
                owner_stage=record.owner_stage,
                surface_class=record.surface_class.value,
                baseline_value=record.baseline_value,
                effective_value=effect.effective_value,
                transform_family=effect.transform_family,
                modifier_inputs=[policy.policy_id],
                workbook_ref=f"{record.workbook_ref.sheet_name}!{record.workbook_ref.cell_range}",
                runtime_mutable=record.runtime_mutable,
            )
