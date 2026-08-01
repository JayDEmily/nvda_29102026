"""Deterministic side-effect-free resolver for the M02 K04 public seam."""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .contracts import (
    AppliedSupersession,
    CalendarFactCandidate,
    CalendarFieldResolutionPolicy,
    CalendarProjection,
    FinancialCalendarLayer,
    FinancialCalendarSnapshot,
    SelectedCalendarField,
    projection_fingerprint,
)


def _validated_snapshot(
    snapshot: FinancialCalendarSnapshot | dict[str, Any],
) -> FinancialCalendarSnapshot:
    payload = snapshot.model_dump() if isinstance(snapshot, FinancialCalendarSnapshot) else snapshot
    return FinancialCalendarSnapshot.model_validate(payload)


def _validated_policy(
    policy: CalendarFieldResolutionPolicy | dict[str, Any],
) -> CalendarFieldResolutionPolicy:
    payload = policy.model_dump() if isinstance(policy, CalendarFieldResolutionPolicy) else policy
    return CalendarFieldResolutionPolicy.model_validate(payload)


def _semantic_value_key(candidate: CalendarFactCandidate) -> tuple[Any, ...]:
    return (
        candidate.fact_family,
        candidate.semantic_key,
        candidate.value_type,
        candidate.unit,
        candidate.value,
        candidate.effective_from_utc,
        candidate.effective_to_utc,
    )


def _lawful_supersession(
    candidate: CalendarFactCandidate,
    candidates: tuple[CalendarFactCandidate, ...],
) -> bool:
    if candidate.layer != FinancialCalendarLayer.OPERATIONAL_CALENDAR_STATE:
        return False
    if (
        not candidate.supersedes_candidate_id
        or not candidate.supersession_reason
        or candidate.supersession_status != "applied"
    ):
        return False
    target = next(
        (item for item in candidates if item.candidate_id == candidate.supersedes_candidate_id),
        None,
    )
    if target is None:
        return False
    return (
        target.layer
        in {
            FinancialCalendarLayer.MARKET_SESSION_REFERENCE,
            FinancialCalendarLayer.FINANCIAL_EVENT_REFERENCE,
            FinancialCalendarLayer.OPERATIONAL_CALENDAR_STATE,
        }
        and target.fact_family == candidate.fact_family
        and target.semantic_key == candidate.semantic_key
        and target.effective_from_utc == candidate.effective_from_utc
        and target.effective_to_utc == candidate.effective_to_utc
        and bool(candidate.owner_id)
    )


def _resolve_candidates(
    candidates: tuple[CalendarFactCandidate, ...],
) -> tuple[tuple[CalendarFactCandidate, ...], bool]:
    ordered = tuple(sorted(candidates, key=lambda item: item.candidate_id))
    if len({_semantic_value_key(item) for item in ordered}) == 1:
        return ordered, False
    lawful = tuple(item for item in ordered if _lawful_supersession(item, ordered))
    if len(lawful) == 1:
        return lawful, False
    return (), True


def _projection(
    *,
    projection_id: str,
    policy: CalendarFieldResolutionPolicy,
    snapshot: FinancialCalendarSnapshot,
    status: str,
    selected_fields: tuple[SelectedCalendarField, ...] = (),
    unresolved_conflicts: tuple[str, ...] = (),
    missing_mandatory_authority: tuple[str, ...] = (),
    degraded_facts: tuple[str, ...] = (),
    applied_supersessions: tuple[AppliedSupersession, ...] | None = None,
) -> CalendarProjection:
    preserved_supersessions = (
        snapshot.applied_supersessions if applied_supersessions is None else applied_supersessions
    )
    return CalendarProjection(
        projection_id=projection_id,
        projection_policy_version=policy.policy_version,
        canonicalisation_version=snapshot.canonicalisation_version,
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        snapshot_fingerprint=snapshot.semantic_fingerprint,
        scope=snapshot.scope,
        effective_from_utc=snapshot.effective_from_utc,
        effective_to_utc=snapshot.effective_to_utc,
        as_of_utc=snapshot.as_of_utc,
        status=status,
        selected_fields=selected_fields,
        unresolved_conflicts=unresolved_conflicts,
        missing_mandatory_authority=missing_mandatory_authority,
        degraded_facts=degraded_facts,
        applied_supersessions=preserved_supersessions,
        semantic_fingerprint=projection_fingerprint(
            projection_id=projection_id,
            projection_policy_version=policy.policy_version,
            canonicalisation_version=snapshot.canonicalisation_version,
            snapshot_id=snapshot.snapshot_id,
            snapshot_version=snapshot.snapshot_version,
            snapshot_fingerprint_value=snapshot.semantic_fingerprint,
            scope=snapshot.scope,
            effective_from_utc=snapshot.effective_from_utc,
            effective_to_utc=snapshot.effective_to_utc,
            as_of_utc=snapshot.as_of_utc,
            status=status,
            selected_fields=selected_fields,
            unresolved_conflicts=unresolved_conflicts,
            missing_mandatory_authority=missing_mandatory_authority,
            degraded_facts=degraded_facts,
            applied_supersessions=preserved_supersessions,
        ),
    )


