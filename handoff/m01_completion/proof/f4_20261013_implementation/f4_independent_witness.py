from datetime import timedelta
import sys
mode=sys.argv[1] if len(sys.argv)>1 else 'combined'
from dataclasses import replace
from decimal import Decimal as D
from nvda_desk.derived_signal_calculation_truth import api
from nvda_desk.raw_signal_occurrence_truth import api as raw
from tests.product.derived_signal.test_m01_f4_approved_monetary_policy import fixture, ev, budget, NOW, kv

# Direct public ingress, without the worker public helper or a seeded derived result.
print('MODE',mode)
context_qty = D(2) if mode=='unit_only' else D(20)
f = fixture()
candidate, live, scope, definition, membership = f['contexts']
candidate = replace(candidate, leg_quantities=(context_qty,))
live = replace(live, signed_quantities=(context_qty,))
membership = replace(membership, parameters=(('account_identity','account'),('sleeve_identity','managed'),('complete_members',(f'option|{context_qty}|position-source',))))
f['contexts'] = (candidate, live, scope, definition, membership)
m00 = raw.create_owner()
values = {'R212':D(2), 'R016':D(100), 'R112':D('.5'), 'R115':D('.04'), 'R116':D('1.2'), 'R117':D('-.2')}
m00.commands.admit_raw_observation_occurrence(raw.RawObservationOccurrenceV1(
    concept_id=raw.concept_id('raw_signal.raw_observation_occurrence'),
    contract_id=raw.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),
    observation_occurrence_id=raw.observation_occurrence_id('position-source'),
    delivery_artifact_ref=raw.delivery_artifact_ref('review-delivery'),
    source_provider=raw.provider_id('review'), native_record=values,
    received_ts_utc=NOW, ingestion_sequence=1,
    ingestion_sequence_scope=raw.ingestion_sequence_scope('review'),
    source_temporal_kind='true_instant',source_timestamp_raw=NOW.isoformat(),
    source_timezone_native='UTC', raw_signal_catalogue_ids=tuple(raw.RawSignalCatalogueId(k) for k in values),
    subject_instrument='NVDA', native_units='review_native',revision_vintage_native='1'))
units = {'R212':'contracts','R016':'shares_per_contract','R112':'delta','R115':'gamma','R116':'currency_per_volatility_fraction','R117':'currency_per_day'}
if mode=='quantity_only': units['R116']='currency_per_volatility_point'
owner=api.create_owner(raw_projection_reader=m00.reads,
    raw_projection_mappings=tuple(raw.RawSignalProjectionMappingV1('map-'+rid,1,raw.RawSignalCatalogueId(rid),'review',None,(rid,),'review_native') for rid in values),
    unit_conventions=tuple(api.UnitConventionVersionV1('unit-'+rid,1,'review_native',units[rid],D(1),D(0)) for rid in values),
    parameter_sets=(api.CalculationParameterSetV1('basic',1,'P_BASIC',(('subject_instrument','NVDA'),)),),
    input_selection_policies=(api.InputSelectionPolicyVersionV1('select',1,('subject_instrument',),timedelta(seconds=30),timedelta(seconds=30),('true_instant',),()),),
    contexts=(live,),utc_now=lambda:NOW)
projected={}
for did in ('D181','D182','D183','D184'):
    req=api.CalculationRequestV1(did,'NVDA',NOW,NOW,'review','basic',1,'select',1,(api.VersionRefV1('live',1),),
        raw_input_bindings=tuple(api.RawInputBindingV1(rid,api.VersionRefV1('map-'+rid,1),api.VersionRefV1('unit-'+rid,1),'NVDA',None) for rid in values))
    occurrence=owner.materialise(req)
    assert occurrence is not None
    projected[did]=(owner._occurrence_kernel_value(occurrence),)
    if did=='D183':
        print('PUBLIC D183', occurrence.result, 'source canonical units',[(x.raw_signal_id,x.canonical_units) for x in occurrence.raw_input_lineage], 'projected risk unit',dict(projected[did][0].metadata)['canonical_risk_unit'])
current=tuple((name,projected[did][0].value) for name,did in zip(('delta','gamma','vega','theta'),projected))
matrix=dict(f['derived']['D174'][0].value); matrix['reference_greeks']=current
f['derived']['D174']=(kv('D174',tuple(matrix.items())),)
b=budget(f)
hf={'raw':{},'derived':{'D175':(kv('D175',b),),**projected},'contexts':f['contexts'],'params':dict(f['params'])|{'target_bands':tuple(n+'|0|0' for n,_ in current)}}
h=ev('D189',hf)
print('SOURCE QUANTITY',values['R212'],'CONTEXT/MEMBERSHIP QUANTITY',live.signed_quantities,'D189 EMITS',h is not None)
if h: print('D189 current',dict(h.value)['current_exposure'],'adjustment',dict(h.value)['adjustment'])
