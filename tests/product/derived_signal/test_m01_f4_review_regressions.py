"""Independent review's four class failures: discriminating repair boundary."""

from dataclasses import replace
from datetime import timedelta
from decimal import Decimal as D
from fractions import Fraction

import pytest

from nvda_desk.derived_signal_calculation_truth import _stage1, api
from nvda_desk.raw_signal_occurrence_truth import api as raw

from .test_m01_f4_approved_execution_edge import case, k
from .test_m01_f4_approved_monetary_policy import (
    NOW,
    action_fixture,
    ev,
    fixture,
    hedge_fixture,
    kv,
)


def public_vega(
    *,
    scope_quantity=D(2),
    scope_multiplier=D(100),
    canonical_unit="USD/vol_point/option_unit",
    scale=D(".01"),
):
    # Direct public M00 ingress: actual source q=2,m=100, per-fraction vega=1.2.
    f = fixture()
    candidate, live, scope, definition, membership = f["contexts"]
    candidate = replace(candidate, leg_quantities=(scope_quantity,))
    live = replace(live, signed_quantities=(scope_quantity,), multipliers=(scope_multiplier,))
    membership = replace(
        membership,
        parameters=(
            ("account_identity", "account"),
            ("sleeve_identity", "managed"),
            ("complete_members", (f"option|{scope_quantity}|position-source",)),
        ),
    )
    contexts = (candidate, live, scope, definition, membership)
    m00 = raw.create_owner()
    values = {"R212": D(2), "R016": D(100), "R116": D("1.2")}
    m00.commands.admit_raw_observation_occurrence(
        raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id("position-source"),
            delivery_artifact_ref=raw.delivery_artifact_ref("review-regression"),
            source_provider=raw.provider_id("review-regression"),
            native_record={**values, "contract_id": "option", "currency": "USD"},
            received_ts_utc=NOW,
            ingestion_sequence=1,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("review-regression"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=NOW.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(r) for r in values),
            subject_instrument="NVDA",
            native_units="native_position",
            revision_vintage_native="1",
        )
    )
    units = {"R212": "contracts", "R016": "shares_per_contract", "R116": canonical_unit}
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(
            raw.RawSignalProjectionMappingV1(
                "map-" + r,
                1,
                raw.RawSignalCatalogueId(r),
                "review-regression",
                None,
                (r,),
                "native_position",
                selection_identity_field_paths=(
                    ("contract_id", ("contract_id",)),
                    ("currency", ("currency",)),
                ),
            )
            for r in values
        ),
        unit_conventions=tuple(
            api.UnitConventionVersionV1(
                "unit-" + r, 1, "native_position", units[r], scale if r == "R116" else D(1), D(0)
            )
            for r in values
        ),
        parameter_sets=(
            api.CalculationParameterSetV1("basic", 1, "P_BASIC", (("rule", "live-exposure"),)),
        ),
        input_selection_policies=(
            api.InputSelectionPolicyVersionV1(
                "selection",
                1,
                ("subject_instrument",),
                timedelta(seconds=30),
                timedelta(seconds=30),
                ("true_instant",),
                (),
            ),
        ),
        contexts=contexts,
        utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D183",
        "NVDA",
        NOW,
        NOW,
        "source-regression",
        "basic",
        1,
        "selection",
        1,
        tuple(api.VersionRefV1(c.context_id, c.version) for c in contexts),
        raw_input_bindings=tuple(
            api.RawInputBindingV1(
                r, api.VersionRefV1("map-" + r, 1), api.VersionRefV1("unit-" + r, 1), "NVDA", None
            )
            for r in values
        ),
    )
    return owner, owner.materialise(request)


def test_explicit_fraction_to_point_unit_conversion_preserves_actual_provenance():
    owner, result = public_vega()
    assert result is not None and result.result == D("2.4")
    metadata = dict(owner._occurrence_kernel_value(result).metadata)
    assert metadata.get("canonical_risk_unit") == "currency_per_volatility_point"


@pytest.mark.parametrize(
    "changed",
    [
        {"scope_quantity": D(20)},
        {"scope_multiplier": D(10)},
        {"canonical_unit": "USD/vol_fraction/option_unit", "scale": D(1)},
        {"canonical_unit": "EUR/vol_point/option_unit"},
    ],
)
def test_actual_scope_and_canonical_units_cannot_be_supplied_as_labels(changed):
    _, result = public_vega(**changed)
    assert result is None


