"""Two D041 cases; actual public predecessor chain and independent frozen oracle."""

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

import pytest

from nvda_desk.configured_market_conditions import api as c
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

T = datetime(2026, 10, 20, 12, 40, tzinfo=UTC)
CUTOFF, NOW = T + timedelta(seconds=1), T + timedelta(seconds=2)
BRIEF = "b9699956358b59300cac8927a3b209e4c295828084273fe7cdb6b11e3016917a"
D040_BRIEF = "ce8a16e3f5c5f886b1847ce09be321477259577560e3543b4b18853b59ad3492"
ROOT = Path(__file__).resolve().parents[3]
PROFILE = json.loads(
    (ROOT / "handoff/configured_market_conditions/authority/D041_PROFILE.json").read_text()
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


def reversion_foundation(raw, cutoff):
    admit(
        raw,
        "last-now",
        T,
        {"trade": {"last": Decimal("110")}, "session": {"id": "controlled-price-session/1"}},
        ("R037",),
        7,
    )
    samples = tuple(T - timedelta(minutes=30 - i) for i in range(31))
    for i, event in enumerate(samples):
        admit(
            raw,
            "risk-" + str(i),
            event,
            {
                "session": {"id": "controlled-risk-20261020/1"},
                "sample": {"kind": "minute_close"},
                "adjustment": {"basis": "unadjusted"},
                "bar": {"close": Decimal("110" if i == 30 else "100")},
            },
            ("R151",),
            i + 8,
        )
    context = f.RealisedRiskWindowContextV1(
        f.VersionRefV1("controlled-risk-calendar", 1),
        samples[0],
        samples[-1],
        datetime(2026, 10, 10, 12, tzinfo=UTC),
        tuple(
            f.SessionFrameV1(
                f.VersionRefV1("controlled-risk-" + day.strftime("%Y%m%d"), 1),
                "controlled_cash",
                day,
                day + timedelta(hours=1),
            )
            for day in (
                datetime(2026, 10, 10, 12, tzinfo=UTC) + timedelta(days=i) for i in range(11)
            )
        ),
        samples,
        tuple(
            f.TradingReturnIntervalV1(a, b, f.ExactRatioV1(1, 15120))
            for a, b in pairwise(samples)
        ),
    )
    specifications = (
        (
            "D026",
            "a2f3fc76cd2cc846fd4885d4f3d3df7a1a3e5c7370700a613ecb0706c853412f",
            "D026-VWAP-DEVIATION-1",
            "mmt-vwap-deviation",
            "mmt-vwap-deviation-selection",
            PRICE_CONTEXT,
            (("R037", "mmt-current-last"), ("R137", "mmt-session-provider-vwap")),
        ),
        (
            "D033",
            "302845c64e6c2b9098e7f6806b41356a269ce1e79f14c026cfb85760d70c18cd",
            "D033-REALISED-VOL-1",
            "mmt-realised-vol-30m-50d",
            "mmt-realised-vol-30m-selection",
            context,
            (("R151", "mmt-risk-close"),),
        ),
    )
    facts, readers = {}, []
    for signal, brief, definition, param, selection, context, mappings in specifications:
        owner = f.create_window_owner(
            admission=f.OwnerAdmissionV1("M02", brief),
            raw_projection_reader=raw.reads,
            storage=f.MemoryStorageV1(),
            utc_now=lambda: T + timedelta(seconds=3),
        )
        req = f.WindowCalculationRequestV1(
            f.CalculationRequestV1(
                signal,
                "NVDA",
                T,
                cutoff,
                definition,
                f.VersionRefV1(param, 1),
                f.VersionRefV1(selection, 1),
                (context.ref,),
                tuple(
                    f.RawInputBindingV1(
                        rid,
                        f.VersionRefV1(mapping, 1),
                        f.VersionRefV1("mmt-pilot-price", 1),
                        "NVDA",
                    )
                    for rid, mapping in mappings
                ),
            ),
            context,
            (),
        )
        facts[signal] = owner.materialise(req)
        assert type(facts[signal]) is f.WindowMeasurementOccurrenceV1
        readers.append(owner.reads)
    return facts, ActualReads(readers)


@pytest.mark.parametrize("refused", [False, True], ids=["success", "refusal"])
def test_d041_signal(tmp_path, refused):
    raw, base_facts, base_reads = foundation_inputs()
    d040 = c.create_owner(
        admission=f.OwnerAdmissionV1("M03", D040_BRIEF),
        predecessor_reader=base_reads,
        storage=f.MemoryStorageV1(),
        utc_now=lambda: NOW,
    )
    trend = d040.materialise(
        c.ScoreRequestV1(
            "D040",
            "NVDA",
            T,
            CUTOFF,
            "p02-d040-controlled/1",
            tuple(base_facts[s].derived_occurrence_id for s in ("D020", "D021", "D027", "D024")),
        )
    )
    assert type(trend) is c.ScoreOccurrenceV1
    cutoff = T + timedelta(seconds=2) if refused else CUTOFF
    facts, foundation_reads = reversion_foundation(raw, cutoff)
    assert trend.request.subject == "NVDA" and trend.effective_as_of_utc == T
    assert trend.knowledge_cutoff_utc == CUTOFF
    assert all(
        p.request.calculation.subject_instrument == "NVDA"
        and p.effective_as_of_utc == T
        and p.knowledge_cutoff_utc == cutoff
        for p in facts.values()
    )
    ids = (
        facts["D026"].derived_occurrence_id,
        trend.derived_occurrence_id,
        facts["D033"].derived_occurrence_id,
    )
    assert foundation_reads.get_derived_occurrence(ids[0]) == facts["D026"]
    assert d040.reads.get_derived_occurrence(ids[1]) == trend
    assert foundation_reads.get_derived_occurrence(ids[2]) == facts["D033"]
    request = c.ScoreRequestV1("D041", "NVDA", T, cutoff, "p02-d041-controlled/1", ids)
    path = str(tmp_path / "d041.sqlite")
    admission = f.OwnerAdmissionV1("M03", BRIEF)
    owner = c.create_reversion_owner(
        admission=admission,
        foundation_reader=foundation_reads,
        score_reader=d040.reads,
        storage=f.SQLiteStorageV1(path, True),
        utc_now=lambda: T + timedelta(seconds=3),
    )
    result = owner.materialise(request)
    if refused:
        assert result is None
        assert (
            owner.reads.list_derived_history(
                derived_signal_id="D041",
                subject_instrument="NVDA",
                effective_at_or_before_utc=T,
                knowledge_at_or_before_utc=cutoff,
                limit=10,
            )
            == ()
        )
        return
    assert type(result) is c.ScoreOccurrenceV1
    assert result.result == f.ExactRatioV1(
        int(
            "4673148473468275679970989035719492701134346950411865422723840889462240"
            "9173652787730180526952464323316367205523744951682968958421784836437148"
            "0216014351600975360500026694492390610103370902206892963522677"
        ),
        int(
            "1118334641222872879090856194617732223528491901424553643707563560473702"
            "6122010924120112481688441631882723511423995801669161306507972417784600"
            "99055375116915708572861408176162898213795850486628731345583764"
        ),
    )
    assert result.owner_object_id == "M03"
    assert result.owner_namespace == "configured_market_conditions/score/v1"
    assert result.implementation_brief_sha256 == BRIEF and result.derived_signal_id == "D041"
    assert result.derived_occurrence_id.startswith("cmcscore1:")
    assert result.request == request and result.profile == c.profile_from_document(PROFILE)
    import hashlib

    assert (
        result.profile_sha256
        == hashlib.sha256(
            (ROOT / "handoff/configured_market_conditions/authority/D041_PROFILE.json").read_bytes()
        ).hexdigest()
    )
    assert result.predecessors == (facts["D026"], trend, facts["D033"])
    assert result.units == "score" and result.result_shape == "exact_ratio"
    assert (result.effective_as_of_utc, result.knowledge_cutoff_utc, result.calculated_at_utc) == (
        T,
        cutoff,
        T + timedelta(seconds=3),
    )
    expected_trend = Fraction(
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
    volatility = Fraction(Decimal("2.1397082297976278396691909270830504534270372226234"))
    expected_x = (Fraction(100, 21), Fraction(100, 21), expected_trend, volatility)
    expected_z = (Fraction(100, 121), Fraction(0), expected_trend, volatility / (1 + volatility))
    assert len(result.features) == 4
    for i, evidence in enumerate(result.features):
        assert evidence.feature == result.profile.features[i]
        assert evidence.source_occurrence_id == ids[(0, 0, 1, 2)[i]]
        assert ratio(evidence.extracted) == expected_x[i]
        assert ratio(evidence.transformed) == expected_z[i]
        expected_o = expected_z[i] * (1, -1, -1, -1)[i]
        assert ratio(evidence.oriented) == expected_o
        assert ratio(evidence.weighted) == expected_o / 3
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id) == result
    reader = c.create_reversion_reader(admission=admission, storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id) == result
    assert not hasattr(reader, "materialise")
