from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.state_policy import MutableRuntimeSurface, PolicyStageOwner

ScalarValue = float | int | str | bool


class RuntimeEnvironmentConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    mode: str
    timezone: str
    trading_calendar: str
    symbol: str
    peers: list[str] = Field(default_factory=list)


class RuntimePathsConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    project_root: str | None = None
    db_path: str | None = None
    signal_score_db_path: str | None = None
    logs_dir: str | None = None
    snapshots_dir: str | None = None
    fixtures_dir: str | None = None
    module_registry_path: str | None = None
    coefficients_registry_path: str | None = None
    coefficient_authority_path: str | None = None
    strategy_variants_path: str | None = None


class RuntimeSafetyConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    block_if_macro_risk_off: bool
    block_if_no_valid_strike: bool
    block_if_missing_options_snapshot: bool
    block_if_missing_vwap_snapshot: bool


class BrokerPrimaryConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    enabled: bool = True
    host: str | None = None
    port: int | None = None
    client_id: int | None = None
    account: str | None = None
    market_data_type: str | None = None
    use_snapshot_data: bool | None = None
    reconnect_on_drop: bool | None = None


class BrokerFallbackConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    allow_secondary_data_vendor: bool = False
    allow_csv_replay: bool = False


class BrokerConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    primary: str
    ibkr: BrokerPrimaryConfig | None = None
    fallbacks: BrokerFallbackConfig | None = None


class RuntimeSettingsDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    profile: str
    environment: RuntimeEnvironmentConfig
    paths: RuntimePathsConfig | None = None
    broker: BrokerConfig | None = None
    safety: RuntimeSafetyConfig


class EvaluationPathsConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    runtime_db_path: str
    signal_score_db_path: str
    logs_dir: str
    output_dir: str
    module_registry_path: str | None = None
    coefficients_registry_path: str | None = None
    coefficient_authority_path: str | None = None
    strategy_variants_path: str | None = None


class EvaluationConfigDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    profile: str
    paths: EvaluationPathsConfig
    notes: list[str] = Field(default_factory=list)


class CoefficientValueSpec(BaseModel):
    model_config = ConfigDict(extra="ignore")

    value: ScalarValue
    test_min: float | int | None = None
    test_max: float | int | None = None
    step: float | int | None = None
    notes: str | None = None


class CoefficientModuleConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    module: str
    weight: float = Field(default=1.0, ge=0)
    enabled: bool = True
    coefficients: dict[str, CoefficientValueSpec] = Field(default_factory=dict)


class RuntimeCoefficientGroups(BaseModel):
    model_config = ConfigDict(extra="ignore")

    layer1_signals: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer2_scoring: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer3_decision: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)
    layer4_execution: dict[str, CoefficientModuleConfig] = Field(default_factory=dict)


class CoefficientsRegistryDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    notes: list[str] = Field(default_factory=list)
    globals: dict[str, Any] = Field(default_factory=dict)
    runtime: RuntimeCoefficientGroups = Field(default_factory=RuntimeCoefficientGroups)


class CoefficientAuthorityUnit(StrEnum):
    SCORE_FRACTION_0_TO_1 = "score_fraction_0_to_1"
    PERCENT = "percent"
    VOLATILITY_INDEX_POINTS = "volatility_index_points"
    BASIS_POINTS = "basis_points"
    RATIO = "ratio"
    MINUTES = "minutes"
    BOOLEAN_FLAG = "boolean_flag"


class CoefficientBoundClass(StrEnum):
    ONE_SIDED_CLAMP = "one_sided_clamp"
    SCORE_THRESHOLD = "score_threshold"
    STATE_DEFINITION_THRESHOLD = "state_definition_threshold"
    TIMING_PARAMETER = "timing_parameter"
    BOOLEAN_REQUIREMENT = "boolean_requirement"


class CoefficientRangeAsymmetry(StrEnum):
    DOWNWARD_ONLY = "downward_only"
    DOWNWARD_FRIENDLY = "downward_friendly"
    NARROW_BIDIRECTIONAL = "narrow_bidirectional"
    SEMANTIC_THRESHOLD = "semantic_threshold"
    CLOCK_WINDOW = "clock_window"
    BOOLEAN_ONLY = "boolean_only"


class CoefficientTransformFamily(StrEnum):
    STATE_CONDITIONED_MODIFIER = "state_conditioned_modifier"
    THRESHOLD_COMPARE = "threshold_compare"
    CLOCK_WINDOW = "clock_window"
    BOOLEAN_OVERRIDE = "boolean_override"


