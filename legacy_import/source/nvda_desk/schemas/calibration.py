"""Typed contracts for deterministic replay, calibration, and stack comparison.

Gate F makes stack definitions, coefficient application, walk-forward slices,
and deterministic comparison reports explicit runtime artefacts rather than
leaving them implied in tests or ad hoc payloads.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.cognition import ReviewExplanationOutput
from nvda_desk.schemas.review import ImportedModuleReviewCitation
from nvda_desk.schemas.state_policy import ResolvedRuntimeSurfaceValue

EXPECTED_REVIEW_STAGES = [
    "temporal",
    "regime",
    "options_flow",
    "posture",
    "eligibility",
    "execution",
]


class ModuleWeightContract(BaseModel):
    """One explicit module-weight override inside a stack or coefficient set."""

    model_config = ConfigDict(extra="forbid")

    module_id: str
    weight: float
    rationale: str = ""


class SubCoefficientContract(BaseModel):
    """One explicit sub-coefficient override inside a stack or coefficient set."""

    model_config = ConfigDict(extra="forbid")

    coefficient_id: str
    weight: float
    coefficient_family: str = "default"
    rationale: str = ""


class StackDefinition(BaseModel):
    """Explicit runtime stack definition used by replay and comparison."""

    model_config = ConfigDict(extra="forbid")

    stack_id: str
    label: str
    description: str = ""
    enabled_playbooks: list[str] = Field(default_factory=list)
    disabled_playbooks: list[str] = Field(default_factory=list)
    module_weights: dict[str, float] = Field(default_factory=dict)
    sub_coefficients: dict[str, float] = Field(default_factory=dict)
    module_weight_contracts: list[ModuleWeightContract] = Field(default_factory=list)
    sub_coefficient_contracts: list[SubCoefficientContract] = Field(default_factory=list)

    @model_validator(mode="after")
    def populate_explicit_contract_lists(self) -> StackDefinition:
        """Mirror dict overrides into explicit contract lists when omitted."""

        if not self.module_weight_contracts:
            self.module_weight_contracts = [
                ModuleWeightContract(module_id=module_id, weight=weight)
                for module_id, weight in sorted(self.module_weights.items())
            ]
        if not self.sub_coefficient_contracts:
            self.sub_coefficient_contracts = [
                SubCoefficientContract(coefficient_id=coefficient_id, weight=weight)
                for coefficient_id, weight in sorted(self.sub_coefficients.items())
            ]
        return self


class CoefficientSet(BaseModel):
    """Named coefficient overrides to apply on top of a stack definition."""

    model_config = ConfigDict(extra="forbid")

    set_id: str
    stack_id: str
    label: str = ""
    module_weights: dict[str, float] = Field(default_factory=dict)
    sub_coefficients: dict[str, float] = Field(default_factory=dict)
    module_weight_contracts: list[ModuleWeightContract] = Field(default_factory=list)
    sub_coefficient_contracts: list[SubCoefficientContract] = Field(default_factory=list)

    @model_validator(mode="after")
    def populate_explicit_contract_lists(self) -> CoefficientSet:
        """Mirror dict overrides into explicit contract lists when omitted."""

        if not self.module_weight_contracts:
            self.module_weight_contracts = [
                ModuleWeightContract(module_id=module_id, weight=weight)
                for module_id, weight in sorted(self.module_weights.items())
            ]
        if not self.sub_coefficient_contracts:
            self.sub_coefficient_contracts = [
                SubCoefficientContract(coefficient_id=coefficient_id, weight=weight)
                for coefficient_id, weight in sorted(self.sub_coefficients.items())
            ]
        return self


class ScenarioExpectation(BaseModel):
    """Expected veto and playbook outcomes for one deterministic scenario."""

    model_config = ConfigDict(extra="forbid")

    expected_veto: bool = False
    expected_playbooks: list[str] = Field(default_factory=list)
    expected_permission_state: str | None = None
    expected_review_stages: list[str] = Field(default_factory=lambda: list(EXPECTED_REVIEW_STAGES))


class ReplayScenarioRecord(BaseModel):
    """One timestamped scenario row for deterministic comparison runs."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    ts: datetime
    payload: dict[str, object]
    expectation: ScenarioExpectation = Field(default_factory=ScenarioExpectation)


