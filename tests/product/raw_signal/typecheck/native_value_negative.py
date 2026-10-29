from array import array
from datetime import UTC, datetime

from nvda_desk.raw_signal_occurrence_truth import api


def reject_values_outside_native_value_v1() -> None:
    bad_datetime: api.NativeValueV1 = datetime(2026, 9, 20, 12, tzinfo=UTC)  # NATIVE_NEGATIVE
    bad_complex: api.NativeValueV1 = complex(1.0, 0.0)  # NATIVE_NEGATIVE
    bad_array: api.NativeValueV1 = array("b", [1])  # NATIVE_NEGATIVE
    bad_key: api.NativeValueV1 = {1: "x"}  # NATIVE_NEGATIVE
    _ = (bad_datetime, bad_complex, bad_array, bad_key)
