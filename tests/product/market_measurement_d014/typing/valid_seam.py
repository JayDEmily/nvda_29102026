from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import assert_type

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r


def lawful(
    admission: f.OwnerAdmissionV1,
    source: f.RawProjectionReaderV1,
    definitions: tuple[f.CalculationDefinitionV1, ...],
    parameters: tuple[f.CalculationParameterSetV1, ...],
    policies: tuple[f.InputSelectionPolicyVersionV1, ...],
    units: tuple[f.UnitConventionVersionV1, ...],
    mappings: tuple[r.RawSignalProjectionMappingV1, ...],
    storage: f.MemoryStorageV1 | f.SQLiteStorageV1,
    readonly: f.SQLiteReadStorageV1,
    clock: Callable[[], datetime],
    request: f.CalculationRequestV1,
    old: f.MeasurementReadsV1,
    predecessor: f.MeasurementRatioReadsV1,
) -> None:
    owner = f.create_raw_ratio_owner(
        admission=admission,
        raw_projection_reader=source,
        definitions=definitions,
        parameter_sets=parameters,
        input_selection_policies=policies,
        unit_conventions=units,
        raw_projection_mappings=mappings,
        storage=storage,
        utc_now=clock,
    )
    assert_type(owner, f.MeasurementRawRatioOwnerV1)
    assert_type(owner.reads, f.MeasurementRawRatioReadsV1)
    assert_type(owner.materialise(request), f.RawRatioOccurrenceV1 | None)
    fact = owner.materialise(request)
    if fact is not None:
        assert_type(fact.result, f.ExactRatioV1)
        assert_type(fact.raw_input_lineage, tuple[f.RawInputLineageV1, ...])
        assert_type(fact.predecessor_occurrence_ids, tuple[str, ...])
    reads = f.create_raw_ratio_reader(admission=admission, storage=readonly)
    assert_type(reads, f.MeasurementRawRatioReadsV1)
    assert_type(reads.get_derived_occurrence("id"), f.RawRatioOccurrenceV1 | None)
    assert_type(
        reads.list_derived_history(
            derived_signal_id="D014",
            subject_instrument="NVDA",
            effective_at_or_before_utc=clock(),
            knowledge_at_or_before_utc=clock(),
            limit=1,
        ),
        tuple[f.RawRatioOccurrenceV1, ...],
    )
    assert_type(
        reads.get_calculation_definition(
            derived_signal_id="D014", calculation_definition_version="v"
        ),
        f.CalculationDefinitionV1 | None,
    )
    ref = f.VersionRefV1("id", 1)
    assert_type(reads.get_parameter_set(ref), f.CalculationParameterSetV1 | None)
    assert_type(reads.get_input_selection_policy(ref), f.InputSelectionPolicyVersionV1 | None)
    assert_type(reads.get_unit_convention(ref), f.UnitConventionVersionV1 | None)
    assert_type(reads.get_projection_mapping(ref), r.RawSignalProjectionMappingV1 | None)
    previous = old.get_derived_occurrence("id")
    if previous is not None:
        assert_type(previous.result, Decimal)
    ratio = predecessor.get_derived_occurrence("id")
    if ratio is not None:
        assert_type(ratio, f.RatioOccurrenceV1)
        assert_type(ratio.predecessor_evidence, tuple[f.PredecessorEvidenceV1, ...])
