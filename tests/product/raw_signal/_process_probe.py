"""Fresh-process probe for Raw Signal PostgreSQL proof.

The probe contains no Raw Signal outcome logic. It invokes the public production owner and
serialises observable committed facts for process-boundary comparison.
"""

from __future__ import annotations

import json
import os
import signal
import sys
from dataclasses import is_dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from tests.product.raw_signal._support import (  # noqa: E402
    admit_observation,
    append_assessment,
    as_mapping,
    build_owner,
    observation,
    policy,
    policy_ref,
    realise_capture,
    register_policy,
    typed_identity,
)


def _ids(token: str) -> dict[str, str]:
    return {
        "policy_id": f"scope::{token}",
        "capture_id": f"capture::{token}",
        "observation_id": f"observation::{token}",
        "fault_observation_id": f"observation-fault::{token}",
        "fault_capture_id": f"capture-fault::{token}",
        "delivery_id": f"delivery::{token}",
        "assessment_zero_id": f"assessment-zero::{token}",
        "assessment_one_id": f"assessment-one::{token}",
        "assessment_fault_id": f"assessment-fault::{token}",
        "assessment_retry_id": f"assessment-retry::{token}",
        "recovered_capture_id": f"recovered-capture::{token}",
        "recovered_assessment_id": f"recovered-assessment::{token}",
        "assessment_stale_id": f"assessment-stale::{token}",
        "capture_conflict_id": f"capture-conflict::{token}",
        "observation_high_same_scope_id": f"observation-high-same::{token}",
        "observation_low_same_scope_id": f"observation-low-same::{token}",
        "observation_low_other_scope_id": f"observation-low-other::{token}",
        "observation_next_same_scope_id": f"observation-next-same::{token}",
        "assessment_immediate_id": f"assessment-immediate::{token}",
    }


def _eligibility(_: Any, __: Any) -> bool:
    return True


def _owner(payload: dict[str, Any], **extra: Any) -> Any:
    return build_owner(
        postgres_dsn=payload["dsn"],
        eligibility_resolver=_eligibility,
        **extra,
    )


def _fact(payload: dict[str, Any], key: str, default: Any) -> Any:
    return payload.get("facts", {}).get(key, default)


def _parse_ts(value: str | None, default: datetime | None) -> datetime | None:
    if value is None:
        return default
    return datetime.fromisoformat(value)


def _policy(payload: dict[str, Any]) -> Any:
    token = payload["token"]
    ids = _ids(token)
    return policy(
        scope_policy_id=ids["policy_id"],
        activation_ts_utc=_parse_ts(
            _fact(payload, "activation_ts_utc", None),
            datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        ),
        deactivation_ts_utc=_parse_ts(
            _fact(payload, "deactivation_ts_utc", None),
            datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
        eligibility_policy_ref=_fact(
            payload, "eligibility_policy_ref", f"eligibility-lineage::{token}"
        ),
    )


def _observation(
    payload: dict[str, Any], *, fault: bool = False, native_record: Any = None
) -> Any:
    token = payload["token"]
    ids = _ids(token)
    default_observation_id = ids["fault_observation_id"] if fault else ids["observation_id"]
    observation_id = _fact(payload, "observation_occurrence_id", default_observation_id)
    return observation(
        observation_occurrence_id=observation_id,
        delivery_artifact_ref=_fact(payload, "delivery_artifact_ref", ids["delivery_id"]),
        source_provider=_fact(payload, "source_provider", f"provider::{token}"),
        native_identifier=_fact(payload, "native_identifier", f"native-id::{token}"),
        native_record=native_record
        if native_record is not None
        else _fact(
            payload,
            "native_record",
            {
                "Bid Price": f"bid::{token}",
                "Provider Null": None,
                "High Entropy": f"native-record::{token}",
            },
        ),
        source_product_api=_fact(payload, "source_product_api", f"product-api::{token}"),
        source_endpoint_callback=_fact(payload, "source_endpoint_callback", f"callback::{token}"),
        native_tick_series_identifier=_fact(
            payload, "native_tick_series_identifier", f"tick-series::{token}"
        ),
        source_variant=_fact(payload, "source_variant", f"variant::{token}"),
        subject_instrument=_fact(payload, "subject_instrument", f"NVDA::{token}"),
        native_units=_fact(payload, "native_units", f"USD::{token}"),
        availability_session=_fact(payload, "availability_session", f"regular::{token}"),
        source_status_native=_fact(payload, "source_status_native", f"published::{token}"),
        revision_vintage_native=_fact(payload, "revision_vintage_native", f"revision::{token}"),
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, 654321, tzinfo=UTC),
        received_epoch_ns=1_758_369_605_654_321_987,
        ingestion_sequence=_fact(payload, "ingestion_sequence", 41 if not fault else 42),
        ingestion_sequence_scope=_fact(payload, "ingestion_sequence_scope", f"collector::{token}"),
        source_temporal_kind="true_instant",
        source_timestamp_raw=_fact(payload, "source_timestamp_raw", "2026-09-20T12:00:04.123456Z"),
        source_timezone_native=_fact(payload, "source_timezone_native", f"UTC-native::{token}"),
        market_timezone_iana=_fact(payload, "market_timezone_iana", "America/New_York"),
        market_session_native=_fact(payload, "market_session_native", f"market-session::{token}"),
    )


