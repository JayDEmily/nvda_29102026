"""Deterministic replay and stack-comparison harness.

This service replays a checked scenario pack through the Desk Cognition runtime,
applies stack definitions plus coefficient overrides, aggregates stable metrics,
and serialises deterministic comparison reports.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import cast

from nvda_desk.config import Settings
from nvda_desk.schemas.calibration import (
    AblationSignalReport,
    CoefficientAuditPacket,
    CoefficientSet,
    ComparisonMetrics,
    ComparisonReport,
    ContextSliceReport,
    FragilitySignalReport,
    GovernedCoefficientSnapshot,
    GroupReviewHorizonResult,
    HorizonDiscoveryOutcome,
    HorizonDiscoveryReport,
    OffsetComparisonOutcome,
    ReplayFixturePack,
    ReplayPacketLineage,
    ReplayRunResult,
    ReplayScenarioRecord,
    StabilityComparisonRule,
    StackDefinition,
    StackVersusStackSummary,
    WalkForwardHarnessAuthorityPacket,
    WalkForwardSliceDefinition,
    WalkForwardWindowContract,
    WalkForwardWindowMode,
    WalkForwardWindowRole,
)
from nvda_desk.schemas.cognition import (
    InventoryState,
    MarketRegimeContextInput,
    OptionsFlowContextInput,
    OptionsFlowMicroSnapshot,
    PinProgressionPoint,
    ReviewExplanationOutput,
    StrikeClusterObservation,
    TemporalContextInput,
    TenorCurvePoint,
)
from nvda_desk.schemas.replay import ReplayHorizonDiscoveryResponse
from nvda_desk.services.cognition_runtime import DeskCognitionRuntime


class ReplayComparisonService:
    """Run deterministic replay comparisons across explicit stack definitions."""

    def __init__(self, settings: Settings):
        self._runtime = DeskCognitionRuntime(settings)

    def load_stack_definitions(self, path: str | Path) -> dict[str, StackDefinition]:
        """Load stack definitions from a JSON file and index them by stack id."""

        raw = json.loads(Path(path).read_text())
        payload = raw if isinstance(raw, dict) else {"stack_definitions": raw}
        definitions = [
            StackDefinition.model_validate(item) for item in payload.get("stack_definitions", [])
        ]
        return {
            definition.stack_id: definition
            for definition in sorted(definitions, key=lambda item: item.stack_id)
        }

    def load_fixture_pack(self, path: str | Path) -> ReplayFixturePack:
        """Load a deterministic replay fixture pack from JSON."""

        raw = json.loads(Path(path).read_text())
        return ReplayFixturePack.model_validate(raw)

    def compare_from_fixture_pack(
        self, path: str | Path
    ) -> tuple[list[ReplayRunResult], ComparisonReport]:
        """Load a fixture pack and run deterministic comparison in one call."""

        fixture_pack = self.load_fixture_pack(path)
        return self.compare(
            fixture_pack_id=fixture_pack.fixture_pack_id,
            scenarios=fixture_pack.scenarios,
            coefficient_sets=fixture_pack.coefficient_sets,
            stack_definitions=fixture_pack.stack_definitions,
            walk_forward_slices=fixture_pack.walk_forward_slices,
        )

    def compare(
        self,
        *,
        fixture_pack_id: str | None,
        scenarios: list[ReplayScenarioRecord],
        coefficient_sets: list[CoefficientSet],
        stack_definitions: list[StackDefinition],
        walk_forward_slices: list[WalkForwardSliceDefinition] | None = None,
    ) -> tuple[list[ReplayRunResult], ComparisonReport]:
        """Run deterministic comparisons and return run-level results plus report."""

        ordered_scenarios = sorted(scenarios, key=lambda item: (item.ts, item.scenario_id))
        ordered_sets = sorted(coefficient_sets, key=lambda item: item.set_id)
        stack_index = {
            definition.stack_id: definition
            for definition in sorted(stack_definitions, key=lambda item: item.stack_id)
        }
        runs: list[ReplayRunResult] = []
        for coefficient_set in ordered_sets:
            stack_definition = stack_index[coefficient_set.stack_id]
            for scenario in ordered_scenarios:
                runs.append(self._run_one(coefficient_set, stack_definition, scenario))

        scenario_ids = [scenario.scenario_id for scenario in ordered_scenarios]
        overall_reports = {
            coefficient_set.set_id: self._aggregate_runs(
                [run for run in runs if run.coefficient_set_id == coefficient_set.set_id]
            )
            for coefficient_set in ordered_sets
        }
        slice_reports: dict[str, dict[str, ComparisonMetrics]] = {}
        for slice_definition in sorted(walk_forward_slices or [], key=lambda item: item.slice_id):
            slice_reports[slice_definition.slice_id] = {
                coefficient_set.set_id: self._aggregate_runs(
                    [
                        run
                        for run in runs
                        if run.coefficient_set_id == coefficient_set.set_id
                        and run.scenario_id in set(slice_definition.scenario_ids)
                    ]
                )
                for coefficient_set in ordered_sets
            }
        stack_vs_stack_summary = self._stack_vs_stack_summary(ordered_sets, overall_reports)
        coefficient_snapshots_by_set = {
            coefficient_set.set_id: self._collect_snapshot_evidence(
                [run for run in runs if run.coefficient_set_id == coefficient_set.set_id]
            )
            for coefficient_set in ordered_sets
        }
        return runs, ComparisonReport(
            fixture_pack_id=fixture_pack_id,
            scenario_ids=scenario_ids,
            reports=overall_reports,
            slice_reports=slice_reports,
            coefficient_snapshots_by_set=coefficient_snapshots_by_set,
            stack_vs_stack_summary=stack_vs_stack_summary,
        )

    def serialize_report(self, report: ComparisonReport, output_path: str | Path) -> str:
        """Serialise a comparison report to stable JSON and write it to disk."""

        serialised = json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True)
        Path(output_path).write_text(serialised + "\n")
        return serialised + "\n"

    def _run_one(
        self,
        coefficient_set: CoefficientSet,
        stack_definition: StackDefinition,
        scenario: ReplayScenarioRecord,
    ) -> ReplayRunResult:
        payload = scenario.payload
        applied_module_weights = self._merge_weights(
            stack_definition.module_weights,
            coefficient_set.module_weights,
        )
        applied_sub_coefficients = self._merge_weights(
            stack_definition.sub_coefficients,
            coefficient_set.sub_coefficients,
        )
        temporal_input = TemporalContextInput(
            ts=self._coerce_datetime(payload["ts"]),
            next_expiry=self._optional_datetime(payload.get("next_expiry")),
            next_event_at=self._optional_datetime(payload.get("next_event_at")),
            prior_session_return_pct=self._get_float(payload, "prior_session_return_pct", 0.0),
            intraday_move_pct=self._get_float(payload, "intraday_move_pct", 0.0),
        )
        regime_input = MarketRegimeContextInput(
            nvda_return_pct=self._get_float(payload, "nvda_return_pct"),
            nq_return_pct=self._get_float(payload, "nq_return_pct"),
            es_return_pct=self._get_float(payload, "es_return_pct"),
            sox_return_pct=self._get_float(payload, "sox_return_pct"),
            breadth_score=self._get_float(payload, "breadth_score"),
            concentration_score=self._get_float(payload, "concentration_score"),
            vix_level=self._override_float("vix_level", payload, applied_sub_coefficients, 1.0),
            vvix_level=self._get_float(payload, "vvix_level"),
            us10y=self._get_float(payload, "us10y"),
            us2y=self._get_float(payload, "us2y"),
            usdjpy=self._get_float(payload, "usdjpy"),
        )
        options_input = OptionsFlowContextInput(
            spot_price=self._get_float(payload, "spot_price"),
            front_dte=self._get_int(payload, "front_dte"),
            next_dte=self._get_int(payload, "next_dte"),
            front_atm_iv=self._override_float(
                "front_atm_iv", payload, applied_sub_coefficients, 1.0
            ),
            next_atm_iv=self._get_float(payload, "next_atm_iv"),
            put_call_skew=self._get_float(payload, "put_call_skew"),
            gamma_pressure_score=self._override_float(
                "gamma_pressure_score", payload, applied_sub_coefficients, 1.0
            ),
            call_put_imbalance=self._get_float(payload, "call_put_imbalance"),
            oi_concentration=self._get_float(payload, "oi_concentration"),
            atm_straddle_value=self._get_float(payload, "atm_straddle_value"),
            front_realised_vol=self._get_float(payload, "front_realised_vol", 0.0),
            next_realised_vol=self._get_float(payload, "next_realised_vol", 0.0),
            vix_level=self._override_float("vix_level", payload, applied_sub_coefficients, 1.0),
            vvix_level=self._get_float(payload, "vvix_level", 0.0),
            spot_to_pin_distance_pct=self._get_float(payload, "spot_to_pin_distance_pct", 0.0),
            call_oi_near_spot=self._get_float(payload, "call_oi_near_spot", 0.0),
            put_oi_near_spot=self._get_float(payload, "put_oi_near_spot", 0.0),
            front_volume_near_spot=self._get_float(payload, "front_volume_near_spot", 0.0),
            next_volume_near_spot=self._get_float(payload, "next_volume_near_spot", 0.0),
            vanna_proxy=self._get_float(payload, "vanna_proxy", 0.0),
            charm_proxy=self._get_float(payload, "charm_proxy", 0.0),
            repeated_snapshot_sequence=[
                OptionsFlowMicroSnapshot.model_validate(item)
                for item in cast(
                    list[dict[str, object]],
                    payload.get("repeated_snapshot_sequence", []),
                )
            ],
            tenor_iv_curve=[
                TenorCurvePoint.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("tenor_iv_curve", []))
            ],
            pin_progression_sequence=[
                PinProgressionPoint.model_validate(item)
                for item in cast(
                    list[dict[str, object]], payload.get("pin_progression_sequence", [])
                )
            ],
            nearby_strike_clusters=[
                StrikeClusterObservation.model_validate(item)
                for item in cast(list[dict[str, object]], payload.get("nearby_strike_clusters", []))
            ],
        )
        runtime_result = self._runtime.run(
            temporal_input=temporal_input,
            regime_input=regime_input,
            options_flow_input=options_input,
            inventory_state=InventoryState.model_validate(payload["inventory_state"]),
            risk_budget_remaining_pct=self._get_float(payload, "risk_budget_remaining_pct"),
            stack_id=stack_definition.stack_id,
            coefficient_set_id=coefficient_set.set_id,
        )
        active_playbook_ids = self._apply_stack_playbook_filter(
            runtime_result.execution.active_playbook_ids,
            stack_definition=stack_definition,
        )
        veto_observed = not active_playbook_ids
        veto_expected = scenario.expectation.expected_veto
        playbook_precision = self._playbook_precision(
            expected_playbooks=scenario.expectation.expected_playbooks,
            active_playbook_ids=active_playbook_ids,
        )
        review_completeness = self._review_completeness(
            expected_stages=scenario.expectation.expected_review_stages,
            runtime_review=runtime_result.review,
        )
        contradiction_count = len(runtime_result.review.contradictions)
        contradiction_rate = round(
            contradiction_count / max(len(scenario.expectation.expected_review_stages), 1),
            4,
        )
        score_components = self._score_components(
            active_playbook_ids=active_playbook_ids,
            permission_state=runtime_result.posture.permission_state.value,
            target_fresh_deployable_pct=runtime_result.execution.target_fresh_deployable_pct,
            applied_module_weights=applied_module_weights,
            applied_sub_coefficients=applied_sub_coefficients,
        )
        governed_snapshot = self._governed_coefficient_snapshot(runtime_result.review)
        replay_score = round(
            score_components["base_capital"]
            * score_components["execution_weight"]
            * score_components["playbook_weight"]
            * score_components["sub_coefficient_scalar"]
            * score_components["permission_scalar"],
            4,
        )
        return ReplayRunResult(
            coefficient_set_id=coefficient_set.set_id,
            stack_id=stack_definition.stack_id,
            scenario_id=scenario.scenario_id,
            permission_state=runtime_result.posture.permission_state.value,
            active_playbook_ids=active_playbook_ids,
            target_fresh_deployable_pct=runtime_result.execution.target_fresh_deployable_pct,
            replay_score=replay_score,
            governed_coefficient_snapshot=governed_snapshot,
            veto_expected=veto_expected,
            veto_observed=veto_observed,
            veto_correct=1.0 if veto_observed == veto_expected else 0.0,
            contradiction_count=contradiction_count,
            contradiction_rate=contradiction_rate,
            playbook_precision=playbook_precision,
            review_completeness=review_completeness,
            conflict_count=len(runtime_result.review.conflict_tags),
            coefficient_audit=CoefficientAuditPacket(
                stack_id=stack_definition.stack_id,
                enabled_playbooks=stack_definition.enabled_playbooks,
                disabled_playbooks=stack_definition.disabled_playbooks,
                applied_module_weights=applied_module_weights,
                applied_sub_coefficients=applied_sub_coefficients,
                scoring_components=score_components,
                governed_coefficient_snapshot_id=(
                    governed_snapshot.snapshot_id if governed_snapshot is not None else None
                ),
            ),
            review=runtime_result.review,
            imported_module_citations=runtime_result.review.imported_module_citations,
            imported_module_maturity_counts=runtime_result.review.imported_module_maturity_counts,
            packet_lineage=ReplayPacketLineage(
                replay_trace_id=(
                    f"replay-trace::{stack_definition.stack_id}::"
                    f"{coefficient_set.set_id}::{scenario.scenario_id}"
                ),
                review_packet_id=runtime_result.stage_packet_ids["review"],
                decision_packet_id=runtime_result.stage_packet_ids["execution"],
                packet_lineage=list(runtime_result.packet_lineage),
                stage_packet_ids=runtime_result.stage_packet_ids,
            ),
        )

    def _governed_coefficient_snapshot(
        self,
        review_output: ReviewExplanationOutput,
    ) -> GovernedCoefficientSnapshot | None:
        effective_policy = review_output.effective_policy
        if effective_policy is None or not effective_policy.resolved_surfaces:
            return None
        resolved_surfaces = sorted(
            effective_policy.resolved_surfaces,
            key=lambda item: item.target_surface.value,
        )
        authority_versions = sorted({item.authority_version for item in resolved_surfaces})
        authority_version = authority_versions[0] if len(authority_versions) == 1 else "+".join(authority_versions)
        canonical_payload = {
            "authority_version": authority_version,
            "resolved_surfaces": [item.model_dump(mode="json") for item in resolved_surfaces],
        }
        digest = hashlib.sha256(
            json.dumps(canonical_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:16]
        return GovernedCoefficientSnapshot(
            snapshot_id=f"coefficient-snapshot::{authority_version}::{digest}",
            authority_version=authority_version,
            resolved_surfaces=resolved_surfaces,
        )

    def _collect_snapshot_evidence(
        self,
        runs: list[ReplayRunResult],
    ) -> list[GovernedCoefficientSnapshot]:
        unique: dict[str, GovernedCoefficientSnapshot] = {}
        for run in runs:
            snapshot = run.governed_coefficient_snapshot
            if snapshot is None:
                continue
            unique.setdefault(snapshot.snapshot_id, snapshot)
        return [unique[key] for key in sorted(unique)]

    def _aggregate_runs(self, runs: list[ReplayRunResult]) -> ComparisonMetrics:
        if not runs:
            return ComparisonMetrics(
                run_count=0,
                veto_rate=0.0,
                veto_correctness_rate=0.0,
                mean_fresh_deployable_pct=0.0,
                mean_replay_score=0.0,
                mean_contradiction_rate=0.0,
                mean_playbook_precision=0.0,
                review_completeness_rate=0.0,
                active_playbook_rate=0.0,
                mean_active_playbook_count=0.0,
                mean_conflict_count=0.0,
            )
        count = float(len(runs))
        return ComparisonMetrics(
            run_count=len(runs),
            veto_rate=round(sum(1.0 if run.veto_observed else 0.0 for run in runs) / count, 4),
            veto_correctness_rate=round(sum(run.veto_correct for run in runs) / count, 4),
            mean_fresh_deployable_pct=round(
                sum(run.target_fresh_deployable_pct for run in runs) / count, 4
            ),
            mean_replay_score=round(sum(run.replay_score for run in runs) / count, 4),
            mean_contradiction_rate=round(sum(run.contradiction_rate for run in runs) / count, 4),
            mean_playbook_precision=round(sum(run.playbook_precision for run in runs) / count, 4),
            review_completeness_rate=round(sum(run.review_completeness for run in runs) / count, 4),
            active_playbook_rate=round(
                sum(1.0 if run.active_playbook_ids else 0.0 for run in runs) / count, 4
            ),
            mean_active_playbook_count=round(
                sum(float(len(run.active_playbook_ids)) for run in runs) / count, 4
            ),
            mean_conflict_count=round(sum(float(run.conflict_count) for run in runs) / count, 4),
        )

    def _stack_vs_stack_summary(
        self,
        coefficient_sets: list[CoefficientSet],
        reports: dict[str, ComparisonMetrics],
    ) -> list[StackVersusStackSummary]:
        summaries: list[StackVersusStackSummary] = []
        ordered_sets = sorted(coefficient_sets, key=lambda item: item.set_id)
        for index, left in enumerate(ordered_sets):
            for right in ordered_sets[index + 1 :]:
                left_report = reports[left.set_id]
                right_report = reports[right.set_id]
                summaries.append(
                    StackVersusStackSummary(
                        left_set_id=left.set_id,
                        right_set_id=right.set_id,
                        left_stack_id=left.stack_id,
                        right_stack_id=right.stack_id,
                        delta_mean_replay_score=round(
                            left_report.mean_replay_score - right_report.mean_replay_score,
                            4,
                        ),
                        delta_veto_correctness_rate=round(
                            left_report.veto_correctness_rate - right_report.veto_correctness_rate,
                            4,
                        ),
                        delta_mean_playbook_precision=round(
                            left_report.mean_playbook_precision
                            - right_report.mean_playbook_precision,
                            4,
                        ),
                        delta_mean_fresh_deployable_pct=round(
                            left_report.mean_fresh_deployable_pct
                            - right_report.mean_fresh_deployable_pct,
                            4,
                        ),
                    )
                )
        return summaries

    def _merge_weights(
        self, baseline: dict[str, float], overrides: dict[str, float]
    ) -> dict[str, float]:
        merged = dict(sorted(baseline.items()))
        merged.update(dict(sorted(overrides.items())))
        return merged

    def _apply_stack_playbook_filter(
        self,
        active_playbook_ids: list[str],
        *,
        stack_definition: StackDefinition,
    ) -> list[str]:
        filtered = list(active_playbook_ids)
        if stack_definition.enabled_playbooks:
            allowed = set(stack_definition.enabled_playbooks)
            filtered = [playbook_id for playbook_id in filtered if playbook_id in allowed]
        if stack_definition.disabled_playbooks:
            blocked = set(stack_definition.disabled_playbooks)
            filtered = [playbook_id for playbook_id in filtered if playbook_id not in blocked]
        return filtered

    def _playbook_precision(
        self, *, expected_playbooks: list[str], active_playbook_ids: list[str]
    ) -> float:
        expected = set(expected_playbooks)
        active = set(active_playbook_ids)
        if not expected and not active:
            return 1.0
        if not active:
            return 0.0
        return round(len(expected & active) / len(active), 4)

    def _review_completeness(
        self,
        *,
        expected_stages: list[str],
        runtime_review: ReviewExplanationOutput,
    ) -> float:
        expected = set(expected_stages)
        actual = {packet.stage for packet in runtime_review.stage_reason_packets}
        if not expected:
            return 1.0
        packet_fraction = len(expected & actual) / len(expected)
        packet_present = 1.0 if runtime_review.review_packet else 0.0
        return round(packet_fraction * packet_present, 4)

    def _score_components(
        self,
        *,
        active_playbook_ids: list[str],
        permission_state: str,
        target_fresh_deployable_pct: float,
        applied_module_weights: dict[str, float],
        applied_sub_coefficients: dict[str, float],
    ) -> dict[str, float]:
        playbook_weights = [
            applied_module_weights.get(playbook_id, 1.0) for playbook_id in active_playbook_ids
        ]
        playbook_weight = sum(playbook_weights) / len(playbook_weights) if playbook_weights else 0.0
        sub_coefficient_scalar = (
            sum(applied_sub_coefficients.values()) / len(applied_sub_coefficients)
            if applied_sub_coefficients
            else 1.0
        )
        permission_scalar = {
            "block": 0.0,
            "derisk": 0.6,
            "allow": 1.0,
        }[permission_state]
        return {
            "base_capital": round(target_fresh_deployable_pct / 100.0, 4),
            "execution_weight": round(applied_module_weights.get("execution_expression", 1.0), 4),
            "playbook_weight": round(playbook_weight, 4),
            "sub_coefficient_scalar": round(sub_coefficient_scalar, 4),
            "permission_scalar": round(permission_scalar, 4),
        }

    def _override_float(
        self,
        field_name: str,
        payload: dict[str, object],
        applied_sub_coefficients: dict[str, float],
        default_weight: float,
    ) -> float:
        weight = applied_sub_coefficients.get(field_name, default_weight)
        return self._get_float(payload, field_name) * weight

    def _get_float(
        self, payload: dict[str, object], field_name: str, default: float | None = None
    ) -> float:
        value = payload.get(field_name, default)
        if value is None:
            raise TypeError(f"scenario field {field_name} is required")
        return float(cast(float | int | str, value))

    def _get_int(self, payload: dict[str, object], field_name: str) -> int:
        value = payload.get(field_name)
        if value is None:
            raise TypeError(f"scenario field {field_name} is required")
        return int(cast(float | int | str, value))

    def _coerce_datetime(self, value: object) -> datetime:
        if not isinstance(value, str):
            raise TypeError("scenario ts must be an ISO datetime string")
        return datetime.fromisoformat(value)

    def _optional_datetime(self, value: object) -> datetime | None:
        if value is None:
            return None
        return self._coerce_datetime(value)

    def discover_review_horizons_from_fixture_pack(
        self,
        path: str | Path,
        authority: WalkForwardHarnessAuthorityPacket,
    ) -> ReplayHorizonDiscoveryResponse:
        """Run the bounded Gate 79 harness from a checked-in replay fixture pack."""

        fixture_pack = self.load_fixture_pack(path)
        generated_windows = self.build_walk_forward_windows(fixture_pack.scenarios, authority)
        forward_slices = [
            WalkForwardSliceDefinition(
                slice_id=window.window_id,
                label=f"{window.surface_key} {window.role.value} {window.block_sessions}",
                scenario_ids=window.scenario_ids,
            )
            for window in generated_windows
            if window.role is WalkForwardWindowRole.FORWARD
        ]
        _, report = self.compare(
            fixture_pack_id=fixture_pack.fixture_pack_id,
            scenarios=fixture_pack.scenarios,
            coefficient_sets=fixture_pack.coefficient_sets,
            stack_definitions=fixture_pack.stack_definitions,
            walk_forward_slices=forward_slices,
        )
        horizon_report = self.evaluate_horizon_discovery(
            report=report,
            authority=authority,
            generated_windows=generated_windows,
            scenarios=fixture_pack.scenarios,
        )
        return ReplayHorizonDiscoveryResponse(
            fixture_pack_id=fixture_pack.fixture_pack_id,
            authority=authority,
            report=horizon_report,
        )

    def build_walk_forward_windows(
        self,
        scenarios: list[ReplayScenarioRecord],
        authority: WalkForwardHarnessAuthorityPacket,
    ) -> list[WalkForwardWindowContract]:
        """Generate chronology-safe calibration, validation, and forward windows."""

        ordered = sorted(scenarios, key=lambda item: (item.ts, item.scenario_id))
        scenario_ids = [scenario.scenario_id for scenario in ordered]
        total = len(scenario_ids)
        windows: list[WalkForwardWindowContract] = []
        for surface_key in authority.surface_keys:
            for block_sessions in authority.candidate_forward_blocks:
                for offset in authority.start_offsets:
                    iteration = 0
                    growth = 0
                    rolling_start = offset.offset_sessions
                    while True:
                        if authority.window_mode is WalkForwardWindowMode.ANCHORED:
                            calibration_start = offset.offset_sessions
                            calibration_end = (
                                calibration_start + authority.calibration_window + growth
                            )
                        else:
                            calibration_start = rolling_start
                            calibration_end = calibration_start + authority.calibration_window
                        validation_start = calibration_end
                        validation_end = validation_start + authority.validation_window
                        forward_start = validation_end
                        forward_end = forward_start + block_sessions
                        if forward_end > total:
                            break
                        spans = [
                            (
                                WalkForwardWindowRole.CALIBRATION,
                                calibration_start,
                                calibration_end,
                            ),
                            (
                                WalkForwardWindowRole.VALIDATION,
                                validation_start,
                                validation_end,
                            ),
                            (WalkForwardWindowRole.FORWARD, forward_start, forward_end),
                        ]
                        for role, start_idx, end_idx in spans:
                            windows.append(
                                WalkForwardWindowContract(
                                    window_id=(
                                        f"{surface_key}::{offset.offset_id}::block_{block_sessions}::"
                                        f"iter_{iteration}::{role.value}"
                                    ),
                                    surface_key=surface_key,
                                    mode=authority.window_mode,
                                    role=role,
                                    block_sessions=block_sessions,
                                    offset_id=offset.offset_id,
                                    start_index=start_idx,
                                    end_index=end_idx,
                                    scenario_ids=scenario_ids[start_idx:end_idx],
                                )
                            )
                        iteration += 1
                        if authority.window_mode is WalkForwardWindowMode.ANCHORED:
                            growth += authority.step_size
                        else:
                            rolling_start += authority.step_size
        return windows

    def evaluate_horizon_discovery(
        self,
        *,
        report: ComparisonReport,
        authority: WalkForwardHarnessAuthorityPacket,
        generated_windows: list[WalkForwardWindowContract],
        scenarios: list[ReplayScenarioRecord],
    ) -> HorizonDiscoveryReport:
        """Evaluate generated windows against the frozen Gate 79 stability rules."""

        scenario_index = {scenario.scenario_id: scenario for scenario in scenarios}
        forward_windows = [
            window for window in generated_windows if window.role is WalkForwardWindowRole.FORWARD
        ]
        group_results: list[GroupReviewHorizonResult] = []
        unstable_keys: list[str] = []
        offset_sensitive_keys: list[str] = []
        report_level_economic_axis_failures: dict[str, list[str]] = {}
        for surface_key in authority.surface_keys:
            surface_windows = [
                window for window in forward_windows if window.surface_key == surface_key
            ]
            result = self._evaluate_surface_key(
                surface_key, surface_windows, report, authority.stability_rule
            )
            group_results.append(result)
            for note in result.notes:
                if note.startswith("economic_axis_failures:"):
                    axes = [axis for axis in note.split(":", 1)[1].split(",") if axis]
                    if axes:
                        report_level_economic_axis_failures[surface_key] = axes
            if result.outcome is HorizonDiscoveryOutcome.OFFSET_SENSITIVE:
                offset_sensitive_keys.append(surface_key)
            elif result.outcome is not HorizonDiscoveryOutcome.STABLE_HORIZON_FOUND:
                unstable_keys.append(surface_key)
        return HorizonDiscoveryReport(
            fixture_pack_id=report.fixture_pack_id,
            generated_windows=generated_windows,
            group_results=group_results,
            event_slice_reports=self._context_slice_reports(
                "event", forward_windows, scenario_index
            ),
            regime_slice_reports=self._context_slice_reports(
                "regime", forward_windows, scenario_index
            ),
            session_slice_reports=self._context_slice_reports(
                "session", forward_windows, scenario_index
            ),
            fragility=FragilitySignalReport(
                hidden_fragility_detected=bool(offset_sensitive_keys or unstable_keys),
                offset_sensitive_surface_keys=sorted(offset_sensitive_keys),
                unstable_surface_keys=sorted(unstable_keys),
                economic_axis_failures=report_level_economic_axis_failures,
                notes=["Harness outputs are bounded evidence surfaces, not promotion decisions."],
            ),
            ablation=self._ablation_report(report, report_level_economic_axis_failures),
            downstream_binding=authority.downstream_binding,
        )

    def _evaluate_surface_key(
        self,
        surface_key: str,
        windows: list[WalkForwardWindowContract],
        report: ComparisonReport,
        rule: StabilityComparisonRule,
    ) -> GroupReviewHorizonResult:
        block_groups: dict[int, list[WalkForwardWindowContract]] = defaultdict(list)
        for window in windows:
            block_groups[window.block_sessions].append(window)
        if not block_groups:
            return GroupReviewHorizonResult(
                surface_key=surface_key,
                outcome=HorizonDiscoveryOutcome.COVERAGE_INSUFFICIENT,
                offset_outcome=OffsetComparisonOutcome.FLAPPING,
                notes=["No generated forward windows were available for this surface."],
            )
        offset_sensitive_seen = False
        evaluated_window_ids: list[str] = []
        aggregated_economic_axes: set[str] = set()
        for block_sessions in sorted(block_groups):
            block_windows = block_groups[block_sessions]
            evaluated_window_ids.extend(window.window_id for window in block_windows)
            populated_windows = [
                window for window in block_windows if report.slice_reports.get(window.window_id)
            ]
            if len(populated_windows) < rule.minimum_forward_windows:
                continue
            offset_map: dict[str, list[WalkForwardWindowContract]] = defaultdict(list)
            for window in populated_windows:
                offset_map[window.offset_id].append(window)
            stable_offsets: list[str] = []
            unstable_offsets: list[str] = []
            offset_rankings: list[list[str]] = []
            any_metrics = False
            for offset_id, offset_windows in sorted(offset_map.items()):
                metrics_by_set = self._metrics_by_set(offset_windows, report)
                if not metrics_by_set:
                    unstable_offsets.append(offset_id)
                    continue
                any_metrics = True
                ranking = self._ranking_for_offset(metrics_by_set)
                offset_rankings.append(ranking)
                if self._metrics_are_stable(metrics_by_set, rule):
                    stable_offsets.append(offset_id)
                else:
                    unstable_offsets.append(offset_id)
            if not any_metrics:
                continue
            ranking_consistent = len({tuple(ranking) for ranking in offset_rankings}) <= 1
            decision_consistent = len(unstable_offsets) == 0
            economic_axis_failures = self._economic_axis_failures(block_windows, report, rule)
            aggregated_economic_axes.update(
                axis for axes in economic_axis_failures.values() for axis in axes
            )
            economic_consistent = not economic_axis_failures
            if (
                stable_offsets
                and ranking_consistent
                and decision_consistent
                and economic_consistent
            ):
                return GroupReviewHorizonResult(
                    surface_key=surface_key,
                    outcome=HorizonDiscoveryOutcome.STABLE_HORIZON_FOUND,
                    smallest_stable_forward_block=block_sessions,
                    evaluated_window_ids=evaluated_window_ids,
                    stable_offset_ids=stable_offsets,
                    unstable_offset_ids=unstable_offsets,
                    offset_outcome=OffsetComparisonOutcome.CONSISTENT,
                    ranking_consistent=ranking_consistent,
                    decision_distribution_consistent=decision_consistent,
                    economic_behaviour_consistent=economic_consistent,
                    notes=["Smallest chronology-safe stable block found."],
                )
            if stable_offsets and not ranking_consistent:
                offset_sensitive_seen = True
        outcome = (
            HorizonDiscoveryOutcome.OFFSET_SENSITIVE
            if offset_sensitive_seen
            else HorizonDiscoveryOutcome.NO_STABLE_HORIZON_FOUND
        )
        offset_outcome = (
            OffsetComparisonOutcome.OFFSET_SENSITIVE
            if offset_sensitive_seen
            else OffsetComparisonOutcome.FLAPPING
        )
        if all(
            len([window for window in group if report.slice_reports.get(window.window_id)])
            < rule.minimum_forward_windows
            for group in block_groups.values()
        ):
            outcome = HorizonDiscoveryOutcome.COVERAGE_INSUFFICIENT
            offset_outcome = OffsetComparisonOutcome.FLAPPING
        final_notes = ["No stable horizon met the frozen Gate 79 comparison rules."]
        if aggregated_economic_axes:
            final_notes.append(
                f"economic_axis_failures:{','.join(sorted(aggregated_economic_axes))}"
            )
        return GroupReviewHorizonResult(
            surface_key=surface_key,
            outcome=outcome,
            evaluated_window_ids=evaluated_window_ids,
            offset_outcome=offset_outcome,
            ranking_consistent=False,
            decision_distribution_consistent=False,
            economic_behaviour_consistent=False,
            notes=final_notes,
        )

    def _metrics_by_set(
        self,
        windows: list[WalkForwardWindowContract],
        report: ComparisonReport,
    ) -> dict[str, list[ComparisonMetrics]]:
        metrics: dict[str, list[ComparisonMetrics]] = defaultdict(list)
        for window in windows:
            slice_metrics = report.slice_reports.get(window.window_id, {})
            for set_id, summary in slice_metrics.items():
                metrics[set_id].append(summary)
        return dict(metrics)

    def _metrics_are_stable(
        self,
        metrics_by_set: dict[str, list[ComparisonMetrics]],
        rule: StabilityComparisonRule,
    ) -> bool:
        for summaries in metrics_by_set.values():
            if not summaries:
                return False
            replay_spread = max(item.mean_replay_score for item in summaries) - min(
                item.mean_replay_score for item in summaries
            )
            veto_spread = max(item.veto_correctness_rate for item in summaries) - min(
                item.veto_correctness_rate for item in summaries
            )
            playbook_spread = max(item.mean_playbook_precision for item in summaries) - min(
                item.mean_playbook_precision for item in summaries
            )
            fresh_spread = max(item.mean_fresh_deployable_pct for item in summaries) - min(
                item.mean_fresh_deployable_pct for item in summaries
            )
            if replay_spread > rule.max_replay_score_spread:
                return False
            if veto_spread > rule.max_veto_correctness_spread:
                return False
            if playbook_spread > rule.max_playbook_precision_spread:
                return False
            if fresh_spread > rule.max_fresh_deployable_spread:
                return False
            if (
                min(item.review_completeness_rate for item in summaries)
                < rule.min_review_completeness_rate
            ):
                return False
        return True

    def _ranking_for_offset(self, metrics_by_set: dict[str, list[ComparisonMetrics]]) -> list[str]:
        ranked = []
        for set_id, summaries in metrics_by_set.items():
            mean_score = sum(item.mean_replay_score for item in summaries) / len(summaries)
            ranked.append((set_id, mean_score))
        return [set_id for set_id, _score in sorted(ranked, key=lambda item: (-item[1], item[0]))]

    def _economic_axis_failures(
        self,
        windows: list[WalkForwardWindowContract],
        report: ComparisonReport,
        rule: StabilityComparisonRule,
    ) -> dict[str, list[str]]:
        failures: dict[str, list[str]] = {}
        for window in windows:
            slice_metrics = report.slice_reports.get(window.window_id, {})
            if not slice_metrics:
                continue
            window_failures: list[str] = []
            values = list(slice_metrics.values())
            fresh_spread = max(metric.mean_fresh_deployable_pct for metric in values) - min(
                metric.mean_fresh_deployable_pct for metric in values
            )
            if fresh_spread > rule.max_fresh_deployable_spread:
                window_failures.append("fresh_deployable_spread")
            active_playbook_spread = max(metric.active_playbook_rate for metric in values) - min(
                metric.active_playbook_rate for metric in values
            )
            if active_playbook_spread > rule.max_active_playbook_rate_spread:
                window_failures.append("active_playbook_rate_spread")
            conflict_spread = max(metric.mean_conflict_count for metric in values) - min(
                metric.mean_conflict_count for metric in values
            )
            if conflict_spread > rule.max_conflict_count_spread:
                window_failures.append("conflict_count_spread")
            if (
                min(metric.review_completeness_rate for metric in values)
                < rule.min_review_completeness_rate
            ):
                window_failures.append("review_completeness_floor")
            if window_failures:
                failures[window.window_id] = window_failures
        return failures

    def _economic_behaviour_consistent(
        self,
        windows: list[WalkForwardWindowContract],
        report: ComparisonReport,
        rule: StabilityComparisonRule,
    ) -> bool:
        return not self._economic_axis_failures(windows, report, rule)

    def _context_slice_reports(
        self,
        dimension: str,
        windows: list[WalkForwardWindowContract],
        scenario_index: dict[str, ReplayScenarioRecord],
    ) -> list[ContextSliceReport]:
        scenario_counter: Counter[str] = Counter()
        window_counter: Counter[str] = Counter()
        for window in windows:
            labels = set()
            for scenario_id in window.scenario_ids:
                scenario = scenario_index[scenario_id]
                labels_for_scenario = self._labels_for_dimension(dimension, scenario)
                for label in labels_for_scenario:
                    scenario_counter[label] += 1
                    labels.add(label)
            for label in labels:
                window_counter[label] += 1
        return [
            ContextSliceReport(
                dimension=dimension,
                label=label,
                scenario_count=scenario_counter[label],
                window_count=window_counter[label],
            )
            for label in sorted(scenario_counter)
        ]

    def _labels_for_dimension(self, dimension: str, scenario: ReplayScenarioRecord) -> list[str]:
        payload = scenario.payload
        if dimension == "event":
            if payload.get("event_slice"):
                return [str(payload["event_slice"])]
            return ["event_adjacent" if payload.get("next_event_at") else "no_event"]
        if dimension == "regime":
            if payload.get("regime_slice"):
                return [str(payload["regime_slice"])]
            breadth = self._get_float(payload, "breadth_score", 0.0)
            return ["broad_risk_on" if breadth >= 0 else "broad_risk_off"]
        if payload.get("session_slice"):
            return [str(payload["session_slice"])]
        ts = self._coerce_datetime(payload["ts"])
        return ["core_session" if 13 <= ts.hour <= 20 else "other_session"]

    def _ablation_report(
        self,
        report: ComparisonReport,
        economic_axis_failures: dict[str, list[str]] | None = None,
    ) -> AblationSignalReport:
        zero_activity_sets = [
            set_id
            for set_id, metrics in report.reports.items()
            if metrics.active_playbook_rate == 0.0
        ]
        notes = []
        if zero_activity_sets:
            notes.append(
                "Sets with zero active-playbook rate across the harness may indicate missing-module or over-pruning suspicion."
            )
        if economic_axis_failures:
            notes.append(
                "Economic axis failures are compact review-safe hints, not promotion decisions."
            )
        return AblationSignalReport(
            suspected_missing_modules=sorted(zero_activity_sets),
            pruning_candidates=sorted(zero_activity_sets),
            economic_axis_failures=(
                {} if economic_axis_failures is None else economic_axis_failures
            ),
            notes=notes,
        )
