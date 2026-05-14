from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from nvda_desk.schemas.checkpoints import CheckpointObservation

from nvda_desk.schemas.dmp import DmpBehaviourClass, DmpGrammarRole, DmpV3Packet
from nvda_desk.schemas.dmp_envelope import (
    DmpV3Lineage,
    DmpV3Producer,
    DmpV3Summary,
    DmpV3Validation,
    DmpV3ValidationCheck,
)
from nvda_desk.schemas.financial_calendar import (
    FinancialCalendarBundleMetadata,
    FinancialCalendarCrosswalkRecord,
    FinancialCalendarReferenceArtifact,
    FinancialCalendarReferenceBundlePayload,
    default_financial_calendar_crosswalk,
)

FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID = (
    "temporal_context.financial_calendar_reference_bundle@1.0.0"
)
FINANCIAL_CALENDAR_STAGE_NAME = "financial_calendar_reference_bundle"
FINANCIAL_CALENDAR_MODULE_ID = "financial_calendar_reference_bundle"


def financial_calendar_crosswalk() -> list[FinancialCalendarCrosswalkRecord]:
    """Return the frozen Gate 89 crosswalk records."""

    return default_financial_calendar_crosswalk()


FinancialCalendarReferencePacket = DmpV3Packet[FinancialCalendarReferenceBundlePayload]


def build_financial_calendar_reference_packet(
    *,
    metadata: FinancialCalendarBundleMetadata,
    artifacts: Sequence[FinancialCalendarReferenceArtifact],
    emitted_at: datetime,
    active_reference_packet_shell: str = "dmp.v3",
    module_version: str = "1.0.0",
    validation: DmpV3Validation | None = None,
) -> FinancialCalendarReferencePacket:
    """Build the repo-native DMPV3 reference-bundle packet for Gate 286."""

    payload = FinancialCalendarReferenceBundlePayload(
        metadata=metadata,
        artifacts=list(artifacts),
        active_reference_packet_shell=active_reference_packet_shell,
        checkpoint_observations=[
            CheckpointObservation(
                checkpoint_name="financial_calendar.reference_packet.built",
                timestamp=emitted_at,
                input_snapshot={
                    "bundle_id": metadata.bundle_id,
                    "calendar_year": metadata.calendar_year,
                    "artifact_count": len(artifacts),
                },
                output_snapshot={
                    "active_reference_packet_shell": active_reference_packet_shell,
                    "dataschema": FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID,
                    "artifact_ids": [artifact.artifact_id for artifact in artifacts],
                },
            )
        ],
    )
    resolved_validation = validation or DmpV3Validation(
        status="valid",
        checks=[DmpV3ValidationCheck(name="schema_validation", passed=True)],
        violations=[],
    )
    return FinancialCalendarReferencePacket(
        id=f"financial-calendar::{metadata.bundle_id}",
        source=f"urn:nvda:producer:{FINANCIAL_CALENDAR_MODULE_ID}",
        type=(
            f"urn:nvda:packet:{DmpGrammarRole.TEMPORAL_CONTEXT.value}."
            f"{DmpBehaviourClass.REPLAY_ARTEFACT.value}"
        ),
        time=emitted_at,
        dataschema=FINANCIAL_CALENDAR_PAYLOAD_CONTRACT_ID,
        traceid=f"trace::financial-calendar::{metadata.bundle_id}",
        runid=f"run::financial-calendar::{metadata.bundle_id}",
        scenarioid=str(metadata.calendar_year),
        packetrole=DmpBehaviourClass.REPLAY_ARTEFACT.value,
        producer=DmpV3Producer(
            module_id=FINANCIAL_CALENDAR_MODULE_ID,
            module_version=module_version,
            module_instance_id=f"{FINANCIAL_CALENDAR_MODULE_ID}::{metadata.calendar_year}",
            grammar_role=DmpGrammarRole.TEMPORAL_CONTEXT.value,
            stage_name=FINANCIAL_CALENDAR_STAGE_NAME,
            behaviour_class=DmpBehaviourClass.REPLAY_ARTEFACT.value,
        ),
        lineage=DmpV3Lineage(
            parentids=[],
            dependencyids=[],
            sourceartifactids=[artifact.artifact_id for artifact in artifacts],
        ),
        validation=resolved_validation,
        summary=DmpV3Summary(
            headline=(
                f"Financial calendar reference bundle for {metadata.calendar_year}; "
                f"{len(metadata.layers)} layers preserved as repo-controlled artefacts."
            ),
            keyflags=[
                f"layers={len(metadata.layers)}",
                f"artifacts={len(artifacts)}",
                active_reference_packet_shell,
            ],
            humanstate=(
                f"financial-calendar reference bundle / "
                f"year={metadata.calendar_year} / artifacts={len(artifacts)}"
            ),
        ),
        data=payload,
        dmpextensions={
            "nvda": {
                "execution_context": {
                    "stack_id": None,
                    "coefficient_set_id": None,
                    "registry_version": "financial_calendar_reference_bundle@1.0.0",
                    "environment_tag": "repo_checked_in_reference",
                },
                "schema_identifiers": {
                    "payload_model_name": "FinancialCalendarReferenceBundlePayload",
                    "payload_module_path": "nvda_desk.schemas.financial_calendar",
                    "input_model_name": None,
                    "output_model_name": "FinancialCalendarReferenceBundlePayload",
                },
                "semantic_dependencies": [],
            }
        },
    )
