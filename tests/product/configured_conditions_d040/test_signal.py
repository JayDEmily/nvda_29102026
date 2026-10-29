"""Two D040 cases; actual public predecessors, independent frozen oracle."""

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from nvda_desk.configured_market_conditions import api as c
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
BRIEF = "ce8a16e3f5c5f886b1847ce09be321477259577560e3543b4b18853b59ad3492"
ROOT = Path(__file__).resolve().parents[3]
PROFILE = json.loads(
    (ROOT / "handoff/configured_market_conditions/authority/D040_PROFILE.json").read_text()
)
CLOSE_CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-close-session", 1),
    T.replace(minute=0),
    T.replace(hour=13, minute=0),
    T.replace(minute=0),
)
PRICE_CONTEXT = f.WindowContextV1(
    f.VersionRefV1("controlled-price-session", 1),
    T.replace(minute=0),
    T.replace(hour=13, minute=0),
    T.replace(minute=0),
)
LOGS = (
    ("D019", 60, "6affd5b55eb03007a23ae80a79bbd3d5665105d70b2e7e65c4050d29cf60c085"),
    ("D020", 300, "811906fdfb073da9b5a7ba137563953d6ff977d50bfe99b8f43adb068f20e839"),
    ("D021", 1800, "913ba660f583f8f3e564190390681e594a374e0fc2d66227bd8452b4d0cbb8cc"),
)


class ActualReads:
    def __init__(self, readers):
        self.readers = readers

    def get_derived_occurrence(self, identity):
        found = [p for rd in self.readers if (p := rd.get_derived_occurrence(identity)) is not None]
        assert len(found) <= 1
        return found[0] if found else None

    def list_derived_history(self, **kwargs):
        return tuple(p for rd in self.readers for p in rd.list_derived_history(**kwargs))


def admit(raw, identity, event, native, tags, sequence):
    raw.commands.admit_raw_observation_occurrence(
        r.RawObservationOccurrenceV1(
            concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
            contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
            observation_occurrence_id=r.observation_occurrence_id(identity),
            delivery_artifact_ref=r.delivery_artifact_ref("controlled-score-delivery"),
            source_provider=r.provider_id("foundation-pilot-fixture"),
            native_record=native,
            received_ts_utc=event,
            ingestion_sequence=sequence,
            ingestion_sequence_scope=r.ingestion_sequence_scope(
                "foundation-pilot-fixture/cash_quote_v1"
            ),
            source_temporal_kind="true_instant",
            raw_signal_catalogue_ids=tuple(r.RawSignalCatalogueId(t) for t in tags),
            source_variant="cash_quote_v1",
            subject_instrument="NVDA",
            native_units="price",
            source_timestamp_raw=event.isoformat().replace("+00:00", "Z"),
            source_timezone_native="UTC",
        )
    )


def foundation_inputs(cutoff=CUTOFF):
    raw = r.create_owner()
    for seq, (name, age, price) in enumerate(
        (("current", 0, "110"), ("one", 60, "120"), ("five", 300, "100"), ("thirty", 1800, "121")),
        1,
    ):
        admit(
            raw,
            name,
            T - timedelta(seconds=age),
            {"bar": {"close": Decimal(price)}},
            ("R143",),
            seq,
        )
    for seq, (name, age, price) in enumerate((("vwap-now", 0, "105"), ("vwap-ref", 300, "100")), 5):
        event = T - timedelta(seconds=age)
        admit(
            raw,
            name,
            event,
            {
                "vwap": {
                    "value": Decimal(price),
                    "session": "controlled-price-session/1",
                    "as_of": event.isoformat().replace("+00:00", "Z"),
                    "basis": "cumulative_session",
                }
            },
            ("R137",),
            seq,
        )
    readers, facts = [], {}
    for signal, seconds, brief in LOGS:
        owner = f.create_window_owner(
            admission=f.OwnerAdmissionV1("M02", brief),
            raw_projection_reader=raw.reads,
            storage=f.MemoryStorageV1(),
            utc_now=lambda: NOW,
        )
        request = f.WindowCalculationRequestV1(
            f.CalculationRequestV1(
                signal,
                "NVDA",
                T,
                cutoff,
                signal + "-LOG-RETURN-1",
                f.VersionRefV1(f"mmt-log-{seconds}s-50d-half-even", 1),
                f.VersionRefV1("mmt-close-selection", 1),
                (CLOSE_CONTEXT.ref,),
                (
                    f.RawInputBindingV1(
                        "R143",
                        f.VersionRefV1("mmt-bar-close", 1),
                        f.VersionRefV1("mmt-pilot-price", 1),
                        "NVDA",
                    ),
                ),
            ),
            CLOSE_CONTEXT,
            (),
        )
        fact = owner.materialise(request)
        assert type(fact) is f.WindowMeasurementOccurrenceV1
        facts[signal] = fact
        readers.append(owner.reads)
    owner = f.create_window_owner(
        admission=f.OwnerAdmissionV1(
            "M02", "7776047c140ed8e6fa76af66a772b4a8ffbf1088ce4681377243ec666ddc9885"
        ),
        raw_projection_reader=raw.reads,
        predecessor_reader=ActualReads(readers),
        storage=f.MemoryStorageV1(),
        utc_now=lambda: NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D024",
            "NVDA",
            T,
            cutoff,
            "D024-RETURN-ACCELERATION-1",
            f.VersionRefV1("mmt-return-acceleration", 1),
            f.VersionRefV1("mmt-return-acceleration-selection", 1),
            (CLOSE_CONTEXT.ref,),
            (),
        ),
        CLOSE_CONTEXT,
        tuple(facts[s].derived_occurrence_id for s in ("D019", "D020", "D021")),
    )
    facts["D024"] = owner.materialise(request)
    assert type(facts["D024"]) is f.WindowMeasurementOccurrenceV1
    readers.append(owner.reads)
    owner = f.create_window_owner(
        admission=f.OwnerAdmissionV1(
            "M02", "6c4a8b6a4451ddfa6b555e9f1b02d659af269ec0788e8ebc15b8ddf9528796bf"
        ),
        raw_projection_reader=raw.reads,
        storage=f.MemoryStorageV1(),
        utc_now=lambda: NOW,
    )
    request = f.WindowCalculationRequestV1(
        f.CalculationRequestV1(
            "D027",
            "NVDA",
            T,
            cutoff,
            "D027-VWAP-RATE-1",
            f.VersionRefV1("mmt-vwap-rate-300s", 1),
            f.VersionRefV1("mmt-vwap-rate-300s-selection", 1),
            (PRICE_CONTEXT.ref,),
            (
                f.RawInputBindingV1(
                    "R137",
                    f.VersionRefV1("mmt-session-provider-vwap", 1),
                    f.VersionRefV1("mmt-pilot-price", 1),
                    "NVDA",
                ),
            ),
        ),
        PRICE_CONTEXT,
        (),
    )
    facts["D027"] = owner.materialise(request)
    assert type(facts["D027"]) is f.WindowMeasurementOccurrenceV1
    readers.append(owner.reads)
    return raw, facts, ActualReads(readers)


