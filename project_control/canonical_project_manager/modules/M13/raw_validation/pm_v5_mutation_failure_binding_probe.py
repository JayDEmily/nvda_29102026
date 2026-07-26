from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

source = Path(sys.argv[1])
spec = spec_from_file_location('nvda_desk.m13_state_kernel', source)
mod = module_from_spec(spec)
sys.modules['nvda_desk.m13_state_kernel'] = mod
spec.loader.exec_module(mod)

key = mod.IdempotencyKey(value='idem-1', command_type='position_reconciliation', consistency_unit_id='position-1')
failed = mod.TransactionCommand(command_id='command-1', idempotency_key=key, input_fingerprint='a'*64, expected_state_version=0, policy_version='transaction-v1')
fresh = mod.TransactionCommand(command_id='command-2', idempotency_key=key, input_fingerprint='b'*64, expected_state_version=0, policy_version='transaction-v1')
boundary = mod.InMemoryUnitOfWork(initial_state={'count': 0})

def fail_mutation(state):
    state['count'] = 99
    raise RuntimeError('mutation failed')

def succeed(state):
    state['count'] += 1
    return {'receipt_id': 'receipt-2', 'result_id': 'result-2'}

try:
    boundary.execute(command=failed, mutation=fail_mutation)
except Exception as exc:
    print(f'attempt_1=failed:{type(exc).__name__}:{exc}')
print(f'after_failure_state_version={boundary.state_version}')
print(f'after_failure_state={boundary.snapshot_state()}')
print(f'after_failure_receipts={boundary.list_receipts()}')
try:
    receipt = boundary.execute(command=fresh, mutation=succeed)
    print(f'different_input_retry=committed:sequence={receipt.sequence}:command_id={receipt.command_id}')
except Exception as exc:
    print(f'different_input_retry=failed:{type(exc).__name__}:{exc}')
print(f'final_state_version={boundary.state_version}')
print(f'final_state={boundary.snapshot_state()}')
print(f'final_receipts={boundary.list_receipts()}')
