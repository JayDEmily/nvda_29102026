"""Fresh-process probe for Raw Signal PostgreSQL proof.

This helper contains no product decisions. It invokes the same public production factory and
fixed proof specimens used by the ordinary product tests, then reports only observable results.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from tests.product.raw_signal._support import (  # noqa: E402
    admit_observation,
    append_assessment,
    build_owner,
    observation,
    policy,
    realise_capture,
    register_policy,
)


def _ids(token: str) -> dict[str, str]:
    return {
        "policy_id": f"scope-{token}",
        "policy_ref": f"scope-{token}@1",
        "capture_id": f"capture-{token}",
        "observation_id": f"observation-{token}",
        "delivery_id": f"delivery-{token}",
        "assessment_zero_id": f"assessment-zero-{token}",
        "assessment_one_id": f"assessment-one-{token}",
        "recovered_capture_id": f"recovered-capture-{token}",
        "recovered_assessment_id": f"recovered-assessment-{token}",
    }


def _owner(payload: dict[str, Any], **extra: Any) -> Any:
    return build_owner(postgres_dsn=payload["dsn"], **extra)


def _policy(token: str) -> Any:
    ids = _ids(token)
    return policy(scope_policy_id=ids["policy_id"])


def _observation(token: str, *, native_record: dict[str, Any] | None = None) -> Any:
    ids = _ids(token)
    return observation(
        observation_occurrence_id=ids["observation_id"],
        delivery_artifact_ref=ids["delivery_id"],
        native_identifier=f"native-{token}",
        native_record=native_record,
        ingestion_sequence_scope=f"collector-{token}",
    )


def write_core(payload: dict[str, Any]) -> dict[str, Any]:
    token = payload["token"]
    ids = _ids(token)
    owner = _owner(payload)
    stored_policy = register_policy(owner, _policy(token))
    capture = realise_capture(
        owner,
        scope_policy_ref=ids["policy_ref"],
        capture_occurrence_id=ids["capture_id"],
    )
    obs = admit_observation(owner, _observation(token))
    return {
        "policy_id": stored_policy.scope_policy_id,
        "capture_id": capture.capture_occurrence_id,
        "observation_id": obs.observation_occurrence_id,
    }


def read_core(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    stored_policy = owner.reads.get_capture_scope_policy(ids["policy_id"], 1)
    capture = owner.reads.get_scheduled_capture_occurrence(ids["capture_id"])
    obs = owner.reads.get_raw_observation_occurrence(ids["observation_id"])
    return {
        "policy": stored_policy is not None,
        "capture": capture is not None,
        "observation": obs is not None,
        "observation_id": None if obs is None else obs.observation_occurrence_id,
    }


def retry_observation(payload: dict[str, Any]) -> dict[str, Any]:
    obs = admit_observation(_owner(payload), _observation(payload["token"]))
    return {"observation_id": obs.observation_occurrence_id}


def conflict_observation(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        admit_observation(
            _owner(payload),
            _observation(payload["token"], native_record={"Bid Price": "999.00"}),
        )
    except (TypeError, ValueError):
        return {"rejected": True}
    raise AssertionError("conflicting durable same-ID observation was accepted")


def write_assessment_chain(payload: dict[str, Any]) -> dict[str, Any]:
    token = payload["token"]
    ids = _ids(token)
    owner = _owner(payload)
    register_policy(owner, _policy(token))
    capture = realise_capture(
        owner,
        scope_policy_ref=ids["policy_ref"],
        capture_occurrence_id=ids["capture_id"],
    )
    zero = append_assessment(
        owner,
        assessment_occurrence_id=ids["assessment_zero_id"],
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
    )
    obs = admit_observation(
        owner,
        observation(
            observation_occurrence_id=ids["observation_id"],
            delivery_artifact_ref=ids["delivery_id"],
            native_identifier=f"native-{token}",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 20, tzinfo=UTC),
            ingestion_sequence=2,
            ingestion_sequence_scope=f"collector-{token}",
        ),
    )
    relation = owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=obs.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )
    assert relation is not None
    one = append_assessment(
        owner,
        assessment_occurrence_id=ids["assessment_one_id"],
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    return {"zero": zero.outcome, "one": one.outcome}


def read_assessment_chain(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    chain = owner.reads.list_receipt_presence_assessments(ids["capture_id"])
    return {
        "ids": [item.assessment_occurrence_id for item in chain],
        "outcomes": [item.outcome for item in chain],
        "supersedes": [item.supersedes_assessment_ref for item in chain],
    }


def fault_write(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload, fault_mode="fail_before_commit")
    try:
        admit_observation(owner, _observation(payload["token"]))
    except Exception:
        return {"failed": True, "observation_id": ids["observation_id"]}
    raise AssertionError("proof fault injection did not interrupt the transaction")


def read_absent(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    return {
        "absent": owner.reads.get_raw_observation_occurrence(ids["observation_id"]) is None
    }


def write_policy(payload: dict[str, Any]) -> dict[str, Any]:
    value = register_policy(_owner(payload), _policy(payload["token"]))
    return {"policy_id": value.scope_policy_id}


def reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    result = owner.commands.reconcile_owed_slots(
        scope_policy_ref=ids["policy_ref"],
        slot_starts_utc=[datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        capture_occurrence_ids=[ids["recovered_capture_id"]],
        assessment_occurrence_ids=[ids["recovered_assessment_id"]],
    )
    assessment = owner.reads.get_receipt_presence_assessment(ids["recovered_assessment_id"])
    return {"count": len(result), "outcome": assessment.outcome}


def read_reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    capture = owner.reads.get_scheduled_capture_occurrence(ids["recovered_capture_id"])
    assessment = owner.reads.get_receipt_presence_assessment(ids["recovered_assessment_id"])
    return {
        "capture": capture is not None,
        "assessment": assessment is not None,
        "outcome": None if assessment is None else assessment.outcome,
    }


ACTIONS = {
    "write_core": write_core,
    "read_core": read_core,
    "retry_observation": retry_observation,
    "conflict_observation": conflict_observation,
    "write_assessment_chain": write_assessment_chain,
    "read_assessment_chain": read_assessment_chain,
    "fault_write": fault_write,
    "read_absent": read_absent,
    "write_policy": write_policy,
    "reconcile": reconcile,
    "read_reconcile": read_reconcile,
}


def main() -> None:
    payload = json.loads(sys.stdin.read())
    action = payload["action"]
    result = {**ACTIONS[action](payload), "_pid": os.getpid()}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