def _normalise(value: Any) -> Any:
    if isinstance(value, datetime):
        return {"__datetime__": value.isoformat()}
    if isinstance(value, Enum):
        return {"__enum_type__": type(value).__qualname__, "value": _normalise(value.value)}
    if type(value) is not str and isinstance(value, str):
        return {"__identity_type__": type(value).__qualname__, "value": str(value)}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {
            str(key): _normalise(item)
            for key, item in sorted(value.items(), key=lambda x: str(x[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_normalise(item) for item in value]
    if hasattr(value, "model_dump") or is_dataclass(value) or hasattr(value, "__dict__"):
        return {key: _normalise(item) for key, item in sorted(as_mapping(value).items())}
    return {"__type__": type(value).__qualname__, "value": str(value)}



def _observe_public_method_return(method: Any, *args: Any, **kwargs: Any) -> Any:
    """Block at the Python public-method return event before caller-side result inspection.

    The profiler is proof-owned. It emits only a constant boundary marker while the returned
    object remains untouched, then waits for the parent proof process to inspect PostgreSQL
    state or kill this process before allowing caller execution to continue.
    """

    target = getattr(method, "__func__", method)
    code = getattr(target, "__code__", None)
    if code is None:
        raise AssertionError("public command must expose an inspectable Python return boundary")
    observed = False

    def profiler(frame: Any, event: str, arg: Any) -> Any:
        nonlocal observed
        if not observed and event == "return" and frame.f_code is code:
            observed = True
            print(
                json.dumps({"event": "public_method_return", "_pid": os.getpid()}),
                flush=True,
            )
            # Freeze the entire child process at the exact Python return event. A stdin
            # barrier would release the GIL and permit a background/lazy commit thread to
            # advance after the public command had already returned. SIGSTOP prevents every
            # thread in this process from running until the parent proof explicitly resumes it.
            os.kill(os.getpid(), signal.SIGSTOP)
        return profiler

    sys.setprofile(profiler)
    try:
        result = method(*args, **kwargs)
    finally:
        sys.setprofile(None)
    if not observed:
        raise AssertionError("public command return boundary was not observed")
    return result


def _policy_ref(token: str) -> Any:
    return policy_ref(f"scope::{token}", 1)



def boundary_write_policy(payload: dict[str, Any]) -> dict[str, Any]:
    owner = _owner(payload)
    value = _observe_public_method_return(
        owner.commands.register_capture_scope_policy, _policy(payload)
    )
    return {"record": _normalise(value)}


def boundary_write_capture(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    value = _observe_public_method_return(
        owner.commands.realise_scheduled_capture_occurrence,
        scope_policy_ref=_policy_ref(payload["token"]),
        capture_occurrence_id=typed_identity(
            "ScheduledCaptureOccurrenceV1", "capture_occurrence_id", ids["capture_id"]
        ),
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    return {"record": _normalise(value)}


def boundary_write_observation(payload: dict[str, Any]) -> dict[str, Any]:
    owner = _owner(payload)
    value = _observe_public_method_return(
        owner.commands.admit_raw_observation_occurrence, _observation(payload)
    )
    return {"record": _normalise(value)}


def boundary_write_zero_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    value = _observe_public_method_return(
        owner.commands.append_capture_receipt_presence_assessment,
        assessment_occurrence_id=typed_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "assessment_occurrence_id",
            ids["assessment_zero_id"],
        ),
        capture_occurrence_ref=typed_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "capture_occurrence_ref",
            ids["capture_id"],
        ),
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, 111111, tzinfo=UTC),
        supersedes_assessment_ref=None,
    )
    return {"record": _normalise(value)}


def boundary_write_one_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    value = _observe_public_method_return(
        owner.commands.append_capture_receipt_presence_assessment,
        assessment_occurrence_id=typed_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "assessment_occurrence_id",
            ids["assessment_one_id"],
        ),
        capture_occurrence_ref=typed_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "capture_occurrence_ref",
            ids["capture_id"],
        ),
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, 222222, tzinfo=UTC),
        supersedes_assessment_ref=typed_identity(
            "CaptureReceiptPresenceAssessmentV1",
            "supersedes_assessment_ref",
            ids["assessment_zero_id"],
        ),
    )
    return {"record": _normalise(value)}


