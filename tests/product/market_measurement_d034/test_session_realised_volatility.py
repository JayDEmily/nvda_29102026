"""Exactly two D034 R151 controlled session risk cases."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
import pytest
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r

BRIEF = "a076d55d611ad35a05d5810aa01fab288af8c0fdf8e124a533b47004319796a6"
AUTHORITY = (
    ("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md", "603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c"),
    ("handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv", "67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549"),
)
D = "D034"
K = 34
STEM = "session"
SAMPLES = tuple(datetime.fromisoformat(x) for x in ('2026-10-20T12:00:00+00:00', '2026-10-20T12:01:00+00:00', '2026-10-20T12:02:00+00:00', '2026-10-20T12:03:00+00:00', '2026-10-20T12:04:00+00:00', '2026-10-20T12:05:00+00:00', '2026-10-20T12:06:00+00:00', '2026-10-20T12:07:00+00:00', '2026-10-20T12:08:00+00:00', '2026-10-20T12:09:00+00:00', '2026-10-20T12:10:00+00:00', '2026-10-20T12:11:00+00:00', '2026-10-20T12:12:00+00:00', '2026-10-20T12:13:00+00:00', '2026-10-20T12:14:00+00:00', '2026-10-20T12:15:00+00:00', '2026-10-20T12:16:00+00:00', '2026-10-20T12:17:00+00:00', '2026-10-20T12:18:00+00:00', '2026-10-20T12:19:00+00:00', '2026-10-20T12:20:00+00:00', '2026-10-20T12:21:00+00:00', '2026-10-20T12:22:00+00:00', '2026-10-20T12:23:00+00:00', '2026-10-20T12:24:00+00:00', '2026-10-20T12:25:00+00:00', '2026-10-20T12:26:00+00:00', '2026-10-20T12:27:00+00:00', '2026-10-20T12:28:00+00:00', '2026-10-20T12:29:00+00:00', '2026-10-20T12:30:00+00:00', '2026-10-20T12:31:00+00:00', '2026-10-20T12:32:00+00:00', '2026-10-20T12:33:00+00:00', '2026-10-20T12:34:00+00:00', '2026-10-20T12:35:00+00:00', '2026-10-20T12:36:00+00:00', '2026-10-20T12:37:00+00:00', '2026-10-20T12:38:00+00:00', '2026-10-20T12:39:00+00:00', '2026-10-20T12:40:00+00:00', '2026-10-20T12:41:00+00:00', '2026-10-20T12:42:00+00:00', '2026-10-20T12:43:00+00:00', '2026-10-20T12:44:00+00:00', '2026-10-20T12:45:00+00:00', '2026-10-20T12:46:00+00:00', '2026-10-20T12:47:00+00:00', '2026-10-20T12:48:00+00:00', '2026-10-20T12:49:00+00:00', '2026-10-20T12:50:00+00:00', '2026-10-20T12:51:00+00:00', '2026-10-20T12:52:00+00:00', '2026-10-20T12:53:00+00:00', '2026-10-20T12:54:00+00:00', '2026-10-20T12:55:00+00:00', '2026-10-20T12:56:00+00:00', '2026-10-20T12:57:00+00:00', '2026-10-20T12:58:00+00:00', '2026-10-20T12:59:00+00:00', '2026-10-20T13:00:00+00:00'))
T = SAMPLES[-1]
CUTOFF = T + timedelta(minutes=2)
NOW = CUTOFF + timedelta(seconds=1)
SESSIONS = tuple(
    f.SessionFrameV1(
        f.VersionRefV1("controlled-risk-" + (datetime(2026, 10, 10, 12, tzinfo=UTC)+timedelta(days=i)).strftime("%Y%m%d"),1),
        "controlled_cash",
        datetime(2026, 10, 10, 12, tzinfo=UTC)+timedelta(days=i),
        datetime(2026, 10, 10, 13, tzinfo=UTC)+timedelta(days=i),
    ) for i in range(11)
)
MAPPING = r.RawSignalProjectionMappingV1(
    "mmt-risk-close",1,r.RawSignalCatalogueId("R151"),"foundation-pilot-fixture","cash_quote_v1",
    ("bar","close"),"price",
    (("session.id",("session","id")),("sample.kind",("sample","kind")),("adjustment.basis",("adjustment","basis"))),
)
UNIT = f.UnitConventionVersionV1("mmt-pilot-price",1,"price","price",Decimal("1"),Decimal("0"))
POLICY = f.InputSelectionPolicyVersionV1(
    "mmt-realised-vol-"+STEM+"-selection",1,("subject_instrument","session"),
    timedelta(days=30),timedelta(0),("true_instant",),(),"foundation-pilot-fixture","cash_quote_v1",
    "foundation-pilot-fixture/cash_quote_v1",100,1000,
)
PARAMETER = f.CalculationParameterSetV1("mmt-realised-vol-"+STEM+"-50d",1,"P_VOL_WINDOW","NVDA",("NVDA",))
DEFINITION = f.CalculationDefinitionV1(
    D,D+"-REALISED-VOL-1","K05_REALIZED_RISK",
    "sqrt(sum(ln(close_i/close_(i-1))^2)/sum(trading_year_fraction_i))",("R151",),(),
    "P_VOL_WINDOW","annualised_volatility","scalar_decimal",
    tuple(f.AuthorityArtifactRefV1(*ref) for ref in AUTHORITY),
)
FRAC = f.ExactRatioV1(1,15120) if K <= 34 else f.ExactRatioV1(1,252)
INTERVALS = tuple(f.TradingReturnIntervalV1(a,b,FRAC) for a,b in zip(SAMPLES,SAMPLES[1:]))
CONTEXT = f.RealisedRiskWindowContextV1(
    f.VersionRefV1("controlled-risk-calendar",1),SAMPLES[0],SAMPLES[-1],SESSIONS[0].start_utc,
    SESSIONS,SAMPLES,INTERVALS,
)

def _kind(event):
    return "official_close" if event.hour == 13 else "session_open" if event.hour == 12 and event.minute == 0 else "minute_close"

def _admit(raw,identity,event,value,seq):
    native={"session":{"id":"controlled-risk-"+event.strftime("%Y%m%d")+"/1"},
            "sample":{"kind":_kind(event)},"adjustment":{"basis":"unadjusted"},
            "bar":{"close":Decimal(value)}}
    raw.commands.admit_raw_observation_occurrence(r.RawObservationOccurrenceV1(
        concept_id=r.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=r.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=r.observation_occurrence_id(identity),
        delivery_artifact_ref=r.delivery_artifact_ref("controlled-delivery"),
        source_provider=r.provider_id("foundation-pilot-fixture"),native_record=native,
        received_ts_utc=event,ingestion_sequence=seq,
        ingestion_sequence_scope=r.ingestion_sequence_scope("foundation-pilot-fixture/cash_quote_v1"),
        source_temporal_kind="true_instant",raw_signal_catalogue_ids=(r.RawSignalCatalogueId("R151"),),
        source_variant="cash_quote_v1",subject_instrument="NVDA",native_units="price",
        source_timestamp_raw=event.isoformat().replace("+00:00","Z"),source_timezone_native="UTC",
    ))

def _page(raw,cutoff,asof):
    page=raw.reads.list_projected_raw_history(
        r.RawSignalCatalogueId("R151"),mappings=(MAPPING,),subject_instrument="NVDA",
        received_at_or_before_utc=cutoff,event_at_or_before_utc=asof,limit=100,cursor=None,
    )
    assert page.next_cursor is None
    return page.items

@pytest.mark.parametrize("refused",[False,True])
def test_d034_session_realised_volatility(tmp_path,refused):
    raw=r.create_owner()
    missing=((len(SAMPLES)-1,))
    for i,event in enumerate(SAMPLES):
        if refused and i in missing:
            continue
        _admit(raw,"sample-"+str(i),event,"110" if i==len(SAMPLES)-1 else "100",i+1)
    if refused and K == 32:
        _admit(raw,"off-grid",datetime(2026,10,20,12,37,30,tzinfo=UTC),"999",999)
    if refused and K == 34:
        late=datetime(2026,10,20,13,1,tzinfo=UTC)
        _admit(raw,"after-close",late,"110",999)
        assert any(x.observation_occurrence_id.value == "after-close" for x in _page(raw,CUTOFF,late))
    if refused and K == 35:
        _admit(raw,"older",datetime(2026,10,14,13,tzinfo=UTC),"100",999)
    projected=_page(raw,CUTOFF,T)
    assert len(projected)==len(SAMPLES)-len(missing if refused else ()) + int(refused and K in (32,35))
    admission=f.OwnerAdmissionV1("M02",BRIEF)
    path=str(tmp_path/"m02.sqlite")
    try:
        owner=f.create_window_owner(admission=admission,raw_projection_reader=raw.reads,
                  storage=f.SQLiteStorageV1(path,True),utc_now=lambda:NOW)
    except ValueError as exc:
        pytest.fail(f"admitted {D} unsupported after lawful public R151 setup: {exc}")
    request=f.WindowCalculationRequestV1(
        f.CalculationRequestV1(D,"NVDA",T,CUTOFF,DEFINITION.calculation_definition_version,
            f.VersionRefV1(PARAMETER.context_id,1),f.VersionRefV1(POLICY.context_id,1),(CONTEXT.ref,),
            (f.RawInputBindingV1("R151",f.VersionRefV1(MAPPING.mapping_id,1),f.VersionRefV1(UNIT.context_id,1),"NVDA"),)),
        CONTEXT,(),
    )
    result=owner.materialise(request)
    if refused:
        assert result is None
        assert owner.reads.list_derived_history(
            derived_signal_id=D,subject_instrument="NVDA",effective_at_or_before_utc=T,
            knowledge_at_or_before_utc=CUTOFF,limit=10)==()
        return
    assert type(result) is f.WindowMeasurementOccurrenceV1
    expected=Decimal("1.5130021990505661763533261763515839450637636850162")
    assert type(result.result) is Decimal and result.result.as_tuple()==expected.as_tuple()
    assert result.owner_object_id=="M02" and result.owner_namespace=="neutral_market_measurement_truth/window/v1"
    assert result.implementation_brief_sha256==BRIEF and result.derived_signal_id==D
    assert result.derived_occurrence_id.startswith("mmtwindow1:")
    assert result.request==request and result.definition==DEFINITION
    assert result.parameter_set==PARAMETER and result.input_selection_policy==POLICY
    assert result.unit_conventions==(UNIT,) and result.projection_mappings==(MAPPING,)
    by_id={p.observation_occurrence_id.value:p for p in projected}
    lines=tuple(f.RawInputLineageV1("R151","sample-"+str(i),
            f.VersionRefV1(MAPPING.mapping_id,1),f.VersionRefV1(UNIT.context_id,1),
            by_id["sample-"+str(i)],by_id["sample-"+str(i)].native_value,event)
            for i,event in enumerate(SAMPLES))
    assert result.raw_input_lineage==lines and result.predecessors==()
    assert result.window_seconds==3600 and result.units=="annualised_volatility"
    assert result.result_shape=="scalar_decimal"
    assert result.effective_as_of_utc==T and result.knowledge_cutoff_utc==CUTOFF
    assert result.calculated_at_utc==NOW
    assert owner.reads.get_derived_occurrence(result.derived_occurrence_id)==result
    reader=f.create_window_reader(admission=admission,storage=f.SQLiteReadStorageV1(path))
    assert reader.get_derived_occurrence(result.derived_occurrence_id)==result