def ratio(value):
    return Fraction(value.numerator, value.denominator)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d040_signal(tmp_path, refused):
    _, facts, reads = foundation_inputs()
    order = ("D020", "D021", "D024", "D027") if refused else ("D020", "D021", "D027", "D024")
    ids = tuple(facts[s].derived_occurrence_id for s in order)
    # Four distinct real facts exist: failure cannot be explained by absence or duplicate IDs.
    assert len(set(ids)) == 4
    assert tuple(reads.get_derived_occurrence(i).derived_signal_id for i in ids) == order
    path = str(tmp_path / "d040.sqlite")
    admission = f.OwnerAdmissionV1("M03", BRIEF)
    owner = c.create_owner(
        admission=admission,
        predecessor_reader=reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: NOW,
    )
    request = c.ScoreRequestV1("D040", "NVDA", T, CUTOFF, "p02-d040-controlled/1", ids)
    result = owner.materialise(request)
    if refused:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D040",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=CUTOFF,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is c.ScoreOccurrenceV1
    assert result.result == f.ExactRatioV1(
        int(
            "5772535406656219261377912607991856373340241174391084767687360450426598"
            "2574657574371065080413793694406792368312828379689158570514484658370511"
            "35869377659"
        ),
        int(
            "6476193208071994787373802516837355775889104075051380024192619923330082"
            "8666317862118447541509938084941522423389870900147045979131100580658197"
            "66936107372"
        ),
    )
    assert result.owner_object_id == "M03"
    assert result.owner_namespace == "configured_market_conditions/score/v1"
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D040"
    assert result.derived_occurrence_id.startswith("cmcscore1:")
    assert result.request == request and result.profile == c.profile_from_document(PROFILE)
    import hashlib

    assert (
        result.profile_sha256
        == hashlib.sha256(
            (ROOT / "handoff/configured_market_conditions/authority/D040_PROFILE.json").read_bytes()
        ).hexdigest()
    )
    assert result.predecessors == tuple(facts[s] for s in order)
    assert result.units == "score" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        CUTOFF,
        NOW,
    )
    assert len(result.features) == 8
    # Independent exact predecessor literals, not values obtained from the product.
    a = Fraction(Decimal("-0.087011376989629766167765901873749540976783972605843"))
    b = Fraction(Decimal("0.095310179804324860043952123280765092220605365308644"))
    values = (b, -b, Fraction(1), a - b / 5)
    for i, evidence in enumerate(result.features):
        feature = result.profile.features[i]
        x = values[i // 2]
        scale = ratio(feature.scale)
        transformed = x / (scale + abs(x))
        clipped = min(max(transformed, Fraction(feature.clip[0])), Fraction(feature.clip[1]))
        oriented = clipped * feature.orientation
        assert evidence.feature == feature
        assert evidence.source_occurrence_id == ids[i // 2]
        assert ratio(evidence.extracted) == x and ratio(evidence.transformed) == clipped
        assert ratio(evidence.oriented) == oriented
        assert ratio(evidence.weighted) == oriented / 4
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = c.create_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert not hasattr(reader, "materialise")
