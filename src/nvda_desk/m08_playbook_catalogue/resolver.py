"""Deterministic owner-local resolver for the bounded M08 K13 public seam."""

from __future__ import annotations

import json
from hashlib import sha256
from typing import Any

from pydantic import ValidationError

from .contracts import (
    CLOSED_AUTHORITY_CLASSES,
    DefinitionDisposition,
    EligibilityContext,
    EligibilityDecision,
    EligibleCandidate,
    FactAuthority,
    PlaybookCatalogue,
    PlaybookDefinition,
    PosturePermission,
    _is_utc,
)


def _canonical_json(material: Any) -> str:
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _validated_catalogue(value: PlaybookCatalogue) -> PlaybookCatalogue:
    if not isinstance(value, PlaybookCatalogue):
        raise TypeError("catalogue_authority_must_be_typed")
    return PlaybookCatalogue.model_validate(value.model_dump(mode="python"))


def _validated_posture(value: PosturePermission | dict[str, Any]) -> PosturePermission:
    material = value.model_dump(mode="python") if isinstance(value, PosturePermission) else value
    return PosturePermission.model_validate(material)


def _validated_context(value: EligibilityContext | dict[str, Any]) -> EligibilityContext:
    material = value.model_dump(mode="python") if isinstance(value, EligibilityContext) else value
    return EligibilityContext.model_validate(material)


def _rejected(*, decision_id: str, reason: str) -> EligibilityDecision:
    return EligibilityDecision(
        decision_id=decision_id,
        status="rejected",
        reason=reason,
        semantic_fingerprint=None,
    )


def _disposition(definition: PlaybookDefinition, reason: str) -> DefinitionDisposition:
    return DefinitionDisposition(
        playbook_id=definition.playbook_id,
        playbook_version=definition.playbook_version,
        candidate_family_id=definition.candidate_family_id,
        candidate_family_version=definition.candidate_family_version,
        setup_variant_id=definition.setup_variant_id,
        setup_variant_version=definition.setup_variant_version,
        reason=reason,
    )


def _candidate(definition: PlaybookDefinition) -> EligibleCandidate:
    return EligibleCandidate(
        playbook_id=definition.playbook_id,
        playbook_version=definition.playbook_version,
        candidate_family_id=definition.candidate_family_id,
        candidate_family_version=definition.candidate_family_version,
        setup_variant_id=definition.setup_variant_id,
        setup_variant_version=definition.setup_variant_version,
        selection_priority=definition.selection_priority,
        lifecycle_intent=dict(definition.lifecycle_intent),
        lifecycle_schema_version=definition.lifecycle_schema_version,
        promotion_lineage=definition.promotion_lineage,
    )


def _definition_key(definition: PlaybookDefinition) -> tuple[str, ...]:
    return definition.identity_tuple


def _candidate_key(candidate: EligibleCandidate) -> tuple[int | str, ...]:
    return (candidate.selection_priority, *candidate.identity_tuple)


def _fact_material(fact: FactAuthority) -> tuple[Any, ...]:
    return (
        fact.fact_ref,
        fact.owner_id,
        fact.contract_version,
        fact.effective_at_utc.isoformat(),
        fact.semantic_fingerprint,
        fact.value,
    )


def _decision_fingerprint(
    *,
    catalogue: PlaybookCatalogue,
    posture: PosturePermission,
    context: EligibilityContext,
    status: str,
    reason: str | None,
    skipped: tuple[DefinitionDisposition, ...],
    ineligible: tuple[DefinitionDisposition, ...],
    eligible: tuple[EligibleCandidate, ...],
    material_facts: tuple[FactAuthority, ...],
) -> str:
    material = {
        "catalogue": [
            catalogue.catalogue_id,
            catalogue.catalogue_version,
            catalogue.schema_version,
            catalogue.authority_id,
            catalogue.authority_version,
            catalogue.effective_version_selector,
            catalogue.eligibility_law_version,
            catalogue.promotion_lineage,
            catalogue.catalogue_fingerprint,
        ],
        "posture": [
            posture.posture_id,
            posture.posture_version,
            posture.status,
            posture.effective_at_utc.isoformat(),
            posture.semantic_fingerprint,
        ],
        "context": [
            context.context_id,
            context.context_version,
            context.effective_at_utc.isoformat(),
            context.semantic_fingerprint,
            [_fact_material(fact) for fact in material_facts],
        ],
        "status": status,
        "reason": reason,
        "skipped": [item.model_dump(mode="json") for item in skipped],
        "ineligible": [item.model_dump(mode="json") for item in ineligible],
        "eligible": [item.model_dump(mode="json") for item in eligible],
        "closed_authority_classes": CLOSED_AUTHORITY_CLASSES,
    }
    return sha256(_canonical_json(material).encode("utf-8")).hexdigest()


