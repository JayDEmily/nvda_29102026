"""D009 atomic three-vintage public statuses and reached partial-newest refusal."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 9, 14, tzinfo=UTC)
NOW = T + timedelta(seconds=1)
PROVIDER, VARIANT = "foundation-controlled-macro", "vintage_v1"
SERIES, PERIOD = "controlled-macro-series/1", "2026-09"
BRIEF = "d548557226dcb7dfaac12aa12f4287adb37b6c897e481e50e980ac4a1bfd92bc"
META = (
    ("series.id", ("series", "id")), ("reference.period", ("series", "period")),
    ("vintage.id", ("vintage", "id")), ("field.role", ("field", "role")),
    ("publication.ordinal", ("publication", "ordinal")),
    ("publication.timestamp", ("publication", "timestamp")),
)
MAPS = tuple(r.RawSignalProjectionMappingV1(
    f"mmt-d009-r{raw}", 1, r.RawSignalCatalogueId(f"R{raw}"), PROVIDER,
    VARIANT, ("macro", field), unit, META,
) for raw, field, unit in (
    ("280", "realtime_start", "native_date"),
    ("281", "realtime_end", "native_date"),
    ("282", "last_updated", "native_offset_datetime"),
))
UNITS = tuple(f.UnitConventionVersionV1(
    f"mmt-d009-{raw}", 1, native, canonical, Decimal(1), Decimal(0),
) for raw, native, canonical in (
    ("r280", "native_date", "date"), ("r281", "native_date", "date"),
    ("r282", "native_offset_datetime", "UTC_datetime"),
))
AUTHORITY = (
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md",
        "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c",
    ),
    f.AuthorityArtifactRefV1(
        "handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv",
        "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549",
    ),
)
DEFINITION = f.CalculationDefinitionV1(
    "D009", "D009-VINTAGE-STATUS-1", "K01_TIME",
    "each visible immutable macro vintage classified at cutoff by separate publication order",
    ("R280", "R281", "R282"), (), "P_TIME", "category", "vintage_status", AUTHORITY,
)
PARAMETER = f.CalculationParameterSetV1("mmt-d009-controlled", 1, "P_TIME", "NVDA", ("NVDA",))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-d009-selection", 1, ("series.id", "reference.period", "vintage.id"),
    timedelta(hours=4), timedelta(0), ("date_only", "true_instant"), ("NVDA",),
    PROVIDER, VARIANT, PROVIDER + "/" + VARIANT, 100, 1000,
)
VINTAGES = (
    ("v1", 1, "2026-10-09T11:00:00Z", "2026-10-09T11:05:00Z",
     "2026-10-01", "2026-10-31", "2026-10-09T10:50:00+00:00", "initial"),
    ("v2", 2, "2026-10-09T12:00:00Z", "2026-10-09T12:05:00Z",
     "2026-10-02", "2026-11-01", "2026-10-09T11:50:00+00:00", "revised"),
    ("v3", 3, "2026-10-09T13:00:00Z", "2026-10-09T13:05:00Z",
     "2026-10-03", "2026-11-02", "2026-10-09T12:50:00+00:00",
     "latest_known_at_cutoff"),
)


def request():
    return f.VintageStatusRequestV1(
        f.CalculationRequestV1(
            "D009", "NVDA", T, T, DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id, 1), f.VersionRefV1(POLICY.context_id, 1), (),
            tuple(f.RawInputBindingV1(m.raw_signal_catalogue_id.value,
                                      f.VersionRefV1(m.mapping_id, 1),
                                      f.VersionRefV1(u.context_id, 1), "NVDA")
                  for m, u in zip(MAPS, UNITS, strict=True)),
        ), SERIES, PERIOD,
    )


@pytest.mark.parametrize("refused", (False, True), ids=("success", "refusal"))
def test_d009_signal(tmp_path, refused):
    raw = r.create_owner()
    projected = {}
    for vintage_id, ordinal, pub, receipt, start, end, updated, _ in VINTAGES:
        for role, (mapping, native) in enumerate(zip(MAPS, (start, end, updated), strict=True)):
            if refused and vintage_id == "v3" and role == 2:
                continue
            identity = r.RawSelectionIdentityV1((
                ("series.id", SERIES), ("reference.period", PERIOD),
                ("vintage.id", vintage_id),
                ("field.role", ("realtime_start", "realtime_end", "last_updated")[role]),
                ("publication.ordinal", ordinal), ("publication.timestamp", pub),
            ))
            raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
                concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
                contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
                observation_occurrence_id=r.observation_occurrence_id(f"d009-{vintage_id}-{role}"),
                delivery_artifact_ref=r.delivery_artifact_ref("d009-controlled"),
                source_provider=r.provider_id(PROVIDER),
                native_record={"series": {"id": SERIES, "period": PERIOD},
                               "vintage": {"id": vintage_id},
                               "field": {"role": identity.value_for("field.role")},
                               "publication": {"ordinal": ordinal, "timestamp": pub},
                               "macro": {mapping.native_field_path[-1]: native}},
                received_ts_utc=datetime.fromisoformat(receipt.replace("Z", "+00:00")),
                ingestion_sequence=ordinal * 10 + role,
                ingestion_sequence_scope=r.ingestion_sequence_scope(PROVIDER + "/" + VARIANT),
                source_temporal_kind="true_instant" if role == 2 else "date_only",
                raw_signal_catalogue_ids=(mapping.raw_signal_catalogue_id,),
                source_variant=VARIANT, subject_instrument="NVDA",
                native_units=mapping.native_units,
                source_timestamp_raw=native,
                source_timezone_native="UTC" if role == 2 else None,
            ))
            page = raw.reads.list_projected_raw_history(
                mapping.raw_signal_catalogue_id, mappings=(mapping,), subject_instrument="NVDA",
                received_at_or_before_utc=T, event_at_or_before_utc=None, limit=100, cursor=None,
            )
            assert page.next_cursor is None
            matched = tuple(i for i in page.items if i.selection_identity == identity)
            assert len(matched) == 1
            assert matched[0].native_value == native
            assert matched[0].received_ts_utc == datetime.fromisoformat(
                receipt.replace("Z", "+00:00"))
            projected[(vintage_id, role)] = matched[0]
    assert len(projected) == (8 if refused else 9)
    admission = f.OwnerAdmissionV1("M02", BRIEF)
    path = str(tmp_path / "d009.sqlite")
    owner = f.create_vintage_owner(
        admission=admission, raw_projection_reader=raw.reads,
        storage=f.SQLiteStorageV1(path, True), utc_now=lambda: NOW,
    )
    result = owner.materialise_vintage_statuses(request())
    reader = f.create_vintage_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    history = dict(derived_signal_id="D009", subject_instrument="NVDA",
                   effective_at_or_before_utc=T, knowledge_at_or_before_utc=T, limit=10)
    if refused:
        assert ("v3", 0) in projected and ("v3", 1) in projected
        assert ("v3", 2) not in projected
        assert result is None
        assert owner.reads.list_derived_history(**history) == ()
        assert reader.list_derived_history(**history) == ()
        return
    assert type(result) is tuple and len(result) == 3
    assert tuple(v.vintage_id for v in result) == ("v1", "v2", "v3")
    assert tuple(v.result for v in result) == tuple(row[-1] for row in VINTAGES)
    assert len({v.derived_occurrence_id for v in result}) == 3
    for record, row in zip(result, VINTAGES, strict=True):
        vid, ordinal, pub, _, start, end, updated, status = row
        assert type(record) is f.VintageStatusOccurrenceV1
        assert record.request == request() and record.definition == DEFINITION
        assert record.parameter_set == PARAMETER and record.input_selection_policy == POLICY
        assert record.projection_mappings == MAPS and record.unit_conventions == UNITS
        assert record.vintage_id == vid and record.publication_ordinal == ordinal
        assert record.visible_vintage_ids == ("v1", "v2", "v3")
        assert record.publication_timestamp_utc == datetime.fromisoformat(
            pub.replace("Z", "+00:00"))
        assert record.realtime_start == date.fromisoformat(start)
        assert record.realtime_end == date.fromisoformat(end)
        assert record.last_updated_utc == datetime.fromisoformat(updated).astimezone(UTC)
        assert tuple(line.projection for line in record.raw_input_lineage) == tuple(
            projected[(vid, i)] for i in range(3))
        assert record.result == status and record.implementation_brief_sha256 == BRIEF
        assert record.units == "category" and record.result_shape == "vintage_status"
        assert (record.effective_as_of_utc, record.knowledge_cutoff_utc,
                record.calculated_at_utc) == (T, T, NOW)
        assert record.derived_occurrence_id.startswith("mmtvintage1:")
        assert reader.get_derived_occurrence(record.derived_occurrence_id) == record
    reopened = reader.list_derived_history(**history)
    assert len(reopened) == 3
    assert {v.derived_occurrence_id for v in reopened} == {
        v.derived_occurrence_id for v in result
    }
