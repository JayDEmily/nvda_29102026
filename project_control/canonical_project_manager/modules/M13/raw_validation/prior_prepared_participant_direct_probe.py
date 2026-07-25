from __future__ import annotations

import importlib.util
import sys
from copy import deepcopy
from pathlib import Path

SOURCE = Path(__file__).with_name('mutant_rollback_only_failing_prepare_participant_source.py')
name = 'nvda_desk.m13_state_kernel'
spec = importlib.util.spec_from_file_location(name, SOURCE)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[name] = m
spec.loader.exec_module(m)

class Participant(m.RepositoryPort):
    def __init__(self, label: str, fail_first_prepare: bool = False) -> None:
        self.label = label
        self.fail_first_prepare = fail_first_prepare
        self.pending = None
        self.visible = []
        self.prepare_calls = 0
        self.commit_calls = 0
        self.rollback_calls = 0

    def prepare(self, *, command, working_state, receipt) -> None:
        self.prepare_calls += 1
        if self.pending is not None:
            raise RuntimeError(f'{self.label}: stale pending transaction survived failed prepare')
        self.pending = {
            'command_id': command.command_id,
            'state': deepcopy(working_state),
            'sequence': receipt.sequence,
        }
        if self.fail_first_prepare and self.prepare_calls == 1:
            raise RuntimeError(f'{self.label}: participant prepare failed')

    def commit(self) -> None:
        self.commit_calls += 1
        self.visible.append(deepcopy(self.pending))
        self.pending = None

    def rollback(self) -> None:
        self.rollback_calls += 1
        self.pending = None

first = Participant('first')
second = Participant('second', fail_first_prepare=True)
boundary = m.InMemoryUnitOfWork(initial_state={'count': 0}, repository_ports=(first, second))
key = m.IdempotencyKey(value='idem-1', command_type='position_reconciliation', consistency_unit_id='position-1')
command = m.TransactionCommand(
    command_id='command-1', idempotency_key=key, input_fingerprint='a'*64,
    expected_state_version=0, policy_version='transaction-v1'
)

def mutate(state):
    state['count'] += 1
    return {'receipt_id':'receipt-1','result_id':'result-1'}

try:
    boundary.execute(command=command, mutation=mutate)
    print('attempt_1=unexpected_success')
except RuntimeError as exc:
    print(f'attempt_1=failed:{exc}')

first_pending_after_attempt_1 = deepcopy(first.pending)
first_rollback_calls_after_attempt_1 = first.rollback_calls
second_pending_after_attempt_1 = deepcopy(second.pending)
second_rollback_calls_after_attempt_1 = second.rollback_calls
print(f'first_pending_after_attempt_1={first_pending_after_attempt_1!r}')
print(f'first_rollback_calls_after_attempt_1={first_rollback_calls_after_attempt_1}')
print(f'second_pending_after_attempt_1={second_pending_after_attempt_1!r}')
print(f'second_rollback_calls_after_attempt_1={second_rollback_calls_after_attempt_1}')

try:
    boundary.execute(command=command, mutation=mutate)
    print('attempt_2=unexpected_success')
except RuntimeError as exc:
    print(f'attempt_2=failed:{exc}')

print(f'first_prepare_calls={first.prepare_calls}')
print(f'first_commit_calls={first.commit_calls}')
print(f'first_rollback_calls={first.rollback_calls}')
print(f'first_pending={first.pending!r}')
print(f'first_visible={first.visible!r}')
print(f'second_prepare_calls={second.prepare_calls}')
print(f'second_commit_calls={second.commit_calls}')
print(f'second_rollback_calls={second.rollback_calls}')
print(f'second_pending={second.pending!r}')
print(f'second_visible={second.visible!r}')
print(f'state_version={boundary.state_version}')
print(f'state={boundary.snapshot_state()!r}')
print(f'receipts={boundary.list_receipts()!r}')

assert first_pending_after_attempt_1 is not None, first_pending_after_attempt_1
assert first_rollback_calls_after_attempt_1 == 0, first_rollback_calls_after_attempt_1
assert second_pending_after_attempt_1 is None, second_pending_after_attempt_1
assert second_rollback_calls_after_attempt_1 == 1, second_rollback_calls_after_attempt_1
assert first.rollback_calls == 1, first.rollback_calls  # only on poisoned retry, not first failure
assert second.rollback_calls == 1, second.rollback_calls
assert first.commit_calls == 0 and second.commit_calls == 0
assert boundary.state_version == 0
assert boundary.snapshot_state() == {'count': 0}
assert boundary.list_receipts() == ()
print('M13_PRIOR_PREPARED_PARTICIPANT_FALSE_POSITIVE_REPRODUCED')
