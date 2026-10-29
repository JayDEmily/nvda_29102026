from decimal import Decimal
from typing import assert_type

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as raw


def lawful(
    owner: f.MeasurementOwnerV1,
    req: f.CalculationRequestV1,
    admission: f.OwnerAdmissionV1,
    store: f.SQLiteReadStorageV1,
) -> None:
    actual_raw: f.RawProjectionReaderV1 = raw.create_owner().reads
    assert_type(actual_raw, f.RawProjectionReaderV1)
    assert_type(owner.materialise(req), f.DerivedSignalOccurrenceV1 | None)
    result = owner.materialise(req)
    if result is not None:
        assert_type(result.result, Decimal)
    reads = f.create_reader(admission=admission, storage=store)
    assert_type(reads, f.MeasurementReadsV1)
    assert_type(reads.get_derived_occurrence("id"), f.DerivedSignalOccurrenceV1 | None)
