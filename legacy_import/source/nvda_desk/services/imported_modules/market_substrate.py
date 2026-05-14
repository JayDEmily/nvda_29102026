"""Gate 18 shared market-data substrate contract services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from nvda_desk.schemas.dmp import (
    DmpBehaviourClass,
    DmpGrammarRole,
    DeskModulePacketV3,
    build_dmp_v3_packet_from_payload,
)
from nvda_desk.schemas.imported_modules.market_substrate import (
    MacroDataCaptureContractOutput,
    MarketSubstrateContext,
    MarketSubstratePayload,
    OptionsDataCaptureContractOutput,
    OptionsMetadataCaptureContractOutput,
    PeerEquityCaptureContractOutput,
    SpotDataCaptureContractOutput,
    VwapAccumulatorContractOutput,
    VwapRocContractOutput,
)
from nvda_desk.schemas.imported_modules.tranche_a import (
    ContractComputationMode,
    ContractDependencyFence,
    ContractDependencyStatus,
)


@dataclass(frozen=True)
class MarketSubstrateContractEmission:
    """One typed substrate contract output plus its DMP packets."""

    output: MarketSubstratePayload
    packet: DeskModulePacketV3


def _dependency_fences(
    dependencies: list[str],
    *,
    satisfied: set[str] | None = None,
    proxied: dict[str, str] | None = None,
) -> list[ContractDependencyFence]:
    satisfied = satisfied or set()
    proxied = proxied or {}
    fences: list[ContractDependencyFence] = []
    for dependency in dependencies:
        if dependency in proxied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.PROXIED_FROM_RUNTIME,
                    note=proxied[dependency],
                )
            )
        elif dependency in satisfied:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.SATISFIED,
                    note="available directly inside the deterministic runtime surface",
                )
            )
        else:
            fences.append(
                ContractDependencyFence(
                    dependency=dependency,
                    status=ContractDependencyStatus.FENCED_MISSING_SOURCE,
                    note="not available in the current deterministic runtime; kept as an explicit contract fence",
                )
            )
    return fences


class MarketSubstrateContractService:
    """Emit Gate-18 shared market-data substrate contracts in frozen order."""

    def evaluate(self, context: MarketSubstrateContext) -> list[MarketSubstrateContractEmission]:
        outputs: list[MarketSubstratePayload] = [
            self._spot_data_capture(context),
            self._peer_equity_capture(context),
            self._options_data_capture(context),
            self._options_metadata_capture(context),
            self._macro_data_capture(context),
            self._vwap_accumulator(context),
            self._vwap_roc(context),
        ]
        return [
            self._emit_packet(
                output=output,
                emitted_at=context.emitted_at,
                stack_id=context.stack_id,
                coefficient_set_id=context.coefficient_set_id,
            )
            for output in outputs
        ]

    def _emit_packet(
        self,
        *,
        output: MarketSubstratePayload,
        emitted_at: datetime,
        stack_id: str | None,
        coefficient_set_id: str | None,
    ) -> MarketSubstrateContractEmission:
        packet = build_dmp_v3_packet_from_payload(
            packet_id=f"dmp::market_substrate::{output.canonical_slug}::{emitted_at.isoformat()}",
            emitted_at=emitted_at,
            grammar_role=DmpGrammarRole(output.grammar_role),
            behaviour_class=DmpBehaviourClass.MODULE_OUTPUT,
            payload=output,
            trader_summary=f"{output.canonical_slug} / {output.computation_mode.value}",
            stack_id=stack_id,
            coefficient_set_id=coefficient_set_id,
            dependencies=[fence.dependency for fence in output.dependency_fences],
            input_model_name="MarketSubstrateContext",
            output_model_name=output.__class__.__name__,
            trace_id=f"trace::market_substrate::{emitted_at.isoformat()}",
            run_id=f"run::market_substrate::{emitted_at.isoformat()}",
            module_instance_id=f"market_substrate::{output.canonical_slug}",
            registry_version="market_substrate_v1",
            environment_tag="research",
        )
        return MarketSubstrateContractEmission(output=output, packet=packet)

    def _spot_data_capture(self, context: MarketSubstrateContext) -> SpotDataCaptureContractOutput:
        return SpotDataCaptureContractOutput(
            canonical_id="archive-module-001",
            canonical_slug="spot_data_capture",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["broker_spot_ticks"],
                proxied={
                    "broker_spot_ticks": "proxied from the current options-flow spot-price input",
                },
            ),
            contract_notes=[
                "Live tick capture remains outside the deterministic runtime; this contract preserves the spot-price surface only.",
            ],
            spot_price=context.options_flow_input.spot_price,
            capture_state="runtime_spot_proxy",
            proxy_basis=["options_flow_input.spot_price"],
        )

    def _peer_equity_capture(
        self, context: MarketSubstrateContext
    ) -> PeerEquityCaptureContractOutput:
        return PeerEquityCaptureContractOutput(
            canonical_id="archive-module-007",
            canonical_slug="peer_equity_capture",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["peer_spot_ticks"],
                proxied={
                    "peer_spot_ticks": "proxied from the current regime-input peer return fields",
                },
            ),
            contract_notes=[
                "Peer capture stays as a shared substrate proxy until live peer-tick ingestion is built explicitly.",
            ],
            peer_symbols=["NQ", "ES", "SOX"],
            peer_returns={
                "NQ": context.regime_input.nq_return_pct,
                "ES": context.regime_input.es_return_pct,
                "SOX": context.regime_input.sox_return_pct,
            },
            capture_state="runtime_peer_proxy",
        )

    def _options_data_capture(
        self, context: MarketSubstrateContext
    ) -> OptionsDataCaptureContractOutput:
        snapshot_count = len(context.options_flow_input.repeated_snapshot_sequence)
        return OptionsDataCaptureContractOutput(
            canonical_id="archive-module-003",
            canonical_slug="options_data_capture",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["broker_options_snapshots"],
                proxied={
                    "broker_options_snapshots": "proxied from the current options-flow snapshot sequence and ATM-IV inputs",
                },
            ),
            contract_notes=[
                "Snapshot capture remains a proxy surface; the deterministic runtime does not own raw options-snapshot ingestion yet.",
            ],
            snapshot_count=snapshot_count,
            front_atm_iv=context.options_flow_input.front_atm_iv,
            next_atm_iv=context.options_flow_input.next_atm_iv,
            capture_state=(
                "runtime_options_proxy"
                if snapshot_count or context.options_flow_input.front_atm_iv
                else "runtime_options_summary_proxy"
            ),
        )

    def _options_metadata_capture(
        self, context: MarketSubstrateContext
    ) -> OptionsMetadataCaptureContractOutput:
        return OptionsMetadataCaptureContractOutput(
            canonical_id="archive-module-004",
            canonical_slug="options_metadata_capture",
            grammar_role=DmpGrammarRole.OPTIONS_FLOW_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["broker_option_chain_metadata"],
                proxied={
                    "broker_option_chain_metadata": "proxied from the current DTE, dominant strike, and strike-cluster context surfaces",
                },
            ),
            contract_notes=[
                "Chain metadata stays as a proxy summary until a separate metadata ingestion boundary exists.",
            ],
            front_dte=context.options_flow_input.front_dte,
            next_dte=context.options_flow_input.next_dte,
            dominant_strike=context.options_flow.dominant_strike,
            metadata_state="runtime_metadata_proxy",
        )

    def _macro_data_capture(
        self, context: MarketSubstrateContext
    ) -> MacroDataCaptureContractOutput:
        return MacroDataCaptureContractOutput(
            canonical_id="archive-module-005",
            canonical_slug="macro_data_capture",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.DERIVED_FROM_RUNTIME_PROXY,
            dependency_fences=_dependency_fences(
                ["macro_market_feeds"],
                proxied={
                    "macro_market_feeds": "proxied from the current regime-input VIX, VVIX, rates, and FX fields",
                },
            ),
            contract_notes=[
                "Macro capture remains a proxy surface until explicit macro-feed ingestion is built outside Gate 18.",
            ],
            vix_level=context.regime_input.vix_level,
            vvix_level=context.regime_input.vvix_level,
            curve_10s2s=round(context.regime_input.us10y - context.regime_input.us2y, 4),
            usdjpy=context.regime_input.usdjpy,
            capture_state="runtime_macro_proxy",
        )

    def _vwap_accumulator(self, context: MarketSubstrateContext) -> VwapAccumulatorContractOutput:
        return VwapAccumulatorContractOutput(
            canonical_id="archive-module-002",
            canonical_slug="vwap_accumulator",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.FENCED_CONTRACT_ONLY,
            dependency_fences=_dependency_fences(["spot_trade_ticks"]),
            contract_notes=[
                "The deterministic runtime does not carry raw trade-tick series, so VWAP accumulation remains fenced at Gate 18.",
            ],
            spot_vwap_10s=None,
            observation_count=None,
            accumulation_state="fenced_missing_trade_ticks",
        )

    def _vwap_roc(self, context: MarketSubstrateContext) -> VwapRocContractOutput:
        return VwapRocContractOutput(
            canonical_id="archive-module-008",
            canonical_slug="vwap_roc",
            grammar_role=DmpGrammarRole.MARKET_REGIME_CONTEXT.value,
            computation_mode=ContractComputationMode.FENCED_CONTRACT_ONLY,
            dependency_fences=_dependency_fences(["spot_vwap_10s"]),
            contract_notes=[
                "VWAP ROC stays fenced until the shared VWAP accumulator has real tick-derived state rather than a proxy placeholder.",
            ],
            vwap_roc=None,
            slope_flag="unknown_without_vwap_ticks",
            derivation_state="fenced_by_missing_vwap_state",
        )
