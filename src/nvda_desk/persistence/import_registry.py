from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from nvda_desk.schemas.import_registry import (
    GrammarMappingRow,
    GrammarRole,
    ImportRegistryDocument,
    ImportRegistryRow,
    MaturityState,
    ReadinessState,
    RuntimeTarget,
)

DEFAULT_IMPORT_REGISTRY_PATH = Path("project_control/import_registry/registry.jsonl")
DEFAULT_GRAMMAR_MAPPING_PATH = Path("project_control/import_registry/grammar_mapping.jsonl")


class ImportRegistryService:
    def __init__(
        self,
        *,
        registry_path: Path | str = DEFAULT_IMPORT_REGISTRY_PATH,
        grammar_mapping_path: Path | str = DEFAULT_GRAMMAR_MAPPING_PATH,
        project_root: Path | str = ".",
    ) -> None:
        self._registry_path = Path(registry_path)
        self._grammar_mapping_path = Path(grammar_mapping_path)
        self._project_root = Path(project_root)

    def registry_path_accessor(self) -> Path:
        return self._registry_path

    def grammar_mapping_path_accessor(self) -> Path:
        return self._grammar_mapping_path

    def project_root(self) -> Path:
        return self._project_root

    def main_entrypoints(self) -> tuple[Path, ...]:
        return tuple(path for path in (self._project_root / "scripts").glob("*.py"))

    def load_seed_registry_rows(self) -> tuple[ImportRegistryRow, ...]:
        return tuple(
            ImportRegistryRow.model_validate(row) for row in self._load_jsonl(self._registry_path)
        )

    def load_seed_grammar_mappings(self) -> tuple[GrammarMappingRow, ...]:
        return tuple(
            GrammarMappingRow.model_validate(row)
            for row in self._load_jsonl(self._grammar_mapping_path)
        )

    def load_enriched_document(self) -> ImportRegistryDocument:
        return ImportRegistryDocument(
            registry_rows=self.build_enriched_registry(self.load_seed_registry_rows()),
            grammar_mappings=self.build_enriched_grammar_mapping(self.load_seed_grammar_mappings()),
        )

    def seed_document(
        self,
        *,
        registry_rows: Iterable[ImportRegistryRow | Mapping[str, Any]],
        grammar_mappings: Iterable[GrammarMappingRow | Mapping[str, Any]],
    ) -> ImportRegistryDocument:
        return ImportRegistryDocument(
            registry_rows=tuple(_coerce_registry_row(row) for row in registry_rows),
            grammar_mappings=tuple(_coerce_grammar_row(row) for row in grammar_mappings),
        )

    def coverage_summary(self, document: ImportRegistryDocument) -> dict[str, int]:
        return {
            "registry_rows": len(document.registry_rows),
            "grammar_mappings": len(document.grammar_mappings),
            "runtime_targets": len({row.runtime_target for row in document.registry_rows}),
        }

    def registry_summary_report(self, document: ImportRegistryDocument) -> dict[str, Any]:
        return {
            "schema_version": document.schema_version,
            **self.coverage_summary(document),
            "maturity_breakdown": dict(
                Counter(row.maturity_state.value for row in document.registry_rows)
            ),
        }

    def runtime_target_ids(
        self, document: ImportRegistryDocument, runtime_target: RuntimeTarget | str
    ) -> tuple[str, ...]:
        target = RuntimeTarget(runtime_target)
        return tuple(
            row.registry_id for row in document.registry_rows if row.runtime_target == target
        )

    def assert_no_loss(
        self, document: ImportRegistryDocument, *, expected_registry_ids: Iterable[str]
    ) -> None:
        expected = {str(value) for value in expected_registry_ids}
        actual = {row.registry_id for row in document.registry_rows}
        missing = sorted(expected - actual)
        if missing:
            raise AssertionError(f"missing registry ids: {missing}")

    def grammar_mapping_summary_report(self, document: ImportRegistryDocument) -> dict[str, Any]:
        return {
            "grammar_mappings": len(document.grammar_mappings),
            "grammar_role_breakdown": dict(
                Counter(row.grammar_role.value for row in document.grammar_mappings)
            ),
        }

    def grammar_role_ids(
        self, document: ImportRegistryDocument, grammar_role: GrammarRole | str
    ) -> tuple[str, ...]:
        return document.grammar_role_ids(grammar_role)

    def runtime_gap_report(self, document: ImportRegistryDocument) -> list[dict[str, Any]]:
        return [
            _row_report(row)
            for row in document.registry_rows
            if row.runtime_target == RuntimeTarget.RUNTIME
            and self.infer_readiness(row) != ReadinessState.READY
        ]

    def runtime_depth_report(self, document: ImportRegistryDocument) -> dict[str, int]:
        depths = [row.import_depth for row in document.registry_rows]
        return {"max_depth": max(depths, default=0), "min_depth": min(depths, default=0)}

    def executable_backlog_report(self, document: ImportRegistryDocument) -> list[dict[str, Any]]:
        return [
            _row_report(row)
            for row in document.registry_rows
            if row.maturity_state == MaturityState.CANDIDATE and not row.blockers
        ]

    def provenance_depth_audit(self, document: ImportRegistryDocument) -> dict[str, int]:
        return {row.registry_id: row.import_depth for row in document.registry_rows}

    def import_depth_by_role_report(self, document: ImportRegistryDocument) -> dict[str, int]:
        depth_by_registry = {row.registry_id: row.import_depth for row in document.registry_rows}
        result: defaultdict[str, int] = defaultdict(int)
        for mapping in document.grammar_mappings:
            result[mapping.grammar_role.value] = max(
                result[mapping.grammar_role.value], depth_by_registry.get(mapping.registry_id, 0)
            )
        return dict(result)

    def refresh(self) -> ImportRegistryDocument:
        return self.load_enriched_document()

    def write_report(self, path: Path | str, report: Mapping[str, Any]) -> None:
        Path(path).write_text(json.dumps(dict(report), indent=2, sort_keys=True), encoding="utf-8")

    def runtime_target_breakdown(self, document: ImportRegistryDocument) -> dict[str, int]:
        return dict(Counter(row.runtime_target.value for row in document.registry_rows))

    def build_enriched_registry(
        self, rows: Iterable[ImportRegistryRow | Mapping[str, Any]]
    ) -> tuple[ImportRegistryRow, ...]:
        return tuple(_coerce_registry_row(row) for row in rows)

    def build_enriched_grammar_mapping(
        self, rows: Iterable[GrammarMappingRow | Mapping[str, Any]]
    ) -> tuple[GrammarMappingRow, ...]:
        return tuple(_coerce_grammar_row(row) for row in rows)

    def tokenize_text(self, value: str) -> tuple[str, ...]:
        return tuple(token for token in re.split(r"[^A-Za-z0-9]+", value.lower()) if token)

    def infer_readiness(self, row: ImportRegistryRow) -> ReadinessState:
        if row.blockers or row.maturity_state == MaturityState.BLOCKED:
            return ReadinessState.BLOCKED
        if row.runtime_target in {
            RuntimeTarget.RUNTIME,
            RuntimeTarget.REVIEW_ONLY,
            RuntimeTarget.RESEARCH_ONLY,
        }:
            return ReadinessState.READY
        return ReadinessState.NOT_RUNTIME

    def readiness_blockers(self, row: ImportRegistryRow) -> tuple[str, ...]:
        return tuple(row.blockers)

    def runtime_contract_status(self, row: ImportRegistryRow) -> str:
        readiness = self.infer_readiness(row).value
        return f"{row.runtime_target.value}_{readiness}"

    def _load_jsonl(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows


def _coerce_registry_row(row: ImportRegistryRow | Mapping[str, Any]) -> ImportRegistryRow:
    if isinstance(row, ImportRegistryRow):
        return row
    return ImportRegistryRow.model_validate(dict(row))


def _coerce_grammar_row(row: GrammarMappingRow | Mapping[str, Any]) -> GrammarMappingRow:
    if isinstance(row, GrammarMappingRow):
        return row
    return GrammarMappingRow.model_validate(dict(row))


def _row_report(row: ImportRegistryRow) -> dict[str, Any]:
    return row.model_dump(mode="json")
