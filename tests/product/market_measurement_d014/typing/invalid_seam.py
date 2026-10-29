from decimal import Decimal

from nvda_desk.market_measurement_truth import api as f


def misuse(
    old: f.MeasurementReadsV1,
    predecessor: f.MeasurementRatioReadsV1,
    old_fact: f.DerivedSignalOccurrenceV1,
    predecessor_fact: f.RatioOccurrenceV1,
    reads: f.MeasurementRawRatioReadsV1,
    owner: f.MeasurementRawRatioOwnerV1,
    fact: f.RawRatioOccurrenceV1,
    request: f.CalculationRequestV1,
    admission: f.OwnerAdmissionV1,
    writer: f.SQLiteStorageV1,
) -> None:
    a: f.MeasurementRawRatioReadsV1 = old  # MISUSE[assignment]
    b: f.MeasurementRawRatioReadsV1 = predecessor  # MISUSE[assignment]
    c: f.RawRatioOccurrenceV1 = old_fact  # MISUSE[assignment]
    d: f.RawRatioOccurrenceV1 = predecessor_fact  # MISUSE[assignment]
    e: Decimal = fact.result  # MISUSE[assignment]
    reads.materialise(request)  # MISUSE[attr-defined]
    owner.materialise("D014")  # MISUSE[arg-type]
    f.create_raw_ratio_reader(admission=admission, storage=writer)  # MISUSE[arg-type]
    g: f.DerivedSignalOccurrenceV1 = fact  # MISUSE[assignment]
    h: f.RatioOccurrenceV1 = fact  # MISUSE[assignment]
    print(a, b, c, d, e, g, h)
