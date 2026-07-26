from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
source=Path(sys.argv[1]); spec=spec_from_file_location('nvda_desk.m13_state_kernel',source); mod=module_from_spec(spec); sys.modules['nvda_desk.m13_state_kernel']=mod; spec.loader.exec_module(mod)
class P(mod.RepositoryPort):
    def __init__(self): self.fail=True; self.pending=None
    def prepare(self, *, command, working_state, receipt):
        self.pending=command.command_id
        if self.fail: raise RuntimeError('prepare failed')
    def commit(self): self.pending=None
    def rollback(self): self.pending=None
key=mod.IdempotencyKey(value='idem-1',command_type='position_reconciliation',consistency_unit_id='position-1')
failed=mod.TransactionCommand(command_id='command-1',idempotency_key=key,input_fingerprint='a'*64,expected_state_version=0,policy_version='transaction-v1')
corrected=mod.TransactionCommand(command_id='command-1',idempotency_key=key,input_fingerprint='b'*64,expected_state_version=0,policy_version='transaction-v1')
p=P(); b=mod.InMemoryUnitOfWork(initial_state={'count':0},repository_ports=(p,))
def mutate(state): state['count']+=1; return {'receipt_id':'receipt-2','result_id':'result-2'}
try: b.execute(command=failed,mutation=mutate)
except Exception as e: print(f'attempt_1=failed:{type(e).__name__}:{e}')
p.fail=False
try:
 r=b.execute(command=corrected,mutation=mutate); print(f'corrected_same_command_id=committed:sequence={r.sequence}')
except Exception as e: print(f'corrected_same_command_id=failed:{type(e).__name__}:{e}')
print(f'state_version={b.state_version}')
print(f'receipts={b.list_receipts()}')
