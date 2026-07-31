"""Minimum truthful public-seam proof for M03 K05/K06 preparation authority."""

from __future__ import annotations

from dataclasses import replace

import pytest

from tests.support.m03_k05_k06_contract_harness import (
    CLOSED_AUTHORITIES,
    MUTANTS,
    ReferenceBuilder,
    ReferenceMandatoryFieldConflictError,
    ReferenceResolver,
    fingerprint,
    production_api,
    production_candidate_payload,
    production_capture_payload,
    production_derivation_payload,
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
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy())
    )
    receipt = api["resolve_canonical_field"](
        candidates=(options, market), policy=policy
    )

    assert receipt.selected_value == 101.0
    assert receipt.candidate_ids == ("market.spot", "options.spot")
    assert receipt.resolution_reason == "semantically_equal_coalesced"
    assert receipt.receipt_fingerprint == api["resolve_canonical_field"](
        candidates=(market, options), policy=policy
    ).receipt_fingerprint


def test_production_explicit_owner_selection_and_conflict_are_fail_closed() -> None:
    api, market, options, policy = _production_candidates_and_policy()
    selected = api["resolve_canonical_field"](
        candidates=(market, options), policy=policy
    )
    reversed_selected = api["resolve_canonical_field"](
        candidates=(options, market), policy=policy
    )

    assert selected == reversed_selected
    assert selected.selected_candidate_id == "options.spot"
    assert selected.resolution_reason == "authoritative_owner_selected"

    no_owner = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy())
    )
    with pytest.raises(api["MandatoryFieldConflictError"]):
        api["resolve_canonical_field"](
            candidates=(market, options), policy=no_owner
        )


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
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy())
    )

    receipt = api["resolve_canonical_field"](
        candidates=(options, market), policy=policy
    )

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