class WalkForwardSliceDefinition(BaseModel):
    """One deterministic walk-forward-ready slice."""

    model_config = ConfigDict(extra="forbid")

    slice_id: str
    label: str
    scenario_ids: list[str] = Field(default_factory=list)




class ParallelRiskLaneSurfaceCalibrationMetadata(BaseModel):
    """Evaluation-prep metadata for one implemented parallel-risk lane surface."""

    model_config = ConfigDict(extra="forbid")

    surface_id: str
    behavioural_purpose: str
    expected_directionality: str
    anti_goal: str
    owner_stage: str
    surface_family: str
    review_cadence: str
    activation_state: str
    evidence_sources: list[str] = Field(default_factory=list)


class ParallelRiskLanePolicyCalibrationMetadata(BaseModel):
    """Evaluation-prep metadata for one stable parallel-risk lane policy slice."""

    model_config = ConfigDict(extra="forbid")

    policy_id: str
    policy_family: str
    primary_target_surface: str
    behavioural_purpose: str
    expected_effect: str
    anti_goal: str
    over_tightening_signs: list[str] = Field(default_factory=list)
    redundancy_signs: list[str] = Field(default_factory=list)
    danger_signs: list[str] = Field(default_factory=list)
    review_cadence: str
    evidence_sources: list[str] = Field(default_factory=list)


class ParallelRiskLaneEvaluationPreparationPacket(BaseModel):
    """Lean calibration/evaluation-prep packet for the implemented lane slices."""

    model_config = ConfigDict(extra="forbid")

    lane_id: str
    implemented_surfaces: list[str] = Field(default_factory=list)
    surface_metadata: list[ParallelRiskLaneSurfaceCalibrationMetadata] = Field(default_factory=list)
    policy_metadata: list[ParallelRiskLanePolicyCalibrationMetadata] = Field(default_factory=list)
    required_receipt_sections: list[str] = Field(
        default_factory=lambda: [
            "surface_changes_observed",
            "policy_firing_summary",
            "help_vs_harm_assessment",
            "over_tightening_and_stack_pressure",
            "redundancy_or_dead_weight_findings",
            "danger_or_unstable_behaviour_findings",
            "opportunity_shaping_absence_or_presence",
            "recommended_next_action",
        ]
    )
    selective_proof_order: list[str] = Field(
        default_factory=lambda: [
            "parallel_risk_runtime_targeted",
            "parallel_risk_review_targeted",
            "imported_child_pack_continuity",
            "vocabulary_build_then_hygiene",
        ]
    )
    notes: list[str] = Field(default_factory=list)


class GovernedCoefficientSnapshot(BaseModel):
    """Stable governed-coefficient evidence bound to replay and horizon outputs."""

    model_config = ConfigDict(extra="forbid")

    snapshot_id: str
    authority_version: str
    resolved_surfaces: list[ResolvedRuntimeSurfaceValue] = Field(default_factory=list)


class CoefficientAuditPacket(BaseModel):
    """Concrete record of weights and coefficients applied to one run."""

    model_config = ConfigDict(extra="forbid")

    stack_id: str
    enabled_playbooks: list[str] = Field(default_factory=list)
    disabled_playbooks: list[str] = Field(default_factory=list)
    applied_module_weights: dict[str, float] = Field(default_factory=dict)
    applied_sub_coefficients: dict[str, float] = Field(default_factory=dict)
    scoring_components: dict[str, float] = Field(default_factory=dict)
    governed_coefficient_snapshot_id: str | None = None


class ReplayPacketLineage(BaseModel):
    """Typed replay lineage surface bound to one replay run result."""

    model_config = ConfigDict(extra="forbid")

    protocol_version: Literal["dmp.v3"] = "dmp.v3"
    replay_trace_id: str
    review_packet_id: str
    decision_packet_id: str
    packet_lineage: list[str] = Field(default_factory=list)
    stage_packet_ids: dict[str, str] = Field(default_factory=dict)


