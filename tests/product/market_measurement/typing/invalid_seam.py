"""Only enumerated misuse diagnostics may satisfy the negative static witness."""

from decimal import Decimal

from nvda_desk.market_measurement_truth import api as f


def misuse(
    owner: f.MeasurementOwnerV1,
    reads: f.MeasurementReadsV1,
    request: f.CalculationRequestV1,
    admission: f.OwnerAdmissionV1,
    writer: f.SQLiteStorageV1,
    reader: f.SQLiteReadStorageV1,
) -> None:
    f.VersionRefV1("x", "1")  # MISUSE[arg-type]
    f.UnitConventionVersionV1("x", 1, "price", "price", 1.0, Decimal("0"))  # MISUSE[arg-type]
    owner.materialise("D011")  # MISUSE[arg-type]
    reads.get_parameter_set("x")  # MISUSE[arg-type]
    reads.get_derived_occurrence(request)  # MISUSE[arg-type]
    reads.materialise(request)  # MISUSE[attr-defined]
    f.create_reader(admission=admission, storage=writer)  # MISUSE[arg-type]
    result: Decimal = owner.materialise(request)  # MISUSE[assignment]
    print(result)
    f.SQLiteStorageV1("/tmp/pilot.sqlite", "yes")  # MISUSE[arg-type]
    f.SQLiteReadStorageV1("/tmp/pilot.sqlite", True)  # MISUSE[call-arg]