def test_production_envelope_rejects_untagged_mapping_and_forged_fingerprint() -> None:
    api = production_api()
    reference = valid_capture_reference()
    capture = api["SourceCaptureReference"].model_validate(
        production_capture_payload(reference)
    )
    payload = api["PreparedRuntimePayloadV1"](
        kind="prepared_runtime_v1", spot_price=101.0
    )
    receipt = api["resolve_canonical_field"](
        candidates=(
            api["FieldCandidate"].model_validate(
                production_candidate_payload(valid_candidate())
            ),
        ),
        policy=api["FieldResolutionPolicy"].model_validate(
            production_policy_payload(valid_policy())
        ),
    )
    derivation = api["DerivationReceipt"].model_validate(
        production_derivation_payload(valid_derivation())
    )
    builder = api["PreparedDataBuilder"]()
    envelope = builder.build(
        source_capture_refs=(capture,),
        input_schema_versions={"market.snapshot": "1.0.0"},
        schema_version="1.0.0",
        preparation_policy_version="prepare.1.0.0",
        alignment_policy_version="alignment.1.0.0",
        fingerprint_policy_version="sha256.1.0.0",
        canonicalisation_version="json.1.0.0",
        derivation_versions={"nvda_return_pct": "1.0.0"},
        effective_at_utc=reference.effective_at_utc,
        payload=payload,
        payload_schema_version="1.0.0",
        field_resolution_receipts=(receipt,),
        derivation_receipts=(derivation,),
    )

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
    api, market, options, policy = _production_candidates_and_policy(equal=True)
    first_receipt = api["resolve_canonical_field"](
        candidates=(market, options), policy=policy
    )
    second_receipt = api["resolve_canonical_field"](
        candidates=(options, market), policy=policy
    )
    capture_type = api["SourceCaptureReference"]
    refs = (
        capture_type.model_validate(production_capture_payload(valid_capture_reference())),
        capture_type.model_validate(
            production_capture_payload(
                valid_capture_reference(
                    capture_id="capture.options.1",
                    source_artifact_id="source.options.1",
                )
            )
        ),
    )
    derivation = api["DerivationReceipt"].model_validate(
        production_derivation_payload(valid_derivation())
    )
    payload = api["PreparedRuntimePayloadV1"](
        kind="prepared_runtime_v1", spot_price=101.0, nvda_return_pct=0.01
    )
    builder = api["PreparedDataBuilder"]()
    common = {
        "input_schema_versions": {"market.snapshot": "1.0.0"},
        "schema_version": "1.0.0",
        "preparation_policy_version": "prepare.1.0.0",
        "alignment_policy_version": "alignment.1.0.0",
        "fingerprint_policy_version": "sha256.1.0.0",
        "canonicalisation_version": "json.1.0.0",
        "derivation_versions": {"nvda_return_pct": "1.0.0"},
        "effective_at_utc": valid_capture_reference().effective_at_utc,
        "payload": payload,
        "payload_schema_version": "1.0.0",
        "derivation_receipts": (derivation,),
    }
    first = builder.build(
        source_capture_refs=refs,
        field_resolution_receipts=(first_receipt,),
        **common,
    )
    second = builder.build(
        source_capture_refs=tuple(reversed(refs)),
        field_resolution_receipts=(second_receipt,),
        **common,
    )

    assert first == second
    assert first.derivation_receipts[0].input_candidate_ids == (
        "market.spot",
        "market.prior_close",
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
    reference = valid_capture_reference()
    capture = api["SourceCaptureReference"].model_validate(
        production_capture_payload(reference)
    )
    candidate = api["FieldCandidate"].model_validate(
        production_candidate_payload(valid_candidate())
    )
    policy = api["FieldResolutionPolicy"].model_validate(
        production_policy_payload(valid_policy())
    )
    receipt = api["resolve_canonical_field"](
        candidates=(candidate,), policy=policy
    )
    derivation = api["DerivationReceipt"].model_validate(
        production_derivation_payload(valid_derivation())
    )
    envelope = api["PreparedDataBuilder"]().build(
        source_capture_refs=(capture,),
        input_schema_versions={"market.snapshot": "1.0.0"},
        schema_version="1.0.0",
        preparation_policy_version="prepare.1.0.0",
        alignment_policy_version="alignment.1.0.0",
        fingerprint_policy_version="sha256.1.0.0",
        canonicalisation_version="json.1.0.0",
        derivation_versions={"nvda_return_pct": "1.0.0"},
        effective_at_utc=reference.effective_at_utc,
        payload=api["PreparedRuntimePayloadV1"](
            kind="prepared_runtime_v1",
            runtime_bar_time_utc=reference.effective_at_utc,
            spot_price=101.0,
            nvda_return_pct=0.01,
        ),
        payload_schema_version="1.0.0",
        field_resolution_receipts=(receipt,),
        derivation_receipts=(derivation,),
    )
    return api, reference, candidate, policy, receipt, envelope


def test_production_receipt_preserves_complete_candidate_and_comparison_evidence() -> None:
    api, market, options, policy = _production_candidates_and_policy(equal=True)
    receipt = api["resolve_canonical_field"](
        candidates=(options, market), policy=policy
    )

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
        api["resolve_canonical_field"](
            candidates=(forged_candidate,), policy=policy
        )

    from nvda_desk.preparation.runtime_preparer import (
        prepare_runtime_snapshot_from_envelope,
    )

    forged_envelope = envelope.model_copy(
        update={"prepared_fingerprint": "f" * 64}
    )
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
    assert snapshot.lineage.input_schema_versions == (("market.snapshot", "1.0.0"),)
    assert snapshot.payload["spot_price"] == 101.0
    assert context.prepared_id == envelope.prepared_id
    assert context.prepared_fingerprint == envelope.prepared_fingerprint
    assert context.payload_kind == "prepared_runtime_v1"
    assert context.source_artifact_ids == ["source.market.1"]
    assert context.capture_ids == ["capture.market.1"]
