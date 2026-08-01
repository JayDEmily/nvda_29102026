"""Deterministic signal-informed intraday phase authority.

The evaluator is pure. Session-scoped state is owned by an injected repository
and remains explicitly process-memory bounded in the alpha implementation.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

PhaseAuthorityState = Literal[
    "signal_informed",
    "market_structure_authoritative",
    "clock_only_degraded",
    "held_degraded",
    "corrected",
]


class IntradayPhase(StrEnum):
    PRE_OPEN = "pre_open"
    OPENING_PRICE_DISCOVERY = "opening_price_discovery"
    OPENING_TRANSITION = "opening_transition"
    CONTINUOUS_SESSION = "continuous_session"
    CLOSING_TRANSITION = "closing_transition"
    CLOSING_AUCTION = "closing_auction"
    POST_CLOSE = "post_close"
    UNRESOLVED = "unresolved"


_ORDERED_PHASES: tuple[IntradayPhase, ...] = (
    IntradayPhase.PRE_OPEN,
    IntradayPhase.OPENING_PRICE_DISCOVERY,
    IntradayPhase.OPENING_TRANSITION,
    IntradayPhase.CONTINUOUS_SESSION,
    IntradayPhase.CLOSING_TRANSITION,
    IntradayPhase.CLOSING_AUCTION,
    IntradayPhase.POST_CLOSE,
)
_PHASE_INDEX = {phase: index for index, phase in enumerate(_ORDERED_PHASES)}


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, BaseModel):
        return _canonical(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    if isinstance(value, StrEnum):
        return value.value
    return value


def semantic_fingerprint(value: Any) -> str:
    payload = json.dumps(_canonical(value), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


def _require_hash(value: str, reason: str) -> str:
    if len(value) != 64:
        raise ValueError(reason)
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(reason) from exc
    return value


def _require_text(value: str | None, reason: str) -> str:
    if value is None or not value.strip():
        raise ValueError(reason)
    return value


class IntradayPhaseEvidence(BaseModel):
    """One immutable, typed observation set offered to phase evaluation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    evidence_id: str
    source_time_utc: datetime
    session_reference_id: str
    activity_participation_signal: str | None
    liquidity_signal: str | None
    price_discovery_signal: str | None
    market_structure_status: str | None
    evidence_fingerprint: str
    signal_observed_at_utc: datetime | None = None
    source_capture_ids: tuple[str, ...] = ()
    schema_version: str = "intraday-phase-evidence.1.0.0"
    derivation_version: str = "signal-state.1.0.0"
    authoritative_correction: bool = False
    correction_reason: str | None = None

    @field_validator("source_time_utc", "signal_observed_at_utc")
    @classmethod
    def _aware_time(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("phase_evidence_time_must_be_timezone_aware")
        return value

    @model_validator(mode="after")
    def _validate_law(self) -> "IntradayPhaseEvidence":
        for value, reason in (
            (self.evidence_id, "phase_evidence_id_required"),
            (self.session_reference_id, "phase_session_reference_required"),
            (self.schema_version, "phase_evidence_schema_version_required"),
            (self.derivation_version, "phase_evidence_derivation_version_required"),
        ):
            _require_text(value, reason)
        _require_hash(self.evidence_fingerprint, "phase_evidence_fingerprint_invalid")
        for value in (
            self.activity_participation_signal,
            self.liquidity_signal,
            self.price_discovery_signal,
            self.market_structure_status,
        ):
            if value is not None and not value.strip():
                raise ValueError("phase_signal_state_must_be_nonempty")
        if len(self.source_capture_ids) != len(set(self.source_capture_ids)) or any(
            not item for item in self.source_capture_ids
        ):
            raise ValueError("phase_source_capture_ids_invalid")
        if self.signal_observed_at_utc and self.signal_observed_at_utc > self.source_time_utc:
            raise ValueError("phase_signal_observed_after_source_time")
        if self.authoritative_correction != (self.correction_reason is not None):
            raise ValueError("phase_correction_reason_law_invalid")
        return self


class IntradayPhasePolicy(BaseModel):
    """Versioned transition, freshness and anti-chatter policy."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    policy_version: str
    minimum_dwell_observations: int
    regression_confirmation_observations: int = 2
    max_signal_age_seconds: int = 120
    contract_version: str = "intraday-phase-policy.1.0.0"

    @model_validator(mode="after")
    def _validate_law(self) -> "IntradayPhasePolicy":
        _require_text(self.policy_version, "phase_policy_version_required")
        _require_text(self.contract_version, "phase_policy_contract_version_required")
        if self.minimum_dwell_observations < 1:
            raise ValueError("minimum_dwell_observations_must_be_positive")
        if self.regression_confirmation_observations < 1:
            raise ValueError("regression_confirmation_observations_must_be_positive")
        if self.max_signal_age_seconds < 0:
            raise ValueError("max_signal_age_seconds_must_be_nonnegative")
        return self


class IntradayPhaseState(BaseModel):
    """One accepted session-scoped phase-state snapshot."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    state_id: str
    session_reference_id: str
    phase: IntradayPhase
    state_version: int
    accepted_at_utc: datetime
    evidence_id: str
    evidence_fingerprint: str
    policy_version: str
    pending_phase: IntradayPhase | None = None
    pending_observation_count: int = 0
    superseded_state_id: str | None = None
    semantic_fingerprint: str

    @classmethod
    def create(
        cls,
        *,
        session_reference_id: str,
        phase: IntradayPhase,
        state_version: int,
        accepted_at_utc: datetime,
        evidence_id: str,
        evidence_fingerprint: str,
        policy_version: str,
        pending_phase: IntradayPhase | None = None,
        pending_observation_count: int = 0,
        superseded_state_id: str | None = None,
    ) -> "IntradayPhaseState":
        material = {
            "session_reference_id": session_reference_id,
            "phase": phase,
            "state_version": state_version,
            "accepted_at_utc": accepted_at_utc,
            "evidence_id": evidence_id,
            "evidence_fingerprint": evidence_fingerprint,
            "policy_version": policy_version,
            "pending_phase": pending_phase,
            "pending_observation_count": pending_observation_count,
            "superseded_state_id": superseded_state_id,
        }
        fingerprint = semantic_fingerprint(material)
        return cls(
            state_id=f"phase-state.{fingerprint[:16]}",
            semantic_fingerprint=fingerprint,
            **material,
        )

    @field_validator("accepted_at_utc")
    @classmethod
    def _accepted_time_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("phase_state_time_must_be_timezone_aware")
        return value

    @model_validator(mode="after")
    def _validate_law(self) -> "IntradayPhaseState":
        if self.phase is IntradayPhase.UNRESOLVED:
            raise ValueError("accepted_phase_state_cannot_be_unresolved")
        if self.state_version < 1:
            raise ValueError("phase_state_version_must_be_positive")
        if self.pending_observation_count < 0:
            raise ValueError("phase_pending_count_invalid")
        if (self.pending_phase is None) != (self.pending_observation_count == 0):
            raise ValueError("phase_pending_state_incomplete")
        _require_hash(self.evidence_fingerprint, "phase_state_evidence_fingerprint_invalid")
        material = self.model_dump(mode="python")
        material.pop("state_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("phase_state_fingerprint_mismatch")
        if self.state_id != f"phase-state.{expected[:16]}":
            raise ValueError("phase_state_identity_mismatch")
        return self


class IntradayPhaseResult(BaseModel):
    """One deterministic phase evaluation result and accepted next state."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    result_id: str
    contract_version: str = "intraday-phase-result.1.0.0"
    phase: IntradayPhase
    clock_prior: str
    authority_state: PhaseAuthorityState
    source_time_utc: datetime
    session_reference_id: str
    evidence_id: str
    evidence_fingerprint: str
    policy_version: str
    state_version: int
    accepted_state_id: str | None
    pending_phase: IntradayPhase | None = None
    pending_observation_count: int = 0
    superseded_state_id: str | None = None
    transition_reason: str
    contributing_signal_states: tuple[tuple[str, str], ...]
    limitations: tuple[str, ...] = ()
    positive_permission: bool = False
    semantic_fingerprint: str

    @field_validator("source_time_utc")
    @classmethod
    def _source_time_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("phase_result_time_must_be_timezone_aware")
        return value

    @model_validator(mode="after")
    def _validate_law(self) -> "IntradayPhaseResult":
        if self.state_version < 1:
            raise ValueError("phase_result_state_version_must_be_positive")
        _require_hash(self.evidence_fingerprint, "phase_result_evidence_fingerprint_invalid")
        if len(self.contributing_signal_states) != len(set(self.contributing_signal_states)):
            raise ValueError("phase_result_signal_lineage_duplicate")
        if self.phase is IntradayPhase.UNRESOLVED and self.accepted_state_id is not None:
            raise ValueError("unresolved_phase_cannot_bind_accepted_state")
        if self.phase is not IntradayPhase.UNRESOLVED and self.accepted_state_id is None:
            raise ValueError("resolved_phase_requires_accepted_state")
        if (
            self.authority_state in {"clock_only_degraded", "held_degraded"}
            and self.positive_permission
        ):
            raise ValueError("degraded_phase_cannot_grant_positive_permission")
        material = self.model_dump(mode="python")
        material.pop("result_id")
        material.pop("semantic_fingerprint")
        expected = semantic_fingerprint(material)
        if self.semantic_fingerprint != expected:
            raise ValueError("phase_result_fingerprint_mismatch")
        if self.result_id != f"phase-result.{expected[:16]}":
            raise ValueError("phase_result_identity_mismatch")
        return self

    def to_state(self) -> IntradayPhaseState | None:
        if self.phase is IntradayPhase.UNRESOLVED:
            return None
        return IntradayPhaseState.create(
            session_reference_id=self.session_reference_id,
            phase=self.phase,
            state_version=self.state_version,
            accepted_at_utc=self.source_time_utc,
            evidence_id=self.evidence_id,
            evidence_fingerprint=self.evidence_fingerprint,
            policy_version=self.policy_version,
            pending_phase=self.pending_phase,
            pending_observation_count=self.pending_observation_count,
            superseded_state_id=self.superseded_state_id,
        )


@runtime_checkable
class IntradayPhaseRepository(Protocol):
    """Session-scoped phase state port; durability is implementation-specific."""

    def load(self, session_reference_id: str) -> IntradayPhaseState | None: ...

    def save(self, state: IntradayPhaseState) -> None: ...

    def history(self, session_reference_id: str) -> tuple[IntradayPhaseState, ...]: ...


class InMemoryIntradayPhaseRepository:
    """Copy-safe process-memory alpha repository; not restart durable."""

    def __init__(self, *, max_history: int = 32) -> None:
        if max_history < 1:
            raise ValueError("phase_history_bound_must_be_positive")
        self._max_history = max_history
        self._states: dict[str, IntradayPhaseState] = {}
        self._history: dict[str, list[IntradayPhaseState]] = {}

    @staticmethod
    def _copy(state: IntradayPhaseState) -> IntradayPhaseState:
        return IntradayPhaseState.model_validate(state.model_dump(mode="python"))

    def load(self, session_reference_id: str) -> IntradayPhaseState | None:
        state = self._states.get(session_reference_id)
        return None if state is None else self._copy(state)

    def save(self, state: IntradayPhaseState) -> None:
        detached = self._copy(state)
        current = self._states.get(state.session_reference_id)
        if current and state.state_version <= current.state_version:
            raise ValueError("phase_state_version_not_monotonic")
        self._states[state.session_reference_id] = detached
        items = self._history.setdefault(state.session_reference_id, [])
        items.append(detached)
        del items[: -self._max_history]

    def history(self, session_reference_id: str) -> tuple[IntradayPhaseState, ...]:
        return tuple(self._copy(item) for item in self._history.get(session_reference_id, ()))


class IntradayPhaseEvaluator:
    """Pure versioned signal-state evaluator with monotonic transition law."""

    def __init__(self, *, policy: IntradayPhasePolicy) -> None:
        self.policy = IntradayPhasePolicy.model_validate(policy.model_dump(mode="python"))

    def evaluate(
        self,
        *,
        evidence: IntradayPhaseEvidence,
        prior_state: IntradayPhaseState | None,
    ) -> IntradayPhaseResult:
        evidence = IntradayPhaseEvidence.model_validate(evidence.model_dump(mode="python"))
        prior = (
            None
            if prior_state is None
            else IntradayPhaseState.model_validate(prior_state.model_dump(mode="python"))
        )
        if prior is not None and prior.session_reference_id != evidence.session_reference_id:
            raise ValueError("phase_prior_session_mismatch")
        if prior is not None and prior.policy_version != self.policy.policy_version:
            raise ValueError("phase_prior_policy_version_mismatch")

        clock_prior = self._clock_prior(evidence)
        observed_at = evidence.signal_observed_at_utc or evidence.source_time_utc
        age = (evidence.source_time_utc - observed_at).total_seconds()
        stale = age > self.policy.max_signal_age_seconds
        core = (
            evidence.activity_participation_signal,
            evidence.liquidity_signal,
            evidence.price_discovery_signal,
        )
        missing = any(value is None for value in core)
        next_version = 1 if prior is None else prior.state_version + 1

        if stale or missing:
            limitations = (
                "behavioural_signals_stale" if stale else "behavioural_signal_families_missing",
            )
            if prior is None:
                return self._build_result(
                    phase=IntradayPhase.UNRESOLVED,
                    authority_state="clock_only_degraded",
                    evidence=evidence,
                    clock_prior=clock_prior,
                    state_version=next_version,
                    accepted_state_id=None,
                    transition_reason="behavioural_authority_unavailable",
                    limitations=limitations,
                    contributing=self._signal_lineage(evidence),
                    positive_permission=False,
                )
            return self._build_result(
                phase=prior.phase,
                authority_state="held_degraded",
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id="pending",
                pending_phase=prior.pending_phase,
                pending_observation_count=prior.pending_observation_count,
                transition_reason="prior_phase_held_for_degraded_evidence",
                limitations=limitations,
                contributing=self._signal_lineage(evidence),
                positive_permission=False,
            )

        proposed, structure_authoritative = self._propose(evidence)
        if proposed is IntradayPhase.UNRESOLVED:
            return self._build_result(
                phase=IntradayPhase.UNRESOLVED,
                authority_state="clock_only_degraded",
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id=None,
                transition_reason="signal_combination_unresolved",
                limitations=("signal_combination_unresolved",),
                contributing=self._signal_lineage(evidence),
                positive_permission=False,
            )

        if prior is None:
            authority: PhaseAuthorityState = (
                "market_structure_authoritative" if structure_authoritative else "signal_informed"
            )
            return self._build_result(
                phase=proposed,
                authority_state=authority,
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id="pending",
                transition_reason="initial_signal_informed_classification",
                contributing=self._signal_lineage(evidence),
                positive_permission=True,
            )

        if proposed is prior.phase:
            return self._build_result(
                phase=prior.phase,
                authority_state=(
                    "market_structure_authoritative"
                    if structure_authoritative
                    else "signal_informed"
                ),
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id="pending",
                transition_reason="phase_sustained",
                contributing=self._signal_lineage(evidence),
                positive_permission=True,
            )

        prior_index = _PHASE_INDEX[prior.phase]
        proposed_index = _PHASE_INDEX[proposed]
        if proposed_index < prior_index:
            if not evidence.authoritative_correction:
                return self._build_result(
                    phase=prior.phase,
                    authority_state="held_degraded",
                    evidence=evidence,
                    clock_prior=clock_prior,
                    state_version=next_version,
                    accepted_state_id="pending",
                    transition_reason="regression_withheld_without_authoritative_correction",
                    limitations=("apparent_phase_regression",),
                    contributing=self._signal_lineage(evidence),
                    positive_permission=False,
                )
            return self._build_result(
                phase=proposed,
                authority_state="corrected",
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id="pending",
                superseded_state_id=prior.state_id,
                transition_reason="authoritative_sequence_correction",
                contributing=self._signal_lineage(evidence),
                positive_permission=True,
            )

        # Do not skip normal intermediate behavioural states.
        target = _ORDERED_PHASES[min(prior_index + 1, proposed_index)]
        count = prior.pending_observation_count + 1 if prior.pending_phase is target else 1
        if structure_authoritative or count >= self.policy.minimum_dwell_observations:
            return self._build_result(
                phase=target,
                authority_state=(
                    "market_structure_authoritative"
                    if structure_authoritative
                    else "signal_informed"
                ),
                evidence=evidence,
                clock_prior=clock_prior,
                state_version=next_version,
                accepted_state_id="pending",
                transition_reason="sustained_forward_transition",
                contributing=self._signal_lineage(evidence),
                positive_permission=True,
            )
        return self._build_result(
            phase=prior.phase,
            authority_state="held_degraded",
            evidence=evidence,
            clock_prior=clock_prior,
            state_version=next_version,
            accepted_state_id="pending",
            pending_phase=target,
            pending_observation_count=count,
            transition_reason="minimum_dwell_not_met",
            limitations=("transition_pending_hysteresis",),
            contributing=self._signal_lineage(evidence),
            positive_permission=False,
        )

    @staticmethod
    def _clock_prior(evidence: IntradayPhaseEvidence) -> str:
        status = (evidence.market_structure_status or "unknown").lower()
        if status in {"pre_open", "opening_auction", "closing_auction", "post_close", "closed"}:
            return status
        return "continuous_session_window"

    @staticmethod
    def _propose(evidence: IntradayPhaseEvidence) -> tuple[IntradayPhase, bool]:
        status = (evidence.market_structure_status or "").lower()
        authoritative = {
            "pre_open": IntradayPhase.PRE_OPEN,
            "opening_auction": IntradayPhase.OPENING_PRICE_DISCOVERY,
            "closing_auction": IntradayPhase.CLOSING_AUCTION,
            "post_close": IntradayPhase.POST_CLOSE,
            "closed": IntradayPhase.POST_CLOSE,
        }
        if status in authoritative:
            return authoritative[status], True

        activity = (evidence.activity_participation_signal or "").lower()
        liquidity = (evidence.liquidity_signal or "").lower()
        discovery = (evidence.price_discovery_signal or "").lower()
        if (
            activity in {"unstable_high", "opening_intense", "surging"}
            or liquidity in {"thin_widening", "unstable", "dislocated"}
            or discovery in {"unstable", "forming", "high"}
        ):
            return IntradayPhase.OPENING_PRICE_DISCOVERY, False
        if (
            activity in {"fading", "closing_build", "auction_build"}
            or liquidity in {"thinning", "closing", "auction"}
            or discovery in {"closing", "reopening", "auction"}
        ):
            return IntradayPhase.CLOSING_TRANSITION, False
        if (
            activity in {"broad_stable", "normal", "steady"}
            and liquidity in {"stable", "normal", "deep"}
            and discovery in {"settled", "stable", "normal"}
        ):
            return IntradayPhase.CONTINUOUS_SESSION, False
        if (
            activity in {"stabilising", "moderating"}
            and liquidity in {"improving", "normalising"}
            and discovery in {"stabilising", "moderating"}
        ):
            return IntradayPhase.OPENING_TRANSITION, False
        return IntradayPhase.UNRESOLVED, False

    @staticmethod
    def _signal_lineage(evidence: IntradayPhaseEvidence) -> tuple[tuple[str, str], ...]:
        values = {
            "activity_participation": evidence.activity_participation_signal or "missing",
            "liquidity": evidence.liquidity_signal or "missing",
            "market_structure": evidence.market_structure_status or "missing",
            "price_discovery": evidence.price_discovery_signal or "missing",
        }
        return tuple(sorted(values.items()))

    def _build_result(
        self,
        *,
        phase: IntradayPhase,
        authority_state: PhaseAuthorityState,
        evidence: IntradayPhaseEvidence,
        clock_prior: str,
        state_version: int,
        accepted_state_id: str | None,
        transition_reason: str,
        contributing: tuple[tuple[str, str], ...],
        pending_phase: IntradayPhase | None = None,
        pending_observation_count: int = 0,
        superseded_state_id: str | None = None,
        limitations: tuple[str, ...] = (),
        positive_permission: bool,
    ) -> IntradayPhaseResult:
        if accepted_state_id == "pending":
            state = IntradayPhaseState.create(
                session_reference_id=evidence.session_reference_id,
                phase=phase,
                state_version=state_version,
                accepted_at_utc=evidence.source_time_utc,
                evidence_id=evidence.evidence_id,
                evidence_fingerprint=evidence.evidence_fingerprint,
                policy_version=self.policy.policy_version,
                pending_phase=pending_phase,
                pending_observation_count=pending_observation_count,
                superseded_state_id=superseded_state_id,
            )
            accepted_state_id = state.state_id
        material: dict[str, Any] = {
            "contract_version": "intraday-phase-result.1.0.0",
            "phase": phase,
            "clock_prior": clock_prior,
            "authority_state": authority_state,
            "source_time_utc": evidence.source_time_utc,
            "session_reference_id": evidence.session_reference_id,
            "evidence_id": evidence.evidence_id,
            "evidence_fingerprint": evidence.evidence_fingerprint,
            "policy_version": self.policy.policy_version,
            "state_version": state_version,
            "accepted_state_id": accepted_state_id,
            "pending_phase": pending_phase,
            "pending_observation_count": pending_observation_count,
            "superseded_state_id": superseded_state_id,
            "transition_reason": transition_reason,
            "contributing_signal_states": contributing,
            "limitations": limitations,
            "positive_permission": positive_permission,
        }
        fingerprint = semantic_fingerprint(material)
        return IntradayPhaseResult(
            result_id=f"phase-result.{fingerprint[:16]}",
            semantic_fingerprint=fingerprint,
            **material,
        )
