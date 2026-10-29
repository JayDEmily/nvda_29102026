from decimal import Decimal

from nvda_desk.market_measurement_truth import api as f


def misuse(
    owner: f.MeasurementOwnerV1,
    reads: f.MeasurementReadsV1,
    request: f.CalculationRequestV1,
    admission: f.OwnerAdmissionV1,
    writer: f.SQLiteStorageV1,
) -> None:
    owner.materialise("D012")  # MISUSE[arg-type]
    result: Decimal = owner.materialise(request)  # MISUSE[assignment]
    reads.materialise(request)  # MISUSE[attr-defined]
    f.create_reader(admission=admission, storage=writer)  # MISUSE[arg-type]
    print(result)