def write_policy_only(payload: dict[str, Any]) -> dict[str, Any]:
    stored = register_policy(_owner(payload), _policy(payload))
    return {"record": _normalise(stored)}


def read_policy(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_capture_scope_policy(
        _policy(payload).scope_policy_id, 1
    )
    return {"record": _normalise(stored), "policy_id": ids["policy_id"]}


def write_capture_only(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = realise_capture(
        _owner(payload),
        scope_policy_ref=_policy_ref(payload["token"]),
        capture_occurrence_id=ids["capture_id"],
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    return {"record": _normalise(stored)}


def read_capture(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_scheduled_capture_occurrence(ids["capture_id"])
    return {"record": _normalise(stored)}


def write_observation_only(payload: dict[str, Any]) -> dict[str, Any]:
    stored = admit_observation(_owner(payload), _observation(payload))
    return {"record": _normalise(stored)}


def read_observation(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_raw_observation_occurrence(ids["observation_id"])
    return {"record": _normalise(stored)}


def retry_observation(payload: dict[str, Any]) -> dict[str, Any]:
    stored = admit_observation(_owner(payload), _observation(payload))
    return {"record": _normalise(stored)}


def conflict_observation(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        admit_observation(
            _owner(payload),
            _observation(payload, native_record={"Bid Price": "conflict"}),
        )
    except (TypeError, ValueError):
        return {"rejected": True}
    raise AssertionError("conflicting durable same-ID observation was accepted")


def write_zero_assessment_only(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = append_assessment(
        _owner(payload),
        assessment_occurrence_id=ids["assessment_zero_id"],
        capture_occurrence_ref=ids["capture_id"],
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, 111111, tzinfo=UTC),
    )
    return {"record": _normalise(stored)}


def write_relation_and_one_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    token = payload["token"]
    ids = _ids(token)
    owner = _owner(payload)
    capture = owner.reads.get_scheduled_capture_occurrence(ids["capture_id"])
    obs = owner.reads.get_raw_observation_occurrence(ids["observation_id"])
    zero = owner.reads.get_receipt_presence_assessment(ids["assessment_zero_id"])
    relation = owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=obs.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )
    assert relation is not None
    stored = append_assessment(
        owner,
        assessment_occurrence_id=ids["assessment_one_id"],
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, 222222, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    return {"record": _normalise(stored), "relation": _normalise(relation)}


def derive_relation_only(payload: dict[str, Any]) -> dict[str, Any]:
    token = payload["token"]
    ids = _ids(token)
    owner = _owner(payload)
    capture = owner.reads.get_scheduled_capture_occurrence(ids["capture_id"])
    obs = owner.reads.get_raw_observation_occurrence(ids["observation_id"])
    relation = owner.commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=obs.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )
    assert relation is not None
    return {"relation": _normalise(relation)}


def write_one_assessment_only(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    zero = owner.reads.get_receipt_presence_assessment(ids["assessment_zero_id"])
    stored = append_assessment(
        owner,
        assessment_occurrence_id=ids["assessment_one_id"],
        capture_occurrence_ref=ids["capture_id"],
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 25, 222222, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    return {"record": _normalise(stored)}


def read_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    which = payload.get("which", "zero")
    assessment_id = ids["assessment_zero_id"] if which == "zero" else ids["assessment_one_id"]
    stored = _owner(payload).reads.get_receipt_presence_assessment(assessment_id)
    return {"record": _normalise(stored)}


def read_assessment_chain(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    chain = _owner(payload).reads.list_receipt_presence_assessments(ids["capture_id"])
    return {"records": [_normalise(item) for item in chain]}




def retry_zero_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = append_assessment(
        _owner(payload),
        assessment_occurrence_id=ids["assessment_zero_id"],
        capture_occurrence_ref=ids["capture_id"],
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, 111111, tzinfo=UTC),
    )
    return {"record": _normalise(stored)}


def conflict_zero_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    try:
        append_assessment(
            _owner(payload),
            assessment_occurrence_id=ids["assessment_zero_id"],
            capture_occurrence_ref=ids["capture_id"],
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 11, 111111, tzinfo=UTC),
        )
    except (TypeError, ValueError, KeyError):
        return {"rejected": True}
    return {"rejected": False}


def fault_capture(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload, fault_mode="fail_before_commit")
    try:
        realise_capture(
            owner,
            scope_policy_ref=_policy_ref(payload["token"]),
            capture_occurrence_id=ids["fault_capture_id"],
            slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        )
    except Exception:
        return {"failed": True, "capture_id": ids["fault_capture_id"]}
    raise AssertionError("proof fault injection did not interrupt the capture transaction")


def read_fault_capture_absent(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_scheduled_capture_occurrence(ids["fault_capture_id"])
    return {"absent": stored is None}


def fault_observation(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload, fault_mode="fail_before_commit")
    try:
        admit_observation(owner, _observation(payload, fault=True))
    except Exception:
        return {"failed": True, "observation_id": ids["fault_observation_id"]}
    raise AssertionError("proof fault injection did not interrupt the observation transaction")


def read_fault_observation_absent(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_raw_observation_occurrence(ids["fault_observation_id"])
    return {"absent": stored is None}


def fault_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload, fault_mode="fail_before_commit")
    try:
        append_assessment(
            owner,
            assessment_occurrence_id=ids["assessment_fault_id"],
            capture_occurrence_ref=ids["capture_id"],
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 27, tzinfo=UTC),
            supersedes_assessment_ref=ids["assessment_one_id"],
        )
    except Exception:
        return {"failed": True, "assessment_id": ids["assessment_fault_id"]}
    raise AssertionError("proof fault injection did not interrupt the assessment transaction")


def read_fault_assessment_absent(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    stored = _owner(payload).reads.get_receipt_presence_assessment(ids["assessment_fault_id"])
    return {"absent": stored is None}


def write_policy_for_reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    return write_policy_only(payload)


def reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    result = owner.commands.reconcile_owed_slots(
        scope_policy_ref=_policy_ref(payload["token"]),
        slot_starts_utc=[datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        capture_occurrence_ids=[ids["recovered_capture_id"]],
        assessment_occurrence_ids=[ids["recovered_assessment_id"]],
    )
    assessment = owner.reads.get_receipt_presence_assessment(ids["recovered_assessment_id"])
    return {"count": len(result), "assessment": _normalise(assessment)}


def reconcile_fault_after_capture(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload, fault_mode="fail_after_occurrence_commit")
    try:
        owner.commands.reconcile_owed_slots(
            scope_policy_ref=_policy_ref(payload["token"]),
            slot_starts_utc=[datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
            capture_occurrence_ids=[ids["recovered_capture_id"]],
            assessment_occurrence_ids=[ids["recovered_assessment_id"]],
        )
    except Exception:
        return {"failed": True}
    raise AssertionError("reconcile fault did not stop after capture commit")


def read_reconcile(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    capture = owner.reads.get_scheduled_capture_occurrence(ids["recovered_capture_id"])
    assessment = owner.reads.get_receipt_presence_assessment(ids["recovered_assessment_id"])
    return {"capture": _normalise(capture), "assessment": _normalise(assessment)}




def reregister_policy_conflict(payload: dict[str, Any]) -> dict[str, Any]:
    token = payload["token"]
    owner = _owner(payload)
    changed = policy(
        scope_policy_id=_ids(token)["policy_id"],
        activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        eligibility_policy_ref=f"changed-eligibility::{token}",
    )
    try:
        register_policy(owner, changed)
    except (TypeError, ValueError):
        return {"rejected": True}
    return {"rejected": False}


def realise_conflicting_capture_for_existing_slot(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    try:
        value = realise_capture(
            owner,
            scope_policy_ref=_policy_ref(payload["token"]),
            capture_occurrence_id=ids["capture_conflict_id"],
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )
    except (TypeError, ValueError):
        return {"rejected": True}
    return {
        "rejected": False,
        "capture_id": str(value.capture_occurrence_id),
        "original_id": ids["capture_id"],
    }


def append_stale_predecessor_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    owner = _owner(payload)
    try:
        append_assessment(
            owner,
            assessment_occurrence_id=ids["assessment_stale_id"],
            capture_occurrence_ref=ids["capture_id"],
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 28, tzinfo=UTC),
            supersedes_assessment_ref=ids["assessment_zero_id"],
        )
    except (TypeError, ValueError, KeyError):
        return {"rejected": True}
    return {"rejected": False}




def admit_high_sequence_same_scope(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    value = admit_observation(
        _owner(payload),
        _observation(
            {
                **payload,
                "facts": {
                    **payload.get("facts", {}),
                    "observation_occurrence_id": ids["observation_high_same_scope_id"],
                    "ingestion_sequence": 42,
                },
            }
        ),
    )
    return {"record": _normalise(value)}


def append_immediate_predecessor_assessment(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    value = append_assessment(
        _owner(payload),
        assessment_occurrence_id=ids["assessment_immediate_id"],
        capture_occurrence_ref=ids["capture_id"],
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 27, tzinfo=UTC),
        supersedes_assessment_ref=ids["assessment_one_id"],
    )
    return {"record": _normalise(value)}


def admit_low_sequence_same_scope(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    try:
        admit_observation(
            _owner(payload),
            _observation(
                {
                    **payload,
                    "facts": {
                        **payload.get("facts", {}),
                        "observation_occurrence_id": ids["observation_low_same_scope_id"],
                        "ingestion_sequence": 40,
                    },
                }
            ),
        )
    except (TypeError, ValueError):
        return {"rejected": True}
    return {"rejected": False}


def admit_low_sequence_other_scope(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    value = admit_observation(
        _owner(payload),
        _observation(
            {
                **payload,
                "facts": {
                    **payload.get("facts", {}),
                    "observation_occurrence_id": ids["observation_low_other_scope_id"],
                    "ingestion_sequence": 1,
                    "ingestion_sequence_scope": f"independent-scope::{payload['token']}",
                },
            }
        ),
    )
    return {"record": _normalise(value)}



def admit_next_sequence_same_scope(payload: dict[str, Any]) -> dict[str, Any]:
    ids = _ids(payload["token"])
    value = admit_observation(
        _owner(payload),
        _observation(
            {
                **payload,
                "facts": {
                    **payload.get("facts", {}),
                    "observation_occurrence_id": ids["observation_next_same_scope_id"],
                    "ingestion_sequence": 43,
                },
            }
        ),
    )
    return {"record": _normalise(value)}


def filesystem_boundary(payload: dict[str, Any]) -> dict[str, Any]:
    host_path = Path(payload["host_path"])
    try:
        host_path.write_text("should-not-write", encoding="utf-8")
    except OSError:
        blocked = True
    else:
        blocked = False
        host_path.unlink(missing_ok=True)

    ephemeral = Path("/run/proof-tmp/nvda-proof-ephemeral")
    ephemeral.write_text("ephemeral", encoding="utf-8")

    writable_mounts: list[dict[str, str]] = []
    rootfs = os.environ["NVDA_PROOF_ROOTFS"]
    for line in Path("/run/proof-mountinfo").read_text(encoding="utf-8").splitlines():
        pre, post = line.split(" - ", 1)
        fields = pre.split()
        mount_target = fields[4]
        if mount_target != rootfs and not mount_target.startswith(rootfs + "/"):
            continue
        options = fields[5].split(",")
        if "rw" not in options:
            continue
        target = mount_target[len(rootfs) :] or "/"
        writable_mounts.append({"target": target, "filesystem": post.split()[0]})
    return {
        "host_write_blocked": blocked,
        "ephemeral_write_ok": ephemeral.exists(),
        "writable_mounts": writable_mounts,
    }


ACTIONS = {
    "boundary_write_policy": boundary_write_policy,
    "boundary_write_capture": boundary_write_capture,
    "boundary_write_observation": boundary_write_observation,
    "boundary_write_zero_assessment": boundary_write_zero_assessment,
    "boundary_write_one_assessment": boundary_write_one_assessment,
    "write_policy_only": write_policy_only,
    "read_policy": read_policy,
    "write_capture_only": write_capture_only,
    "read_capture": read_capture,
    "write_observation_only": write_observation_only,
    "read_observation": read_observation,
    "retry_observation": retry_observation,
    "conflict_observation": conflict_observation,
    "write_zero_assessment_only": write_zero_assessment_only,
    "write_relation_and_one_assessment": write_relation_and_one_assessment,
    "derive_relation_only": derive_relation_only,
    "write_one_assessment_only": write_one_assessment_only,
    "read_assessment": read_assessment,
    "read_assessment_chain": read_assessment_chain,
    "retry_zero_assessment": retry_zero_assessment,
    "conflict_zero_assessment": conflict_zero_assessment,
    "fault_capture": fault_capture,
    "read_fault_capture_absent": read_fault_capture_absent,
    "fault_observation": fault_observation,
    "read_fault_observation_absent": read_fault_observation_absent,
    "fault_assessment": fault_assessment,
    "read_fault_assessment_absent": read_fault_assessment_absent,
    "write_policy_for_reconcile": write_policy_for_reconcile,
    "reconcile": reconcile,
    "reconcile_fault_after_capture": reconcile_fault_after_capture,
    "read_reconcile": read_reconcile,
    "reregister_policy_conflict": reregister_policy_conflict,
    "realise_conflicting_capture_for_existing_slot": realise_conflicting_capture_for_existing_slot,
    "append_stale_predecessor_assessment": append_stale_predecessor_assessment,
    "append_immediate_predecessor_assessment": append_immediate_predecessor_assessment,
    "admit_high_sequence_same_scope": admit_high_sequence_same_scope,
    "admit_low_sequence_same_scope": admit_low_sequence_same_scope,
    "admit_low_sequence_other_scope": admit_low_sequence_other_scope,
    "admit_next_sequence_same_scope": admit_next_sequence_same_scope,
    "filesystem_boundary": filesystem_boundary,
}


def main() -> None:
    first_line = sys.stdin.readline()
    payload = json.loads(first_line)
    result = {**ACTIONS[payload["action"]](payload), "_pid": os.getpid()}
    print(json.dumps(result, sort_keys=True), flush=True)
    if payload.get("hold_open"):
        release = sys.stdin.readline().strip()
        if release != "release":
            raise RuntimeError("hold-open probe exited without explicit release")


if __name__ == "__main__":
    main()