class ReplayRunResult(BaseModel):
    """One deterministic replay run result for a coefficient set."""

    model_config = ConfigDict(extra="forbid")

    coefficient_set_id: str
    stack_id: str
    scenario_id: str
    permission_state: str
    active_playbook_ids: list[str] = Field(default_factory=list)
    target_fresh_deployable_pct: float
    replay_score: float
    governed_coefficient_snapshot: GovernedCoefficientSnapshot | None = None
    veto_expected: bool
    veto_observed: bool
    veto_correct: float = Field(ge=0.0, le=1.0)
    contradiction_count: int = 0
    contradiction_rate: float = Field(ge=0.0, le=1.0)
    playbook_precision: float = Field(ge=0.0, le=1.0)
    review_completeness: float = Field(ge=0.0, le=1.0)
    conflict_count: int = 0
    coefficient_audit: CoefficientAuditPacket
    review: ReviewExplanationOutput
    imported_module_citations: list[ImportedModuleReviewCitation] = Field(default_factory=list)
    imported_module_maturity_counts: dict[str, int] = Field(default_factory=dict)
    packet_lineage: ReplayPacketLineage | None = None


class ComparisonMetrics(BaseModel):
    """Stable metrics used to compare deterministic replay runs."""

    model_config = ConfigDict(extra="forbid")

    run_count: int = Field(ge=0)
    veto_rate: float = Field(ge=0.0, le=1.0)
    veto_correctness_rate: float = Field(ge=0.0, le=1.0)
    mean_fresh_deployable_pct: float = Field(ge=0.0)
    mean_replay_score: float = Field(ge=0.0)
    mean_contradiction_rate: float = Field(ge=0.0, le=1.0)
    mean_playbook_precision: float = Field(ge=0.0, le=1.0)
    review_completeness_rate: float = Field(ge=0.0, le=1.0)
    active_playbook_rate: float = Field(ge=0.0, le=1.0)
    mean_active_playbook_count: float = Field(ge=0.0)
    mean_conflict_count: float = Field(ge=0.0)


class StackVersusStackSummary(BaseModel):
    """Stable delta surface for one stack-versus-stack comparison pair."""

    model_config = ConfigDict(extra="forbid")

    left_set_id: str
    right_set_id: str
    left_stack_id: str
    right_stack_id: str
    delta_mean_replay_score: float
    delta_veto_correctness_rate: float
    delta_mean_playbook_precision: float
    delta_mean_fresh_deployable_pct: float


class ComparisonReport(BaseModel):
    """Deterministic comparison report across one or more coefficient sets."""

    model_config = ConfigDict(extra="forbid")

    fixture_pack_id: str | None = None
    scenario_ids: list[str] = Field(default_factory=list)
    reports: dict[str, ComparisonMetrics] = Field(default_factory=dict)
    slice_reports: dict[str, dict[str, ComparisonMetrics]] = Field(default_factory=dict)
    coefficient_snapshots_by_set: dict[str, list[GovernedCoefficientSnapshot]] = Field(default_factory=dict)
    stack_vs_stack_summary: list[StackVersusStackSummary] = Field(default_factory=list)


class ReplayFixturePack(BaseModel):
    """Checked-in deterministic replay regression fixture pack."""

    model_config = ConfigDict(extra="forbid")

    fixture_pack_id: str
    stack_definitions: list[StackDefinition] = Field(default_factory=list)
    coefficient_sets: list[CoefficientSet] = Field(default_factory=list)
    scenarios: list[ReplayScenarioRecord] = Field(default_factory=list)
    walk_forward_slices: list[WalkForwardSliceDefinition] = Field(default_factory=list)


class WalkForwardWindowMode(StrEnum):
    """Bounded window-generation modes for the Gate 79 harness."""

    ANCHORED = "anchored"
    ROLLING = "rolling"


class WalkForwardWindowRole(StrEnum):
    """One chronology role inside a generated walk-forward block."""

    CALIBRATION = "calibration"
    VALIDATION = "validation"
    FORWARD = "forward"


