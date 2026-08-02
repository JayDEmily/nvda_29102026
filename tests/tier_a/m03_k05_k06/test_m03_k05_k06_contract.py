"""Minimum truthful public-seam proof for M03 K05/K06 preparation authority."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import BaseModel, ConfigDict
from tests.support.m03_k05_k06_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    ReferenceBuilder,
    ReferenceMandatoryFieldConflictError,
    ReferenceResolver,
    production_api,
    production_candidate_payload,
    production_policy_payload,
    valid_candidate,
    valid_capture_reference,
    valid_derivation,
    valid_policy,
)


def _reference_build_kwargs() -> dict[str, object]:
    receipt = ReferenceResolver().resolve((valid_candidate(),), valid_policy())
    derivation = valid_derivation()
    return {
        "source_capture_refs": (valid_capture_reference(),),
        "input_schema_versions": (("market.snapshot", "1.0.0"),),
        "preparation_policy_version": "prepare.1.0.0",
        "derivation_versions": (("nvda_return_pct", "1.0.0"),),
        "effective_at_utc": valid_capture_reference().effective_at_utc,
        "payload_kind": "prepared_runtime_v1",
        "payload": {
            "kind": "prepared_runtime_v1",
            "spot_price": 101.0,
            "nvda_return_pct": 0.01,
        },
        "field_resolution_receipts": (receipt,),
        "derivation_receipts": (derivation,),
    }


def test_reference_equal_candidates_coalesce_with_complete_lineage() -> None:
    first = valid_candidate(candidate_id="market.spot")
    second = valid_candidate(
        candidate_id="options.spot",
        source_owner="options",
        source_artifact_id="source.options.1",
        capture_id="capture.options.1",
    )
    receipt = ReferenceResolver().resolve((second, first), valid_policy())

    assert receipt.selected_value == 101.0
    assert receipt.candidate_ids == ("market.spot", "options.spot")
    assert receipt.source_refs == (
        ("source.market.1", "capture.market.1"),
        ("source.options.1", "capture.options.1"),
    )
    assert receipt.resolution_reason == "semantically_equal_coalesced"


def test_reference_explicit_owner_selection_is_caller_order_independent() -> None:
    market = valid_candidate(candidate_id="market.spot", value=100.0)
    options = valid_candidate(
        candidate_id="options.spot",
        source_owner="options",
        value=101.0,
        source_artifact_id="source.options.1",
        capture_id="capture.options.1",
    )
    policy = valid_policy(authoritative_owner="options", fallback_owners=("market",))
    resolver = ReferenceResolver()

    first = resolver.resolve((market, options), policy)
    second = resolver.resolve((options, market), policy)

    assert first == second
    assert first.selected_candidate_id == "options.spot"
    assert first.resolution_reason == "authoritative_owner_selected"


def test_reference_unresolved_mandatory_conflict_fails_closed() -> None:
    candidates = (
        valid_candidate(candidate_id="market.spot", value=100.0),
        valid_candidate(
            candidate_id="options.spot",
            source_owner="options",
            value=101.0,
            source_artifact_id="source.options.1",
            capture_id="capture.options.1",
        ),
    )
    with pytest.raises(ReferenceMandatoryFieldConflictError):
        ReferenceResolver().resolve(candidates, valid_policy())


def test_reference_optional_absence_is_explicit_not_fabricated() -> None:
    receipt = ReferenceResolver().resolve((), valid_policy(mandatory=False))

    assert receipt.resolution_status == "unavailable"
    assert receipt.selected_value is None
    assert receipt.candidate_ids == ()
    assert receipt.resolution_reason == "optional_field_unavailable"


def test_reference_envelope_is_tagged_deterministic_and_side_effect_closed() -> None:
    builder = ReferenceBuilder()
    first = builder.build(**_reference_build_kwargs())
    second = builder.build(**_reference_build_kwargs())

    assert first == second
    assert first.prepared_id.startswith("prepared:")
    assert first.payload_kind == first.payload["kind"]
    assert first.closed_authority_classes == CLOSED_AUTHORITIES
    assert first.foreign_authority_claimed is False


def test_reference_material_derivation_preserves_version_and_exact_inputs() -> None:
    envelope = ReferenceBuilder().build(**_reference_build_kwargs())
    receipt = envelope.derivation_receipts[0]

    assert dict(envelope.derivation_versions)[receipt.semantic_field] == receipt.derivation_version
    assert receipt.input_candidate_ids == ("market.spot", "market.prior_close")
    assert receipt.input_fingerprints == ("a" * 64, "b" * 64)


@pytest.mark.parametrize("mutant_name", tuple(MUTANTS))
def test_each_false_positive_mutant_is_killed(mutant_name: str) -> None:
    mutant = MUTANTS[mutant_name]()

    if mutant_name == "caller_order":
        market = valid_candidate(candidate_id="market.spot", value=100.0)
        options = valid_candidate(
            candidate_id="options.spot",
            source_owner="options",
            value=101.0,
            source_artifact_id="source.options.1",
            capture_id="capture.options.1",
        )
        policy = valid_policy(authoritative_owner="options")
        reference = ReferenceResolver().resolve((market, options), policy)
        mutated = mutant.resolve((market, options), policy)
        assert reference.selected_candidate_id == "options.spot"
        assert mutated.selected_candidate_id == "market.spot"
    elif mutant_name == "lineage_dropping":
        candidates = (
            valid_candidate(candidate_id="market.spot"),
            valid_candidate(
                candidate_id="options.spot",
                source_owner="options",
                source_artifact_id="source.options.1",
                capture_id="capture.options.1",
            ),
        )
        reference = ReferenceResolver().resolve(candidates, valid_policy())
        mutated = mutant.resolve(candidates, valid_policy())
        assert len(reference.candidate_ids) == 2
        assert len(mutated.candidate_ids) == 1
    elif mutant_name == "fabricated_capture":
        reference = ReferenceBuilder().build(**_reference_build_kwargs())
        mutated = mutant.build(**_reference_build_kwargs())
        assert reference.source_capture_refs[0].capture_id == "capture.market.1"
        assert mutated.source_capture_refs[0].capture_id == "a" * 64
    elif mutant_name == "untagged_payload":
        kwargs = _reference_build_kwargs()
        kwargs["payload"] = {"spot_price": 101.0}
        with pytest.raises(ValueError, match="tagged_typed_payload_required"):
            ReferenceBuilder().build(**kwargs)
        mutated = mutant.build(**kwargs)
        assert mutated.payload["kind"] == "prepared_runtime_v1"
    elif mutant_name == "derivation_dropping":
        reference = ReferenceBuilder().build(**_reference_build_kwargs())
        mutated = mutant.build(**_reference_build_kwargs())
        assert reference.derivation_receipts
        assert mutated.derivation_receipts == ()
    else:
        reference = ReferenceBuilder().build(**_reference_build_kwargs())
        mutated = mutant.build(**_reference_build_kwargs())
        assert reference.foreign_authority_claimed is False
        assert "capital" in reference.closed_authority_classes
        assert mutated.foreign_authority_claimed is True
        assert "capital" not in mutated.closed_authority_classes


def test_production_exports_exact_frozen_public_contracts() -> None:
    api = production_api()
    for name in (
        "SourceCaptureReference",
        "PreparedRuntimePayloadV1",
        "DerivationReceipt",
        "PreparedDataEnvelope",
        "FieldCandidate",
        "FieldResolutionPolicy",
        "FieldResolutionReceipt",
    ):
        model = api[name]
        assert model.model_config.get("extra") == "forbid"
        assert model.model_config.get("frozen") is True

    envelope_fields = set(api["PreparedDataEnvelope"].model_fields)
    assert {
        "prepared_id",
        "schema_version",
        "source_capture_refs",
        "input_schema_versions",
        "preparation_policy_version",
        "alignment_policy_version",
        "fingerprint_policy_version",
        "canonicalisation_version",
        "derivation_versions",
        "effective_at_utc",
        "input_fingerprint",
        "prepared_fingerprint",
        "validation_state",
        "completeness_state",
        "limitations",
        "failed_mandatory_transformations",
        "missing_optional_enrichments",
        "parent_prepared_ids",
        "payload_kind",
        "payload_schema_version",
        "payload",
        "field_resolution_receipts",
        "derivation_receipts",
        "closed_authority_classes",
        "foreign_authority_claimed",
    }.issubset(envelope_fields)


def _production_candidates_and_policy(*, equal: bool = False):
    api = production_api()
    market = api["FieldCandidate"].model_validate(
        production_candidate_payload(valid_candidate(value=101.0 if equal else 100.0))
    )
    options = api["FieldCandidate"].model_validate(
        production_candidate_payload(
            valid_candidate(
                candidate_id="options.spot",
                source_owner="options",
                value=101.0,
                source_artifact_id="source.options.1",
                capture_id="capture.options.1",
            )
        )
    )
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(
            valid_policy(authoritative_owner="options", fallback_owners=("market",))
        )
    )
    return api, market, options, policy


def test_production_equal_candidates_coalesce_with_complete_provenance() -> None:
    api, market, options, _ = _production_candidates_and_policy(equal=True)
    policy = api["FieldResolutionPolicy"].model_validate(production_policy_payload(valid_policy()))
    receipt = api["resolve_canonical_field"](candidates=(options, market), policy=policy)

    assert receipt.selected_value == 101.0
    assert receipt.candidate_ids == ("market.spot", "options.spot")
    assert receipt.resolution_reason == "semantically_equal_coalesced"
    assert (
        receipt.receipt_fingerprint
        == api["resolve_canonical_field"](
            candidates=(market, options), policy=policy
        ).receipt_fingerprint
    )


def test_production_explicit_owner_selection_and_conflict_are_fail_closed() -> None:
    api, market, options, policy = _production_candidates_and_policy()
    selected = api["resolve_canonical_field"](candidates=(market, options), policy=policy)
    reversed_selected = api["resolve_canonical_field"](candidates=(options, market), policy=policy)

    assert selected == reversed_selected
    assert selected.selected_candidate_id == "options.spot"
    assert selected.resolution_reason == "authoritative_owner_selected"

    no_owner = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy())
    )
    with pytest.raises(api["MandatoryFieldConflictError"]):
        api["resolve_canonical_field"](candidates=(market, options), policy=no_owner)


def test_production_exact_float_comparison_coalesces_integer_and_float_forms() -> None:
    api = production_api()
    market = api["FieldCandidate"].model_validate(
        production_candidate_payload(valid_candidate(candidate_id="market.spot", value=1))
    )
    options = api["FieldCandidate"].model_validate(
        production_candidate_payload(
            valid_candidate(
                candidate_id="options.spot",
                source_owner="options",
                value=1.0,
                source_artifact_id="source.options.1",
                capture_id="capture.options.1",
            )
        )
    )
    policy = api["FieldResolutionPolicy"].model_validate(production_policy_payload(valid_policy()))

    receipt = api["resolve_canonical_field"](candidates=(options, market), policy=policy)

    assert receipt.equality_result == "equal"
    assert receipt.resolution_reason == "semantically_equal_coalesced"


def test_production_conflicting_authoritative_owner_cannot_fall_through_to_fallback() -> None:
    api = production_api()
    candidates = tuple(
        api["FieldCandidate"].model_validate(production_candidate_payload(item))
        for item in (
            valid_candidate(candidate_id="market.spot", value=99.0),
            valid_candidate(
                candidate_id="options.spot.1",
                source_owner="options",
                value=100.0,
                source_artifact_id="source.options.1",
                capture_id="capture.options.1",
            ),
            valid_candidate(
                candidate_id="options.spot.2",
                source_owner="options",
                value=101.0,
                source_artifact_id="source.options.2",
                capture_id="capture.options.2",
            ),
        )
    )
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(
            valid_policy(authoritative_owner="options", fallback_owners=("market",))
        )
    )

    with pytest.raises(api["MandatoryFieldConflictError"]):
        api["resolve_canonical_field"](candidates=candidates, policy=policy)


def test_production_optional_missing_field_returns_explicit_unavailable_receipt() -> None:
    api = production_api()
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy(mandatory=False))
    )
    receipt = api["resolve_canonical_field"](candidates=(), policy=policy)

    assert receipt.resolution_status == "unavailable"
    assert receipt.selected_value is None
    assert receipt.candidate_ids == ()


class _StrictMarketSourcePayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    spot_price: float
    prior_close: float
    runtime_bar_time_utc: datetime


class _StrictOptionsSourcePayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    spot_price: float


def _strict_source_artifact(
    *,
    owner: str = "market",
    spot_price: float = 101.0,
    prior_close: float = 100.0,
    runtime_bar_time_utc: datetime = datetime(2026, 8, 3, 0, 0, tzinfo=UTC),
    limitations: tuple[str, ...] = (),
):
    from nvda_desk import m01_source_admission as m01

    if owner == "market":
        payload = _StrictMarketSourcePayload(
            spot_price=spot_price,
            prior_close=prior_close,
            runtime_bar_time_utc=runtime_bar_time_utc,
        )
        bindings = (
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
    elif owner == "options":
        payload = _StrictOptionsSourcePayload(spot_price=spot_price)
        bindings = (
            m01.SourceSemanticBinding(
                semantic_field="spot_price",
                payload_field="spot_price",
                value_type="float",
                unit="USD",
                requirement=m01.SourceFactRequirement.REQUIRED,
            ),
        )
    else:
        raise ValueError("unsupported_test_source_owner")

    family_id = f"strict_{owner}_source"
    source_artifact_id = f"source.{owner}.1"
    service = m01.SourceAdmissionService(
        registry=m01.SourceFamilyRegistry.build(
            [
                m01.SourceFamilyContract(
                    family_id=family_id,
                    contract_id=f"{family_id}.v1",
                    schema_version="1.0.0",
                    payload_model=type(payload),
                    providers=(
                        m01.SourceProviderContract(
                            provider_id=owner,
                            acquisition_channels=("recorded_api_response",),
                        ),
                    ),
                    source_identifier=m01.SourceIdentifierContract(
                        requirement=m01.SourceFactRequirement.REQUIRED,
                        owner=owner,
                        namespace=f"{owner}/strict-source",
                        uniqueness_scope=f"{owner}/strict-source",
                        stability_rule="stable_for_source_object_lifetime",
                        generation_rule="issued_by_upstream_provider",
                    ),
                    source_time_kind=m01.SourceTimeKind.INSTANT,
                    downstream_owner=m01.SourceDownstreamOwner.M03,
                    output_contract=m01.SourceOutputContract.RAW_SIGNAL_BATCH,
                    signal_family_id=family_id,
                    permitted_limitations=limitations,
                    semantic_bindings=bindings,
                )
            ]
        ),
        capture_id_factory=lambda _: f"capture.{owner}.1",
        source_artifact_id_factory=lambda *_: source_artifact_id,
    )
    result = service.admit(
        m01.SourceAdmissionRequest(
            family_id=family_id,
            contract_id=f"{family_id}.v1",
            schema_version="1.0.0",
            provider_id=owner,
            acquisition_channel="recorded_api_response",
            source_object_id=f"provider.{owner}.1",
            observed_at_utc=runtime_bar_time_utc,
            captured_at_utc=runtime_bar_time_utc,
            captured_material=payload.model_dump_json().encode(),
            typed_payload=payload,
            declared_limitations=limitations,
        )
    )
    assert result.status == "accepted"
    return result.source_artifact


def _strict_policy(
    semantic_field: str,
    *,
    admitted_source_roles: tuple[str, ...],
    value_type: str,
    unit: str | None,
    authoritative_owner: str | None,
    allow_degraded_candidates: bool = False,
):
    api = production_api()
    return api["FieldResolutionPolicy"](
        policy_id=f"m03.policy.{semantic_field}",
        policy_version="1.0.0",
        output_contract_version="1.0.0",
        semantic_field=semantic_field,
        mandatory=True,
        admitted_source_roles=admitted_source_roles,
        value_type=value_type,
        unit=unit,
        temporal_comparison_rule="exact_effective_interval",
        comparison_rule="exact",
        authoritative_owner=authoritative_owner,
        allow_degraded_candidates=allow_degraded_candidates,
        unresolved_consequence="withhold",
        optional_absence_consequence="unavailable",
    )


def _strict_build_kwargs(
    *,
    artifacts=None,
    unresolved_spot: bool = False,
    include_derivation: bool = True,
) -> dict[str, object]:
    api = production_api()
    governed_artifacts = tuple(artifacts or (_strict_source_artifact(),))
    owners = tuple(sorted({item.source_identifier.owner for item in governed_artifacts}))
    allow_degraded = any(item.validation_status == "degraded" for item in governed_artifacts)
    policies = [
        _strict_policy(
            "spot_price",
            admitted_source_roles=owners,
            value_type="float",
            unit="USD",
            authoritative_owner=None if unresolved_spot else "market",
            allow_degraded_candidates=allow_degraded,
        )
    ]
    if any(
        binding.semantic_field == "prior_close"
        for artifact in governed_artifacts
        for binding in artifact.semantic_bindings
    ):
        policies.extend(
            [
                _strict_policy(
                    "prior_close",
                    admitted_source_roles=("market",),
                    value_type="float",
                    unit="USD",
                    authoritative_owner="market",
                    allow_degraded_candidates=allow_degraded,
                ),
                _strict_policy(
                    "runtime_bar_time_utc",
                    admitted_source_roles=("market",),
                    value_type="datetime",
                    unit=None,
                    authoritative_owner="market",
                    allow_degraded_candidates=allow_degraded,
                ),
            ]
        )
    derivation_rules = ()
    if include_derivation:
        derivation_rules = (
            api["PreparedDerivationRule"](
                semantic_field="nvda_return_pct",
                derivation_version="1.0.0",
                input_semantic_fields=("spot_price", "prior_close"),
                operation="percentage_return",
                unit_alignment_policy="same_currency",
                temporal_alignment_policy="same_effective_interval",
                mandatory=True,
            ),
        )
    return {
        "source_artifacts": governed_artifacts,
        "calendar_projections": (),
        "field_resolution_policies": tuple(policies),
        "derivation_rules": derivation_rules,
        "schema_version": "1.0.0",
        "preparation_policy_version": "prepare.1.0.0",
        "alignment_policy_version": "alignment.1.0.0",
        "fingerprint_policy_version": "sha256.1.0.0",
        "canonicalisation_version": "json.1.0.0",
        "effective_at_utc": datetime(2026, 8, 3, 0, 0, tzinfo=UTC),
        "payload_schema_version": "1.0.0",
    }


def _strict_envelope(**overrides):
    kwargs = _strict_build_kwargs(**overrides)
    return production_api()["PreparedDataBuilder"]().build(**kwargs)


def test_production_envelope_rejects_untagged_mapping_and_forged_fingerprint() -> None:
    api = production_api()
    envelope = _strict_envelope()

    assert envelope.payload_kind == "prepared_runtime_v1"
    assert envelope.payload.kind == "prepared_runtime_v1"
    assert envelope.source_capture_refs[0].capture_id == "capture.market.1"
    assert envelope.closed_authority_classes == CLOSED_AUTHORITIES
    assert envelope.foreign_authority_claimed is False

    with pytest.raises((TypeError, ValueError), match="payload|tag|typed|kind|contract"):
        api["PreparedDataEnvelope"].model_validate(
            {
                **envelope.model_dump(mode="python"),
                "payload_kind": None,
                "payload": {"spot_price": 101.0},
            }
        )
    with pytest.raises((TypeError, ValueError), match="fingerprint"):
        api["PreparedDataEnvelope"].model_validate(
            {**envelope.model_dump(mode="python"), "prepared_fingerprint": "f" * 64}
        )


def test_production_builder_is_order_independent_and_preserves_derivation_inputs() -> None:
    market = _strict_source_artifact(owner="market", spot_price=101.0)
    options = _strict_source_artifact(owner="options", spot_price=101.0)
    first = _strict_envelope(artifacts=(market, options))
    second = _strict_envelope(artifacts=(options, market))

    assert first == second
    assert first.derivation_receipts[0].input_candidate_ids == (
        "m01:source.market.1:spot_price",
        "m01:source.market.1:prior_close",
    )
    assert first.input_fingerprint == second.input_fingerprint
    assert first.prepared_fingerprint == second.prepared_fingerprint


def test_production_runtime_lineage_names_material_m03_authority() -> None:
    from dataclasses import fields

    from nvda_desk.preparation.runtime_preparer import PreparedRuntimeLineage

    names = {item.name for item in fields(PreparedRuntimeLineage)}
    assert {
        "source_artifact_ids",
        "capture_ids",
        "input_fingerprint",
        "input_schema_version",
        "preparation_policy_version",
        "derivation_versions",
    }.issubset(names)


def _production_envelope():
    api = production_api()
    envelope = _strict_envelope()
    receipt = next(
        item for item in envelope.field_resolution_receipts if item.semantic_field == "spot_price"
    )
    candidate = next(
        item
        for item in receipt.candidate_records
        if item.candidate_id == receipt.selected_candidate_id
    )
    policy = next(
        item
        for item in _strict_build_kwargs()["field_resolution_policies"]
        if item.semantic_field == "spot_price"
    )
    return api, valid_capture_reference(), candidate, policy, receipt, envelope


def test_production_receipt_preserves_complete_candidate_and_comparison_evidence() -> None:
    api, market, options, policy = _production_candidates_and_policy(equal=True)
    receipt = api["resolve_canonical_field"](candidates=(options, market), policy=policy)

    assert receipt.receipt_id == f"resolution:{receipt.receipt_fingerprint[:24]}"
    assert receipt.candidate_records == (market, options)
    assert receipt.candidate_ids == ("market.spot", "options.spot")
    assert receipt.equality_result == "equal"
    assert receipt.temporal_alignment_result == "exact"
    assert receipt.normalisation_evidence == (
        ("market.spot", ()),
        ("options.spot", ()),
    )
    assert receipt.selected_source_artifact_id == "source.market.1"
    assert receipt.selected_capture_id == "capture.market.1"


def test_production_public_boundaries_revalidate_copied_authority() -> None:
    api, _, candidate, policy, _, envelope = _production_envelope()
    forged_candidate = candidate.model_copy(update={"value": "not-a-float"})
    with pytest.raises(ValueError, match="typed_value"):
        api["resolve_canonical_field"](candidates=(forged_candidate,), policy=policy)

    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    forged_envelope = envelope.model_copy(update={"prepared_fingerprint": "f" * 64})
    with pytest.raises(ValueError, match="fingerprint"):
        prepare_runtime_snapshot_from_envelope(forged_envelope)


def test_production_typed_payload_has_no_generic_extension_authority() -> None:
    api = production_api()
    with pytest.raises(ValueError, match="extra|forbidden|extensions"):
        api["PreparedRuntimePayloadV1"].model_validate(
            {"kind": "prepared_runtime_v1", "extensions": {"capital": 1}}
        )


def test_production_envelope_adapts_into_legacy_views_without_fabricated_lineage() -> None:
    _, _, _, _, _, envelope = _production_envelope()

    from nvda_desk.preparation.context_packet import build_prepared_context_payload
    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    snapshot = prepare_runtime_snapshot_from_envelope(envelope)
    context = build_prepared_context_payload(snapshot)

    assert snapshot.prepared_envelope == envelope
    assert snapshot.lineage.source_artifact_ids == ("source.market.1",)
    assert snapshot.lineage.capture_ids == ("capture.market.1",)
    assert snapshot.lineage.input_fingerprint == envelope.input_fingerprint
    assert snapshot.lineage.input_schema_versions == (("m01:source.market.1", "1.0.0"),)
    assert snapshot.payload["spot_price"] == 101.0
    assert context.prepared_id == envelope.prepared_id
    assert context.prepared_fingerprint == envelope.prepared_fingerprint
    assert context.payload_kind == "prepared_runtime_v1"
    assert context.source_artifact_ids == ["source.market.1"]
    assert context.capture_ids == ["capture.market.1"]


def test_repair_rejects_valid_complete_envelope_from_degraded_source() -> None:
    limitation = "source_partial"
    envelope = _strict_envelope(
        artifacts=(
            _strict_source_artifact(
                owner="market",
                limitations=(limitation,),
            ),
        )
    )

    assert envelope.validation_state == "degraded"
    assert envelope.completeness_state == "degraded"
    assert limitation in envelope.limitations


def test_repair_requires_resolution_receipt_for_competing_payload_sources() -> None:
    api = production_api()
    artifacts = (
        _strict_source_artifact(owner="market", spot_price=100.0),
        _strict_source_artifact(owner="options", spot_price=101.0),
    )

    with pytest.raises(api["MandatoryFieldConflictError"]):
        _strict_envelope(artifacts=artifacts, unresolved_spot=True)


def test_repair_rejects_resolution_receipt_payload_disagreement() -> None:
    artifact = _strict_source_artifact(owner="market", spot_price=101.0)
    forged = artifact.model_copy(
        update={"typed_payload": artifact.typed_payload.model_copy(update={"spot_price": 999.0})}
    )

    with pytest.raises(ValueError, match="source_artifact_evidence_mismatch"):
        _strict_envelope(artifacts=(forged,))


def test_repair_rejects_derivation_receipt_payload_disagreement() -> None:
    from inspect import signature

    parameters = signature(production_api()["PreparedDataBuilder"].build).parameters
    envelope = _strict_envelope()
    derivation = envelope.derivation_receipts[0]

    assert "derivation_receipts" not in parameters
    assert "payload" not in parameters
    assert derivation.semantic_field == "nvda_return_pct"
    assert derivation.value == pytest.approx(0.01)
    assert envelope.payload.nvda_return_pct == derivation.value


def _unit2_packet(snapshot, *, packet_id: str = "prepared-context-unit2"):
    from nvda_desk.contracts.packets import DmpV3ExecutionContext
    from nvda_desk.preparation.context_packet import build_prepared_context_packet

    return build_prepared_context_packet(
        packet_id=packet_id,
        snapshot=snapshot,
        emitted_at=datetime(2026, 8, 2, 10, 0, tzinfo=UTC),
        execution_context=DmpV3ExecutionContext(
            traceid="trace-unit2",
            runid="run-unit2",
            scenarioid="scenario-unit2",
        ),
        module_version="m03-prepared-packet.1",
        module_instance_id="m03-prepared-packet-instance-1",
        parentids=["source-capture-packet-1"],
    )


def test_unit2_prepared_packet_projects_exact_m03_identity_and_lineage() -> None:
    from nvda_desk.contracts.packets import (
        K07_COMMON_CHECKS,
        K07_ROLE_CHECKS,
        PreparedContextIdentity,
    )
    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    _, _, _, _, _, envelope = _production_envelope()
    packet = _unit2_packet(prepare_runtime_snapshot_from_envelope(envelope))

    assert packet.data == PreparedContextIdentity(
        prepared_id=envelope.prepared_id,
        prepared_fingerprint=envelope.prepared_fingerprint,
        schema_version=envelope.schema_version,
        preparation_policy_version=envelope.preparation_policy_version,
    )
    assert packet.producer.module_version == "m03-prepared-packet.1"
    assert packet.producer.module_instance_id == "m03-prepared-packet-instance-1"
    assert packet.traceid == "trace-unit2"
    assert packet.runid == "run-unit2"
    assert packet.scenarioid == "scenario-unit2"
    assert packet.lineage.parentids == ["source-capture-packet-1"]
    assert packet.lineage.derivedfrom == envelope.prepared_id
    assert packet.lineage.sourceartifactids == ["source.market.1"]
    assert packet.lineage.inputfingerprint == envelope.prepared_fingerprint
    assert packet.validation.status == "valid"
    assert tuple(check.name for check in packet.validation.checks) == (
        *K07_COMMON_CHECKS,
        *K07_ROLE_CHECKS["prepared_context_packet"],
    )
    assert all(check.passed for check in packet.validation.checks)


def test_unit2_prepared_packet_degradation_is_envelope_admitted_and_restricted() -> None:
    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    limitation = "calendar_reference_projection_missing"
    envelope = _strict_envelope(
        artifacts=(
            _strict_source_artifact(
                owner="market",
                limitations=(limitation,),
            ),
        )
    )

    packet = _unit2_packet(prepare_runtime_snapshot_from_envelope(envelope))

    assert packet.validation.status == "degraded"
    assert packet.validation.violations == [limitation]
    assert packet.validation.checks[-1].name == f"optional_quality:{limitation}"
    assert packet.validation.checks[-1].passed is False
    assert "consumer_restriction:non_binding_prepared_context" in packet.summary.keyflags


def test_unit2_prepared_packet_rejects_noncanonical_compatibility_snapshot() -> None:
    from nvda_desk.ingress.raw_bundle_loader import load_api_payload
    from nvda_desk.preparation.runtime_preparer import prepare_runtime_dataset

    snapshot = prepare_runtime_dataset(
        load_api_payload(
            {
                "snapshot_id": "raw-compatibility-only",
                "source_time_utc": datetime(2026, 8, 2, 9, 30, tzinfo=UTC),
                "market_snapshot": {"spot_price": 101.0},
            }
        )
    ).primary_snapshot

    with pytest.raises(ValueError, match="canonical_prepared_envelope_required"):
        _unit2_packet(snapshot)


def test_unit2_prepared_packet_revalidates_copied_envelope() -> None:
    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    _, _, _, _, _, envelope = _production_envelope()
    snapshot = prepare_runtime_snapshot_from_envelope(envelope)
    snapshot.prepared_envelope = envelope.model_copy(update={"prepared_fingerprint": "f" * 64})

    with pytest.raises(ValueError, match="prepared_envelope_contract_invalid"):
        _unit2_packet(snapshot)


class _SemanticMarketPayloadForM03(__import__("pydantic").BaseModel):
    model_config = __import__("pydantic").ConfigDict(extra="forbid", frozen=True)

    spot_price: float


def _semantic_m01_artifact_for_m03(*, spot_price: float = 190.0):
    from nvda_desk import m01_source_admission as m01

    binding = m01.SourceSemanticBinding(
        semantic_field="spot_price",
        payload_field="spot_price",
        value_type="float",
        unit="USD",
        requirement=m01.SourceFactRequirement.REQUIRED,
    )
    service = m01.SourceAdmissionService(
        registry=m01.SourceFamilyRegistry.build(
            [
                m01.SourceFamilyContract(
                    family_id="semantic_market",
                    contract_id="semantic_market.v1",
                    schema_version="1.0.0",
                    payload_model=_SemanticMarketPayloadForM03,
                    providers=(
                        m01.SourceProviderContract(
                            provider_id="recorded-provider",
                            acquisition_channels=("recorded_api_response",),
                        ),
                    ),
                    source_identifier=m01.SourceIdentifierContract(
                        requirement=m01.SourceFactRequirement.REQUIRED,
                        owner="recorded-provider",
                        namespace="recorded-provider/semantic-market",
                        uniqueness_scope="recorded-provider/semantic-market",
                        stability_rule="stable_for_source_object_lifetime",
                        generation_rule="issued_by_upstream_provider",
                    ),
                    source_time_kind=m01.SourceTimeKind.INSTANT,
                    downstream_owner=m01.SourceDownstreamOwner.M03,
                    output_contract=m01.SourceOutputContract.RAW_SIGNAL_BATCH,
                    signal_family_id="semantic_market",
                    semantic_bindings=(binding,),
                )
            ]
        ),
        capture_id_factory=lambda _: "capture.semantic.market.1",
        source_artifact_id_factory=lambda *_: "source.semantic.market.1",
    )
    payload = _SemanticMarketPayloadForM03(spot_price=spot_price)
    result = service.admit(
        m01.SourceAdmissionRequest(
            family_id="semantic_market",
            contract_id="semantic_market.v1",
            schema_version="1.0.0",
            provider_id="recorded-provider",
            acquisition_channel="recorded_api_response",
            source_object_id="provider.semantic.market.1",
            observed_at_utc=datetime(2026, 8, 3, 0, 0, tzinfo=UTC),
            captured_at_utc=datetime(2026, 8, 3, 0, 0, 1, tzinfo=UTC),
            captured_material=payload.model_dump_json().encode(),
            typed_payload=payload,
        )
    )
    assert result.status == "accepted"
    return result.source_artifact


def _semantic_spot_policy_for_m03():
    api = production_api()
    return api["FieldResolutionPolicy"](
        policy_id="m03.policy.spot_price",
        policy_version="1.0.0",
        output_contract_version="1.0.0",
        semantic_field="spot_price",
        mandatory=True,
        admitted_source_roles=("recorded-provider",),
        value_type="float",
        unit="USD",
        temporal_comparison_rule="exact_effective_interval",
        comparison_rule="exact",
        authoritative_owner="recorded-provider",
        allow_degraded_candidates=False,
        unresolved_consequence="withhold",
        optional_absence_consequence="unavailable",
    )


def _semantic_strict_build_kwargs() -> dict[str, object]:
    return {
        "source_artifacts": (_semantic_m01_artifact_for_m03(),),
        "calendar_projections": (),
        "field_resolution_policies": (_semantic_spot_policy_for_m03(),),
        "derivation_rules": (),
        "schema_version": "1.0.0",
        "preparation_policy_version": "prepare.semantic.1",
        "alignment_policy_version": "align.semantic.1",
        "fingerprint_policy_version": "fingerprint.semantic.1",
        "canonicalisation_version": "canonical.semantic.1",
        "effective_at_utc": datetime(2026, 8, 3, 0, 1, tzinfo=UTC),
        "payload_schema_version": "1.0.0",
    }


def test_semantic_continuity_m03_builder_has_no_caller_authored_payload() -> None:
    from inspect import signature

    parameters = signature(production_api()["PreparedDataBuilder"].build).parameters

    assert "payload" not in parameters
    assert "source_artifacts" in parameters
    assert "field_resolution_policies" in parameters


def test_semantic_continuity_m03_constructs_exact_value_from_m01_owner_evidence() -> None:
    envelope = production_api()["PreparedDataBuilder"]().build(**_semantic_strict_build_kwargs())

    assert envelope.payload.spot_price == 190.0
    assert envelope.field_resolution_receipts[0].selected_value == 190.0
    assert envelope.field_resolution_receipts[0].selected_source_artifact_id == (
        "source.semantic.market.1"
    )


def _semantic_m02_projection_for_m03():
    from dataclasses import replace

    from tests.support.m02_k04_contract_harness import (
        field_policy,
        production_policy_payload,
        production_snapshot_payload,
        valid_snapshot,
    )
    from tests.support.m02_k04_contract_harness import (
        valid_candidate as valid_calendar_candidate,
    )

    from nvda_desk import m02_financial_calendar as m02

    next_event = replace(
        valid_calendar_candidate(
            candidate_id="calendar.next_event.1",
            semantic_key="next_event_time_utc",
            value="2026-08-03T02:00:00+00:00",
            source_artifact_id="source.market.1",
        ),
        fact_family="financial_event",
    )
    snapshot = m02.FinancialCalendarSnapshot.model_validate(
        production_snapshot_payload(valid_snapshot(session_candidates=(next_event,)))
    )
    policy = m02.CalendarFieldResolutionPolicy.model_validate(
        production_policy_payload(field_policy(semantic_key="next_event_time_utc"))
    )
    return m02.CalendarResolver().project(
        snapshot,
        policy,
        projection_id="projection.semantic.next-event.1",
    )


def _semantic_m01_m02_build_kwargs() -> dict[str, object]:
    kwargs = _strict_build_kwargs()
    kwargs["calendar_projections"] = (_semantic_m02_projection_for_m03(),)
    kwargs["field_resolution_policies"] = (
        *kwargs["field_resolution_policies"],
        _strict_policy(
            "next_event_time_utc",
            admitted_source_roles=("M02",),
            value_type="datetime",
            unit=None,
            authoritative_owner="M02",
        ),
    )
    return kwargs


def test_semantic_continuity_m03_constructs_exact_value_from_m02_owner_projection() -> None:
    envelope = production_api()["PreparedDataBuilder"]().build(**_semantic_m01_m02_build_kwargs())

    assert envelope.payload.next_event_time_utc == datetime(2026, 8, 3, 2, 0, tzinfo=UTC)
    receipt = next(
        item
        for item in envelope.field_resolution_receipts
        if item.semantic_field == "next_event_time_utc"
    )
    assert receipt.selected_source_owner == "M02"
    assert receipt.selected_source_artifact_id == "projection.semantic.next-event.1"
    assert envelope.calendar_projection_refs[0].semantic_fingerprint == (
        _semantic_m02_projection_for_m03().semantic_fingerprint
    )


def test_semantic_continuity_m03_rejects_copied_m02_value_not_in_projection_fingerprint() -> None:
    projection = _semantic_m02_projection_for_m03()
    forged_field = projection.selected_fields[0].model_copy(
        update={"value": "2026-08-04T02:00:00+00:00"}
    )
    forged = projection.model_copy(update={"selected_fields": (forged_field,)})
    kwargs = _semantic_m01_m02_build_kwargs()
    kwargs["calendar_projections"] = (forged,)

    with pytest.raises(ValueError, match="calendar_projection_contract_invalid"):
        production_api()["PreparedDataBuilder"]().build(**kwargs)


def test_semantic_continuity_m03_rejects_copied_source_value_not_in_capture() -> None:
    artifact = _semantic_m01_artifact_for_m03()
    forged = artifact.model_copy(
        update={"typed_payload": _SemanticMarketPayloadForM03(spot_price=999.0)}
    )
    kwargs = _semantic_strict_build_kwargs()
    kwargs["source_artifacts"] = (forged,)

    with pytest.raises(ValueError, match="source_artifact_evidence_mismatch"):
        production_api()["PreparedDataBuilder"]().build(**kwargs)
