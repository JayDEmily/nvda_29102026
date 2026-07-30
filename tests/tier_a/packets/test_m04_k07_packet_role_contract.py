"""Expected-red M04 K07 packet-role contract pending independent MLC-V."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from hashlib import sha256

import pytest
from tests.support.m04_k07_contract_harness import (
    COMMON_CHECKS,
    LINEAGE_FIELDS,
    LINEAGE_MATRIX,
    MUTANTS,
    ROLE_CHECKS,
    ROLES,
    EmissionRejected,
    ProductionSubject,
    ReferenceSubject,
    assert_complete_packet,
    positive_case,
    with_lineage,
)


@pytest.mark.parametrize("role", ROLES)
def test_pf01_reference_subject_accepts_every_complete_role_profile(role: str) -> None:
    case = positive_case(role, activate_conditionals=True)
    packet = ReferenceSubject().emit(case)
    assert_complete_packet(case, packet)
    assert {call.split(":", 1)[0] for call in case.ports.calls} >= {
        "typed_payload",
        "authority_boundary",
    }


@pytest.mark.parametrize("role", ROLES)
@pytest.mark.parametrize("field_name", ("traceid", "runid", "scenarioid"))
@pytest.mark.parametrize("invalid", ("", "contains space", "live"))
def test_pf02_each_missing_or_invalid_context_fact_stands_down_exactly(
    role: str, field_name: str, invalid: str
) -> None:
    case = replace(positive_case(role), **{field_name: invalid})
    with pytest.raises(EmissionRejected, match=field_name) as error:
        ReferenceSubject().emit(case)
    assert error.value.fact == field_name


@pytest.mark.parametrize("role", ROLES)
def test_pf02_no_execution_context_value_is_derived_from_occurrence_identity(role: str) -> None:
    case = positive_case(role)
    packet = ReferenceSubject().emit(case)
    assert packet.packet_id not in packet.context
    assert packet.context == (case.traceid, case.runid, case.scenarioid)


@pytest.mark.parametrize("role", ROLES)
@pytest.mark.parametrize("field_name", LINEAGE_FIELDS)
def test_pf03_explicit_lineage_matrix_enforces_every_cell(role: str, field_name: str) -> None:
    case = positive_case(role)
    state = dict(zip(LINEAGE_FIELDS, LINEAGE_MATRIX[role], strict=True))[field_name]
    empty = [] if field_name in {"parentids", "dependencyids", "sourceartifactids"} else None
    populated = (
        [f"activated::{field_name}"]
        if field_name in {"parentids", "dependencyids", "sourceartifactids"}
        else f"activated::{field_name}"
    )

    if state == "R":
        with pytest.raises(EmissionRejected, match=field_name):
            ReferenceSubject().emit(with_lineage(case, field_name, empty))
    elif state == "N":
        with pytest.raises(EmissionRejected, match=field_name):
            ReferenceSubject().emit(with_lineage(case, field_name, populated))
    else:
        ReferenceSubject().emit(case)
        activated = replace(
            with_lineage(case, field_name, populated),
            activated_lineage=case.activated_lineage | {field_name},
        )
        if field_name == "sourceartifactids":
            activated = replace(
                activated,
                ports=replace(activated.ports, artefacts=set(populated)),
            )
        if field_name == "inputfingerprint":
            activated = with_lineage(
                activated,
                field_name,
                sha256(activated.material).hexdigest(),
            )
        ReferenceSubject().emit(activated)


@pytest.mark.parametrize("role", ROLES)
def test_pf03_source_artefacts_are_retrievable_and_not_replaced_by_fingerprint(
    role: str,
) -> None:
    case = positive_case(role)
    if case.lineage["sourceartifactids"]:
        missing = replace(case, ports=replace(case.ports, artefacts=set()))
        with pytest.raises(EmissionRejected, match="sourceartifactids"):
            ReferenceSubject().emit(missing)
    else:
        ReferenceSubject().emit(case)


@pytest.mark.parametrize("role", ROLES)
def test_pf04_all_common_and_exact_role_checks_arise_from_owner_facts(role: str) -> None:
    case = positive_case(role, activate_conditionals=True)
    packet = ReferenceSubject().emit(case)
    names = tuple(result.name for result in packet.validation_results)
    assert names == (*COMMON_CHECKS, *ROLE_CHECKS[role])
    assert all(result.evidence == f"owner_fact:{result.name}" for result in packet.validation_results)
    assert "typed_payload" in case.ports.calls
    assert "authority_boundary" in case.ports.calls


def test_pf04_typed_contract_and_authority_failures_identify_exact_facts() -> None:
    typed_invalid = positive_case("stage_packet")
    typed_invalid.payload["contract_version"] = "wrong"
    with pytest.raises(EmissionRejected, match="typed_payload"):
        ReferenceSubject().emit(typed_invalid)

    authority_invalid = positive_case("stage_packet")
    authority_invalid.payload["capital_authority"] = True
    with pytest.raises(EmissionRejected, match="authority_boundary"):
        ReferenceSubject().emit(authority_invalid)


def test_pf05_degradation_is_bounded_to_named_optional_quality() -> None:
    case = replace(
        positive_case("prepared_context_packet"),
        optional_limitation="optional_enrichment_unavailable",
    )
    packet = ReferenceSubject().emit(case)
    assert packet.validation_status == "degraded"
    assert packet.summary_flags == ("optional_enrichment_unavailable",)


def test_pf05_binding_failure_and_diagnostic_are_separate_occurrences() -> None:
    binding = replace(positive_case("stage_packet"), traceid="")
    with pytest.raises(EmissionRejected, match="traceid"):
        ReferenceSubject().emit(binding)

    diagnostic = positive_case("diagnostic_packet")
    packet = ReferenceSubject().emit(diagnostic)
    assert packet.role == "diagnostic_packet"
    assert packet.packet_id != binding.packet_id
    assert packet.context != (binding.traceid, binding.runid, binding.scenarioid)
    assert packet.outcome == "authoritative"


def test_pf06_replay_result_with_missing_evidence_is_non_authoritative_incomplete() -> None:
    case = replace(
        positive_case("replay_result_packet"),
        authoritative_evidence_available=False,
    )
    packet = ReferenceSubject().emit(case)
    assert packet.outcome == "non_authoritative_incomplete"
    assert packet.validation_status == "valid"


@pytest.mark.parametrize(
    "role", ("replay_request_packet", "replay_result_packet", "replay_comparison_packet")
)
def test_pf06_new_replay_occurrence_has_new_identity_and_controlled_time(role: str) -> None:
    case = positive_case(role)
    packet = ReferenceSubject().emit(case)
    assert packet.packet_id != case.preserved_original_id
    assert packet.emitted_at != case.preserved_original_time
    assert packet.lineage["replayref"]
    assert packet.lineage["replaytraceid"]


def test_pf07_occurrence_time_extensions_and_side_effect_boundaries() -> None:
    case = positive_case("stage_packet", activate_conditionals=True)
    packet = ReferenceSubject().emit(case)
    assert packet.packet_id == case.packet_id
    assert packet.emitted_at == datetime(2026, 7, 30, 9, 30, tzinfo=UTC)
    assert packet.extensions == {"nvda": {"contract": "m04.k07.v1"}}
    assert packet.side_effects == ()


def test_pf07_unlisted_roles_are_rejected() -> None:
    case = replace(positive_case("stage_packet"), role="capital_deployment_decision")
    with pytest.raises(EmissionRejected, match="packetrole"):
        ReferenceSubject().emit(case)


def _mutant_context_default(subject: ReferenceSubject) -> None:
    packet = subject.emit(replace(positive_case("stage_packet"), traceid=""))
    assert packet.context[0] == ""


def _mutant_drop_lineage(subject: ReferenceSubject) -> None:
    case = positive_case("stage_packet")
    packet = subject.emit(case)
    assert packet.lineage["sourceartifactids"] == case.lineage["sourceartifactids"]


def _mutant_n_field(subject: ReferenceSubject) -> None:
    case = with_lineage(positive_case("reference_packet"), "decisiontraceid", "decision::bad")
    try:
        subject.emit(case)
    except EmissionRejected as error:
        assert error.fact == "lineage.decisiontraceid:not_applicable"
    else:
        raise AssertionError("not-applicable lineage was accepted")


def _mutant_hardcoded_checks(subject: ReferenceSubject) -> None:
    case = positive_case("stage_packet")
    subject.emit(case)
    assert "typed_payload" in case.ports.calls
    assert "authority_boundary" in case.ports.calls


def _mutant_wrong_reason(subject: ReferenceSubject) -> None:
    with pytest.raises(EmissionRejected) as error:
        subject.emit(replace(positive_case("stage_packet"), traceid=""))
    assert error.value.fact == "traceid"


def _mutant_degraded_bypass(subject: ReferenceSubject) -> None:
    case = replace(
        positive_case("replay_result_packet"),
        authoritative_evidence_available=False,
    )
    packet = subject.emit(case)
    assert packet.validation_status != "degraded"


def _mutant_diagnostic_substitute(subject: ReferenceSubject) -> None:
    packet = subject.emit(positive_case("diagnostic_packet"))
    assert packet.role == "diagnostic_packet"


def _mutant_artifact_hash_substitute(subject: ReferenceSubject) -> None:
    case = positive_case("stage_packet")
    subject.emit(case)
    assert any(call.startswith("artefact:") for call in case.ports.calls)


def _mutant_replay_overclaim(subject: ReferenceSubject) -> None:
    case = replace(
        positive_case("replay_result_packet"),
        authoritative_evidence_available=False,
    )
    assert subject.emit(case).outcome == "non_authoritative_incomplete"


def _mutant_replay_identity_reuse(subject: ReferenceSubject) -> None:
    case = positive_case("replay_result_packet")
    packet = subject.emit(case)
    assert packet.packet_id != case.preserved_original_id
    assert packet.emitted_at != case.preserved_original_time


MUTANT_ASSERTIONS = {
    "MUT-CONTEXT-DEFAULT": _mutant_context_default,
    "MUT-DROP-LINEAGE": _mutant_drop_lineage,
    "MUT-N-FIELD": _mutant_n_field,
    "MUT-HARDCODE-CHECKS": _mutant_hardcoded_checks,
    "MUT-WRONG-REASON": _mutant_wrong_reason,
    "MUT-DEGRADED-BYPASS": _mutant_degraded_bypass,
    "MUT-DIAGNOSTIC-SUBSTITUTE": _mutant_diagnostic_substitute,
    "MUT-ARTIFACT-HASH-SUBSTITUTE": _mutant_artifact_hash_substitute,
    "MUT-REPLAY-OVERCLAIM": _mutant_replay_overclaim,
    "MUT-REPLAY-IDENTITY-REUSE": _mutant_replay_identity_reuse,
}


@pytest.mark.parametrize("mutant", MUTANTS)
def test_pf08_each_named_false_positive_mutant_is_killed(mutant: str) -> None:
    with pytest.raises((AssertionError, EmissionRejected)):
        MUTANT_ASSERTIONS[mutant](ReferenceSubject(mutant))


@pytest.mark.parametrize("role", ROLES)
def test_production_subject_records_complete_k07_validation_profile_expected_red(
    role: str,
) -> None:
    packet = ProductionSubject().emit(positive_case(role, activate_conditionals=True))
    result_names = tuple(check.name for check in packet.validation.checks)
    assert result_names == (*COMMON_CHECKS, *ROLE_CHECKS[role])


@pytest.mark.parametrize("field_name", ("traceid", "runid", "scenarioid"))
def test_production_subject_rejects_missing_context_without_defaulting_expected_red(
    field_name: str,
) -> None:
    with pytest.raises(ValueError, match=field_name):
        ProductionSubject().emit(replace(positive_case("stage_packet"), **{field_name: ""}))
