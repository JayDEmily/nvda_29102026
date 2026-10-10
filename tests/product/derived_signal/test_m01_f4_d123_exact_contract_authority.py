"""F4 D123 first invariant: official OI change for one exact option contract.

Accepted brief K02: D123 = current_OI - prior_official_OI.  Catalogue
D123 declares R047 (call OI) and R048 (put OI).  This public M00 witness
preserves the physical option-right distinction rather than putting an
opposite-right value on the selected option contract to satisfy a join.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 10, 9, tzinfo=UTC)


def _identity(contract: str, right: str) -> raw.RawSelectionIdentityV1:
    return raw.RawSelectionIdentityV1((
        ("contract_id", contract),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal(150)),
        ("option_right", right),
    ))


def test_d123_exact_call_oi_change_with_lawful_put_source_present() -> None:
    m00 = raw.create_owner()
    call = _identity("C150", "call")
    put = _identity("P150", "put")
    for i, (rid, ident, value, age) in enumerate((
        ("R047", call, Decimal(100), timedelta(days=1)),
        ("R047", call, Decimal(125), timedelta(seconds=10)),
        ("R048", put, Decimal(40), timedelta(days=1)),
        ("R048", put, Decimal(42), timedelta(seconds=10)),
    ), 1):
        stamp = NOW - age
        m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=raw.observation_occurrence_id(f"d123-oi-{i}"),
            delivery_artifact_ref=raw.delivery_artifact_ref(f"d123-oi-{i}"),
            source_provider=raw.provider_id("controlled-native-official-oi"),
            native_record={"value": value, "identity": dict(ident.values)},
            received_ts_utc=stamp + timedelta(seconds=1),
            ingestion_sequence=i,
            ingestion_sequence_scope=raw.ingestion_sequence_scope("d123:oi"),
            source_temporal_kind="true_instant",
            source_timestamp_raw=stamp.isoformat(),
            source_timezone_native="UTC",
            raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
            source_variant="official-oi", subject_instrument="NVDA",
            native_units="contracts", revision_vintage_native="official-v1",
        ))
    paths = tuple((key, ("identity", key)) for key, _ in call.values)
    owner = api.create_owner(
        raw_projection_reader=m00.reads,
        raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1(
            f"d123-map-{rid}", 1, raw.RawSignalCatalogueId(rid),
            "controlled-native-official-oi", "official-oi", ("value",),
            "contracts", paths,
        ) for rid in ("R047", "R048")),
        parameter_sets=(api.CalculationParameterSetV1(
            "d123-basic", 1, "P_BASIC", (("subject_instrument", "NVDA"),),
        ),),
        input_selection_policies=(api.InputSelectionPolicyVersionV1(
            "d123-contract", 1, tuple(dict(call.values)),
            timedelta(days=2), timedelta(days=2), ("true_instant",), (),
        ),),
        unit_conventions=(api.UnitConventionVersionV1(
            "d123-units", 1, "contracts", "contracts", Decimal(1), Decimal(0),
        ),),
        contexts=(), utc_now=lambda: NOW,
    )
    request = api.CalculationRequestV1(
        "D123", "NVDA", NOW, NOW, "d123-truth", "d123-basic", 1,
        "d123-contract", 1, (),
        raw_input_bindings=tuple(api.RawInputBindingV1(
            rid, api.VersionRefV1(f"d123-map-{rid}", 1),
            api.VersionRefV1("d123-units", 1), "NVDA", ident,
        ) for rid, ident in (("R047", call), ("R048", put))),
    )
    # Expected from accepted K02 D123 on the selected exact call contract:
    # current 125 minus prior official 100 = 25 contracts.
    selection = owner._selection_policy(request)  # Diagnostic only, not an alternate seam
    assert selection is not None
    assert owner._selection_policy_satisfies_row_authority(
        "D123", request, owner._parameter_sets[("d123-basic", 1)], selection
    )
    assert not owner._bindings_satisfy_join_keys(request, ("R047", "R048"), selection)
    result = owner.materialise(request)
    assert result is not None and result.result == Decimal(25)
    assert result.selection_identity == call
    assert {x.observation_occurrence_id for x in result.raw_input_lineage} == {
        "d123-oi-1", "d123-oi-2",
    }
