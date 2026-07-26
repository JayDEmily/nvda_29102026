from __future__ import annotations
import argparse, importlib.util, sys
from pathlib import Path

parser=argparse.ArgumentParser(); parser.add_argument('source'); args=parser.parse_args()
source=Path(args.source)
spec=importlib.util.spec_from_file_location('candidate', source); assert spec and spec.loader
m=importlib.util.module_from_spec(spec); sys.modules['candidate']=m; spec.loader.exec_module(m)

class Participant(m.RepositoryPort):
    def __init__(self):
        self.fail=True; self.pending=None; self.rollback_calls=0
    def prepare(self, *, command, working_state, receipt):
        self.pending=(command.command_id, working_state.copy(), receipt.sequence)
        if self.fail:
            raise RuntimeError('prepare failed')
    def commit(self): self.pending=None
    def rollback(self): self.rollback_calls += 1; self.pending=None

key=m.IdempotencyKey(value='idem-1', command_type='position_reconciliation', consistency_unit_id='position-1')
first=m.TransactionCommand(command_id='command-1', idempotency_key=key, input_fingerprint='a'*64, expected_state_version=0, policy_version='transaction-v1')
second=m.TransactionCommand(command_id='command-2', idempotency_key=key, input_fingerprint='b'*64, expected_state_version=0, policy_version='transaction-v1')
p=Participant(); uow=m.InMemoryUnitOfWork(initial_state={'count':0}, repository_ports=(p,))

def mutate(state):
    state['count'] += 1
    return {'receipt_id':'receipt-1','result_id':'result-1'}

try:
    uow.execute(command=first, mutation=mutate)
except Exception as exc:
    print(f'attempt_1=failed:{exc}')
print(f'after_failure_rollback_calls={p.rollback_calls}')
print(f'after_failure_pending={p.pending!r}')
print(f'after_failure_state_version={uow.state_version}')
print(f'after_failure_receipts={uow.list_receipts()!r}')
p.fail=False
try:
    receipt=uow.execute(command=second, mutation=mutate)
    print(f'different_input_retry=committed:sequence={receipt.sequence}:command_id={receipt.command_id}')
except Exception as exc:
    print(f'different_input_retry=failed:{type(exc).__name__}:{exc}')
print(f'final_state_version={uow.state_version}')
print(f'final_state={uow.snapshot_state()!r}')
print(f'final_receipts={uow.list_receipts()!r}')