def _authority_error(
    posture: PosturePermission,
    context: EligibilityContext,
) -> str | None:
    if not all((posture.posture_id, posture.posture_version, posture.semantic_fingerprint)):
        return "invalid_posture_authority"
    if not _is_utc(posture.effective_at_utc):
        return "invalid_posture_authority"
    if not all((context.context_id, context.context_version, context.semantic_fingerprint)):
        return "invalid_eligibility_context"
    if not _is_utc(context.effective_at_utc):
        return "invalid_eligibility_context"
    for fact_ref, fact in context.facts.items():
        if (
            fact_ref != fact.fact_ref
            or not all((fact.owner_id, fact.contract_version, fact.semantic_fingerprint))
            or not _is_utc(fact.effective_at_utc)
        ):
            return "invalid_required_fact_authority"
    return None


def _required_fact_refs(
    definitions: tuple[PlaybookDefinition, ...],
) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                constraint.fact_ref
                for definition in definitions
                if definition.enabled
                for constraint in definition.constraints
                if constraint.required
            }
        )
    )


def _material_fact_refs(
    definitions: tuple[PlaybookDefinition, ...],
    context: EligibilityContext,
) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                constraint.fact_ref
                for definition in definitions
                if definition.enabled
                for constraint in definition.constraints
                if constraint.fact_ref in context.facts
            }
        )
    )


def _accepted(
    *,
    decision_id: str,
    catalogue: PlaybookCatalogue,
    posture: PosturePermission,
    context: EligibilityContext,
    status: str,
    reason: str | None,
    skipped: tuple[DefinitionDisposition, ...],
    ineligible: tuple[DefinitionDisposition, ...],
    eligible: tuple[EligibleCandidate, ...],
    material_facts: tuple[FactAuthority, ...],
) -> EligibilityDecision:
    fingerprint = _decision_fingerprint(
        catalogue=catalogue,
        posture=posture,
        context=context,
        status=status,
        reason=reason,
        skipped=skipped,
        ineligible=ineligible,
        eligible=eligible,
        material_facts=material_facts,
    )
    return EligibilityDecision(
        decision_id=decision_id,
        semantic_fingerprint=fingerprint,
        status=status,
        reason=reason,
        catalogue_id=catalogue.catalogue_id,
        catalogue_version=catalogue.catalogue_version,
        catalogue_schema_version=catalogue.schema_version,
        authority_id=catalogue.authority_id,
        authority_version=catalogue.authority_version,
        eligibility_law_version=catalogue.eligibility_law_version,
        catalogue_fingerprint=catalogue.catalogue_fingerprint,
        catalogue_promotion_lineage=catalogue.promotion_lineage,
        posture_id=posture.posture_id,
        posture_version=posture.posture_version,
        posture_status=posture.status,
        posture_effective_at_utc=posture.effective_at_utc,
        posture_fingerprint=posture.semantic_fingerprint,
        context_id=context.context_id,
        context_version=context.context_version,
        context_effective_at_utc=context.effective_at_utc,
        context_fingerprint=context.semantic_fingerprint,
        material_fact_lineage=material_facts,
        skipped_definitions=skipped,
        ineligible_definitions=ineligible,
        eligible_candidates=eligible,
        eligibility_lead=eligible[0] if eligible else None,
    )