class CoefficientUpstreamDriver(StrEnum):
    CLOCK_ENVELOPE = "clock_envelope"
    EVENT_WINDOW_STATE = "event_window_state"
    SIGNAL_CONFLICT_STATE = "signal_conflict_state"
    PERMISSION_STATE = "permission_state"
    DEALER_PRESSURE_STATE = "dealer_pressure_state"
    GAMMA_STATE = "gamma_state"
    OPTIONS_BEHAVIOR_CLUSTER = "options_behavior_cluster"
    VOLATILITY_REGIME = "volatility_regime"
    INVENTORY_POSTURE_STATE = "inventory_posture_state"
    FRESH_VS_INVENTORY_STATE = "fresh_vs_inventory_state"
    CAPITAL_LOCKUP_STATE = "capital_lockup_state"
    RELATIVE_VOLUME_RATIO = "relative_volume_ratio"
    RV5_BPS = "rv5_bps"
    DISTANCE_TO_VWAP_BPS = "distance_to_vwap_bps"
    IMPULSE_AGE_MINUTES = "impulse_age_minutes"
    RANGE5_BPS = "range5_bps"
    VWAP_SLOPE_5M_BPS = "vwap_slope_5m_bps"
    MINUTES_TO_CLOSE = "minutes_to_close"


class TemporalThresholdId(StrEnum):
    OPEN_DISORDER_RELVOL_MIN = "open_disorder_relvol_min"
    OPEN_DISORDER_RV5_BPS_MIN = "open_disorder_rv5_bps_min"
    OPEN_DISORDER_VWAP_DIST_BPS_MIN = "open_disorder_vwap_dist_bps_min"
    ANCHOR_VWAP_DIST_BPS_MAX = "anchor_vwap_dist_bps_max"
    ANCHOR_RV5_BPS_MAX = "anchor_rv5_bps_max"
    ANCHOR_RELVOL_MIN = "anchor_relvol_min"
    ANCHOR_RELVOL_MAX = "anchor_relvol_max"
    ANCHOR_IMPULSE_AGE_MIN = "anchor_impulse_age_min"
    COMPRESSION_RV5_BPS_MAX = "compression_rv5_bps_max"
    COMPRESSION_RANGE5_BPS_MAX = "compression_range5_bps_max"
    COMPRESSION_VWAP_DIST_BPS_MAX = "compression_vwap_dist_bps_max"
    COMPRESSION_RELVOL_MAX = "compression_relvol_max"
    TREND_VWAP_SLOPE_BPS_MIN = "trend_vwap_slope_bps_min"
    TREND_VWAP_DIST_BPS_MIN = "trend_vwap_dist_bps_min"
    TREND_RELVOL_MIN = "trend_relvol_min"
    TREND_IMPULSE_AGE_MAX = "trend_impulse_age_max"


class TimingParameterId(StrEnum):
    POWER_HOUR_WINDOW_MIN = "power_hour_window_min"
    UNWIND_WINDOW_MIN = "unwind_window_min"


def _validate_numeric_range(*, minimum: float, baseline: float, maximum: float, units: CoefficientAuthorityUnit) -> None:
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    if not minimum <= baseline <= maximum:
        raise ValueError("baseline must lie inside minimum/maximum bounds")
    if units is CoefficientAuthorityUnit.SCORE_FRACTION_0_TO_1 and not (0.0 <= minimum <= maximum <= 1.0):
        raise ValueError("score_fraction_0_to_1 entries must stay inside [0, 1]")
    if units is CoefficientAuthorityUnit.PERCENT and not (0.0 <= minimum <= maximum <= 100.0):
        raise ValueError("percent entries must stay inside [0, 100]")
    if units is CoefficientAuthorityUnit.VOLATILITY_INDEX_POINTS and not (0.0 <= minimum <= maximum <= 100.0):
        raise ValueError("volatility_index_points entries must stay inside [0, 100]")
    if units is CoefficientAuthorityUnit.BASIS_POINTS and not (0.0 <= minimum <= maximum <= 500.0):
        raise ValueError("basis_points entries must stay inside [0, 500]")
    if units is CoefficientAuthorityUnit.RATIO and not (0.0 < minimum <= maximum <= 5.0):
        raise ValueError("ratio entries must stay inside (0, 5]")
    if units is CoefficientAuthorityUnit.MINUTES and not (0.0 < minimum <= maximum <= 390.0):
        raise ValueError("minutes entries must stay inside (0, 390]")
    if units is CoefficientAuthorityUnit.BOOLEAN_FLAG:
        raise ValueError("numeric range validation cannot be applied to boolean units")


class MutableNumericSurfaceAuthoritySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface_id: MutableRuntimeSurface
    owner_stage: PolicyStageOwner
    units: CoefficientAuthorityUnit
    bound_class: CoefficientBoundClass
    asymmetry: CoefficientRangeAsymmetry
    baseline: float
    minimum: float
    maximum: float
    transform_family: CoefficientTransformFamily = CoefficientTransformFamily.STATE_CONDITIONED_MODIFIER
    allowed_upstream_drivers: list[CoefficientUpstreamDriver] = Field(default_factory=list)
    activation_gate: Literal["Gate 124"] = "Gate 124"
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_semantics(self) -> MutableNumericSurfaceAuthoritySpec:
        if self.units is CoefficientAuthorityUnit.BOOLEAN_FLAG:
            raise ValueError("mutable numeric surfaces cannot use boolean units")
        if self.bound_class not in {
            CoefficientBoundClass.ONE_SIDED_CLAMP,
            CoefficientBoundClass.SCORE_THRESHOLD,
        }:
            raise ValueError("mutable numeric surfaces must be clamp or score-threshold entries")
        if self.transform_family is not CoefficientTransformFamily.STATE_CONDITIONED_MODIFIER:
            raise ValueError("mutable numeric surfaces must use state_conditioned_modifier transform family")
        _validate_numeric_range(
            minimum=float(self.minimum),
            baseline=float(self.baseline),
            maximum=float(self.maximum),
            units=self.units,
        )
        if self.surface_id is MutableRuntimeSurface.TARGET_FRESH_DEPLOYABLE_PCT and self.maximum != self.baseline:
            raise ValueError("target_fresh_deployable_pct must not exceed its tranche-one baseline")
        return self


class MutableBooleanSurfaceAuthoritySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface_id: Literal[MutableRuntimeSurface.HEDGE_REQUIRED]
    owner_stage: PolicyStageOwner
    units: Literal[CoefficientAuthorityUnit.BOOLEAN_FLAG] = CoefficientAuthorityUnit.BOOLEAN_FLAG
    bound_class: Literal[CoefficientBoundClass.BOOLEAN_REQUIREMENT] = CoefficientBoundClass.BOOLEAN_REQUIREMENT
    asymmetry: Literal[CoefficientRangeAsymmetry.BOOLEAN_ONLY] = CoefficientRangeAsymmetry.BOOLEAN_ONLY
    baseline: bool
    transform_family: Literal[CoefficientTransformFamily.BOOLEAN_OVERRIDE] = CoefficientTransformFamily.BOOLEAN_OVERRIDE
    allowed_upstream_drivers: list[CoefficientUpstreamDriver] = Field(default_factory=list)
    activation_gate: Literal["Gate 124"] = "Gate 124"
    notes: list[str] = Field(default_factory=list)


class TemporalThresholdAuthoritySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold_id: TemporalThresholdId
    owner_stage: Literal[PolicyStageOwner.TEMPORAL] = PolicyStageOwner.TEMPORAL
    units: CoefficientAuthorityUnit
    bound_class: Literal[CoefficientBoundClass.STATE_DEFINITION_THRESHOLD] = CoefficientBoundClass.STATE_DEFINITION_THRESHOLD
    asymmetry: Literal[CoefficientRangeAsymmetry.SEMANTIC_THRESHOLD] = CoefficientRangeAsymmetry.SEMANTIC_THRESHOLD
    baseline: float
    minimum: float
    maximum: float
    transform_family: Literal[CoefficientTransformFamily.THRESHOLD_COMPARE] = CoefficientTransformFamily.THRESHOLD_COMPARE
    allowed_upstream_drivers: list[CoefficientUpstreamDriver] = Field(default_factory=list)
    workbook_ref: str
    activation_gate: Literal["Gate 126"] = "Gate 126"
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_semantics(self) -> TemporalThresholdAuthoritySpec:
        if self.units is CoefficientAuthorityUnit.BOOLEAN_FLAG:
            raise ValueError("temporal thresholds cannot use boolean units")
        _validate_numeric_range(
            minimum=float(self.minimum),
            baseline=float(self.baseline),
            maximum=float(self.maximum),
            units=self.units,
        )
        return self


class TimingParameterAuthoritySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    parameter_id: TimingParameterId
    owner_stage: Literal[PolicyStageOwner.TEMPORAL] = PolicyStageOwner.TEMPORAL
    units: Literal[CoefficientAuthorityUnit.MINUTES] = CoefficientAuthorityUnit.MINUTES
    bound_class: Literal[CoefficientBoundClass.TIMING_PARAMETER] = CoefficientBoundClass.TIMING_PARAMETER
    asymmetry: Literal[CoefficientRangeAsymmetry.CLOCK_WINDOW] = CoefficientRangeAsymmetry.CLOCK_WINDOW
    baseline: float
    minimum: float
    maximum: float
    transform_family: Literal[CoefficientTransformFamily.CLOCK_WINDOW] = CoefficientTransformFamily.CLOCK_WINDOW
    allowed_upstream_drivers: list[CoefficientUpstreamDriver] = Field(default_factory=list)
    workbook_ref: str
    activation_gate: Literal["Gate 126"] = "Gate 126"
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_semantics(self) -> TimingParameterAuthoritySpec:
        _validate_numeric_range(
            minimum=float(self.minimum),
            baseline=float(self.baseline),
            maximum=float(self.maximum),
            units=self.units,
        )
        return self


class CoefficientAuthorityDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["coefficient_authority.v1"]
    authority_version: str
    notes: list[str] = Field(default_factory=list)
    mutable_numeric_surfaces: list[MutableNumericSurfaceAuthoritySpec] = Field(default_factory=list)
    mutable_boolean_surfaces: list[MutableBooleanSurfaceAuthoritySpec] = Field(default_factory=list)
    temporal_thresholds: list[TemporalThresholdAuthoritySpec] = Field(default_factory=list)
    timing_parameters: list[TimingParameterAuthoritySpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_document(self) -> CoefficientAuthorityDocument:
        numeric_ids = [item.surface_id for item in self.mutable_numeric_surfaces]
        boolean_ids = [item.surface_id for item in self.mutable_boolean_surfaces]
        if len(set(numeric_ids)) != len(numeric_ids):
            raise ValueError("duplicate mutable numeric surface ids are not allowed")
        if len(set(boolean_ids)) != len(boolean_ids):
            raise ValueError("duplicate mutable boolean surface ids are not allowed")
        threshold_ids = [item.threshold_id for item in self.temporal_thresholds]
        if len(set(threshold_ids)) != len(threshold_ids):
            raise ValueError("duplicate temporal threshold ids are not allowed")
        timing_ids = [item.parameter_id for item in self.timing_parameters]
        if len(set(timing_ids)) != len(timing_ids):
            raise ValueError("duplicate timing parameter ids are not allowed")
        timing_by_id = {item.parameter_id: item for item in self.timing_parameters}
        power_hour = timing_by_id.get(TimingParameterId.POWER_HOUR_WINDOW_MIN)
        unwind = timing_by_id.get(TimingParameterId.UNWIND_WINDOW_MIN)
        if power_hour is not None and unwind is not None and not (
            float(power_hour.minimum) > float(unwind.minimum)
            and float(power_hour.baseline) > float(unwind.baseline)
            and float(power_hour.maximum) > float(unwind.maximum)
        ):
            raise ValueError(
                "power_hour_window_min must stay above unwind_window_min across the full envelope"
            )
        numeric_by_surface = {item.surface_id: item for item in self.mutable_numeric_surfaces}
        caution = numeric_by_surface.get(MutableRuntimeSurface.RISK_VIX_CAUTION_THRESHOLD)
        hot = numeric_by_surface.get(MutableRuntimeSurface.RISK_VIX_HOT_THRESHOLD)
        if caution is not None and hot is not None and not (
            caution.baseline < hot.baseline
            and caution.minimum < hot.minimum
            and caution.maximum < hot.maximum
        ):
            raise ValueError(
                "risk_vix_hot_threshold must stay above risk_vix_caution_threshold across the full envelope"
            )
        return self

    def mutable_numeric_surface_index(self) -> dict[MutableRuntimeSurface, MutableNumericSurfaceAuthoritySpec]:
        return {item.surface_id: item for item in self.mutable_numeric_surfaces}

    def mutable_boolean_surface_index(self) -> dict[MutableRuntimeSurface, MutableBooleanSurfaceAuthoritySpec]:
        return {item.surface_id: item for item in self.mutable_boolean_surfaces}

    def mutable_surface_index(self) -> dict[MutableRuntimeSurface, MutableNumericSurfaceAuthoritySpec | MutableBooleanSurfaceAuthoritySpec]:
        payload: dict[MutableRuntimeSurface, MutableNumericSurfaceAuthoritySpec | MutableBooleanSurfaceAuthoritySpec] = {
            item.surface_id: item for item in self.mutable_numeric_surfaces
        }
        payload.update({item.surface_id: item for item in self.mutable_boolean_surfaces})
        return payload

    def temporal_threshold_index(self) -> dict[TemporalThresholdId, TemporalThresholdAuthoritySpec]:
        return {item.threshold_id: item for item in self.temporal_thresholds}

    def timing_parameter_index(self) -> dict[TimingParameterId, TimingParameterAuthoritySpec]:
        return {item.parameter_id: item for item in self.timing_parameters}

    @classmethod
    def from_yaml_text(cls, text: str) -> CoefficientAuthorityDocument:
        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise TypeError("expected mapping at coefficient authority root")
        return cls.model_validate(loaded)

    @classmethod
    def from_yaml_path(cls, path: Path) -> CoefficientAuthorityDocument:
        return cls.from_yaml_text(path.read_text(encoding="utf-8"))

    def to_yaml_text(self) -> str:
        return str(yaml.safe_dump(self.model_dump(mode="json"), sort_keys=False))




def default_coefficient_authority_path(repo_root: Path | None = None) -> Path:
    """Return the repo-native governed coefficient authority file path."""

    resolved_root = repo_root or Path(__file__).resolve().parents[2]
    return resolved_root / "config" / "coefficient_authority.v1.yaml"


class VariantEnabledModules(BaseModel):
    model_config = ConfigDict(extra="ignore")

    layer1_signals: list[str] = Field(default_factory=list)
    layer2_scoring: list[str] = Field(default_factory=list)
    layer3_decision: list[str] = Field(default_factory=list)
    layer4_execution: list[str] = Field(default_factory=list)


class VariantOverrides(BaseModel):
    model_config = ConfigDict(extra="ignore")

    weights: dict[str, float] = Field(default_factory=dict)
    coefficients: dict[str, dict[str, ScalarValue]] = Field(default_factory=dict)
    runtime: dict[str, Any] = Field(default_factory=dict)


class StrategyVariantDefinition(BaseModel):
    model_config = ConfigDict(extra="ignore")

    description: str
    enabled_modules: VariantEnabledModules = Field(default_factory=VariantEnabledModules)
    overrides: VariantOverrides = Field(default_factory=VariantOverrides)


class StrategyVariantDefaults(BaseModel):
    model_config = ConfigDict(extra="ignore")

    base_variant: str
    inherit_missing_from: str
    clamp_scores: bool = True
    require_human_review_for_live_use: bool = True


class StrategyVariantsDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    version: str
    project: str
    notes: list[str] = Field(default_factory=list)
    defaults: StrategyVariantDefaults
    variants: dict[str, StrategyVariantDefinition] = Field(default_factory=dict)


class ConfigBundle(BaseModel):
    runtime_settings: RuntimeSettingsDocument
    evaluation_config: EvaluationConfigDocument
    coefficients_registry: CoefficientsRegistryDocument
    coefficient_authority: CoefficientAuthorityDocument
    strategy_variants: StrategyVariantsDocument


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise TypeError(f"expected mapping at {path}")
    return raw


def load_config_bundle(config_dir: Path) -> ConfigBundle:
    return ConfigBundle(
        runtime_settings=RuntimeSettingsDocument.model_validate(
            _load_yaml(config_dir / "runtime_settings.example.yaml")
        ),
        evaluation_config=EvaluationConfigDocument.model_validate(
            _load_yaml(config_dir / "evaluation_config.example.yaml")
        ),
        coefficients_registry=CoefficientsRegistryDocument.model_validate(
            _load_yaml(config_dir / "coefficients_registry.example.yaml")
        ),
        coefficient_authority=CoefficientAuthorityDocument.model_validate(
            _load_yaml(config_dir / default_coefficient_authority_path(config_dir.parent).name)
        ),
        strategy_variants=StrategyVariantsDocument.model_validate(
            _load_yaml(config_dir / "strategy_variants.example.yaml")
        ),
    )
