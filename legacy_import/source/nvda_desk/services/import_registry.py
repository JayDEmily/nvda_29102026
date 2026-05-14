"""Canonical import-registry loading, enrichment, and reporting helpers.

This service treats Gate B as a deterministic build step. Enriched registry and
mapping artefacts are generated from frozen source baselines under
``docs/planning/`` so refreshes do not depend on previously enriched output.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypeVar, cast

from nvda_desk.schemas.import_registry import (
    CanonicalGrammarMappingEntry,
    CanonicalGrammarMappingSeedEntry,
    CanonicalImportRegistryItem,
    CanonicalImportRegistrySeedItem,
    GrammarRole,
    ImplementationReadiness,
    RuntimeContractStatus,
    RuntimeTarget,
)

ROLE_PRIORITY: dict[GrammarRole, int] = {
    GrammarRole.TEMPORAL_CONTEXT: 10,
    GrammarRole.MARKET_REGIME_CONTEXT: 20,
    GrammarRole.OPTIONS_FLOW_CONTEXT: 30,
    GrammarRole.POSTURE_RISK_PERMISSION: 40,
    GrammarRole.PLAYBOOK_ELIGIBILITY: 50,
    GrammarRole.EXPRESSION_EXECUTION: 60,
    GrammarRole.REVIEW_EXPLANATION: 70,
    GrammarRole.EVIDENCE_ONLY: 99,
}
GRAMMAR_ROLE_ORDER: tuple[GrammarRole, ...] = tuple(
    role for role, _ in sorted(ROLE_PRIORITY.items(), key=lambda item: item[1])
)
PLAYBOOK_KEYWORDS: dict[str, tuple[str, ...]] = {
    "continuation_ladder": ("continuation", "trend", "ladder"),
    "negative_gamma_flush": ("gamma", "squeeze", "flush", "dealer"),
    "pin_reversion": ("pin", "magnet", "reversion"),
    "compression_breakout": ("compression", "breakout", "range_break"),
    "front_expiry_pin_pressure": ("front", "expiry", "pin", "pressure"),
    "term_structure_dislocation": ("term", "curve", "dislocation", "tenor"),
    "skew_pressure_reversal": ("skew", "pressure", "reversal", "dealer"),
    "event_suppressed": ("event", "earnings", "macro", "calendar", "analyst"),
    "overnight_carry": ("overnight", "carry", "weekend", "gap"),
}
OPTIONS_KEYWORDS = (
    "option",
    "options",
    "iv",
    "gamma",
    "skew",
    "strike",
    "expiry",
    "chain",
    "pin",
)
INVENTORY_KEYWORDS = (
    "inventory",
    "capital",
    "deployable",
    "exposure",
    "position",
    "thesis",
    "drawdown",
    "adverse",
    "hedge",
    "overnight",
)
STRUCTURED_SOURCE_FORMS = {
    "json_spec",
    "yaml_spec",
    "python_script",
    "implemented_code",
}
REPORT_INPUTS = {
    "registry_seed": "docs/planning/2026-03-23_GATE_B_SOURCE_REGISTRY.jsonl",
    "mapping_seed": "docs/planning/2026-03-23_GATE_B_SOURCE_GRAMMAR_MAPPING.json",
}
OUTPUT_FILES = {
    "registry": "docs/planning/canonical_import_registry.jsonl",
    "mapping": "docs/planning/canonical_grammar_mapping.json",
    "registry_summary": "docs/planning/canonical_import_registry_summary.json",
    "mapping_summary": "docs/planning/canonical_grammar_mapping_summary.json",
    "runtime_depth": "docs/planning/2026-03-23_CANONICAL_RUNTIME_DEPTH_REPORT.json",
    "executable_backlog": "docs/planning/2026-03-23_EXECUTABLE_IMPORT_BACKLOG.json",
    "provenance_depth": "docs/planning/2026-03-23_PROVENANCE_DEPTH_AUDIT.json",
    "import_depth_by_role": "docs/planning/2026-03-23_IMPORT_DEPTH_BY_DESK_ROLE.json",
}

T = TypeVar("T")


class CanonicalImportRegistryService:
    """Load, enrich, and report over canonical registry and grammar artefacts."""

    def __init__(self, project_root: Path):
        self._project_root = project_root

    @property
    def registry_seed_path(self) -> Path:
        """Return the frozen registry-seed JSONL path."""
        return self._project_root / REPORT_INPUTS["registry_seed"]

    @property
    def mapping_seed_path(self) -> Path:
        """Return the frozen mapping-seed JSON path."""
        return self._project_root / REPORT_INPUTS["mapping_seed"]

    @property
    def registry_path(self) -> Path:
        """Return the enriched canonical import-registry JSONL path."""
        return self._project_root / OUTPUT_FILES["registry"]

    @property
    def grammar_mapping_path(self) -> Path:
        """Return the enriched canonical grammar-mapping JSON path."""
        return self._project_root / OUTPUT_FILES["mapping"]

    def load_registry_seed(self) -> list[CanonicalImportRegistrySeedItem]:
        """Load the frozen source registry used for deterministic Gate-B refreshes."""
        return self._load_jsonl(self.registry_seed_path, CanonicalImportRegistrySeedItem)

    def load_mapping_seed(self) -> list[CanonicalGrammarMappingSeedEntry]:
        """Load the frozen source grammar mapping used for deterministic refreshes."""
        raw = json.loads(self.mapping_seed_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not isinstance(raw.get("items"), list):
            raise TypeError(
                "gate-b source grammar mapping must be a JSON object with an items list"
            )
        return [CanonicalGrammarMappingSeedEntry.model_validate(item) for item in raw["items"]]

    def load_registry(self) -> list[CanonicalImportRegistryItem]:
        """Load and validate the enriched canonical import registry."""
        return self._load_jsonl(self.registry_path, CanonicalImportRegistryItem)

    def load_mapping(self) -> list[CanonicalGrammarMappingEntry]:
        """Load and validate the enriched canonical grammar mapping."""
        raw = json.loads(self.grammar_mapping_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not isinstance(raw.get("items"), list):
            raise TypeError("canonical grammar mapping must be a JSON object with an items list")
        return [CanonicalGrammarMappingEntry.model_validate(item) for item in raw["items"]]

    def coverage_summary(self) -> dict[str, int]:
        """Return a small coverage summary for registry and mapping consistency."""
        registry_ids = {item.canonical_id for item in self.load_registry()}
        mapping_ids = {item.canonical_id for item in self.load_mapping()}
        return {
            "registry_count": len(registry_ids),
            "mapping_count": len(mapping_ids),
            "orphan_count": len(registry_ids.symmetric_difference(mapping_ids)),
        }

    def registry_summary(self) -> dict[str, object]:
        """Return deterministic registry counts across preservation dimensions."""
        registry = self.load_registry()
        item_class_counts = Counter(item.item_class for item in registry)
        maturity_counts = Counter(item.maturity_state.value for item in registry)
        runtime_target_counts = Counter(item.runtime_target.value for item in registry)
        readiness_counts = Counter(
            item.implementation_readiness.value
            for item in registry
            if item.implementation_readiness
        )
        source_form_counts: Counter[str] = Counter()
        for item in registry:
            source_form_counts.update(record.source_form.value for record in item.provenance)
        return {
            "total_items": len(registry),
            "coverage_summary": self.coverage_summary(),
            "item_class_counts": dict(sorted(item_class_counts.items())),
            "maturity_counts": dict(sorted(maturity_counts.items())),
            "runtime_target_counts": dict(sorted(runtime_target_counts.items())),
            "readiness_counts": dict(sorted(readiness_counts.items())),
            "source_form_counts": dict(sorted(source_form_counts.items())),
            "report_inputs": REPORT_INPUTS,
        }

    def canonical_ids_for_runtime_target(self, runtime_target: str) -> list[str]:
        """Return sorted canonical IDs for one runtime target."""
        return sorted(
            item.canonical_id
            for item in self.load_registry()
            if item.runtime_target.value == runtime_target
        )

    def assert_no_loss(self, *, expected_total: int) -> None:
        """Raise if the canonical registry count drifts from the preserved universe."""
        actual_total = len(self.load_registry())
        if actual_total != expected_total:
            raise ValueError(
                f"canonical import registry count drifted: expected {expected_total}, got {actual_total}"
            )

    def grammar_mapping_summary(self) -> dict[str, object]:
        """Return deterministic role and runtime summaries for the grammar mapping."""
        mapping = self.load_mapping()
        grammar_role_counts = Counter(item.grammar_role.value for item in mapping)
        architecture_role_counts = Counter(item.architecture_role.value for item in mapping)
        runtime_target_counts = Counter(item.runtime_target.value for item in mapping)
        implementation_state_counts = Counter(item.implementation_state.value for item in mapping)
        contract_status_counts = Counter(
            item.runtime_contract_status.value for item in mapping if item.runtime_contract_status
        )
        return {
            "total_items": len(mapping),
            "grammar_role_counts": dict(sorted(grammar_role_counts.items())),
            "architecture_role_counts": dict(sorted(architecture_role_counts.items())),
            "runtime_target_counts": dict(sorted(runtime_target_counts.items())),
            "implementation_state_counts": dict(sorted(implementation_state_counts.items())),
            "runtime_contract_status_counts": dict(sorted(contract_status_counts.items())),
            "runtime_gap_report": self.runtime_gap_report(),
            "report_inputs": REPORT_INPUTS,
        }

    def grammar_role_ids(self, grammar_role: str) -> list[str]:
        """Return sorted canonical IDs for one grammar role."""
        return sorted(
            item.canonical_id
            for item in self.load_mapping()
            if item.grammar_role.value == grammar_role
        )

    def runtime_gap_report(self) -> dict[str, object]:
        """Return a deterministic gap report between runtime targets and grammar roles."""
        mapping = self.load_mapping()
        roles: dict[str, dict[str, int]] = {}
        for role in GRAMMAR_ROLE_ORDER:
            role_items = [item for item in mapping if item.grammar_role == role]
            if not role_items:
                continue
            roles[role.value] = {
                target.value: sum(1 for item in role_items if item.runtime_target == target)
                for target in RuntimeTarget
            }
        return {"total_items": len(mapping), "roles": roles}

    def runtime_depth_report(self) -> dict[str, object]:
        """Return runtime-target depth counts split by class, category, and desk role."""
        registry = self.load_registry()
        mapping = self.load_mapping()
        by_item_class = self._runtime_target_breakdown(registry, lambda item: item.item_class)
        by_category = self._runtime_target_breakdown(registry, lambda item: item.category)
        by_runtime_target = Counter(item.runtime_target.value for item in registry)
        by_grammar_role: dict[str, dict[str, int]] = {}
        for role in GRAMMAR_ROLE_ORDER:
            role_rows = [item for item in mapping if item.grammar_role == role]
            if not role_rows:
                continue
            by_grammar_role[role.value] = {
                "priority": ROLE_PRIORITY[role],
                "total_items": len(role_rows),
                **{
                    target.value: sum(1 for item in role_rows if item.runtime_target == target)
                    for target in RuntimeTarget
                },
            }
        return {
            "total_items": len(registry),
            "by_item_class": by_item_class,
            "by_category": by_category,
            "by_runtime_target": dict(sorted(by_runtime_target.items())),
            "by_grammar_role": by_grammar_role,
            "report_inputs": REPORT_INPUTS,
        }

    def executable_backlog_view(self) -> dict[str, object]:
        """Return the executable backlog excluding evidence-only artefacts."""
        registry = self.load_registry()
        executable_items = [
            item for item in registry if item.runtime_target != RuntimeTarget.EVIDENCE_ONLY
        ]
        readiness_counts = Counter(
            item.implementation_readiness.value
            for item in executable_items
            if item.implementation_readiness
        )
        role_counts = Counter(
            item.primary_grammar_role.value
            for item in executable_items
            if item.primary_grammar_role is not None
        )
        sorted_items = sorted(
            executable_items,
            key=lambda item: (item.desk_role_priority, item.canonical_slug),
        )
        return {
            "total_items": len(registry),
            "executable_backlog_count": len(executable_items),
            "excluded_evidence_only_count": len(registry) - len(executable_items),
            "by_readiness": dict(sorted(readiness_counts.items())),
            "by_grammar_role": dict(sorted(role_counts.items())),
            "items": [
                {
                    "canonical_id": item.canonical_id,
                    "canonical_slug": item.canonical_slug,
                    "primary_grammar_role": (
                        item.primary_grammar_role.value if item.primary_grammar_role else None
                    ),
                    "desk_role_priority": item.desk_role_priority,
                    "implementation_readiness": (
                        item.implementation_readiness.value
                        if item.implementation_readiness
                        else None
                    ),
                    "readiness_blockers": item.readiness_blockers,
                }
                for item in sorted_items
            ],
            "report_inputs": REPORT_INPUTS,
        }

    def provenance_depth_audit(self) -> dict[str, object]:
        """Return provenance-depth counts and IDs for preservation-only artefacts."""
        registry = self.load_registry()
        preservation_only_ids: list[str] = []
        implemented_or_translated_ids: list[str] = []
        structured_source_ids: list[str] = []
        for item in registry:
            source_forms = {record.source_form.value for record in item.provenance}
            if any(source_form in STRUCTURED_SOURCE_FORMS for source_form in source_forms):
                structured_source_ids.append(item.canonical_id)
            if "implemented_code" in source_forms:
                implemented_or_translated_ids.append(item.canonical_id)
            else:
                preservation_only_ids.append(item.canonical_id)
        return {
            "total_items": len(registry),
            "preservation_only_count": len(preservation_only_ids),
            "implemented_or_translated_count": len(implemented_or_translated_ids),
            "structured_source_count": len(structured_source_ids),
            "preservation_only_ids": preservation_only_ids,
            "implemented_or_translated_ids": implemented_or_translated_ids,
            "structured_source_ids": structured_source_ids,
            "methodology": {
                "preservation_only": "items without implemented_code provenance",
                "implemented_or_translated": "items with implemented_code provenance",
                "structured_source": "items carrying json_spec, yaml_spec, python_script, or implemented_code provenance",
            },
            "report_inputs": REPORT_INPUTS,
        }

    def import_depth_target_report(self) -> dict[str, object]:
        """Return implemented-runtime depth grouped by desk role priority."""
        registry = self.load_registry()
        registry_by_id = {item.canonical_id: item for item in registry}
        mapping = self.load_mapping()
        rows: list[dict[str, Any]] = []
        for role in GRAMMAR_ROLE_ORDER:
            role_items = [item for item in mapping if item.grammar_role == role]
            if not role_items:
                continue
            implemented_count = sum(
                1 for item in role_items if item.runtime_target == RuntimeTarget.IMPLEMENTED_RUNTIME
            )
            concept_count = sum(
                1 for item in role_items if item.runtime_target == RuntimeTarget.CONCEPT_CONTRACT
            )
            evidence_count = sum(
                1 for item in role_items if item.runtime_target == RuntimeTarget.EVIDENCE_ONLY
            )
            ready_count = sum(
                1
                for item in role_items
                if registry_by_id[item.canonical_id].implementation_readiness
                == ImplementationReadiness.READY_FOR_CONTRACT_IMPORT
            )
            total_items = len(role_items)
            rows.append(
                {
                    "grammar_role": role.value,
                    "desk_role_priority": ROLE_PRIORITY[role],
                    "total_items": total_items,
                    "implemented_runtime_count": implemented_count,
                    "concept_contract_count": concept_count,
                    "evidence_only_count": evidence_count,
                    "remaining_backlog_count": concept_count + evidence_count,
                    "ready_for_contract_import_count": ready_count,
                    "implemented_runtime_pct": round((implemented_count / total_items) * 100, 2),
                }
            )
        return {
            "roles": rows,
            "summary": {
                "total_roles": len(rows),
                "implemented_runtime_count": sum(row["implemented_runtime_count"] for row in rows),
                "ready_for_contract_import_count": sum(
                    row["ready_for_contract_import_count"] for row in rows
                ),
            },
            "report_inputs": REPORT_INPUTS,
        }

    def refresh_registry_surfaces(self) -> None:
        """Rewrite enriched registry, mapping, and Gate-B reports to disk."""
        registry_seed = self.load_registry_seed()
        mapping_seed = self.load_mapping_seed()
        seed_mapping_by_id = {item.canonical_id: item for item in mapping_seed}
        if {item.canonical_id for item in registry_seed} != set(seed_mapping_by_id):
            raise ValueError("Gate-B seed registry and seed mapping cover different canonical IDs")

        registry = self._enriched_registry(registry_seed, seed_mapping_by_id)
        mapping = self._enriched_mapping(
            mapping_seed, {item.canonical_id: item for item in registry}
        )

        self.registry_path.write_text(
            "\n".join(item.model_dump_json() for item in registry) + "\n",
            encoding="utf-8",
        )
        self.grammar_mapping_path.write_text(
            json.dumps({"items": [item.model_dump(mode="json") for item in mapping]}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        self._write_report(OUTPUT_FILES["registry_summary"], self.registry_summary())
        self._write_report(OUTPUT_FILES["mapping_summary"], self.grammar_mapping_summary())
        self._write_report(OUTPUT_FILES["runtime_depth"], self.runtime_depth_report())
        self._write_report(OUTPUT_FILES["executable_backlog"], self.executable_backlog_view())
        self._write_report(OUTPUT_FILES["provenance_depth"], self.provenance_depth_audit())
        self._write_report(OUTPUT_FILES["import_depth_by_role"], self.import_depth_target_report())

    def _write_report(self, relative_path: str, payload: dict[str, object]) -> None:
        """Write one JSON report under docs/planning."""
        report_path = self._project_root / relative_path
        report_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def _load_jsonl(self, path: Path, model: type[T]) -> list[T]:
        """Load one JSONL file into a list of validated models."""
        rows = path.read_text(encoding="utf-8").splitlines()
        validate_json = cast(Any, model).model_validate_json
        return [cast(T, validate_json(line)) for line in rows if line.strip()]

    def _runtime_target_breakdown(
        self,
        rows: Iterable[CanonicalImportRegistryItem],
        group_key: Any,
    ) -> dict[str, dict[str, int]]:
        """Return runtime-target counts for a registry grouping function."""
        row_list = list(rows)
        grouped: dict[str, dict[str, int]] = {}
        for key in sorted({group_key(item) for item in row_list}):
            group_rows = [item for item in row_list if group_key(item) == key]
            grouped[str(key)] = {
                target.value: sum(1 for item in group_rows if item.runtime_target == target)
                for target in RuntimeTarget
            }
        return grouped

    def _enriched_registry(
        self,
        registry_seed: list[CanonicalImportRegistrySeedItem],
        mapping_by_id: dict[str, CanonicalGrammarMappingSeedEntry],
    ) -> list[CanonicalImportRegistryItem]:
        """Return registry rows enriched with readiness, affinity, and priority fields."""
        enriched: list[CanonicalImportRegistryItem] = []
        for item in registry_seed:
            mapping = mapping_by_id[item.canonical_id]
            playbook_affinity = self._infer_playbook_affinity(
                canonical_slug=item.canonical_slug,
                category=item.category,
                summary=item.summary,
                notes=item.notes,
                rationale=mapping.rationale,
            )
            readiness = self._infer_readiness(item)
            enriched.append(
                CanonicalImportRegistryItem(
                    **item.model_dump(mode="python"),
                    primary_grammar_role=mapping.grammar_role,
                    desk_role_priority=ROLE_PRIORITY[mapping.grammar_role],
                    implementation_readiness=readiness,
                    readiness_blockers=self._readiness_blockers(item, readiness),
                    playbook_affinity=playbook_affinity,
                    options_affinity=self._infer_options_affinity(
                        grammar_role=mapping.grammar_role,
                        item=item,
                        rationale=mapping.rationale,
                    ),
                    inventory_affinity=self._infer_inventory_affinity(
                        grammar_role=mapping.grammar_role,
                        item=item,
                        rationale=mapping.rationale,
                    ),
                )
            )
        return enriched

    def _enriched_mapping(
        self,
        mapping_seed: list[CanonicalGrammarMappingSeedEntry],
        registry_by_id: dict[str, CanonicalImportRegistryItem],
    ) -> list[CanonicalGrammarMappingEntry]:
        """Return mapping rows enriched with contract status and affinity fields."""
        enriched: list[CanonicalGrammarMappingEntry] = []
        for item in mapping_seed:
            registry_item = registry_by_id[item.canonical_id]
            enriched.append(
                CanonicalGrammarMappingEntry(
                    **item.model_dump(mode="python"),
                    desk_role_priority=registry_item.desk_role_priority,
                    runtime_contract_status=self._runtime_contract_status(item),
                    playbook_affinity=registry_item.playbook_affinity,
                    options_affinity=registry_item.options_affinity,
                    inventory_affinity=registry_item.inventory_affinity,
                )
            )
        return enriched

    def _infer_playbook_affinity(
        self,
        *,
        canonical_slug: str,
        category: str,
        summary: str,
        notes: str,
        rationale: list[str],
    ) -> list[str]:
        """Infer playbook-family affinity tags from preserved item text."""
        tokens = set(self._text_tokens(canonical_slug, category, summary, notes, *rationale))
        matches = [
            family
            for family, keywords in PLAYBOOK_KEYWORDS.items()
            if any(keyword in tokens for keyword in keywords)
        ]
        return sorted(matches)

    def _infer_options_affinity(
        self,
        *,
        grammar_role: GrammarRole,
        item: CanonicalImportRegistrySeedItem,
        rationale: list[str],
    ) -> bool:
        """Infer whether an item directly supports options-state reasoning."""
        if grammar_role == GrammarRole.OPTIONS_FLOW_CONTEXT:
            return True
        tokens = set(
            self._text_tokens(
                item.canonical_slug,
                item.category,
                item.summary,
                item.notes,
                *item.known_inputs,
                *item.known_outputs,
                *item.known_dependencies,
                *rationale,
            )
        )
        return any(keyword in tokens for keyword in OPTIONS_KEYWORDS)

    def _infer_inventory_affinity(
        self,
        *,
        grammar_role: GrammarRole,
        item: CanonicalImportRegistrySeedItem,
        rationale: list[str],
    ) -> bool:
        """Infer whether an item directly supports inventory and capital governance."""
        if grammar_role in {
            GrammarRole.POSTURE_RISK_PERMISSION,
            GrammarRole.EXPRESSION_EXECUTION,
        }:
            return True
        tokens = set(
            self._text_tokens(
                item.canonical_slug,
                item.category,
                item.summary,
                item.notes,
                *item.known_inputs,
                *item.known_outputs,
                *item.known_dependencies,
                *rationale,
            )
        )
        return any(keyword in tokens for keyword in INVENTORY_KEYWORDS)

    def _text_tokens(self, *parts: str) -> list[str]:
        """Tokenize text parts for deterministic affinity inference."""
        return re.findall(r"[a-z0-9_]+", " ".join(parts).lower())

    def _infer_readiness(self, item: CanonicalImportRegistrySeedItem) -> ImplementationReadiness:
        """Infer a deterministic implementation-readiness state for one item."""
        if item.runtime_target == RuntimeTarget.IMPLEMENTED_RUNTIME:
            return ImplementationReadiness.IMPLEMENTED_RUNTIME
        if item.runtime_target == RuntimeTarget.EVIDENCE_ONLY:
            return ImplementationReadiness.EVIDENCE_ONLY
        source_forms = {record.source_form.value for record in item.provenance}
        has_structured_source = any(
            source_form in STRUCTURED_SOURCE_FORMS for source_form in source_forms
        )
        has_explicit_io = bool(item.known_inputs or item.known_outputs)
        if has_structured_source and has_explicit_io:
            return ImplementationReadiness.READY_FOR_CONTRACT_IMPORT
        return ImplementationReadiness.NEEDS_SCOPE_DEFINITION

    def _readiness_blockers(
        self,
        item: CanonicalImportRegistrySeedItem,
        readiness: ImplementationReadiness,
    ) -> list[str]:
        """Return deterministic readiness blockers for one item."""
        if readiness == ImplementationReadiness.IMPLEMENTED_RUNTIME:
            return []
        if readiness == ImplementationReadiness.EVIDENCE_ONLY:
            return ["evidence_only_preservation"]
        source_forms = {record.source_form.value for record in item.provenance}
        blockers = ["missing_runtime_translation"]
        if not any(source_form in STRUCTURED_SOURCE_FORMS for source_form in source_forms):
            blockers.append("needs_structured_source_form")
        if not item.known_inputs and not item.known_outputs:
            blockers.append("missing_explicit_io_contract")
        blockers.extend(
            f"dependency:{dependency}" for dependency in sorted(item.known_dependencies)
        )
        return blockers

    def _runtime_contract_status(
        self, item: CanonicalGrammarMappingSeedEntry
    ) -> RuntimeContractStatus:
        """Infer the runtime contract completeness state for one mapping entry."""
        if item.runtime_target == RuntimeTarget.IMPLEMENTED_RUNTIME:
            return RuntimeContractStatus.IMPLEMENTED_BINDING_CONTRACT
        if item.runtime_target == RuntimeTarget.EVIDENCE_ONLY:
            return RuntimeContractStatus.EVIDENCE_ONLY_NO_CONTRACT
        return RuntimeContractStatus.CONCEPT_CONTRACT_ONLY


def _project_root() -> Path:
    """Return the repository root from the installed source tree."""
    return Path(__file__).resolve().parents[3]


def main() -> int:
    """Refresh enriched registry artefacts and Gate-B reports on disk."""
    service = CanonicalImportRegistryService(_project_root())
    service.refresh_registry_surfaces()
    print(service.registry_path)
    print(service.grammar_mapping_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
