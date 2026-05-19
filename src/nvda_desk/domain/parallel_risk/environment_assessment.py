"""Pure independent parallel-risk environment assessment."""

from __future__ import annotations

from nvda_desk.contracts.parallel_risk import (
    ParallelRiskEnvelope,
    ParallelRiskEnvelopeContribution,
    ParallelRiskEnvironmentAssessment,
    ParallelRiskPreparationPacket,
    ParallelRiskVixThresholdPolicy,
)
from nvda_desk.contracts.temporal import build_source_temporal_payload


def assess_environment(packet: ParallelRiskPreparationPacket) -> ParallelRiskEnvironmentAssessment:
    """Return one bounded environment assessment from the bootstrap temporal input."""

    temporal_input = packet.temporal_input
    window_ids = [window.event_id for window in temporal_input.windows]
    window_tags = sorted({tag for window in temporal_input.windows for tag in window.tags})
    notes = [
        "environment_assessment_only",
        "serial_spine_preserved",
        "stage_a_uses_module_8_bootstrap_input_only",
    ]
    if temporal_input.next_event_time_utc is None:
        notes.append("next_event_absent")
    return ParallelRiskEnvironmentAssessment(
        **build_source_temporal_payload(
            source_time_utc=temporal_input.source_time_utc,
            source_date=temporal_input.source_date,
            source_time_raw=temporal_input.source_time_raw,
            source_time_kind=temporal_input.source_time_kind,
            source_timezone_raw=temporal_input.source_timezone_raw,
            captured_at_utc=temporal_input.captured_at_utc,
            persisted_at_utc=temporal_input.persisted_at_utc,
            source_provider=temporal_input.source_provider,
            source_channel=temporal_input.source_channel,
            time_granularity=temporal_input.time_granularity,
        ),
        next_event_time_utc=temporal_input.next_event_time_utc,
        window_ids=window_ids,
        window_tags=window_tags,
        invariant_reads=list(packet.invariant_reads),
        notes=notes,
    )


DEFAULT_VIX_THRESHOLD_POLICY = ParallelRiskVixThresholdPolicy(
    policy_id="prl_vix_compatibility_legacy_30_50",
    mode="compatibility_legacy_30_50",
    caution_threshold=30.0,
    block_threshold=50.0,
    coefficient_authority_refs=[
        "config/coefficient_authority.v1.yaml#risk_vix_caution_threshold",
        "config/coefficient_authority.v1.yaml#risk_vix_hot_threshold",
    ],
    migration_status="explicit_compatibility_preserved_no_silent_change",
)


def assess_risk_envelope(
    packet: ParallelRiskPreparationPacket,
    *,
    vix_threshold_policy: ParallelRiskVixThresholdPolicy | None = None,
) -> ParallelRiskEnvelope:
    """Return the independent risk envelope from admitted parallel-risk primitives."""

    policy = vix_threshold_policy or DEFAULT_VIX_THRESHOLD_POLICY
    contributions: list[ParallelRiskEnvelopeContribution] = []
    caution_flags: list[str] = []
    hard_blocks: list[str] = []

    temporal_tags = {tag for window in packet.temporal_input.windows for tag in window.tags}
    if "scheduled_event_window_active" in temporal_tags:
        caution_flags.append("scheduled_event_window_active")
        contributions.append(
            ParallelRiskEnvelopeContribution(
                source_family="temporal_event_context",
                state="caution",
                reason="scheduled_event_window_active",
            )
        )

    if (
        packet.options_flow_input.front_dte is not None
        and packet.options_flow_input.next_dte is not None
        and packet.options_flow_input.front_dte > packet.options_flow_input.next_dte
    ):
        caution_flags.append("front_term_structure_backwardation")
        contributions.append(
            ParallelRiskEnvelopeContribution(
                source_family="options_repricing_context",
                state="caution",
                reason="front_term_structure_backwardation",
            )
        )

    vix_level = packet.regime_input.vix_level
    if vix_level is not None and vix_level >= policy.caution_threshold:
        caution_flags.append(policy.caution_flag)
        contributions.append(
            ParallelRiskEnvelopeContribution(
                source_family=policy.contribution_source_family,
                state=policy.contribution_state,
                reason=policy.caution_flag,
            )
        )
    if vix_level is not None and vix_level >= policy.block_threshold:
        hard_blocks.append(policy.block_flag)

    if hard_blocks:
        envelope_state = "block"
    elif caution_flags:
        envelope_state = "caution"
    elif contributions:
        envelope_state = "broad"
    else:
        envelope_state = "tight"

    return ParallelRiskEnvelope(
        envelope_state=envelope_state,
        contributions=contributions,
        hard_blocks=hard_blocks,
        caution_flags=caution_flags,
    )