class EligibilityResolver:
    """Resolve one exact M08 catalogue without hidden state or side effects."""

    def resolve(
        self,
        catalogue: PlaybookCatalogue | None,
        posture: PosturePermission | dict[str, Any] | None,
        context: EligibilityContext | dict[str, Any] | None,
        *,
        decision_id: str,
        caller_candidate_order: tuple[str, ...] = (),
    ) -> EligibilityDecision:
        del caller_candidate_order
        if not isinstance(decision_id, str) or not decision_id:
            raise ValueError("decision_id_required")
        if catalogue is None:
            return _rejected(decision_id=decision_id, reason="catalogue_authority_missing")
        try:
            authority = _validated_catalogue(catalogue)
        except (ValidationError, TypeError, ValueError):
            return _rejected(decision_id=decision_id, reason="invalid_catalogue_authority")
        if posture is None:
            return _rejected(decision_id=decision_id, reason="posture_authority_missing")
        try:
            governed_posture = _validated_posture(posture)
        except (ValidationError, TypeError, ValueError):
            return _rejected(decision_id=decision_id, reason="invalid_posture_authority")
        if context is None:
            return _rejected(decision_id=decision_id, reason="eligibility_context_missing")
        try:
            governed_context = _validated_context(context)
        except (ValidationError, TypeError, ValueError):
            return _rejected(decision_id=decision_id, reason="invalid_eligibility_context")
        error = _authority_error(governed_posture, governed_context)
        if error is not None:
            return _rejected(decision_id=decision_id, reason=error)

        definitions = tuple(sorted(authority.definitions, key=_definition_key))
        required_refs = _required_fact_refs(definitions)
        missing = next(
            (fact_ref for fact_ref in required_refs if fact_ref not in governed_context.facts),
            None,
        )
        if missing is not None:
            return _rejected(decision_id=decision_id, reason="missing_required_fact")
        material_refs = _material_fact_refs(definitions, governed_context)
        material_facts = tuple(governed_context.facts[fact_ref] for fact_ref in material_refs)

        skipped = tuple(
            _disposition(definition, "disabled")
            for definition in definitions
            if not definition.enabled
        )
        enabled = tuple(definition for definition in definitions if definition.enabled)
        if governed_posture.status == "blocked":
            return _accepted(
                decision_id=decision_id,
                catalogue=authority,
                posture=governed_posture,
                context=governed_context,
                status="stand_down_posture_blocked",
                reason="posture_blocked",
                skipped=skipped,
                ineligible=(),
                eligible=(),
                material_facts=material_facts,
            )
        if not enabled:
            return _accepted(
                decision_id=decision_id,
                catalogue=authority,
                posture=governed_posture,
                context=governed_context,
                status="stand_down_no_candidate_families",
                reason="no_enabled_candidate_families",
                skipped=skipped,
                ineligible=(),
                eligible=(),
                material_facts=material_facts,
            )

        ineligible: list[DefinitionDisposition] = []
        candidates: list[EligibleCandidate] = []
        for definition in enabled:
            for constraint in definition.constraints:
                fact = governed_context.facts.get(constraint.fact_ref)
                if fact is None:
                    if constraint.required:
                        return _rejected(
                            decision_id=decision_id,
                            reason="missing_required_fact",
                        )
                    continue
                if fact.value != constraint.expected:
                    ineligible.append(_disposition(definition, "constraint_not_satisfied"))
                    break
            else:
                candidates.append(_candidate(definition))

        ordered_candidates = tuple(sorted(candidates, key=_candidate_key))
        ordered_ineligible = tuple(
            sorted(
                ineligible,
                key=lambda item: (
                    item.candidate_family_id,
                    item.candidate_family_version,
                    item.playbook_id,
                    item.playbook_version,
                    item.setup_variant_id,
                    item.setup_variant_version,
                ),
            )
        )
        if not ordered_candidates:
            return _accepted(
                decision_id=decision_id,
                catalogue=authority,
                posture=governed_posture,
                context=governed_context,
                status="stand_down_no_eligible_candidates",
                reason="no_eligible_candidates",
                skipped=skipped,
                ineligible=ordered_ineligible,
                eligible=(),
                material_facts=material_facts,
            )
        return _accepted(
            decision_id=decision_id,
            catalogue=authority,
            posture=governed_posture,
            context=governed_context,
            status="eligible",
            reason=None,
            skipped=skipped,
            ineligible=ordered_ineligible,
            eligible=ordered_candidates,
            material_facts=material_facts,
        )


__all__ = ["EligibilityResolver"]
