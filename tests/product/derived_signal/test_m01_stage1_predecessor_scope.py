"""Reviewer 2026-10-08: public-seam proof for different parent/child selection scopes."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw_api

NOW = datetime(2026, 10, 8, 5, 30, tzinfo=UTC)
EXACT = ("contract_id", "underlying_instrument", "expiry", "strike", "option_right")
PAIR = ("underlying_instrument", "expiry", "strike")


def _contract(
    contract: str, right: str, strike: Decimal = Decimal("100")
) -> raw_api.RawSelectionIdentityV1:
    return raw_api.RawSelectionIdentityV1(
        values=(
            ("contract_id", contract),
            ("underlying_instrument", "NVDA"),
            ("expiry", "2026-12-18"),
            ("strike", strike),
            ("option_right", right),
        )
    )


def _setup(
    *,
    target: str,
    missing: tuple[str, str] | None = None,
    wrong: tuple[str, str] | None = None,
    child_policy: bool = True,
    reversed_bindings: bool = False,
    put_strike: Decimal = Decimal("100"),
    put_delta: Decimal = Decimal("-0.5"),
) -> tuple[object, api.CalculationRequestV1]:
    identities = {
        "C100": _contract("C100", "call"),
        "P100": _contract("P100", "put", put_strike),
    }
    points = {
        ("R034", "C100"): Decimal("4"),
        ("R035", "C100"): Decimal("6"),
        ("R034", "P100"): Decimal("3"),
        ("R035", "P100"): Decimal("5"),
        ("R112", "C100"): Decimal("0.5"),
        ("R112", "P100"): put_delta,
        ("R014", "C100"): Decimal("100"),
        ("R014", "P100"): put_strike,
    }
    if missing is not None:
        del points[missing]

    def point_identity(raw_id: str, contract: str) -> raw_api.RawSelectionIdentityV1:
        original = identities[contract]
        if wrong != (raw_id, contract):
            return original
        return raw_api.RawSelectionIdentityV1(
            values=tuple(
                (key, Decimal("105") if key == "strike" else value)
                for key, value in original.values
            )
        )

    units = api.UnitConventionVersionV1(
        context_id="unit-price",
        version=1,
        native_units="number",
        canonical_units="number",
        scale=Decimal(1),
        offset=Decimal(0),
    )
    mappings = tuple(
        raw_api.RawSignalProjectionMappingV1(
            mapping_id=f"map-{rid}",
            version=1,
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(rid),
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("field", rid),
            native_units="number",
        )
        for rid in ("R034", "R035", "R112", "R014")
    )
    projections = {}
    for (rid, contract), value in points.items():
        projections[(rid, contract)] = raw_api.ProjectedRawValueV1(
            raw_signal_catalogue_id=raw_api.RawSignalCatalogueId(rid),
            observation_occurrence_id=raw_api.observation_occurrence_id(f"obs-{rid}-{contract}"),
            projection_mapping_id=f"map-{rid}",
            projection_mapping_version=1,
            source_provider="p",
            source_variant="snapshot",
            native_field_path=("field", rid),
            native_value=value,
            native_units="number",
            subject_instrument="NVDA",
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            received_ts_utc=NOW,
            ingestion_sequence=int(rid[1:]),
            ingestion_sequence_scope=raw_api.ingestion_sequence_scope("p:snapshot"),
            revision_vintage_native=None,
            selection_identity=point_identity(rid, contract),
        )

    class Reader:
        def list_projected_raw_history(self, raw_signal_catalogue_id: Any, **kwargs: Any) -> Any:
            rid = raw_signal_catalogue_id.value
            return raw_api.ProjectedRawHistoryPageV1(
                items=tuple(p for (signal, _), p in projections.items() if signal == rid),
                next_cursor=None,
            )

        def project_raw_value(self, *args: object, **kwargs: object) -> object | None:
            return None

    basic = api.CalculationParameterSetV1(
        context_id="p-basic",
        version=1,
        profile="P_BASIC",
        parameters=(("atm_delta_bucket", "atm"),),
    )
    rule = api.CalculationParameterSetV1(
        context_id="p-rule",
        version=1,
        profile="P_RULE",
        parameters=(
            ("delta_bucket_boundaries", (Decimal(0), Decimal("0.4"), Decimal(1))),
            ("delta_bucket_labels", ("wing", "atm")),
        ),
    )
    parent = api.InputSelectionPolicyVersionV1(
        context_id="parent-pair" if target == "D109" else "parent-structure",
        version=1,
        join_keys=PAIR if target == "D109" else ("subject_instrument",),
        maximum_staleness=timedelta(minutes=1),
        maximum_skew=timedelta(seconds=10),
        temporal_basis_permissions=("true_instant",),
        basket_membership=(),
    )
    exact = replace(parent, context_id="child-exact", join_keys=EXACT)
    candidate = api.CandidateStructureContextV1(
        context_id="two-leg",
        version=1,
        candidate_identity="long-straddle",
        leg_contract_identities=("C100", "P100"),
        leg_sides=("buy", "buy"),
        leg_quantities=(Decimal(1), Decimal(1)),
        quantity=Decimal(1),
        premium_assumptions=(("C100", Decimal(5)), ("P100", Decimal(4))),
        entry_assumptions=(),
        risk_capital_currency=Decimal(1000),
    )
    binds = tuple(
        api.RawInputBindingV1(
            rid,
            api.VersionRefV1(f"map-{rid}", 1),
            api.VersionRefV1("unit-price", 1),
            "NVDA",
            selection_identity=point_identity(rid, contract),
        )
        for (rid, contract) in points
    )
    if reversed_bindings:
        binds = tuple(reversed(binds))
    owner = api.create_owner(
        raw_projection_reader=Reader(),
        raw_projection_mappings=mappings,
        parameter_sets=(basic, rule),
        input_selection_policies=(parent, exact) if child_policy else (parent,),
        unit_conventions=(units,),
        contexts=(candidate,),
        utc_now=lambda: NOW,
    )
    selections = (("D087", api.VersionRefV1("child-exact", 1)),)
    if target == "D109":
        selections += (("D091", api.VersionRefV1("child-exact", 1)),)
    request = api.CalculationRequestV1(
        derived_signal_id=target,
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-v1",
        parameter_set_id="p-basic",
        parameter_set_version=1,
        input_selection_policy_id=parent.context_id,
        input_selection_policy_version=1,
        context_refs=(api.VersionRefV1("two-leg", 1),) if target == "D170" else (),
        parameter_profile_refs=(api.ParameterProfileRefV1("P_RULE", "p-rule", 1),),
        raw_input_bindings=binds,
        predecessor_selection_policy_refs=selections,
    )
    return owner, request


@pytest.mark.parametrize(
    "target,result",
    [
        ("D109", Decimal("9")),
        ("D170", (Decimal("91"), Decimal("109"))),
    ],
)
def test_public_aggregate_resolves_both_exact_contract_occurrences_and_lineage(
    target: str,
    result: object,
) -> None:
    owner, request = _setup(target=target)
    occurrence = owner.materialise(request)
    assert occurrence is not None
    assert occurrence.result == result
    mids = [
        owner.reads.get_derived_occurrence(ref) for ref in occurrence.predecessor_occurrence_ids
    ]
    assert len([p for p in mids if p and p.derived_signal_id == "D087"]) == 2
    assert {
        p.selection_identity.value_for("contract_id")
        for p in mids
        if p and p.derived_signal_id == "D087"
    } == {"C100", "P100"}
    assert all(p and api.VersionRefV1("child-exact", 1) in p.parameter_context_refs for p in mids)
    assert {item.observation_occurrence_id for item in occurrence.raw_input_lineage} >= {
        f"obs-R034-{c}" for c in ("C100", "P100")
    }
    again = owner.materialise(request)
    assert again is not None and again.derived_occurrence_id == occurrence.derived_occurrence_id
    reordered_owner, reordered_request = _setup(target=target, reversed_bindings=True)
    reordered = reordered_owner.materialise(reordered_request)
    assert (
        reordered is not None
        and reordered.derived_occurrence_id == occurrence.derived_occurrence_id
    )


@pytest.mark.parametrize(
    "target,missing",
    [
        ("D109", ("R035", "P100")),
        ("D109", ("R112", "C100")),
        ("D170", ("R034", "P100")),
        ("D170", ("R014", "P100")),
    ],
)
def test_public_aggregate_refuses_incomplete_contract_edge(
    target: str, missing: tuple[str, str]
) -> None:
    owner, request = _setup(target=target, missing=missing)
    assert owner.materialise(request) is None


@pytest.mark.parametrize("target", ["D109", "D170"])
def test_public_aggregate_refuses_missing_explicit_child_policy(target: str) -> None:
    owner, request = _setup(target=target, child_policy=False)
    assert owner.materialise(request) is None


@pytest.mark.parametrize("target", ["D109", "D170"])
def test_public_aggregate_refuses_cross_contract_strike_mismatch(target: str) -> None:
    owner, request = _setup(target=target, wrong=("R034", "P100"))
    assert owner.materialise(request) is None


def test_multi_strike_structure_keeps_per_leg_contract_identity() -> None:
    # Unlike an ATM pair, a structure can have genuinely different strikes.
    owner, request = _setup(target="D170", put_strike=Decimal("105"))
    result = owner.materialise(request)
    assert result is not None and result.result == (Decimal("96"), Decimal("109"))
    children = [
        owner.reads.get_derived_occurrence(ref) for ref in result.predecessor_occurrence_ids
    ]
    premiums = [child for child in children if child and child.derived_signal_id == "D087"]
    assert {item.selection_identity.value_for("strike") for item in premiums} == {
        Decimal("100"),
        Decimal("105"),
    }


def test_atm_pair_refuses_non_atm_member_under_named_delta_bucket() -> None:
    owner, request = _setup(target="D109", put_delta=Decimal("-0.25"))
    assert owner.materialise(request) is None
