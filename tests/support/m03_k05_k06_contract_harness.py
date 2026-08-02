"""Reference and false-positive subjects for the bounded M03 K05/K06 proof."""

from __future__ import annotations

import importlib
import json
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Final

from pydantic import BaseModel, ConfigDict

CLOSED_AUTHORITIES: Final = (
    "candidate_expression",
    "risk_posture",
    "capital",
    "broker_order",
    "position_inventory",
    "exit_close",
    "lifecycle",
    "transaction",
    "replay",
)
_EFFECTIVE_AT = datetime(2026, 7, 31, 5, 0, tzinfo=UTC)


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime_must_be_timezone_aware")
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_canonical(item) for item in value]
    return value


def fingerprint(value: Any) -> str:
    material = asdict(value) if hasattr(value, "__dataclass_fields__") else value
    return sha256(
        json.dumps(_canonical(material), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


@dataclass(frozen=True)
class CaptureReferenceCase:
    capture_id: str
    source_artifact_id: str
    family_id: str = "nvda.market.snapshot"
    contract_id: str = "market.snapshot.v1"
    schema_version: str = "1.0.0"
    source_owner: str = "market"
    effective_at_utc: datetime = _EFFECTIVE_AT
    input_fingerprint: str = "a" * 64


@dataclass(frozen=True)
class FieldCandidateCase:
    candidate_id: str
    source_owner: str
    semantic_field: str
    value: Any
    source_artifact_id: str
    capture_id: str
    contract_version: str = "1.0.0"
    schema_version: str = "1.0.0"
    effective_at_utc: datetime = _EFFECTIVE_AT
    input_fingerprint: str = "a" * 64
    validation_state: str = "valid"


@dataclass(frozen=True)
class FieldPolicyCase:
    policy_id: str
    policy_version: str
    semantic_field: str
    mandatory: bool
    authoritative_owner: str | None = None
    fallback_owners: tuple[str, ...] = ()
    comparison_rule: str = "exact"


@dataclass(frozen=True)
class ResolutionCase:
    semantic_field: str
    policy_id: str
    policy_version: str
    resolution_status: str
    selected_value: Any
    selected_candidate_id: str | None
    selected_source_owner: str | None
    candidate_ids: tuple[str, ...]
    source_refs: tuple[tuple[str, str], ...]
    resolution_reason: str
    rejected_candidate_ids: tuple[str, ...]
    receipt_fingerprint: str
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES
    foreign_authority_claimed: bool = False


@dataclass(frozen=True)
class DerivationCase:
    derivation_id: str
    semantic_field: str
    derivation_version: str
    input_candidate_ids: tuple[str, ...]
    input_fingerprints: tuple[str, ...]
    value: Any
    receipt_fingerprint: str


@dataclass(frozen=True)
class EnvelopeCase:
    prepared_id: str
    source_capture_refs: tuple[CaptureReferenceCase, ...]
    input_schema_versions: tuple[tuple[str, str], ...]
    preparation_policy_version: str
    derivation_versions: tuple[tuple[str, str], ...]
    effective_at_utc: datetime
    input_fingerprint: str
    prepared_fingerprint: str
    validation_state: str
    completeness_state: str
    payload_kind: str
    payload: dict[str, Any]
    field_resolution_receipts: tuple[ResolutionCase, ...]
    derivation_receipts: tuple[DerivationCase, ...]
    closed_authority_classes: tuple[str, ...] = CLOSED_AUTHORITIES
    foreign_authority_claimed: bool = False


class ReferenceMandatoryFieldConflictError(ValueError):
    """Reference failure for an unresolved mandatory semantic field."""


class ReferenceMissingMandatoryFieldError(ValueError):
    """Reference failure for a missing mandatory semantic field."""


class ReferenceResolver:
    """Resolve one semantic field under explicit owner and equality law."""

    def resolve(
        self,
        candidates: tuple[FieldCandidateCase, ...],
        policy: FieldPolicyCase,
    ) -> ResolutionCase:
        ordered = tuple(sorted(candidates, key=lambda item: item.candidate_id))
        if any(item.semantic_field != policy.semantic_field for item in ordered):
            raise ValueError("candidate_semantic_field_mismatch")
        if len({item.candidate_id for item in ordered}) != len(ordered):
            raise ValueError("duplicate_candidate_id")
        if not ordered:
            if policy.mandatory:
                raise ReferenceMissingMandatoryFieldError(policy.semantic_field)
            return self._receipt(
                ordered,
                policy,
                status="unavailable",
                selected=None,
                reason="optional_field_unavailable",
            )
        if any(item.validation_state != "valid" for item in ordered):
            raise ValueError("invalid_field_candidate")

        values = {_json_key(item.value) for item in ordered}
        if len(values) == 1:
            return self._receipt(
                ordered,
                policy,
                status="selected",
                selected=ordered[0],
                reason="semantically_equal_coalesced",
            )

        owner_order = tuple(
            owner
            for owner in (policy.authoritative_owner, *policy.fallback_owners)
            if owner is not None
        )
        for owner in owner_order:
            owned = tuple(item for item in ordered if item.source_owner == owner)
            if len(owned) == 1:
                reason = (
                    "authoritative_owner_selected"
                    if owner == policy.authoritative_owner
                    else "fallback_owner_selected"
                )
                return self._receipt(
                    ordered,
                    policy,
                    status="selected",
                    selected=owned[0],
                    reason=reason,
                )
            if len(owned) > 1 and len({_json_key(item.value) for item in owned}) == 1:
                return self._receipt(
                    ordered,
                    policy,
                    status="selected",
                    selected=owned[0],
                    reason="authoritative_owner_equal_candidates_coalesced",
                )

        if policy.mandatory:
            raise ReferenceMandatoryFieldConflictError(policy.semantic_field)
        return self._receipt(
            ordered,
            policy,
            status="withheld",
            selected=None,
            reason="optional_field_conflict_withheld",
        )

    def _receipt(
        self,
        candidates: tuple[FieldCandidateCase, ...],
        policy: FieldPolicyCase,
        *,
        status: str,
        selected: FieldCandidateCase | None,
        reason: str,
    ) -> ResolutionCase:
        material = {
            "semantic_field": policy.semantic_field,
            "policy_id": policy.policy_id,
            "policy_version": policy.policy_version,
            "resolution_status": status,
            "selected_value": None if selected is None else selected.value,
            "selected_candidate_id": None if selected is None else selected.candidate_id,
            "selected_source_owner": None if selected is None else selected.source_owner,
            "candidate_ids": [item.candidate_id for item in candidates],
            "source_refs": [[item.source_artifact_id, item.capture_id] for item in candidates],
            "resolution_reason": reason,
            "rejected_candidate_ids": [
                item.candidate_id
                for item in candidates
                if selected is not None and item.candidate_id != selected.candidate_id
            ],
        }
        return ResolutionCase(
            semantic_field=material["semantic_field"],
            policy_id=material["policy_id"],
            policy_version=material["policy_version"],
            resolution_status=material["resolution_status"],
            selected_value=material["selected_value"],
            selected_candidate_id=material["selected_candidate_id"],
            selected_source_owner=material["selected_source_owner"],
            candidate_ids=tuple(material["candidate_ids"]),
            source_refs=tuple(tuple(item) for item in material["source_refs"]),
            resolution_reason=material["resolution_reason"],
            rejected_candidate_ids=tuple(material["rejected_candidate_ids"]),
            receipt_fingerprint=fingerprint(material),
        )


class ReferenceBuilder:
    """Build one deterministic tagged prepared envelope from admitted evidence."""

    def build(
        self,
        *,
        source_capture_refs: tuple[CaptureReferenceCase, ...],
        input_schema_versions: tuple[tuple[str, str], ...],
        preparation_policy_version: str,
        derivation_versions: tuple[tuple[str, str], ...],
        effective_at_utc: datetime,
        payload_kind: str,
        payload: dict[str, Any],
        field_resolution_receipts: tuple[ResolutionCase, ...],
        derivation_receipts: tuple[DerivationCase, ...],
    ) -> EnvelopeCase:
        if not source_capture_refs:
            raise ValueError("source_capture_refs_required")
        if not payload_kind or payload.get("kind") != payload_kind:
            raise ValueError("tagged_typed_payload_required")
        if any(not item.capture_id or not item.source_artifact_id for item in source_capture_refs):
            raise ValueError("source_and_capture_identity_required")
        declared = dict(derivation_versions)
        for receipt in derivation_receipts:
            if declared.get(receipt.semantic_field) != receipt.derivation_version:
                raise ValueError("derivation_version_or_input_provenance_missing")
            if not receipt.input_candidate_ids or not receipt.input_fingerprints:
                raise ValueError("derivation_version_or_input_provenance_missing")

        ordered_refs = tuple(
            sorted(source_capture_refs, key=lambda item: (item.capture_id, item.source_artifact_id))
        )
        ordered_resolutions = tuple(
            sorted(field_resolution_receipts, key=lambda item: item.semantic_field)
        )
        ordered_derivations = tuple(
            sorted(derivation_receipts, key=lambda item: item.semantic_field)
        )
        input_material = {
            "source_capture_refs": [asdict(item) for item in ordered_refs],
            "input_schema_versions": sorted(input_schema_versions),
        }
        input_fingerprint = fingerprint(input_material)
        prepared_material = {
            "source_capture_refs": [asdict(item) for item in ordered_refs],
            "input_schema_versions": sorted(input_schema_versions),
            "preparation_policy_version": preparation_policy_version,
            "derivation_versions": sorted(derivation_versions),
            "effective_at_utc": effective_at_utc,
            "input_fingerprint": input_fingerprint,
            "validation_state": "valid",
            "completeness_state": "complete",
            "payload_kind": payload_kind,
            "payload": payload,
            "field_resolution_receipts": [asdict(item) for item in ordered_resolutions],
            "derivation_receipts": [asdict(item) for item in ordered_derivations],
        }
        prepared_fingerprint = fingerprint(prepared_material)
        return EnvelopeCase(
            prepared_id=f"prepared:{prepared_fingerprint[:24]}",
            source_capture_refs=ordered_refs,
            input_schema_versions=tuple(sorted(input_schema_versions)),
            preparation_policy_version=preparation_policy_version,
            derivation_versions=tuple(sorted(derivation_versions)),
            effective_at_utc=effective_at_utc,
            input_fingerprint=input_fingerprint,
            prepared_fingerprint=prepared_fingerprint,
            validation_state="valid",
            completeness_state="complete",
            payload_kind=payload_kind,
            payload=dict(payload),
            field_resolution_receipts=ordered_resolutions,
            derivation_receipts=ordered_derivations,
        )


def _json_key(value: Any) -> str:
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))


