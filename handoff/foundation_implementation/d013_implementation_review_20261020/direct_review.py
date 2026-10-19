"""Independent literal-only public sequencing; no Worker test/support imports."""
from datetime import UTC, datetime, timedelta
from decimal import Decimal, localcontext, Inexact, Rounded
from dataclasses import replace
from pathlib import Path
import subprocess
import sys
import pickle
import hashlib
import sqlite3

from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence

BASE=Path(__file__).parent
T=datetime(2026,10,16,1,tzinfo=UTC)
OLD='a31c482d2dc4822539ede99e955761319585af4badea93b9fc279638e1e1f393'
NEW='1f53d9c21c6eb4b90213137c4699a0688f994cd0ed55e54082268d8477abc148'
AUTH=(f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CALCULATION_TRUTH_INPUT_BRIEF.md','603b850802a418780109095e7ae69bcece449da79fb24140a6d50297605e927c'),f.AuthorityArtifactRefV1('handoff/m01_completion/authority/NVDA_DERIVED_SIGNAL_CATALOGUE.csv','67bacbcf77afa766cec220a8d4a0f9589c9568d4a1f5c5818334915adf72e549'))
PARAMS=tuple(f.CalculationParameterSetV1('mmt-pilot-basic',v,'P_BASIC','NVDA',('NVDA',)) for v in (1,2))
DEFS=tuple(f.CalculationDefinitionV1(d,f'{d}-{label}-{v}','K02_ALGEBRA',eq,('R034','R035'),(),'P_BASIC','price','scalar_decimal',AUTH) for d,label,eq in (('D011','MIDPOINT','(R034 + R035) / 2'),('D012','SPREAD','R035 - R034')) for v in (1,2))
RDEFS=tuple(f.CalculationDefinitionV1('D013',f'D013-RELATIVE-SPREAD-{v}','K02_ALGEBRA','100 * D012 / D011',(),('D011','D012'),'P_BASIC','percent','scalar_exact_ratio',AUTH) for v in (1,2))
MAPS=tuple(r.RawSignalProjectionMappingV1('mmt-pilot-'+side,v,r.RawSignalCatalogueId(rid),'foundation-pilot-fixture','cash_quote_v1',('quote',side),'price',()) for v in (1,2) for side,rid in (('bid','R034'),('ask','R035')))
POLICIES=tuple(f.InputSelectionPolicyVersionV1('mmt-pilot-selection',v,('subject_instrument',),timedelta(seconds=60),timedelta(seconds=10),('true_instant',),(),'foundation-pilot-fixture','cash_quote_v1','foundation-pilot-fixture/cash_quote_v1',100,1000) for v in (1,2))
UNITS=tuple(f.UnitConventionVersionV1('mmt-pilot-price',v,'price','price',Decimal('1'),Decimal('0')) for v in (1,2))

def old_request(d, *, definition=1, parameter=1, selection=1, unit=1, mapping=1, cutoff=T):
    return f.CalculationRequestV1(d,'NVDA',T,cutoff,f'{d}-'+('MIDPOINT' if d=='D011' else 'SPREAD')+f'-{definition}',f.VersionRefV1('mmt-pilot-basic',parameter),f.VersionRefV1('mmt-pilot-selection',selection),(),tuple(f.RawInputBindingV1(rid,f.VersionRefV1('mmt-pilot-'+side,mapping),f.VersionRefV1('mmt-pilot-price',unit),'NVDA') for rid,side in (('R034','bid'),('R035','ask'))))

def history(reader):
    return reader.list_derived_history(derived_signal_id='D013',subject_instrument='NVDA',effective_at_or_before_utc=T+timedelta(days=1),knowledge_at_or_before_utc=T+timedelta(days=1),limit=1000)

def ratio_request(a,b,**kw):
    return f.RatioCalculationRequestV1('D013','NVDA',T,T,kw.get('definition','D013-RELATIVE-SPREAD-1'),f.VersionRefV1('mmt-pilot-basic',kw.get('parameter',1)),(a.derived_occurrence_id,b.derived_occurrence_id))

def writer():
    root=BASE/'stores'; root.mkdir()
    raw=r.create_owner(durability_port=create_sqlite_persistence(str(root/'raw.sqlite'),create=True))
    clock=[T+timedelta(seconds=1)]
    previous=f.create_owner(admission=f.OwnerAdmissionV1('M02',OLD),raw_projection_reader=raw.reads,definitions=DEFS,parameter_sets=PARAMS,input_selection_policies=POLICIES,unit_conventions=UNITS,raw_projection_mappings=MAPS,storage=f.SQLiteStorageV1(str(root/'old.sqlite'),True),utc_now=lambda:clock[0])
    class Reader:
        mode=None
        def __getattr__(self,name): return getattr(previous.reads,name)
        def get_derived_occurrence(self,identity):
            item=previous.reads.get_derived_occurrence(identity)
            if item is None or item.derived_signal_id!='D011': return item
            if self.mode=='representation': return replace(item,result=Decimal('101.0'))
            if self.mode=='wrong-result': return replace(item,result=Decimal('999'))
            if self.mode=='hash': return replace(item,definition_content_sha256='0'*64)
            return item
        def get_unit_convention(self,ref):
            value=previous.reads.get_unit_convention(ref)
            return replace(value,scale=Decimal('1.0')) if self.mode=='configuration' else value
    reader=Reader()
    ratio=f.create_ratio_owner(admission=f.OwnerAdmissionV1('M02',NEW),predecessor_reader=reader,definitions=RDEFS,parameter_sets=PARAMS,storage=f.SQLiteStorageV1(str(root/'ratio.sqlite'),True),utc_now=lambda:clock[0])
    missing=f.RatioCalculationRequestV1('D013','NVDA',T,T,'D013-RELATIVE-SPREAD-1',f.VersionRefV1('mmt-pilot-basic',1),('not-yet-midpoint','not-yet-spread'))
    assert previous.materialise(old_request('D011')) is None
    assert ratio.materialise(missing) is None and history(ratio.reads)==()
    for side,rid,value,event,receipt,seq in (('bid','R034','100',T-timedelta(seconds=2),T-timedelta(seconds=1),1),('ask','R035','102',T-timedelta(seconds=1),T,2)):
        observation=r.RawObservationOccurrenceV1(concept_id=r.concept_id('raw_signal.raw_observation_occurrence'),contract_id=r.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),observation_occurrence_id=r.observation_occurrence_id('independent-'+side),delivery_artifact_ref=r.delivery_artifact_ref('independent-delivery'),source_provider=r.provider_id('foundation-pilot-fixture'),native_record={'quote':{side:Decimal(value)}},received_ts_utc=receipt,ingestion_sequence=seq,ingestion_sequence_scope=r.ingestion_sequence_scope('foundation-pilot-fixture/cash_quote_v1'),source_temporal_kind='true_instant',raw_signal_catalogue_ids=(r.RawSignalCatalogueId(rid),),source_variant='cash_quote_v1',subject_instrument='NVDA',native_units='price',source_timestamp_raw=event.isoformat().replace('+00:00','Z'),source_timezone_native='UTC')
        raw.commands.admit_raw_observation_occurrence(observation)
    mid=previous.materialise(old_request('D011'))
    assert ratio.materialise(missing) is None and history(ratio.reads)==()
    spread=previous.materialise(old_request('D012'))
    assert type(mid.result) is type(spread.result) is Decimal
    req=ratio_request(mid,spread)
    result=ratio.materialise(req)
    assert result.result==f.ExactRatioV1(200,101)
    before=history(ratio.reads)
    for mode in ('representation','wrong-result','hash','configuration'):
        reader.mode=mode
        assert ratio.materialise(req) is None and history(ratio.reads)==before,mode
    reader.mode=None
    clock[0]=T+timedelta(seconds=90)
    assert ratio.materialise(req)==result
    assert ratio.materialise(missing) is None and history(ratio.reads)==before
    outputs=[result]
    for which in ('definition','selection','unit','mapping','parameter'):
        mid2=previous.materialise(old_request('D011',**{which:2}))
        assert mid2 is not None
        before=history(ratio.reads)
        mixed=ratio.materialise(ratio_request(mid2,spread))
        if which=='definition':
            assert mixed is not None and mixed!=result
            outputs.append(mixed)
        else:
            assert mixed is None and history(ratio.reads)==before,which
            spread2=previous.materialise(old_request('D012',**{which:2}))
            joint=ratio.materialise(ratio_request(mid2,spread2,parameter=2 if which=='parameter' else 1))
            assert joint is not None and joint.result==f.ExactRatioV1(200,101),which
            outputs.append(joint)
    later=ratio.materialise(ratio_request(mid,spread,definition='D013-RELATIVE-SPREAD-2'))
    assert later is not None and later!=result
    outputs.append(later)
    cutoff_mid=previous.materialise(old_request('D011',cutoff=T+timedelta(seconds=1)))
    before=history(ratio.reads)
    assert ratio.materialise(ratio_request(cutoff_mid,spread)) is None and history(ratio.reads)==before
    for output in outputs: assert ratio.reads.get_derived_occurrence(output.derived_occurrence_id)==output
    assert previous.reads.get_derived_occurrence(mid.derived_occurrence_id)==mid
    assert type(previous.reads.get_derived_occurrence(spread.derived_occurrence_id).result) is Decimal
    print('WRITER PASS absence/admit/midpoint/absence/spread/ratio/4forgeries/nonempty-refusal/later-retry/5version-dimensions/cutoff/old-Decimal',flush=True)
    return tuple(outputs),history(ratio.reads),RDEFS,PARAMS

