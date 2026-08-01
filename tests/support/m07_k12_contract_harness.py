"""Reference and false-positive subjects for the bounded M07 K12 proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any, Final

CLOSED_AUTHORITIES: Final = (
    "capital",
    "playbook",
    "execution",
    "lifecycle",
    "replay",
    "transaction",
    "downstream_state_mutation",
)


@dataclass(frozen=True)
class CoefficientCase:
    coefficient_id: str
    coefficient_version: str
    owner_stage: str
    baseline: Decimal
    lower: Decimal
    upper: Decimal


@dataclass(frozen=True)
class ModifierCase:
    modifier_id: str
    modifier_version: str
    target: str
    fact_ref: str
    precedence: int
    operator: str
    operand: Decimal
    conflicts: tuple[str, ...] = ()
    kill_switch: bool = False


@dataclass(frozen=True)
class BundleCase:
    bundle_id: str
    bundle_version: str
    schema_version: str
    authority_id: str
    authority_version: str
    resolution_law_version: str
    owner_stage: str
    coefficients: tuple[CoefficientCase, ...]
    modifiers: tuple[ModifierCase, ...]


@dataclass(frozen=True)
class InputFactsCase:
    context_id: str
    context_version: str
    effective_at_utc: datetime
    fingerprint: str
    facts: dict[str, bool]


@dataclass(frozen=True)
class CoefficientResult:
    coefficient_id: str
    baseline: Decimal
    pre_clamp_candidate: Decimal
    lower: Decimal
    upper: Decimal
    effective: Decimal
    bound_disposition: str


@dataclass(frozen=True)
class ReferenceDecision:
    status: str
    reason: str | None
    semantic_fingerprint: str | None
    applied_modifiers: tuple[str, ...]
    skipped_modifiers: tuple[tuple[str, str], ...]
    coefficient_results: tuple[CoefficientResult, ...]
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES


@dataclass(frozen=True)
class ReferenceReceipt:
    receipt_id: str
    application_id: str
    source_decision_fingerprint: str
    decision_status: str
    emitted_at_utc: datetime
    no_op_class: str | None
    external_mutation_proven: bool
    closed_authority_classes: tuple[str, ...]


def _fingerprint_payload(
    bundle: BundleCase,
    facts: InputFactsCase,
    status: str,
    applied: tuple[str, ...],
    skipped: tuple[tuple[str, str], ...],
    results: tuple[CoefficientResult, ...],
) -> str:
    payload = {
        "bundle": [
            bundle.bundle_id,
            bundle.bundle_version,
            bundle.schema_version,
            bundle.authority_id,
            bundle.authority_version,
            bundle.resolution_law_version,
        ],
        "owner_stage": bundle.owner_stage,
        "input": [
            facts.context_id,
            facts.context_version,
            facts.effective_at_utc.isoformat(),
            facts.fingerprint,
        ],
        "status": status,
        "applied": applied,
        "skipped": skipped,
        "results": [
            {
                "coefficient_id": result.coefficient_id,
                "baseline": str(result.baseline),
                "pre_clamp_candidate": str(result.pre_clamp_candidate),
                "lower": str(result.lower),
                "upper": str(result.upper),
                "effective": str(result.effective),
                "bound_disposition": result.bound_disposition,
            }
            for result in results
        ],
        "closed_authority_classes": CLOSED_AUTHORITIES,
    }
    return sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


class ReferenceSubject:
    """Small deterministic resolver implementing only section 7.7 proof law."""

    def resolve(
        self,
        bundle: BundleCase | None,
        facts: InputFactsCase,
        *,
        caller_modifier_order: tuple[str, ...] = (),
    ) -> ReferenceDecision:
        del caller_modifier_order
        if bundle is None:
            return ReferenceDecision("rejected", "bundle_authority_missing", None, (), (), ())
        if not bundle.bundle_id or not bundle.bundle_version or not bundle.coefficients:
            return ReferenceDecision("rejected", "invalid_policy_bundle", None, (), (), ())
        if (
            facts.effective_at_utc.tzinfo is None
            or facts.effective_at_utc.utcoffset() != UTC.utcoffset(None)
        ):
            return ReferenceDecision("rejected", "invalid_input_state_time", None, (), (), ())

        coefficients = {item.coefficient_id: item for item in bundle.coefficients}
        if len(coefficients) != len(bundle.coefficients):
            return ReferenceDecision("rejected", "duplicate_coefficient_identity", None, (), (), ())
        if any(
            coefficient.owner_stage != bundle.owner_stage
            or coefficient.lower > coefficient.baseline
            or coefficient.baseline > coefficient.upper
            for coefficient in bundle.coefficients
        ):
            return ReferenceDecision("rejected", "invalid_coefficient_authority", None, (), (), ())

        if not bundle.modifiers:
            results = self._baseline_results(bundle)
            return self._accepted(bundle, facts, "no_modifier_members", (), (), results)

        applicable: list[ModifierCase] = []
        skipped: list[tuple[str, str]] = []
        for modifier in bundle.modifiers:
            if modifier.target not in coefficients or modifier.target == "":
                return ReferenceDecision("rejected", "invalid_modifier_target", None, (), (), ())
            if modifier.fact_ref not in facts.facts:
                return ReferenceDecision("rejected", "missing_applicability_fact", None, (), (), ())
            if facts.facts[modifier.fact_ref]:
                applicable.append(modifier)
            else:
                skipped.append((modifier.modifier_id, "not_applicable"))

        if not applicable:
            results = self._baseline_results(bundle)
            return self._accepted(
                bundle,
                facts,
                "no_applicable_modifiers",
                (),
                tuple(sorted(skipped)),
                results,
            )

        kill_targets = {modifier.target for modifier in applicable if modifier.kill_switch}
        dominated = [
            modifier
            for modifier in applicable
            if not modifier.kill_switch and modifier.target in kill_targets
        ]
        skipped.extend((modifier.modifier_id, "dominated_by_kill_switch") for modifier in dominated)
        applicable = [
            modifier
            for modifier in applicable
            if modifier.kill_switch or modifier.target not in kill_targets
        ]
        ordered = sorted(
            applicable,
            key=lambda modifier: (
                modifier.precedence,
                modifier.modifier_id,
                modifier.modifier_version,
            ),
        )
        for index, modifier in enumerate(ordered):
            for other in ordered[index + 1 :]:
                if modifier.target != other.target:
                    continue
                incompatible = (
                    other.modifier_id in modifier.conflicts
                    or modifier.modifier_id in other.conflicts
                )
                if incompatible and modifier.precedence == other.precedence:
                    return ReferenceDecision(
                        "rejected", "unresolved_modifier_conflict", None, (), (), ()
                    )

        values = {item.coefficient_id: item.baseline for item in bundle.coefficients}
        applied_ids: list[str] = []
        for modifier in ordered:
            current = values[modifier.target]
            if modifier.kill_switch:
                candidate = Decimal("0")
            elif modifier.operator == "add":
                candidate = current + modifier.operand
            elif modifier.operator == "multiply":
                candidate = current * modifier.operand
            elif modifier.operator == "set":
                candidate = modifier.operand
            else:
                return ReferenceDecision(
                    "rejected", "unsupported_transform_operator", None, (), (), ()
                )
            values[modifier.target] = candidate
            applied_ids.append(modifier.modifier_id)

        results = tuple(
            self._result(coefficient, values[coefficient.coefficient_id])
            for coefficient in bundle.coefficients
        )
        return self._accepted(
            bundle,
            facts,
            "applied",
            tuple(applied_ids),
            tuple(sorted(skipped)),
            results,
        )

    @staticmethod
    def _baseline_results(bundle: BundleCase) -> tuple[CoefficientResult, ...]:
        return tuple(
            CoefficientResult(
                coefficient_id=item.coefficient_id,
                baseline=item.baseline,
                pre_clamp_candidate=item.baseline,
                lower=item.lower,
                upper=item.upper,
                effective=item.baseline,
                bound_disposition="within_bounds",
            )
            for item in bundle.coefficients
        )

    @staticmethod
    def _result(item: CoefficientCase, candidate: Decimal) -> CoefficientResult:
        effective = min(max(candidate, item.lower), item.upper)
        if effective == candidate:
            disposition = "within_bounds"
        elif effective == item.lower:
            disposition = "clamped_lower"
        else:
            disposition = "clamped_upper"
        return CoefficientResult(
            coefficient_id=item.coefficient_id,
            baseline=item.baseline,
            pre_clamp_candidate=candidate,
            lower=item.lower,
            upper=item.upper,
            effective=effective,
            bound_disposition=disposition,
        )

    @staticmethod
    def _accepted(
        bundle: BundleCase,
        facts: InputFactsCase,
        status: str,
        applied: tuple[str, ...],
        skipped: tuple[tuple[str, str], ...],
        results: tuple[CoefficientResult, ...],
    ) -> ReferenceDecision:
        return ReferenceDecision(
            status=status,
            reason=None,
            semantic_fingerprint=_fingerprint_payload(
                bundle, facts, status, applied, skipped, results
            ),
            applied_modifiers=applied,
            skipped_modifiers=skipped,
            coefficient_results=results,
        )

    @staticmethod
    def build_receipt(
        decision: ReferenceDecision,
        *,
        receipt_id: str,
        application_id: str,
        emitted_at_utc: datetime,
    ) -> ReferenceReceipt | None:
        if decision.status == "rejected" or decision.semantic_fingerprint is None:
            return None
        no_op_class = (
            decision.status
            if decision.status in {"no_modifier_members", "no_applicable_modifiers"}
            else None
        )
        return ReferenceReceipt(
            receipt_id=receipt_id,
            application_id=application_id,
            source_decision_fingerprint=decision.semantic_fingerprint,
            decision_status=decision.status,
            emitted_at_utc=emitted_at_utc,
            no_op_class=no_op_class,
            external_mutation_proven=False,
            closed_authority_classes=CLOSED_AUTHORITIES,
        )


class CallerOrderMutant(ReferenceSubject):
    def resolve(self, bundle, facts, *, caller_modifier_order=()):
        if bundle is None or not caller_modifier_order:
            return super().resolve(bundle, facts, caller_modifier_order=caller_modifier_order)
        by_id = {modifier.modifier_id: modifier for modifier in bundle.modifiers}
        ordered = tuple(
            replace(by_id[item], precedence=index)
            for index, item in enumerate(caller_modifier_order)
            if item in by_id
        )
        return super().resolve(
            replace(bundle, modifiers=ordered),
            facts,
            caller_modifier_order=caller_modifier_order,
        )


class MissingBundleAsEmptyMutant(ReferenceSubject):
    def resolve(self, bundle, facts, *, caller_modifier_order=()):
        if bundle is None:
            bundle = valid_bundle(modifiers=())
        return super().resolve(bundle, facts, caller_modifier_order=caller_modifier_order)


class ClampBeforeAlgebraMutant(ReferenceSubject):
    def resolve(self, bundle, facts, *, caller_modifier_order=()):
        decision = super().resolve(bundle, facts, caller_modifier_order=caller_modifier_order)
        if bundle is None or decision.status != "applied":
            return decision
        coefficients = {item.coefficient_id: item for item in bundle.coefficients}
        values = {item.coefficient_id: item.baseline for item in bundle.coefficients}
        for modifier in sorted(bundle.modifiers, key=lambda item: item.precedence):
            if not facts.facts.get(modifier.fact_ref, False):
                continue
            current = values[modifier.target]
            if modifier.operator == "add":
                current += modifier.operand
            elif modifier.operator == "multiply":
                current *= modifier.operand
            elif modifier.operator == "set" or modifier.kill_switch:
                current = Decimal("0") if modifier.kill_switch else modifier.operand
            item = coefficients[modifier.target]
            values[modifier.target] = min(max(current, item.lower), item.upper)
        results = tuple(
            self._result(item, values[item.coefficient_id]) for item in bundle.coefficients
        )
        return replace(decision, coefficient_results=results)


class ArbitraryConflictTieMutant(ReferenceSubject):
    def resolve(self, bundle, facts, *, caller_modifier_order=()):
        if bundle is None:
            return super().resolve(bundle, facts, caller_modifier_order=caller_modifier_order)
        stripped = tuple(replace(modifier, conflicts=()) for modifier in bundle.modifiers)
        return super().resolve(
            replace(bundle, modifiers=stripped),
            facts,
            caller_modifier_order=caller_modifier_order,
        )


class ReceiptMutationAuthorityMutant(ReferenceSubject):
    @staticmethod
    def build_receipt(decision, *, receipt_id, application_id, emitted_at_utc):
        receipt = ReferenceSubject.build_receipt(
            decision,
            receipt_id=receipt_id,
            application_id=application_id,
            emitted_at_utc=emitted_at_utc,
        )
        if receipt is None:
            return None
        return replace(receipt, external_mutation_proven=True, closed_authority_classes=())


MUTANTS: Final = {
    "caller_order": CallerOrderMutant,
    "missing_bundle_as_empty": MissingBundleAsEmptyMutant,
    "clamp_before_algebra": ClampBeforeAlgebraMutant,
    "arbitrary_conflict_tie": ArbitraryConflictTieMutant,
    "receipt_mutation_authority": ReceiptMutationAuthorityMutant,
}


def valid_facts(**updates: Any) -> InputFactsCase:
    base = InputFactsCase(
        context_id="state::posture::20260731T030000Z",
        context_version="1.0.0",
        effective_at_utc=datetime(2026, 7, 31, 3, 0, tzinfo=UTC),
        fingerprint="facts-sha256-001",
        facts={"stress": True, "volatility": True, "kill": False},
    )
    return replace(base, **updates)


def valid_bundle(*, modifiers: tuple[ModifierCase, ...] | None = None) -> BundleCase:
    coefficient = CoefficientCase(
        coefficient_id="posture.exposure_scale",
        coefficient_version="1.0.0",
        owner_stage="posture",
        baseline=Decimal("0.60"),
        lower=Decimal("0.00"),
        upper=Decimal("1.00"),
    )
    if modifiers is None:
        modifiers = (
            ModifierCase(
                modifier_id="stress_add",
                modifier_version="1.0.0",
                target=coefficient.coefficient_id,
                fact_ref="stress",
                precedence=10,
                operator="add",
                operand=Decimal("0.50"),
            ),
            ModifierCase(
                modifier_id="volatility_multiply",
                modifier_version="1.0.0",
                target=coefficient.coefficient_id,
                fact_ref="volatility",
                precedence=20,
                operator="multiply",
                operand=Decimal("2.00"),
            ),
        )
    return BundleCase(
        bundle_id="m07.posture.coefficients",
        bundle_version="2026.07.31.1",
        schema_version="1.0.0",
        authority_id="m07.k12",
        authority_version="1.0.0",
        resolution_law_version="k12.v1",
        owner_stage="posture",
        coefficients=(coefficient,),
        modifiers=modifiers,
    )


def conflict_bundle() -> BundleCase:
    first = ModifierCase(
        modifier_id="conflict_a",
        modifier_version="1.0.0",
        target="posture.exposure_scale",
        fact_ref="stress",
        precedence=10,
        operator="add",
        operand=Decimal("0.10"),
        conflicts=("conflict_b",),
    )
    second = ModifierCase(
        modifier_id="conflict_b",
        modifier_version="1.0.0",
        target="posture.exposure_scale",
        fact_ref="volatility",
        precedence=10,
        operator="multiply",
        operand=Decimal("0.50"),
        conflicts=("conflict_a",),
    )
    return valid_bundle(modifiers=(first, second))


def production_api() -> dict[str, Any]:
    module = importlib.import_module("nvda_desk.m07_coefficient_modifier_authority")
    required = (
        "PolicyBundle",
        "ModifierDecision",
        "ModifierApplicationReceipt",
        "resolve_k12",
        "build_k12_receipt",
    )
    return {name: getattr(module, name) for name in required}
