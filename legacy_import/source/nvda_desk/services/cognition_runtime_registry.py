"""Runtime registry and contract helpers for the Desk Cognition Grammar.

Gate C keeps the runtime-layer contract surface explicit by deriving field
contracts from the actual schema models and by enforcing a mandatory docstring
contract template for imported runtime services.
"""

from __future__ import annotations

from collections.abc import Iterable
from importlib import import_module
from typing import Any

from pydantic import BaseModel

from nvda_desk.schemas.cognition import (
    ModuleDocstringContractTemplate,
    RuntimeLayerContract,
    TraceStagePacket,
)


class DeskCognitionRuntimeRegistryService:
    """Expose deterministic runtime-layer contracts and docstring rules.

    Purpose:
        Keep the binding desk-runtime contract surface explicit and introspected.
    Inputs:
        No runtime payload is required; the registry inspects schema classes.
    Outputs:
        Ordered runtime-layer contracts, trace packets, and docstring checks.
    Determinism:
        Contracts are derived from the live schema models, not copied strings.
    """

    _CONTRACT_REQUIRED_FIELD_OVERRIDES: dict[str, set[str]] = {
        "playbook_eligibility": {
            "add_candidates",
            "hold_candidates",
            "trim_candidates",
            "reduce_candidates",
            "hedge_candidates",
            "rejected_playbook_reasons",
        },
        "review_explanation": {
            "stage_reason_packets",
            "rejected_playbooks",
            "contradictions",
            "review_packet",
        },
    }

    _LAYER_SPECS: tuple[tuple[str, str, str, str], ...] = (
        (
            "temporal_context",
            "nvda_desk.services.temporal_context.TemporalContextService",
            "nvda_desk.schemas.cognition.TemporalContextInput",
            "nvda_desk.schemas.cognition.TemporalContextOutput",
        ),
        (
            "market_regime_context",
            "nvda_desk.services.market_regime_context.MarketRegimeContextService",
            "nvda_desk.schemas.cognition.MarketRegimeContextInput",
            "nvda_desk.schemas.cognition.MarketRegimeContextOutput",
        ),
        (
            "options_flow_context",
            "nvda_desk.services.options_flow_context.OptionsFlowContextService",
            "nvda_desk.schemas.cognition.OptionsFlowContextInput",
            "nvda_desk.schemas.cognition.OptionsFlowContextOutput",
        ),
        (
            "posture_risk_permission",
            "nvda_desk.services.posture_risk.PostureRiskService",
            "nvda_desk.schemas.cognition.PostureRiskInput",
            "nvda_desk.schemas.cognition.PostureRiskOutput",
        ),
        (
            "playbook_eligibility",
            "nvda_desk.services.playbook_eligibility.PlaybookEligibilityService",
            "nvda_desk.schemas.cognition.PlaybookEligibilityInput",
            "nvda_desk.schemas.cognition.PlaybookEligibilityOutput",
        ),
        (
            "expression_execution",
            "nvda_desk.services.execution_expression.ExecutionExpressionService",
            "nvda_desk.schemas.cognition.ExecutionExpressionInput",
            "nvda_desk.schemas.cognition.ExecutionExpressionOutput",
        ),
        (
            "review_explanation",
            "nvda_desk.services.review_explanation.ReviewExplanationService",
            "nvda_desk.schemas.cognition.ReviewExplanationInput",
            "nvda_desk.schemas.cognition.ReviewExplanationOutput",
        ),
    )

    def docstring_template(self) -> ModuleDocstringContractTemplate:
        """Return the mandatory Gate C docstring template.

        Purpose:
            Provide the required docstring sections for runtime services.
        Inputs:
            No payload.
        Outputs:
            One template with the required section headers.
        Determinism:
            The template is static and shared across all binding layers.
        """

        return ModuleDocstringContractTemplate(
            template_id="gate_c_runtime_service_docstring",
            required_sections=["Purpose:", "Inputs:", "Outputs:", "Determinism:"],
        )

    def layer_contracts(self) -> list[RuntimeLayerContract]:
        """Return the ordered binding runtime contracts for all desk layers.

        Purpose:
            Expose runtime-layer contracts derived from the live schema models.
        Inputs:
            No payload.
        Outputs:
            Ordered runtime-layer contracts with required and optional fields.
        Determinism:
            Field lists are derived from model definitions in a stable order.
        """

        template_sections = self.docstring_template().required_sections
        contracts: list[RuntimeLayerContract] = []
        for grammar_role, service_path, input_path, output_path in self._LAYER_SPECS:
            input_model = self._resolve_model(input_path)
            output_model = self._resolve_model(output_path)
            required_input_fields, optional_input_fields = self._split_fields(input_model)
            required_output_fields, optional_output_fields = self._split_fields(output_model)
            required_output_override = self._CONTRACT_REQUIRED_FIELD_OVERRIDES.get(
                grammar_role, set()
            )
            if required_output_override:
                required_output_fields = sorted(
                    set(required_output_fields) | required_output_override
                )
                optional_output_fields = [
                    field_name
                    for field_name in optional_output_fields
                    if field_name not in required_output_override
                ]
            contracts.append(
                RuntimeLayerContract(
                    grammar_role=grammar_role,
                    service_path=service_path,
                    service_class_name=service_path.rsplit(".", 1)[-1],
                    input_model_name=input_model.__name__,
                    output_model_name=output_model.__name__,
                    required_input_fields=required_input_fields,
                    optional_input_fields=optional_input_fields,
                    required_output_fields=required_output_fields,
                    optional_output_fields=optional_output_fields,
                    docstring_contract_sections=template_sections,
                )
            )
        return contracts

    def build_trace_packet(self, *, grammar_role: str, summary: str) -> TraceStagePacket:
        """Build one deterministic trace-stage packet for an executed runtime layer.

        Purpose:
            Mirror runtime-layer contract metadata into one trace packet.
        Inputs:
            `grammar_role` selects the layer and `summary` records the result.
        Outputs:
            One trace packet with required field surfaces embedded.
        Determinism:
            The packet is derived from the ordered runtime contract registry.
        """

        contract = next(
            contract for contract in self.layer_contracts() if contract.grammar_role == grammar_role
        )
        return TraceStagePacket(
            grammar_role=contract.grammar_role,
            service_path=contract.service_path,
            input_model_name=contract.input_model_name,
            output_model_name=contract.output_model_name,
            required_input_fields=contract.required_input_fields,
            required_output_fields=contract.required_output_fields,
            summary=summary,
        )

    def assert_complete_contract_surface(self) -> None:
        """Raise if any binding grammar role is missing from the contract surface.

        Purpose:
            Guard against contract drift in the seven binding runtime layers.
        Inputs:
            No payload.
        Outputs:
            Raises on drift; otherwise returns `None`.
        Determinism:
            Compares the observed role order against the fixed registry order.
        """

        observed_roles = [contract.grammar_role for contract in self.layer_contracts()]
        expected_roles = [layer_spec[0] for layer_spec in self._LAYER_SPECS]
        if observed_roles != expected_roles:
            raise ValueError(
                f"runtime contract surface drifted: expected {expected_roles}, got {observed_roles}"
            )

    def assert_docstring_contracts(self) -> None:
        """Raise if any binding runtime service drifts from the docstring template.

        Purpose:
            Enforce the mandatory Gate C service docstring template.
        Inputs:
            No payload.
        Outputs:
            Raises on any missing section.
        Determinism:
            Checks the live class docstrings against one shared section list.
        """

        required_sections = self.docstring_template().required_sections
        missing: list[str] = []
        for contract in self.layer_contracts():
            service_class = self._resolve_object(contract.service_path)
            docstring = service_class.__doc__ or ""
            absent_sections = [section for section in required_sections if section not in docstring]
            if absent_sections:
                missing.append(f"{contract.service_class_name}:{','.join(absent_sections)}")
        if missing:
            raise ValueError(f"runtime service docstring drifted: {'; '.join(missing)}")

    def _resolve_model(self, dotted_path: str) -> type[BaseModel]:
        module_path, attr_name = dotted_path.rsplit(".", 1)
        model = getattr(import_module(module_path), attr_name)
        if not isinstance(model, type) or not issubclass(model, BaseModel):
            raise TypeError(f"{dotted_path} is not a pydantic model")
        return model

    def _resolve_object(self, dotted_path: str) -> Any:
        module_path, attr_name = dotted_path.rsplit(".", 1)
        return getattr(import_module(module_path), attr_name)

    def _split_fields(self, model: type[BaseModel]) -> tuple[list[str], list[str]]:
        required_fields: list[str] = []
        optional_fields: list[str] = []
        for field_name, field_info in model.model_fields.items():
            if field_info.is_required():
                required_fields.append(field_name)
            else:
                optional_fields.append(field_name)
        return required_fields, optional_fields

    def _flatten(self, values: Iterable[str]) -> list[str]:
        return list(values)
