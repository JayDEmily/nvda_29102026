"""D116 authority-derived public M00-to-M01 proof: exact option volume / applicable OI.

Programme Owner 2026-10-11: R041 and one conditional R047/R048; never R075.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 11, 4, tzinfo=UTC)


def identity(
    right: str = "call",
    *,
    contract: str | None = None,
    strike: Decimal = Decimal(150),
    expiry: str = "2026-12-18",
    underlying: str = "NVDA",
) -> raw.RawSelectionIdentityV1:
    return raw.RawSelectionIdentityV1(
        (
            ("contract_id", contract or ("C150" if right == "call" else "P150")),
            ("underlying_instrument", underlying),
            ("expiry", expiry),
            ("strike", strike),
            ("option_right", right),
        )
    )


def public(
    *,
    right: str = "call",
    denominator: Decimal = Decimal(1000),
    volume: Decimal = Decimal(300),
    missing: str | None = None,
    wrong: str | None = None,
    future: str | None = None,
    opposing: bool = False,
    unrelated: bool = False,
    r075: bool = False,
    bind_override: tuple[str, ...] | None = None,
    version_error: str | None = None,
    cutoff: datetime = NOW,
    observed_at: datetime | None = None,
    extra_oi: Decimal | None = None,
    extra_age_seconds: int = 0,
    persistence: object | None = None,
) -> tuple[api.DerivedSignalCalculationOwnerV1, api.CalculationRequestV1]:
    m00 = raw.create_owner()
    selected = identity(right)
    oi = "R047" if right == "call" else "R048"
    other = "R048" if right == "call" else "R047"
    observations = [("R041", volume, selected), (oi, denominator, selected)]
    if opposing:
        observations.append((other, Decimal(10), identity("put" if right == "call" else "call")))
    if unrelated:
        for mutation in (
            {"contract": "ANOTHER"},
            {"strike": Decimal(151)},
            {"expiry": "2027-01-15"},
            {"underlying": "AMD"},
        ):
            observations.append((oi, Decimal(50), identity(right, **mutation)))
    if r075:
        observations.append(("R075", Decimal(200), selected))
    if extra_oi is not None:
        observations.append((oi, extra_oi, selected))
    valid_ids = ("R041", "R047", "R048", "R075")
    for index, (rid, value, ident) in enumerate(observations, 1):
        if rid == missing:
            continue
        if rid == wrong and ident == selected:
            ident = identity(right, contract="WRONG")
        stamp = observed_at or NOW - timedelta(seconds=5)
        if extra_oi is not None and index == len(observations):
            stamp -= timedelta(seconds=extra_age_seconds)
        received = NOW + timedelta(seconds=1) if rid == future else stamp
        m00.commands.admit_raw_observation_occurrence(
            raw.RawObservationOccurrenceV1(
                concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=raw.observation_occurrence_id(f"d116-{index}"),
                delivery_artifact_ref=raw.delivery_artifact_ref(f"d116-{index}"),
                source_provider=raw.provider_id("controlled-d116"),
                native_record={"metric": {rid: value}, "identity": dict(ident.values)},
                received_ts_utc=received,
                ingestion_sequence=index,
                ingestion_sequence_scope=raw.ingestion_sequence_scope("d116:volume-oi"),
                source_temporal_kind="true_instant",
                source_timestamp_raw=stamp.isoformat(),
                source_timezone_native="UTC",
                raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
                source_variant="controlled-option",
                subject_instrument="NVDA",
                native_units="contracts",
                revision_vintage_native="controlled-v1",
            )
        )
    paths = tuple((key, ("identity", key)) for key, _ in selected.values)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        persistence=persistence,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "d116-map-" + rid,
                1,
                raw.RawSignalCatalogueId(rid),
                "controlled-d116",
                "controlled-option",
                ("metric", rid),
                "contracts",
                paths,
            )
            for rid in valid_ids
        ),
        parameter_sets=(
            api.CalculationParameterSetV1(
                "d116-basic",
                1,
                "P_BASIC",
                (("subject_instrument", "NVDA"),),
            ),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "d116-exact",
                1,
                tuple(dict(selected.values)),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                (),
            ),
        ),
        unit_conventions=(
            api.UnitConventionVersionV1(
                "d116-contracts",
                1,
                "contracts",
                "contracts",
                Decimal(1),
                Decimal(0),
            ),
        ),
        contexts=(),
        utc_now=lambda: NOW,
    )
    bindings = bind_override if bind_override is not None else ("R041", oi)
    req = api.CalculationRequestV1(
        "D116",
        "NVDA",
        NOW,
        cutoff,
        "D116-20261011-01",
        "d116-basic",
        1,
        "d116-exact",
        1,
        (),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                rid,
                api.VersionRefV1("d116-map-" + rid, 2 if rid == version_error else 1),
                api.VersionRefV1("d116-contracts", 1),
                "NVDA",
                selected,
            )
            for rid in bindings
        ),
    )
    return owner, req


@pytest.mark.parametrize("right", ("call", "put"))
@pytest.mark.parametrize("opposing", (False, True))
@pytest.mark.parametrize("unrelated", (False, True))
def test_d116_correct_ratio_persistence_identity_lineage_and_retry(
    right: str,
    opposing: bool,
    unrelated: bool,
) -> None:
    owner, req = public(right=right, opposing=opposing, unrelated=unrelated, r075=True)
    result = owner.materialise(req)
    oi = "R047" if right == "call" else "R048"
    assert result is not None and result.result == Decimal("0.3")
    assert result.selection_identity == identity(right)
    assert {line.raw_signal_id for line in result.raw_input_lineage} == {"R041", oi}
    assert {line.observation_occurrence_id for line in result.raw_input_lineage} == {
        "d116-1",
        "d116-2",
    }
    assert owner.materialise(req) == result


@pytest.mark.parametrize("right", ("call", "put"))
def test_d116_valid_zero_numerator_is_zero_not_absent(right: str) -> None:
    owner, req = public(right=right, volume=Decimal(0))
    result = owner.materialise(req)
    assert result is not None and result.result == Decimal(0)


@pytest.mark.parametrize("right", ("call", "put"))
@pytest.mark.parametrize("denominator", (Decimal(0), Decimal(-1)))
def test_d116_zero_or_negative_oi_refuses(right: str, denominator: Decimal) -> None:
    owner, req = public(right=right, denominator=denominator)
    assert owner.materialise(req) is None


@pytest.mark.parametrize("right", ("call", "put"))
def test_d116_missing_applicable_side_and_r075_substitution_refuses(right: str) -> None:
    oi = "R047" if right == "call" else "R048"
    owner, req = public(right=right, missing=oi, r075=True)
    assert owner.materialise(req) is None
    owner, req = public(right=right, r075=True, bind_override=("R041", "R075"))
    assert owner.materialise(req) is None


@pytest.mark.parametrize("right", ("call", "put"))
def test_d116_contract_and_temporal_and_version_incompatibilities_refuse(right: str) -> None:
    oi = "R047" if right == "call" else "R048"
    for changes in (
        {"wrong": oi},
        {"future": oi},
        {"version_error": oi},
        {"missing": "R041"},
        {"observed_at": NOW - timedelta(seconds=45)},
        {"cutoff": NOW - timedelta(seconds=10)},
    ):
        owner, req = public(right=right, **changes)
        assert owner.materialise(req) is None, changes
    owner, req = public(right=right)
    altered = replace(
        req,
        raw_input_bindings=(
            replace(
                req.raw_input_bindings[0],
                selection_identity=identity(right, underlying="AMD"),
            ),
            req.raw_input_bindings[1],
        ),
    )
    assert owner.materialise(altered) is None


def test_d116_latest_current_oi_only_has_exact_selected_lineage() -> None:
    owner, req = public(extra_oi=Decimal(2222), extra_age_seconds=15)
    result = owner.materialise(req)
    assert result is not None and result.result == Decimal("0.3")
    assert {item.observation_occurrence_id for item in result.raw_input_lineage} == {
        "d116-1",
        "d116-2",
    }


def test_d116_ambiguous_same_time_competing_oi_refuses() -> None:
    owner, req = public(extra_oi=Decimal(2222))
    assert owner.materialise(req) is None


def test_d116_opposite_side_alone_cannot_substitute_applicable_side() -> None:
    owner, req = public(missing="R047", opposing=True)
    assert owner.materialise(req) is None
    owner, req = public(right="put", missing="R048", opposing=True)
    assert owner.materialise(req) is None
