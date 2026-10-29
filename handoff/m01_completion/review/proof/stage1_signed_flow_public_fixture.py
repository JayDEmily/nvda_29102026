"""Independent reviewer: authority-derived D016/D120 public-seam fixture."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw

NOW = datetime(2026, 10, 8, 3, 0, tzinfo=UTC)
IDENT = raw.RawSelectionIdentityV1(
    values=(
        ("contract_id", "C100"),
        ("underlying_instrument", "NVDA"),
        ("expiry", "2026-12-18"),
        ("strike", Decimal("100")),
        ("option_right", "call"),
    )
)
raw_values = {
    "R034": Decimal("4"),
    "R035": Decimal("6"),
    "R120": Decimal("6"),
    "R121": Decimal("2"),
    "R126": Decimal("4"),
    "R127": Decimal("6"),
    "R015": Decimal("100"),
}
points = {}
for rid, value in raw_values.items():
    oid = "obs-quote-C100" if rid in ("R034", "R035") else "obs-trade-C100"
    points[rid] = raw.ProjectedRawValueV1(
        raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
        observation_occurrence_id=raw.observation_occurrence_id(oid),
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
        ingestion_sequence_scope=raw.ingestion_sequence_scope("p:snapshot"),
        revision_vintage_native=None,
        selection_identity=IDENT,
    )


class Reader:
    def list_projected_raw_history(self, raw_signal_catalogue_id, **kwargs):
        rid = raw_signal_catalogue_id.value
        return raw.ProjectedRawHistoryPageV1(
            items=(points[rid],) if rid in points else (), next_cursor=None
        )

    def project_raw_value(self, *args, **kwargs):
        return None


unit = api.UnitConventionVersionV1("unit-number", 1, "number", "number", Decimal(1), Decimal(0))
models = tuple(
    raw.RawSignalProjectionMappingV1(
        mapping_id=f"map-{rid}",
        version=1,
        raw_signal_catalogue_id=raw.RawSignalCatalogueId(rid),
        source_provider="p",
        source_variant="snapshot",
        native_field_path=("field", rid),
        native_units="number",
    )
    for rid in raw_values
)
params = (
    api.CalculationParameterSetV1("p-basic", 1, "P_BASIC", (("selection_mode", "exact"),)),
    api.CalculationParameterSetV1(
        "p-rule", 1, "P_RULE", (("selection_mode", "exact"), ("window_seconds", Decimal(60)))
    ),
)
selection = api.InputSelectionPolicyVersionV1(
    context_id="exact-contract",
    version=1,
    join_keys=("contract_id", "underlying_instrument", "expiry", "strike", "option_right"),
    maximum_staleness=timedelta(minutes=1),
    maximum_skew=timedelta(seconds=10),
    temporal_basis_permissions=("true_instant",),
    basket_membership=(),
)
bindings = tuple(
    api.RawInputBindingV1(
        rid,
        api.VersionRefV1(f"map-{rid}", 1),
        api.VersionRefV1("unit-number", 1),
        "NVDA",
        selection_identity=IDENT,
    )
    for rid in raw_values
)
owner = api.create_owner(
    raw_projection_reader=Reader(),
    raw_projection_mappings=models,
    parameter_sets=params,
    input_selection_policies=(selection,),
    unit_conventions=(unit,),
    contexts=(),
    utc_now=lambda: NOW,
)


def request(did):
    rule = "p-basic" if did == "D011" else "p-rule"
    return api.CalculationRequestV1(
        derived_signal_id=did,
        subject_instrument="NVDA",
        as_of_utc=NOW,
        knowledge_cutoff_utc=NOW,
        calculation_definition_version="calc-v1",
        parameter_set_id=rule,
        parameter_set_version=1,
        input_selection_policy_id="exact-contract",
        input_selection_policy_version=1,
        context_refs=(),
        parameter_profile_refs=(
            api.ParameterProfileRefV1("P_BASIC", "p-basic", 1),
            api.ParameterProfileRefV1("P_RULE", "p-rule", 1),
        ),
        raw_input_bindings=bindings,
    )


if __name__ == "__main__":
    for d in ("D011", "D015", "D016", "D120"):
        result = owner.materialise(request(d))
        print(f"{d}: {None if result is None else result.result!r}")
        if result is not None:
            print(f"{d}_id: {result.derived_occurrence_id}")
            raw_ids = sorted({item.observation_occurrence_id for item in result.raw_input_lineage})
            print(f"{d}_raw_ids: {raw_ids}")
            print(f"{d}_predecessor_ids: {result.predecessor_occurrence_ids}")
    print("NORMATIVE_EXPECTED_D120: ((signed_contracts, 2), (signed_premium_notional, 1200))")
