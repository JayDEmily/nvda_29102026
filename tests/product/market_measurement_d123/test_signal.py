"""D123 selected exact CALL official OI period/revision and same-period refusal."""
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
SUBJECT = "controlled-nvda-2026-12-18-C150"
PROVIDER, VARIANT = "foundation-controlled-official-oi", "period_v1"
BRIEF = "5451c5c6c99559cc859b5aecac4cffa1ea6aa18676d53dbb3e77bb67222ad4dc"
META = tuple((key, ("identity", key)) for key in (
    "contract_id", "underlying_instrument", "expiry", "strike", "option_right",
    "official_reporting_period_id", "official_reporting_period_order",
    "official_revision_id", "official_revision_precedence",
))
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-d123-r047-official-oi", 1, r.RawSignalCatalogueId("R047"),
    PROVIDER, VARIANT, ("quantity",), "contracts", META,
)
UNIT = f.UnitConventionVersionV1("mmt-d123-contracts", 1, "contracts", "contracts",
                                 Decimal(1), Decimal(0))
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/D123_CALCULATION_DEFINITION_AUTHORISED_CLARIFICATION_20261011.md",
        "3dcbb5090f0e32e909e16b361b7b93b2a28cae6e5cc687475e8f78c1e83304ad",
    ),
)
CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-official-oi-selection", 1),
    datetime(2026, 10, 20, 12, tzinfo=UTC), datetime(2026, 10, 20, 13, tzinfo=UTC),
    datetime(2026, 10, 20, 12, tzinfo=UTC),
)
DEFINITION = f.CalculationDefinitionV1(
    "D123", "D123-20261011-01", "K02_ALGEBRA",
    "highest official current period revision minus highest prior distinct period revision",
    ("R047", "R048"), (), "P_BASIC", "contracts", "exact_ratio", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1(
    "mmt-d123-controlled", 1, "P_BASIC", SUBJECT, (SUBJECT,),
)
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d123-selection", 1,
    ("subject_instrument", "contract_id", "underlying_instrument", "expiry", "strike",
     "option_right"), timedelta(seconds=60), timedelta(0), ("true_instant",),
    (SUBJECT,), PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)


def request():
    return f.WindowCalculationRequestV1(f.CalculationRequestV1(
        "D123", SUBJECT, T, CUTOFF, DEFINITION.calculation_definition_version,
        f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1),
        (CONTEXT.ref,), (f.RawInputBindingV1(
            "R047", f.VersionRefV1(MAPPING.mapping_id, 1),
            f.VersionRefV1(UNIT.context_id, 1), SUBJECT,
        ),),
    ), CONTEXT, ())


def native(index, refused):
    period = "P2" if refused or index else "P1"
    return {"quantity": (Decimal(100), Decimal(125), Decimal(130))[index],
            "identity": {
                "contract_id": "C150", "underlying_instrument": "NVDA",
                "expiry": "2026-12-18", "strike": "150", "option_right": "call",
                "official_reporting_period_id": period,
                "official_reporting_period_order": 2 if period == "P2" else 1,
                "official_revision_id": ("precursor", "base", "correction")[index],
                "official_revision_precedence": (1, 2, 3)[index],
            }}


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d123_signal(tmp_path, refused):
    raw = r.create_owner()
    for index in range(3):
        raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(f"d123-{index}"),
            delivery_artifact_ref=r.delivery_artifact_ref("d123-controlled"),
            source_provider=r.provider_id(PROVIDER), native_record=native(index, refused),
            received_ts_utc=T - timedelta(seconds=3-index), ingestion_sequence=index+1,
            ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=(MAPPING.raw_signal_catalogue_id,),
            source_variant=VARIANT, subject_instrument=SUBJECT, native_units="contracts",
            source_timestamp_raw="2026-10-20T12:39:50Z", source_timezone_native="UTC",
        ))
    page = raw.reads.list_projected_raw_history(
        MAPPING.raw_signal_catalogue_id, mappings=(MAPPING,), subject_instrument=SUBJECT,
        received_at_or_before_utc=CUTOFF, event_at_or_before_utc=T, limit=100, cursor=None,
    )
    assert page.next_cursor is None and len(page.items) == 3
    projected = sorted(page.items, key=lambda item: item.ingestion_sequence)
    for index, item in enumerate(projected):
        obj = native(index, refused)
        assert item.native_value == obj["quantity"]
        assert item.observation_occurrence_id.value == f"d123-{index}"
        assert item.selection_identity == r.RawSelectionIdentityV1(tuple(
            (key, obj["identity"][key]) for key, _ in META))
    periods = tuple(item.selection_identity.value_for("official_reporting_period_id")
                    for item in projected)
    assert periods == (("P2", "P2", "P2") if refused else ("P1", "P2", "P2"))
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d123.sqlite")
    owner = f.create_window_owner(admission=admission, raw_projection_reader=raw.reads,
                                  storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW)
    result = owner.materialise(request())
    reader = f.create_window_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    args = dict(derived_signal_id="D123", subject_instrument=SUBJECT,
                effective_at_or_before_utc=T, knowledge_at_or_before_utc=CUTOFF, limit=10)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(**args) == ()
        assert reader.list_derived_history(**args) == ()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    assert result.result == f.ExactRatioV1(30, 1)
    assert result.request == request() and result.definition == DEFINITION
    assert result.parameter_set == PARAMETER and result.input_selection_policy == POLICY
    assert result.projection_mappings == (MAPPING,) and result.unit_conventions == (UNIT,)
    assert tuple(line.projection for line in result.raw_input_lineage) == (
        projected[0], projected[2])
    assert result.predecessors == () and result.units == "contracts"
    assert result.result_shape == "exact_ratio"
    assert result.implementation_brief_sha256 == BRIEF
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc,
            result.calculated_at_utc) == (T, CUTOFF, NOW)
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert reader.list_derived_history(**args) == (result,)
