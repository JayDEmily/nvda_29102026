import base64, pickle, sys
from pathlib import Path
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal, localcontext, Inexact, Rounded
from _support import configuration, observation, mapping, request, NOW, ASOF
from nvda_desk.market_measurement_truth import api as f
from nvda_desk.raw_signal_occurrence_truth import api as r
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
root=Path(sys.argv[1]); root.mkdir(exist_ok=True)
raw=r.create_owner(durability_port=create_sqlite_persistence(str(root/'raw.sqlite'),create=True))
clock=[NOW]
config=configuration(raw.reads, root/'ratio.sqlite',now=lambda:clock[0])
owner=f.create_raw_ratio_owner(**config)
req=request()
def hist():
 return owner.reads.list_derived_history(derived_signal_id='D014',subject_instrument='NVDA',effective_at_or_before_utc=clock[0],knowledge_at_or_before_utc=clock[0],limit=1000)
assert hist()==() and owner.materialise(req) is None and hist()==()
assert raw.reads.project_raw_value(r.RawSignalCatalogueId('R033'),r.observation_occurrence_id('mmt-size-bid-001'),mappings=(mapping('bid'),)) is None
for side,val in [('bid','2.50'),('ask','1.25')]:
 raw.commands.admit_raw_observation_occurrence(observation(side,value=Decimal(val)))
 p=raw.reads.project_raw_value(r.RawSignalCatalogueId('R033' if side=='bid' else 'R036'),r.observation_occurrence_id('mmt-size-'+side+'-001'),mappings=(mapping(side),))
 assert type(p) is r.ProjectedRawValueV1 and p.native_value.as_tuple()==Decimal(val).as_tuple()
with localcontext() as ctx:
 ctx.prec=1; ctx.traps[Inexact]=ctx.traps[Rounded]=True
 first=owner.materialise(req)
assert first.result==f.ExactRatioV1(1,3) and first.calculated_at_utc==NOW
assert [x.projection.native_value.as_tuple() for x in first.raw_input_lineage]==[Decimal('2.50').as_tuple(),Decimal('1.25').as_tuple()]
clock[0]+=timedelta(days=1)
assert owner.materialise(req)==first and hist()==(first,)
# Refusals after a real persisted first fact, each preserving the populated history.
for bad in [replace(req,derived_signal_id='D013'),replace(req,raw_input_bindings=tuple(reversed(req.raw_input_bindings))),replace(req,context_refs=(f.VersionRefV1('other',1),))]:
 assert owner.materialise(bad) is None and hist()==(first,)
# Each legal configuration dimension changes alone; mixed mapping/unit versions remain lawful.
variants=[replace(req,calculation_definition_version='D014-SIZE-IMBALANCE-2'),replace(req,parameter_set_ref=f.VersionRefV1('mmt-size-basic',2)),replace(req,input_selection_policy_ref=f.VersionRefV1('mmt-size-selection',2))]
for index in [0,1]:
 for field,ref in [('unit_convention_ref',f.VersionRefV1('mmt-size-shares',2)),('projection_mapping_ref',f.VersionRefV1('mmt-size-'+('bid' if index==0 else 'ask'),2))]:
  bindings=list(req.raw_input_bindings); bindings[index]=replace(bindings[index],**{field:ref}); variants.append(replace(req,raw_input_bindings=tuple(bindings)))
facts=[first]
for changed in variants:
 fact=owner.materialise(changed)
 assert type(fact) is f.RawRatioOccurrenceV1 and fact.result==f.ExactRatioV1(1,3)
 assert fact.derived_occurrence_id not in [x.derived_occurrence_id for x in facts]
 assert owner.materialise(changed)==fact
 facts.append(fact)
# Actual public duplicate projection page, changed representation, invalid after good.
class ConflictingReader:
 def list_projected_raw_history(self,rid,**kw):
  page=raw.reads.list_projected_raw_history(rid,**kw)
  if rid.value=='R033':
   p=page.items[0]
   return replace(page,items=(p,replace(p,native_value=Decimal('2.500'))))
  return page
bad_owner=f.create_raw_ratio_owner(**(config|dict(raw_projection_reader=ConflictingReader(),storage=f.SQLiteStorageV1(str(root/'ratio.sqlite'),False))))
before=hist(); assert bad_owner.materialise(req) is None and hist()==before
# Signed out-of-range result is artificial algebra; no physical-validity inference.
other=r.create_owner(durability_port=create_sqlite_persistence(str(root/'signed-raw.sqlite'),create=True))
for side,val in [('bid','-3'),('ask','1')]:other.commands.admit_raw_observation_occurrence(observation(side,value=Decimal(val)))
signed=f.create_raw_ratio_owner(**configuration(other.reads,root/'signed-ratio.sqlite'))
assert signed.materialise(req).result==f.ExactRatioV1(2,1)
# Only literal/config records from support: all semantic operations above are explicit.
bundle=dict(facts=tuple(facts),definitions=config['definitions'],parameters=config['parameter_sets'],policies=config['input_selection_policies'],units=config['unit_conventions'],mappings=config['raw_projection_mappings'],history=hist())
print(base64.b64encode(pickle.dumps(bundle)).decode())