class _StrictPreparedSourcePayload(BaseModel):
    """Typed M01 source payload for packet-surface proof fixtures."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    spot_price: float
    prior_close: float
    runtime_bar_time_utc: datetime


def strict_production_envelope(
    *,
    source_artifact_id: str = "source.market.1",
    capture_id: str = "capture.market.1",
    spot_price: float = 100.0,
    prior_close: float = 90.0,
    runtime_bar_time_utc: datetime = _EFFECTIVE_AT,
    limitations: tuple[str, ...] = (),
):
    """Build an M03 envelope from exact admitted M01 evidence.

    This helper exists for packet-surface tests whose proposition starts after M03.
    It deliberately uses the production M01 and M03 seams so those tests cannot
    recreate the prohibited caller-authored prepared-payload path.
    """

    from nvda_desk import m01_source_admission as m01
    from nvda_desk import m03_preparation as m03

    payload = _StrictPreparedSourcePayload(
        spot_price=spot_price,
        prior_close=prior_close,
        runtime_bar_time_utc=runtime_bar_time_utc,
    )
    semantic_bindings = (
        m01.SourceSemanticBinding(
            semantic_field="spot_price",
            payload_field="spot_price",
            value_type="float",
            unit="USD",
            requirement=m01.SourceFactRequirement.REQUIRED,
        ),
        m01.SourceSemanticBinding(
            semantic_field="prior_close",
            payload_field="prior_close",
            value_type="float",
            unit="USD",
            requirement=m01.SourceFactRequirement.REQUIRED,
        ),
        m01.SourceSemanticBinding(
            semantic_field="runtime_bar_time_utc",
            payload_field="runtime_bar_time_utc",
            value_type="datetime",
            unit=None,
            requirement=m01.SourceFactRequirement.REQUIRED,
        ),
    )
    family_id = f"strict_packet_surface::{source_artifact_id}"
    service = m01.SourceAdmissionService(
        registry=m01.SourceFamilyRegistry.build(
            [
                m01.SourceFamilyContract(
                    family_id=family_id,
                    contract_id=f"{family_id}.v1",
                    schema_version="1.0.0",
                    payload_model=_StrictPreparedSourcePayload,
                    providers=(
                        m01.SourceProviderContract(
                            provider_id="market",
                            acquisition_channels=("recorded_api_response",),
                        ),
                    ),
                    source_identifier=m01.SourceIdentifierContract(
                        requirement=m01.SourceFactRequirement.REQUIRED,
                        owner="market",
                        namespace="market/strict-packet-surface",
                        uniqueness_scope="market/strict-packet-surface",
                        stability_rule="stable_for_source_object_lifetime",
                        generation_rule="issued_by_upstream_provider",
                    ),
                    source_time_kind=m01.SourceTimeKind.INSTANT,
                    downstream_owner=m01.SourceDownstreamOwner.M03,
                    output_contract=m01.SourceOutputContract.RAW_SIGNAL_BATCH,
                    signal_family_id=family_id,
                    permitted_limitations=limitations,
                    semantic_bindings=semantic_bindings,
                )
            ]
        ),
        capture_id_factory=lambda _: capture_id,
        source_artifact_id_factory=lambda *_: source_artifact_id,
    )
    result = service.admit(
        m01.SourceAdmissionRequest(
            family_id=family_id,
            contract_id=f"{family_id}.v1",
            schema_version="1.0.0",
            provider_id="market",
            acquisition_channel="recorded_api_response",
            source_object_id=f"provider::{source_artifact_id}",
            observed_at_utc=runtime_bar_time_utc,
            captured_at_utc=runtime_bar_time_utc,
            captured_material=payload.model_dump_json().encode(),
            typed_payload=payload,
            declared_limitations=limitations,
        )
    )
    if result.status != "accepted":
        raise AssertionError(f"strict_m01_fixture_not_admitted:{result}")

    allow_degraded = bool(limitations)
    policies = tuple(
        m03.FieldResolutionPolicy(
            policy_id=f"m03.policy.{binding.semantic_field}",
            policy_version="1.0.0",
            output_contract_version="1.0.0",
            semantic_field=binding.semantic_field,
            mandatory=True,
            admitted_source_roles=("market",),
            value_type=binding.value_type,
            unit=binding.unit,
            temporal_comparison_rule="exact_effective_interval",
            comparison_rule="exact",
            authoritative_owner="market",
            allow_degraded_candidates=allow_degraded,
            unresolved_consequence="withhold",
            optional_absence_consequence="unavailable",
        )
        for binding in semantic_bindings
    )
    return m03.PreparedDataBuilder().build(
        source_artifacts=(result.source_artifact,),
        calendar_projections=(),
        field_resolution_policies=policies,
        derivation_rules=(),
        schema_version="1.0.0",
        preparation_policy_version="prepare.1.0.0",
        alignment_policy_version="alignment.1.0.0",
        fingerprint_policy_version="sha256.1.0.0",
        canonicalisation_version="json.1.0.0",
        effective_at_utc=runtime_bar_time_utc,
        payload_schema_version="1.0.0",
    )


def valid_capture_reference(
    *, capture_id: str = "capture.market.1", source_artifact_id: str = "source.market.1"
) -> CaptureReferenceCase:
    return CaptureReferenceCase(
        capture_id=capture_id,
        source_artifact_id=source_artifact_id,
    )


def valid_candidate(
    *,
    candidate_id: str = "market.spot",
    source_owner: str = "market",
    value: Any = 101.0,
    source_artifact_id: str = "source.market.1",
    capture_id: str = "capture.market.1",
    semantic_field: str = "spot_price",
) -> FieldCandidateCase:
    return FieldCandidateCase(
        candidate_id=candidate_id,
        source_owner=source_owner,
        semantic_field=semantic_field,
        value=value,
        source_artifact_id=source_artifact_id,
        capture_id=capture_id,
    )


def valid_policy(
    *,
    mandatory: bool = True,
    authoritative_owner: str | None = None,
    fallback_owners: tuple[str, ...] = (),
) -> FieldPolicyCase:
    return FieldPolicyCase(
        policy_id="policy.spot",
        policy_version="1.0.0",
        semantic_field="spot_price",
        mandatory=mandatory,
        authoritative_owner=authoritative_owner,
        fallback_owners=fallback_owners,
    )


def valid_derivation() -> DerivationCase:
    material = {
        "derivation_id": "derivation.return.1",
        "semantic_field": "nvda_return_pct",
        "derivation_version": "1.0.0",
        "input_candidate_ids": ["market.spot", "market.prior_close"],
        "input_fingerprints": ["a" * 64, "b" * 64],
        "value": 0.01,
    }
    return DerivationCase(
        derivation_id=material["derivation_id"],
        semantic_field=material["semantic_field"],
        derivation_version=material["derivation_version"],
        input_candidate_ids=tuple(material["input_candidate_ids"]),
        input_fingerprints=tuple(material["input_fingerprints"]),
        value=material["value"],
        receipt_fingerprint=fingerprint(material),
    )


class CallerOrderMutant(ReferenceResolver):
    def resolve(self, candidates, policy):  # type: ignore[no-untyped-def]
        if not candidates:
            return super().resolve(candidates, policy)
        ordered = tuple(candidates)
        return self._receipt(
            ordered,
            policy,
            status="selected",
            selected=ordered[0],
            reason="caller_order_selected",
        )


class LineageDroppingMutant(ReferenceResolver):
    def resolve(self, candidates, policy):  # type: ignore[no-untyped-def]
        result = super().resolve(candidates, policy)
        if result.selected_candidate_id is None:
            return result
        return replace(
            result,
            candidate_ids=(result.selected_candidate_id,),
            source_refs=(result.source_refs[0],),
        )


class FabricatedCaptureMutant(ReferenceBuilder):
    def build(self, **kwargs):  # type: ignore[no-untyped-def]
        refs = tuple(
            replace(item, capture_id=item.input_fingerprint)
            for item in kwargs["source_capture_refs"]
        )
        kwargs["source_capture_refs"] = refs
        return super().build(**kwargs)


class UntaggedPayloadMutant(ReferenceBuilder):
    def build(self, **kwargs):  # type: ignore[no-untyped-def]
        payload = dict(kwargs["payload"])
        payload.setdefault("kind", kwargs["payload_kind"])
        kwargs["payload"] = payload
        return super().build(**kwargs)


class DerivationDroppingMutant(ReferenceBuilder):
    def build(self, **kwargs):  # type: ignore[no-untyped-def]
        kwargs["derivation_versions"] = ()
        kwargs["derivation_receipts"] = ()
        return super().build(**kwargs)


class ForeignAuthorityMutant(ReferenceBuilder):
    def build(self, **kwargs):  # type: ignore[no-untyped-def]
        result = super().build(**kwargs)
        return replace(
            result,
            closed_authority_classes=tuple(
                item for item in result.closed_authority_classes if item != "capital"
            ),
            foreign_authority_claimed=True,
        )


MUTANTS: Final = {
    "caller_order": CallerOrderMutant,
    "lineage_dropping": LineageDroppingMutant,
    "fabricated_capture": FabricatedCaptureMutant,
    "untagged_payload": UntaggedPayloadMutant,
    "derivation_dropping": DerivationDroppingMutant,
    "foreign_authority": ForeignAuthorityMutant,
}


def production_api() -> dict[str, Any]:
    contracts = importlib.import_module("nvda_desk.contracts.prepared_data")
    resolution = importlib.import_module("nvda_desk.preparation.field_resolution")
    preparation = importlib.import_module("nvda_desk.m03_preparation")
    names = (
        "SourceCaptureReference",
        "PreparedRuntimePayloadV1",
        "PreparedDerivationRule",
        "DerivationReceipt",
        "PreparedDataEnvelope",
    )
    api = {name: getattr(contracts, name) for name in names}
    for name in (
        "FieldCandidate",
        "FieldResolutionPolicy",
        "FieldResolutionReceipt",
        "MandatoryFieldConflictError",
        "MissingMandatoryFieldError",
        "resolve_canonical_field",
    ):
        api[name] = getattr(resolution, name)
    api["PreparedDataBuilder"] = getattr(preparation, "PreparedDataBuilder")
    return api


def production_candidate_payload(candidate: FieldCandidateCase) -> dict[str, Any]:
    payload = asdict(candidate)
    payload.update(
        candidate_state="value",
        value_type="float",
        unit=None,
        effective_to_utc=None,
        normalisation_operations=(),
        limitations=(),
    )
    return payload


def production_policy_payload(policy: FieldPolicyCase) -> dict[str, Any]:
    payload = asdict(policy)
    payload.update(
        output_contract_version="1.0.0",
        admitted_source_roles=("market", "options"),
        value_type="float",
        unit=None,
        temporal_comparison_rule="exact_effective_interval",
        equality_tolerance=None,
        allow_degraded_candidates=False,
        unresolved_consequence="withhold",
        optional_absence_consequence="unavailable",
    )
    return payload


def production_capture_payload(reference: CaptureReferenceCase) -> dict[str, Any]:
    payload = asdict(reference)
    payload.update(
        source_time_utc=reference.effective_at_utc,
        source_date=None,
        temporal_precision="instant",
        validation_state="valid",
        limitations=(),
        semantic_fields=("spot_price", "prior_close"),
        provider_id=None,
        acquisition_method=None,
    )
    return payload


def production_derivation_payload(receipt: DerivationCase) -> dict[str, Any]:
    payload = asdict(receipt)
    payload.pop("receipt_fingerprint")
    payload.update(
        input_semantic_fields=("spot_price", "prior_close"),
        operation="percentage_return",
        unit_alignment_policy="price_same_currency",
        temporal_alignment_policy="same_effective_bar",
        result_state="derived",
    )
    return payload
