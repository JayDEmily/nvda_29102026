"""Typed checked-in playbook registry contracts.

These schemas define the checked-in deterministic playbook registry. Registry v2
extends the earlier flat list so the runtime can represent trader-real
hierarchy without changing the runtime order:

family -> setup variant -> execution expression.

The legacy flat `playbooks` list remains as an explicit compatibility bridge for
runtime components that still iterate one ordered list of live playbooks.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self, cast

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.cognition import PlaybookAction, PlaybookDecision


class PlaybookHorizon(StrEnum):
    """Canonical horizon taxonomy for playbook registry v2."""

    INTRADAY = "intraday"
    OVERNIGHT = "overnight"
    WEEKEND = "weekend"
    EVENT_CARRY = "event_carry"


class PlaybookDecisionProfile(BaseModel):
    """Registry-backed output contract for one playbook decision state.

    `sizing_fraction` is retained as a compatibility field only and is not live
    fresh-capital authority for the serial stack.
    """

    model_config = ConfigDict(extra="forbid")

    decision: PlaybookDecision
    action_bias: PlaybookAction
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False


class PlaybookConstraints(BaseModel):
    """Bounded eligibility constraints owned by the registry rather than prose."""

    model_config = ConfigDict(extra="forbid")

    allowed_desk_windows: list[str] = Field(default_factory=list)
    blocked_event_window_states: list[str] = Field(default_factory=list)
    required_options_behavior_clusters: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PlaybookRiskOverrides(BaseModel):
    """Optional risk and posture overrides for one setup variant."""

    model_config = ConfigDict(extra="forbid")

    block_permission_states: list[str] = Field(default_factory=list)
    watch_only_permission_states: list[str] = Field(default_factory=list)
    force_hedge_when_dealer_pressure_states: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PlaybookFamilySpec(BaseModel):
    """Top-level trading family in the registry hierarchy."""

    model_config = ConfigDict(extra="forbid")

    family_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    thesis: str = Field(min_length=1)
    active: bool = True
    notes: list[str] = Field(default_factory=list)


class SetupVariantSpec(BaseModel):
    """One deterministic setup variant beneath a top-level family."""

    model_config = ConfigDict(extra="forbid")

    setup_variant_id: str = Field(min_length=1)
    family_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    horizon: PlaybookHorizon = PlaybookHorizon.INTRADAY
    priority: int = Field(ge=1)
    execution_expression_id: str = Field(min_length=1)
    legacy_playbook_id: str | None = None
    constraints: PlaybookConstraints = Field(default_factory=PlaybookConstraints)
    risk_overrides: PlaybookRiskOverrides = Field(default_factory=PlaybookRiskOverrides)
    active: bool = True
    notes: list[str] = Field(default_factory=list)


class PlaybookSpec(BaseModel):
    """One checked-in legacy-compatible live-playbook definition."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    execution_template_id: str = Field(min_length=1)
    execution_expression_id: str | None = None
    family_id: str = Field(min_length=1)
    setup_variant_id: str = Field(min_length=1)
    horizon: PlaybookHorizon = PlaybookHorizon.INTRADAY
    priority: int = Field(ge=1)
    active: bool = True
    constraints: PlaybookConstraints = Field(default_factory=PlaybookConstraints)
    risk_overrides: PlaybookRiskOverrides = Field(default_factory=PlaybookRiskOverrides)
    eligible: PlaybookDecisionProfile
    watch_only: PlaybookDecisionProfile
    ineligible: PlaybookDecisionProfile
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_decision_profiles(self) -> Self:
        if self.execution_expression_id is None:
            self.execution_expression_id = self.execution_template_id
        if self.eligible.decision is not PlaybookDecision.ELIGIBLE:
            raise ValueError("eligible profile must use PlaybookDecision.ELIGIBLE")
        if self.watch_only.decision is not PlaybookDecision.WATCH_ONLY:
            raise ValueError("watch_only profile must use PlaybookDecision.WATCH_ONLY")
        if self.ineligible.decision is not PlaybookDecision.INELIGIBLE:
            raise ValueError("ineligible profile must use PlaybookDecision.INELIGIBLE")
        return self


class ExecutionTemplateSpec(BaseModel):
    """Execution-shape contract shared by one or more playbooks."""

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1)
    entry_style: str = Field(min_length=1)
    watch_execution_style: str = Field(default="watchlist", min_length=1)
    scaling_step_factors: list[float] = Field(default_factory=list)
    default_inventory_action: str = Field(min_length=1)
    default_fresh_capital_action: str = Field(min_length=1)
    thesis_invalidation_state: str = Field(min_length=1)
    invalidation_reasons: list[str] = Field(default_factory=list)
    exit_reasons: list[str] = Field(default_factory=list)
    hedge_exit_reason: str = Field(default="overlay_hedge_if_gamma_reaccelerates", min_length=1)
    passive_aggressive_bias: str = Field(default="balanced", min_length=1)
    ladder_spacing_bps: float = Field(default=20.0, ge=0.0)
    max_chase_distance_bps: float = Field(default=35.0, ge=0.0)
    stop_distance_bps: float = Field(default=55.0, ge=0.0)
    take_profit_distance_bps: float = Field(default=85.0, ge=0.0)
    hedge_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    base_risk_per_slice_pct: float = Field(default=0.10, ge=0.0)
    respect_posture_biases: bool = True
    posture_override_actions: list[str] = Field(default_factory=lambda: ["reduce", "trim", "hedge"])
    inventory_pressure_states: list[str] = Field(default_factory=lambda: ["trapped", "full"])
    inventory_pressure_exit_reason: str = Field(default="respect_inventory_pressure", min_length=1)

    @model_validator(mode="after")
    def _validate_scaling_steps(self) -> Self:
        if any(step < 0.0 for step in self.scaling_step_factors):
            raise ValueError("scaling_step_factors must be non-negative")
        return self


