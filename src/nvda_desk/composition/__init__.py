"""A00 composition boundary for admitted runtime owners and technical mechanisms."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from nvda_desk.architecture.registry import ArchitectureRegistry
from nvda_desk.raw_signal_occurrence_truth.api import (
    CaptureReceiptEvidenceRelationV1,
    CaptureReceiptPresenceAssessmentV1,
    CaptureScopePolicyV1,
    RawObservationOccurrenceV1,
    ScheduledCaptureOccurrenceV1,
    create_owner,
)
from nvda_desk.raw_signal_occurrence_truth.api import (
    scope_policy_ref as make_scope_policy_ref,
)


@dataclass(frozen=True, slots=True)
class CompositionPlan:
    """Explicit list of active executable identities; never a service locator."""

    object_ids: tuple[str, ...]

    @classmethod
    def from_registry(cls, registry: ArchitectureRegistry) -> CompositionPlan:
        return cls(tuple(sorted(item.id for item in registry.objects if item.composable)))

    def require(self, registry: ArchitectureRegistry, object_id: str) -> None:
        registry.require_composable(object_id)
        if object_id not in self.object_ids:
            raise ValueError(f"{object_id} is not present in this composition plan")


_RawSignalOwnerFactory = Callable[..., Any]
_RawSignalEligibilityResolver = Callable[[RawObservationOccurrenceV1, CaptureScopePolicyV1], bool]


@dataclass(frozen=True, slots=True)
class RawSignalSequenceResult:
    """Exact M00 results returned from one governed A00 orchestration sequence."""

    policy: CaptureScopePolicyV1
    capture: ScheduledCaptureOccurrenceV1
    observation: RawObservationOccurrenceV1
    relation: CaptureReceiptEvidenceRelationV1 | None
    assessment: CaptureReceiptPresenceAssessmentV1
    readback: RawObservationOccurrenceV1 | None


@dataclass(frozen=True, slots=True)
class Application:
    """Top-level A00 application composition without Raw Signal semantic ownership."""

    __raw_signal_owner: Any

    def run_raw_signal_proof_sequence(
        self,
        *,
        capture_scope_policy: CaptureScopePolicyV1,
        scope_policy_ref: Any,
        slot_start_utc: datetime,
        capture_occurrence_id: Any,
        raw_observation: RawObservationOccurrenceV1,
        assessment_occurrence_id: Any,
        assessment_evidence_as_of_ts_utc: datetime,
        supersedes_assessment_ref: Any | None,
    ) -> RawSignalSequenceResult:
        """Orchestrate the authorised Raw Signal sequence through M00 only."""

        commands = self.__raw_signal_owner.commands
        reads = self.__raw_signal_owner.reads

        registered_policy = commands.register_capture_scope_policy(capture_scope_policy)
        authoritative_policy_ref = make_scope_policy_ref(
            f"{registered_policy.scope_policy_id.value}@{registered_policy.scope_policy_version}"
        )
        if scope_policy_ref != authoritative_policy_ref:
            raise ValueError("scope_policy_ref must identify the policy accepted for this sequence")

        capture = commands.realise_scheduled_capture_occurrence(
            scope_policy_ref=scope_policy_ref,
            slot_start_utc=slot_start_utc,
            capture_occurrence_id=capture_occurrence_id,
        )
        observation = commands.admit_raw_observation_occurrence(raw_observation)
        relation = commands.derive_capture_receipt_evidence_relation(
            observation_occurrence_ref=observation.observation_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            scope_policy_ref=capture.scope_policy_ref,
        )
        assessment = commands.append_capture_receipt_presence_assessment(
            assessment_occurrence_id=assessment_occurrence_id,
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=assessment_evidence_as_of_ts_utc,
            supersedes_assessment_ref=supersedes_assessment_ref,
        )
        readback = reads.get_raw_observation_occurrence(observation.observation_occurrence_id)
        return RawSignalSequenceResult(
            policy=registered_policy,
            capture=capture,
            observation=observation,
            relation=relation,
            assessment=assessment,
            readback=readback,
        )


def create_application(
    *,
    postgres_dsn: str | None = None,
    sqlite_path: str | None = None,
    raw_signal_owner_factory: _RawSignalOwnerFactory | None = None,
    raw_signal_eligibility_resolver: _RawSignalEligibilityResolver | None = None,
) -> Application:
    """Construct the admitted A00 -> M00 production composition.

    The production path requires exactly one store and constructs the accepted technical
    persistence mechanism before injecting it into M00. A bounded owner-factory-only path
    exists for proof of A00 delegation without fabricating a production database dependency.
    """

    owner_kwargs: dict[str, Any] = {}
    if raw_signal_eligibility_resolver is not None:
        owner_kwargs["eligibility_resolver"] = raw_signal_eligibility_resolver

    if postgres_dsn is not None and sqlite_path is not None:
        raise ValueError("exactly one of postgres_dsn or sqlite_path is required")
    if sqlite_path is not None:
        if raw_signal_owner_factory is not None:
            raise ValueError("raw_signal_owner_factory cannot be combined with sqlite_path")
        if type(sqlite_path) is not str:
            raise TypeError("sqlite_path must be a string")
        if not sqlite_path:
            raise ValueError("sqlite_path must be nonempty")
        from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

        durability_port = create_sqlite_persistence(sqlite_path, create=False)
        return Application(create_owner(durability_port=durability_port, **owner_kwargs))

    if postgres_dsn is None:
        if raw_signal_owner_factory is None:
            raise ValueError(
                "exactly one store is required for production application construction"
            )
        return Application(raw_signal_owner_factory(**owner_kwargs))

    if raw_signal_owner_factory is not None:
        raise ValueError(
            "raw_signal_owner_factory is proof-only and cannot be combined with postgres_dsn"
        )
    if type(postgres_dsn) is not str or not postgres_dsn.strip():
        raise ValueError("postgres_dsn must be a non-empty string")

    from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence

    durability_port = create_postgres_persistence(postgres_dsn)
    owner = create_owner(durability_port=durability_port, **owner_kwargs)
    return Application(owner)