class ChronologyRule(StrEnum):
    """Frozen no-leakage rules for review-horizon discovery windows."""

    STRICT_FORWARD_ONLY = "strict_forward_only"
    ADJACENT_SLICES_ONLY = "adjacent_slices_only"
    NO_FUTURE_LEAKAGE = "no_future_leakage"


class OffsetComparisonOutcome(StrEnum):
    """How multiple start offsets behaved for one candidate horizon."""

    CONSISTENT = "consistent"
    OFFSET_SENSITIVE = "offset_sensitive"
    FLAPPING = "flapping"


class HorizonDiscoveryOutcome(StrEnum):
    """Bounded Gate 79 outcomes for review-horizon discovery."""

    STABLE_HORIZON_FOUND = "stable_horizon_found"
    OFFSET_SENSITIVE = "offset_sensitive"
    NO_STABLE_HORIZON_FOUND = "no_stable_horizon_found"
    COVERAGE_INSUFFICIENT = "coverage_insufficient"


class DownstreamConsumerMode(StrEnum):
    """Permitted downstream interpretation of Gate 79 outputs."""

    REVIEW_CONTEXT_ONLY = "review_context_only"
    CANDIDATE_CONTEXT_ONLY = "candidate_context_only"
    RESEARCH_RESET_CONTEXT_ONLY = "research_reset_context_only"


class WalkForwardStartOffset(BaseModel):
    """One allowed starting offset for harness window generation."""

    model_config = ConfigDict(extra="forbid")

    offset_id: str
    offset_sessions: int = Field(ge=0)


class StabilityComparisonRule(BaseModel):
    """Frozen spread thresholds used to decide whether a horizon is stable."""

    model_config = ConfigDict(extra="forbid")

    max_replay_score_spread: float = Field(ge=0.0, default=0.25)
    max_veto_correctness_spread: float = Field(ge=0.0, default=0.25)
    max_playbook_precision_spread: float = Field(ge=0.0, default=0.25)
    max_fresh_deployable_spread: float = Field(ge=0.0, default=20.0)
    max_active_playbook_rate_spread: float = Field(ge=0.0, default=0.35)
    max_conflict_count_spread: float = Field(ge=0.0, default=1.5)
    min_review_completeness_rate: float = Field(ge=0.0, le=1.0, default=0.9)
    minimum_forward_windows: int = Field(ge=1, default=2)


class WalkForwardWindowContract(BaseModel):
    """One generated chronology-safe window inside the harness contract."""

    model_config = ConfigDict(extra="forbid")

    window_id: str
    surface_key: str
    mode: WalkForwardWindowMode
    role: WalkForwardWindowRole
    block_sessions: int = Field(ge=1)
    offset_id: str
    start_index: int = Field(ge=0)
    end_index: int = Field(ge=0)
    scenario_ids: list[str] = Field(default_factory=list)


class ContextSliceReport(BaseModel):
    """Coverage counts for one event/regime/session slice label."""

    model_config = ConfigDict(extra="forbid")

    dimension: str
    label: str
    scenario_count: int = Field(ge=0, default=0)
    window_count: int = Field(ge=0, default=0)


class FragilitySignalReport(BaseModel):
    """Gate 79 fragility summary that later research can consume."""

    model_config = ConfigDict(extra="forbid")

    hidden_fragility_detected: bool = False
    offset_sensitive_surface_keys: list[str] = Field(default_factory=list)
    unstable_surface_keys: list[str] = Field(default_factory=list)
    economic_axis_failures: dict[str, list[str]] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)


class AblationSignalReport(BaseModel):
    """Bounded ablation and module-pruning hints, without executing search."""

    model_config = ConfigDict(extra="forbid")

    suspected_missing_modules: list[str] = Field(default_factory=list)
    pruning_candidates: list[str] = Field(default_factory=list)
    economic_axis_failures: dict[str, list[str]] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)


