"""Independent public ingress witnesses; no worker fixture imports.
Meaning: accepted brief K02 D025/D099/D100 and K08 D120, §§8.1,9,11,17.
"""
from datetime import UTC, datetime, timedelta
from decimal import Decimal as D
from dataclasses import replace
from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw
T = datetime(2026,10,14,12,tzinfo=UTC)
KEYS=('contract_id','underlying_instrument','expiry','strike','option_right')
IDENT=dict(contract_id='review-C',underlying_instrument='NVDA',expiry='2026-12-18',strike=D(150),option_right='call')
class Harness:
    def __init__(self, rids, identities, join_keys=KEYS):
        self.m00=raw.create_owner(); self.seq=0; self.rids=rids
        self.owner=api.create_owner(raw_projection_reader=self.m00.reads,
            raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1('review-'+rid,1,raw.RawSignalCatalogueId(rid),'independent-review','native',('values',rid),'canonical',tuple((k,('identity',k)) for k in KEYS)) for rid in rids),
            parameter_sets=(api.CalculationParameterSetV1('basic',1,'P_BASIC',(('selection_mode','exact'),)),api.CalculationParameterSetV1('rule',1,'P_RULE',(('window_seconds',D(60)),))),
            input_selection_policies=(api.InputSelectionPolicyVersionV1('select',1,join_keys,timedelta(seconds=60),timedelta(seconds=15),('true_instant',),()),),
            unit_conventions=(api.UnitConventionVersionV1('unit',1,'canonical','canonical',D(1),D(0)),),contexts=(),utc_now=lambda:T+timedelta(seconds=30))
        self.bindings=tuple(api.RawInputBindingV1(rid,api.VersionRefV1('review-'+rid,1),api.VersionRefV1('unit',1),'NVDA',raw.RawSelectionIdentityV1(tuple(ident.items()))) for ident in identities for rid in rids)
    def admit(self,oid,values,at=T,ident=IDENT):
        self.seq+=1
        self.m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
            concept_id=raw.concept_id('raw_signal.raw_observation_occurrence'),contract_id=raw.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),
            observation_occurrence_id=raw.observation_occurrence_id(oid),delivery_artifact_ref=raw.delivery_artifact_ref('artifact-'+oid),source_provider=raw.provider_id('independent-review'),
            native_record={'values':values,'identity':ident},received_ts_utc=at,ingestion_sequence=self.seq,ingestion_sequence_scope=raw.ingestion_sequence_scope('review-native'),source_temporal_kind='true_instant',source_timestamp_raw=at.isoformat(),source_timezone_native='UTC',raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(rid) for rid in values),source_variant='native',subject_instrument='NVDA',native_units='canonical',revision_vintage_native='v1'))
    def calc(self,did,at=T):
        req=api.CalculationRequestV1(did,'NVDA',at,at,'independent-native-v1','rule' if did in {'D015','D016','D120'} else 'basic',1,'select',1,(),parameter_profile_refs=(api.ParameterProfileRefV1('P_BASIC','basic',1),api.ParameterProfileRefV1('P_RULE','rule',1)),raw_input_bindings=self.bindings)
        return self.owner.materialise(req)
def check(label,actual,expected):
    print(label,repr(actual),'expected',repr(expected),flush=True); assert actual==expected,label

def range_witness():
    h=Harness(('R037','R039','R040'),(IDENT,))
    h.admit('review-range',{'R037':D(113),'R039':D(140),'R040':D(104)})
    out=h.calc('D025'); check('D025 asymmetric',None if out is None else out.result,D('.25'))
    assert {x.raw_signal_id for x in out.raw_input_lineage}=={'R037','R039','R040'}
    h2=Harness(('R037','R039','R040'),(IDENT,)); h2.admit('zero-range',{'R037':D(104),'R039':D(104),'R040':D(104)})
    check('D025 zero denominator',h2.calc('D025'),None)

def skew_witness():
    identities=tuple(dict(IDENT,contract_id=cid,option_right=side,strike=strike) for cid,side,strike in (('C25','call',D(160)),('P25','put',D(140)),('C10','call',D(170)),('P10','put',D(130))))
    vals=((D('.31'),D('.25'),'C'),(D('.44'),D('-.25'),'P'),(D('.27'),D('.10'),'C'),(D('.46'),D('-.10'),'P'))
    for defect in (None,'numeric','conflict','missing'):
        h=Harness(('R111','R112','R015'),identities,('underlying_instrument','expiry'))
        for ident,(iv,delta,right) in zip(identities,vals):
            v={'R111':iv,'R112':delta,'R015':right}
            if ident['contract_id']=='P25':
                if defect=='numeric':v['R015']=ident['strike']
                if defect=='conflict':v['R015']='C'
                if defect=='missing':del v['R015']
            h.admit('review-'+str(ident['contract_id']),v,ident=ident)
        for did,expected in (('D099',D(13)),('D100',D(19))):
            out=h.calc(did)
            check(did+' '+str(defect),None if out is None else out.result,expected if defect is None else None)
            if out:assert {x.raw_signal_id for x in out.raw_input_lineage}=={'R111','R112','R015'}

def flow_witness():
    rids=('R034','R035','R120','R121','R126','R127','R015','R016')
    def setup(defect=None):
        h=Harness(rids,(IDENT,))
        h.admit('quote-start',{'R034':D(4),'R035':D(6)})
        for oid,at,price,size in (('buy',T,D(6),D(2)),('sell',T+timedelta(seconds=5),D(4),D(3))):
            v={'R120':price,'R121':size,'R126':D(4),'R127':D(6),'R015':'C','R016':D(75)}
            if oid=='sell':
                if defect=='missing_multiplier':del v['R016']
                if defect=='numeric_right':v['R015']=D(75)
                if defect=='conflict_right':v['R015']='P'
                if defect=='zero_multiplier':v['R016']=D(0)
            h.admit(oid,v,at)
        return h
    h=setup(); out=h.calc('D120',T+timedelta(seconds=5))
    check('D120 cold recursive',None if out is None else dict(out.result),{'signed_contracts':D(-1),'signed_premium_notional':D(0)})
    assert {'R015','R016','R120','R121'} <= {x.raw_signal_id for x in out.raw_input_lineage}
    h.admit('quote-only-later',{'R034':D(2),'R035':D(4)},T+timedelta(seconds=10))
    later=h.calc('D120',T+timedelta(seconds=10)); check('D120 quote-only update',None if later is None else dict(later.result),{'signed_contracts':D(-1),'signed_premium_notional':D(0)})
    check('D120 retry',h.calc('D120',T+timedelta(seconds=10)),later)
    # Non-zero premium distinguishes the actual multiplier from option right/strike.
    single=Harness(rids,(IDENT,)); single.admit('q',{'R034':D(4),'R035':D(6)}); single.admit('b',{'R120':D(6),'R121':D(2),'R126':D(4),'R127':D(6),'R015':'C','R016':D(75)})
    one=single.calc('D120');check('D120 multiplier 75',None if one is None else dict(one.result),{'signed_contracts':D(2),'signed_premium_notional':D(900)})
    for defect in ('missing_multiplier','numeric_right','conflict_right','zero_multiplier'):
        bad=setup(defect); check('D120 '+defect,bad.calc('D120',T+timedelta(seconds=5)),None)
if __name__=='__main__':
    import sys
    for unit in sys.argv[1:] or ('range','skew','flow'):
        globals()[unit+'_witness']()
    print('ALL REQUESTED INDEPENDENT WITNESSES PASSED')