def test_exact_shared_lambda_products_do_not_round_components_independently():
    f = fixture((D(".3"), D(0), D(".7"), D(0)))
    f["params"].update(tail_fraction=D(".0001"), stress_active=False)
    tail = dict(f["derived"]["D162"][0].value)
    tail["CVaR_currency"] = D(3)
    f["derived"]["D162"] = (kv("D162", tuple(tail.items())),)
    result = ev("D189", hedge_fixture(f))
    assert result is not None
    h = dict(result.value)
    assert Fraction(*h["risk_limit_currency_exact"]) == Fraction(1, 3)
    factor = Fraction(h["clipping_fraction"])
    assert tuple(Fraction(x) for _, x in h["adjustment"]) == tuple(
        factor * Fraction(x) for _, x in h["unclipped_adjustment"]
    )
    assert Fraction(*h["adjustment_risk_currency_exact"]) <= Fraction(1, 3)


def test_embedded_risk_reference_claims_require_actual_typed_producer_metadata():
    f = fixture()
    for identity in ("D174", "D162"):
        old = f["derived"][identity][0]
        # Actual typed occurrence and production projection carry empty actual refs.
        occurrence = api.DerivedSignalOccurrenceV1(
            identity,
            identity,
            "reference",
            (),
            "NVDA",
            None,
            NOW,
            None,
            NOW,
            NOW,
            old.value,
            "currency",
            "structured",
            (),
            (),
            (),
        )
        owner = api.create_owner(
            raw_projection_reader=raw.create_owner().reads, utc_now=lambda: NOW
        )
        f["derived"][identity] = (owner._occurrence_kernel_value(occurrence),)
    assert ev("D175", f) is None


@pytest.mark.parametrize("identity", ("D133", "D177"))
def test_execution_reference_claims_require_actual_producer_context_and_convention(identity):
    c = case()
    raw_values = {
        key: (
            k(key, value, contract_id="option", currency="USD", unit_convention_ref=("premium", 1)),
        )
        for key, value in c["raw"].items()
    }
    inputs = {"D133": (k("D133", c["cost"]),), "D177": (k("D177", c["utility"]),)}
    inputs[identity] = (replace(inputs[identity][0], metadata=()),)
    result = _stage1.evaluate_stage1_kernel(
        "D178",
        raw_inputs=raw_values,
        derived_inputs=inputs,
        parameter_set=api.CalculationParameterSetV1(
            "execution-rule", 1, "P_RULE", tuple(c["params"].items())
        ),
        contexts=c["contexts"],
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
    )
    assert result is None


@pytest.mark.parametrize("datum,expected", [(D(".2"), "hold"), (D(".9"), "exit"), (True, None)])
def test_actual_numeric_score_boolean_catalogue_carrier_is_not_python_truthiness(datum, expected):
    f = action_fixture()
    owner = api.create_owner(raw_projection_reader=raw.create_owner().reads, utc_now=lambda: NOW)
    occurrence = api.DerivedSignalOccurrenceV1(
        "D187",
        "score",
        "score-definition",
        (),
        "NVDA",
        None,
        NOW,
        None,
        NOW,
        NOW,
        datum,
        "score/boolean",
        "scalar",
        (),
        (),
        (),
    )
    f["derived"]["D187"] = (owner._occurrence_kernel_value(occurrence),)
    result = ev("D192", f)
    assert (None if result is None else result.value) == expected


@pytest.mark.parametrize("identity", ("D174", "D162"))
def test_embedded_reference_time_cannot_relabel_an_older_actual_producer(identity):
    f = fixture()
    f["derived"][identity] = (replace(f["derived"][identity][0],
        effective_at_utc=NOW - timedelta(seconds=1)),)
    assert ev("D175", f) is None


def test_live_greek_from_another_effective_snapshot_requires_revaluation():
    f = hedge_fixture(fixture())
    f["derived"]["D183"] = (replace(f["derived"]["D183"][0],
        effective_at_utc=NOW - timedelta(seconds=1)),)
    assert ev("D189", f) is None
