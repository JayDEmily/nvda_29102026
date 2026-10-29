from decimal import Decimal as D
from tests.product.derived_signal.test_m01_f4_approved_monetary_policy import fixture, hedge_fixture, ev, kv, budget, NOW
from nvda_desk.derived_signal_calculation_truth import api, _financial_policy as p
from nvda_desk.raw_signal_occurrence_truth import api as raw

f=fixture((D('.3'),D(0),D('.7'),D(0)))
f['params'].update(tail_fraction=D('.0001'),stress_active=False)
tail=dict(f['derived']['D162'][0].value);tail['CVaR_currency']=D(3)
f['derived']['D162']=(kv('D162',tuple(tail.items())),)
hf=hedge_fixture(f)
print('ROUNDING budget',dict(budget(f))['maximum_currency_exact'],'D189',ev('D189',hf))
try: p.hedge_adjustment(hf['derived'],hf['params'],hf['contexts'],NOW,NOW)
except ValueError as e: print(type(e).__name__,str(e))

f=fixture(); owner=api.create_owner(raw_projection_reader=raw.create_owner().reads,utc_now=lambda:NOW)
for did in ('D174','D162'):
    original=f['derived'][did][0]
    occurrence=api.DerivedSignalOccurrenceV1(did,did,'review-definition',(), 'NVDA',None,NOW,None,NOW,NOW,original.value,'structured','structured',(),(),())
    f['derived'][did]=(owner._occurrence_kernel_value(occurrence),)
    print('PROVENANCE',did,dict(f['derived'][did][0].metadata)['parameter_context_refs'],dict(f['derived'][did][0].metadata)['predecessor_occurrence_ids'])
result=ev('D175',f)
print('PROVENANCE typed metadata absent / named claims present -> budget',dict(result.value)['maximum_currency_exact'] if result else None)

from tests.product.derived_signal.test_m01_f4_approved_monetary_policy import action_fixture
from nvda_desk.derived_signal_calculation_truth import _catalogue
f=action_fixture()
x=f['derived']['D187'][0]
o=api.DerivedSignalOccurrenceV1('D187','D187','review',(),'NVDA',None,NOW,None,NOW,NOW,x.value,_catalogue.catalogue_row('D187').units,'scalar',(),(),())
f['derived']['D187']=(owner._occurrence_kernel_value(o),)
print('SCORE canonical persisted D187 units',o.units,'D192',ev('D192',f))
