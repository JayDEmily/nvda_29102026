from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nvda_desk.config_models import (
    CoefficientModuleConfig,
    ConfigBundle,
    EvaluationConfigDocument,
    RuntimeSettingsDocument,
    StrategyVariantDefinition,
    load_config_bundle,
)
from nvda_desk.schemas.config import (
    CoefficientGroupListResponse,
    CoefficientGroupParameterPayload,
    CoefficientGroupPayload,
    StrategyVariantListResponse,
    StrategyVariantPayload,
    StrategyVariantSummaryPayload,
)
from nvda_desk.schemas.slv import StrategicLadderReplayInput


class ConfigSurfaceLookupError(LookupError):
    pass


@dataclass(frozen=True)
class ReplayOverrideSet:
    entry_gate_score_floor: float | None = None
    zone_score_threshold: float | None = None
    distance_to_vwap_soft_limit_pct: float | None = None
    risk_vix_caution_threshold: float | None = None
    risk_vix_hot_threshold: float | None = None
    risk_budget_remaining_pct: float | None = None
    sources: tuple[str, ...] = ()


class ConfigSurfaceService:
    def __init__(self, config_dir: Path):
        self._config_dir = config_dir
        self._bundle: ConfigBundle | None = None

    def bundle(self) -> ConfigBundle:
        if self._bundle is None:
            self._bundle = load_config_bundle(self._config_dir)
        return self._bundle

    def runtime_settings(self) -> RuntimeSettingsDocument:
        return self.bundle().runtime_settings

    def evaluation_config(self) -> EvaluationConfigDocument:
        return self.bundle().evaluation_config

    def list_coefficient_groups(self) -> CoefficientGroupListResponse:
        groups: list[CoefficientGroupPayload] = []
        runtime = self.bundle().coefficients_registry.runtime
        for layer_name in (
            "layer1_signals",
            "layer2_scoring",
            "layer3_decision",
            "layer4_execution",
        ):
            layer = getattr(runtime, layer_name)
            for key, config in sorted(layer.items()):
                groups.append(self._coefficient_group_payload(layer_name, key, config))
        return CoefficientGroupListResponse(groups=groups)

    def get_coefficient_group(self, key: str) -> CoefficientGroupPayload:
        layer_name, config = self._lookup_coefficient_group(key)
        return self._coefficient_group_payload(layer_name, key, config)

    def list_strategy_variants(self) -> StrategyVariantListResponse:
        variants = [
            StrategyVariantSummaryPayload(
                name=name,
                description=variant.description,
                weight_override_keys=sorted(variant.overrides.weights.keys()),
                coefficient_override_keys=sorted(variant.overrides.coefficients.keys()),
                supported_sandbox_overrides=self._variant_supported_overrides(variant),
            )
            for name, variant in sorted(self.bundle().strategy_variants.variants.items())
        ]
        return StrategyVariantListResponse(variants=variants)

    def get_strategy_variant(self, name: str) -> StrategyVariantPayload:
        variant = self._lookup_strategy_variant(name)
        return StrategyVariantPayload(
            name=name,
            description=variant.description,
            enabled_module_counts={
                "layer1_signals": len(variant.enabled_modules.layer1_signals),
                "layer2_scoring": len(variant.enabled_modules.layer2_scoring),
                "layer3_decision": len(variant.enabled_modules.layer3_decision),
                "layer4_execution": len(variant.enabled_modules.layer4_execution),
            },
            weight_overrides=variant.overrides.weights,
            coefficient_overrides=variant.overrides.coefficients,
            runtime_overrides=variant.overrides.runtime,
            supported_sandbox_overrides=self._variant_supported_overrides(variant),
        )

    def apply_replay_overrides(
        self,
        payload: StrategicLadderReplayInput,
        *,
        strategy_variant_name: str | None = None,
        coefficient_group_name: str | None = None,
    ) -> StrategicLadderReplayInput:
        overrides = self.resolve_replay_overrides(
            strategy_variant_name=strategy_variant_name,
            coefficient_group_name=coefficient_group_name,
        )
        update: dict[str, float] = {}
        if overrides.entry_gate_score_floor is not None:
            update["entry_gate_score_floor"] = overrides.entry_gate_score_floor
        if overrides.zone_score_threshold is not None:
            update["zone_score_threshold"] = overrides.zone_score_threshold
        if overrides.distance_to_vwap_soft_limit_pct is not None:
            update["distance_to_vwap_soft_limit_pct"] = overrides.distance_to_vwap_soft_limit_pct
        if overrides.risk_vix_caution_threshold is not None:
            update["risk_vix_caution_threshold"] = overrides.risk_vix_caution_threshold
        if overrides.risk_vix_hot_threshold is not None:
            update["risk_vix_hot_threshold"] = overrides.risk_vix_hot_threshold
        if overrides.risk_budget_remaining_pct is not None:
            update["risk_budget_remaining_pct"] = overrides.risk_budget_remaining_pct
        if not update:
            return payload
        return payload.model_copy(update=update)

    def resolve_replay_overrides(
        self,
        *,
        strategy_variant_name: str | None = None,
        coefficient_group_name: str | None = None,
    ) -> ReplayOverrideSet:
        entry_gate_score_floor: float | None = None
        zone_score_threshold: float | None = None
        distance_limit: float | None = None
        risk_vix_caution: float | None = None
        risk_vix_hot: float | None = None
        risk_budget_remaining_pct: float | None = None
        sources: list[str] = []

        if strategy_variant_name is not None:
            variant = self._lookup_strategy_variant(strategy_variant_name)
            entry_gate = variant.overrides.coefficients.get("L3_01", {}).get("score_floor")
            if isinstance(entry_gate, int | float):
                entry_gate_score_floor = float(entry_gate)
                sources.append(f"variant:{strategy_variant_name}:L3_01.score_floor")
            zone_threshold = variant.overrides.coefficients.get("L3_03", {}).get(
                "zone_score_threshold"
            )
            if isinstance(zone_threshold, int | float):
                zone_score_threshold = float(zone_threshold)
                sources.append(f"variant:{strategy_variant_name}:L3_03.zone_score_threshold")
            risk_budget = variant.overrides.coefficients.get("L4_02", {}).get("max_risk_per_trade")
            if isinstance(risk_budget, int | float):
                risk_budget_remaining_pct = max(
                    5.0, min((float(risk_budget) / 500.0) * 100.0, 100.0)
                )
                sources.append(f"variant:{strategy_variant_name}:L4_02.max_risk_per_trade")

        if coefficient_group_name is not None:
            _, group = self._lookup_coefficient_group(coefficient_group_name)
            if coefficient_group_name == "S06":
                risk_threshold = group.coefficients.get("vix_risk_threshold")
                if risk_threshold is not None and isinstance(risk_threshold.value, int | float):
                    risk_vix_caution = float(risk_threshold.value)
                    risk_vix_hot = float(risk_threshold.value) + 8.0
                    sources.append("coeff:S06.vix_risk_threshold")
            if coefficient_group_name == "S08":
                vwap_limit = group.coefficients.get("vwap_proximity_pct")
                if vwap_limit is not None and isinstance(vwap_limit.value, int | float):
                    distance_limit = float(vwap_limit.value)
                    sources.append("coeff:S08.vwap_proximity_pct")

        return ReplayOverrideSet(
            entry_gate_score_floor=entry_gate_score_floor,
            zone_score_threshold=zone_score_threshold,
            distance_to_vwap_soft_limit_pct=distance_limit,
            risk_vix_caution_threshold=risk_vix_caution,
            risk_vix_hot_threshold=risk_vix_hot,
            risk_budget_remaining_pct=risk_budget_remaining_pct,
            sources=tuple(sources),
        )

    def effective_weight(
        self, *, config_key: str | None, strategy_variant_name: str | None = None
    ) -> float | None:
        if config_key is None:
            return None
        _, group = self._lookup_coefficient_group(config_key)
        weight = group.weight
        if strategy_variant_name is not None:
            variant = self._lookup_strategy_variant(strategy_variant_name)
            variant_weight = variant.overrides.weights.get(config_key)
            if variant_weight is not None:
                return float(variant_weight)
        return float(weight)

    def reserve_vix_thresholds(
        self, *, coefficient_group_name: str | None = None
    ) -> tuple[float, float]:
        if coefficient_group_name == "S06":
            _, group = self._lookup_coefficient_group(coefficient_group_name)
            risk_threshold = group.coefficients.get("vix_risk_threshold")
            if risk_threshold is not None and isinstance(risk_threshold.value, int | float):
                caution = float(risk_threshold.value)
                return caution, caution + 8.0
        return 18.0, 25.0

    def _lookup_coefficient_group(self, key: str) -> tuple[str, CoefficientModuleConfig]:
        runtime = self.bundle().coefficients_registry.runtime
        for layer_name in (
            "layer1_signals",
            "layer2_scoring",
            "layer3_decision",
            "layer4_execution",
        ):
            layer = getattr(runtime, layer_name)
            if key in layer:
                return layer_name, layer[key]
        raise ConfigSurfaceLookupError(f"unknown coefficient group: {key}")

    def _lookup_strategy_variant(self, name: str) -> StrategyVariantDefinition:
        variant = self.bundle().strategy_variants.variants.get(name)
        if variant is None:
            raise ConfigSurfaceLookupError(f"unknown strategy variant: {name}")
        return variant

    def _coefficient_group_payload(
        self,
        layer_name: str,
        key: str,
        config: CoefficientModuleConfig,
    ) -> CoefficientGroupPayload:
        return CoefficientGroupPayload(
            key=key,
            layer=layer_name,
            module=config.module,
            weight=config.weight,
            enabled=config.enabled,
            parameters=[
                CoefficientGroupParameterPayload(
                    name=name,
                    value=parameter.value,
                    test_min=parameter.test_min,
                    test_max=parameter.test_max,
                    step=parameter.step,
                    notes=parameter.notes,
                )
                for name, parameter in sorted(config.coefficients.items())
            ],
            supported_sandbox_overrides=self._coefficient_supported_overrides(key),
        )

    def _coefficient_supported_overrides(self, key: str) -> list[str]:
        if key == "S06":
            return ["risk_vix_caution_threshold", "risk_vix_hot_threshold"]
        if key == "S08":
            return ["distance_to_vwap_soft_limit_pct"]
        return []

    def _variant_supported_overrides(self, variant: StrategyVariantDefinition) -> list[str]:
        supported: list[str] = []
        if "L3_01" in variant.overrides.coefficients:
            supported.append("entry_gate_score_floor")
        if "L3_03" in variant.overrides.coefficients:
            supported.append("zone_score_threshold")
        if "L4_02" in variant.overrides.coefficients:
            supported.append("risk_budget_remaining_pct")
        if variant.overrides.weights:
            supported.append("allocation_weight_overrides")
        return supported
