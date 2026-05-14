from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from nvda_desk.schemas.checkpoints import CheckpointObservation

from nvda_desk.schemas.dmp import DmpV3Packet
from nvda_desk.schemas.financial_calendar import (
    FinancialCalendarBundleMetadata,
    FinancialCalendarImportedBundle,
    FinancialCalendarImportedRecord,
    FinancialCalendarLayerArtifact,
    FinancialCalendarReferenceArtifact,
    FinancialCalendarReferenceArtifactKind,
    FinancialCalendarReferenceBundlePayload,
    FinancialCalendarRepoManifest,
)
from nvda_desk.services.financial_calendar_reference import (
    build_financial_calendar_reference_packet,
)


class FinancialCalendarImportService:
    """Load repo-controlled financial-calendar artefacts without activating runtime behaviour.

    Purpose:
        Provide one deterministic seam from checked-in reference artefacts into
        provenance-bearing import-stage records.
    Inputs:
        Repo-controlled JSON and markdown artefacts under
        `data/reference/financial_calendar/`.
    Outputs:
        `FinancialCalendarImportedBundle` and repo-native DMPV3 reference
        packets that keep artefact lineage explicit.
    Determinism:
        Uses checked-in files only. No runtime web fetches, no behavioural
        projection, and no canonical event-store wiring in Gate 90.
    """

    def __init__(self, repo_root: Path | None = None):
        self._repo_root = repo_root or Path(__file__).resolve().parents[3]
        self._root = self._repo_root / "data/reference/financial_calendar"

    @property
    def root(self) -> Path:
        return self._root

    def load_repo_manifest(self) -> FinancialCalendarRepoManifest:
        return FinancialCalendarRepoManifest.model_validate(
            json.loads((self._root / "repo_manifest.json").read_text(encoding="utf-8"))
        )

    def load_bundle_metadata(self) -> FinancialCalendarBundleMetadata:
        return FinancialCalendarBundleMetadata.model_validate(
            json.loads((self._root / "financial_calendar_master_2026.json").read_text(encoding="utf-8"))
        )

    def load_layer_artifacts(self) -> list[FinancialCalendarLayerArtifact]:
        manifest = self.load_repo_manifest()
        return [
            FinancialCalendarLayerArtifact.model_validate(
                json.loads((self._root / rel_path).read_text(encoding="utf-8"))
            )
            for rel_path in manifest.layer_files
        ]

    def list_reference_artifacts(self, *, include_supporting: bool = True) -> list[FinancialCalendarReferenceArtifact]:
        manifest = self.load_repo_manifest()
        checksums = json.loads((self._root / manifest.checksum_manifest_file).read_text(encoding="utf-8"))
        artifacts: list[FinancialCalendarReferenceArtifact] = [
            self._artifact_for(
                artifact_id="master_manifest",
                artifact_kind=FinancialCalendarReferenceArtifactKind.MASTER_MANIFEST,
                rel_path=manifest.bundle_metadata_file,
                checksums=checksums,
                schema_id="financial_calendar.master_manifest@1.0.0",
            ),
            self._artifact_for(
                artifact_id="source_manifest",
                artifact_kind=FinancialCalendarReferenceArtifactKind.SOURCE_MANIFEST,
                rel_path=manifest.source_manifest_file,
                checksums=checksums,
                schema_id="financial_calendar.source_manifest@1.0.0",
            ),
            self._artifact_for(
                artifact_id="checksum_manifest",
                artifact_kind=FinancialCalendarReferenceArtifactKind.CHECKSUM_MANIFEST,
                rel_path=manifest.checksum_manifest_file,
                checksums=checksums,
                schema_id="financial_calendar.checksums@1.0.0",
            ),
        ]
        for rel_path in manifest.layer_files:
            layer_name = Path(rel_path).stem.replace("_2026", "")
            artifacts.append(
                self._artifact_for(
                    artifact_id=layer_name,
                    artifact_kind=FinancialCalendarReferenceArtifactKind.LAYER_JSON,
                    rel_path=rel_path,
                    checksums=checksums,
                    schema_id="financial_calendar.layer@1.0.0",
                )
            )
        if include_supporting:
            for rel_path in manifest.supporting_files:
                rel_name = Path(rel_path).name
                if rel_name.endswith('.md'):
                    kind = FinancialCalendarReferenceArtifactKind.BINDING_PLAN if rel_name != 'README.md' else FinancialCalendarReferenceArtifactKind.BUNDLE_README
                    schema_id = 'financial_calendar.binding_plan@1.0.0' if rel_name != 'README.md' else 'financial_calendar.bundle_readme@1.0.0'
                elif rel_name.endswith('_bundle_example.json'):
                    kind = FinancialCalendarReferenceArtifactKind.EXTERNAL_EXAMPLE_PACKET
                    schema_id = 'financial_calendar.external_example_packet@1.0.0'
                else:
                    kind = FinancialCalendarReferenceArtifactKind.EXTERNAL_VALIDATION_RESULT
                    schema_id = 'financial_calendar.external_validation_result@1.0.0'
                artifact_id = Path(rel_path).stem
                artifacts.append(
                    self._artifact_for(
                        artifact_id=artifact_id,
                        artifact_kind=kind,
                        rel_path=rel_path,
                        checksums=checksums,
                        schema_id=schema_id,
                    )
                )
        return artifacts

    def import_bundle(self) -> FinancialCalendarImportedBundle:
        metadata = self.load_bundle_metadata()
        manifest = self.load_repo_manifest()
        artifacts = self.list_reference_artifacts(include_supporting=True)
        artifact_by_path = {artifact.repo_path: artifact for artifact in artifacts}
        imported_records: list[FinancialCalendarImportedRecord] = []
        for layer in self.load_layer_artifacts():
            rel_path = next(
                rel_path for rel_path in manifest.layer_files if layer.layer_id.value in rel_path
            )
            repo_path = f"data/reference/financial_calendar/{rel_path}"
            artifact = artifact_by_path[repo_path]
            for event in layer.events:
                imported_records.append(
                    FinancialCalendarImportedRecord(
                        record_id=f"fc::{event.event_id}",
                        repo_artifact_id=artifact.artifact_id,
                        repo_artifact_path=artifact.repo_path,
                        import_lineage_key=f"financial_calendar::{event.layer_id.value}::{event.event_id}",
                        event_id=event.event_id,
                        layer_id=event.layer_id,
                        event_type=event.event_type,
                        title=event.title,
                        start_date=event.start_date,
                        end_date=event.end_date,
                        start_time_local=event.start_time_local,
                        end_time_local=event.end_time_local,
                        timezone=event.timezone,
                        jurisdiction=event.jurisdiction,
                        venues=list(event.venues),
                        entities=list(event.entities),
                        impact_level=event.impact_level,
                        runtime_tags=list(event.runtime_tags),
                        evaluation_tags=list(event.evaluation_tags),
                        source_status=event.source_status,
                        source_document=event.source_document,
                        notes_md=event.notes_md,
                    )
                )
        return FinancialCalendarImportedBundle(
            metadata=metadata,
            repo_manifest=manifest,
            artifacts=artifacts,
            imported_records=imported_records,
            checkpoint_observations=[
                CheckpointObservation(
                    checkpoint_name="financial_calendar.import_bundle.loaded",
                    timestamp=datetime.now(UTC),
                    input_snapshot={
                        "bundle_id": metadata.bundle_id,
                        "calendar_year": metadata.calendar_year,
                        "supporting_artifact_count": len(manifest.supporting_files),
                    },
                    output_snapshot={
                        "artifact_count": len(artifacts),
                        "imported_record_count": len(imported_records),
                        "active_reference_packet_shell": manifest.active_reference_packet_shell,
                    },
                )
            ],
        )

    def build_reference_packet(self, *, emitted_at: datetime) -> DmpV3Packet[FinancialCalendarReferenceBundlePayload]:
        metadata = self.load_bundle_metadata()
        manifest = self.load_repo_manifest()
        authoritative_artifacts = self.list_reference_artifacts(include_supporting=False)
        return build_financial_calendar_reference_packet(
            metadata=metadata,
            artifacts=authoritative_artifacts,
            emitted_at=emitted_at,
            active_reference_packet_shell=(manifest.active_reference_packet_shell or "dmp.v3"),
        )

    def _artifact_for(
        self,
        *,
        artifact_id: str,
        artifact_kind: FinancialCalendarReferenceArtifactKind,
        rel_path: str,
        checksums: dict[str, str],
        schema_id: str,
    ) -> FinancialCalendarReferenceArtifact:
        full_path = self._root / rel_path
        media_type = "application/json" if full_path.suffix == ".json" else "text/markdown"
        return FinancialCalendarReferenceArtifact(
            artifact_id=artifact_id,
            artifact_kind=artifact_kind,
            repo_path=f"data/reference/financial_calendar/{rel_path}",
            media_type=media_type,
            schema_id=schema_id,
            checksum=checksums.get(rel_path),
            byte_count=full_path.stat().st_size,
        )
