"""Reference and false-positive subjects for the bounded M02 K04 proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Any, Final

CLOSED_AUTHORITIES: Final = (
    "candidate_formation",
    "risk_permission",
    "capital",
    "broker_order",
    "position_inventory",
    "lifecycle",
    "review",
    "replay",
    "transaction",
)


class LayerCase(StrEnum):
    MARKET_SESSION_REFERENCE = "market_session_reference"
    FINANCIAL_EVENT_REFERENCE = "financial_event_reference"
    OPERATIONAL_CALENDAR_STATE = "operational_calendar_state"
    DERIVED_RUNTIME_CALENDAR_CONTEXT = "derived_runtime_calendar_context"


@dataclass(frozen=True)
class CandidateCase:
    candidate_id: str
    layer: LayerCase
    fact_family: str
    semantic_key: str
    value: Any
    value_type: str
    unit: str | None
    effective_from_utc: datetime
    effective_to_utc: datetime | None
    source_artifact_id: str
    source_version: str
    contract_version: str
    owner_id: str
    validation_state: str = "valid"
    observed_at_utc: datetime | None = None
    capture_id: str | None = None
    captured_at_utc: datetime | None = None
    supersedes_candidate_id: str | None = None
    supersession_reason: str | None = None
    supersession_status: str | None = None


@dataclass(frozen=True)
class SnapshotCase:
    snapshot_id: str
    snapshot_version: str
    schema_version: str
    scope: str
    effective_from_utc: datetime
    effective_to_utc: datetime
    as_of_utc: datetime
    market_session_reference: tuple[CandidateCase, ...]
    financial_event_reference: tuple[CandidateCase, ...]
    operational_calendar_state: tuple[CandidateCase, ...]
    derived_runtime_calendar_context: tuple[CandidateCase, ...]
    session_completeness: str
    event_completeness: str
    operational_completeness: str
    selected_reference_bundles: tuple[tuple[str, str], ...]
    unresolved_conflicts: tuple[str, ...]
    applied_supersessions: tuple[tuple[str, str, str, str], ...]
    projection_policy_version: str | None
    canonicalisation_version: str = "m02-k04-v1"
    semantic_fingerprint: str = ""


@dataclass(frozen=True)
class FieldPolicyCase:
    policy_id: str
    policy_version: str
    semantic_key: str
    mandatory: bool
    allow_reference_only_degraded: bool = False


@dataclass(frozen=True)
class SelectedFieldCase:
    semantic_key: str
    value: Any
    candidate_ids: tuple[str, ...]
    source_refs: tuple[tuple[str, str], ...]
    layers: tuple[LayerCase, ...]


@dataclass(frozen=True)
class ProjectionCase:
    projection_id: str
    projection_policy_version: str
    snapshot_id: str
    snapshot_version: str
    snapshot_fingerprint: str
    scope: str
    effective_from_utc: datetime
    effective_to_utc: datetime
    as_of_utc: datetime
    status: str
    selected_fields: tuple[SelectedFieldCase, ...]
    unresolved_conflicts: tuple[str, ...]
    missing_mandatory_authority: tuple[str, ...]
    degraded_facts: tuple[str, ...]
    semantic_fingerprint: str | None
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES
    foreign_authority_claimed: bool = False


def _candidate_material(candidate: CandidateCase) -> dict[str, Any]:
    return {
        "candidate_id": candidate.candidate_id,
        "layer": candidate.layer.value,
        "fact_family": candidate.fact_family,
        "semantic_key": candidate.semantic_key,
        "value": candidate.value,
        "value_type": candidate.value_type,
        "unit": candidate.unit,
        "effective_from_utc": candidate.effective_from_utc.isoformat(),
        "effective_to_utc": (
            candidate.effective_to_utc.isoformat()
            if candidate.effective_to_utc is not None
            else None
        ),
        "source_artifact_id": candidate.source_artifact_id,
        "source_version": candidate.source_version,
        "contract_version": candidate.contract_version,
        "owner_id": candidate.owner_id,
        "validation_state": candidate.validation_state,
        "observed_at_utc": (
            candidate.observed_at_utc.isoformat()
            if candidate.observed_at_utc is not None
            else None
        ),
        "capture_id": candidate.capture_id,
        "captured_at_utc": (
            candidate.captured_at_utc.isoformat()
            if candidate.captured_at_utc is not None
            else None
        ),
        "supersedes_candidate_id": candidate.supersedes_candidate_id,
        "supersession_reason": candidate.supersession_reason,
        "supersession_status": candidate.supersession_status,
    }


def snapshot_fingerprint(snapshot: SnapshotCase) -> str:
    material = {
        "snapshot_id": snapshot.snapshot_id,
        "snapshot_version": snapshot.snapshot_version,
        "schema_version": snapshot.schema_version,
        "scope": snapshot.scope,
        "effective_from_utc": snapshot.effective_from_utc.isoformat(),
        "effective_to_utc": snapshot.effective_to_utc.isoformat(),
        "as_of_utc": snapshot.as_of_utc.isoformat(),
        "layers": {
            layer_name: [
                _candidate_material(candidate)
                for candidate in sorted(
                    candidates,
                    key=lambda item: (item.semantic_key, item.candidate_id),
                )
            ]
            for layer_name, candidates in (
                ("market_session_reference", snapshot.market_session_reference),
                ("financial_event_reference", snapshot.financial_event_reference),
                ("operational_calendar_state", snapshot.operational_calendar_state),
                (
                    "derived_runtime_calendar_context",
                    snapshot.derived_runtime_calendar_context,
                ),
            )
        },
        "session_completeness": snapshot.session_completeness,
        "event_completeness": snapshot.event_completeness,
        "operational_completeness": snapshot.operational_completeness,
        "selected_reference_bundles": [
            {"bundle_id": bundle_id, "bundle_version": bundle_version}
            for bundle_id, bundle_version in snapshot.selected_reference_bundles
        ],
        "unresolved_conflicts": snapshot.unresolved_conflicts,
        "applied_supersessions": [
            {
                "superseding_candidate_id": winner_id,
                "superseded_candidate_id": target_id,
                "reason": reason,
                "status": status,
            }
            for winner_id, target_id, reason, status in snapshot.applied_supersessions
        ],
        "projection_policy_version": snapshot.projection_policy_version,
        "canonicalisation_version": snapshot.canonicalisation_version,
    }
    return sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def valid_candidate(
    *,
    candidate_id: str = "session.reference.a",
    layer: LayerCase = LayerCase.MARKET_SESSION_REFERENCE,
    semantic_key: str = "session_open_utc",
    value: Any = "2026-07-31T13:30:00+00:00",
    source_artifact_id: str = "calendar.reference.a",
    source_version: str = "2026.07.31.1",
    observed_at_utc: datetime | None = None,
    capture_id: str | None = None,
    captured_at_utc: datetime | None = None,
    supersedes_candidate_id: str | None = None,
    supersession_reason: str | None = None,
    supersession_status: str | None = None,
) -> CandidateCase:
    return CandidateCase(
        candidate_id=candidate_id,
        layer=layer,
        fact_family="market_session",
        semantic_key=semantic_key,
        value=value,
        value_type="datetime",
        unit=None,
        effective_from_utc=datetime(2026, 7, 31, 0, 0, tzinfo=UTC),
        effective_to_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        source_artifact_id=source_artifact_id,
        source_version=source_version,
        contract_version="1.0.0",
        owner_id=f"owner.{layer.value}",
        observed_at_utc=observed_at_utc,
        capture_id=capture_id,
        captured_at_utc=captured_at_utc,
        supersedes_candidate_id=supersedes_candidate_id,
        supersession_reason=supersession_reason,
        supersession_status=(
            supersession_status
            if supersession_status is not None
            else ("applied" if supersedes_candidate_id is not None else None)
        ),
    )


def event_candidate(*, candidate_id: str = "event.reference.a") -> CandidateCase:
    return replace(
        valid_candidate(
            candidate_id=candidate_id,
            layer=LayerCase.FINANCIAL_EVENT_REFERENCE,
            semantic_key="event.fomc.window",
            value="2026-07-31T18:00:00+00:00",
            source_artifact_id="calendar.events.a",
        ),
        fact_family="financial_event",
    )


def valid_snapshot(
    *,
    session_candidates: tuple[CandidateCase, ...] | None = None,
    event_candidates: tuple[CandidateCase, ...] | None = None,
    operational_candidates: tuple[CandidateCase, ...] = (),
    derived_candidates: tuple[CandidateCase, ...] = (),
    session_completeness: str = "complete",
    event_completeness: str = "complete",
    operational_completeness: str = "complete",
) -> SnapshotCase:
    all_candidates = (
        (() if session_candidates is None else session_candidates)
        + (() if event_candidates is None else event_candidates)
        + operational_candidates
        + derived_candidates
    )
    applied_supersessions = tuple(
        sorted(
            (
                item.candidate_id,
                item.supersedes_candidate_id or "",
                item.supersession_reason or "",
                item.supersession_status or "",
            )
            for item in all_candidates
            if item.supersedes_candidate_id is not None
            and item.layer == LayerCase.OPERATIONAL_CALENDAR_STATE
        )
    )
    snapshot = SnapshotCase(
        snapshot_id="m02.nvda.calendar.2026-07-31",
        snapshot_version="2026.07.31.1",
        schema_version="1.0.0",
        scope="NVDA:XNAS:2026-07-31",
        effective_from_utc=datetime(2026, 7, 31, 0, 0, tzinfo=UTC),
        effective_to_utc=datetime(2026, 8, 1, 0, 0, tzinfo=UTC),
        as_of_utc=datetime(2026, 7, 31, 4, 0, tzinfo=UTC),
        market_session_reference=(valid_candidate(),)
        if session_candidates is None
        else session_candidates,
        financial_event_reference=(event_candidate(),)
        if event_candidates is None
        else event_candidates,
        operational_calendar_state=operational_candidates,
        derived_runtime_calendar_context=derived_candidates,
        session_completeness=session_completeness,
        event_completeness=event_completeness,
        operational_completeness=operational_completeness,
        selected_reference_bundles=(("calendar.bundle.nvda", "2026.07.31.1"),),
        unresolved_conflicts=(),
        applied_supersessions=applied_supersessions,
        projection_policy_version=("k04.v1" if derived_candidates else None),
    )
    return replace(snapshot, semantic_fingerprint=snapshot_fingerprint(snapshot))


def field_policy(
    *,
    semantic_key: str = "session_open_utc",
    mandatory: bool = True,
    allow_reference_only_degraded: bool = False,
) -> FieldPolicyCase:
    return FieldPolicyCase(
        policy_id=f"m02.policy.{semantic_key}",
        policy_version="1.0.0",
        semantic_key=semantic_key,
        mandatory=mandatory,
        allow_reference_only_degraded=allow_reference_only_degraded,
    )


class ReferenceSubject:
    """Small executable reference for the accepted K04 proposition."""

    def project(
        self,
        snapshot: SnapshotCase | None,
        policy: FieldPolicyCase,
        *,
        projection_id: str = "projection.reference",
    ) -> ProjectionCase:
        if snapshot is None:
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=None,
                status="rejected",
                missing=("snapshot_authority",),
            )
        if snapshot.semantic_fingerprint != snapshot_fingerprint(snapshot):
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=snapshot,
                status="rejected",
                missing=("snapshot_fingerprint_mismatch",),
            )
        if snapshot.session_completeness != "complete" or not snapshot.market_session_reference:
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=snapshot,
                status="withheld",
                missing=("market_session_reference",),
            )
        if snapshot.event_completeness == "unknown":
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=snapshot,
                status="degraded",
                degraded=("financial_event_reference_unknown",),
            )
        candidates = tuple(
            candidate
            for collection in (
                snapshot.market_session_reference,
                snapshot.financial_event_reference,
                snapshot.operational_calendar_state,
                snapshot.derived_runtime_calendar_context,
            )
            for candidate in collection
            if candidate.semantic_key == policy.semantic_key
            and candidate.validation_state == "valid"
        )
        if not candidates:
            status = "withheld" if policy.mandatory else "degraded"
            missing = (policy.semantic_key,) if policy.mandatory else ()
            degraded = () if policy.mandatory else (policy.semantic_key,)
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=snapshot,
                status=status,
                missing=missing,
                degraded=degraded,
            )
        selected, conflict = self._resolve_candidates(candidates)
        if conflict:
            return self._result(
                projection_id=projection_id,
                policy=policy,
                snapshot=snapshot,
                status="withheld" if policy.mandatory else "degraded",
                conflicts=(policy.semantic_key,),
                degraded=() if policy.mandatory else (policy.semantic_key,),
            )
        field = SelectedFieldCase(
            semantic_key=policy.semantic_key,
            value=selected[0].value,
            candidate_ids=tuple(sorted(item.candidate_id for item in selected)),
            source_refs=tuple(
                sorted((item.source_artifact_id, item.source_version) for item in selected)
            ),
            layers=tuple(sorted((item.layer for item in selected), key=str)),
        )
        status = "projected"
        degraded: tuple[str, ...] = ()
        if (
            snapshot.operational_completeness != "complete"
            and policy.allow_reference_only_degraded
        ):
            status = "degraded"
            degraded = ("operational_calendar_state_unavailable",)
        return self._result(
            projection_id=projection_id,
            policy=policy,
            snapshot=snapshot,
            status=status,
            selected=(field,),
            degraded=degraded,
        )

    def _resolve_candidates(
        self, candidates: tuple[CandidateCase, ...]
    ) -> tuple[tuple[CandidateCase, ...], bool]:
        values = {
            (
                item.fact_family,
                item.semantic_key,
                item.value_type,
                item.unit,
                item.value,
                item.effective_from_utc,
                item.effective_to_utc,
            )
            for item in candidates
        }
        if len(values) == 1:
            return candidates, False
        source_candidates = tuple(
            item
            for item in candidates
            if item.layer != LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT
        )
        lawful = tuple(
            item
            for item in source_candidates
            if item.supersedes_candidate_id is not None
            and item.supersession_reason
            and any(
                target.candidate_id == item.supersedes_candidate_id
                and target.fact_family == item.fact_family
                and target.semantic_key == item.semantic_key
                for target in source_candidates
            )
        )
        if len(lawful) == 1:
            return lawful, False
        return (), True

    def _result(
        self,
        *,
        projection_id: str,
        policy: FieldPolicyCase,
        snapshot: SnapshotCase | None,
        status: str,
        selected: tuple[SelectedFieldCase, ...] = (),
        conflicts: tuple[str, ...] = (),
        missing: tuple[str, ...] = (),
        degraded: tuple[str, ...] = (),
    ) -> ProjectionCase:
        if snapshot is None:
            snapshot_id = ""
            snapshot_version = ""
            snapshot_fingerprint_value = ""
            scope = ""
            effective_from = datetime(2026, 7, 31, 0, 0, tzinfo=UTC)
            effective_to = datetime(2026, 8, 1, 0, 0, tzinfo=UTC)
            as_of = datetime(2026, 7, 31, 4, 0, tzinfo=UTC)
        else:
            snapshot_id = snapshot.snapshot_id
            snapshot_version = snapshot.snapshot_version
            snapshot_fingerprint_value = snapshot.semantic_fingerprint
            scope = snapshot.scope
            effective_from = snapshot.effective_from_utc
            effective_to = snapshot.effective_to_utc
            as_of = snapshot.as_of_utc
        material = {
            "projection_id": projection_id,
            "projection_policy_version": policy.policy_version,
            "snapshot_id": snapshot_id,
            "snapshot_version": snapshot_version,
            "snapshot_fingerprint": snapshot_fingerprint_value,
            "scope": scope,
            "effective_from_utc": effective_from.isoformat(),
            "effective_to_utc": effective_to.isoformat(),
            "as_of_utc": as_of.isoformat(),
            "status": status,
            "selected_fields": [
                {
                    "semantic_key": item.semantic_key,
                    "value": item.value,
                    "candidate_ids": item.candidate_ids,
                    "source_refs": item.source_refs,
                    "layers": tuple(layer.value for layer in item.layers),
                }
                for item in selected
            ],
            "unresolved_conflicts": conflicts,
            "missing_mandatory_authority": missing,
            "degraded_facts": degraded,
        }
        fingerprint = sha256(
            json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return ProjectionCase(
            projection_id=projection_id,
            projection_policy_version=policy.policy_version,
            snapshot_id=snapshot_id,
            snapshot_version=snapshot_version,
            snapshot_fingerprint=snapshot_fingerprint_value,
            scope=scope,
            effective_from_utc=effective_from,
            effective_to_utc=effective_to,
            as_of_utc=as_of,
            status=status,
            selected_fields=selected,
            unresolved_conflicts=conflicts,
            missing_mandatory_authority=missing,
            degraded_facts=degraded,
            semantic_fingerprint=fingerprint,
        )


class CallerOrderMutant(ReferenceSubject):
    def _resolve_candidates(self, candidates):
        return (candidates[-1],), False


class DerivedOverrideMutant(ReferenceSubject):
    def _resolve_candidates(self, candidates):
        derived = tuple(
            item
            for item in candidates
            if item.layer == LayerCase.DERIVED_RUNTIME_CALENDAR_CONTEXT
        )
        return (derived[-1],), False


class MissingSessionAsProjectedMutant(ReferenceSubject):
    def project(self, snapshot, policy, *, projection_id="projection.reference"):
        if snapshot is not None and not snapshot.market_session_reference:
            snapshot = replace(
                snapshot,
                market_session_reference=(valid_candidate(candidate_id="fabricated.session"),),
                session_completeness="complete",
            )
            snapshot = replace(snapshot, semantic_fingerprint=snapshot_fingerprint(snapshot))
        return super().project(snapshot, policy, projection_id=projection_id)


class UnknownEventsAsEmptyMutant(ReferenceSubject):
    def project(self, snapshot, policy, *, projection_id="projection.reference"):
        if snapshot is not None and snapshot.event_completeness == "unknown":
            snapshot = replace(snapshot, event_completeness="complete")
            snapshot = replace(snapshot, semantic_fingerprint=snapshot_fingerprint(snapshot))
        return super().project(snapshot, policy, projection_id=projection_id)


class LineageDroppingMutant(ReferenceSubject):
    def _result(self, **kwargs):
        result = super()._result(**kwargs)
        if result.selected_fields:
            field = result.selected_fields[0]
            result = replace(
                result,
                selected_fields=(
                    replace(
                        field,
                        candidate_ids=field.candidate_ids[:1],
                        source_refs=field.source_refs[:1],
                        layers=field.layers[:1],
                    ),
                ),
            )
        return result


class ForeignAuthorityMutant(ReferenceSubject):
    def _result(self, **kwargs):
        return replace(
            super()._result(**kwargs),
            closed_authority_classes=("candidate_formation",),
            foreign_authority_claimed=True,
        )


MUTANTS = {
    "caller_order": CallerOrderMutant,
    "derived_override": DerivedOverrideMutant,
    "missing_session_as_projected": MissingSessionAsProjectedMutant,
    "unknown_events_as_empty": UnknownEventsAsEmptyMutant,
    "lineage_dropping": LineageDroppingMutant,
    "foreign_authority": ForeignAuthorityMutant,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m02_financial_calendar")
    return {
        name: getattr(module, name)
        for name in (
            "FinancialCalendarLayer",
            "CalendarFactCandidate",
            "FinancialCalendarSnapshot",
            "CalendarProjection",
            "CalendarFieldResolutionPolicy",
            "CalendarResolver",
        )
    }


def production_candidate_payload(candidate: CandidateCase) -> dict[str, Any]:
    payload = _candidate_material(candidate)
    payload["layer"] = candidate.layer.value
    return payload


def production_snapshot_payload(snapshot: SnapshotCase | None = None) -> dict[str, Any]:
    subject = snapshot or valid_snapshot()
    return {
        "snapshot_id": subject.snapshot_id,
        "snapshot_version": subject.snapshot_version,
        "schema_version": subject.schema_version,
        "scope": subject.scope,
        "effective_from_utc": subject.effective_from_utc,
        "effective_to_utc": subject.effective_to_utc,
        "as_of_utc": subject.as_of_utc,
        "market_session_reference": [
            production_candidate_payload(item)
            for item in subject.market_session_reference
        ],
        "financial_event_reference": [
            production_candidate_payload(item)
            for item in subject.financial_event_reference
        ],
        "operational_calendar_state": [
            production_candidate_payload(item)
            for item in subject.operational_calendar_state
        ],
        "derived_runtime_calendar_context": [
            production_candidate_payload(item)
            for item in subject.derived_runtime_calendar_context
        ],
        "session_completeness": subject.session_completeness,
        "event_completeness": subject.event_completeness,
        "operational_completeness": subject.operational_completeness,
        "selected_reference_bundles": [
            {"bundle_id": bundle_id, "bundle_version": bundle_version}
            for bundle_id, bundle_version in subject.selected_reference_bundles
        ],
        "unresolved_conflicts": list(subject.unresolved_conflicts),
        "applied_supersessions": [
            {
                "superseding_candidate_id": winner,
                "superseded_candidate_id": target,
                "reason": reason,
                "status": status,
            }
            for winner, target, reason, status in subject.applied_supersessions
        ],
        "projection_policy_version": subject.projection_policy_version,
        "canonicalisation_version": subject.canonicalisation_version,
        "semantic_fingerprint": subject.semantic_fingerprint,
    }


def production_policy_payload(policy: FieldPolicyCase | None = None) -> dict[str, Any]:
    subject = policy or field_policy()
    return {
        "policy_id": subject.policy_id,
        "policy_version": subject.policy_version,
        "semantic_key": subject.semantic_key,
        "mandatory": subject.mandatory,
        "allow_reference_only_degraded": subject.allow_reference_only_degraded,
    }
