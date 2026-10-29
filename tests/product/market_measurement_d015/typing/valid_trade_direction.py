"""Positive consumer for the one additive D015 public shape."""

from nvda_desk.market_measurement_truth.api import (
    MeasurementTradeDirectionOwnerV1,
    MeasurementTradeDirectionReadsV1,
    TradeDirectionOccurrenceV1,
    TradeDirectionRequestV1,
)


def consume(
    owner: MeasurementTradeDirectionOwnerV1,
    reader: MeasurementTradeDirectionReadsV1,
    request: TradeDirectionRequestV1,
) -> tuple[TradeDirectionOccurrenceV1 | None, TradeDirectionOccurrenceV1 | None]:
    produced = owner.materialise(request)
    recovered = (
        None if produced is None else reader.get_derived_occurrence(produced.derived_occurrence_id)
    )
    return produced, recovered
