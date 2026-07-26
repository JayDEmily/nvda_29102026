from __future__ import annotations
import importlib.util, sys
from pathlib import Path


def load(path: Path):
    name='nvda_desk.m13_state_kernel'
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError(path)
    mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod

source=Path(sys.argv[1])
m=load(source)
a=m.InMemoryUnitOfWork(initial_state={'a':0})
b=m.InMemoryUnitOfWork(initial_state={'b':0})
key_a=m.IdempotencyKey('key-a','command-a','unit-a')
key_b=m.IdempotencyKey('key-b','command-b','unit-b')
cmd_a=m.TransactionCommand('cmd-a',key_a,'a'*64,0,'policy-a')
cmd_b=m.TransactionCommand('cmd-b',key_b,'b'*64,0,'policy-b')

def mutate_b(state):
    state['b'] += 1
    return {'receipt_id':'receipt-b','result_id':'result-b'}

def mutate_a(state):
    state['a'] += 1
    inner=b.execute(command=cmd_b, mutation=mutate_b)
    assert inner.receipt_id == 'receipt-b'
    return {'receipt_id':'receipt-a','result_id':'result-a'}

outer=a.execute(command=cmd_a, mutation=mutate_a)
assert outer.receipt_id == 'receipt-a'
assert a.snapshot_state() == {'a':1}
assert b.snapshot_state() == {'b':1}
assert [r.sequence for r in a.list_receipts()] == [1]
assert [r.sequence for r in b.list_receipts()] == [1]
print('two_instance_independence=PASS')
