"""Deterministic Gate 78 runtime integration for state-conditioned modifiers.

This service reads the approved state vector, applies bounded modifier law to
mutable runtime surfaces, and emits a typed runtime packet with full lineage.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from nvda_desk.config_models import CoefficientAuthorityDocument, default_coefficient_authority_path
from nvda_desk.schemas.cognition import (
    ExecutionExpressionOutput,
    GammaState,
    MarketRegimeContextOutput,
    ModifierCompatibilityBridgeSurface,
    OptionsFlowContextOutput,
    PermissionState,
    PostureRiskOutput,
    TemporalContextInput,
    TemporalContextOutput,
)
from nvda_desk.schemas.market import (
    PrecursorContradictionClass,
    PrecursorPostureState,
)
from nvda_desk.schemas.risk import CarryHorizonState, DayPhaseState
from nvda_desk.schemas.state_policy import (
    CanonicalStateVectorField,
    CombinationLaw,
    DegradationStep,
    EffectiveCoefficientLineage,
    KillSwitchCondition,
    ModifierPriorityBand,
    ModifierRuntimePacket,
    ModifierTransformType,
    MutableRuntimeSurface,
    NonActionClass,
    OverrideDisposition,
    ResolvedRuntimeSurfaceValue,
    SignalConflictClass,
)


@dataclass(frozen=True)
class _PolicyApplication:
    policy_id: str
    band: ModifierPriorityBand
    target_surface: MutableRuntimeSurface
    transform_type: ModifierTransformType
    scale: float | None = None
    additive_offset: float | None = None
    clamp_floor: float | None = None
    clamp_cap: float | None = None
    boolean_value: bool | None = None
    notes: tuple[str, ...] = ()


def project_day_phase_state(temporal: TemporalContextOutput) -> DayPhaseState:
    """Return the canonical Gate 69 day-phase projection for one temporal snapshot."""

    mapping = {
        "open_disorder": DayPhaseState.OPENING_DISORDER,
        "early_anchor": DayPhaseState.OPENING_RESOLUTION,
        "mid_morning": DayPhaseState.TREND_WINDOW,
        "lunch": DayPhaseState.MIDDAY_COMPRESSION,
        "trend_window": DayPhaseState.TREND_WINDOW,
        "late_session": DayPhaseState.LATE_SESSION,
        "close": DayPhaseState.CLOSE_AUCTION,
        "after_hours": DayPhaseState.POST_CLOSE,
        "closed": DayPhaseState.POST_CLOSE,
        "pre_market": DayPhaseState.OPENING_RESOLUTION,
    }
    return mapping.get(temporal.desk_window, DayPhaseState.TREND_WINDOW)


def project_carry_horizon_state(temporal: TemporalContextOutput) -> CarryHorizonState:
    """Return the canonical Gate 69 carry-horizon projection for one temporal snapshot."""

    if temporal.event_proximity_state in {
        "event_same_day",
        "event_scheduled",
    } and temporal.desk_window in {"late_session", "close"}:
        return CarryHorizonState.EVENT_CARRY_SETUP
    if temporal.desk_window == "close":
        return CarryHorizonState.OVERNIGHT_SETUP
    return CarryHorizonState.INTRADAY_ONLY


def project_event_option_state_labels(
    temporal: TemporalContextOutput,
    options_flow: OptionsFlowContextOutput,
) -> set[str]:
    """Return the canonical Gate 70 event/options-stress labels for one runtime snapshot."""

    labels: set[str] = set()
    if temporal.event_window_state == "event_live_window":
        labels.add("event_live")
    elif temporal.event_window_state == "event_imminent_window":
        labels.add("event_imminent")
    if options_flow.options_behavior_cluster == "event_suppressed":
        labels.add("event_suppressed")
    if options_flow.gamma_state is GammaState.DESTABILISING:
        labels.add("negative_gamma_stress")
    if (
        options_flow.pin_risk_state in {"pin_risk_present", "pin_risk_high"}
        or options_flow.options_behavior_cluster == "pin_reversion_ready"
    ):
        labels.add("pin_risk")
    if temporal.expiry_cycle_state == "expiry_day":
        labels.add("expiry_distortion")
    return labels


@lru_cache(maxsize=8)
def _load_governed_coefficient_authority(path: str) -> CoefficientAuthorityDocument:
    """Load the governed coefficient authority document from one resolved path."""

    return CoefficientAuthorityDocument.from_yaml_path(Path(path))


class StateConditionedModifierService:
    """Apply frozen Gate 78 modifier law without changing cognition grammar.

    Purpose:
        Convert approved state into bounded effective coefficients plus typed
        stand-down, conflict, kill-switch, and lineage outputs.
    Inputs:
        Temporal, regime, options, posture, and additive precursor/event truth.
    Outputs:
        `ModifierRuntimePacket` carrying resolved mutable-surface values and
        review-visible application lineage.
    Determinism:
        Uses checked-in governed authority, precedence bands, and fixed rules only.
    """

    _PRECEDENCE_ORDER: dict[ModifierPriorityBand, int] = {
        ModifierPriorityBand.BASELINE: 0,
        ModifierPriorityBand.REGIME: 1,
        ModifierPriorityBand.PRECURSOR: 2,
        ModifierPriorityBand.PHASE_CARRY: 3,
        ModifierPriorityBand.EVENT_OPTIONS_STRESS: 4,
        ModifierPriorityBand.HARD_BLOCK: 5,
        ModifierPriorityBand.KILL_SWITCH: 6,
    }

    def __init__(
        self,
        *,
        authority_path: Path | None = None,
        authority_document: CoefficientAuthorityDocument | None = None,
    ) -> None:
        """Load the governed mutable-surface authority for runtime use."""

        self._authority_document = authority_document or _load_governed_coefficient_authority(
            str((authority_path or default_coefficient_authority_path()).resolve())
        )
        self._mutable_surface_authority = self._authority_document.mutable_surface_index()
        self._baseline_numeric = {
            surface: float(spec.baseline)
            for surface, spec in self._authority_document.mutable_numeric_surface_index().items()
            if spec.activation_gate == "Gate 124"
        }
        self._baseline_boolean = {
            surface: bool(spec.baseline)
            for surface, spec in self._authority_document.mutable_boolean_surface_index().items()
            if spec.activation_gate == "Gate 124"
        }
        self._surface_floors = {
            surface: float(spec.minimum)
            for surface, spec in self._authority_document.mutable_numeric_surface_index().items()
            if spec.activation_gate == "Gate 124"
        }
        self._surface_caps = {
            surface: float(spec.maximum)
            for surface, spec in self._authority_document.mutable_numeric_surface_index().items()
            if spec.activation_gate == "Gate 124"
        }

    def evaluate(
        self,
        *,
        temporal_input: TemporalContextInput,
        temporal: TemporalContextOutput,
        regime: MarketRegimeContextOutput,
        options_flow: OptionsFlowContextOutput,
        posture: PostureRiskOutput,
    ) -> ModifierRuntimePacket:
        """Return one typed Gate 78 modifier packet for this runtime snapshot."""

        active_state_fields = self._active_state_fields(temporal, regime, options_flow, posture)
        policy_applications: list[_PolicyApplication] = []
        active_policy_ids: list[str] = []
        active_precedence_bands: set[ModifierPriorityBand] = {ModifierPriorityBand.BASELINE}
        applied_combination_laws: set[CombinationLaw] = set()
        suppressed_state_labels: list[str] = []
        conflict_classes: list[SignalConflictClass] = []
        notes: list[str] = []
        triggered_kill_switch: KillSwitchCondition | None = None
        stand_down_class: NonActionClass | None = None
        degradation_step = DegradationStep.NORMAL

        day_phase_state = self._day_phase_state(temporal)
        carry_horizon_state = self._carry_horizon_state(temporal)
        if (
            day_phase_state in {DayPhaseState.LATE_SESSION, DayPhaseState.CLOSE_AUCTION}
            or carry_horizon_state is not CarryHorizonState.INTRADAY_ONLY
        ):
            active_precedence_bands.add(ModifierPriorityBand.PHASE_CARRY)
            policy_id = f"phase_carry:{day_phase_state.value}:{carry_horizon_state.value}"
            active_policy_ids.append(policy_id)
            applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
            policy_applications.append(
                _PolicyApplication(
                    policy_id=policy_id,
                    band=ModifierPriorityBand.PHASE_CARRY,
                    target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                    transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                    scale=(
                        0.50 if carry_horizon_state is not CarryHorizonState.INTRADAY_ONLY else 0.70
                    ),
                    notes=("late_or_carry_sensitive_phase_compresses_fresh_deployable_capital",),
                )
            )
            policy_applications.append(
                _PolicyApplication(
                    policy_id=f"{policy_id}:entry_gate",
                    band=ModifierPriorityBand.PHASE_CARRY,
                    target_surface=MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
                    transform_type=ModifierTransformType.ADDITIVE_OFFSET,
                    additive_offset=0.05,
                    notes=("carry_sensitive_phase_raises_entry_gate_floor",),
                )
            )
            if carry_horizon_state is not CarryHorizonState.INTRADAY_ONLY:
                degradation_step = DegradationStep.CONFIDENCE_REDUCED
                notes.append("carry_sensitive_phase_reduced_operating_confidence")

        event_states = self._event_option_state_labels(temporal, options_flow)
        event_family_class = self._event_family_class(temporal)
        venue_session_distortion = self._has_venue_session_distortion(temporal)
        if event_states or venue_session_distortion:
            active_precedence_bands.add(ModifierPriorityBand.EVENT_OPTIONS_STRESS)
        if "event_live" in event_states:
            triggered_kill_switch = KillSwitchCondition.EVENT_LIVE_HARD_BLOCK
            stand_down_class = NonActionClass.EVENT_RISK_STAND_DOWN
            degradation_step = DegradationStep.VETO
            suppressed_state_labels.extend(["phase_carry", "precursor", "regime", "baseline"])
            notes.append("event_live_hard_block_engaged")
        if (
            "event_suppressed" in event_states
            and "negative_gamma_stress" in event_states
            and triggered_kill_switch is None
        ):
            triggered_kill_switch = KillSwitchCondition.EVENT_SUPPRESSED_WITH_NEGATIVE_GAMMA
            stand_down_class = NonActionClass.OPTIONS_FLOW_STAND_DOWN
            degradation_step = DegradationStep.VETO
            suppressed_state_labels.extend(["phase_carry", "precursor", "regime", "baseline"])
            notes.append("event_suppressed_with_negative_gamma_engaged_kill_switch")
        if triggered_kill_switch is None:
            if "negative_gamma_stress" in event_states:
                policy_id = "event_options:negative_gamma_stress"
                active_policy_ids.append(policy_id)
                applied_combination_laws.update(
                    {
                        CombinationLaw.MULTIPLY_THEN_CLAMP,
                        CombinationLaw.BLOCK_OVERRIDES_SCALE,
                    }
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.55,
                        notes=("negative_gamma_caps_fresh_deployable_capital",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:hedge",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.HEDGE_REQUIRED,
                        transform_type=ModifierTransformType.SUPPRESSION_VETO,
                        boolean_value=True,
                        notes=("negative_gamma_requires_hedge_overlay",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:max_risk",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.MAX_RISK_PER_TRADE,
                        transform_type=ModifierTransformType.CLAMP,
                        clamp_cap=0.20,
                        notes=("negative_gamma_clamps_max_risk_per_trade",),
                    )
                )
                conflict_classes.append(SignalConflictClass.POSTURE_DEGRADATION)
                degradation_step = max(
                    degradation_step,
                    DegradationStep.SIZE_REDUCED,
                    key=self._degradation_rank,
                )
            if "pin_risk" in event_states:
                policy_id = "event_options:pin_risk"
                active_policy_ids.append(policy_id)
                applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.70,
                        notes=("pin_risk_caps_fresh_deployable_capital",),
                    )
                )
            if "event_imminent" in event_states:
                policy_id = "event_options:event_imminent"
                active_policy_ids.append(policy_id)
                applied_combination_laws.update(
                    {
                        CombinationLaw.MULTIPLY_THEN_CLAMP,
                        CombinationLaw.ADDITIVE_OFFSET_THEN_CLAMP,
                    }
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.65,
                        notes=("event_imminent_reduces_deployable_capital",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:entry_gate",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
                        transform_type=ModifierTransformType.ADDITIVE_OFFSET,
                        additive_offset=0.04,
                        notes=("event_imminent_tightens_entry_gate_floor",),
                    )
                )
                degradation_step = max(
                    degradation_step,
                    DegradationStep.CONFIDENCE_REDUCED,
                    key=self._degradation_rank,
                )
            if event_family_class == "macro" and event_states.intersection({"event_imminent", "event_live"}):
                policy_id = "event_options:macro_event_window"
                active_policy_ids.append(policy_id)
                applied_combination_laws.update(
                    {
                        CombinationLaw.MULTIPLY_THEN_CLAMP,
                        CombinationLaw.ADDITIVE_OFFSET_THEN_CLAMP,
                    }
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.60,
                        notes=("macro_event_window_compresses_deployable_capital",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:entry_gate",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
                        transform_type=ModifierTransformType.ADDITIVE_OFFSET,
                        additive_offset=0.05,
                        notes=("macro_event_window_raises_entry_gate_floor",),
                    )
                )
            if event_family_class == "company" and event_states.intersection({"event_imminent", "event_live"}):
                policy_id = "event_options:company_event_window"
                active_policy_ids.append(policy_id)
                applied_combination_laws.update(
                    {
                        CombinationLaw.MULTIPLY_THEN_CLAMP,
                        CombinationLaw.ADDITIVE_OFFSET_THEN_CLAMP,
                    }
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.72,
                        notes=("company_event_window_compresses_deployable_capital",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:entry_gate",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
                        transform_type=ModifierTransformType.ADDITIVE_OFFSET,
                        additive_offset=0.03,
                        notes=("company_event_window_raises_entry_gate_floor",),
                    )
                )
            if "expiry_distortion" in event_states:
                policy_id = "event_options:expiry_distortion"
                active_policy_ids.append(policy_id)
                applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.82,
                        notes=("expiry_distortion_compresses_deployable_capital",),
                    )
                )
            if venue_session_distortion:
                policy_id = "event_options:venue_session_distortion"
                active_policy_ids.append(policy_id)
                applied_combination_laws.update(
                    {
                        CombinationLaw.MULTIPLY_THEN_CLAMP,
                        CombinationLaw.ADDITIVE_OFFSET_THEN_CLAMP,
                    }
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=policy_id,
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                        transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                        scale=0.85,
                        notes=("venue_session_distortion_compresses_deployable_capital",),
                    )
                )
                policy_applications.append(
                    _PolicyApplication(
                        policy_id=f"{policy_id}:entry_gate",
                        band=ModifierPriorityBand.EVENT_OPTIONS_STRESS,
                        target_surface=MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR,
                        transform_type=ModifierTransformType.ADDITIVE_OFFSET,
                        additive_offset=0.02,
                        notes=("venue_session_distortion_raises_entry_gate_floor",),
                    )
                )

        precursor = temporal_input.precursor_runtime_packet
        if precursor is not None:
            active_precedence_bands.add(ModifierPriorityBand.PRECURSOR)
            if precursor.contradiction_class is not PrecursorContradictionClass.NONE:
                conflict_classes.append(SignalConflictClass.OBSERVATION_DIVERGENCE)
                notes.append(f"precursor_contradiction:{precursor.contradiction_class.value}")
            if precursor.posture_state is PrecursorPostureState.UNRESOLVED_CONTEXT:
                triggered_kill_switch = (
                    triggered_kill_switch or KillSwitchCondition.DATA_QUALITY_HARD_BLOCK
                )
                stand_down_class = NonActionClass.DATA_QUALITY_STAND_DOWN
                degradation_step = DegradationStep.VETO
                suppressed_state_labels.extend(["regime", "baseline"])
                notes.append("precursor_unresolved_context_forced_data_quality_hard_block")
            elif triggered_kill_switch is None:
                if precursor.posture_state is PrecursorPostureState.STAND_DOWN_PRESSURE:
                    policy_id = "precursor:stand_down_pressure"
                    active_policy_ids.append(policy_id)
                    applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
                    policy_applications.append(
                        _PolicyApplication(
                            policy_id=policy_id,
                            band=ModifierPriorityBand.PRECURSOR,
                            target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                            transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                            scale=0.40,
                            notes=("precursor_stand_down_pressure_compresses_deployable_capital",),
                        )
                    )
                    stand_down_class = NonActionClass.DATA_QUALITY_STAND_DOWN
                    degradation_step = max(
                        degradation_step,
                        DegradationStep.STAND_DOWN,
                        key=self._degradation_rank,
                    )
                elif precursor.posture_state is PrecursorPostureState.TIGHTENED_POSTURE:
                    policy_id = "precursor:tightened_posture"
                    active_policy_ids.append(policy_id)
                    applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
                    policy_applications.append(
                        _PolicyApplication(
                            policy_id=policy_id,
                            band=ModifierPriorityBand.PRECURSOR,
                            target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                            transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                            scale=0.75,
                            notes=("precursor_tightened_posture_reduces_deployable_capital",),
                        )
                    )
                    degradation_step = max(
                        degradation_step,
                        DegradationStep.CONFIRMATION_TIGHTENED,
                        key=self._degradation_rank,
                    )
                elif precursor.posture_state is PrecursorPostureState.DEGRADED_CONFIDENCE:
                    policy_id = "precursor:degraded_confidence"
                    active_policy_ids.append(policy_id)
                    applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
                    policy_applications.append(
                        _PolicyApplication(
                            policy_id=policy_id,
                            band=ModifierPriorityBand.PRECURSOR,
                            target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                            transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                            scale=0.85,
                            notes=("precursor_degraded_confidence_reduces_deployable_capital",),
                        )
                    )

        if (
            regime.volatility_regime.value == "stressed"
            and regime.breadth_state.value == "weak"
            and triggered_kill_switch is None
        ):
            active_precedence_bands.add(ModifierPriorityBand.REGIME)
            policy_id = "regime:stressed_weak_breadth"
            active_policy_ids.append(policy_id)
            applied_combination_laws.add(CombinationLaw.MULTIPLY_THEN_CLAMP)
            policy_applications.append(
                _PolicyApplication(
                    policy_id=policy_id,
                    band=ModifierPriorityBand.REGIME,
                    target_surface=MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT,
                    transform_type=ModifierTransformType.MULTIPLICATIVE_SCALE,
                    scale=0.80,
                    notes=("stressed_weak_breadth_reduces_deployable_capital",),
                )
            )
            conflict_classes.append(SignalConflictClass.POSTURE_DEGRADATION)
            degradation_step = max(
                degradation_step,
                DegradationStep.SIZE_REDUCED,
                key=self._degradation_rank,
            )

        resolved_surfaces, effective_lineage = self._resolve_surfaces(
            policy_applications=policy_applications,
            active_bands=active_precedence_bands,
            triggered_kill_switch=triggered_kill_switch,
            active_policy_ids=active_policy_ids,
        )
        if triggered_kill_switch is not None:
            resolved_surfaces = self._with_hard_block_surfaces(
                resolved_surfaces=resolved_surfaces,
                active_policy_ids=active_policy_ids,
                triggered_kill_switch=triggered_kill_switch,
            )
            effective_lineage = self._hard_block_lineage(resolved_surfaces, active_policy_ids)
            active_precedence_bands.add(ModifierPriorityBand.KILL_SWITCH)
            applied_combination_laws.add(CombinationLaw.BLOCK_OVERRIDES_SCALE)
            conflict_classes.append(SignalConflictClass.HARD_VETO_CONFLICT)
            degradation_step = DegradationStep.VETO

        return ModifierRuntimePacket(
            active_state_fields=active_state_fields,
            active_policy_ids=active_policy_ids,
            resolved_surfaces=resolved_surfaces,
            effective_lineage=effective_lineage,
            active_precedence_bands=sorted(active_precedence_bands, key=self._band_sort),
            applied_combination_laws=sorted(applied_combination_laws, key=lambda item: item.value),
            triggered_kill_switch=triggered_kill_switch,
            suppressed_state_labels=sorted(set(suppressed_state_labels)),
            stand_down_class=stand_down_class,
            conflict_classes=sorted(set(conflict_classes), key=lambda item: item.value),
            degradation_step=degradation_step,
            override_disposition=(
                OverrideDisposition.FORBIDDEN
                if triggered_kill_switch
                else OverrideDisposition.NOT_APPLICABLE
            ),
            notes=notes,
        )

    def _posture_bridge_surface(
        self,
        *,
        posture: PostureRiskOutput,
        packet: ModifierRuntimePacket,
        update: dict[str, object],
        target_fresh: float | None,
    ) -> ModifierCompatibilityBridgeSurface:
        overridden_fields: list[str] = []
        compared_fields = (
            "permission_state",
            "posture_label",
            "fresh_deployable_capital_pct",
            "overnight_deployable_capital_pct",
            "inventory_action_bias",
        )
        for field_name in compared_fields:
            if field_name in update and update[field_name] != getattr(posture, field_name):
                overridden_fields.append(field_name)
        notes = ["modifier_runtime_packet_authority"]
        if overridden_fields:
            notes.append("posture_fields_overridden_by_compatibility_bridge")
        else:
            notes.append("no_posture_field_override_required")
        return ModifierCompatibilityBridgeSurface(
            compatibility_bridge_active=bool(packet.active_policy_ids or overridden_fields or packet.triggered_kill_switch is not None),
            applied_policy_ids=list(packet.active_policy_ids),
            overridden_fields=overridden_fields,
            target_fresh_deployable_capital_pct=(
                round(float(target_fresh), 4) if target_fresh is not None else None
            ),
            notes=notes,
        )

    def _execution_bridge_surface(
        self,
        *,
        execution: ExecutionExpressionOutput,
        packet: ModifierRuntimePacket,
        update: dict[str, object],
        target_fresh: float | None,
        hedge_required: bool | None,
    ) -> ModifierCompatibilityBridgeSurface:
        overridden_fields: list[str] = []
        compared_fields = (
            "entry_gate_score_floor",
            "zone_score_threshold",
            "distance_to_vwap_soft_limit_pct",
            "risk_vix_caution_threshold",
            "risk_vix_hot_threshold",
            "max_risk_per_trade",
            "hedge_required",
        )
        for field_name in compared_fields:
            if field_name in update and update[field_name] != getattr(execution, field_name):
                overridden_fields.append(field_name)
        notes = ["modifier_runtime_packet_authority"]
        if overridden_fields:
            notes.append("execution_fields_overridden_by_compatibility_bridge")
        else:
            notes.append("execution_operative_surfaces_already_reflect_modifier_runtime_packet")
        return ModifierCompatibilityBridgeSurface(
            compatibility_bridge_active=bool(packet.active_policy_ids or overridden_fields or packet.triggered_kill_switch is not None),
            applied_policy_ids=list(packet.active_policy_ids),
            overridden_fields=overridden_fields,
            target_fresh_deployable_capital_pct=(
                round(float(target_fresh), 4) if target_fresh is not None else None
            ),
            entry_gate_score_floor=self._resolved_numeric(
                packet, MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR
            ),
            zone_score_threshold=self._resolved_numeric(
                packet, MutableRuntimeSurface.ZONE_SCORE_THRESHOLD
            ),
            max_risk_per_trade=self._resolved_numeric(
                packet, MutableRuntimeSurface.MAX_RISK_PER_TRADE
            ),
            hedge_required=hedge_required,
            notes=notes,
        )

    def apply_to_posture(
        self, posture: PostureRiskOutput, packet: ModifierRuntimePacket
    ) -> PostureRiskOutput:
        """Return posture output with bounded Gate 78 policy effects applied."""

        target_fresh = self._resolved_numeric(
            packet, MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT
        )
        reasons = list(posture.reasons)
        downstream_annotations = list(posture.downstream_annotations)
        if packet.active_policy_ids:
            policy_note = f"modifier_runtime_policies:{packet.active_policy_ids}"
            reasons.append(policy_note)
            downstream_annotations.append(policy_note)
        if packet.triggered_kill_switch is not None:
            kill_switch_note = f"modifier_kill_switch:{packet.triggered_kill_switch.value}"
            reasons.append(kill_switch_note)
            downstream_annotations.append(kill_switch_note)
        if packet.stand_down_class is not None:
            stand_down_note = f"stand_down_class:{packet.stand_down_class.value}"
            reasons.append(stand_down_note)
            downstream_annotations.append(stand_down_note)
        if packet.conflict_classes:
            conflict_note = f"modifier_conflicts:{[item.value for item in packet.conflict_classes]}"
            reasons.append(conflict_note)
            downstream_annotations.append(conflict_note)
        downstream_annotations.append("modifier_runtime_packet_authority")
        if target_fresh is None:
            target_fresh = posture.fresh_deployable_capital_pct

        update: dict[str, object] = {
            "modifier_runtime_packet": packet,
            "stand_down_class": packet.stand_down_class,
            "conflict_classes": list(packet.conflict_classes),
            "degradation_step": packet.degradation_step,
            "override_disposition": packet.override_disposition,
            "downstream_annotations": downstream_annotations,
            "reasons": reasons,
        }
        if packet.triggered_kill_switch is not None or packet.degradation_step in {
            DegradationStep.VETO,
            DegradationStep.STAND_DOWN,
        }:
            update.update(
                {
                    "permission_state": PermissionState.BLOCK,
                    "posture_label": "state_policy_block",
                    "fresh_deployable_capital_pct": 0.0,
                    "overnight_deployable_capital_pct": 0.0,
                    "inventory_action_bias": "reduce",
                }
            )
        else:
            adjusted_fresh = round(min(posture.fresh_deployable_capital_pct, target_fresh), 4)
            adjusted_overnight = round(
                min(posture.overnight_deployable_capital_pct, adjusted_fresh), 4
            )
            update["fresh_deployable_capital_pct"] = adjusted_fresh
            update["overnight_deployable_capital_pct"] = adjusted_overnight
            if posture.permission_state is PermissionState.ALLOW and packet.degradation_step in {
                DegradationStep.CONFIDENCE_REDUCED,
                DegradationStep.WATCH_ONLY,
            }:
                update["permission_state"] = PermissionState.DERISK
                update["posture_label"] = "state_conditioned_derisk"
                if posture.inventory_action_bias == "add":
                    update["inventory_action_bias"] = "hold"
        update["modifier_compatibility_bridge"] = self._posture_bridge_surface(
            posture=posture,
            packet=packet,
            update=update,
            target_fresh=target_fresh,
        )
        return posture.model_copy(update=update)

    def apply_to_execution(
        self,
        execution: ExecutionExpressionOutput,
        packet: ModifierRuntimePacket,
    ) -> ExecutionExpressionOutput:
        """Return execution output with additive Gate 78 policy effects applied."""

        hedge_required = self._resolved_boolean(packet, MutableRuntimeSurface.HEDGE_REQUIRED)
        target_fresh = self._resolved_numeric(
            packet, MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT
        )
        update: dict[str, object] = {"modifier_runtime_packet": packet}
        reasons = list(execution.reasons)
        numeric_surface_field_map = {
            MutableRuntimeSurface.ENTRY_GATE_SCORE_FLOOR: "entry_gate_score_floor",
            MutableRuntimeSurface.ZONE_SCORE_THRESHOLD: "zone_score_threshold",
            MutableRuntimeSurface.DISTANCE_TO_VWAP_SOFT_LIMIT_PCT: "distance_to_vwap_soft_limit_pct",
            MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD: "risk_vix_caution_threshold",
            MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD: "risk_vix_hot_threshold",
            MutableRuntimeSurface.MAX_RISK_PER_TRADE: "max_risk_per_trade",
        }
        for surface, field_name in numeric_surface_field_map.items():
            effective = self._resolved_numeric(packet, surface)
            if effective is not None and round(float(getattr(execution, field_name)), 4) != round(float(effective), 4):
                update[field_name] = round(effective, 4)
        if hedge_required and not execution.hedge_required:
            update["hedge_required"] = True
            reasons.append("modifier_runtime_required_hedge")
            exit_reasons = list(execution.exit_reasons)
            if "modifier_runtime_required_hedge" not in exit_reasons:
                exit_reasons.append("modifier_runtime_required_hedge")
            update["exit_reasons"] = exit_reasons
        elif hedge_required is not None and execution.hedge_required != hedge_required:
            update["hedge_required"] = hedge_required
        if target_fresh is not None:
            reasons.append("modifier_runtime_target_fresh_compatibility_ignored_for_serial_shape")
        if any(policy_id.startswith("precursor:") for policy_id in packet.active_policy_ids):
            reasons.append("modifier_runtime_surfaces_extended_to_execution_output")
        update["modifier_compatibility_bridge"] = self._execution_bridge_surface(
            execution=execution,
            packet=packet,
            update=update,
            target_fresh=target_fresh,
            hedge_required=hedge_required,
        )
        update["reasons"] = reasons
        return execution.model_copy(update=update)

    def _resolve_surfaces(
        self,
        *,
        policy_applications: list[_PolicyApplication],
        active_bands: set[ModifierPriorityBand],
        triggered_kill_switch: KillSwitchCondition | None,
        active_policy_ids: list[str],
    ) -> tuple[list[ResolvedRuntimeSurfaceValue], list[EffectiveCoefficientLineage]]:
        numeric_surfaces = set(self._baseline_numeric)
        boolean_surfaces = set(self._baseline_boolean)
        resolved: list[ResolvedRuntimeSurfaceValue] = []
        lineage: list[EffectiveCoefficientLineage] = []
        grouped: dict[MutableRuntimeSurface, list[_PolicyApplication]] = {}
        for application in policy_applications:
            grouped.setdefault(application.target_surface, []).append(application)

        for surface in sorted(numeric_surfaces | boolean_surfaces, key=lambda item: item.value):
            policies = sorted(
                grouped.get(surface, []),
                key=lambda item: self._band_sort(item.band),
                reverse=True,
            )
            if surface in self._baseline_numeric:
                authority = self._mutable_surface_authority[surface]
                baseline_value = self._baseline_numeric[surface]
                value = baseline_value
                notes: list[str] = []
                clamped = False
                for policy in policies:
                    if (
                        policy.transform_type is ModifierTransformType.MULTIPLICATIVE_SCALE
                        and policy.scale is not None
                    ):
                        value *= policy.scale
                    elif (
                        policy.transform_type is ModifierTransformType.ADDITIVE_OFFSET
                        and policy.additive_offset is not None
                    ):
                        value += policy.additive_offset
                    if policy.clamp_floor is not None and value < policy.clamp_floor:
                        value = policy.clamp_floor
                        clamped = True
                    if policy.clamp_cap is not None and value > policy.clamp_cap:
                        value = policy.clamp_cap
                        clamped = True
                    notes.extend(policy.notes)
                floor = self._surface_floors.get(surface)
                cap = self._surface_caps.get(surface)
                if floor is not None and value < floor:
                    value = floor
                    clamped = True
                if cap is not None and value > cap:
                    value = cap
                    clamped = True
                winning_band = policies[0].band if policies else ModifierPriorityBand.BASELINE
                source_policy_ids = [policy.policy_id for policy in policies]
                resolved.append(
                    ResolvedRuntimeSurfaceValue(
                        target_surface=surface,
                        owner_stage=authority.owner_stage,
                        authority_version=self._authority_document.authority_version,
                        baseline_reference=(
                            f"coefficient_authority:{self._authority_document.authority_version}:{surface.value}"
                        ),
                        baseline_numeric_value=baseline_value,
                        minimum_numeric_value=self._surface_floors.get(surface),
                        maximum_numeric_value=self._surface_caps.get(surface),
                        effective_numeric_value=round(value, 4),
                        winning_precedence_band=winning_band,
                        source_policy_ids=source_policy_ids,
                        clamped=clamped,
                        notes=notes,
                    )
                )
                lineage.append(
                    EffectiveCoefficientLineage(
                        target_surface=surface,
                        baseline_reference=(
                            f"coefficient_authority:{self._authority_document.authority_version}:{surface.value}"
                        ),
                        active_modifier_policy_ids=source_policy_ids,
                        explanation_id=(
                            None
                            if not source_policy_ids
                            else f"effective:{surface.value}:{source_policy_ids[0]}"
                        ),
                    )
                )
            else:
                authority = self._mutable_surface_authority[surface]
                baseline_value = self._baseline_boolean[surface]
                value = baseline_value
                notes = []
                for policy in policies:
                    if policy.boolean_value is not None:
                        value = value or policy.boolean_value
                    notes.extend(policy.notes)
                winning_band = policies[0].band if policies else ModifierPriorityBand.BASELINE
                source_policy_ids = [policy.policy_id for policy in policies]
                resolved.append(
                    ResolvedRuntimeSurfaceValue(
                        target_surface=surface,
                        owner_stage=authority.owner_stage,
                        authority_version=self._authority_document.authority_version,
                        baseline_reference=(
                            f"coefficient_authority:{self._authority_document.authority_version}:{surface.value}"
                        ),
                        baseline_boolean_value=baseline_value,
                        effective_boolean_value=value,
                        winning_precedence_band=winning_band,
                        source_policy_ids=source_policy_ids,
                        notes=notes,
                    )
                )
                lineage.append(
                    EffectiveCoefficientLineage(
                        target_surface=surface,
                        baseline_reference=(
                            f"coefficient_authority:{self._authority_document.authority_version}:{surface.value}"
                        ),
                        active_modifier_policy_ids=source_policy_ids,
                        explanation_id=(
                            None
                            if not source_policy_ids
                            else f"effective:{surface.value}:{source_policy_ids[0]}"
                        ),
                    )
                )
        if triggered_kill_switch is not None and not active_policy_ids:
            lineage = self._hard_block_lineage(resolved, [])
        return resolved, lineage

    def _with_hard_block_surfaces(
        self,
        *,
        resolved_surfaces: list[ResolvedRuntimeSurfaceValue],
        active_policy_ids: list[str],
        triggered_kill_switch: KillSwitchCondition,
    ) -> list[ResolvedRuntimeSurfaceValue]:
        updated: list[ResolvedRuntimeSurfaceValue] = []
        for surface in resolved_surfaces:
            if surface.target_surface is MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT:
                updated.append(
                    surface.model_copy(
                        update={
                            "effective_numeric_value": 0.0,
                            "winning_precedence_band": ModifierPriorityBand.KILL_SWITCH,
                            "source_policy_ids": [
                                *surface.source_policy_ids,
                                triggered_kill_switch.value,
                            ],
                            "clamped": True,
                            "notes": [
                                *surface.notes,
                                "kill_switch_zeroed_fresh_deployable_capital",
                            ],
                        }
                    )
                )
            else:
                updated.append(surface)
        return updated

    def _hard_block_lineage(
        self,
        resolved_surfaces: list[ResolvedRuntimeSurfaceValue],
        active_policy_ids: list[str],
    ) -> list[EffectiveCoefficientLineage]:
        return [
            EffectiveCoefficientLineage(
                target_surface=surface.target_surface,
                baseline_reference=(
                    f"coefficient_authority:{self._authority_document.authority_version}:{surface.target_surface.value}"
                ),
                active_modifier_policy_ids=[
                    *active_policy_ids,
                    *surface.source_policy_ids,
                ],
                explanation_id=f"effective:{surface.target_surface.value}:kill_switch",
            )
            for surface in resolved_surfaces
        ]

    def _resolved_numeric(
        self, packet: ModifierRuntimePacket, surface: MutableRuntimeSurface
    ) -> float | None:
        for item in packet.resolved_surfaces:
            if item.target_surface is surface:
                return item.effective_numeric_value
        return None

    def _resolved_boolean(
        self, packet: ModifierRuntimePacket, surface: MutableRuntimeSurface
    ) -> bool | None:
        for item in packet.resolved_surfaces:
            if item.target_surface is surface:
                return item.effective_boolean_value
        return None

    def _active_state_fields(
        self,
        temporal: TemporalContextOutput,
        regime: MarketRegimeContextOutput,
        options_flow: OptionsFlowContextOutput,
        posture: PostureRiskOutput,
    ) -> list[CanonicalStateVectorField]:
        fields = {
            CanonicalStateVectorField.DESK_WINDOW,
            CanonicalStateVectorField.CLOCK_ENVELOPE,
            CanonicalStateVectorField.DAY_PHASE_STATE,
            CanonicalStateVectorField.CARRY_HORIZON_STATE,
            CanonicalStateVectorField.CARRYOVER_STATE,
            CanonicalStateVectorField.EXPIRY_CYCLE_STATE,
            CanonicalStateVectorField.EVENT_PROXIMITY_STATE,
            CanonicalStateVectorField.EVENT_WINDOW_STATE,
            CanonicalStateVectorField.VOLATILITY_REGIME,
            CanonicalStateVectorField.BREADTH_STATE,
            CanonicalStateVectorField.SECTOR_LEADERSHIP_STATE,
            CanonicalStateVectorField.RATES_REGIME_STATE,
            CanonicalStateVectorField.FX_STRESS_STATE,
            CanonicalStateVectorField.SIGNAL_CONFLICT_STATE,
            CanonicalStateVectorField.TERM_STRUCTURE_STATE,
            CanonicalStateVectorField.SKEW_STATE,
            CanonicalStateVectorField.GAMMA_STATE,
            CanonicalStateVectorField.DEALER_PRESSURE_STATE,
            CanonicalStateVectorField.OPTIONS_BEHAVIOR_CLUSTER,
            CanonicalStateVectorField.INVENTORY_POSTURE_STATE,
            CanonicalStateVectorField.FRESH_VS_INVENTORY_STATE,
            CanonicalStateVectorField.THESIS_STATE,
            CanonicalStateVectorField.CAPITAL_LOCKUP_STATE,
            CanonicalStateVectorField.TIME_STOP_STATE,
            CanonicalStateVectorField.PERMISSION_STATE,
        }
        return sorted(fields, key=lambda item: item.value)

    def _day_phase_state(self, temporal: TemporalContextOutput) -> DayPhaseState:
        return project_day_phase_state(temporal)

    def _carry_horizon_state(self, temporal: TemporalContextOutput) -> CarryHorizonState:
        return project_carry_horizon_state(temporal)

    def _event_option_state_labels(
        self,
        temporal: TemporalContextOutput,
        options_flow: OptionsFlowContextOutput,
    ) -> set[str]:
        return project_event_option_state_labels(temporal, options_flow)


    def _event_family_class(self, temporal: TemporalContextOutput) -> str | None:
        event_family = (temporal.active_event_family or '').lower()
        if any(token in event_family for token in {"fomc", "cpi", "ppi", "pce", "nfp", "gdp", "macro", "policy"}):
            return "macro"
        if "earnings" in event_family or event_family.startswith("nvda_") or event_family.startswith("mega_cap_ai_"):
            return "company"
        if "expiry" in event_family or temporal.expiry_cycle_state == "expiry_day":
            return "expiry"
        return None

    def _has_venue_session_distortion(self, temporal: TemporalContextOutput) -> bool:
        return bool(temporal.calendar_closure_classes)

    def _band_sort(self, band: ModifierPriorityBand) -> int:
        return self._PRECEDENCE_ORDER[band]

    def _degradation_rank(self, step: DegradationStep) -> int:
        ordered = [
            DegradationStep.NORMAL,
            DegradationStep.CONFIRMATION_TIGHTENED,
            DegradationStep.CONFIDENCE_REDUCED,
            DegradationStep.SIZE_REDUCED,
            DegradationStep.WATCH_ONLY,
            DegradationStep.STAND_DOWN,
            DegradationStep.VETO,
        ]
        return ordered.index(step)
