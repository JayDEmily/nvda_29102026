"""Literal Brief2 tables -> immutable input/oracle; deliberately imports no M00 code."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
def jline(path,rows):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n' for x in rows))
def typed(v):
 if isinstance(v,dict):return {k:typed(x) for k,x in v.items()}
 if isinstance(v,tuple):return {'native_type':'Decimal','value':v[0]}
 if v is None:return {'native_type':'NoneType','value':None}
 return {'native_type':type(v).__name__,'value':str(v) if type(v) is int else v}
def d(s):return (s,)
def clock(s,date='2026-10-20'):return date+'T'+s+'Z'
subjects={'STK':'NVDA-STK-CONTROL-1','CALL':'NVDA-OPT-C100-CONTROL-1','PUT':'NVDA-OPT-P100-CONTROL-1'}
families={'A':('NVDA-IBKR-M00-SYNTHETIC-INPUT-V1',1,'foundation-controlled-ibkr-m00-v1'),'B':('NVDA-CONTROLLED-IBKR-RECEIPT-BOOK-V1',1,'foundation-controlled-ibkr-book-v1'),'C':('NVDA-M00-COHERENT-INTEGRATION-V2',2,'foundation-controlled-ibkr-m00-coherent-v2')}
# Tuples fix sequence, receipt, native fields; these literals are the authority-derived operands.
tables={
'A1':[(1,'12:40:00.080',{'bid_price':d('99'),'ask_price':d('101'),'bid_size':d('3'),'ask_size':d('1')})],
'A2':[(11,'12:40:00.100',{'tickType':1,'price':d('1.20')}),(12,'12:40:00.130',{'tickType':0,'size':d('10')}),(13,'12:40:00.160',{'tickType':2,'price':d('1.40')}),(14,'12:40:00.180',{'tickType':3,'size':d('8')})],
'A3':[(15,'12:40:00.200',{'tickType':1,'price':d('2.20')}),(16,'12:40:00.220',{'tickType':0,'size':d('6')}),(17,'12:40:00.250',{'tickType':2,'price':d('2.40')}),(18,'12:40:00.270',{'tickType':3,'size':d('4')})],
'A4':[(21,'12:39:59.100',(1,0,'99.00','5')),(22,'12:39:59.200',(1,1,'98.00','3')),(23,'12:39:59.300',(0,0,'101.00','2')),(24,'12:39:59.400',(0,1,'102.00','4'))],
'A5':[(31,'12:39:59.100',(1,0,'99.80','5')),(32,'12:39:59.200',(1,1,'99.00','7')),(33,'12:39:59.300',(0,0,'100.20','3'))],
'A6':[(34,'12:39:59.600',(1,0,'2.20','6')),(35,'12:39:59.700',(0,0,'2.40','4'))],
'B':[(1001,'14:00:01.000000',(1,0,'99.00','5')),(1002,'14:00:02.000000',(1,1,'98.50','3')),(1003,'14:00:03.000000',(0,0,'101.00','2')),(1004,'14:00:04.000000',(0,1,'101.50','4')),(2001,'14:00:05.000000',(1,0,'99.80','5')),(2002,'14:00:06.000000',(1,1,'99.00','7')),(2003,'14:00:07.000000',(0,0,'100.20','3'))],
'C1':[(301,'12:39:59.100',(1,0,'1.20','5')),(302,'12:39:59.200',(1,1,'0.70','7')),(303,'12:39:59.300',(0,0,'1.40','3'))],
'C2':[(401,'12:39:58.100',(1,0,'99.00','4','ALPHA')),(402,'12:39:58.200',(1,1,'98.50','1','BETA')),(403,'12:39:58.300',(0,0,'101.00','2','ALPHA')),(404,'12:39:58.400',(0,1,'101.50','1','BETA'))],
'C3':[(501,'12:39:58.500',(1,0,'1.20','4','ALPHA')),(502,'12:39:58.600',(1,1,'1.10','1','BETA')),(503,'12:39:58.700',(0,0,'1.40','2','ALPHA')),(504,'12:39:58.800',(0,1,'1.50','1','BETA'))]}
scopes={'A1':('STK1/BIDASK/G1','STK-BIDASK-R1','STK-BIDASK-G1'),'A2':('OPT-C100/L1/G1','OPT-C100-R1','OPT-L1-G1'),'A3':('OPT-P100/L1/G1','OPT-P100-R1','OPT-P100-L1-G1'),'A4':('STK1/SMART/G1','STK-SMART-R1','STK-SMART-G1'),'A5':('OPT-C100/SMART/LEGACY-G1','OPT-C100-LEGACY-R1','OPT-C100-LEGACY-G1'),'A6':('OPT-P100/SMART/G1','OPT-P100-SMART-R1','OPT-P100-SMART-G1'),'C1':('OPT-C100/SMART/COHERENT-V2','COH-CALL-R1','OPT-C100-SMART-COHERENT-V2'),'C2':('STK1/DIRECT-EXCH1/GEN1','COH-DIRECT-STK-R1','COH-DIRECT-STK-GEN1'),'C3':('OPT-C100/DIRECT-EXCH1/GEN1','COH-DIRECT-CALL-R1','COH-DIRECT-CALL-GEN1')}
inputs=[]; expected=[]; mappings={}; counts={}
for scenario,events in tables.items():
 fam=scenario[0];fixture,version,provider=families[fam]
 for ix,(seq,receipt,values) in enumerate(events):
  instrument='STK' if scenario in ['A1','A4','C2'] or scenario=='B' and seq<2000 else 'PUT' if scenario in ['A3','A6'] else 'CALL'
  direct=scenario in ['C2','C3'];l1=scenario in ['A1','A2','A3']
  scope,request,generation=scopes.get(scenario,('SYNTH-STK-SMART-01','B-STK-R1','GEN-STK-01') if instrument=='STK' else ('SYNTH-OPT-SMART-01','B-OPT-R1','GEN-OPT-01'))
  subject=subjects[instrument]
  if fam=='B':subject='NVDA/STK/USD/SMART/TEST-ONLY' if instrument=='STK' else 'NVDA/OPT/20261030/100/C/100/USD/SMART/TEST-ONLY'
  group=scenario+'-'+instrument;native_req={'A1':111,'A2':112,'A3':113,'A4':101,'A5':115,'A6':116,'B-STK':201,'B-CALL':202,'C1':301,'C2':302,'C3':303}[group if scenario=='B' else scenario]
  exchange='SYNTH-DIRECT-EXCHANGE-1' if scenario=='C2' else 'SYNTH-DIRECT-OPT-EXCHANGE-1' if scenario=='C3' else 'SMART' if not l1 else 'SYNTH-L1'
  collector={'schema_version':'collector-envelope/1','fixture_id':fixture,'fixture_version':version,'scenario_id':scenario,'subject':subject,'request':request,'generation':generation,'requested_exchange':exchange,'origin':'synthetic','native_req_id':native_req,'contract_spec':{'security_type':'STK' if instrument=='STK' else 'OPT','right':None if instrument=='STK' else 'C' if instrument=='CALL' else 'P','multiplier':1 if instrument=='STK' else 100,'currency':'USD','expiry':None if instrument=='STK' else '2026-10-30' if fam=='B' else '2026-10-23','strike':None if instrument=='STK' else '100'}}
  if l1:
   native=values.copy();callback='tickByTickBidAsk' if scenario=='A1' else 'tickPrice' if 'price' in values else 'tickSize'
   roles={'R033':('bid_size','shares'),'R034':('bid_price','USD/share'),'R035':('ask_price','USD/share'),'R036':('ask_size','shares')} if scenario=='A1' else {['R034','R033','R035','R036'][ix]:(('price' if 'price' in values else 'size'),('USD/underlying-share-premium' if 'price' in values else 'contracts'))}
  else:
   side,pos,price,size,*mpid=values;native={'position':pos,'operation':0,'side':side,'price':d(price),'size':d(size),'isSmartDepth':not direct,'marketMaker':mpid[0] if direct else 'SYNTH-EXCHANGE'};callback='updateMktDepthL2'
   ids=['R192','R194','R195','R196','R197'] if direct else ['R185','R187','R188','R189','R190'];fields=['position','operation','side','price','size'];units=['book-position','operation-code','side-code','USD/share' if instrument=='STK' else 'USD/underlying-share-premium','shares' if instrument=='STK' else 'contracts'];roles={rid:(field,unit) for rid,field,unit in zip(ids,fields,units)}
   if direct:roles['R193']=('marketMaker','MPID')
  native['reqId']=native_req;native['_collector']=collector
  oid='SYN-L1-STK-ATOMIC-01' if scenario=='A1' else f'NVDA-M00-A-V1-{scenario}-SEQ{seq}' if fam=='A' else f'SYNTH-IBKR-V1-{"S" if instrument=="STK" else "O"}{(ix+1 if instrument=="STK" else ix-3):02}' if fam=='B' else f'COH-SMART-C{ix+1:02}' if scenario=='C1' else f'COH-DIRECT-{"STK" if scenario=="C2" else "CALL"}-{ix+1:02}'
  at=clock(receipt,'2026-10-26' if fam=='B' else '2026-10-20')
  # Canonical microsecond receipt formatting; native source text kept exact.
  if '.' in at:at=at[:-1].split('.')[0]+'.'+at[:-1].split('.')[1].ljust(6,'0')+'Z'
  observation=dict(concept_id='raw_signal.raw_observation_occurrence',contract_id='nvda.raw_signal.RawObservationOccurrence.v1',observation_occurrence_id=oid,delivery_artifact_ref='synthetic-delivery:'+oid,source_provider=provider,native_record=typed(native),received_ts_utc=at,ingestion_sequence=seq,ingestion_sequence_scope=scope,source_temporal_kind='true_instant' if scenario=='A1' else 'receipt_only',raw_signal_catalogue_ids=sorted(roles),source_product_api='TWS_SOCKET_API_SYNTHETIC_SPECIMEN',source_endpoint_callback=callback,native_identifier=subject,native_tick_series_identifier=request,source_variant='SMART' if fam=='B' else 'ibkr-bidask-atomic/native-v1' if scenario=='A1' else 'ibkr-async-l1/native-v1' if l1 else 'ibkr-direct-depth/native-v2' if direct else 'ibkr-smart-depth/native-v2' if fam=='C' else 'ibkr-smart-depth/native-v1',subject_instrument=subject,native_units='mixed-native-roles',availability_session=None,source_status_native=None,revision_vintage_native=None,received_epoch_ns=None,source_timestamp_raw='2026-10-20T12:40:00.000Z' if scenario=='A1' else None,source_timezone_native='UTC' if scenario=='A1' else None,market_timezone_iana=None,market_session_native=None)
  meta=dict(fixture_id=fixture,fixture_version=version,family=fam,scenario_id=scenario,mapping_group=group)
  inputs.append(dict(**meta,observation=observation));expected.append(dict(kind='observation',**meta,value=observation))
  identity_paths={k:['_collector',k] for k in ['subject','request','generation','requested_exchange','scenario_id']}
  if not l1:identity_paths.update(isSmartDepth=['isSmartDepth'],marketMaker=['marketMaker'])
  for rid,(field,unit) in sorted(roles.items()):
   mapping=dict(mapping_id=f'm00b2-{group.lower()}-{rid.lower()}',version=1,raw_signal_catalogue_id=rid,source_provider=provider,source_variant=observation['source_variant'],native_field_path=[field],native_units=unit,selection_identity_field_paths=[[key,path] for key,path in sorted(identity_paths.items())])
   mappings.setdefault(group,{})[rid]=mapping
   identity={k:(collector[k] if path[0]=='_collector' else native[path[0]]) for k,path in identity_paths.items()}
   p=dict(raw_signal_catalogue_id=rid,observation_occurrence_id=oid,projection_mapping_id=mapping['mapping_id'],projection_mapping_version=1,source_provider=provider,source_variant=observation['source_variant'],native_field_path=[field],native_value=typed(native[field]),native_units=unit,subject_instrument=subject,source_temporal_kind=observation['source_temporal_kind'],source_timestamp_raw=observation['source_timestamp_raw'],source_timezone_native=observation['source_timezone_native'],received_ts_utc=at,ingestion_sequence=seq,ingestion_sequence_scope=scope,revision_vintage_native=None,selection_identity=identity)
   expected.append(dict(kind='projection',**meta,value=p))
  counts.setdefault(scenario,[0,0]);counts[scenario][0]+=1;counts[scenario][1]+=len(roles)
expected.sort(key=lambda x:(x['family'],x['scenario_id'],x['kind'],x['value'].get('raw_signal_catalogue_id',''),x['value']['received_ts_utc'],x['value']['ingestion_sequence_scope'],x['value']['ingestion_sequence'],x['value']['observation_occurrence_id']))
for fam in families:
 jline(root/'fixtures'/fam/'synthetic_input_v1.jsonl',[x for x in inputs if x['family']==fam]);jline(root/'fixtures'/fam/'expected_m00_output_v1.jsonl',[x for x in expected if x['family']==fam])
(root/'mapping_manifest_v1.json').write_text(json.dumps({'schema_version':'m00b2-mappings/1','groups':mappings,'callback_field_map':{'tickPrice':'tickType identifies bid/ask; brief bid_price/ask_price maps to native price','tickSize':'tickType identifies bid/ask; brief bid_size/ask_size maps to native size','tickByTickBidAsk':'authorised snake_case aliases, values exactly as brief','collector':'_collector is synthetic collector-added metadata, never IBKR arguments'},'harness_choices':'Unspecified synthetic request/generation/reqId identities are fixed here. No real conId/feed entitlement claimed.'},indent=2,sort_keys=True)+'\n')
negatives=[('N01','preserve side values, no inversion'),('N02','valid receipt-only and no source timestamp'),('N03','reject receipt-only invented timestamp'),('N04','event cutoff excludes receipt-only'),('N05','equal receipt/scope/sequence keeps both IDs; causal ambiguity explicit'),('N06','remove each native operation/position/side/size/MPID, no corresponding R'),('N07','preserve INSERT/UPDATE/DELETE/zero size'),('N08','discover error317 after depth'),('N09','discover316/reconnect/gap/restart and generation links'),('N10','isolate subject/right/source/request/generation'),('N11','one asynchronous callback different contract stays different'),('N12','duplicate batch receipt keeps callback IDs'),('N13','strictly post-cutoff excluded from history only'),('N14','no initial snapshot/field implies no fabricated completeness'),('N15','known control ID retrieval cannot replace discovery'),('N16','identical replay idempotent, changed same-ID payload refuses'),('N17','direct MPID separate requested exchange'),('N18','missing receipt carrier absent; valid carrier UTC equals envelope')]
jline(root/'fixtures/negative/expectations_v1.jsonl',[dict(case_id=i,expectation=e,base_scenario='C2' if i in ['N06','N17'] else 'A4',isolation='fresh SQLite store and copy; never mutate approved positive bytes') for i,e in negatives])
controls=[]
for i,kind in enumerate(['error317','error316','reconnect','gap','restart']):
 c=dict(schema_version='m00-control-envelope/1',kind=kind,request='STK-SMART-R1',generation_before='STK-SMART-G1',generation_after='STK-SMART-G2' if kind=='restart' else 'STK-SMART-G1',invalidates=True,origin='provider_callback' if kind.startswith('error') else 'collector_control')
 controls.append(dict(control_id='M00B2-CONTROL-'+kind,subject=subjects['STK'],request='STK-SMART-R1',scope='STK1/SMART/G1',receipt=clock(f'12:39:59.{500+i*100:03}000'),sequence=25+i,native_callback={'reqId':101,'errorCode':int(kind[5:]),'errorString':'synthetic '+kind} if kind.startswith('error') else {},control=c))
jline(root/'fixtures/controls/control_input_v1.jsonl',controls)

# Concrete perturbation/query operands, separate from immutable positive bytes.
operands={
'N01':{'base_scenario':'A4','operations':[],'expected_native_sides':[1,1,0,0]},
'N02':{'base_scenario':'A4','operations':[],'query':{'event_at_or_before_utc':None}},
'N03':{'base_scenario':'A4','replace_envelope':{'source_timestamp_raw':'2026-10-20T12:39:59Z'},'expected':'REJECT_TEMPORAL_DISCRIMINANT'},
'N04':{'base_scenario':'B','query':{'event_at_or_before_utc':'2026-10-26T14:00:10Z'},'expected_projection_count':0},
'N05':{'base_scenario':'A4','copy_event_index':0,'new_id':'M00B2-N05-TIED','preserve':['received_ts_utc','ingestion_sequence_scope','ingestion_sequence'],'expected':'BOTH_RETAINED_CAUSAL_ORDER_UNKNOWN'},
'N06':{'base_scenario':'C2','event_index':0,'remove_native_fields':['operation','position','side','size','marketMaker'],'expected_missing_roles':['R194','R192','R195','R197','R193'],'perturbation_mode':'ONE_FIELD_AT_A_TIME_FRESH_STORE','other_native_facts':'PRESERVED_EXACTLY'},
'N07':{'base_scenario':'A4','event_index':0,'mutation_events':[{'operation':0,'position':0,'size':'5'},{'operation':1,'position':0,'size':'0'},{'operation':2,'position':0,'size':'0'}],'expected':'EXACT_NATIVE_NOT_STANDING_STATE'},
'N08':{'base_scenario':'A4','controls':['M00B2-CONTROL-error317'],'query':{'request':'STK-SMART-R1','generation':'STK-SMART-G1','receipt_cutoff':'2026-10-20T12:40:01Z'}},
'N09':{'base_scenario':'A4','controls':['M00B2-CONTROL-error316','M00B2-CONTROL-reconnect','M00B2-CONTROL-gap','M00B2-CONTROL-restart'],'expected':'DISCOVERABLE_INVALIDITY_AND_GENERATION_LINKS'},
'N10':{'base_scenarios':['A4','A5','A6','C2','C3'],'selector_dimensions':['subject','request','generation','source_provider','source_variant','requested_exchange'],'perturbations':{'request':'OTHER-REQUEST','generation':'OTHER-GENERATION','subject':'OTHER-SUBJECT'},'expected':'ONLY_EXACT_SELECTED_IDENTITY'},
'N11':{'base_scenario':'A2','event_index':3,'replace_envelope':{'subject_instrument':'NVDA-OPT-P100-CONTROL-1'},'replace_collector':{'subject':'NVDA-OPT-P100-CONTROL-1','contract_spec':{'security_type':'OPT','right':'P','multiplier':100,'currency':'USD','expiry':'2026-10-23','strike':'100'}},'expected':'FOUR_DISTINCT_IDS_WITH_REPLACED_CONTRACT_RETAINED'},
'N12':{'base_scenario':'A2','replace_envelope':{'received_ts_utc':'2026-10-20T12:40:00.100000Z'},'expected_distinct_occurrences':4},
'N13':{'base_scenario':'A4','copy_event_index':0,'new_id':'M00B2-N13-FUTURE','replace_envelope':{'received_ts_utc':'2026-10-20T12:40:02.000000Z','ingestion_sequence':1000},'receipt_cutoff':'2026-10-20T12:40:01Z','expected':'HISTORY_EXCLUDES_KNOWN_ID_READ_PRESERVES'},
'N14':{'base_scenario':'A4','event_index':0,'remove_native_fields':['position'],'admit_only_event_index':0,'expected':'SEEN_FACTS_NO_COMPLETE_SNAPSHOT_CLAIM'},
'N15':{'base_scenario':'A4','control_id':'M00B2-CONTROL-error317','known_id_lookup_first':True,'consumer_knows_ids':False,'query':{'request':'STK-SMART-R1','generation':'STK-SMART-G1','receipt_cutoff':'2026-10-20T12:40:01Z'},'expected':'PUBLIC_DISCOVERY_REQUIRED'},
'N16':{'base_scenario':'A4','event_index':0,'identical_retry':True,'conflicting_native':{'price':{'native_type':'Decimal','value':'999.00'}},'expected':'IDENTICAL_IDEMPOTENT_CONFLICT_REJECTED_ORIGINAL_RETAINED'},
'N17':{'base_scenario':'C3','event_index':0,'expected_mpid':'ALPHA','expected_requested_exchange':'SYNTH-DIRECT-OPT-EXCHANGE-1','expected_isSmartDepth':False},
'N18':{'base_scenario':'A4','event_index':0,'carrier_path':['time','receipt'],'mapping_raw_id':'R001','valid_collector_receipt':{'native_type':'datetime','value':'2026-10-20T12:39:59.100000Z'},'missing_carrier_expected':'ABSENT','valid_carrier_expected':'EQUAL_ENVELOPE_RECEIPT_NOT_PROVIDER_TIME'}
}
jline(root/'fixtures/negative/expectations_v1.jsonl',[{'case_id':case,'index_only':True,'specification':f'{case}_v1.jsonl','base_scenario':operands[case].get('base_scenario'),'expectation':expectation} for case,expectation in negatives])
for row in negatives:
 case=row[0]; obj={'case_id':case,**operands[case]}
 jline(root/'fixtures/negative'/f'{case}_v1.jsonl',[obj])
for control in controls:
 control.update(source_provider='foundation-controlled-ibkr-m00-v1',source_variant='ibkr-smart-depth/native-v1',source_endpoint_callback='error' if control['control']['origin']=='provider_callback' else 'collectorControl',source_temporal_kind='receipt_only',source_timestamp_raw=None)
jline(root/'fixtures/controls/control_input_v1.jsonl',controls)
jline(root/'fixtures/controls/expected_control_output_v1.jsonl',[{'kind':'control','fixture_id':'M00B2-CONTROLS-V1','fixture_version':1,'family':'CONTROLS','scenario_id':'CONTROL','mapping_group':'CONTROL','value':x} for x in controls])
# Closed schemas use only keywords implemented by the unchanged kernel validator.
def obj(props):return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
string={'type':'string'};nonempty={'type':'string','minLength':1};nullable={'type':['string','null']};integer={'type':'integer'}
utc={'type':'string','pattern':r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z'}
tag=obj({'native_type':{'enum':['Decimal','int','str','bool','NoneType','datetime']},'value':{}})
kindvalues={'Decimal':{'type':'string','pattern':r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[Ee][+-]?[0-9]+)?'},'int':{'type':'string','pattern':r'-?(?:0|[1-9][0-9]*)'},'str':string,'bool':{'type':'boolean'},'NoneType':{'type':'null'},'datetime':utc}
tag['allOf']=[{'if':{'properties':{'native_type':{'const':k}}},'then':{'properties':{'value':v}}} for k,v in kindvalues.items()]
def native(depth):
 if depth==0:return tag
 return {'type':'object','if':{'required':['native_type']},'then':tag,'allOf':[{'if':{'not':{'required':['native_type']}},'then':{'type':'object','additionalProperties':native(depth-1)}}]}
observation_props={key:nullable if value is None else integer if type(value) is int else string for key,value in inputs[0]['observation'].items()}
observation_props.update(source_timestamp_raw=nullable,source_timezone_native=nullable,native_record={'type':'object','additionalProperties':native(4)},received_ts_utc=utc,ingestion_sequence=integer,received_epoch_ns={'type':['integer','null']},raw_signal_catalogue_ids={'type':['array','null'],'items':{'type':'string','pattern':'R[0-9]{3}'}},source_temporal_kind={'enum':['receipt_only','date_only','true_instant']})
obs_schema=obj(observation_props)
obs_schema['allOf']=[{'if':{'properties':{'source_temporal_kind':{'const':'receipt_only'}}},'then':{'properties':{'source_timestamp_raw':{'type':'null'}}}}]
projection_props={key:nullable if value is None else integer if type(value) is int else string for key,value in next(x['value'] for x in expected if x['kind']=='projection').items()}
projection_props.update(source_timestamp_raw=nullable,source_timezone_native=nullable,native_value=tag,native_field_path={'type':'array','minItems':1,'items':nonempty},received_ts_utc=utc,selection_identity={'type':'object','required':['subject','request','generation','requested_exchange','scenario_id'],'additionalProperties':{'type':['string','integer','boolean']}},source_temporal_kind={'enum':['receipt_only','date_only','true_instant']})
projection_props['raw_signal_catalogue_id']={'type':'string','pattern':'R[0-9]{3}'}
proj_schema=obj(projection_props);proj_schema['allOf']=obs_schema['allOf']
control_schema=obj({'control_id':nonempty,'subject':nonempty,'request':nonempty,'scope':nonempty,'receipt':utc,'sequence':integer,'native_callback':{'type':'object','additionalProperties':False,'properties':{'reqId':integer,'errorCode':integer,'errorString':string}},'control':obj({'schema_version':{'const':'m00-control-envelope/1'},'kind':{'enum':['error317','error316','reconnect','gap','restart']},'request':nonempty,'generation_before':nonempty,'generation_after':nonempty,'invalidates':{'type':'boolean'},'origin':{'enum':['provider_callback','collector_control']}}),'source_provider':nonempty,'source_variant':nonempty,'source_endpoint_callback':nonempty,'source_temporal_kind':{'const':'receipt_only'},'source_timestamp_raw':{'type':'null'}})
schema=obj({'kind':{'enum':['observation','projection','control','absence','rejection']},'fixture_id':nonempty,'fixture_version':integer,'family':nonempty,'scenario_id':nonempty,'mapping_group':nonempty,'value':{'type':'object'}})
schema['allOf']=[{'if':{'properties':{'kind':{'const':k}}},'then':{'properties':{'value':v}}} for k,v in {'observation':obs_schema,'projection':proj_schema,'control':control_schema,'absence':obj({'case_id':nonempty,'observation_occurrence_id':nonempty,'raw_signal_catalogue_id':{'type':'string','pattern':'R[0-9]{3}'},'reason':nonempty}),'rejection':obj({'case_id':nonempty,'observation_occurrence_id':nonempty,'reason':nonempty})}.items()]
def anchor_patterns(node):
 if isinstance(node,dict):
  for key,value in node.items():
   if key=='pattern':node[key]='^'+value+'$'
   else:anchor_patterns(value)
 elif isinstance(node,list):
  for value in node:anchor_patterns(value)
anchor_patterns(schema)
(root/'output_schema_v1.json').write_text(json.dumps(schema,indent=2,sort_keys=True)+'\n')
assert counts=={'A1':[1,4],'A2':[4,4],'A3':[4,4],'A4':[4,20],'A5':[3,15],'A6':[2,10],'B':[7,35],'C1':[3,15],'C2':[4,24],'C3':[4,24]},counts
hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'fixtures').rglob('*')) if p.is_file()}
for name in ['mapping_manifest_v1.json','output_schema_v1.json']:hashes[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
(root/'fixture_manifest_v1.json').write_text(json.dumps({'schema_version':'m00b2-fixtures/1','status':'EXPECTED_SYNTHETIC_OUTPUT_AUTHORISED','actual_output_status':'NOT_ATTEMPTED','counts':counts,'observation_total':36,'projection_total':155,'hashes':hashes,'controls_additional':5,'direct_put':'NOT_COVERED; PUT L1/SMART A3/A6 are mandatory and included','native_source_claim':'SYNTHETIC_ONLY'},indent=2,sort_keys=True)+'\n')
print('Authoring checks:10 literal scenarios,36 observations/155 expected projections,18 concrete negative specifications,5 separate expected controls; no M00 import/execution.')
