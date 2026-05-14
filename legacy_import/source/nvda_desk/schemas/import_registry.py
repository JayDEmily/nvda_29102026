"""Typed contracts for canonical import registry and grammar mappings.

These models describe preserved modules, features, and desk-cognition fragments
before or during runtime import. They keep provenance explicit and prevent silent
loss of meaning when preserved concepts are translated into deterministic code.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class SourceFormType(StrEnum):
    """Supported preserved source forms for recovered ideas and modules."""

    PYTHON_SCRIPT = "python_script"
    GATSBY_ARTIFACT = "gatsby_artifact"
    YAML_SPEC = "yaml_spec"
    JSON_SPEC = "json_spec"
    BACKLOG_ENTRY = "backlog_entry"
    MARKDOWN_FRAGMENT = "markdown_fragment"
    IMPLEMENTED_CODE = "implemented_code"
    PHASE_A_REGISTRY = "phase_a_registry"


class MaturityState(StrEnum):
    """Known maturity states for canonical import items."""

    CONCEPTUAL_PRESERVED = "conceptual_preserved"
    PARTIALLY_PROMOTED = "partially_promoted"
    IMPLEMENTED = "implemented"
    EVIDENCE_ONLY = "evidence_only"


class GrammarRole(StrEnum):
    """Binding Desk Cognition Grammar roles."""

    TEMPORAL_CONTEXT = "temporal_context"
    MARKET_REGIME_CONTEXT = "market_regime_context"
    OPTIONS_FLOW_CONTEXT = "options_flow_context"
    POSTURE_RISK_PERMISSION = "posture_risk_permission"
    PLAYBOOK_ELIGIBILITY = "playbook_eligibility"
    EXPRESSION_EXECUTION = "expression_execution"
    REVIEW_EXPLANATION = "review_explanation"
    EVIDENCE_ONLY = "evidence_only"


class ArchitectureRole(StrEnum):
    """Runtime architecture positions for imported items."""

    RAW_INPUT = "raw_input"
    DERIVED_STATE = "derived_state"
    CLASSIFIER = "classifier"
    POSTURE_GATE = "posture_gate"
    PLAYBOOK_QUALIFIER = "playbook_qualifier"
    EXECUTION_COMPONENT = "execution_component"
    REVIEW_COMPONENT = "review_component"
    EVIDENCE_COMPONENT = "evidence_component"


class RuntimeTarget(StrEnum):
    """Current runtime target for an imported item."""

    IMPLEMENTED_RUNTIME = "implemented_runtime"
    CONCEPT_CONTRACT = "concept_contract"
    EVIDENCE_ONLY = "evidence_only"


class ImplementationReadiness(StrEnum):
    """Implementation readiness state for registry-backed import planning."""

    IMPLEMENTED_RUNTIME = "implemented_runtime"
    READY_FOR_CONTRACT_IMPORT = "ready_for_contract_import"
    NEEDS_SCOPE_DEFINITION = "needs_scope_definition"
    EVIDENCE_ONLY = "evidence_only"


class RuntimeContractStatus(StrEnum):
    """Runtime contract completeness for grammar-mapping entries."""

    IMPLEMENTED_BINDING_CONTRACT = "implemented_binding_contract"
    CONCEPT_CONTRACT_ONLY = "concept_contract_only"
    EVIDENCE_ONLY_NO_CONTRACT = "evidence_only_no_contract"


class RegistryProvenance(BaseModel):
    """Provenance record for a canonical import item."""

    model_config = ConfigDict(extra="forbid")

    source_form: SourceFormType
    source_ref: str
    source_origin: str


class CanonicalImportRegistrySeedItem(BaseModel):
    """Frozen pre-enrichment registry row used as the Gate-B source baseline."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    item_class: str
    canonical_name: str
    canonical_slug: str
    category: str
    maturity_state: MaturityState
    runtime_target: RuntimeTarget
    summary: str
    provenance: list[RegistryProvenance] = Field(default_factory=list)
    known_inputs: list[str] = Field(default_factory=list)
    known_outputs: list[str] = Field(default_factory=list)
    known_dependencies: list[str] = Field(default_factory=list)
    related_ids: list[str] = Field(default_factory=list)
    notes: str = ""


class CanonicalImportRegistryItem(CanonicalImportRegistrySeedItem):
    """Canonical registry entry for a recovered idea, feature, or module."""

    primary_grammar_role: GrammarRole | None = None
    desk_role_priority: int = 99
    implementation_readiness: ImplementationReadiness | None = None
    readiness_blockers: list[str] = Field(default_factory=list)
    playbook_affinity: list[str] = Field(default_factory=list)
    options_affinity: bool = False
    inventory_affinity: bool = False


class CanonicalGrammarMappingSeedEntry(BaseModel):
    """Frozen pre-enrichment grammar-mapping row used as the Gate-B baseline."""

    model_config = ConfigDict(extra="forbid")

    canonical_id: str
    canonical_slug: str
    grammar_role: GrammarRole
    architecture_role: ArchitectureRole
    runtime_target: RuntimeTarget
    implementation_state: MaturityState
    implemented_paths: list[str] = Field(default_factory=list)
    rationale: list[str] = Field(default_factory=list)


class CanonicalGrammarMappingEntry(CanonicalGrammarMappingSeedEntry):
    """Grammar and architecture mapping for a canonical import item."""

    desk_role_priority: int = 99
    runtime_contract_status: RuntimeContractStatus | None = None
    playbook_affinity: list[str] = Field(default_factory=list)
    options_affinity: bool = False
    inventory_affinity: bool = False
