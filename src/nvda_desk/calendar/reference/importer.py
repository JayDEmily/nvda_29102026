"""Import governed calendar reference artefacts into typed repo contracts."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from nvda_desk.contracts.reference_data import (
    BundleLayerReference,
    ImportedReferenceBundle,
    ReferenceArtifact,
    ReferenceArtifactKind,
)
from nvda_desk.packets.dmp_packets import build_reference_packet

_FORBIDDEN_MANIFEST_KEYS = frozenset(
    {
        "online_calendar_mutation",
        "live_market_fetch",
        "candidate_formation",
        "trading_instruction",
        "capital_sizing",
    }
)


class FinancialCalendarImporter:
    """Deterministically convert reference artefacts into bundle contracts."""

    def __init__(self, repo_root: Path | None = None):
        self._repo_root = repo_root

    @property
    def repo_root(self) -> Path | None:
        """Return the optional repo-root used for bundle-relative resolution."""

        return self._repo_root

    def load_manifest(self, manifest: Mapping[str, Any]) -> ImportedReferenceBundle:
        """Build a typed reference bundle from one manifest dictionary."""

        return load_manifest(manifest)

    def load_layers(self, layers: Iterable[Mapping[str, Any]]) -> list[BundleLayerReference]:
        """Build typed layer references from manifest-supplied layer dictionaries."""

        return load_layers(layers)

    def build_reference_packet(self, *, bundle: ImportedReferenceBundle, packet_id: str):
        """Emit one reference-data packet for an already-typed bundle."""

        return build_reference_packet(
            packet_id=packet_id,
            dataschema="ImportedReferenceBundle",
            data=asdict(bundle),
        )


def _artifact_kind_from_value(value: str | None) -> ReferenceArtifactKind:
    if value is None:
        return ReferenceArtifactKind.CALENDAR_BUNDLE
    try:
        return ReferenceArtifactKind(value)
    except ValueError:
        return ReferenceArtifactKind.CALENDAR_BUNDLE


def _find_forbidden_manifest_authority(value: Any) -> list[str]:
    found: set[str] = set()
    if isinstance(value, Mapping):
        found.update(key for key in value if key in _FORBIDDEN_MANIFEST_KEYS)
        for nested_value in value.values():
            found.update(_find_forbidden_manifest_authority(nested_value))
    elif isinstance(value, list | tuple):
        for nested_value in value:
            found.update(_find_forbidden_manifest_authority(nested_value))
    return sorted(found)


def _reject_forbidden_manifest_authority(manifest: Mapping[str, Any]) -> None:
    present = _find_forbidden_manifest_authority(manifest)
    if present:
        raise ValueError(f"calendar manifest contains forbidden runtime authority keys: {present}")


def _require_unique(values: list[str], *, label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ValueError(f"duplicate {label} values are not allowed: {duplicates}")


def load_manifest(manifest: Mapping[str, Any]) -> ImportedReferenceBundle:
    """Return an ``ImportedReferenceBundle`` from a plain manifest mapping."""

    _reject_forbidden_manifest_authority(manifest)
    artifacts = [
        ReferenceArtifact(
            artifact_id=str(item["artifact_id"]),
            kind=_artifact_kind_from_value(item.get("kind")),
            source_path=str(item["source_path"]),
            version=str(item.get("version", manifest.get("version", "unknown"))),
        )
        for item in manifest.get("artifacts", [])
    ]
    artifact_ids = [artifact.artifact_id for artifact in artifacts]
    _require_unique(artifact_ids, label="reference artifact_id")

    layers = load_layers(manifest.get("layers", []))
    _require_unique([layer.layer_id for layer in layers], label="calendar layer_id")
    unknown_refs = sorted(
        {artifact_id for layer in layers for artifact_id in layer.artifact_ids} - set(artifact_ids)
    )
    if unknown_refs:
        raise ValueError(f"calendar layers reference unknown artifacts: {unknown_refs}")

    return ImportedReferenceBundle(
        bundle_id=str(manifest["bundle_id"]),
        version=str(manifest.get("version", "unknown")),
        artifacts=artifacts,
        layers=layers,
    )


def load_layers(layers: Iterable[Mapping[str, Any]]) -> list[BundleLayerReference]:
    """Return typed layer references from plain layer dictionaries."""

    return [
        BundleLayerReference(
            layer_id=str(item["layer_id"]),
            artifact_ids=[str(v) for v in item.get("artifact_ids", [])],
            notes=[str(v) for v in item.get("notes", [])],
        )
        for item in layers
    ]