class CalendarResolver:
    """Resolve one validated K04 snapshot without hidden state or side effects."""

    def project(
        self,
        snapshot: FinancialCalendarSnapshot | dict[str, Any],
        policy: CalendarFieldResolutionPolicy | dict[str, Any],
        *,
        projection_id: str,
    ) -> CalendarProjection:
        if not isinstance(projection_id, str) or not projection_id.strip():
            raise ValueError("projection_id_required")
        try:
            authority = _validated_snapshot(snapshot)
            governed_policy = _validated_policy(policy)
        except (ValidationError, TypeError, ValueError) as exc:
            raise ValueError("invalid_calendar_authority") from exc

        if authority.session_completeness != "complete" or not authority.market_session_reference:
            return _projection(
                projection_id=projection_id,
                policy=governed_policy,
                snapshot=authority,
                status="withheld",
                missing_mandatory_authority=("market_session_reference",),
            )

        if governed_policy.semantic_key in authority.unresolved_conflicts:
            return _projection(
                projection_id=projection_id,
                policy=governed_policy,
                snapshot=authority,
                status="withheld" if governed_policy.mandatory else "degraded",
                unresolved_conflicts=(governed_policy.semantic_key,),
            )

        candidates = tuple(
            candidate
            for collection in (
                authority.market_session_reference,
                authority.financial_event_reference,
                authority.operational_calendar_state,
                authority.derived_runtime_calendar_context,
            )
            for candidate in collection
            if candidate.semantic_key == governed_policy.semantic_key
            and candidate.validation_state == "valid"
        )

        if not candidates:
            if governed_policy.mandatory:
                return _projection(
                    projection_id=projection_id,
                    policy=governed_policy,
                    snapshot=authority,
                    status="withheld",
                    missing_mandatory_authority=(governed_policy.semantic_key,),
                )
            return _projection(
                projection_id=projection_id,
                policy=governed_policy,
                snapshot=authority,
                status="degraded",
                degraded_facts=(governed_policy.semantic_key,),
            )

        selected, conflict = _resolve_candidates(candidates)
        if conflict:
            return _projection(
                projection_id=projection_id,
                policy=governed_policy,
                snapshot=authority,
                status="withheld" if governed_policy.mandatory else "degraded",
                unresolved_conflicts=(governed_policy.semantic_key,),
                degraded_facts=() if governed_policy.mandatory else (governed_policy.semantic_key,),
            )

        selected_field = SelectedCalendarField(
            semantic_key=governed_policy.semantic_key,
            value=selected[0].value,
            candidate_ids=tuple(item.candidate_id for item in selected),
            source_refs=tuple(
                sorted({(item.source_artifact_id, item.source_version) for item in selected})
            ),
            layers=tuple(sorted((item.layer for item in selected), key=str)),
        )

        degraded: list[str] = []
        status = "projected"
        if authority.event_completeness != "complete":
            status = "degraded"
            degraded.append("financial_event_reference_unknown")
        if authority.operational_completeness != "complete":
            if governed_policy.allow_reference_only_degraded:
                status = "degraded"
                degraded.append("operational_calendar_state_unavailable")
            else:
                return _projection(
                    projection_id=projection_id,
                    policy=governed_policy,
                    snapshot=authority,
                    status="withheld",
                    missing_mandatory_authority=("operational_calendar_state",),
                )

        return _projection(
            projection_id=projection_id,
            policy=governed_policy,
            snapshot=authority,
            status=status,
            selected_fields=(selected_field,),
            degraded_facts=tuple(degraded),
            applied_supersessions=authority.applied_supersessions,
        )
