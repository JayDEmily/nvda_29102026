"""Reference and false-positive subjects for the bounded M08 K13 proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Final

CLOSED_AUTHORITIES: Final = (
    "candidate_expression",
    "capital",
    "broker_order",
    "position_inventory",
    "exit_close",
    "coefficient",
    "source_ingress",
    "replay",
    "transaction",
)


@dataclass(frozen=True)
class ConstraintCase:
    fact_ref: str
    operator: str
    expected: Any
    required: bool = True


@dataclass(frozen=True)
class DefinitionCase:
    playbook_id: str
    playbook_version: str
    candidate_family_id: str
    candidate_family_version: str
    setup_variant_id: str
    setup_variant_version: str
    selection_priority: int
    constraints: tuple[ConstraintCase, ...]
    enabled: bool = True
    lifecycle_intent: tuple[tuple[str, str], ...] = (
        ("horizon_class", "intraday"),
        ("handoff_schema", "m05.expression.v1"),
    )
    lifecycle_schema_version: str = "1.0.0"
    promotion_lineage: str = "workbook://playbook-definition/1.0.0"


@dataclass(frozen=True)
class CatalogueCase:
    catalogue_id: str
    catalogue_version: str
    schema_version: str
    authority_id: str
    authority_version: str
    effective_version_selector: str
    eligibility_law_version: str
    promotion_lineage: str
    definitions: tuple[DefinitionCase, ...]
    catalogue_fingerprint: str


@dataclass(frozen=True)
class PostureCase:
    posture_id: str
    posture_version: str
    status: str
    effective_at_utc: datetime
    semantic_fingerprint: str


@dataclass(frozen=True)
class FactCase:
    fact_ref: str
    owner_id: str
    contract_version: str
    effective_at_utc: datetime
    semantic_fingerprint: str
    value: Any


@dataclass(frozen=True)
class EligibilityContextCase:
    context_id: str
    context_version: str
    effective_at_utc: datetime
    semantic_fingerprint: str
    facts: dict[str, FactCase]


@dataclass(frozen=True)
class CandidateCase:
    playbook_id: str
    playbook_version: str
    candidate_family_id: str
    candidate_family_version: str
    setup_variant_id: str
    setup_variant_version: str
    selection_priority: int
    lifecycle_intent: tuple[tuple[str, str], ...]

    @property
    def identity_tuple(self) -> tuple[str, ...]:
        return (
            self.candidate_family_id,
            self.candidate_family_version,
            self.playbook_id,
            self.playbook_version,
            self.setup_variant_id,
            self.setup_variant_version,
        )


@dataclass(frozen=True)
class ReferenceDecision:
    status: str
    reason: str | None
    semantic_fingerprint: str | None
    skipped_definitions: tuple[tuple[str, str], ...]
    ineligible_definitions: tuple[tuple[str, str], ...]
    eligible_candidates: tuple[CandidateCase, ...]
    eligibility_lead: CandidateCase | None
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES
    foreign_authority_claimed: bool = False


def _definition_payload(definition: DefinitionCase) -> dict[str, Any]:
    return {
        "playbook_id": definition.playbook_id,
        "playbook_version": definition.playbook_version,
        "candidate_family_id": definition.candidate_family_id,
        "candidate_family_version": definition.candidate_family_version,
        "setup_variant_id": definition.setup_variant_id,
        "setup_variant_version": definition.setup_variant_version,
        "selection_priority": definition.selection_priority,
        "constraints": [
            {
                "fact_ref": constraint.fact_ref,
                "operator": constraint.operator,
                "expected": constraint.expected,
                "required": constraint.required,
            }
            for constraint in definition.constraints
        ],
        "enabled": definition.enabled,
        "lifecycle_intent": dict(definition.lifecycle_intent),
        "lifecycle_schema_version": definition.lifecycle_schema_version,
        "promotion_lineage": definition.promotion_lineage,
    }


def catalogue_fingerprint_for_material(
    *,
    catalogue_id: str,
    catalogue_version: str,
    schema_version: str,
    authority_id: str,
    authority_version: str,
    effective_version_selector: str,
    eligibility_law_version: str,
    promotion_lineage: str,
    definitions: tuple[DefinitionCase, ...],
) -> str:
    material = {
        "catalogue_id": catalogue_id,
        "catalogue_version": catalogue_version,
        "schema_version": schema_version,
        "authority_id": authority_id,
        "authority_version": authority_version,
        "effective_version_selector": effective_version_selector,
        "eligibility_law_version": eligibility_law_version,
        "promotion_lineage": promotion_lineage,
        "definitions": [
            _definition_payload(definition)
            for definition in sorted(
                definitions,
                key=lambda item: (
                    item.candidate_family_id,
                    item.candidate_family_version,
                    item.playbook_id,
                    item.playbook_version,
                    item.setup_variant_id,
                    item.setup_variant_version,
                ),
            )
        ],
    }
    return sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def valid_definition(
    *,
    playbook_id: str = "playbook.breakout",
    candidate_family_id: str = "family.breakout",
    setup_variant_id: str = "variant.breakout.confirmed",
    selection_priority: int = 20,
    fact_ref: str = "breakout_ready",
    expected: Any = True,
    enabled: bool = True,
) -> DefinitionCase:
    return DefinitionCase(
        playbook_id=playbook_id,
        playbook_version="1.0.0",
        candidate_family_id=candidate_family_id,
        candidate_family_version="1.0.0",
        setup_variant_id=setup_variant_id,
        setup_variant_version="1.0.0",
        selection_priority=selection_priority,
        constraints=(ConstraintCase(fact_ref, "eq", expected),),
        enabled=enabled,
    )


def valid_catalogue(*, definitions: tuple[DefinitionCase, ...] | None = None) -> CatalogueCase:
    members = (
        definitions
        if definitions is not None
        else (
            valid_definition(),
            valid_definition(
                playbook_id="playbook.reversion",
                candidate_family_id="family.reversion",
                setup_variant_id="variant.reversion.standard",
                selection_priority=10,
                fact_ref="reversion_ready",
            ),
        )
    )
    material = {
        "catalogue_id": "m08.nvda.playbooks",
        "catalogue_version": "2026.07.31.1",
        "schema_version": "1.0.0",
        "authority_id": "m08.k13",
        "authority_version": "1.0.0",
        "effective_version_selector": "promoted:2026.07.31.1",
        "eligibility_law_version": "k13.v1",
        "promotion_lineage": "workbook://playbook-catalogue/2026.07.31.1",
        "definitions": members,
    }
    return CatalogueCase(
        **material,
        catalogue_fingerprint=catalogue_fingerprint_for_material(**material),
    )


def valid_posture(*, status: str = "permitted") -> PostureCase:
    return PostureCase(
        posture_id="posture.nvda.session",
        posture_version="1.0.0",
        status=status,
        effective_at_utc=datetime(2026, 7, 31, 4, 0, tzinfo=UTC),
        semantic_fingerprint="posture-fingerprint-v1",
    )


def valid_context(*, facts: dict[str, Any] | None = None) -> EligibilityContextCase:
    effective_at = datetime(2026, 7, 31, 4, 0, tzinfo=UTC)
    raw_facts = (
        facts
        if facts is not None
        else {
            "breakout_ready": True,
            "reversion_ready": True,
            "momentum_ready": True,
        }
    )
    governed_facts = {
        fact_ref: (
            value
            if isinstance(value, FactCase)
            else FactCase(
                fact_ref=fact_ref,
                owner_id=f"owner.{fact_ref}",
                contract_version="1.0.0",
                effective_at_utc=effective_at,
                semantic_fingerprint=f"{fact_ref}-fingerprint-v1",
                value=value,
            )
        )
        for fact_ref, value in raw_facts.items()
    }
    return EligibilityContextCase(
        context_id="context.nvda.session",
        context_version="1.0.0",
        effective_at_utc=effective_at,
        semantic_fingerprint="context-fingerprint-v1",
        facts=governed_facts,
    )


def _candidate(definition: DefinitionCase) -> CandidateCase:
    return CandidateCase(
        playbook_id=definition.playbook_id,
        playbook_version=definition.playbook_version,
        candidate_family_id=definition.candidate_family_id,
        candidate_family_version=definition.candidate_family_version,
        setup_variant_id=definition.setup_variant_id,
        setup_variant_version=definition.setup_variant_version,
        selection_priority=definition.selection_priority,
        lifecycle_intent=definition.lifecycle_intent,
    )


def _utc(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() == UTC.utcoffset(None)


class ReferenceSubject:
    """Small deterministic resolver implementing only section 7.8 proof law."""

    def resolve(
        self,
        catalogue: CatalogueCase | None,
        posture: PostureCase | None,
        context: EligibilityContextCase | None,
        *,
        caller_candidate_order: tuple[str, ...] = (),
    ) -> ReferenceDecision:
        authority_error = self._validate_authority(catalogue, posture, context)
        if authority_error is not None:
            return self._rejected(authority_error)
        assert catalogue is not None and posture is not None and context is not None

        if posture.status == "blocked":
            return self._accepted(
                catalogue,
                posture,
                context,
                status="stand_down_posture_blocked",
                reason="posture_blocked",
                skipped=(),
                ineligible=(),
                eligible=(),
            )
        if posture.status != "permitted":
            return self._rejected("invalid_posture_status")

        skipped = tuple(
            (definition.playbook_id, "disabled")
            for definition in catalogue.definitions
            if not definition.enabled
        )
        enabled = tuple(definition for definition in catalogue.definitions if definition.enabled)
        if not enabled:
            return self._accepted(
                catalogue,
                posture,
                context,
                status="stand_down_no_candidate_families",
                reason="no_enabled_candidate_families",
                skipped=skipped,
                ineligible=(),
                eligible=(),
            )

        ineligible: list[tuple[str, str]] = []
        candidates: list[CandidateCase] = []
        for definition in enabled:
            for constraint in definition.constraints:
                if constraint.fact_ref not in context.facts:
                    if constraint.required:
                        return self._rejected("missing_required_fact")
                    continue
                if constraint.operator != "eq":
                    return self._rejected("unsupported_constraint_operator")
                if context.facts[constraint.fact_ref].value != constraint.expected:
                    ineligible.append((definition.playbook_id, "constraint_not_satisfied"))
                    break
            else:
                candidates.append(_candidate(definition))

        ordered = self._order_candidates(tuple(candidates), caller_candidate_order)
        if not ordered:
            return self._accepted(
                catalogue,
                posture,
                context,
                status="stand_down_no_eligible_candidates",
                reason="no_eligible_candidates",
                skipped=skipped,
                ineligible=tuple(sorted(ineligible)),
                eligible=(),
            )
        return self._accepted(
            catalogue,
            posture,
            context,
            status="eligible",
            reason=None,
            skipped=skipped,
            ineligible=tuple(sorted(ineligible)),
            eligible=ordered,
        )

    def _validate_authority(
        self,
        catalogue: CatalogueCase | None,
        posture: PostureCase | None,
        context: EligibilityContextCase | None,
    ) -> str | None:
        if catalogue is None:
            return "catalogue_authority_missing"
        if not all(
            (
                catalogue.catalogue_id,
                catalogue.catalogue_version,
                catalogue.schema_version,
                catalogue.authority_id,
                catalogue.authority_version,
                catalogue.effective_version_selector,
                catalogue.eligibility_law_version,
                catalogue.promotion_lineage,
            )
        ):
            return "invalid_catalogue_authority"
        if not catalogue.definitions:
            return "empty_catalogue_invalid"
        expected_fingerprint = catalogue_fingerprint_for_material(
            catalogue_id=catalogue.catalogue_id,
            catalogue_version=catalogue.catalogue_version,
            schema_version=catalogue.schema_version,
            authority_id=catalogue.authority_id,
            authority_version=catalogue.authority_version,
            effective_version_selector=catalogue.effective_version_selector,
            eligibility_law_version=catalogue.eligibility_law_version,
            promotion_lineage=catalogue.promotion_lineage,
            definitions=catalogue.definitions,
        )
        if catalogue.catalogue_fingerprint != expected_fingerprint:
            return "catalogue_fingerprint_mismatch"
        playbook_ids = {
            (definition.playbook_id, definition.playbook_version)
            for definition in catalogue.definitions
        }
        family_ids = {
            (definition.candidate_family_id, definition.candidate_family_version)
            for definition in catalogue.definitions
        }
        if len(playbook_ids) != len(catalogue.definitions):
            return "duplicate_playbook_identity"
        if len(family_ids) != len(catalogue.definitions):
            return "duplicate_candidate_family_identity"
        if any(
            not all(
                (
                    definition.playbook_id,
                    definition.playbook_version,
                    definition.candidate_family_id,
                    definition.candidate_family_version,
                    definition.setup_variant_id,
                    definition.setup_variant_version,
                    definition.lifecycle_schema_version,
                    definition.promotion_lineage,
                )
            )
            or not isinstance(definition.selection_priority, int)
            or not definition.constraints
            for definition in catalogue.definitions
        ):
            return "invalid_playbook_definition"
        if posture is None:
            return "posture_authority_missing"
        if not all(
            (
                posture.posture_id,
                posture.posture_version,
                posture.semantic_fingerprint,
            )
        ) or not _utc(posture.effective_at_utc):
            return "invalid_posture_authority"
        if context is None:
            return "eligibility_context_missing"
        if not all(
            (
                context.context_id,
                context.context_version,
                context.semantic_fingerprint,
            )
        ) or not _utc(context.effective_at_utc):
            return "invalid_eligibility_context"
        if any(
            fact_ref != fact.fact_ref
            or not all(
                (
                    fact.owner_id,
                    fact.contract_version,
                    fact.semantic_fingerprint,
                )
            )
            or not _utc(fact.effective_at_utc)
            for fact_ref, fact in context.facts.items()
        ):
            return "invalid_required_fact_authority"
        return None

    def _order_candidates(
        self,
        candidates: tuple[CandidateCase, ...],
        caller_candidate_order: tuple[str, ...],
    ) -> tuple[CandidateCase, ...]:
        del caller_candidate_order
        return tuple(
            sorted(
                candidates,
                key=lambda item: (item.selection_priority, *item.identity_tuple),
            )
        )

    @staticmethod
    def _rejected(reason: str) -> ReferenceDecision:
        return ReferenceDecision(
            status="rejected",
            reason=reason,
            semantic_fingerprint=None,
            skipped_definitions=(),
            ineligible_definitions=(),
            eligible_candidates=(),
            eligibility_lead=None,
        )

    def _accepted(
        self,
        catalogue: CatalogueCase,
        posture: PostureCase,
        context: EligibilityContextCase,
        *,
        status: str,
        reason: str | None,
        skipped: tuple[tuple[str, str], ...],
        ineligible: tuple[tuple[str, str], ...],
        eligible: tuple[CandidateCase, ...],
    ) -> ReferenceDecision:
        lead = eligible[0] if eligible else None
        material = {
            "catalogue": [
                catalogue.catalogue_id,
                catalogue.catalogue_version,
                catalogue.schema_version,
                catalogue.authority_id,
                catalogue.authority_version,
                catalogue.eligibility_law_version,
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
                [
                    (
                        fact_ref,
                        fact.owner_id,
                        fact.contract_version,
                        fact.effective_at_utc.isoformat(),
                        fact.semantic_fingerprint,
                        fact.value,
                    )
                    for fact_ref, fact in sorted(context.facts.items())
                ],
            ],
            "status": status,
            "reason": reason,
            "skipped": skipped,
            "ineligible": ineligible,
            "eligible": [
                {
                    "identity": candidate.identity_tuple,
                    "selection_priority": candidate.selection_priority,
                    "lifecycle_intent": candidate.lifecycle_intent,
                }
                for candidate in eligible
            ],
            "closed_authority_classes": CLOSED_AUTHORITIES,
        }
        fingerprint = sha256(
            json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return ReferenceDecision(
            status=status,
            reason=reason,
            semantic_fingerprint=fingerprint,
            skipped_definitions=skipped,
            ineligible_definitions=ineligible,
            eligible_candidates=eligible,
            eligibility_lead=lead,
        )


class CallerOrderSubject(ReferenceSubject):
    def _order_candidates(
        self,
        candidates: tuple[CandidateCase, ...],
        caller_candidate_order: tuple[str, ...],
    ) -> tuple[CandidateCase, ...]:
        rank = {candidate_id: index for index, candidate_id in enumerate(caller_candidate_order)}
        return tuple(sorted(candidates, key=lambda item: rank.get(item.candidate_family_id, 999)))


class MissingCatalogueAsEmptySubject(ReferenceSubject):
    def resolve(self, catalogue, posture, context, **kwargs):
        if catalogue is None:
            return ReferenceDecision(
                "stand_down_no_candidate_families",
                "no_enabled_candidate_families",
                "fabricated-fingerprint",
                (),
                (),
                (),
                None,
            )
        return super().resolve(catalogue, posture, context, **kwargs)


class PostureBlockIgnoredSubject(ReferenceSubject):
    def resolve(self, catalogue, posture, context, **kwargs):
        if posture is not None and posture.status == "blocked":
            posture = replace(posture, status="permitted")
        return super().resolve(catalogue, posture, context, **kwargs)


class CatalogueOrderTieSubject(ReferenceSubject):
    def _order_candidates(self, candidates, caller_candidate_order):
        del caller_candidate_order
        return tuple(sorted(candidates, key=lambda item: item.selection_priority))


class ForeignAuthorityClaimSubject(ReferenceSubject):
    def resolve(self, catalogue, posture, context, **kwargs):
        decision = super().resolve(catalogue, posture, context, **kwargs)
        if decision.status != "rejected":
            return replace(
                decision,
                closed_authority_classes=tuple(
                    item for item in decision.closed_authority_classes if item != "capital"
                ),
                foreign_authority_claimed=True,
            )
        return decision


MUTANTS: Final = {
    "caller_order": CallerOrderSubject,
    "missing_catalogue_as_empty": MissingCatalogueAsEmptySubject,
    "posture_block_ignored": PostureBlockIgnoredSubject,
    "catalogue_order_tie": CatalogueOrderTieSubject,
    "foreign_authority_claim": ForeignAuthorityClaimSubject,
}


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m08_playbook_catalogue")
    required = (
        "PlaybookDefinition",
        "PlaybookCatalogue",
        "EligibilityDecision",
        "EligibilityResolver",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise AssertionError(f"canonical M08 package is missing exports: {missing}")
    return {name: getattr(module, name) for name in required}


def production_definition_payload(
    definition: DefinitionCase | None = None,
) -> dict[str, Any]:
    item = definition or valid_definition()
    return _definition_payload(item)


def production_catalogue_payload(
    definitions: tuple[DefinitionCase, ...] | None = None,
) -> dict[str, Any]:
    catalogue = valid_catalogue(definitions=definitions)
    return {
        "catalogue_id": catalogue.catalogue_id,
        "catalogue_version": catalogue.catalogue_version,
        "schema_version": catalogue.schema_version,
        "authority_id": catalogue.authority_id,
        "authority_version": catalogue.authority_version,
        "effective_version_selector": catalogue.effective_version_selector,
        "eligibility_law_version": catalogue.eligibility_law_version,
        "promotion_lineage": catalogue.promotion_lineage,
        "definitions": [production_definition_payload(item) for item in catalogue.definitions],
        "catalogue_fingerprint": catalogue.catalogue_fingerprint,
    }


def production_posture_payload(*, status: str = "permitted") -> dict[str, Any]:
    posture = valid_posture(status=status)
    return {
        "posture_id": posture.posture_id,
        "posture_version": posture.posture_version,
        "status": posture.status,
        "effective_at_utc": posture.effective_at_utc,
        "semantic_fingerprint": posture.semantic_fingerprint,
    }


def production_context_payload(*, facts: dict[str, Any] | None = None) -> dict[str, Any]:
    context = valid_context(facts=facts)
    return {
        "context_id": context.context_id,
        "context_version": context.context_version,
        "effective_at_utc": context.effective_at_utc,
        "semantic_fingerprint": context.semantic_fingerprint,
        "facts": {
            fact_ref: {
                "fact_ref": fact.fact_ref,
                "owner_id": fact.owner_id,
                "contract_version": fact.contract_version,
                "effective_at_utc": fact.effective_at_utc,
                "semantic_fingerprint": fact.semantic_fingerprint,
                "value": fact.value,
            }
            for fact_ref, fact in context.facts.items()
        },
    }
