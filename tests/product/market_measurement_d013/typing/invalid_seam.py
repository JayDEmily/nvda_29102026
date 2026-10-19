from decimal import Decimal

from nvda_desk.market_measurement_truth import api as f


def misuse(
    old: f.MeasurementReadsV1,
    old_result: f.DerivedSignalOccurrenceV1,
    owner: f.MeasurementRatioOwnerV1,
    reads: f.MeasurementRatioReadsV1,
    request: f.RatioCalculationRequestV1,
    result: f.RatioOccurrenceV1,
    admission: f.OwnerAdmissionV1,
    writer: f.SQLiteStorageV1,
) -> None:
    ratio_reads: f.MeasurementRatioReadsV1 = old  # MISUSE[assignment]
    ratio_result: f.RatioOccurrenceV1 = old_result  # MISUSE[assignment]
    decimal: Decimal = result.result  # MISUSE[assignment]
    reads.materialise(request)  # MISUSE[attr-defined]
    owner.materialise("D013")  # MISUSE[arg-type]
    f.create_ratio_reader(admission=admission, storage=writer)  # MISUSE[arg-type]
    original: f.DerivedSignalOccurrenceV1 = result  # MISUSE[assignment]
    print(ratio_reads, ratio_result, decimal, original)