class HorizonDiscoveryBinding(BaseModel):
    """Frozen downstream bindings for review, candidate, and research consumers."""

    model_config = ConfigDict(extra="forbid")

    review_consumer_mode: DownstreamConsumerMode = DownstreamConsumerMode.REVIEW_CONTEXT_ONLY
    candidate_consumer_mode: DownstreamConsumerMode = DownstreamConsumerMode.CANDIDATE_CONTEXT_ONLY
    research_consumer_mode: DownstreamConsumerMode = (
        DownstreamConsumerMode.RESEARCH_RESET_CONTEXT_ONLY
    )
    notes: list[str] = Field(default_factory=list)


class GroupReviewHorizonResult(BaseModel):
    """Review-horizon discovery result for one coefficient group or policy surface."""

    model_config = ConfigDict(extra="forbid")

    surface_key: str
    outcome: HorizonDiscoveryOutcome
    smallest_stable_forward_block: int | None = Field(default=None, ge=1)
    evaluated_window_ids: list[str] = Field(default_factory=list)
    stable_offset_ids: list[str] = Field(default_factory=list)
    unstable_offset_ids: list[str] = Field(default_factory=list)
    offset_outcome: OffsetComparisonOutcome
    ranking_consistent: bool = False
    decision_distribution_consistent: bool = False
    economic_behaviour_consistent: bool = False
    notes: list[str] = Field(default_factory=list)


class WalkForwardHarnessAuthorityPacket(BaseModel):
    """Frozen Gate 79 authority packet for review-horizon discovery harness rules."""

    model_config = ConfigDict(extra="forbid")

    harness_id: str
    window_mode: WalkForwardWindowMode = WalkForwardWindowMode.ANCHORED
    calibration_window: int = Field(ge=1)
    validation_window: int = Field(ge=1)
    candidate_forward_blocks: list[int] = Field(default_factory=list)
    step_size: int = Field(ge=1, default=1)
    start_offsets: list[WalkForwardStartOffset] = Field(default_factory=list)
    chronology_rules: list[ChronologyRule] = Field(
        default_factory=lambda: [
            ChronologyRule.STRICT_FORWARD_ONLY,
            ChronologyRule.ADJACENT_SLICES_ONLY,
            ChronologyRule.NO_FUTURE_LEAKAGE,
        ]
    )
    stability_rule: StabilityComparisonRule = Field(default_factory=StabilityComparisonRule)
    surface_keys: list[str] = Field(default_factory=list)
    downstream_binding: HorizonDiscoveryBinding = Field(default_factory=HorizonDiscoveryBinding)
    no_go_language: str = (
        "Do not replace discovered evidence blocks with guessed calendar numbers or folklore horizons."
    )

    @model_validator(mode="after")
    def validate_candidate_blocks(self) -> WalkForwardHarnessAuthorityPacket:
        if not self.candidate_forward_blocks:
            self.candidate_forward_blocks = [1]
        self.candidate_forward_blocks = sorted(set(self.candidate_forward_blocks))
        if not self.start_offsets:
            self.start_offsets = [WalkForwardStartOffset(offset_id="offset_0", offset_sessions=0)]
        if not self.surface_keys:
            self.surface_keys = ["coefficient_groups_default"]
        return self


class HorizonDiscoveryReport(BaseModel):
    """Bounded Gate 79 report surface emitted by the harness service."""

    model_config = ConfigDict(extra="forbid")

    fixture_pack_id: str | None = None
    generated_windows: list[WalkForwardWindowContract] = Field(default_factory=list)
    group_results: list[GroupReviewHorizonResult] = Field(default_factory=list)
    event_slice_reports: list[ContextSliceReport] = Field(default_factory=list)
    regime_slice_reports: list[ContextSliceReport] = Field(default_factory=list)
    session_slice_reports: list[ContextSliceReport] = Field(default_factory=list)
    fragility: FragilitySignalReport = Field(default_factory=FragilitySignalReport)
    ablation: AblationSignalReport = Field(default_factory=AblationSignalReport)
    downstream_binding: HorizonDiscoveryBinding = Field(default_factory=HorizonDiscoveryBinding)
