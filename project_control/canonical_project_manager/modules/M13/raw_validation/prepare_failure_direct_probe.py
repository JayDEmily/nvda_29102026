from __future__ import annotations

from copy import deepcopy

from mutant_register_after_prepare_source import (
    IdempotencyKey,
    InMemoryUnitOfWork,
    RepositoryPort,
    TransactionCommand,
)


class PrepareFailureParticipant(RepositoryPort):
    def __init__(self) -> None:
        self.visible: list[object] = []
        self.pending: object | None = None
        self.prepare_calls = 0
        self.commit_calls = 0
        self.rollback_calls = 0

    def prepare(self, *, command, working_state, receipt) -> None:
        self.prepare_calls += 1
        if self.pending is not None:
            raise RuntimeError("stale pending transaction survived failed prepare")
        self.pending = {
            "command_id": command.command_id,
            "state": deepcopy(working_state),
            "state_version": receipt.resulting_state_version,
            "sequence": receipt.sequence,
        }
        raise RuntimeError("participant prepare failed")

    def commit(self) -> None:
        self.commit_calls += 1
        self.visible.append(deepcopy(self.pending))
        self.pending = None

    def rollback(self) -> None:
        self.rollback_calls += 1
        self.pending = None


participant = PrepareFailureParticipant()
boundary = InMemoryUnitOfWork(
    initial_state={"count": 0},
    repository_ports=(participant,),
)
key = IdempotencyKey(
    value="idem-1",
    command_type="position_reconciliation",
    consistency_unit_id="position-1",
)
command = TransactionCommand(
    command_id="command-1",
    idempotency_key=key,
    input_fingerprint="a" * 64,
    expected_state_version=0,
    policy_version="transaction-v1",
)


def mutate(state):
    state["count"] += 1
    return {"receipt_id": "receipt-1", "result_id": "result-1"}


outcomes: list[str] = []
for attempt in (1, 2):
    try:
        boundary.execute(command=command, mutation=mutate)
    except RuntimeError as exc:
        outcomes.append(f"attempt_{attempt}=failed:{exc}")
    else:
        outcomes.append(f"attempt_{attempt}=unexpected_success")

for outcome in outcomes:
    print(outcome)
print(f"prepare_calls={participant.prepare_calls}")
print(f"commit_calls={participant.commit_calls}")
print(f"rollback_calls={participant.rollback_calls}")
print(f"pending={participant.pending is not None}")
print(f"participant_visible={participant.visible!r}")
print(f"state_version={boundary.state_version}")
print(f"state={boundary.snapshot_state()!r}")
print(f"receipts={boundary.list_receipts()!r}")

assert outcomes == [
    "attempt_1=failed:participant prepare failed",
    "attempt_2=failed:stale pending transaction survived failed prepare",
]
assert participant.prepare_calls == 2
assert participant.commit_calls == 0
assert participant.rollback_calls == 0
assert participant.pending is not None
assert participant.visible == []
assert boundary.state_version == 0
assert boundary.snapshot_state() == {"count": 0}
assert boundary.list_receipts() == ()
print("M13_PREPARE_FAILURE_FALSE_POSITIVE_REPRODUCED")
