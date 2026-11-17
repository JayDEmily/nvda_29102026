"""D091/L04: exactly 18 owner-admitted physical product proof functions.

AUTHORING ONLY: do not run with the Worker, run through normal pytest, or
install a proof generation. Strict execution belongs to the separately
appointed Tester, at an admitted dependency window on the exact runner.

All lawful source admissions go through checked ingress into a fresh real
M00 owner that remains privately held by the controlled coordinator.
Test-only B cohorts and C/D/E faults never create a second successful
R112 source policy; no direct RecordState.append/SQL or monkeypatch counts.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import fields, replace
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from nvda_desk.raw_signal_occurrence_truth import api as raw
from nvda_desk.market_measurement_truth import api as m02
from nvda_desk.market_measurement_truth import _controlled_r112 as controlled
from nvda_desk.market_measurement_truth import _native_d091 as implementation


ROOT = Path(__file__).resolve().parents[4]
SOURCE_PATH = ROOT / "handoff/m02_completion_28_execution/L01b/CONTROLLED_BATCH_INPUTS.json"
SOURCE_SHA256 = "1f4c46c5c247c78e3e18bb2de02c172f775379f664bad8e056ef6867a39d03dc"
CONTRACT_PATH = ROOT / "handoff/m02_completion_28_execution/L01b/R112_SOURCE_CONTRACT_PROPOSED.json"
CONTRACT_SHA256 = "31c811e77468f44c2e412893326bc6d5f9ea037cdbf28712ce8e213652fdfc63"
NEGATIVE_DIR = ROOT / "handoff/m02_completion_28_execution/L04/D091_PROOF_ADMISSION_REVISION_20261116/NEGATIVE_FIXTURES"
GETTER_NEGATIVE_DIR = ROOT / "handoff/m02_completion_28_execution/L04/D091_ORIGINAL_GETTER_FAULT_PREP_20261116/NEGATIVE_FIXTURES"
SOURCE_DELIVERY_REF = "T01-R112-CLOSED-BATCH-V1"
SUBJECT = "SYNTH-NVDA-OPT-C100-20261120"
CLOCK = datetime.fromisoformat("2026-11-15T12:02:30+00:00")
IDENTITY = {
    "contract_id": "SYNTH-NVDA-OPT-C100-20261120",
    "underlying": "NVDA",
    "security_type": "OPT",
    "right": "C",
    "expiry_date": "2026-11-20",
    "strike": "100",
    "currency": "USD",
    "model_variant": "CONTROLLED_SIGNED_DELTA_V1",
    "scale": "signed_decimal_fraction",
    "generation": "T01-R112-CONTROL-G1",
    "request_id": "T01-R112-BOUNDARIES-1",
}
# Independent signed-value/category oracles from the accepted five interval law.
# All twelve points are inside ONE owner-admitted positive physical case.
EXPECTED = (
    ("0", "ABS_00_10"), ("-0.10", "ABS_10_25"), ("0.10", "ABS_10_25"),
    ("-0.25", "ABS_25_50"), ("0.25", "ABS_25_50"),
    ("-0.50", "ABS_50_75"), ("0.50", "ABS_50_75"),
    ("-0.75", "ABS_75_100"), ("0.75", "ABS_75_100"),
    ("-1.00", "ABS_75_100"), ("1.00", "ABS_75_100"),
    ("0.499", "ABS_25_50"),
)


def _load_source() -> tuple[dict, ...]:
    assert hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest() == SOURCE_SHA256
    assert hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest() == CONTRACT_SHA256
    data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    members = tuple(data["members"])
    assert len(members) == 15
    assert [x["observation"]["observation_occurrence_id"] for x in members] == [
        f"T01-R112-BATCH-{n:02d}" for n in range(15)
    ]
    assert all(x["observation"]["native_record"]["identity"] == IDENTITY for x in members)
    assert all(
        x["observation"]["native_record"]["model"]["delta"]["text"] == expected[0]
        for x, expected in zip(members[:12], EXPECTED, strict=True)
    )
    assert members[12]["observation"]["native_record"]["model"]["delta"]["text"] == "1.01"
    assert members[13]["observation"]["native_record"]["model"]["delta"]["text"] == "NaN"
    assert "delta" not in members[14]["observation"]["native_record"]["model"]
    return members


def _utc(text: str) -> datetime:
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    assert value.utcoffset() == timedelta()
    return value


def _native(value: object) -> object:
    if isinstance(value, dict):
        if set(value) == {"native_type", "text"}:
            assert value["native_type"] == "Decimal"
            return Decimal(value["text"])
        return {key: _native(subvalue) for key, subvalue in value.items()}
    if isinstance(value, list):
        return [_native(item) for item in value]
    return value


def _raw_member(member: dict, *, delivery: str = SOURCE_DELIVERY_REF) -> raw.RawObservationOccurrenceV1:
    o = member["observation"]
    return raw.RawObservationOccurrenceV1(
        concept_id=raw.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=raw.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=raw.observation_occurrence_id(o["observation_occurrence_id"]),
        delivery_artifact_ref=raw.delivery_artifact_ref(delivery),
        source_provider=raw.provider_id(o["source_provider"]),
        native_record=_native(o["native_record"]),
        received_ts_utc=_utc(o["received_ts_utc"]),
        ingestion_sequence=o["ingestion_sequence"],
        ingestion_sequence_scope=raw.ingestion_sequence_scope(o["ingestion_sequence_scope"]),
        source_temporal_kind=o["source_temporal_kind"],
        raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(s) for s in o["raw_signal_catalogue_ids"]),
        source_variant=o["source_variant"],
        subject_instrument=o["subject_instrument"],
        native_units=o["native_units"],
        source_timestamp_raw=o["source_timestamp_raw"],
        source_timezone_native=o["source_timezone_native"],
    )


def _mapping() -> raw.RawSignalProjectionMappingV1:
    return raw.RawSignalProjectionMappingV1(
        mapping_id="t01-controlled-r112-delta",
        version=1,
        raw_signal_catalogue_id=raw.RawSignalCatalogueId("R112"),
        source_provider="t01-controlled-option-delta",
        source_variant="controlled-option-model-delta/fraction-v1",
        native_field_path=("model", "delta"),
        native_units="signed_decimal_fraction",
        selection_identity_field_paths=tuple(
            (key, ("identity", key)) for key in IDENTITY
        ),
    )


def _actual_pages(reads: object, cutoff: datetime) -> tuple[tuple[raw.ProjectedRawValueV1, ...], tuple[int, ...]]:
    cursor = None
    seen: set[str] = set()
    collected: list[raw.ProjectedRawValueV1] = []
    sizes: list[int] = []
    while True:
        page = reads.list_projected_raw_history(
            raw.RawSignalCatalogueId("R112"),
            mappings=(_mapping(),),
            subject_instrument=SUBJECT,
            received_at_or_before_utc=cutoff,
            event_at_or_before_utc=None,
            limit=8,
            cursor=cursor,
        )
        assert type(page) is raw.ProjectedRawHistoryPageV1
        assert 0 < len(page.items) <= 8
        sizes.append(len(page.items))
        collected.extend(page.items)
        if page.next_cursor is None:
            break
        assert page.next_cursor not in seen
        seen.add(page.next_cursor)
        cursor = page.next_cursor
    return tuple(collected), tuple(sizes)


def _coordinator(*, negative_cohort: str | None = None) -> object:
    if negative_cohort is None:
        return controlled.create_controlled_coordinator()
    # The construction-only negative B manifest is never a successful R112
    # cohort mode available through the ordinary production factory.
    assert negative_cohort in {"B_TIE", "B_OVER64"}
    return controlled._create_negative_only_coordinator(negative_cohort)


def _admit_and_seal(members: tuple[dict, ...], *, negative_cohort: str | None = None) -> object:
    source = _coordinator(negative_cohort=negative_cohort)
    for member in members:
        observation = _raw_member(member)
        admitted = source.checked_admit(observation)
        assert type(admitted) is raw.RawObservationOccurrenceV1
        assert admitted.observation_occurrence_id == observation.observation_occurrence_id
    receipt = source.seal()
    assert receipt is not None
    reads = source.read_only_capability()
    assert not hasattr(reads, "commands")
    for member in members:
        observation_id = raw.observation_occurrence_id(member["observation"]["observation_occurrence_id"])
        real = reads.get_raw_observation_occurrence(observation_id)
        assert type(real) is raw.RawObservationOccurrenceV1
        assert real.observation_occurrence_id == observation_id
    return source


def _request(member: dict, *, as_of: datetime | None = None, cutoff: datetime | None = None) -> m02.D091BucketRequestV1:
    o = member["observation"]
    receipt = _utc(o["received_ts_utc"])
    actual_asof = receipt if as_of is None else as_of
    actual_cutoff = actual_asof if cutoff is None else cutoff
    return m02.D091BucketRequestV1(
        derived_signal_id="D091",
        subject_instrument=SUBJECT,
        as_of_utc=actual_asof,
        knowledge_cutoff_utc=actual_cutoff,
        calculation_definition_version="T01-D091-ABS-DELTA-DEF-V1",
        source_profile_ref=m02.VersionRefV1("T01-R112-CONTROLLED-FRACTION-1", 1),
        selection_policy_ref=m02.VersionRefV1("T01-R112-EXACT-RECEIPT-1", 1),
        projection_mapping_ref=m02.VersionRefV1("t01-controlled-r112-delta", 1),
        unit_convention_ref=m02.VersionRefV1("T01-R112-FRACTION-IDENTITY", 1),
        rule_profile_ref=m02.VersionRefV1("D091-SYNTHETIC-TENTATIVE-V1", 1),
        **IDENTITY,
    )


def _owner(source: object, db: Path, clock: object, observer: object) -> m02.D091BucketOwnerV1:
    return m02.create_d091_bucket_owner(
        admission=m02.OwnerAdmissionV1("M02", implementation.BRIEF),
        controlled_source_read_capability=source.read_only_capability(),
        storage=m02.SQLiteStorageV1(str(db), True),
        utc_now=clock,
        diagnostic_observer=observer,
    )


def _reader(db: Path) -> m02.D091BucketReadsV1:
    return m02.create_d091_bucket_reader(
        admission=m02.OwnerAdmissionV1("M02", implementation.BRIEF),
        storage=m02.SQLiteReadStorageV1(str(db)),
    )


def _rows(db: Path, cutoff: datetime = CLOCK) -> tuple[m02.D091BucketOccurrenceV1, ...]:
    return _reader(db).list_derived_history(
        derived_signal_id="D091",
        subject_instrument=SUBJECT,
        effective_at_or_before_utc=cutoff,
        knowledge_at_or_before_utc=cutoff,
        limit=64,
    )


def _observe(event: object, *, stage: str, target_id: str | None = None) -> None:
    assert type(event) is m02.D091DiagnosticEventV1
    assert tuple(field.name for field in fields(event)) == (
        "request_identity", "source_observation_occurrence_id", "stage",
        "source_profile_ref", "rule_profile_ref",
    )
    assert event.stage == stage
    assert type(event.request_identity) is str and event.request_identity
    assert event.source_profile_ref == m02.VersionRefV1("T01-R112-CONTROLLED-FRACTION-1", 1)
    assert event.rule_profile_ref == m02.VersionRefV1("D091-SYNTHETIC-TENTATIVE-V1", 1)
    if target_id is not None:
        assert event.source_observation_occurrence_id == target_id


def _refuses(
    source: object, member: dict, db: Path, *,
    stage: str, as_of: datetime | None = None, cutoff: datetime | None = None,
    target_id: str | None = None, clock: datetime = CLOCK,
) -> None:
    events: list[m02.D091DiagnosticEventV1] = []
    owner = _owner(source, db, lambda: clock, events.append)
    request = _request(member, as_of=as_of, cutoff=cutoff)
    assert owner.materialise(request) is None
    assert len(events) == 1
    _observe(events[0], stage=stage, target_id=target_id)
    assert events[0].request_identity == request.request_identity
    assert _rows(db) == ()


def _assert_clean_source(source: object, members: tuple[dict, ...]) -> None:
    reads = source.read_only_capability()
    for member in members:
        oid = raw.observation_occurrence_id(member["observation"]["observation_occurrence_id"])
        existing = reads.get_raw_observation_occurrence(oid)
        assert type(existing) is raw.RawObservationOccurrenceV1
        assert existing.observation_occurrence_id == oid


def _fault_fixture(name: str, source_sha256: str) -> dict:
    path = NEGATIVE_DIR / f"d091_controlled_{name}.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source_sha256
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["original_source_sha256"] == SOURCE_SHA256
    return data


class _SelectorReadAdapter:
    """Read-only C/D fault applied only AFTER genuine source read/delegation.

    This test port never has the M00 owner, command facet, source manifest
    writer or diagnostic-stage setter. It is passed ONLY as the D091 selector's
    read capability; private trusted manifest validation still uses original M00.
    """
    def __init__(self, genuine: object, fault: str) -> None:
        assert fault in {"H06", "H07", "G01", "G02", "G03"}
        self._genuine = genuine
        self._fault = fault
        self.page_calls = 0
        self.getter_calls = 0
        self.injected = 0
        self._first_page: tuple[raw.ProjectedRawValueV1, ...] = ()

    def list_projected_raw_history(self, *args: object, **kwargs: object) -> raw.ProjectedRawHistoryPageV1:
        page = self._genuine.list_projected_raw_history(*args, **kwargs)
        assert type(page) is raw.ProjectedRawHistoryPageV1
        self.page_calls += 1
        if self._fault == "H06" and self.page_calls == 1:
            self.injected += 1
            assert page.next_cursor is not None
            return replace(page, next_cursor="0")
        if self._fault == "H07" and self.page_calls == 2:
            assert self._first_page and page.items
            self.injected += 1
            contradiction = replace(self._first_page[0], native_value=Decimal("0.998"))
            return replace(page, items=(contradiction, *page.items[1:]))
        if self.page_calls == 1:
            self._first_page = page.items
        return page

    def get_raw_observation_occurrence(self, occurrence_id: object) -> raw.RawObservationOccurrenceV1 | None:
        original = self._genuine.get_raw_observation_occurrence(occurrence_id)
        self.getter_calls += 1
        if getattr(occurrence_id, "value", None) != "T01-R112-BATCH-11" or self.injected:
            return original
        if self._fault == "G01":
            assert type(original) is raw.RawObservationOccurrenceV1
            self.injected += 1
            return None
        if self._fault == "G02":
            assert type(original) is raw.RawObservationOccurrenceV1
            self.injected += 1
            return replace(original, native_units="decimal_percent")
        if self._fault == "G03":
            assert type(original) is raw.RawObservationOccurrenceV1
            self.injected += 1
            native = copy.deepcopy(dict(original.native_record))
            native["identity"]["generation"] = "T01-R112-CONTROL-G2"
            return replace(original, native_record=native)
        return original


def _faulting_owner(source: object, db: Path, adapter: _SelectorReadAdapter, events: list) -> m02.D091BucketOwnerV1:
    # Test-only wrapped *read* port: the private trusted B getter MUST remain
    # the real coordinator's own reader, not this wrapper.
    return m02.create_d091_bucket_owner(
        admission=m02.OwnerAdmissionV1("M02", implementation.BRIEF),
        controlled_source_read_capability=source.test_only_selector_capability(adapter),
        storage=m02.SQLiteStorageV1(str(db), True),
        utc_now=lambda: CLOCK,
        diagnostic_observer=events.append,
    )


def _bounded_fault_owner(source: object, db: Path, mode: str) -> m02.D091BucketOwnerV1:
    assert mode in {"D01", "D02", "D03"}
    return implementation._build_test_only_owner_from_fixed_policy(
        admission=m02.OwnerAdmissionV1("M02", implementation.BRIEF),
        controlled_source_read_capability=source.read_only_capability(),
        storage=m02.SQLiteStorageV1(str(db), True),
        utc_now=lambda: CLOCK,
        test_fault_id=mode,
    )


# The following functions, and only these functions, are the 18 admitted
# D091 physical product cases. Helpers do not create additional cases.
def test_d091_controlled_success(tmp_path: Path) -> None:
    members = _load_source()
    source = _admit_and_seal(members)
    assert not hasattr(source.read_only_capability(), "commands")
    real, pages = _actual_pages(source.read_only_capability(), _utc(members[11]["observation"]["received_ts_utc"]))
    assert pages == (8, 4) and len(real) == 12
    assert tuple(x.observation_occurrence_id.value for x in real) == tuple(
        f"T01-R112-BATCH-{n:02d}" for n in range(12)
    )
    events: list[m02.D091DiagnosticEventV1] = []
    clock = [CLOCK]
    db = tmp_path / "d091_success.sqlite3"
    owner = _owner(source, db, lambda: clock[0], events.append)
    stored = []
    for index, (signed_text, expected_label) in enumerate(EXPECTED):
        request = _request(members[index])
        outcome = owner.materialise(request)
        assert type(outcome) is m02.D091BucketOccurrenceV1
        assert type(outcome.result) is m02.D091CategoryV1
        assert type(outcome.result.label) is str and outcome.result.label == expected_label
        assert type(outcome.signed_delta) is Decimal
        assert outcome.signed_delta == Decimal(signed_text)
        assert outcome.selected_projection.native_value == Decimal(signed_text)
        assert outcome.original_observation.observation_occurrence_id.value == f"T01-R112-BATCH-{index:02d}"
        assert outcome.request == request
        assert outcome.units == "category" and outcome.result_shape == "category"
        assert outcome.definition.raw_dependencies == ("R112",)
        assert outcome.definition.derived_dependencies == ()
        assert outcome.source_contract_sha256 == CONTRACT_SHA256
        assert outcome.source_artifact_sha256 == SOURCE_SHA256
        assert outcome.calculated_at_utc == clock[0]
        assert outcome.derived_occurrence_id.startswith("d091-occurrence-v1:")
        assert outcome.cohort_content_digest
        assert _reader(db).get_derived_occurrence(outcome.derived_occurrence_id) == outcome
        stored.append(outcome)
    first = stored[11]
    clock[0] = CLOCK + timedelta(seconds=7)
    repeated = owner.materialise(_request(members[11]))
    assert repeated == first and repeated.calculated_at_utc == first.calculated_at_utc
    assert len(set(o.derived_occurrence_id for o in stored)) == 12
    assert _rows(db) == tuple(stored)
    assert events == []
    _assert_clean_source(source, members)


def test_d091_controlled_reached_refusal(tmp_path: Path) -> None:
    members = _load_source()
    source = _admit_and_seal(members)
    _refuses(source, members[12], tmp_path / "range.sqlite3", stage="RANGE", target_id="T01-R112-BATCH-12")
    _assert_clean_source(source, members)


def test_d091_controlled_seal_refusal(tmp_path: Path) -> None:
    members = _load_source()
    source = _admit_and_seal(members)
    extra = copy.deepcopy(members[0])
    extra["observation"]["observation_occurrence_id"] = "NEG-R112-POSTSEAL-16"
    candidate = _raw_member(extra, delivery="T01-R112-TEST-POSTSEAL")
    with pytest.raises(controlled.CoordinatorSealRefusal) as caught:
        source.checked_admit(candidate)
    assert caught.value.code == "COORDINATOR_POSTSEAL_INGRESS_REFUSAL"
    assert source.read_only_capability().get_raw_observation_occurrence(candidate.observation_occurrence_id) is None
    _assert_clean_source(source, members)
    events = []
    owner = _owner(source, tmp_path / "postseal.sqlite3", lambda: CLOCK, events.append)
    outcome = owner.materialise(_request(members[11]))
    assert type(outcome) is m02.D091BucketOccurrenceV1 and outcome.result.label == "ABS_25_50"
    assert events == []


def test_d091_controlled_nonfinite_refusal(tmp_path: Path) -> None:
    members = _load_source()
    source = _admit_and_seal(members)
    assert Decimal(members[13]["observation"]["native_record"]["model"]["delta"]["text"]).is_nan()
    _refuses(source, members[13], tmp_path / "nonfinite.sqlite3", stage="NONFINITE", target_id="T01-R112-BATCH-13")


def test_d091_controlled_absent_refusal(tmp_path: Path) -> None:
    members = _load_source()
    assert "delta" not in members[14]["observation"]["native_record"]["model"]
    source = _admit_and_seal(members)
    # A missing target is present as an original raw event but intentionally
    # absent from the M00 projected history; distinguish absence from no source.
    assert source.read_only_capability().get_raw_observation_occurrence(
        raw.observation_occurrence_id("T01-R112-BATCH-14")
    ) is not None
    _refuses(source, members[14], tmp_path / "absent.sqlite3", stage="ABSENT", target_id="T01-R112-BATCH-14")


def test_d091_controlled_receipt_asof_refusal(tmp_path: Path) -> None:
    stimulus = _fault_fixture("receipt_asof_refusal", "cf079a54252dd708201d09c3e76c216221bc3f7b6b07beb1914888674a37d706")
    assert stimulus["input_identity"] == "H01"
    assert stimulus["input"]["request"]["as_of_utc"] == "2026-11-15T12:00:00.500000Z"
    members = _load_source()
    source = _admit_and_seal(members)
    requested = _utc("2026-11-15T12:00:00.500000Z")
    real, sizes = _actual_pages(source.read_only_capability(), requested)
    assert sizes == (1,) and real[0].received_ts_utc < requested
    _refuses(source, members[0], tmp_path / "nonzero_age.sqlite3",
             stage="CLOCK_OR_SCOPE", as_of=requested, cutoff=requested)


def test_d091_controlled_cutoff_order_refusal(tmp_path: Path) -> None:
    stimulus = _fault_fixture("cutoff_order_refusal", "53c9a8d7c7eaf38a4544584ceea518881c49469f976a206be6f7c4010ba548b7")
    assert stimulus["input_identity"] == "H02"
    members = _load_source()
    source = _admit_and_seal(members)
    events = []
    db = tmp_path / "cutoff_order.sqlite3"
    owner = _owner(source, db, lambda: CLOCK, events.append)
    request = _request(members[0], cutoff=_utc("2026-11-15T11:59:59Z"))
    # This must reach D091 CLOCK_OR_SCOPE, rather than obtain an early generic
    # constructor failure or fabricate an ABSENT result before page reads.
    assert owner.materialise(request) is None
    assert len(events) == 1
    _observe(events[0], stage="CLOCK_OR_SCOPE")
    assert _rows(db) == ()


def test_d091_controlled_top_rank_tie_refusal(tmp_path: Path) -> None:
    fixture = _fault_fixture("top_rank_tie_refusal", "0d34b51e309db8799bd6426f1e183a80e1d9244354cda2867af2b1e7271ef0fc")
    members = tuple(fixture["input"]["members"])
    assert [m["observation"]["observation_occurrence_id"] for m in members] == ["NEG-R112-TIE-A", "NEG-R112-TIE-B"]
    source = _admit_and_seal(members, negative_cohort="B_TIE")
    actual, pages = _actual_pages(source.read_only_capability(), _utc("2026-11-15T12:00:00Z"))
    assert len(actual) == 2 and pages == (2,)
    assert actual[0].received_ts_utc == actual[1].received_ts_utc
    assert actual[0].ingestion_sequence == actual[1].ingestion_sequence
    assert actual[0].observation_occurrence_id != actual[1].observation_occurrence_id
    _refuses(source, members[0], tmp_path / "tie.sqlite3",
             stage="HISTORY_OR_AMBIGUOUS_RANK")


def test_d091_controlled_over_64_refusal(tmp_path: Path) -> None:
    fixture = _fault_fixture("over_64_refusal", "ba7129a821d9e6434be9fc5fcc454d8ebd78f043c090255f0c1c2cfde630caf7")
    members = tuple(fixture["input"]["members"])
    assert len(members) == 65
    assert [m["observation"]["observation_occurrence_id"] for m in members] == [
        f"NEG-R112-OVER64-{n:03d}" for n in range(65)
    ]
    source = _admit_and_seal(members, negative_cohort="B_OVER64")
    last = members[-1]
    observed, pages = _actual_pages(source.read_only_capability(), _utc(last["observation"]["received_ts_utc"]))
    assert pages == (8, 8, 8, 8, 8, 8, 8, 8, 1)
    assert len(observed) == 65
    _refuses(source, last, tmp_path / "over64.sqlite3",
             stage="HISTORY_OR_AMBIGUOUS_RANK", clock=CLOCK)


def test_d091_controlled_cursor_nonprogress_refusal(tmp_path: Path) -> None:
    _fault_fixture("cursor_nonprogress_refusal", "4031f4640a1373c377a623f442a0f2ec859a176ac725906c48cc6b2b1e5d2fcf")
    members = _load_source()
    source = _admit_and_seal(members)
    adapter = _SelectorReadAdapter(source.read_only_capability(), "H06")
    events = []
    db = tmp_path / "cursor.sqlite3"
    owner = _faulting_owner(source, db, adapter, events)
    assert owner.materialise(_request(members[11])) is None
    assert adapter.injected == 1 and adapter.page_calls >= 1
    assert len(events) == 1
    _observe(events[0], stage="HISTORY_OR_AMBIGUOUS_RANK")
    assert _rows(db) == ()
    _assert_clean_source(source, members)


def test_d091_controlled_duplicate_id_conflict_refusal(tmp_path: Path) -> None:
    _fault_fixture("duplicate_id_conflict_refusal", "c9fbf5aa427b87d287f05e4b5cfe2daadb50e3236d1529654fd6450db6896c98")
    members = _load_source()
    source = _admit_and_seal(members)
    adapter = _SelectorReadAdapter(source.read_only_capability(), "H07")
    events = []
    db = tmp_path / "duplicate_page.sqlite3"
    owner = _faulting_owner(source, db, adapter, events)
    assert owner.materialise(_request(members[11])) is None
    assert adapter.injected == 1 and adapter.page_calls >= 2
    assert len(events) == 1
    _observe(events[0], stage="HISTORY_OR_AMBIGUOUS_RANK")
    assert _rows(db) == ()
    _assert_clean_source(source, members)


def test_d091_controlled_precommit_sqlite_failure(tmp_path: Path) -> None:
    _fault_fixture("precommit_sqlite_failure", "0f954fc8d7a132091576cb7af92072d7eabc839c47373189658130437cc4e20b")
    members = _load_source()
    source = _admit_and_seal(members)
    db = tmp_path / "precommit.sqlite3"
    owner = _bounded_fault_owner(source, db, "D01")
    with pytest.raises(m02.PersistenceFailureV1) as caught:
        owner.materialise(_request(members[11]))
    assert caught.value.outcome_uncertain is False
    assert _rows(db) == ()
    _assert_clean_source(source, members)


def test_d091_controlled_uncertain_commit_failure(tmp_path: Path) -> None:
    _fault_fixture("uncertain_commit_failure", "15b15b769d92258731c6cd72cc6ca322a331401249d42be74443f0166cd135e3")
    members = _load_source()
    source = _admit_and_seal(members)
    db = tmp_path / "postcommit.sqlite3"
    owner = _bounded_fault_owner(source, db, "D02")
    with pytest.raises(m02.PersistenceFailureV1) as caught:
        owner.materialise(_request(members[11]))
    assert caught.value.outcome_uncertain is True
    # This tested hook is after genuine COMMIT, not an inferred rollback.
    reopened = _rows(db)
    assert len(reopened) == 1
    assert reopened[0].signed_delta == Decimal("0.499")
    assert reopened[0].result.label == "ABS_25_50"
    _assert_clean_source(source, members)


def test_d091_controlled_same_id_content_conflict(tmp_path: Path) -> None:
    _fault_fixture("same_id_content_conflict", "93154f6bf3d26c09b1b74718112016d1002ef39efcaf084c189f1b4a1af06408")
    members = _load_source()
    source = _admit_and_seal(members)
    db = tmp_path / "sameid.sqlite3"
    owner = _bounded_fault_owner(source, db, "D03")
    request = _request(members[11])
    initial = owner.materialise(request)
    assert type(initial) is m02.D091BucketOccurrenceV1
    assert initial.signed_delta == Decimal("0.499")
    assert initial.result.label == "ABS_25_50"
    first = _reader(db).get_derived_occurrence(initial.derived_occurrence_id)
    assert first == initial
    with pytest.raises(m02.PersistenceFailureV1) as caught:
        owner.materialise(request)
    assert caught.value.outcome_uncertain is False
    assert "immutable measurement identity conflict" in str(caught.value)
    assert _reader(db).get_derived_occurrence(initial.derived_occurrence_id) == first
    assert len(_rows(db)) == 1
    assert source.read_only_capability().get_raw_observation_occurrence(
        raw.observation_occurrence_id("T01-R112-BATCH-11")
    ).native_record["model"]["delta"] == Decimal("0.499")
    _assert_clean_source(source, members)


def test_d091_controlled_original_getter_missing(tmp_path: Path) -> None:
    _exercise_getter_fault(tmp_path, "G01", "original_getter_missing", "ac1b985e87cb2f4ca0dfed0fd1dc3bb4c0fac8d5794ff4831cda2014a68810b3")


def test_d091_controlled_original_getter_units_mismatch(tmp_path: Path) -> None:
    _exercise_getter_fault(tmp_path, "G02", "original_getter_units_mismatch", "a80a39c150eafb970089f40f7d8ba60c82ae43cb248abb5e472497f2edd49608")


def test_d091_controlled_original_getter_generation_mismatch(tmp_path: Path) -> None:
    _exercise_getter_fault(tmp_path, "G03", "original_getter_generation_mismatch", "e3b11ca22017e465fc63f11b102bbc6d696d2fe40436b6bc5a501e0da4078352")


def test_d091_controlled_unsealed_refusal(tmp_path: Path) -> None:
    members = _load_source()
    source = _coordinator()
    first = _raw_member(members[0])
    assert source.checked_admit(first).observation_occurrence_id == first.observation_occurrence_id
    genuine_reads = source.read_only_capability()
    page_observer = _SelectorReadAdapter(genuine_reads, "H06")
    db = tmp_path / "unsealed.sqlite3"
    events = []
    owner = _faulting_owner(source, db, page_observer, events)
    assert owner.materialise(_request(members[0])) is None
    assert page_observer.page_calls == 0 and page_observer.injected == 0
    assert len(events) == 1
    _observe(events[0], stage="UNSEALED", target_id="T01-R112-BATCH-00")
    assert _rows(db) == ()
    # Real coordinator stayed ADMITTING; the remaining exact originals can
    # still be admitted and source sealed with no unapproved member.
    for member in members[1:]:
        candidate = _raw_member(member)
        assert source.checked_admit(candidate).observation_occurrence_id == candidate.observation_occurrence_id
    assert source.seal() is not None
    _assert_clean_source(source, members)


def _exercise_getter_fault(tmp_path: Path, fault: str, fixture_name: str, fixture_sha256: str) -> None:
    assert fault in {"G01", "G02", "G03"}
    fixture_path = GETTER_NEGATIVE_DIR / f"d091_controlled_{fixture_name}.json"
    assert hashlib.sha256(fixture_path.read_bytes()).hexdigest() == fixture_sha256
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert fixture["original_fifteen_member_batch_sha256"] == SOURCE_SHA256
    assert fixture["expected_stage"] == "ORIGIN_OR_IDENTITY"
    members = _load_source()
    source = _admit_and_seal(members)
    adapter = _SelectorReadAdapter(source.read_only_capability(), fault)
    events = []
    db = tmp_path / f"{fault}.sqlite3"
    owner = _faulting_owner(source, db, adapter, events)
    assert owner.materialise(_request(members[11])) is None
    assert adapter.injected == 1
    assert adapter.page_calls >= 2 and adapter.getter_calls >= 1
    assert len(events) == 1
    _observe(events[0], stage="ORIGIN_OR_IDENTITY", target_id="T01-R112-BATCH-11")
    assert _rows(db) == ()
    # The private genuine source/getter was not altered by selector-only port.
    _assert_clean_source(source, members)

