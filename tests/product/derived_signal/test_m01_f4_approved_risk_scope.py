"""Owner-approved context amendment: immutable references, never risk answers."""

from dataclasses import FrozenInstanceError

import pytest

from nvda_desk.derived_signal_calculation_truth import _catalogue, api


def test_approved_context_conjunctions_preserve_dependency_edges():
    assert _catalogue.catalogue_row("D175").typed_contexts == (
        "CandidateStructureContext", "RiskScopeContext"
    )
    assert _catalogue.catalogue_row("D189").typed_contexts == (
        "LivePositionContext", "RiskScopeContext"
    )


def test_risk_scope_is_reference_only_and_immutable():
    cls = getattr(api, "RiskScopeContextV1", None)
    assert cls is not None, "approved reference-only risk scope is absent"
    kwargs = dict(
        context_id="scope", version=1, account_identity="account",
        account_subject_identity="account-subject", currency_code="USD",
        sleeve_identity="managed", underlying_identity="NVDA", scope_mode="live_sleeve",
        candidate_structure_ref=api.VersionRefV1("candidate", 1),
        live_position_ref=api.VersionRefV1("live", 1),
        position_membership_source_refs=("raw-position",),
        membership_definition_ref=api.VersionRefV1("membership", 1),
        risk_definition_parameter_ref=api.VersionRefV1("risk-definition", 1),
    )
    scope = cls(**kwargs)
    with pytest.raises(FrozenInstanceError):
        scope.version = 2
    for changed in (
        {"version": 0}, {"currency_code": ""}, {"scope_mode": "accountwide"},
        {"live_position_ref": None}, {"underlying_identity": "OTHER"},
        {"position_membership_source_refs": ()},
        {"position_membership_source_refs": ("duplicate", "duplicate")},
        {"candidate_structure_ref": "candidate"},
    ):
        with pytest.raises((TypeError, ValueError)):
            cls(**(kwargs | changed))
