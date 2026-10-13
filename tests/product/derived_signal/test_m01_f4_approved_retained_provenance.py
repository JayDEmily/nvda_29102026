"""Real persisted M01 predecessor metadata, rather than worker-only labels."""

from dataclasses import replace
from decimal import Decimal as D

import pytest

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

from .test_m01_f4_approved_monetary_policy import NOW, fixture
from .test_m01_f4_rc16_position_public import GREEKS, _public


@pytest.mark.parametrize("identity", tuple(GREEKS))
def test_public_live_greek_retains_actual_position_sources_and_declared_units(identity):
    owner, request = _public(identity)
    occurrence = owner.materialise(request)
    assert occurrence is not None
    projected = owner._occurrence_kernel_value(occurrence)
    metadata = dict(projected.metadata)
    assert metadata.get("position_source_refs") is not None
    assert set(metadata["position_source_refs"]) == {"pos-leg-a", "pos-leg-b"}
    assert (
        metadata["canonical_risk_unit"]
        == {
            "D181": "shares",
            "D182": "shares_per_currency",
            "D183": "currency_per_volatility_point",
            "D184": "currency_per_day",
        }[identity]
    )
    assert metadata["parameter_context_refs"] == occurrence.parameter_context_refs


@pytest.mark.parametrize(
    "identity,key,value", [("D190", "utility_domain", "net_currency"), ("D191", "currency", "USD")]
)
def test_persisted_domain_comes_from_exact_producer_parameter_reference(identity, key, value):
    producer = api.CalculationParameterSetV1("producer", 2, "P_BASIC", ((key, value),))
    owner = api.create_owner(
        raw_projection_reader=raw.create_owner().reads,
        parameter_sets=(producer,),
        utc_now=lambda: NOW,
    )
    occurrence = api.DerivedSignalOccurrenceV1(
        identity,
        "occurrence",
        "definition",
        (api.VersionRefV1("producer", 2),),
        "NVDA",
        None,
        NOW,
        None,
        NOW,
        NOW,
        D(4),
        "utility/currency",
        "scalar",
        (),
        (),
        (),
    )
    metadata = dict(owner._occurrence_kernel_value(occurrence).metadata)
    assert metadata.get(key) == value
    wrong = replace(occurrence, parameter_context_refs=(api.VersionRefV1("producer", 1),))
    assert key not in dict(owner._occurrence_kernel_value(wrong).metadata)
