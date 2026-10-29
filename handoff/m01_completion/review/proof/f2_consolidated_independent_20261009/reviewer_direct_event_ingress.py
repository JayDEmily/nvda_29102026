"""Independent public-seam sequence that admits an event *after* first calculation."""

import importlib.util
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from nvda_desk.raw_signal_occurrence_truth import api as raw

SRC = str(
    Path(__file__).resolve().parents[5]
    / "tests/product/derived_signal/test_m01_f2b_event_public.py"
)
spec = importlib.util.spec_from_file_location("worker_test_helpers", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
NOW = mod.NOW
owner, request, m00 = mod._fixture(mod._base())
first = owner.materialise(request)
assert first is not None and first.result is True, ("initial", first)


# Real sequential admission through M00 public commands, not fixture preload.
def add_record(rid: str, event_id: str, suffix: str, value, seconds: int, seq: int):
    provider = "controlled-a"
    variant = "event-calendar"
    item = raw.RawObservationOccurrenceV1(
        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw.observation_occurrence_id(suffix),
        delivery_artifact_ref=raw.delivery_artifact_ref("deliver-" + suffix),
        source_provider=raw.provider_id(provider),
        native_record={
            "event": {
                "id": event_id,
                "scheduled": value if rid == "R284" else NOW.isoformat(),
                "importance": value if rid == "R289" else Decimal("0"),
            }
        },
        received_ts_utc=NOW + timedelta(seconds=seconds),
        ingestion_sequence=seq,
        ingestion_sequence_scope=raw.ingestion_sequence_scope(provider + ":" + variant),
        source_temporal_kind="receipt_only",
        raw_signal_catalogue_ids=(raw.RawSignalCatalogueId(rid),),
        source_variant=variant,
        subject_instrument="NVDA",
        native_units="native_event",
        revision_vintage_native="v" + str(seq),
    )
    m00.commands.admit_raw_observation_occurrence(item)


add_record("R289", "macro-A", "review-importance-a-2", Decimal("0.2"), 10, 3)
req2 = replace(
    request, knowledge_cutoff_utc=NOW + timedelta(seconds=15), as_of_utc=NOW + timedelta(seconds=15)
)
second = owner.materialise(req2)
assert second is not None and second.result is False, ("importance revision", second)
assert {
    r.observation_occurrence_id for r in second.raw_input_lineage if r.raw_signal_id == "R289"
} == {"review-importance-a-2"}
assert owner.materialise(request) == first

# A second competing event arrives later, nearer to decision instant, with no
# corresponding importance. M01 must refuse, not reuse A's importance.
add_record(
    "R284", "macro-B", "review-schedule-b-1", (NOW + timedelta(seconds=25)).isoformat(), 20, 4
)
req3 = replace(
    request, knowledge_cutoff_utc=NOW + timedelta(seconds=25), as_of_utc=NOW + timedelta(seconds=25)
)
third = owner.materialise(req3)
assert third is None, ("must not borrow importance across events", third)
print(
    "REVIEWER_DIRECT_SEQUENCE_OK: initial=True; importance revision=False; "
    "competing unscored event=None; original immutable=True"
)
