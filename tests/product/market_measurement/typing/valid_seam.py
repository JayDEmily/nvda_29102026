"""FND-P06 lawful actual-M00 structural reader and every public return type."""

from datetime import datetime
from typing import assert_type

from nvda_desk.market_measurement_truth import api as f

from nvda_desk.raw_signal_occurrence_truth import api as raw_api


def lawful(
    admission: f.OwnerAdmissionV1,
    request: f.CalculationRequestV1,
    definition: f.CalculationDefinitionV1,
    parameters: f.CalculationParameterSetV1,
    policy: f.InputSelectionPolicyVersionV1,
    unit: f.UnitConventionVersionV1,
    mapping: raw_api.RawSignalProjectionMappingV1,
    now: datetime,
    writer: f.SQLiteStorageV1,
    reader: f.SQLiteReadStorageV1,
) -> None:
    raw = raw_api.create_owner()
    raw_reader: f.RawProjectionReaderV1 = raw.reads
    owner = f.create_owner(
        admission=admission,
        raw_projection_reader=raw_reader,
        definitions=(definition,),
        parameter_sets=(parameters,),
        input_selection_policies=(policy,),
        unit_conventions=(unit,),
        raw_projection_mappings=(mapping,),
        storage=writer,
        utc_now=lambda: now,
    )
    assert_type(owner, f.MeasurementOwnerV1)
    assert_type(owner.reads, f.MeasurementReadsV1)
    assert_type(owner.materialise(request), f.DerivedSignalOccurrenceV1 | None)
    reads = f.create_reader(admission=admission, storage=reader)
    assert_type(reads, f.MeasurementReadsV1)
    assert_type(reads.get_derived_occurrence("mmt1:unknown"), f.DerivedSignalOccurrenceV1 | None)
    assert_type(
        reads.list_derived_history(
            derived_signal_id="D011",
            subject_instrument="NVDA",
            effective_at_or_before_utc=now,
            knowledge_at_or_before_utc=now,
            limit=100,
        ),
        tuple[f.DerivedSignalOccurrenceV1, ...],
    )
    assert_type(
        reads.get_calculation_definition(
            derived_signal_id="D011", calculation_definition_version="D011-MIDPOINT-1"
        ),
        f.CalculationDefinitionV1 | None,
    )
    ref = f.VersionRefV1("mmt-pilot-basic", 1)
    assert_type(reads.get_parameter_set(ref), f.CalculationParameterSetV1 | None)
    assert_type(reads.get_input_selection_policy(ref), f.InputSelectionPolicyVersionV1 | None)
    assert_type(reads.get_unit_convention(ref), f.UnitConventionVersionV1 | None)
    assert_type(reads.get_projection_mapping(ref), raw_api.RawSignalProjectionMappingV1 | None)
    result = owner.materialise(request)
    if result is not None:
        assert_type(result.raw_input_lineage, tuple[f.RawInputLineageV1, ...])
        assert_type(result.raw_input_lineage[0].projection, raw_api.ProjectedRawValueV1)
