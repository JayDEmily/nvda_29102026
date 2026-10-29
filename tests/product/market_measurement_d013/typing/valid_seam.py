from collections.abc import Callable
from datetime import datetime
from decimal import Decimal
from typing import assert_type

from nvda_desk.market_measurement_truth import api as f


def lawful(
    old: f.MeasurementOwnerV1,
    old_request: f.CalculationRequestV1,
    request: f.RatioCalculationRequestV1,
    admission: f.OwnerAdmissionV1,
    storage: f.SQLiteStorageV1,
    readonly: f.SQLiteReadStorageV1,
    definitions: tuple[f.CalculationDefinitionV1, ...],
    parameters: tuple[f.CalculationParameterSetV1, ...],
    clock: Callable[[], datetime],
) -> None:
    owner = f.create_ratio_owner(
        admission=admission,
        predecessor_reader=old.reads,
        definitions=definitions,
        parameter_sets=parameters,
        storage=storage,
        utc_now=clock,
    )
    assert_type(owner, f.MeasurementRatioOwnerV1)
    assert_type(owner.reads, f.MeasurementRatioReadsV1)
    assert_type(owner.materialise(request), f.RatioOccurrenceV1 | None)
    result = owner.materialise(request)
    if result is not None:
        assert_type(result.result, f.ExactRatioV1)
        assert_type(result.result.numerator, int)
        assert_type(result.predecessor_evidence, tuple[f.PredecessorEvidenceV1, ...])
        assert_type(result.predecessor_evidence[0].occurrence, f.DerivedSignalOccurrenceV1)
    reads = f.create_ratio_reader(admission=admission, storage=readonly)
    assert_type(reads, f.MeasurementRatioReadsV1)
    assert_type(reads.get_derived_occurrence("id"), f.RatioOccurrenceV1 | None)
    previous = old.materialise(old_request)
    if previous is not None:
        assert_type(previous.result, Decimal)
    assert_type(f.create_reader(admission=admission, storage=readonly), f.MeasurementReadsV1)
