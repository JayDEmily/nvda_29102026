"""Deterministically project the accepted human vocabulary registry.

Semantic authority lives in ``docs/vocabulary/vocabulary_registry.md``.  This
module validates and transforms the explicit projection metadata attached to each
accepted human record; it does not seed, infer, rename, admit, or suppress terms.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from nvda_desk.schemas.vocabulary import (
    VocabularyDocument,
    VocabularyEntry,
    VocabularyNamespace,
)

REGISTRY_PATH = Path("docs/vocabulary/vocabulary_registry.md")
OUTPUT_PATH = Path("data/vocabulary/canonical_vocabulary.json")
GOVERNED_SOURCE_PATHS = (
    Path("docs/10_VOCABULARY_AND_TERM_GOVERNANCE_CORE.md"),
    Path("docs/10.1_VOCABULARY_AND_TERM_GOVERNANCE_WORKING.md"),
    Path("docs/vocabulary/README.md"),
    Path("docs/vocabulary/CONSOLIDATION_WORKFLOW.md"),
    REGISTRY_PATH,
    Path("scripts/build_canonical_vocabulary.py"),
    Path("src/nvda_desk/schemas/vocabulary.py"),
    Path("src/nvda_desk/vocabulary_builder.py"),
    Path("src/nvda_desk/vocabulary_synonym_audit.py"),
    OUTPUT_PATH,
)

_HEADER_FIELDS = MappingProxyType(
    {
        "schema_version": "Projection schema version:",
        "registry_version": "Projection registry version:",
        "notes": "Projection document notes:",
        "namespaces": "Projection namespace scopes:",
    }
)
_REQUIRED_HUMAN_FIELDS = (
    "Definition",
    "Scope",
    "Owner",
    "Relationships",
    "Aliases",
    "Disallowed or misleading use",
    "Lifecycle",
)
_HUMAN_FIELD_PREFIXES = MappingProxyType(
    {
        "Definition": ("Definition:",),
        "Scope": ("Scope:",),
        "Owner": ("Owner:",),
        "Relationships": ("Relationships:",),
        "Aliases": ("Aliases:",),
        "Disallowed or misleading use": (
            "Disallowed or misleading use:",
            "Disallowed or misleading uses:",
        ),
        "Lifecycle": ("Lifecycle:",),
    }
)
_METADATA_PREFIX = "Projection metadata:"
_RECORD_HEADING = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class RegistryAdmissionRecord:
    """One accepted human semantic record and its explicit projection metadata."""

    heading: str
    line_number: int
    human_fields: dict[str, str]
    projection: dict[str, Any]

    @property
    def semantic_decision_refs(self) -> tuple[str, ...]:
        refs = self.projection["semantic_decision_refs"]
        return tuple(str(item) for item in refs)

    def to_entry(self) -> VocabularyEntry:
        metadata = self.projection
        notes = [
            f"Definition: {self.human_fields['Definition']}",
            f"Scope: {self.human_fields['Scope']}",
            f"Semantic owner: {self.human_fields['Owner']}",
            f"Relationships: {self.human_fields['Relationships']}",
            f"Lifecycle: {self.human_fields['Lifecycle']}",
            "Semantic decisions: " + ", ".join(self.semantic_decision_refs),
            f"Human aliases: {self.human_fields['Aliases']}",
            "Human disallowed or misleading use: "
            + self.human_fields["Disallowed or misleading use"],
        ]
        omissions = metadata.get("machine_projection_omissions", [])
        if omissions:
            notes.append("Machine projection omissions: " + "; ".join(omissions))

        return VocabularyEntry(
            namespace=metadata.get("namespace", "global"),
            canonical_slug=metadata["canonical_slug"],
            canonical_label=metadata["canonical_label"],
            category=metadata["category"],
            stage_owner=metadata["stage_owner"],
            maps_to_contract=metadata["maps_to_contract"],
            raw_or_derived=metadata.get("raw_or_derived", "not_applicable"),
            allowed_aliases=list(metadata.get("allowed_aliases", [])),
            disallowed_phrases=list(metadata.get("disallowed_phrases", [])),
            notes=notes,
        )


def _strip_markdown_code(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1]
    return stripped


def _parse_document_header(
    text: str,
) -> tuple[str, str, list[str], dict[str, VocabularyNamespace]]:
    values: dict[str, Any] = {}
    for name, prefix in _HEADER_FIELDS.items():
        matches = [line for line in text.splitlines() if line.startswith(prefix)]
        if len(matches) != 1:
            raise ValueError(f"registry must contain exactly one {prefix!r} line")
        raw_value = matches[0][len(prefix) :].strip()
        if name == "notes":
            parsed = json.loads(raw_value)
            if not isinstance(parsed, list) or not all(
                isinstance(item, str) and item.strip() for item in parsed
            ):
                raise ValueError("Projection document notes must be a non-empty-string list")
            values[name] = parsed
        elif name == "namespaces":
            parsed = json.loads(raw_value)
            if not isinstance(parsed, dict) or not parsed:
                raise ValueError("Projection namespace scopes must be a non-empty object")
            namespaces: dict[str, VocabularyNamespace] = {}
            for namespace, raw_scope in parsed.items():
                if not isinstance(namespace, str) or not isinstance(raw_scope, dict):
                    raise ValueError("Projection namespace scopes must contain keyed objects")
                scope = VocabularyNamespace(
                    namespace=namespace,
                    scan_paths=list(raw_scope.get("scan_paths", [])),
                    imports=list(raw_scope.get("imports", [])),
                )
                scope.validate()
                namespaces[namespace] = scope
            values[name] = namespaces
        else:
            value = _strip_markdown_code(raw_value)
            if not value:
                raise ValueError(f"{prefix} must declare a non-empty value")
            values[name] = value
    return (
        values["schema_version"],
        values["registry_version"],
        values["notes"],
        values["namespaces"],
    )


def _parse_human_fields(block: str, heading: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in block.splitlines()[1:]:
        matched = False
        for field_name, prefixes in _HUMAN_FIELD_PREFIXES.items():
            for prefix in prefixes:
                if line.startswith(prefix):
                    if field_name in values:
                        raise ValueError(f"duplicate {field_name!r} field for {heading}")
                    value = line[len(prefix) :].strip()
                    if not value:
                        raise ValueError(f"empty {field_name!r} field for {heading}")
                    values[field_name] = value
                    matched = True
                    break
            if matched:
                break
    missing = [field_name for field_name in _REQUIRED_HUMAN_FIELDS if field_name not in values]
    if missing:
        raise ValueError(f"registry record {heading!r} is missing human fields: {missing}")
    return values


def _parse_projection(block: str, heading: str) -> dict[str, Any]:
    lines = [line for line in block.splitlines() if line.startswith(_METADATA_PREFIX)]
    if len(lines) != 1:
        raise ValueError(
            f"registry record {heading!r} must contain exactly one projection metadata line"
        )
    metadata = json.loads(lines[0][len(_METADATA_PREFIX) :].strip())
    if not isinstance(metadata, dict):
        raise ValueError(f"projection metadata for {heading!r} must be a JSON object")

    required = {
        "projection_status",
        "canonical_label",
        "canonical_slug",
        "category",
        "stage_owner",
        "maps_to_contract",
        "raw_or_derived",
        "allowed_aliases",
        "disallowed_phrases",
        "semantic_decision_refs",
        "machine_projection_omissions",
        "audit_noncanonical_phrases",
    }
    missing = sorted(required - metadata.keys())
    optional = {"namespace"}
    unknown = sorted(metadata.keys() - required - optional)
    if missing or unknown:
        raise ValueError(
            f"projection metadata keys for {heading!r} are invalid; missing={missing}, unknown={unknown}"
        )
    if metadata["projection_status"] != "canonical":
        raise ValueError(
            f"registry record {heading!r} is not an accepted canonical projection record"
        )
    if metadata["canonical_label"] != heading:
        raise ValueError(
            f"projection canonical_label {metadata['canonical_label']!r} does not match heading {heading!r}"
        )
    for field_name in (
        "canonical_slug",
        "category",
        "stage_owner",
        "maps_to_contract",
        "raw_or_derived",
    ):
        if not isinstance(metadata[field_name], str) or not metadata[field_name].strip():
            raise ValueError(f"projection {field_name} must be non-empty for {heading!r}")
    namespace = metadata.get("namespace", "global")
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError(f"projection namespace must be non-empty for {heading!r}")
    for field_name in (
        "allowed_aliases",
        "disallowed_phrases",
        "semantic_decision_refs",
        "machine_projection_omissions",
        "audit_noncanonical_phrases",
    ):
        values = metadata[field_name]
        if not isinstance(values, list) or not all(
            isinstance(item, str) and item.strip() for item in values
        ):
            raise ValueError(f"projection {field_name} must be a string list for {heading!r}")
    if not metadata["semantic_decision_refs"]:
        raise ValueError(f"semantic_decision_refs must not be empty for {heading!r}")
    return metadata


def read_registry_admission_records(
    path: Path = REGISTRY_PATH,
) -> tuple[
    str,
    str,
    list[str],
    dict[str, VocabularyNamespace],
    list[RegistryAdmissionRecord],
]:
    """Read and validate the complete accepted human registry."""

    text = path.read_text(encoding="utf-8")
    schema_version, registry_version, notes, namespaces = _parse_document_header(text)
    matches = list(_RECORD_HEADING.finditer(text))
    if not matches:
        raise ValueError("vocabulary registry contains no accepted records")

    records: list[RegistryAdmissionRecord] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end].rstrip()
        heading = match.group(1).strip()
        line_number = text.count("\n", 0, match.start()) + 1
        records.append(
            RegistryAdmissionRecord(
                heading=heading,
                line_number=line_number,
                human_fields=_parse_human_fields(block, heading),
                projection=_parse_projection(block, heading),
            )
        )

    canonical_ids = [
        (
            record.projection.get("namespace", "global") + "." + record.projection["canonical_slug"]
        ).casefold()
        for record in records
    ]
    if len(canonical_ids) != len(set(canonical_ids)):
        raise ValueError("projection canonical ids must be unique after case folding")
    return schema_version, registry_version, notes, namespaces, records


def build_document() -> VocabularyDocument:
    schema_version, registry_version, notes, namespaces, records = read_registry_admission_records()
    document = VocabularyDocument(
        schema_version=schema_version,
        registry_version=registry_version,
        notes=notes,
        namespaces=namespaces,
        entries=[record.to_entry() for record in records],
    )
    document.validate()
    return document


def build_canonical_vocabulary() -> VocabularyDocument:
    return build_document()


def build_canonical_payload() -> dict[str, Any]:
    return build_document().to_dict()


def governed_source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in GOVERNED_SOURCE_PATHS:
        if path.exists():
            hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def write_canonical_vocabulary() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(build_canonical_payload(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
