from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SourceForm(str, Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    CONSTANT = "constant"
    DOCUMENT = "document"


class MaturityState(str, Enum):
    CANDIDATE = "candidate"
    BLOCKED = "blocked"
    PROMOTED = "promoted"
    RETIRED = "retired"


class GrammarRole(str, Enum):
    SERVICE = "service"
    SCHEMA = "schema"
    REPOSITORY = "repository"
    ENTRYPOINT = "entrypoint"
    HELPER = "helper"


class RuntimeTarget(str, Enum):
    RUNTIME = "runtime"
    REVIEW_ONLY = "review_only"
    RESEARCH_ONLY = "research_only"
    NONE = "none"


class ReadinessState(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"
    REVIEW_ONLY = "review_only"
    NOT_RUNTIME = "not_runtime"


class ImportRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    registry_id: str
    source_form: SourceForm
    maturity_state: MaturityState = MaturityState.CANDIDATE
    runtime_target: RuntimeTarget = RuntimeTarget.NONE
    import_depth: int = 0
    source_path: str | None = None
    runtime_contract_id: str | None = None
    blockers: tuple[str, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _ids_are_non_empty(self) -> "ImportRegistryRow":
        if not self.registry_id.strip():
            raise ValueError("registry_id must be non-empty")
        if self.import_depth < 0:
            raise ValueError("import_depth must be non-negative")
        return self


class GrammarMappingRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mapping_id: str
    registry_id: str
    grammar_role: GrammarRole
    source_tokens: tuple[str, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _ids_are_non_empty(self) -> "GrammarMappingRow":
        if not self.mapping_id.strip():
            raise ValueError("mapping_id must be non-empty")
        if not self.registry_id.strip():
            raise ValueError("registry_id must be non-empty")
        return self


class ImportRegistryDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "import_registry.v1"
    registry_rows: tuple[ImportRegistryRow, ...] = Field(default_factory=tuple)
    grammar_mappings: tuple[GrammarMappingRow, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _ids_are_unique_and_mappings_have_sources(self) -> "ImportRegistryDocument":
        registry_ids = [row.registry_id for row in self.registry_rows]
        duplicate_registry_ids = sorted(
            {value for value in registry_ids if registry_ids.count(value) > 1}
        )
        if duplicate_registry_ids:
            raise ValueError(f"duplicate registry_id: {duplicate_registry_ids[0]}")
        mapping_ids = [row.mapping_id for row in self.grammar_mappings]
        duplicate_mapping_ids = sorted(
            {value for value in mapping_ids if mapping_ids.count(value) > 1}
        )
        if duplicate_mapping_ids:
            raise ValueError(f"duplicate mapping_id: {duplicate_mapping_ids[0]}")
        registry_id_set = set(registry_ids)
        missing = sorted(
            mapping.registry_id
            for mapping in self.grammar_mappings
            if mapping.registry_id not in registry_id_set
        )
        if missing:
            raise ValueError(f"grammar mapping references unknown registry_id: {missing[0]}")
        return self

    def registry_index(self) -> dict[str, ImportRegistryRow]:
        return {row.registry_id: row for row in self.registry_rows}

    def grammar_role_ids(self, role: GrammarRole | str) -> tuple[str, ...]:
        role_value = GrammarRole(role)
        return tuple(
            row.mapping_id for row in self.grammar_mappings if row.grammar_role == role_value
        )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    @classmethod
    def from_json_path(cls, path: Path | str) -> "ImportRegistryDocument":
        import json

        return import_registry_document_from_dict(
            json.loads(Path(path).read_text(encoding="utf-8"))
        )


def import_registry_document_from_dict(payload: Mapping[str, Any]) -> ImportRegistryDocument:
    return ImportRegistryDocument.model_validate(dict(payload))
