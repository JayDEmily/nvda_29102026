"""Build the canonical desk vocabulary document.

The generator stays aligned with the pinned runtime registry and the Gate 60/61
state-policy governance vocabulary so the committed JSON cannot drift from the
authoritative builder.
"""

from __future__ import annotations

from pathlib import Path

from nvda_desk.schemas.playbook_registry import PlaybookHorizon
from nvda_desk.schemas.vocabulary import (
    RawDerivedTag,
    VocabularyCategory,
    VocabularyDocument,
    VocabularyEntry,
)
from nvda_desk.services.playbook_registry import PlaybookRegistryService

OUTPUT_PATH = Path("docs/vocabulary/2026-03-25_CANONICAL_DESK_COGNITION_VOCABULARY.json")


def build_document() -> VocabularyDocument:
    """Return the canonical vocabulary document for the current repo state."""

    registry = PlaybookRegistryService()
    document = registry.document()
    entries: list[VocabularyEntry] = [
        VocabularyEntry(
            canonical_slug="temporal_context",
            canonical_label="Temporal Context",
            category=VocabularyCategory.STAGE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.cognition.TemporalContextOutput",
            allowed_aliases=["step_1", "time_phase_context"],
            notes=["Binding Stage 1 grammar slot."],
        ),
        VocabularyEntry(
            canonical_slug="market_regime_context",
            canonical_label="Market Regime Context",
            category=VocabularyCategory.STAGE,
            stage_owner="market_regime_context",
            maps_to_contract="nvda_desk.schemas.cognition.MarketRegimeContextOutput",
            allowed_aliases=["regime_context"],
        ),
        VocabularyEntry(
            canonical_slug="options_flow_context",
            canonical_label="Options and Flow Context",
            category=VocabularyCategory.STAGE,
            stage_owner="options_flow_context",
            maps_to_contract="nvda_desk.schemas.cognition.OptionsFlowContextOutput",
            allowed_aliases=["options_context", "flow_context"],
        ),
        VocabularyEntry(
            canonical_slug="posture_risk_permission",
            canonical_label="Posture and Risk Permission",
            category=VocabularyCategory.STAGE,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.cognition.PostureRiskOutput",
            allowed_aliases=["posture_risk", "permission_layer"],
            notes=[
                "Gate 237 restores the bounded local permission envelope as the active Step 4 surface and keeps deployable-capital echoes downstream or compatibility-only.",
            ],
        ),
        VocabularyEntry(
            canonical_slug="posture_hard_invariants",
            canonical_label="Posture Hard Invariants",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.cognition.PostureHardInvariantsSurface",
            allowed_aliases=["hard_invariant_surface"],
            notes=[
                "Additive posture-owned hard-stop surface preserved before selector citations or later modifier consequences."
            ],
        ),
        VocabularyEntry(
            canonical_slug="posture_local_envelope",
            canonical_label="Posture Local Envelope",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.cognition.PostureLocalEnvelopeSurface",
            allowed_aliases=["local_envelope_surface"],
            notes=[
                "Additive posture-owned envelope surface preserving base permission, deployable capital, and derisk reasons before downstream annotations.",
                "Legacy deployable-capital echoes remain compatibility-only until later readers are fully retired."
            ],
        ),
        VocabularyEntry(
            canonical_slug="posture_downstream_annotations",
            canonical_label="Posture Downstream Annotations",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.cognition.PostureRiskOutput.downstream_annotations",
            allowed_aliases=["posture_annotation_lineage"],
            notes=[
                "Selector citations and later modifier notes carried separately from posture-owned hard invariants and local envelope."
            ],
        ),
        VocabularyEntry(
            canonical_slug="playbook_eligibility",
            canonical_label="Playbook Eligibility",
            category=VocabularyCategory.STAGE,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.cognition.PlaybookEligibilityOutput",
            allowed_aliases=["selector_layer"],
        ),
        VocabularyEntry(
            canonical_slug="eligibility_admissibility",
            canonical_label="Eligibility Admissibility",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.cognition.EligibilityAdmissibilitySurface",
            allowed_aliases=["stage5_admissibility_surface"],
            notes=[
                "Additive Stage 5 surface preserving admissible and watch-only family, setup-variant, and playbook ids apart from Stage 6 ranking."
            ],
        ),
        VocabularyEntry(
            canonical_slug="expression_execution",
            canonical_label="Expression and Execution",
            category=VocabularyCategory.STAGE,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.cognition.ExecutionExpressionOutput",
            allowed_aliases=["execution_expression"],
            notes=[
                "Gate 239 restores stateless recommendation behaviour at Step 6 and keeps target-deployment semantics out of the recommendation surface.",
            ],
        ),
        VocabularyEntry(
            canonical_slug="execution_candidate_ownership",
            canonical_label="Execution Candidate Ownership",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.cognition.ExecutionCandidateOwnershipSurface",
            allowed_aliases=["stage6_candidate_ownership_surface"],
            notes=[
                "Additive Stage 6 surface preserving the admitted candidate pool seen by execution, adjudicated playbook ids, and the selected lead playbook."
            ],
        ),
        VocabularyEntry(
            canonical_slug="overlay_risk_decision",
            canonical_label="Overlay Risk Decision",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="risk_gateway",
            maps_to_contract="nvda_desk.schemas.risk.RiskDecision",
            allowed_aliases=["market_overlay_decision"],
            notes=[
                "Preserved overlay-evaluation decision carried before posture-aware terminal application reshapes the final risk action."
            ],
        ),
        VocabularyEntry(
            canonical_slug="terminal_risk_application",
            canonical_label="Terminal Risk Application",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="risk_gateway",
            maps_to_contract="nvda_desk.schemas.cognition.TerminalRiskApplicationSurface",
            allowed_aliases=["final_risk_application_surface"],
            notes=[
                "Additive seam preserving overlay decision, final terminal decision, posture permission state, and bounded overlap classes before downstream review migration."
            ],
        ),
        VocabularyEntry(
            canonical_slug="review_explanation",
            canonical_label="Review and Explanation",
            category=VocabularyCategory.STAGE,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.cognition.ReviewExplanationOutput",
            allowed_aliases=["review_packet", "reason_packet"],
        ),
        VocabularyEntry(
            canonical_slug="temporal_state",
            canonical_label="Temporal State",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.temporal_surface.TemporalStateFeaturePayload",
            allowed_aliases=["step1_temporal_state"],
            disallowed_phrases=["hard_clock_truth"],
        ),
        VocabularyEntry(
            canonical_slug="session_clock",
            canonical_label="Session Clock",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.session_clock.SessionClockFeaturePayload",
            allowed_aliases=["session_clock_wrapper"],
            disallowed_phrases=["canonical_step1_truth"],
            notes=["Explicit compatibility wrapper retained over temporal_state."],
        ),
        VocabularyEntry(
            canonical_slug="raw_primitive",
            canonical_label="Raw Primitive",
            category=VocabularyCategory.DATA_CLASSIFICATION,
            stage_owner="research_doctrine",
            raw_or_derived=RawDerivedTag.RAW,
            maps_to_contract="data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx",
            allowed_aliases=["raw_signal"],
        ),
        VocabularyEntry(
            canonical_slug="derived_feature",
            canonical_label="Derived Feature",
            category=VocabularyCategory.DATA_CLASSIFICATION,
            stage_owner="research_doctrine",
            raw_or_derived=RawDerivedTag.DERIVED,
            maps_to_contract="data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx",
            allowed_aliases=["derived_state"],
        ),
        VocabularyEntry(
            canonical_slug="vocabulary_workflow",
            canonical_label="Vocabulary Workflow",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="docs/vocabulary/CONSOLIDATION_WORKFLOW.md",
            allowed_aliases=["consolidation_workflow"],
        ),
        VocabularyEntry(
            canonical_slug="calendar_horizon_gate",
            canonical_label="Calendar Horizon Gate",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="step0_calendar_horizon",
            maps_to_contract="docs/planning/2026-03-26_CALENDAR_HORIZON_OWNERSHIP.md",
            allowed_aliases=["step_0", "horizon_router"],
            notes=[
                "Explicit runtime routing concern that selects intraday vs carry evaluation horizon."
            ],
        ),
        VocabularyEntry(
            canonical_slug="candidate_family_generation",
            canonical_label="Candidate Family Generation",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="docs/planning/2026-03-26_COGNITIVE_WORKFLOW_IMPLEMENTATION_MAP.md",
            allowed_aliases=["family_generation", "candidate_setup_generation"],
            notes=["Owned by the playbook-selection grammar slot rather than Step 1 or posture."],
        ),
        VocabularyEntry(
            canonical_slug="playbook_family",
            canonical_label="Playbook Family",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookFamilySpec",
            allowed_aliases=["family_layer"],
        ),
        VocabularyEntry(
            canonical_slug="setup_variant",
            canonical_label="Setup Variant",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="playbook_eligibility",
            maps_to_contract="nvda_desk.schemas.playbook_registry.SetupVariantSpec",
            allowed_aliases=["deterministic_setup_variant"],
        ),
        VocabularyEntry(
            canonical_slug="execution_expression",
            canonical_label="Execution Expression",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.playbook_registry.ExecutionTemplateSpec",
            allowed_aliases=["execution_shape"],
        ),
        VocabularyEntry(
            canonical_slug="carry_handoff",
            canonical_label="Carry Handoff",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="carry_horizon",
            maps_to_contract="nvda_desk.schemas.overnight.CloseStateCarryHandoff",
            allowed_aliases=["close_state_handoff"],
            notes=[
                "Typed bridge from intraday close-state into overnight/weekend/event carry evaluation."
            ],
        ),
        VocabularyEntry(
            canonical_slug="carry_horizon_branch",
            canonical_label="Carry Horizon Branch",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="carry_horizon",
            maps_to_contract="nvda_desk.schemas.overnight.CarryHorizon",
            allowed_aliases=["carry_branch"],
            notes=["Separate horizon branch for overnight, weekend, and event carry decisions."],
        ),
        VocabularyEntry(
            canonical_slug="position_context",
            canonical_label="Position Context",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.cognition.PositionContextInput",
            allowed_aliases=["managed_position_context"],
            notes=[
                "Additive execution-stage ingress slot for the bounded managed-position specimen context."
            ],
        ),
        VocabularyEntry(
            canonical_slug="lifecycle_plan",
            canonical_label="Lifecycle Plan",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="expression_execution",
            maps_to_contract="nvda_desk.schemas.cognition.LifecyclePlanOutput",
            allowed_aliases=["second_half_plan"],
            notes=[
                "Additive execution-stage egress slot for the bounded second-half lifecycle plan."
            ],
        ),
        VocabularyEntry(
            canonical_slug="stage_local_handoff",
            canonical_label="Stage-Local Handoff",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.cognition.StageLocalHandoffSurface",
            allowed_aliases=["handoff_surface"],
            notes=[
                "Additive review-visible handoff surface preserving cited posture, cited eligibility, pre-final execution, and terminal risk decision without changing stage order."
            ],
        ),
        VocabularyEntry(
            canonical_slug="terminal_risk_decision",
            canonical_label="Terminal Risk Decision",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.risk.RiskDecision",
            allowed_aliases=["final_risk_decision"],
            notes=[
                "Preserved terminal risk decision carried inside the stage-local handoff surface before final join mutates execution."
            ],
        ),
        VocabularyEntry(
            canonical_slug="state_vector",
            canonical_label="State Vector",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.cognition.RuntimeStateVector",
            allowed_aliases=["approved_state_vector"],
            notes=[
                "Gate 60 freezes the readable runtime state fields before policy matrices exist."
            ],
        ),
        VocabularyEntry(
            canonical_slug="baseline_coefficient",
            canonical_label="Baseline Coefficient",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.RuntimeSurfaceClass",
            allowed_aliases=["release_coefficient"],
            disallowed_phrases=["live_tuning"],
            notes=[
                "May change only through reviewed release, never through runtime self-adjustment."
            ],
        ),
        VocabularyEntry(
            canonical_slug="state_conditioned_modifier",
            canonical_label="State-Conditioned Modifier",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.ModifierPolicySpec",
            allowed_aliases=["bounded_modifier"],
            disallowed_phrases=["freeform_override"],
            notes=[
                "Approved runtime policy object that deforms posture without mutating cognition grammar."
            ],
        ),
        VocabularyEntry(
            canonical_slug="effective_coefficient",
            canonical_label="Effective Coefficient",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.EffectiveCoefficientLineage",
            allowed_aliases=["effective_policy_surface"],
            notes=["Lawful baseline-plus-modifier result recorded for review lineage."],
        ),
        VocabularyEntry(
            canonical_slug="precursor_stitching",
            canonical_label="Precursor Stitching",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.market.PrecursorStitchingAuthorityPacket",
            allowed_aliases=["precursor_fallback_law", "precursor_contradiction_law"],
            notes=[
                "Gate 75 freezes venue order, fallback, stale-data, and contradiction handling before runtime binding."
            ],
        ),
        VocabularyEntry(
            canonical_slug="precursor_runtime_packet",
            canonical_label="Precursor Runtime Packet",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.market.PrecursorRuntimePacket",
            allowed_aliases=["precursor_context_packet"],
            notes=["Gate 76 preserves precursor truth additively into runtime and review packets."],
        ),
        VocabularyEntry(
            canonical_slug="financial_calendar_reference_bundle",
            canonical_label="Financial Calendar Reference Bundle",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.financial_calendar.FinancialCalendarBundleMetadata",
            allowed_aliases=["financial_calendar_bundle"],
            notes=[
                "Repo-controlled scheduled-facts artefact lane for the post-Gate-87 financial-calendar tranche."
            ],
        ),
        VocabularyEntry(
            canonical_slug="financial_calendar_crosswalk",
            canonical_label="Financial Calendar Crosswalk",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.financial_calendar.FinancialCalendarCrosswalkRecord",
            allowed_aliases=["calendar_crosswalk"],
            notes=[
                "Deterministic mapping from bundle fact families into canonical calendar, event, precursor, and temporal surfaces."
            ],
        ),
        VocabularyEntry(
            canonical_slug="financial_calendar_import_record",
            canonical_label="Financial Calendar Import Record",
            category=VocabularyCategory.DATA_CLASSIFICATION,
            stage_owner="temporal_context",
            raw_or_derived=RawDerivedTag.RAW,
            maps_to_contract="nvda_desk.schemas.financial_calendar.FinancialCalendarImportedRecord",
            allowed_aliases=["calendar_import_record"],
            notes=[
                "Provenance-bearing import-stage record retained before Gate 91 canonical projection."
            ],
        ),
        VocabularyEntry(
            canonical_slug="review_failure_taxonomy",
            canonical_label="Review Failure Taxonomy",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.review.ReviewFailurePacket",
            allowed_aliases=["failure_classification_packet"],
            notes=[
                "Gate 77 freezes trader-grade failure classes and non-action outputs for later review and promotion evidence."
            ],
        ),
        VocabularyEntry(
            canonical_slug="modifier_runtime_packet",
            canonical_label="Modifier Runtime Packet",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="posture_risk",
            maps_to_contract="nvda_desk.schemas.state_policy.ModifierRuntimePacket",
            allowed_aliases=["runtime_modifier_packet", "effective_modifier_packet"],
            notes=[
                "Gate 78 materialises one typed runtime packet carrying effective coefficients, kill-switch outcomes, and modifier lineage."
            ],
        ),
        VocabularyEntry(
            canonical_slug="modifier_compatibility_bridge",
            canonical_label="Modifier Compatibility Bridge",
            category=VocabularyCategory.COMPATIBILITY_SURFACE,
            stage_owner="state_conditioned_modifier",
            maps_to_contract="nvda_desk.schemas.cognition.ModifierCompatibilityBridgeSurface",
            allowed_aliases=["compatibility_bridge_surface"],
            notes=[
                "Explicit additive bridge showing which posture or execution fields were changed from the modifier runtime packet while the packet remains the authority."
            ],
        ),
        VocabularyEntry(
            canonical_slug="prohibited_runtime_variation",
            canonical_label="Prohibited Runtime Variation",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="planning_governance",
            maps_to_contract="nvda_desk.schemas.state_policy.ProhibitedRuntimeSurface",
            allowed_aliases=["locked_surface"],
            disallowed_phrases=["runtime_rewrite"],
            notes=[
                "Surfaces such as grammar order, calendar truth, and baseline values remain locked at runtime."
            ],
        ),
        VocabularyEntry(
            canonical_slug="stand_down_class",
            canonical_label="Stand-Down Class",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.NonActionClass",
            allowed_aliases=["non_action_class"],
            notes=["Gate 61 makes disciplined non-participation a first-class governed outcome."],
        ),
        VocabularyEntry(
            canonical_slug="conflict_class",
            canonical_label="Conflict Class",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.SignalConflictClass",
            allowed_aliases=["signal_conflict_class"],
            notes=[
                "Ordered conflict severity remains visible in review rather than being silently absorbed."
            ],
        ),
        VocabularyEntry(
            canonical_slug="degradation_step",
            canonical_label="Degradation Step",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="posture_risk_permission",
            maps_to_contract="nvda_desk.schemas.state_policy.DegradationStep",
            allowed_aliases=["posture_degradation_step"],
            notes=["Ordered ladder from confirmation tightening through stand-down and veto."],
        ),
        VocabularyEntry(
            canonical_slug="override_disposition",
            canonical_label="Override Disposition",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.OverrideDisposition",
            allowed_aliases=["override_status"],
            disallowed_phrases=["trader_feel_override"],
            notes=[
                "Gate 61 forbids smuggled discretionary runtime behaviour and allows only bounded audit/release pathways."
            ],
        ),
        VocabularyEntry(
            canonical_slug="stability_scorecard",
            canonical_label="Stability Scorecard",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.SurfaceStabilityScorecard",
            allowed_aliases=["surface_scorecard"],
            notes=[
                "Gate 62 freezes the multi-axis stability surface before review law or candidate comparison."
            ],
        ),
        VocabularyEntry(
            canonical_slug="corridor_zone",
            canonical_label="Corridor Zone",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.CorridorZone",
            allowed_aliases=["target_drift_breach_zone"],
            notes=[
                "Target, tolerated-drift, and breach zones remain explicit in governed scorecards."
            ],
        ),
        VocabularyEntry(
            canonical_slug="review_evidence_block",
            canonical_label="Review Evidence Block",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.ReviewEvidenceBlock",
            allowed_aliases=["evidence_floor_block"],
            notes=[
                "Gate 63 requires explicit evidence floors before a surface may become review-eligible."
            ],
        ),
        VocabularyEntry(
            canonical_slug="review_outcome",
            canonical_label="Review Outcome",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.ReviewOutcome",
            allowed_aliases=["governed_review_outcome"],
            notes=[
                "Includes review_not_eligible and review_no_change as first-class governed results."
            ],
        ),
        VocabularyEntry(
            canonical_slug="candidate_role",
            canonical_label="Candidate Role",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.CandidateRole",
            allowed_aliases=["candidate_state_role"],
            notes=[
                "Gate 64 limits candidate roles to champion, shadow challenger, dormant candidate, and retired candidate."
            ],
        ),
        VocabularyEntry(
            canonical_slug="adjudication_disposition",
            canonical_label="Adjudication Disposition",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.AdjudicationDisposition",
            allowed_aliases=["reserved_span_state"],
            notes=[
                "The reserved adjudication span stays explicit so live paper cannot quietly exhaust it."
            ],
        ),
        VocabularyEntry(
            canonical_slug="event_taxonomy",
            canonical_label="Event Taxonomy",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.events.EventTaxonomyAuthorityPacket",
            allowed_aliases=["bounded_event_identity"],
            notes=[
                "Gate 65 freezes desk-relevant event classes, subclasses, materiality, and semantic phases."
            ],
        ),
        VocabularyEntry(
            canonical_slug="desk_calendar_contract",
            canonical_label="Desk Calendar Contract",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.session_clock.DeskCalendarAuthorityPacket",
            allowed_aliases=["venue_calendar_authority"],
            notes=[
                "Gate 66 freezes venue/timezone/closure/bridge semantics before runtime plumbing."
            ],
        ),
        VocabularyEntry(
            canonical_slug="event_window_state",
            canonical_label="Event Window State",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.temporal_surface.EventWindowAuthorityPacket",
            allowed_aliases=["event_window_semantics"],
            notes=[
                "Gate 67 freezes event proximity, overlap, cooling-off, and event-memory semantics before later policy gates."
            ],
        ),
        VocabularyEntry(
            canonical_slug="precursor_universe",
            canonical_label="Precursor Universe",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="market_context",
            maps_to_contract="nvda_desk.schemas.market.PrecursorUniverseAuthorityPacket",
            allowed_aliases=["asia_precursor_context"],
            notes=[
                "Gate 68 freezes the bounded ex-US precursor venue universe plus approved raw and derived field families."
            ],
        ),
        VocabularyEntry(
            canonical_slug="phase_carry_policy",
            canonical_label="Phase Carry Policy",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="posture_risk",
            maps_to_contract="nvda_desk.schemas.risk.PhaseCarryoverPolicyAuthorityPacket",
            allowed_aliases=["ordinary_session_policy_matrix"],
            notes=[
                "Gate 69 freezes ordinary day-phase and carryover posture law before later event-stress matrices."
            ],
        ),
        VocabularyEntry(
            canonical_slug="event_options_stress_policy",
            canonical_label="Event and Options-Stress Policy",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="posture_risk",
            maps_to_contract="nvda_desk.schemas.state_policy.EventOptionsStressAuthorityPacket",
            allowed_aliases=["event_stress_matrix", "options_stress_policy"],
            notes=[
                "Gate 70 freezes imminent/live event risk and options-stress posture law before precedence control."
            ],
        ),
        VocabularyEntry(
            canonical_slug="modifier_control_law",
            canonical_label="Modifier Control Law",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.state_policy.ModifierControlLawAuthorityPacket",
            allowed_aliases=["precedence_matrix", "kill_switch_law"],
            notes=[
                "Gate 71 freezes precedence, compatible combination algebra, clamps, vetoes, and kill-switches."
            ],
        ),
        VocabularyEntry(
            canonical_slug="event_provenance_contract",
            canonical_label="Event Provenance Contract",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="research_doctrine",
            maps_to_contract="nvda_desk.schemas.events.EventIngestionAuthorityPacket",
            allowed_aliases=["event_source_normalisation", "event_ingestion_contract"],
            notes=[
                "Gate 72 freezes source inventory, freshness, confidence, conflict, and outage semantics for event truth."
            ],
        ),
        VocabularyEntry(
            canonical_slug="shared_event_store",
            canonical_label="Shared Event Store",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="review_explanation",
            maps_to_contract="nvda_desk.schemas.events.EventStoreAuthorityPacket",
            allowed_aliases=["event_store_query", "shared_event_truth"],
            notes=[
                "Gate 73 freezes nearby-event windows, materiality floors, lineage retrieval, and replay-consumer semantics."
            ],
        ),
        VocabularyEntry(
            canonical_slug="live_event_richness",
            canonical_label="Live Event Richness",
            category=VocabularyCategory.WORKFLOW,
            stage_owner="temporal_context",
            maps_to_contract="nvda_desk.schemas.events.LiveEventRichnessAuthorityPacket",
            allowed_aliases=["live_event_snapshot", "event_rich_temporal_input"],
            notes=[
                "Gate 74 preserves event identity, impact, provenance, nearby summaries, and lineage into live cognition packets."
            ],
        ),
    ]
    for horizon in PlaybookHorizon:
        entries.append(
            VocabularyEntry(
                canonical_slug=horizon.value,
                canonical_label=horizon.value.replace("_", " ").title(),
                category=VocabularyCategory.HORIZON,
                stage_owner="playbook_eligibility",
                horizon=horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookHorizon",
                allowed_aliases=[f"carry_{horizon.value}"],
            )
        )
    for family in document.families:
        entries.append(
            VocabularyEntry(
                canonical_slug=family.family_id,
                canonical_label=family.title,
                category=VocabularyCategory.PLAYBOOK_FAMILY,
                stage_owner="playbook_eligibility",
                family=family.family_id,
                maps_to_contract="nvda_desk.schemas.playbook_registry.PlaybookFamilySpec",
                allowed_aliases=[f"family:{family.family_id}"],
                notes=list(family.notes),
            )
        )
    template_index = document.execution_template_index()
    for variant in document.setup_variants:
        template = template_index[variant.execution_expression_id]
        entries.append(
            VocabularyEntry(
                canonical_slug=variant.setup_variant_id,
                canonical_label=variant.title,
                category=VocabularyCategory.SETUP_VARIANT,
                stage_owner="playbook_eligibility",
                family=variant.family_id,
                setup_variant=variant.setup_variant_id,
                execution_expression=variant.execution_expression_id,
                horizon=variant.horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.SetupVariantSpec",
                allowed_aliases=(
                    [f"legacy_playbook:{variant.legacy_playbook_id}"]
                    if variant.legacy_playbook_id
                    else []
                ),
                notes=list(variant.notes),
            )
        )
        entries.append(
            VocabularyEntry(
                canonical_slug=template.template_id,
                canonical_label=template.entry_style.replace("_", " ").title(),
                category=VocabularyCategory.EXECUTION_EXPRESSION,
                stage_owner="expression_execution",
                family=variant.family_id,
                setup_variant=variant.setup_variant_id,
                execution_expression=template.template_id,
                horizon=variant.horizon.value,
                maps_to_contract="nvda_desk.schemas.playbook_registry.ExecutionTemplateSpec",
                allowed_aliases=[template.entry_style],
                notes=[template.thesis_invalidation_state],
            )
        )
    entries.extend(
        [
            VocabularyEntry(
                canonical_slug="walk_forward_harness",
                canonical_label="Walk Forward Harness",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="review_replay",
                maps_to_contract="nvda_desk.schemas.calibration.WalkForwardHarnessAuthorityPacket",
                notes=["Frozen Gate 79 review-horizon discovery harness contract."],
            ),
            VocabularyEntry(
                canonical_slug="review_horizon_discovery",
                canonical_label="Review Horizon Discovery",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="review_replay",
                maps_to_contract="nvda_desk.schemas.calibration.HorizonDiscoveryReport",
                notes=["Bounded Gate 79 horizon-discovery output surface."],
            ),
            VocabularyEntry(
                canonical_slug="offset_sensitive",
                canonical_label="Offset Sensitive",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="review_replay",
                maps_to_contract="nvda_desk.schemas.calibration.HorizonDiscoveryOutcome",
                notes=["Gate 79 outcome meaning offsets disagree materially."],
            ),
            VocabularyEntry(
                canonical_slug="prepared_runtime_regime_packet",
                canonical_label="Prepared Runtime Regime Packet",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="market_regime_context",
                maps_to_contract="nvda_desk.schemas.dataset.PreparedRuntimeRegimePacket",
                allowed_aliases=["promoted_regime_packet"],
                notes=[
                    "Bounded prepared-runtime carriage packet for promoted cross-asset regime truth before lawful live Step 2 ingress.",
                ],
            ),
            VocabularyEntry(
                canonical_slug="prepared_participation_baseline_packet",
                canonical_label="Prepared Participation Baseline Packet",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="temporal_context",
                maps_to_contract="nvda_desk.schemas.dataset.PreparedParticipationBaselinePacket",
                allowed_aliases=["participation_baseline_packet"],
                notes=[
                    "Bounded prepared-runtime carriage packet for same-bucket participation proxy truth without inventing historical baseline authority.",
                ],
            ),
            VocabularyEntry(
                canonical_slug="options_flow_history_lane",
                canonical_label="Options and Flow Context History Lane",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="options_flow_context",
                maps_to_contract="src/nvda_desk/services/options_flow_history.py",
                allowed_aliases=["options_flow_history", "observational_lane"],
                disallowed_phrases=["eighth_stage"],
                notes=[
                    "Adjacent observational lane anchored to the fully formed Options and Flow Context boundary; not a desk-cognition stage and not recommendation authority.",
                ],
            ),
            VocabularyEntry(
                canonical_slug="options_surface_observation_record",
                canonical_label="Options Surface Observation Record",
                category=VocabularyCategory.COMPATIBILITY_SURFACE,
                stage_owner="options_flow_context",
                maps_to_contract="nvda_desk.schemas.options_flow_history.OptionsFlowHistoryObservationRecord",
                allowed_aliases=["options_flow_history_observation_record"],
                disallowed_phrases=["recommendation_receipt"],
                notes=[
                    "Bounded observational record captured at the Options and Flow Context boundary with one lawful raw-source authority only per cycle.",
                ],
            ),
            VocabularyEntry(
                canonical_slug="options_surface_observation_store",
                canonical_label="Options Surface Observation Store",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="options_flow_context",
                maps_to_contract="nvda_desk.db.models.OptionsFlowHistoryObservation",
                allowed_aliases=["options_flow_history_store"],
                notes=[
                    "Append-only bounded persistence surface for observational records captured outside recommendation and allocator memory.",
                ],
            ),
            VocabularyEntry(
                canonical_slug="independent_parallel_risk_lane",
                canonical_label="Independent Parallel Risk Lane",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="temporal_context",
                maps_to_contract="docs/planning/2026-04-02_GATE158_CO_RESIDENT_PARALLEL_RISK_LANE_LAW.md",
                allowed_aliases=[
                    "parallel risk pipeline",
                    "co-resident risk lane",
                    "parallel_risk_pipeline",
                ],
                disallowed_phrases=["step_1_1", "step_8", "eighth_stage"],
                notes=[
                    "First-class co-resident lane planned from session start; not a numbered stage and not a bypass of the seven-step desk cognition grammar."
                ],
            ),
            VocabularyEntry(
                canonical_slug="signal_coefficient_reference_workbook",
                canonical_label="Signal-Coefficient Reference Workbook",
                category=VocabularyCategory.DATA_CLASSIFICATION,
                stage_owner="planning_governance",
                maps_to_contract="data/reference/signal_workbooks/2026-03-25_NVDA_SIGNAL_WORKBOOK_v3_bounds_handoff_copy.xlsx",
                allowed_aliases=[
                    "signal workbook",
                    "coefficient register workbook",
                    "live reference workbook",
                ],
                disallowed_phrases=["runtime authority workbook", "normative workbook"],
                notes=[
                    "Governed live reference ledger for signal/coefficient provenance, bounds research, and workbook_ref lineage; never direct runtime authority without typed promotion."
                ],
            ),
            VocabularyEntry(
                canonical_slug="capital_deployment_authority_service",
                canonical_label="Capital Deployment Authority Service",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="review_explanation",
                maps_to_contract="nvda_desk.services.capital_deployment_authority.CapitalDeploymentAuthorityService",
                allowed_aliases=[
                    "capital deployment authority",
                    "capital_deployment_authority",
                ],
                notes=[
                    "Bounded downstream fresh-capital authoriser for already-formed opening candidates only; not a full arbiter and not close-position logic."
                ],
            ),
            VocabularyEntry(
                canonical_slug="capital_deployment_authority_decision",
                canonical_label="Capital Deployment Authority Decision",
                category=VocabularyCategory.WORKFLOW,
                stage_owner="review_explanation",
                maps_to_contract="nvda_desk.schemas.cognition.CapitalDeploymentAuthorityDecision",
                allowed_aliases=["deployment decision"],
                notes=[
                    "Bounded downstream decision carrying deploy-versus-stand-down authority, authorised percentage, authorised notional, and rationale codes for fresh capital only."
                ],
            ),
        ]
    )
    return VocabularyDocument(
        schema_version="desk_vocabulary.v1",
        registry_version="gate157-parallel-risk-lane-foundation-2026-04-02",
        notes=[
            "Generated from current live playbook registry and pinned architecture surfaces.",
            "Gates 60-79 extend the workflow vocabulary with state-policy, event, precursor, modifier, and review-horizon terms.",
            "Gate 157 adds first-class lane/workbook discoverability terms without claiming runtime packet implementation.",
            "Vocabulary workflow is feeder-process only and must not be treated as blind runtime truth.",
        ],
        entries=entries,
    )


def main() -> None:
    """Write the generated vocabulary document to the committed JSON path."""

    document = build_document()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(document.to_json_text(), encoding="utf-8")


if __name__ == "__main__":
    main()
