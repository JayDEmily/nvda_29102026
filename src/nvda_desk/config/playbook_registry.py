"""Typed playbook-registry loader for the benchmark-owned config home."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from yaml.constructor import ConstructorError

from nvda_desk.contracts.playbook import (
    PlaybookDefinition,
    PlaybookMetadataReceipt,
    playbook_payload_fingerprint,
    reject_hidden_playbook_authority,
)

DEFAULT_PLAYBOOK_REGISTRY_PATH = Path("config/playbook_registry.example.yaml")


class _UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys before they collapse."""


def _construct_mapping_without_duplicates(loader: yaml.Loader, node: yaml.Node, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate YAML key: {key}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_without_duplicates,
)


class PlaybookRegistryDocument(BaseModel):
    """Bounded typed view over the checked-in playbook registry document."""

    model_config = ConfigDict(extra="forbid")
    schema_version: str = "playbook_registry.v1"
    registry_id: str
    playbooks: tuple[PlaybookDefinition, ...] = Field(default_factory=tuple)
    registry_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("registry_id")
    @classmethod
    def _registry_id_is_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("registry_id must not be blank")
        return value

    @field_validator("registry_metadata")
    @classmethod
    def _metadata_has_no_hidden_authority(cls, value: dict[str, Any]) -> dict[str, Any]:
        reject_hidden_playbook_authority(value)
        return deepcopy(dict(value))

    @model_validator(mode="after")
    def _playbook_ids_are_unique(self) -> "PlaybookRegistryDocument":
        playbook_ids = tuple(playbook.playbook_id for playbook in self.playbooks)
        duplicates = sorted({value for value in playbook_ids if playbook_ids.count(value) > 1})
        if duplicates:
            raise ValueError(f"duplicate playbook_id: {duplicates[0]}")
        return self

    def enabled_playbooks(self) -> tuple[PlaybookDefinition, ...]:
        """Return enabled playbooks as a copy-safe tuple."""

        return tuple(
            playbook.model_copy(deep=True) for playbook in self.playbooks if playbook.enabled
        )

    def fingerprint(self) -> str:
        """Return a deterministic fingerprint of the registry payload."""

        return playbook_payload_fingerprint(self.model_dump(mode="json"))


def _normalise_playbooks(payload: dict[str, Any]) -> dict[str, Any]:
    raw_playbooks = payload.get("playbooks", ())
    if isinstance(raw_playbooks, dict):
        playbooks = []
        for playbook_id, playbook_payload in raw_playbooks.items():
            if not isinstance(playbook_payload, dict):
                raise ValueError(f"playbook payload must be a mapping: {playbook_id}")
            merged = dict(playbook_payload)
            merged.setdefault("playbook_id", str(playbook_id))
            playbooks.append(merged)
        payload = dict(payload)
        payload["playbooks"] = playbooks
    return payload


def load_playbook_registry(
    path: Path | str = DEFAULT_PLAYBOOK_REGISTRY_PATH,
) -> PlaybookRegistryDocument:
    """Load and validate the repo-owned playbook registry example document."""

    raw_text = Path(path).read_text(encoding="utf-8")
    try:
        payload = yaml.load(raw_text, Loader=_UniqueKeyLoader) or {}
    except ConstructorError as exc:
        raise ValueError(str(exc)) from exc
    if not isinstance(payload, dict):
        raise ValueError("playbook registry document must be a mapping")
    return PlaybookRegistryDocument.model_validate(_normalise_playbooks(payload))


def build_playbook_metadata_receipts(
    registry: PlaybookRegistryDocument,
    *,
    setup_family_ids: list[str] | tuple[str, ...] | None = None,
    setup_variant_ids: list[str] | tuple[str, ...] | None = None,
) -> list[PlaybookMetadataReceipt]:
    """Build deterministic playbook metadata receipts from a governed registry."""

    family_filter = set(setup_family_ids or [])
    variant_filter = set(setup_variant_ids or [])
    fingerprint = registry.fingerprint()
    receipts: list[PlaybookMetadataReceipt] = []
    for playbook in registry.enabled_playbooks():
        if family_filter and playbook.setup_family not in family_filter:
            continue
        constraint_ids = tuple(
            constraint.constraint_id for constraint in playbook.eligibility_constraints
        )
        for setup_variant_id in playbook.setup_variant_ids:
            if variant_filter and setup_variant_id not in variant_filter:
                continue
            receipts.append(
                PlaybookMetadataReceipt(
                    receipt_id=f"{registry.registry_id}:{playbook.playbook_id}:{setup_variant_id}",
                    registry_id=registry.registry_id,
                    playbook_id=playbook.playbook_id,
                    setup_family=playbook.setup_family,
                    setup_variant_id=setup_variant_id,
                    eligibility_constraint_ids=constraint_ids,
                    selection_metadata=deepcopy(dict(playbook.selection_metadata)),
                    source_registry_fingerprint=fingerprint,
                )
            )
    return receipts
