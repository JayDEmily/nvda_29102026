import json, os, subprocess, sys, tempfile, hashlib
from pathlib import Path
from datetime import UTC, datetime
from decimal import Decimal
from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
from export_m00_synthetic import difference

def read(path):
 raw=r.create_owner(durability_port=create_sqlite_persistence(str(path),create=False))
 m=r.RawSignalProjectionMappingV1('independent-export-price',1,r.RawSignalCatalogueId('R189'),'review-synthetic','review-depth',('price',),'USD/underlying share premium')
 result=[]
 for key in ('absent','present'):
  p=raw.reads.project_raw_value(r.RawSignalCatalogueId('R189'),r.observation_occurrence_id(key),mappings=(m,))
  result.append(None if p is None else {'native_type':type(p.native_value).__name__,'value':str(p.native_value),'source_timestamp_raw':p.source_timestamp_raw})
 return result

def main():
 path=Path(tempfile.mkdtemp(prefix='l05-independent-'))/'raw.db'
 raw=r.create_owner(durability_port=create_sqlite_persistence(str(path),create=True))
 def observation(key,sequence,native):
  return r.RawObservationOccurrenceV1(concept_id=r.concept_id('raw_signal.raw_observation_occurrence'),contract_id=r.contract_id('nvda.raw_signal.RawObservationOccurrence.v1'),observation_occurrence_id=r.observation_occurrence_id(key),delivery_artifact_ref=r.delivery_artifact_ref('review:'+key),source_provider=r.provider_id('review-synthetic'),native_record=native,received_ts_utc=datetime(2026,10,20,12,39,59,tzinfo=UTC),ingestion_sequence=sequence,ingestion_sequence_scope=r.ingestion_sequence_scope('review-export'),source_temporal_kind='receipt_only',raw_signal_catalogue_ids=(r.RawSignalCatalogueId('R189'),),source_variant='review-depth',subject_instrument='review-CALL')
 raw.commands.admit_raw_observation_occurrence(observation('absent',1,{}))
 assert read(path)==[None,None]
 raw.commands.admit_raw_observation_occurrence(observation('present',2,{'price':Decimal('1.20')}))
 del raw
 before=hashlib.sha256(path.read_bytes()).hexdigest()
 child=subprocess.run([sys.executable,__file__,'read',str(path)],text=True,capture_output=True,check=True,env=dict(os.environ))
 actual=json.loads(child.stdout)
 expected=[None,{'native_type':'Decimal','value':'1.20','source_timestamp_raw':None}]
 assert actual==expected
 assert difference(expected,actual) is None
 altered=[None,{**actual[1],'value':'1.2'}]
 assert Decimal(actual[1]['value'])==Decimal(altered[1]['value'])
 witness=difference(expected,altered)
 assert witness is not None and witness['index']==1
 assert hashlib.sha256(path.read_bytes()).hexdigest()==before
 print('DIRECT_SEQUENCE_PASS',json.dumps({'missing_then_present':actual,'numeric_equal_scale_mismatch_rejected':True,'fresh_readonly_bytes_unchanged':True},sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='read':print(json.dumps(read(Path(sys.argv[2])),sort_keys=True))
 else:main()
