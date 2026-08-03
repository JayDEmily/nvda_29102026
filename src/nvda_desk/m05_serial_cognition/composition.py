"""Canonical M03→M05 cognition composition from exact owner authority."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any, Final

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from nvda_desk.cognition.serial.posture import evaluate_posture
from nvda_desk.contracts.eligibility import (
    EligibilityAdmissibilitySurface,
    PlaybookEligibilityOutput,
)
from nvda_desk.contracts.execution import ExecutionExpressionInput
from nvda_desk.contracts.options_flow import OptionsFlowContextInput
from nvda_desk.contracts.posture import PermissionState
from nvda_desk.contracts.regime import MarketRegimeContextInput
from nvda_desk.contracts.temporal import TemporalContextInput, TemporalEventWindow
from nvda_desk.domain.execution.candidate_expression import evaluate_execution_expression
from nvda_desk.m03_preparation import PreparedDataEnvelope
from nvda_desk.m07_coefficient_modifier_authority import (
    ModifierApplicationReceipt,
    ModifierDecision,
    PolicyBundle,
    build_k12_receipt,
    resolve_k12,
)
from nvda_desk.m07_coefficient_modifier_authority.contracts import InputStateFacts
from nvda_desk.m08_playbook_catalogue import (
    EligibilityDecision,
    EligibilityResolver,
    PlaybookCatalogue,
)
from nvda_desk.m08_playbook_catalogue.contracts import (
    EligibilityContext,
    FactAuthority,
    PosturePermission,
)
from nvda_desk.services.options_flow_context_service import OptionsFlowContextService
from nvda_desk.services.regime_context_service import RegimeContextService
from nvda_desk.services.temporal_context_service import TemporalContextService

from .contracts import (
    CLOSED_AUTHORITY_CLASSES,
    SERIAL_STAGE_DEPENDENCIES,
    SERIAL_STAGE_ORDER,
    CarrierFact,
    SerialCandidate,
    StageContext,
    StageInput,
    StageOutput,
    semantic_fingerprint,
)
from .runner import SerialRunner

AuthorityRef = tuple[str, str, str, str]
Pair = tuple[str, str]

DEFAULT_MAPPING_POLICY_VERSIONS: Final[tuple[Pair, ...]] = tuple(
    (stage, f"m05.mapping.{stage}.1.0.0") for stage in SERIAL_STAGE_ORDER
)
_REQUIRED_M07_COEFFICIENTS: Final[frozenset[str]] = frozenset(
    {
        "risk_vix_caution_threshold",
        "risk_vix_hot_threshold",
        "max_risk_per_trade",
        "hedge_required",
    }
)
_SUPPORTED_M07_FACTS: Final[frozenset[str]] = frozenset(
    {
        "regime_high_volatility",
        "regime_divergent",
        "regime_normal",
        "regime_unknown",
        "vix_present",
    }
)


class SerialCognitionRequest(BaseModel):
    """Exact M03, M07 and M08 authority required for one canonical serial run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    prepared_data: PreparedDataEnvelope
    modifier_bundle: PolicyBundle
    playbook_catalogue: PlaybookCatalogue
    context_contract_version: str = "1.0.0"
    serial_order_version: str = "serial-order.1.0.0"
    runner_version: str = "serial-runner.1.0.0"
    mapping_policy_versions: tuple[Pair, ...] = DEFAULT_MAPPING_POLICY_VERSIONS
    modifier_receipt_id: str = Field(min_length=1)
    modifier_application_id: str = Field(min_length=1)
    modifier_receipt_emitted_at_utc: datetime
    eligibility_decision_id: str = Field(min_length=1)
    eligibility_context_version: str = "1.0.0"
    posture_version: str = "1.0.0"
    expression_policy_version: str = "candidate-expression.1.0.0"

    @field_validator("modifier_receipt_emitted_at_utc")
    @classmethod
    def _receipt_time_is_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
            raise ValueError("modifier_receipt_emission_time_must_be_utc")
        return value

    @model_validator(mode="after")
    def _validate_authority(self) -> "SerialCognitionRequest":
        if self.modifier_bundle.owner_stage != "posture":
            raise ValueError("m07_bundle_owner_stage_must_be_posture")
        if tuple(name for name, _ in self.mapping_policy_versions) != SERIAL_STAGE_ORDER:
            raise ValueError("mapping_policy_versions_must_cover_exact_stage_order")
        if len({name for name, _ in self.mapping_policy_versions}) != len(SERIAL_STAGE_ORDER):
            raise ValueError("mapping_policy_versions_must_be_unique")
        observed_coefficients = {item.coefficient_id for item in self.modifier_bundle.coefficients}
        missing_coefficients = _REQUIRED_M07_COEFFICIENTS.difference(observed_coefficients)
        if missing_coefficients:
            raise ValueError(f"m07_required_coefficient_missing:{sorted(missing_coefficients)[0]}")
        unsupported = {
            fact_ref
            for modifier in self.modifier_bundle.modifiers
            for fact_ref in modifier.applicability_fact_refs
            if fact_ref not in _SUPPORTED_M07_FACTS
        }
        if unsupported:
            raise ValueError(f"unsupported_m07_applicability_fact:{sorted(unsupported)[0]}")
        if self.modifier_receipt_emitted_at_utc < self.prepared_data.effective_at_utc:
            raise ValueError("modifier_receipt_precedes_prepared_authority")
        return self


