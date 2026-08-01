"""M05 proof for the typed signal-informed temporal authority boundary."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from tests.support.m05_k08_k09_contract_harness import (
    production_context_payload,
    valid_context,
)

from nvda_desk.domain.temporal.intraday_phase import (
    InMemoryIntradayPhaseRepository,
    IntradayPhase,
    IntradayPhaseEvaluator,
    IntradayPhaseEvidence,
    IntradayPhasePolicy,
    IntradayPhaseState,
)
from nvda_desk.m05_serial_cognition import StageContext, TemporalStageAdapter

NOW = datetime(2026, 7, 31, 14, 0, tzinfo=UTC)
HASH_A = "a" * 64
HASH_B = "b" * 64


def evidence(
    identity: str,
    *,
    activity: str | None = "broad_stable",
    liquidity: str | None = "stable",
    discovery: str | None = "settled",
    structure: str | None = "continuous_trading",
    observed_at: datetime | None = None,
    correction: bool = False,
) -> IntradayPhaseEvidence:
    return IntradayPhaseEvidence(
        evidence_id=identity,
        source_time_utc=NOW,
        signal_observed_at_utc=observed_at or NOW,
        session_reference_id="session-1",
        activity_participation_signal=activity,
        liquidity_signal=liquidity,
        price_discovery_signal=discovery,
        market_structure_status=structure,
        evidence_fingerprint=HASH_A if identity.endswith("a") else HASH_B,
        authoritative_correction=correction,
        correction_reason="venue_status_corrected" if correction else None,
    )


def policy(**updates: object) -> IntradayPhasePolicy:
    values: dict[str, object] = {
        "policy_version": "phase-v1",
        "minimum_dwell_observations": 1,
        "regression_confirmation_observations": 2,
        "max_signal_age_seconds": 120,
    }
    values.update(updates)
    return IntradayPhasePolicy(**values)


def state(phase: IntradayPhase, *, version: int = 1) -> IntradayPhaseState:
    return IntradayPhaseState.create(
        session_reference_id="session-1",
        phase=phase,
        state_version=version,
        accepted_at_utc=NOW - timedelta(minutes=5),
        evidence_id="prior-evidence",
        evidence_fingerprint=HASH_A,
        policy_version="phase-v1",
    )


def test_same_clock_uses_sustained_signal_meaning_not_wall_clock() -> None:
    evaluator = IntradayPhaseEvaluator(policy=policy())
    discovery = evaluator.evaluate(
        evidence=evidence(
            "evidence-a",
            activity="unstable_high",
            liquidity="thin_widening",
            discovery="unstable",
        ),
        prior_state=None,
    )
    settled = evaluator.evaluate(evidence=evidence("evidence-b"), prior_state=None)

    assert discovery.source_time_utc == settled.source_time_utc == NOW
    assert discovery.phase is IntradayPhase.OPENING_PRICE_DISCOVERY
    assert settled.phase is IntradayPhase.CONTINUOUS_SESSION
    assert discovery.semantic_fingerprint != settled.semantic_fingerprint


def test_clock_only_is_unresolved_and_never_positive_permission() -> None:
    result = IntradayPhaseEvaluator(policy=policy()).evaluate(
        evidence=evidence(
            "clock-a",
            activity=None,
            liquidity=None,
            discovery=None,
        ),
        prior_state=None,
    )

    assert result.phase is IntradayPhase.UNRESOLVED
    assert result.authority_state == "clock_only_degraded"
    assert result.positive_permission is False
    assert "behavioural_signal_families_missing" in result.limitations


def test_minimum_dwell_and_hysteresis_prevent_single_observation_transition() -> None:
    evaluator = IntradayPhaseEvaluator(policy=policy(minimum_dwell_observations=2))
    first = evaluator.evaluate(
        evidence=evidence("settled-a"),
        prior_state=state(IntradayPhase.OPENING_PRICE_DISCOVERY),
    )
    second = evaluator.evaluate(
        evidence=evidence("settled-b"),
        prior_state=first.to_state(),
    )

    assert first.phase is IntradayPhase.OPENING_PRICE_DISCOVERY
    assert first.authority_state == "held_degraded"
    assert first.pending_phase is IntradayPhase.OPENING_TRANSITION
    assert first.pending_observation_count == 1
    assert second.phase is IntradayPhase.OPENING_TRANSITION
    assert second.pending_phase is None


def test_noisy_regression_is_held_without_authoritative_correction() -> None:
    result = IntradayPhaseEvaluator(policy=policy()).evaluate(
        evidence=evidence(
            "noise-a",
            activity="unstable_high",
            liquidity="thin_widening",
            discovery="unstable",
        ),
        prior_state=state(IntradayPhase.CONTINUOUS_SESSION),
    )

    assert result.phase is IntradayPhase.CONTINUOUS_SESSION
    assert result.authority_state == "held_degraded"
    assert result.positive_permission is False
    assert result.superseded_state_id is None


def test_authoritative_correction_preserves_superseded_state_lineage() -> None:
    prior = state(IntradayPhase.CONTINUOUS_SESSION)
    result = IntradayPhaseEvaluator(policy=policy()).evaluate(
        evidence=evidence(
            "correction-a",
            activity="unstable_high",
            liquidity="thin_widening",
            discovery="unstable",
            correction=True,
        ),
        prior_state=prior,
    )

    assert result.phase is IntradayPhase.OPENING_PRICE_DISCOVERY
    assert result.authority_state == "corrected"
    assert result.superseded_state_id == prior.state_id
    assert result.transition_reason == "authoritative_sequence_correction"


def test_stale_signals_fail_closed_and_replay_is_deterministic() -> None:
    evaluator = IntradayPhaseEvaluator(policy=policy(max_signal_age_seconds=30))
    stale = evidence("stale-a", observed_at=NOW - timedelta(minutes=10))
    first = evaluator.evaluate(evidence=stale, prior_state=None)
    second = evaluator.evaluate(evidence=stale, prior_state=None)

    assert first == second
    assert first.phase is IntradayPhase.UNRESOLVED
    assert first.authority_state == "clock_only_degraded"
    assert first.positive_permission is False
    assert "behavioural_signals_stale" in first.limitations


def test_repository_is_copy_safe_and_m05_adapter_carries_typed_authority() -> None:
    repository = InMemoryIntradayPhaseRepository()
    adapter = TemporalStageAdapter(
        evaluator=IntradayPhaseEvaluator(policy=policy()),
        repository=repository,
    )
    context = StageContext.model_validate(production_context_payload(valid_context()))

    result, stage_input = adapter.evaluate(
        evidence=evidence("adapter-a"),
        context=context,
    )
    loaded = repository.load("session-1")

    assert loaded == result.to_state()
    assert loaded is not result.to_state()
    assert stage_input.stage == "temporal"
    assert stage_input.missing_state is None
    assert {fact.fact_id for fact in stage_input.carrier_facts} == {
        "intraday_phase",
        "intraday_phase_authority_state",
        "intraday_phase_result_id",
        "intraday_phase_fingerprint",
        "intraday_phase_policy_version",
        "intraday_phase_state_version",
        "intraday_phase_positive_permission",
    }
    assert stage_input.authority_refs == (
        (
            "temporal_domain",
            result.result_id,
            result.contract_version,
            result.semantic_fingerprint,
        ),
    )