class PlaybookRegistryDocument(BaseModel):
    """Checked-in registry containing live playbooks and execution templates."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(min_length=1)
    registry_version: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)
    families: list[PlaybookFamilySpec] = Field(default_factory=list)
    setup_variants: list[SetupVariantSpec] = Field(default_factory=list)
    execution_templates: list[ExecutionTemplateSpec] = Field(default_factory=list)
    playbooks: list[PlaybookSpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_cross_references(self) -> Self:
        template_ids = [template.template_id for template in self.execution_templates]
        if len(set(template_ids)) != len(template_ids):
            raise ValueError("execution template ids must be unique")
        family_ids = [family.family_id for family in self.families]
        if len(set(family_ids)) != len(family_ids):
            raise ValueError("family ids must be unique")
        variant_ids = [variant.setup_variant_id for variant in self.setup_variants]
        if len(set(variant_ids)) != len(variant_ids):
            raise ValueError("setup variant ids must be unique")
        variant_priorities = [variant.priority for variant in self.setup_variants]
        if len(set(variant_priorities)) != len(variant_priorities):
            raise ValueError("setup variant priorities must be unique")
        playbook_ids = [playbook.playbook_id for playbook in self.playbooks]
        if len(set(playbook_ids)) != len(playbook_ids):
            raise ValueError("playbook ids must be unique")
        priorities = [playbook.priority for playbook in self.playbooks]
        if len(set(priorities)) != len(priorities):
            raise ValueError("playbook priorities must be unique")
        family_id_set = set(family_ids)
        template_id_set = set(template_ids)
        variant_id_set = set(variant_ids)
        for variant in self.setup_variants:
            if variant.family_id not in family_id_set:
                raise ValueError(
                    f"unknown family for setup variant {variant.setup_variant_id}: {variant.family_id}"
                )
            if variant.execution_expression_id not in template_id_set:
                raise ValueError(
                    f"unknown execution expression for setup variant {variant.setup_variant_id}: "
                    f"{variant.execution_expression_id}"
                )
        variant_lookup = {variant.setup_variant_id: variant for variant in self.setup_variants}
        for playbook in self.playbooks:
            if playbook.execution_template_id not in template_id_set:
                raise ValueError(
                    f"unknown execution template for playbook {playbook.playbook_id}: "
                    f"{playbook.execution_template_id}"
                )
            if playbook.execution_expression_id not in template_id_set:
                raise ValueError(
                    f"unknown execution expression for playbook {playbook.playbook_id}: "
                    f"{playbook.execution_expression_id}"
                )
            if playbook.family_id not in family_id_set:
                raise ValueError(
                    f"unknown family for playbook {playbook.playbook_id}: {playbook.family_id}"
                )
            if playbook.setup_variant_id not in variant_id_set:
                raise ValueError(
                    f"unknown setup variant for playbook {playbook.playbook_id}: {playbook.setup_variant_id}"
                )
            variant = variant_lookup[playbook.setup_variant_id]
            if variant.family_id != playbook.family_id:
                raise ValueError(
                    f"playbook {playbook.playbook_id} family {playbook.family_id} does not match setup variant family {variant.family_id}"
                )
            if playbook.execution_expression_id != variant.execution_expression_id:
                raise ValueError(
                    f"playbook {playbook.playbook_id} execution expression must match setup variant {variant.setup_variant_id}"
                )
        return self

    def ordered_playbooks(self) -> list[PlaybookSpec]:
        """Return active playbooks in deterministic priority order."""

        return sorted(
            (playbook for playbook in self.playbooks if playbook.active),
            key=lambda item: item.priority,
        )

    def ordered_setup_variants(self) -> list[SetupVariantSpec]:
        """Return active setup variants in deterministic priority order."""

        return sorted(
            (variant for variant in self.setup_variants if variant.active),
            key=lambda item: item.priority,
        )

    def execution_template_index(self) -> dict[str, ExecutionTemplateSpec]:
        """Return deterministic template lookup by id."""

        return {template.template_id: template for template in self.execution_templates}

    def family_index(self) -> dict[str, PlaybookFamilySpec]:
        """Return deterministic family lookup by id."""

        return {family.family_id: family for family in self.families}

    def setup_variant_index(self) -> dict[str, SetupVariantSpec]:
        """Return deterministic setup-variant lookup by id."""

        return {variant.setup_variant_id: variant for variant in self.setup_variants}

    @classmethod
    def from_yaml_text(cls, text: str) -> PlaybookRegistryDocument:
        """Parse one checked-in YAML registry string."""

        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("playbook registry YAML must decode to a mapping")
        return cls.model_validate(loaded)

    @classmethod
    def from_yaml_path(cls, path: Path | str) -> PlaybookRegistryDocument:
        """Load one checked-in YAML registry file."""

        return cls.from_yaml_text(Path(path).read_text(encoding="utf-8"))

    def to_yaml_text(self) -> str:
        """Serialise the registry to deterministic YAML text."""

        return cast(
            str,
            yaml.safe_dump(self.model_dump(mode="json"), sort_keys=False, allow_unicode=False),
        )