def fresh_reader(path, ids):
    before=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    reader=f.create_ratio_reader(admission=f.OwnerAdmissionV1('M02',NEW),storage=f.SQLiteReadStorageV1(path))
    occurrences=tuple(reader.get_derived_occurrence(identity) for identity in ids)
    definitions=tuple(reader.get_calculation_definition(derived_signal_id='D013',calculation_definition_version='D013-RELATIVE-SPREAD-'+str(v)) for v in (1,2))
    parameters=tuple(reader.get_parameter_set(f.VersionRefV1('mmt-pilot-basic',v)) for v in (1,2))
    assert not hasattr(reader,'materialise')
    assert before==hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return occurrences,history(reader),definitions,parameters

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='writer':
        result=writer()
        with (BASE/'writer_result.pickle').open('wb') as stream: pickle.dump(result,stream)
    elif len(sys.argv)>1 and sys.argv[1]=='reader':
        result=fresh_reader(sys.argv[2],sys.argv[3:])
        sys.stdout.buffer.write(pickle.dumps(result))
    else:
        subprocess.run([sys.executable,__file__,'writer'],check=True)
        with (BASE/'writer_result.pickle').open('rb') as stream: expected=pickle.load(stream)
        ids=[value.derived_occurrence_id for value in expected[0]]
        actual=pickle.loads(subprocess.check_output([sys.executable,__file__,'reader',str(BASE/'stores/ratio.sqlite'),*ids]))
        assert actual==expected
        for occurrence in actual[0]:
            assert type(occurrence) is f.RatioOccurrenceV1 and len(occurrence.predecessor_evidence)==2
            assert all(type(ev.occurrence.result) is Decimal for ev in occurrence.predecessor_evidence)
        print('FRESH READER PASS complete typed bundle/7facts/2definitions/2parameters/history/no-reregistration/no-byte-write')
