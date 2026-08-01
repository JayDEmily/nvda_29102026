"""Narrow M05 adapter for temporal-domain signal-informed phase authority."""

from __future__ import annotations

from typing import Any

from nvda_desk.domain.temporal.intraday_phase import (
    IntradayPhaseEvidence,
    IntradayPhaseEvaluator,
    IntradayPhaseRepository,
    IntradayPhaseResult,
)

from .contracts import CarrierFact, StageContext, StageInput, semantic_fingerprint


class TemporalStageAdapter:
    """Evaluate temporal authority, retain its state, and build one M05 carrier."""

    def __init__(
        self,
        *,
        evaluator: IntradayPhaseEvaluator,
        repository: IntradayPhaseRepository,
    ) -> None:
        self._evaluator = evaluator
        self._repository = repository

    def evaluate(
        self,
        *,
        evidence: IntradayPhaseEvidence,
        context: StageContext,
    ) -> tuple[IntradayPhaseResult, StageInput]:
        prior = self._repository.load(evidence.session_reference_id)
        result = self._evaluator.evaluate(evidence=evidence, prior_state=prior)
        next_state = result.to_state()
        if next_state is not None:
            self._repository.save(next_state)
        return result, self._build_stage_input(result=result, context=context)

    @staticmethod
    def _fact(
        *,
        fact_id: str,
        value: Any,
        contract_version: str,
    ) -> CarrierFact:
        material = {
            "fact_id": fact_id,
            "owner_id": "temporal_domain",
            "contract_version": contract_version,
            "value": value,
        }
        return CarrierFact(
            semantic_fingerprint=semantic_fingerprint(material),
            **material,
        )

    def _build_stage_input(
        self,
        *,
        result: IntradayPhaseResult,
        context: StageContext,
    ) -> StageInput:
        facts = tuple(
            self._fact(
                fact_id=fact_id,
                value=value,
                contract_version=result.contract_version,
            )
            for fact_id, value in (
                ("intraday_phase", result.phase.value),
                ("intraday_phase_authority_state", result.authority_state),
                ("intraday_phase_result_id", result.result_id),
                ("intraday_phase_fingerprint", result.semantic_fingerprint),
                ("intraday_phase_policy_version", result.policy_version),
                ("intraday_phase_state_version", result.state_version),
                ("intraday_phase_positive_permission", result.positive_permission),
            )
        )
        carrier_id = f"carrier.temporal.{result.semantic_fingerprint[:16]}"
        missing_state = None if result.positive_permission else result.authority_state
        material = {
            "stage": "temporal",
            "context_id": context.context_id,
            "context_fingerprint": context.semantic_fingerprint,
            "contract_version": "m05-stage-input.1.0.0",
            "carrier_stage": "temporal",
            "carrier_id": carrier_id,
            "carrier_contract_version": "temporal-stage-carrier.1.0.0",
            "carrier_schema_version": "temporal-stage-carrier.schema.1.0.0",
            "carrier_facts": facts,
            "authority_refs": (
                (
                    "temporal_domain",
                    result.result_id,
                    result.contract_version,
                    result.semantic_fingerprint,
                ),
            ),
            "missing_state": missing_state,
        }
        return StageInput(
            carrier_fingerprint=semantic_fingerprint(material),
            **material,
        )
