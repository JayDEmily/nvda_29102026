"""Pure deterministic resolver for the bounded M07 K12 public seam."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any

from pydantic import ValidationError

from .contracts import (
    CLOSED_AUTHORITY_CLASSES,
    CoefficientMember,
    CoefficientResolution,
    InputStateFacts,
    ModifierApplicationReceipt,
    ModifierDecision,
    ModifierDisposition,
    ModifierMember,
    PolicyBundle,
)


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() is not None
        and value.utcoffset() == UTC.utcoffset(value)
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value: Any) -> str:
    return sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _authority_key(modifier: ModifierMember) -> tuple[int, str, str]:
    return (modifier.precedence_rank, modifier.modifier_id, modifier.modifier_version)


def _disposition(modifier: ModifierMember, reason: str) -> ModifierDisposition:
    return ModifierDisposition(
        modifier_id=modifier.modifier_id,
        modifier_version=modifier.modifier_version,
        precedence_rank=modifier.precedence_rank,
        reason=reason,
    )


def _baseline_results(bundle: PolicyBundle) -> tuple[CoefficientResolution, ...]:
    return tuple(
        CoefficientResolution(
            coefficient_id=item.coefficient_id,
            coefficient_version=item.coefficient_version,
            baseline_value=item.baseline_value,
            pre_clamp_candidate=item.baseline_value,
            hard_lower_bound=item.hard_lower_bound,
            hard_upper_bound=item.hard_upper_bound,
            effective_value=item.baseline_value,
            bound_disposition="within_bounds",
        )
        for item in sorted(bundle.coefficients, key=lambda member: member.coefficient_id)
    )


def _rejected(
    *,
    owner_stage: str | None,
    reasons: tuple[str, ...],
    input_state: InputStateFacts | None = None,
    bundle: PolicyBundle | None = None,
) -> ModifierDecision:
    identity_payload = {
        "owner_stage": owner_stage,
        "reasons": reasons,
        "bundle_id": bundle.bundle_id if bundle is not None else None,
        "bundle_version": bundle.bundle_version if bundle is not None else None,
        "input_context_id": input_state.context_id if input_state is not None else None,
        "input_context_version": input_state.context_version if input_state is not None else None,
        "input_fingerprint": input_state.fingerprint if input_state is not None else None,
    }
    return ModifierDecision(
        decision_id=f"m07-decision::rejected::{_digest(identity_payload)[:24]}",
        semantic_fingerprint=None,
        bundle_id=bundle.bundle_id if bundle is not None else None,
        bundle_version=bundle.bundle_version if bundle is not None else None,
        schema_version=bundle.schema_version if bundle is not None else None,
        authority_id=bundle.authority_id if bundle is not None else None,
        authority_version=bundle.authority_version if bundle is not None else None,
        resolution_law_version=bundle.resolution_law_version if bundle is not None else None,
        owner_stage=owner_stage,
        input_context_id=input_state.context_id if input_state is not None else None,
        input_context_version=input_state.context_version if input_state is not None else None,
        input_effective_at_utc=(input_state.effective_at_utc if input_state is not None else None),
        input_fingerprint=input_state.fingerprint if input_state is not None else None,
        status="rejected",
        rejection_reasons=reasons,
    )


def _accepted(
    *,
    bundle: PolicyBundle,
    input_state: InputStateFacts,
    status: str,
    evaluated: tuple[ModifierDisposition, ...],
    applied: tuple[ModifierDisposition, ...],
    skipped: tuple[ModifierDisposition, ...],
    results: tuple[CoefficientResolution, ...],
    conflicts: tuple[str, ...] = (),
    vetoes: tuple[str, ...] = (),
    kills: tuple[str, ...] = (),
) -> ModifierDecision:
    material = {
        "bundle": bundle.model_dump(mode="json"),
        "input_state": {
            "context_id": input_state.context_id,
            "context_version": input_state.context_version,
            "effective_at_utc": input_state.effective_at_utc.isoformat(),
            "fingerprint": input_state.fingerprint,
            "facts": dict(sorted(input_state.facts.items())),
        },
        "status": status,
        "evaluated_modifiers": [item.model_dump(mode="json") for item in evaluated],
        "applied_modifiers": [item.model_dump(mode="json") for item in applied],
        "skipped_modifiers": [item.model_dump(mode="json") for item in skipped],
        "coefficient_results": [item.model_dump(mode="json") for item in results],
        "conflict_dispositions": conflicts,
        "veto_dispositions": vetoes,
        "kill_switch_dispositions": kills,
        "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
    }
    fingerprint = _digest(material)
    return ModifierDecision(
        decision_id=f"m07-decision::{fingerprint[:24]}",
        semantic_fingerprint=fingerprint,
        bundle_id=bundle.bundle_id,
        bundle_version=bundle.bundle_version,
        schema_version=bundle.schema_version,
        authority_id=bundle.authority_id,
        authority_version=bundle.authority_version,
        resolution_law_version=bundle.resolution_law_version,
        owner_stage=bundle.owner_stage,
        input_context_id=input_state.context_id,
        input_context_version=input_state.context_version,
        input_effective_at_utc=input_state.effective_at_utc,
        input_fingerprint=input_state.fingerprint,
        status=status,
        evaluated_modifiers=evaluated,
        applied_modifiers=applied,
        skipped_modifiers=skipped,
        coefficient_results=results,
        conflict_dispositions=conflicts,
        veto_dispositions=vetoes,
        kill_switch_dispositions=kills,
    )


def _validated_bundle(value: PolicyBundle | Any) -> PolicyBundle:
    material = value.model_dump(mode="python") if isinstance(value, PolicyBundle) else value
    return PolicyBundle.model_validate(material)


def _validated_input_state(value: InputStateFacts | Any) -> InputStateFacts:
    material = value.model_dump(mode="python") if isinstance(value, InputStateFacts) else value
    return InputStateFacts.model_validate(material)


def _first_missing_fact(
    modifiers: tuple[ModifierMember, ...],
    input_state: InputStateFacts,
) -> str | None:
    for modifier in modifiers:
        for fact_ref in modifier.applicability_fact_refs:
            if fact_ref not in input_state.facts:
                return fact_ref
    return None


def _applicable(
    modifiers: tuple[ModifierMember, ...],
    input_state: InputStateFacts,
) -> tuple[ModifierMember, ...]:
    return tuple(
        modifier
        for modifier in modifiers
        if all(input_state.facts[fact_ref] for fact_ref in modifier.applicability_fact_refs)
    )


def _unresolved_pair(modifiers: tuple[ModifierMember, ...]) -> tuple[str, str] | None:
    for index, first in enumerate(modifiers):
        first_targets = set(first.target_coefficient_ids)
        for second in modifiers[index + 1 :]:
            if first_targets.isdisjoint(second.target_coefficient_ids):
                continue
            explicit_conflict = (
                second.modifier_id in first.conflict_modifier_ids
                or first.modifier_id in second.conflict_modifier_ids
            )
            equal_precedence = first.precedence_rank == second.precedence_rank
            if explicit_conflict or equal_precedence:
                return (first.modifier_id, second.modifier_id)
    return None


def _apply_modifier(current: Decimal, modifier: ModifierMember) -> Decimal:
    if modifier.transform_operator == "add":
        return current + modifier.operand
    if modifier.transform_operator == "multiply":
        return current * modifier.operand
    return modifier.operand


def _resolved_value(
    coefficient: CoefficientMember,
    candidate: Decimal,
) -> CoefficientResolution:
    if candidate < coefficient.hard_lower_bound:
        effective = coefficient.hard_lower_bound
        disposition = "clamped_lower"
    elif candidate > coefficient.hard_upper_bound:
        effective = coefficient.hard_upper_bound
        disposition = "clamped_upper"
    else:
        effective = candidate
        disposition = "within_bounds"
    return CoefficientResolution(
        coefficient_id=coefficient.coefficient_id,
        coefficient_version=coefficient.coefficient_version,
        baseline_value=coefficient.baseline_value,
        pre_clamp_candidate=candidate,
        hard_lower_bound=coefficient.hard_lower_bound,
        hard_upper_bound=coefficient.hard_upper_bound,
        effective_value=effective,
        bound_disposition=disposition,
    )


def resolve_k12(
    *,
    bundle: PolicyBundle | None,
    owner_stage: str,
    input_state: InputStateFacts | dict[str, Any],
) -> ModifierDecision:
    """Resolve one admitted M07 K12 bundle without side effects or hidden state."""

    if not isinstance(owner_stage, str) or not owner_stage:
        return _rejected(owner_stage=None, reasons=("owner_stage_missing",))

    try:
        facts = _validated_input_state(input_state)
    except (ValidationError, TypeError, ValueError):
        return _rejected(owner_stage=owner_stage, reasons=("invalid_input_state",))
    if not _is_utc(facts.effective_at_utc):
        return _rejected(
            owner_stage=owner_stage,
            reasons=("input_state_time_must_be_utc",),
            input_state=facts,
        )
    if bundle is None:
        return _rejected(
            owner_stage=owner_stage,
            reasons=("bundle_authority_missing",),
            input_state=facts,
        )
    try:
        authority = _validated_bundle(bundle)
    except (ValidationError, TypeError, ValueError):
        return _rejected(
            owner_stage=owner_stage,
            reasons=("bundle_authority_invalid",),
            input_state=facts,
        )
    if authority.owner_stage != owner_stage:
        return _rejected(
            owner_stage=owner_stage,
            reasons=("bundle_owner_stage_mismatch",),
            input_state=facts,
            bundle=authority,
        )

    ordered = tuple(sorted(authority.modifiers, key=_authority_key))
    missing_fact = _first_missing_fact(ordered, facts)
    if missing_fact is not None:
        return _rejected(
            owner_stage=owner_stage,
            reasons=(f"missing_applicability_fact:{missing_fact}",),
            input_state=facts,
            bundle=authority,
        )

    if not ordered:
        return _accepted(
            bundle=authority,
            input_state=facts,
            status="no_modifier_members",
            evaluated=(),
            applied=(),
            skipped=(),
            results=_baseline_results(authority),
        )

    active = _applicable(ordered, facts)
    inactive = tuple(modifier for modifier in ordered if modifier not in active)
    evaluated = tuple(
        _disposition(
            modifier,
            "applicable" if modifier in active else "not_applicable",
        )
        for modifier in ordered
    )
    if not active:
        skipped = tuple(_disposition(modifier, "not_applicable") for modifier in inactive)
        return _accepted(
            bundle=authority,
            input_state=facts,
            status="no_applicable_modifiers",
            evaluated=evaluated,
            applied=(),
            skipped=skipped,
            results=_baseline_results(authority),
        )

    kill_targets = {
        target_id
        for modifier in active
        if modifier.kill_switch
        for target_id in modifier.target_coefficient_ids
    }
    kill_dominated = tuple(
        modifier
        for modifier in active
        if not modifier.kill_switch and not kill_targets.isdisjoint(modifier.target_coefficient_ids)
    )
    after_kill = tuple(modifier for modifier in active if modifier not in kill_dominated)

    vetoed_ids = {vetoed_id for modifier in after_kill for vetoed_id in modifier.veto_modifier_ids}
    vetoed = tuple(modifier for modifier in after_kill if modifier.modifier_id in vetoed_ids)
    effective_modifiers = tuple(modifier for modifier in after_kill if modifier not in vetoed)

    conflict = _unresolved_pair(effective_modifiers)
    if conflict is not None:
        return _rejected(
            owner_stage=owner_stage,
            reasons=(f"unresolved_modifier_conflict:{conflict[0]}:{conflict[1]}",),
            input_state=facts,
            bundle=authority,
        )

    values = {
        coefficient.coefficient_id: coefficient.baseline_value
        for coefficient in authority.coefficients
    }
    applied = tuple(_disposition(modifier, "applied") for modifier in effective_modifiers)
    for modifier in effective_modifiers:
        for target_id in modifier.target_coefficient_ids:
            values[target_id] = _apply_modifier(values[target_id], modifier)

    skipped = tuple(
        sorted(
            (
                *(_disposition(modifier, "not_applicable") for modifier in inactive),
                *(
                    _disposition(modifier, "dominated_by_kill_switch")
                    for modifier in kill_dominated
                ),
                *(_disposition(modifier, "vetoed_by_authority_modifier") for modifier in vetoed),
            ),
            key=lambda item: (item.precedence_rank, item.modifier_id, item.modifier_version),
        )
    )
    results = tuple(
        _resolved_value(coefficient, values[coefficient.coefficient_id])
        for coefficient in sorted(authority.coefficients, key=lambda item: item.coefficient_id)
    )
    kill_dispositions = tuple(
        f"kill_switch_applied:{modifier.modifier_id}"
        for modifier in effective_modifiers
        if modifier.kill_switch
    )
    veto_dispositions = tuple(f"modifier_vetoed:{modifier.modifier_id}" for modifier in vetoed)
    return _accepted(
        bundle=authority,
        input_state=facts,
        status="applied",
        evaluated=evaluated,
        applied=applied,
        skipped=skipped,
        results=results,
        vetoes=veto_dispositions,
        kills=kill_dispositions,
    )


def build_k12_receipt(
    *,
    decision: ModifierDecision,
    receipt_id: str,
    application_id: str,
    emitted_at_utc: datetime,
) -> ModifierApplicationReceipt | None:
    """Build occurrence evidence for one non-rejected decision without claiming mutation."""

    material = (
        decision.model_dump(mode="python") if isinstance(decision, ModifierDecision) else decision
    )
    try:
        governed_decision = ModifierDecision.model_validate(material)
    except (ValidationError, TypeError, ValueError) as exc:
        raise ValueError("receipt_source_contract_invalid") from exc

    if governed_decision.status == "rejected" or governed_decision.semantic_fingerprint is None:
        return None
    decision = governed_decision
    if any(
        value is None
        for value in (
            decision.bundle_id,
            decision.bundle_version,
            decision.schema_version,
            decision.authority_id,
            decision.authority_version,
            decision.resolution_law_version,
            decision.input_context_id,
            decision.input_context_version,
            decision.input_effective_at_utc,
            decision.input_fingerprint,
        )
    ):
        raise ValueError("non_rejected_decision_lineage_incomplete")

    no_op_class = (
        decision.status
        if decision.status in {"no_modifier_members", "no_applicable_modifiers"}
        else None
    )
    return ModifierApplicationReceipt(
        receipt_id=receipt_id,
        application_id=application_id,
        source_decision_id=decision.decision_id,
        source_decision_fingerprint=decision.semantic_fingerprint,
        bundle_id=decision.bundle_id,
        bundle_version=decision.bundle_version,
        schema_version=decision.schema_version,
        authority_id=decision.authority_id,
        authority_version=decision.authority_version,
        resolution_law_version=decision.resolution_law_version,
        owner_stage=decision.owner_stage,
        input_context_id=decision.input_context_id,
        input_context_version=decision.input_context_version,
        input_effective_at_utc=decision.input_effective_at_utc,
        input_fingerprint=decision.input_fingerprint,
        decision_status=decision.status,
        applied_modifiers=decision.applied_modifiers,
        skipped_modifiers=decision.skipped_modifiers,
        coefficient_results=decision.coefficient_results,
        conflict_dispositions=decision.conflict_dispositions,
        veto_dispositions=decision.veto_dispositions,
        kill_switch_dispositions=decision.kill_switch_dispositions,
        no_op_class=no_op_class,
        emitted_at_utc=emitted_at_utc,
    )
