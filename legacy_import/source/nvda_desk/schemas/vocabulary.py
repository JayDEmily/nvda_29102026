"""Canonical vocabulary governance contracts.

The vocabulary layer governs labels and aliases after the runtime architecture is
pinned. It does not redesign the runtime; it records and validates the terms the
runtime already uses.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

import orjson
from pydantic import BaseModel, ConfigDict, Field, model_validator


class VocabularyCategory(StrEnum):
    STAGE = "stage"
    PLAYBOOK_FAMILY = "playbook_family"
    SETUP_VARIANT = "setup_variant"
    EXECUTION_EXPRESSION = "execution_expression"
    HORIZON = "horizon"
    COMPATIBILITY_SURFACE = "compatibility_surface"
    DATA_CLASSIFICATION = "data_classification"
    WORKFLOW = "workflow"


class RawDerivedTag(StrEnum):
    RAW = "raw"
    DERIVED = "derived"
    NOT_APPLICABLE = "not_applicable"


class VocabularyEntry(BaseModel):
    """One governed vocabulary item."""

    model_config = ConfigDict(extra="forbid")

    canonical_slug: str = Field(min_length=1)
    canonical_label: str = Field(min_length=1)
    category: VocabularyCategory
    stage_owner: str = Field(min_length=1)
    family: str | None = None
    setup_variant: str | None = None
    execution_expression: str | None = None
    horizon: str | None = None
    raw_or_derived: RawDerivedTag = RawDerivedTag.NOT_APPLICABLE
    maps_to_contract: str = Field(min_length=1)
    allowed_aliases: list[str] = Field(default_factory=list)
    disallowed_phrases: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class VocabularyDocument(BaseModel):
    """Canonical vocabulary file used by the enforcement tests."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(min_length=1)
    registry_version: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)
    entries: list[VocabularyEntry] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_uniqueness(self) -> Self:
        slugs = [entry.canonical_slug for entry in self.entries]
        if len(set(slugs)) != len(slugs):
            raise ValueError("canonical_slug values must be unique")
        labels = [entry.canonical_label for entry in self.entries]
        if len(set(labels)) != len(labels):
            raise ValueError("canonical_label values must be unique")
        alias_index: dict[str, str] = {}
        for entry in self.entries:
            if entry.canonical_label in entry.allowed_aliases:
                raise ValueError(
                    f"canonical label cannot also be an alias: {entry.canonical_label}"
                )
            for alias in entry.allowed_aliases:
                owner = alias_index.setdefault(alias, entry.canonical_slug)
                if owner != entry.canonical_slug:
                    raise ValueError(f"alias used by multiple entries: {alias}")
            if entry.canonical_slug in entry.allowed_aliases:
                raise ValueError(f"canonical slug cannot also be an alias: {entry.canonical_slug}")
        return self

    def entry_index(self) -> dict[str, VocabularyEntry]:
        return {entry.canonical_slug: entry for entry in self.entries}

    @classmethod
    def from_json_text(cls, text: str) -> VocabularyDocument:
        data = orjson.loads(text)
        if not isinstance(data, dict):
            raise ValueError("vocabulary JSON must decode to an object")
        return cls.model_validate(data)

    @classmethod
    def from_json_path(cls, path: Path | str) -> VocabularyDocument:
        return cls.from_json_text(Path(path).read_text(encoding="utf-8"))

    def to_json_text(self) -> str:
        return orjson.dumps(self.model_dump(mode="json"), option=orjson.OPT_INDENT_2).decode(
            "utf-8"
        )