class SerialCognitionOutcome(BaseModel):
    """Exact M05 result plus concrete M07/M08 owner products used to form it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate: SerialCandidate
    stage_inputs: tuple[StageInput, ...]
    modifier_decision: ModifierDecision
    modifier_receipt: ModifierApplicationReceipt | None
    eligibility_decision: EligibilityDecision | None

    @model_validator(mode="after")
    def _validate_owner_binding(self) -> "SerialCognitionOutcome":
        if tuple(item.stage for item in self.stage_inputs) != SERIAL_STAGE_ORDER:
            raise ValueError("serial_cognition_outcome_stage_inputs_invalid")
        by_stage = {item.stage: item for item in self.stage_inputs}
        for output in self.candidate.stage_outputs:
            stage_input = by_stage[output.stage]
            if (
                output.input_carrier_id,
                output.input_carrier_fingerprint,
            ) != (stage_input.carrier_id, stage_input.carrier_fingerprint):
                raise ValueError("serial_cognition_outcome_input_output_lineage_mismatch")
        if self.modifier_decision.semantic_fingerprint is not None:
            decision_ref = (
                "m07",
                self.modifier_decision.decision_id,
                self.modifier_decision.schema_version or "1.0.0",
                self.modifier_decision.semantic_fingerprint,
            )
            if decision_ref not in self.candidate.m07_authority_refs:
                raise ValueError("candidate_missing_exact_m07_decision")
        if self.modifier_receipt is not None:
            receipt_ref = (
                "m07",
                self.modifier_receipt.receipt_id,
                self.modifier_receipt.schema_version,
                semantic_fingerprint(self.modifier_receipt.model_dump(mode="python")),
            )
            if receipt_ref not in self.candidate.m07_authority_refs:
                raise ValueError("candidate_missing_exact_m07_receipt")
        if (
            self.eligibility_decision is not None
            and self.eligibility_decision.semantic_fingerprint is not None
        ):
            eligibility_ref = (
                "m08",
                self.eligibility_decision.decision_id,
                self.eligibility_decision.decision_schema_version,
                self.eligibility_decision.semantic_fingerprint,
            )
            if eligibility_ref not in self.candidate.m08_authority_refs:
                raise ValueError("candidate_missing_exact_m08_decision")
        if self.candidate.status == "formed":
            if self.modifier_receipt is None:
                raise ValueError("formed_candidate_missing_m07_receipt")
            if self.eligibility_decision is None or self.eligibility_decision.status != "eligible":
                raise ValueError("formed_candidate_missing_eligible_m08_decision")
        return self


class SerialCognitionService:
    """Compose actual bounded stage owners behind the canonical M05 contracts."""

    def __init__(
        self,
        *,
        temporal_service: TemporalContextService | None = None,
        regime_service: RegimeContextService | None = None,
        options_flow_service: OptionsFlowContextService | None = None,
        eligibility_resolver: EligibilityResolver | None = None,
    ) -> None:
        self._temporal = temporal_service or TemporalContextService()
        self._regime = regime_service or RegimeContextService()
        self._options_flow = options_flow_service or OptionsFlowContextService()
        self._eligibility = eligibility_resolver or EligibilityResolver()

    def run(self, request: SerialCognitionRequest) -> SerialCognitionOutcome:
        """Return one serial result and the exact M07/M08 products that formed it."""

        governed = self._request(request)
        prepared = governed.prepared_data
        context = self._context(governed)

        temporal_input = self._temporal_input(context, prepared)
        regime_input = self._regime_input(context, prepared)
        options_input = self._options_input(context, prepared)

        temporal_result = self._temporal.evaluate(temporal_input)
        regime_result = self._regime.evaluate(regime_input)
        options_result = self._options_flow.evaluate(options_input)

        m03_ref = (
            "m03",
            prepared.prepared_id,
            prepared.schema_version,
            prepared.prepared_fingerprint,
        )
        temporal_stage_input = self._stage_input(
            context,
            stage="temporal",
            authority_refs=(m03_ref,),
            facts={
                "effective_at_utc": prepared.effective_at_utc,
                "source_time_utc": prepared.payload.source_time_utc,
                "runtime_bar_time_utc": prepared.payload.runtime_bar_time_utc,
                "next_event_time_utc": prepared.payload.next_event_time_utc,
            },
            owner_id="m03",
            owner_version=prepared.schema_version,
        )
        regime_stage_input = self._stage_input(
            context,
            stage="regime",
            authority_refs=(m03_ref,),
            facts={
                "nvda_return_pct": prepared.payload.nvda_return_pct,
                "nq_return_pct": prepared.payload.nq_return_pct,
                "vix_level": prepared.payload.vix_level,
            },
            owner_id="m03",
            owner_version=prepared.schema_version,
        )
        options_stage_input = self._stage_input(
            context,
            stage="options_flow",
            authority_refs=(m03_ref,),
            facts={
                "spot_price": prepared.payload.spot_price,
                "front_dte": prepared.payload.front_dte,
                "next_dte": prepared.payload.next_dte,
            },
            owner_id="m03",
            owner_version=prepared.schema_version,
        )

        outputs: dict[str, StageOutput] = {}
        outputs["temporal"] = self._stage_output(
            context,
            temporal_stage_input,
            dependencies=(),
            status="complete",
            result_refs=self._pairs(
                temporal_policy_version=temporal_result.temporal_policy_version,
                session_state=temporal_result.session_state,
                next_event_time_utc=(
                    temporal_result.next_event_time_utc.isoformat()
                    if temporal_result.next_event_time_utc is not None
                    else "unavailable"
                ),
            ),
            reasons=tuple(temporal_result.active_tags),
        )
        outputs["regime"] = self._stage_output(
            context,
            regime_stage_input,
            dependencies=(),
            status="complete",
            result_refs=self._pairs(
                regime_policy_version=regime_result.regime_policy_version,
                volatility_regime=regime_result.volatility_regime,
                cross_asset_pressure_score=str(regime_result.cross_asset_pressure_score),
                vix_level=(
                    str(regime_result.vix_level)
                    if regime_result.vix_level is not None
                    else "unavailable"
                ),
            ),
            reasons=tuple(regime_result.reasons),
        )
        outputs["options_flow"] = self._stage_output(
            context,
            options_stage_input,
            dependencies=(),
            status="complete",
            result_refs=self._pairs(
                term_structure_state=options_result.term_structure_state,
                skew_state=options_result.skew_state,
                gamma_state=options_result.gamma_state,
            ),
            reasons=tuple(options_result.reasons),
        )

        m07_facts = self._m07_facts(context, regime_result)
        modifier_decision = resolve_k12(
            bundle=governed.modifier_bundle,
            owner_stage="posture",
            input_state=m07_facts,
        )
        modifier_receipt = build_k12_receipt(
            decision=modifier_decision,
            receipt_id=governed.modifier_receipt_id,
            application_id=governed.modifier_application_id,
            emitted_at_utc=governed.modifier_receipt_emitted_at_utc,
        )
        posture_refs = self._m07_refs(governed.modifier_bundle, modifier_decision, modifier_receipt)
        posture_input = self._stage_input(
            context,
            stage="posture",
            authority_refs=posture_refs,
            facts={
                "modifier_decision_status": modifier_decision.status,
                "posture_policy_ref": governed.modifier_bundle.resolution_law_version,
            },
            owner_id="m07",
            owner_version=governed.modifier_bundle.schema_version,
        )
        if modifier_decision.status == "rejected" or modifier_receipt is None:
            outputs["posture"] = self._stage_output(
                context,
                posture_input,
                dependencies=(outputs["regime"],),
                status="rejected",
                result_refs=(),
                reasons=modifier_decision.rejection_reasons or ("m07_modifier_decision_rejected",),
            )
            candidate, stage_inputs = self._run_terminal(
                governed,
                context,
                outputs,
                (
                    temporal_stage_input,
                    regime_stage_input,
                    options_stage_input,
                    posture_input,
                ),
                terminal_stage="posture",
            )
            return SerialCognitionOutcome(
                candidate=candidate,
                stage_inputs=stage_inputs,
                modifier_decision=modifier_decision,
                modifier_receipt=None,
                eligibility_decision=None,
            )

        posture_result = evaluate_posture(
            regime=regime_result,
            coefficient_values=self._validated_coefficient_values(modifier_decision),
        )
        posture_status = (
            "blocked" if posture_result.permission_state is PermissionState.BLOCK else "permitted"
        )
        posture_stage_status = "stand_down" if posture_status == "blocked" else "complete"
        outputs["posture"] = self._stage_output(
            context,
            posture_input,
            dependencies=(outputs["regime"],),
            status=posture_stage_status,
            result_refs=(
                self._pairs(posture_status=posture_status)
                if posture_stage_status == "complete"
                else ()
            ),
            reasons=tuple(posture_result.reasons),
        )
        if posture_stage_status == "stand_down":
            candidate, stage_inputs = self._run_terminal(
                governed,
                context,
                outputs,
                (
                    temporal_stage_input,
                    regime_stage_input,
                    options_stage_input,
                    posture_input,
                ),
                terminal_stage="posture",
            )
            return SerialCognitionOutcome(
                candidate=candidate,
                stage_inputs=stage_inputs,
                modifier_decision=modifier_decision,
                modifier_receipt=modifier_receipt,
                eligibility_decision=None,
            )

        posture_permission = self._posture_permission(
            governed,
            context,
            modifier_decision,
            modifier_receipt,
            posture_status,
        )
        eligibility_context = self._eligibility_context(
            governed,
            context,
            prepared,
            temporal_result,
            regime_result,
            options_result,
            posture_permission,
        )
        eligibility_decision = self._eligibility.resolve(
            governed.playbook_catalogue,
            posture_permission,
            eligibility_context,
            decision_id=governed.eligibility_decision_id,
        )
        eligibility_refs = self._m08_refs(governed.playbook_catalogue, eligibility_decision)
        eligibility_input = self._stage_input(
            context,
            stage="eligibility",
            authority_refs=eligibility_refs,
            facts=self._eligibility_carrier_facts(eligibility_decision),
            owner_id="m08",
            owner_version=governed.playbook_catalogue.schema_version,
        )
        eligibility_status, stage_status, reasons = self._eligibility_status(eligibility_decision)
        eligibility_result_refs = self._eligibility_result_refs(eligibility_decision)
        outputs["eligibility"] = self._stage_output(
            context,
            eligibility_input,
            dependencies=(outputs["posture"],),
            status=stage_status,
            result_refs=eligibility_result_refs if stage_status == "complete" else (),
            reasons=reasons,
        )
        if stage_status != "complete":
            candidate, stage_inputs = self._run_terminal(
                governed,
                context,
                outputs,
                (
                    temporal_stage_input,
                    regime_stage_input,
                    options_stage_input,
                    posture_input,
                    eligibility_input,
                ),
                terminal_stage="eligibility",
            )
            return SerialCognitionOutcome(
                candidate=candidate,
                stage_inputs=stage_inputs,
                modifier_decision=modifier_decision,
                modifier_receipt=modifier_receipt,
                eligibility_decision=eligibility_decision,
            )
        if eligibility_status != "eligible" or eligibility_decision.eligibility_lead is None:
            raise ValueError("eligible_stage_output_missing_exact_m08_lead")

        execution_input = self._stage_input(
            context,
            stage="execution",
            authority_refs=tuple(
                ref
                for ref in eligibility_refs
                if ref[1] != governed.playbook_catalogue.catalogue_id
            ),
            facts={
                "eligibility_lead_id": eligibility_decision.eligibility_lead.playbook_id,
                "expression_policy_ref": governed.expression_policy_version,
            },
            owner_id="m08",
            owner_version=eligibility_decision.decision_schema_version,
        )
        expression_refs = self._execution_result_refs(
            governed,
            context,
            temporal_result,
            regime_result,
            options_result,
            posture_result,
            eligibility_decision,
        )
        outputs["execution"] = self._stage_output(
            context,
            execution_input,
            dependencies=tuple(outputs[name] for name in SERIAL_STAGE_DEPENDENCIES["execution"]),
            status="complete",
            result_refs=expression_refs,
            reasons=(),
        )
        inputs = (
            temporal_stage_input,
            regime_stage_input,
            options_stage_input,
            posture_input,
            eligibility_input,
            execution_input,
        )
        return SerialCognitionOutcome(
            candidate=self._runner(governed, outputs).run(
                context=context,
                stage_inputs=inputs,
            ),
            stage_inputs=inputs,
            modifier_decision=modifier_decision,
            modifier_receipt=modifier_receipt,
            eligibility_decision=eligibility_decision,
        )

    @staticmethod
    def _request(value: SerialCognitionRequest) -> SerialCognitionRequest:
        if not isinstance(value, SerialCognitionRequest):
            raise TypeError("typed_serial_cognition_request_required")
        return SerialCognitionRequest.model_validate(value.model_dump(mode="python"))

    @staticmethod
    def _context(request: SerialCognitionRequest) -> StageContext:
        prepared = request.prepared_data
        source_refs = tuple(
            sorted(
                (item.source_artifact_id, item.capture_id) for item in prepared.source_capture_refs
            )
        )
        identity_material = {
            "prepared_id": prepared.prepared_id,
            "prepared_fingerprint": prepared.prepared_fingerprint,
            "modifier_bundle": (
                request.modifier_bundle.bundle_id,
                request.modifier_bundle.bundle_version,
                semantic_fingerprint(request.modifier_bundle.model_dump(mode="python")),
            ),
            "playbook_catalogue": (
                request.playbook_catalogue.catalogue_id,
                request.playbook_catalogue.catalogue_version,
                request.playbook_catalogue.catalogue_fingerprint,
            ),
            "serial_order_version": request.serial_order_version,
            "runner_version": request.runner_version,
            "mapping_policy_versions": request.mapping_policy_versions,
        }
        context_id = f"context.m05.{semantic_fingerprint(identity_material)[:16]}"
        payload: dict[str, Any] = {
            "context_id": context_id,
            "contract_version": request.context_contract_version,
            "prepared_id": prepared.prepared_id,
            "prepared_schema_version": prepared.schema_version,
            "prepared_fingerprint": prepared.prepared_fingerprint,
            "prepared_input_fingerprint": prepared.input_fingerprint,
            "source_capture_refs": source_refs,
            "preparation_policy_version": prepared.preparation_policy_version,
            "alignment_policy_version": prepared.alignment_policy_version,
            "fingerprint_policy_version": prepared.fingerprint_policy_version,
            "canonicalisation_version": prepared.canonicalisation_version,
            "derivation_versions": prepared.derivation_versions,
            "effective_at_utc": prepared.effective_at_utc,
            "prepared_validation_state": prepared.validation_state,
            "prepared_completeness_state": prepared.completeness_state,
            "serial_order_version": request.serial_order_version,
            "runner_version": request.runner_version,
            "mapping_policy_versions": request.mapping_policy_versions,
            "limitations": prepared.limitations,
            "unavailable_owner_facts": prepared.missing_optional_enrichments,
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "foreign_authority_claimed": False,
            "semantic_fingerprint": "",
        }
        material = dict(payload)
        material.pop("semantic_fingerprint")
        payload["semantic_fingerprint"] = semantic_fingerprint(material)
        return StageContext.model_validate(payload)

    @staticmethod
    def _temporal_input(
        context: StageContext, prepared: PreparedDataEnvelope
    ) -> TemporalContextInput:
        payload = prepared.payload
        source_time = payload.source_time_utc or payload.runtime_bar_time_utc
        if source_time is None:
            raise ValueError("m03_temporal_authority_missing")
        return TemporalContextInput(
            common_context_ref=context.context_id,
            source_time_utc=source_time,
            source_date=payload.source_date,
            next_event_time_utc=payload.next_event_time_utc,
            windows=[
                TemporalEventWindow(
                    event_id=item.event_id,
                    window_start_utc=item.window_start_utc,
                    window_end_utc=item.window_end_utc,
                    tags=list(item.tags),
                )
                for item in payload.windows
            ],
        )

    @staticmethod
    def _regime_input(
        context: StageContext, prepared: PreparedDataEnvelope
    ) -> MarketRegimeContextInput:
        payload = prepared.payload
        values = {
            "nvda_return_pct": payload.nvda_return_pct,
            "nq_return_pct": payload.nq_return_pct,
            "vix_level": payload.vix_level,
        }
        return MarketRegimeContextInput(
            common_context_ref=context.context_id,
            **values,
            missing_fields=[name for name, value in values.items() if value is None],
        )

    @staticmethod
    def _options_input(
        context: StageContext, prepared: PreparedDataEnvelope
    ) -> OptionsFlowContextInput:
        payload = prepared.payload
        values = {
            "spot_price": payload.spot_price,
            "front_dte": payload.front_dte,
            "next_dte": payload.next_dte,
        }
        return OptionsFlowContextInput(
            common_context_ref=context.context_id,
            options_evidence_ref=f"prepared:{prepared.prepared_id}",
            **values,
            missing_fields=[name for name, value in values.items() if value is None],
        )

    @staticmethod
    def _fact(
        *,
        fact_id: str,
        owner_id: str,
        contract_version: str,
        value: Any,
    ) -> CarrierFact:
        material = {
            "fact_id": fact_id,
            "owner_id": owner_id,
            "contract_version": contract_version,
            "value": value,
        }
        return CarrierFact(**material, semantic_fingerprint=semantic_fingerprint(material))

    @classmethod
    def _stage_input(
        cls,
        context: StageContext,
        *,
        stage: str,
        authority_refs: tuple[AuthorityRef, ...],
        facts: Mapping[str, Any],
        owner_id: str,
        owner_version: str,
        missing_state: str | None = None,
    ) -> StageInput:
        carrier_facts = tuple(
            cls._fact(
                fact_id=fact_id,
                owner_id=owner_id,
                contract_version=owner_version,
                value=value,
            )
            for fact_id, value in facts.items()
        )
        material: dict[str, Any] = {
            "stage": stage,
            "context_id": context.context_id,
            "context_fingerprint": context.semantic_fingerprint,
            "contract_version": "1.0.0",
            "carrier_stage": stage,
            "carrier_id": f"carrier.{stage}.{semantic_fingerprint((context.context_id, stage, carrier_facts, authority_refs))[:16]}",
            "carrier_contract_version": f"m05.{stage}.carrier.1.0.0",
            "carrier_schema_version": "1.0.0",
            "carrier_facts": carrier_facts,
            "authority_refs": authority_refs,
            "missing_state": missing_state,
        }
        material["carrier_fingerprint"] = semantic_fingerprint(material)
        return StageInput.model_validate(material)

    @staticmethod
    def _stage_output(
        context: StageContext,
        stage_input: StageInput,
        *,
        dependencies: tuple[StageOutput, ...],
        status: str,
        result_refs: tuple[Pair, ...],
        reasons: tuple[str, ...],
    ) -> StageOutput:
        material: dict[str, Any] = {
            "stage": stage_input.stage,
            "owner_id": {
                "temporal": "temporal_context",
                "regime": "market_regime_context",
                "options_flow": "options_flow",
                "posture": "posture_permission",
                "eligibility": "playbook_eligibility",
                "execution": "candidate_expression",
            }[stage_input.stage],
            "contract_version": "1.0.0",
            "schema_version": "1.0.0",
            "context_id": context.context_id,
            "context_fingerprint": context.semantic_fingerprint,
            "input_carrier_id": stage_input.carrier_id,
            "input_carrier_fingerprint": stage_input.carrier_fingerprint,
            "dependency_output_ids": tuple(item.output_id for item in dependencies),
            "dependency_fingerprints": tuple(item.semantic_fingerprint for item in dependencies),
            "status": status,
            "result_refs": result_refs,
            "reasons": reasons,
            "consumed_authority_refs": stage_input.authority_refs,
            "packet_refs": (),
            "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
            "foreign_authority_claimed": False,
        }
        fingerprint = semantic_fingerprint(material)
        return StageOutput.model_validate(
            {
                "output_id": f"stage.{stage_input.stage}.{fingerprint[:16]}",
                **material,
                "semantic_fingerprint": fingerprint,
            }
        )

    @staticmethod
    def _pairs(**values: str) -> tuple[Pair, ...]:
        return tuple((key, value) for key, value in values.items())

    @staticmethod
    def _m07_facts(context: StageContext, regime: Any) -> InputStateFacts:
        facts = {
            "regime_high_volatility": regime.volatility_regime == "high_volatility",
            "regime_divergent": regime.volatility_regime == "divergent",
            "regime_normal": regime.volatility_regime == "normal",
            "regime_unknown": regime.volatility_regime == "unknown",
            "vix_present": regime.vix_level is not None,
        }
        material = {
            "context_id": f"m07-input:{context.context_id}",
            "context_version": "1.0.0",
            "effective_at_utc": context.effective_at_utc,
            "facts": facts,
        }
        return InputStateFacts(**material, fingerprint=semantic_fingerprint(material))

    @staticmethod
    def _m07_refs(
        bundle: PolicyBundle,
        decision: ModifierDecision,
        receipt: ModifierApplicationReceipt | None,
    ) -> tuple[AuthorityRef, ...]:
        bundle_ref = (
            "m07",
            bundle.bundle_id,
            bundle.bundle_version,
            semantic_fingerprint(bundle.model_dump(mode="python")),
        )
        if decision.semantic_fingerprint is None:
            return (bundle_ref,)
        refs: list[AuthorityRef] = [
            bundle_ref,
            (
                "m07",
                decision.decision_id,
                decision.schema_version or "1.0.0",
                decision.semantic_fingerprint,
            ),
        ]
        if receipt is not None:
            refs.append(
                (
                    "m07",
                    receipt.receipt_id,
                    receipt.schema_version,
                    semantic_fingerprint(receipt.model_dump(mode="python")),
                )
            )
        return tuple(refs)

    @staticmethod
    def _validated_coefficient_values(
        decision: ModifierDecision,
    ) -> dict[str, float | bool]:
        values: dict[str, float | bool] = {}
        for item in decision.coefficient_results:
            if item.coefficient_id == "hedge_required":
                values[item.coefficient_id] = bool(item.effective_value)
            else:
                values[item.coefficient_id] = float(item.effective_value)
        missing = _REQUIRED_M07_COEFFICIENTS.difference(values)
        if missing:
            raise ValueError(f"m07_effective_coefficient_missing:{sorted(missing)[0]}")
        caution = float(values["risk_vix_caution_threshold"])
        hot = float(values["risk_vix_hot_threshold"])
        if caution >= hot:
            raise ValueError("m07_effective_vix_threshold_order_invalid")
        return values

    @staticmethod
    def _posture_permission(
        request: SerialCognitionRequest,
        context: StageContext,
        decision: ModifierDecision,
        receipt: ModifierApplicationReceipt,
        status: str,
    ) -> PosturePermission:
        material = {
            "context_id": context.context_id,
            "decision_id": decision.decision_id,
            "decision_fingerprint": decision.semantic_fingerprint,
            "receipt_id": receipt.receipt_id,
            "receipt_fingerprint": semantic_fingerprint(receipt.model_dump(mode="python")),
            "status": status,
            "effective_at_utc": context.effective_at_utc,
        }
        return PosturePermission(
            posture_id=f"posture:{semantic_fingerprint(material)[:16]}",
            posture_version=request.posture_version,
            status=status,
            effective_at_utc=context.effective_at_utc,
            semantic_fingerprint=semantic_fingerprint(material),
        )

    @staticmethod
    def _fact_authority(
        *,
        fact_ref: str,
        owner_id: str,
        contract_version: str,
        effective_at_utc: datetime,
        value: Any,
    ) -> FactAuthority:
        material = {
            "fact_ref": fact_ref,
            "owner_id": owner_id,
            "contract_version": contract_version,
            "effective_at_utc": effective_at_utc,
            "value": value,
        }
        return FactAuthority(**material, semantic_fingerprint=semantic_fingerprint(material))

    @classmethod
    def _eligibility_context(
        cls,
        request: SerialCognitionRequest,
        context: StageContext,
        prepared: PreparedDataEnvelope,
        temporal: Any,
        regime: Any,
        options: Any,
        posture: PosturePermission,
    ) -> EligibilityContext:
        values = {
            "session_state": (
                "temporal_context",
                temporal.temporal_policy_version,
                temporal.session_state,
            ),
            "volatility_regime": (
                "market_regime_context",
                regime.regime_policy_version,
                regime.volatility_regime,
            ),
            "cross_asset_pressure_score": (
                "market_regime_context",
                regime.regime_policy_version,
                regime.cross_asset_pressure_score,
            ),
            "vix_level": ("market_regime_context", regime.regime_policy_version, regime.vix_level),
            "term_structure_state": (
                "options_flow",
                "options-flow.surface.v1",
                options.term_structure_state,
            ),
            "skew_state": ("options_flow", "options-flow.surface.v1", options.skew_state),
            "gamma_state": ("options_flow", "options-flow.surface.v1", options.gamma_state),
            "posture_status": ("posture_permission", request.posture_version, posture.status),
            "spot_price": ("m03", prepared.schema_version, prepared.payload.spot_price),
            "front_dte": ("m03", prepared.schema_version, prepared.payload.front_dte),
            "next_dte": ("m03", prepared.schema_version, prepared.payload.next_dte),
        }
        facts = {
            fact_ref: cls._fact_authority(
                fact_ref=fact_ref,
                owner_id=owner,
                contract_version=version,
                effective_at_utc=context.effective_at_utc,
                value=value,
            )
            for fact_ref, (owner, version, value) in values.items()
            if value is not None
        }
        material = {
            "context_id": f"eligibility:{context.context_id}",
            "context_version": request.eligibility_context_version,
            "effective_at_utc": context.effective_at_utc,
            "facts": facts,
        }
        return EligibilityContext(**material, semantic_fingerprint=semantic_fingerprint(material))

    @staticmethod
    def _m08_refs(
        catalogue: PlaybookCatalogue,
        decision: EligibilityDecision,
    ) -> tuple[AuthorityRef, ...]:
        refs: list[AuthorityRef] = [
            (
                "m08",
                catalogue.catalogue_id,
                catalogue.catalogue_version,
                catalogue.catalogue_fingerprint,
            )
        ]
        if decision.semantic_fingerprint is None:
            return tuple(refs)
        refs.append(
            (
                "m08",
                decision.decision_id,
                decision.decision_schema_version,
                decision.semantic_fingerprint,
            )
        )
        if decision.eligibility_lead is not None:
            lead = decision.eligibility_lead
            refs.append(
                (
                    "m08",
                    f"eligibility-lead:{decision.decision_id}:{lead.playbook_id}",
                    lead.playbook_version,
                    semantic_fingerprint(lead.model_dump(mode="python")),
                )
            )
        return tuple(refs)

    @staticmethod
    def _eligibility_carrier_facts(decision: EligibilityDecision) -> dict[str, Any]:
        lead = decision.eligibility_lead
        return {
            "eligibility_status": decision.status,
            "eligibility_lead_id": lead.playbook_id if lead is not None else None,
            "ordered_eligible_candidate_ids": tuple(
                item.playbook_id for item in decision.eligible_candidates
            ),
        }

    @staticmethod
    def _eligibility_status(
        decision: EligibilityDecision,
    ) -> tuple[str, str, tuple[str, ...]]:
        if decision.status == "eligible":
            return "eligible", "complete", ()
        if decision.status.startswith("stand_down"):
            return decision.status, "stand_down", (decision.reason or decision.status,)
        return decision.status, "rejected", (decision.reason or "m08_eligibility_rejected",)

    @staticmethod
    def _eligibility_result_refs(decision: EligibilityDecision) -> tuple[Pair, ...]:
        if decision.status != "eligible" or decision.eligibility_lead is None:
            return ()
        pairs: list[Pair] = [
            ("eligibility_status", "eligible"),
            ("eligibility_lead_id", decision.eligibility_lead.playbook_id),
        ]
        pairs.extend(
            (f"eligible_candidate.{index:03d}", item.playbook_id)
            for index, item in enumerate(decision.eligible_candidates)
        )
        return tuple(pairs)

    @staticmethod
    def _execution_result_refs(
        request: SerialCognitionRequest,
        context: StageContext,
        temporal: Any,
        regime: Any,
        options: Any,
        posture: Any,
        decision: EligibilityDecision,
    ) -> tuple[Pair, ...]:
        lead = decision.eligibility_lead
        if lead is None:
            raise ValueError("execution_requires_exact_m08_eligibility_lead")
        legacy_eligibility = PlaybookEligibilityOutput(
            admissibility_surface=EligibilityAdmissibilitySurface(
                permission_state=(
                    PermissionState.ALLOW
                    if posture.permission_state is not PermissionState.BLOCK
                    else PermissionState.BLOCK
                ),
                no_trade_reasons=[],
            ),
            active_family_ids=[item.playbook_id for item in decision.eligible_candidates],
            active_setup_variant_ids=[
                item.setup_variant_id
                for item in decision.eligible_candidates
                if item.setup_variant_id
            ],
            registry_id=decision.catalogue_id,
        )
        expression_input = ExecutionExpressionInput(
            temporal=temporal.model_dump(mode="python"),
            regime=regime.model_dump(mode="python"),
            options_flow=options.model_dump(mode="python"),
            posture=posture.model_dump(mode="python"),
            eligibility=decision.model_dump(mode="python"),
        )
        expression_seed = {
            "context_id": context.context_id,
            "eligibility_decision_id": decision.decision_id,
            "eligibility_decision_fingerprint": decision.semantic_fingerprint,
            "expression_policy_version": request.expression_policy_version,
        }
        expression_id = f"expression:{semantic_fingerprint(expression_seed)[:16]}"
        expression = evaluate_execution_expression(
            execution_input=expression_input,
            eligibility_output=legacy_eligibility,
            candidate_id=expression_id,
        )
        expression_material = {
            "expression_id": expression_id,
            "expression_version": request.expression_policy_version,
            "expression": expression.model_dump(mode="python"),
            "eligibility_decision_fingerprint": decision.semantic_fingerprint,
        }
        refs: list[Pair] = [
            ("playbook_family_id", lead.candidate_family_id),
            ("playbook_family_version", lead.candidate_family_version),
            ("playbook_id", lead.playbook_id),
            ("playbook_version", lead.playbook_version),
            ("setup_variant_id", lead.setup_variant_id),
            ("setup_variant_version", lead.setup_variant_version),
            ("expression_id", expression_id),
            ("expression_version", request.expression_policy_version),
            ("expression_fingerprint", semantic_fingerprint(expression_material)),
        ]
        refs.extend((f"lifecycle.{key}", value) for key, value in lead.lifecycle_intent.items())
        return tuple(refs)

    @staticmethod
    def _runner(
        request: SerialCognitionRequest,
        outputs: Mapping[str, StageOutput],
    ) -> SerialRunner:
        return SerialRunner(
            handlers={
                stage: (lambda _input, _deps, *, _stage=stage: outputs[_stage])
                for stage in SERIAL_STAGE_ORDER
            },
            runner_version=request.runner_version,
            stage_order_version=request.serial_order_version,
        )

    @classmethod
    def _run_terminal(
        cls,
        request: SerialCognitionRequest,
        context: StageContext,
        outputs: Mapping[str, StageOutput],
        existing_inputs: tuple[StageInput, ...],
        *,
        terminal_stage: str,
    ) -> tuple[SerialCandidate, tuple[StageInput, ...]]:
        by_stage = {item.stage: item for item in existing_inputs}
        for stage in SERIAL_STAGE_ORDER:
            if stage in by_stage:
                continue
            by_stage[stage] = cls._stage_input(
                context,
                stage=stage,
                authority_refs=(),
                facts={},
                owner_id="m08" if stage in {"eligibility", "execution"} else "m07",
                owner_version="1.0.0",
                missing_state=f"not_evaluated_after_{terminal_stage}",
            )
        stage_inputs = tuple(by_stage[stage] for stage in SERIAL_STAGE_ORDER)
        candidate = cls._runner(request, outputs).run(
            context=context,
            stage_inputs=stage_inputs,
        )
        return candidate, stage_inputs


__all__ = [
    "DEFAULT_MAPPING_POLICY_VERSIONS",
    "SerialCognitionOutcome",
    "SerialCognitionRequest",
    "SerialCognitionService",
]
