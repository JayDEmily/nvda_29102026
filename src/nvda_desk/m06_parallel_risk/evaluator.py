"""Deterministic, side-effect-free M06 K10 evaluator."""

from __future__ import annotations

from typing import Any

from nvda_desk.m06_parallel_risk.contracts import (
    CLOSED_AUTHORITY_CLASSES,
    ParallelRiskAssessment,
    ParallelRiskInput,
    ParallelRiskObservation,
    parallel_risk_assessment_fingerprint,
    parallel_risk_observation_fingerprint,
)


class ParallelRiskEvaluator:
    """Evaluate one revalidated Parallel Risk Input without hidden state."""

    def evaluate(self, risk_input: ParallelRiskInput) -> ParallelRiskAssessment:
        if not isinstance(risk_input, ParallelRiskInput):
            raise TypeError("typed_parallel_risk_input_required")
        governed = ParallelRiskInput.model_validate(risk_input.model_dump(mode="python"))
        source_references = tuple(
            f"{item.capture_id}:{item.input_fingerprint}" for item in governed.source_capture_refs
        )
        observations = tuple(
            sorted(
                (
                    self._concentration_observation(governed, source_references),
                    self._inventory_observation(governed, source_references),
                    self._liquidity_observation(governed, source_references),
                    self._options_observation(governed, source_references),
                    self._event_observation(governed, source_references),
                    self._volatility_observation(governed, source_references),
                ),
                key=lambda item: item.family,
            )
        )
        cautions = tuple(item.reason for item in observations if item.state == "caution")
        blocks = tuple(item.reason for item in observations if item.state == "block")
        unknown = tuple(item.family for item in observations if item.state == "unknown")
        limitations = tuple(
            sorted(
                set(governed.prepared_limitations)
                | set(governed.missing_optional_enrichments)
                | {item.limitation for item in observations if item.limitation}
            )
        )
        state = (
            "block" if blocks else "caution" if cautions else "unknown" if unknown else "observe"
        )
        payload: dict[str, Any] = {
            "assessment_id": "pending",
            "input_id": governed.input_id,
            "input_fingerprint": governed.input_fingerprint,
            "prepared_id": governed.prepared_id,
            "prepared_fingerprint": governed.prepared_fingerprint,
            "evaluator_version": governed.evaluator_version,
            "evaluator_policy_version": governed.evaluator_policy_version,
            "aggregation_version": governed.aggregation_version,
            "state": state,
            "observations": observations,
            "caution_flags": cautions,
            "hard_blocks": blocks,
            "unknown_families": unknown,
            "prepared_limitations": governed.prepared_limitations,
            "missing_optional_enrichments": governed.missing_optional_enrichments,
            "limitations": limitations,
            "semantic_fingerprint": "0" * 64,
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "foreign_authority_claimed": False,
        }
        provisional = ParallelRiskAssessment.model_construct(**payload)
        fp = parallel_risk_assessment_fingerprint(provisional)
        payload["semantic_fingerprint"] = fp
        payload["assessment_id"] = f"parallel-risk-assessment:{fp[:24]}"
        return ParallelRiskAssessment.model_validate(payload)

    @staticmethod
    def _build_observation(**payload: Any) -> ParallelRiskObservation:
        payload["observation_id"] = "pending"
        payload["semantic_fingerprint"] = "0" * 64
        provisional = ParallelRiskObservation.model_construct(**payload)
        fp = parallel_risk_observation_fingerprint(provisional)
        payload["semantic_fingerprint"] = fp
        payload["observation_id"] = f"parallel-risk-observation:{fp[:24]}"
        return ParallelRiskObservation.model_validate(payload)

    def _unavailable_observation(
        self,
        family: str,
        reason: str,
        source_field: str,
        source_references: tuple[str, ...],
    ) -> ParallelRiskObservation:
        return self._build_observation(
            family=family,
            state="unknown",
            reason=reason,
            source_fields=(source_field,),
            source_references=source_references,
            limitation=reason,
        )

    def _owner_fact_unavailable(
        self,
        *,
        family: str,
        source_field: str,
        base_reason: str,
        fact: Any,
        effective_at_utc: Any,
        source_references: tuple[str, ...],
    ) -> ParallelRiskObservation | None:
        if fact is None:
            return self._unavailable_observation(
                family, base_reason, source_field, source_references
            )
        if effective_at_utc < fact.as_of_utc:
            reason = f"{family}_owner_fact_not_yet_effective"
        elif effective_at_utc > fact.valid_until_utc:
            reason = f"{family}_owner_fact_stale"
        else:
            return None
        return self._build_observation(
            family=family,
            state="unknown",
            reason=reason,
            source_fields=(source_field,),
            source_references=tuple(
                sorted(set(source_references) | set(fact.authority_references))
            ),
            limitation=reason,
        )

    def _concentration_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        fact = None if risk_input.owner_facts is None else risk_input.owner_facts.concentration
        unavailable = self._owner_fact_unavailable(
            family="concentration",
            source_field="owner_facts.concentration",
            base_reason="concentration_context_unavailable",
            fact=fact,
            effective_at_utc=risk_input.effective_at_utc,
            source_references=source_references,
        )
        if unavailable is not None:
            return unavailable
        assert fact is not None
        reasons = {
            "observe": "concentration_within_owner_limit",
            "caution": "concentration_near_owner_limit",
            "block": "concentration_owner_limit_breached",
        }
        return self._build_observation(
            family="concentration",
            state=fact.condition,
            reason=reasons[fact.condition],
            source_fields=(
                "owner_facts.concentration.concentration_ratio",
                "owner_facts.concentration.warning_ratio",
                "owner_facts.concentration.block_ratio",
            ),
            source_references=tuple(
                sorted(set(source_references) | set(fact.authority_references))
            ),
            limitation=None,
        )

    def _inventory_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        fact = None if risk_input.owner_facts is None else risk_input.owner_facts.inventory_stress
        unavailable = self._owner_fact_unavailable(
            family="inventory_stress",
            source_field="owner_facts.inventory_stress",
            base_reason="inventory_stress_context_unavailable",
            fact=fact,
            effective_at_utc=risk_input.effective_at_utc,
            source_references=source_references,
        )
        if unavailable is not None:
            return unavailable
        assert fact is not None
        reasons = {
            "observe": "inventory_coverage_sufficient",
            "caution": "inventory_coverage_thin",
            "block": "inventory_coverage_insufficient",
        }
        return self._build_observation(
            family="inventory_stress",
            state=fact.condition,
            reason=reasons[fact.condition],
            source_fields=(
                "owner_facts.inventory_stress.coverage_ratio",
                "owner_facts.inventory_stress.warning_coverage_ratio",
                "owner_facts.inventory_stress.block_coverage_ratio",
            ),
            source_references=tuple(
                sorted(set(source_references) | set(fact.authority_references))
            ),
            limitation=None,
        )

    def _liquidity_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        fact = None if risk_input.owner_facts is None else risk_input.owner_facts.liquidity
        unavailable = self._owner_fact_unavailable(
            family="liquidity",
            source_field="owner_facts.liquidity",
            base_reason="liquidity_context_unavailable",
            fact=fact,
            effective_at_utc=risk_input.effective_at_utc,
            source_references=source_references,
        )
        if unavailable is not None:
            return unavailable
        assert fact is not None
        reasons = {
            "observe": "liquidity_coverage_sufficient",
            "caution": "liquidity_coverage_thin",
            "block": "liquidity_coverage_insufficient",
        }
        return self._build_observation(
            family="liquidity",
            state=fact.condition,
            reason=reasons[fact.condition],
            source_fields=(
                "owner_facts.liquidity.coverage_ratio",
                "owner_facts.liquidity.warning_coverage_ratio",
                "owner_facts.liquidity.block_coverage_ratio",
            ),
            source_references=tuple(
                sorted(set(source_references) | set(fact.authority_references))
            ),
            limitation=None,
        )

    def _event_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        tags = {tag for window in risk_input.windows for tag in window.tags}
        active = "scheduled_event_window_active" in tags
        return self._build_observation(
            family="scheduled_event",
            state="caution" if active else "observe",
            reason=(
                "scheduled_event_window_active" if active else "no_active_scheduled_event_window"
            ),
            source_fields=("windows",),
            source_references=source_references,
            limitation=None,
        )

    def _options_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        if risk_input.front_dte is None or risk_input.next_dte is None:
            return self._build_observation(
                family="options_term_structure",
                state="unknown",
                reason="options_dte_missing",
                source_fields=("front_dte", "next_dte"),
                source_references=source_references,
                limitation="options_term_structure_unavailable",
            )
        inverted = risk_input.front_dte > risk_input.next_dte
        return self._build_observation(
            family="options_term_structure",
            state="caution" if inverted else "observe",
            reason=(
                "front_term_structure_backwardation"
                if inverted
                else "front_term_structure_not_inverted"
            ),
            source_fields=("front_dte", "next_dte"),
            source_references=source_references,
            limitation=None,
        )

    def _volatility_observation(
        self, risk_input: ParallelRiskInput, source_references: tuple[str, ...]
    ) -> ParallelRiskObservation:
        if risk_input.vix_level is None:
            return self._build_observation(
                family="volatility",
                state="unknown",
                reason="vix_level_missing",
                source_fields=("vix_level",),
                source_references=source_references,
                limitation="volatility_context_unavailable",
            )
        state = (
            "block"
            if risk_input.vix_level >= risk_input.vix_block_threshold
            else (
                "caution" if risk_input.vix_level >= risk_input.vix_caution_threshold else "observe"
            )
        )
        return self._build_observation(
            family="volatility",
            state=state,
            reason=(
                "vix_block_threshold_reached"
                if state == "block"
                else (
                    "vix_caution_threshold_reached"
                    if state == "caution"
                    else "vix_below_caution_threshold"
                )
            ),
            source_fields=("vix_level",),
            source_references=tuple(
                sorted(set(source_references) | set(risk_input.threshold_authority_refs))
            ),
            limitation=None,
        )


__all__ = ["ParallelRiskEvaluator"]
