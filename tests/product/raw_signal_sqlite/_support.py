"""Literal fixtures and process plumbing; expected answers live in the proof families."""

import base64
import importlib
import importlib.util
import pickle
import subprocess
import sys
from datetime import UTC, datetime
from decimal import Decimal

from nvda_desk.raw_signal_occurrence_truth import api

T0 = datetime(2026, 9, 20, 12, tzinfo=UTC)


def mechanism():
    name = "nvda_desk.raw_signal_occurrence_truth._sqlite"
    assert importlib.util.find_spec(name) is not None, "accepted M00 SQLite capability is missing"
    return importlib.import_module(name)


def owner(path, *, create=False, eligible=True, now=T0):
    port = mechanism().create_sqlite_persistence(str(path), create=create)
    return api.create_owner(
        durability_port=port,
        eligibility_resolver=lambda observation, policy: eligible,
        utc_now=lambda: now,
    )


def policy(**changes):
    values = dict(
        concept_id=api.concept_id("raw_signal.capture_scope_policy"),
        contract_id=api.contract_id("nvda.raw_signal.CaptureScopePolicy.v1"),
        units="not_applicable",
        scope_policy_id=api.scope_policy_id("policy"),
        scope_policy_version=1,
        activation_ts_utc=T0,
        eligibility_policy_ref=api.eligibility_policy_ref("eligibility/v1"),
    )
    return api.CaptureScopePolicyV1(**(values | changes))


def observation(identity="obs", sequence=1, scope="scope-A", native=None, **changes):
    values = dict(
        concept_id=api.concept_id("raw_signal.raw_observation_occurrence"),
        contract_id=api.contract_id("nvda.raw_signal.RawObservationOccurrence.v1"),
        observation_occurrence_id=api.observation_occurrence_id(identity),
        delivery_artifact_ref=api.delivery_artifact_ref("delivery"),
        source_provider=api.provider_id("controlled-provider"),
        native_record={"value": Decimal("1.00")} if native is None else native,
        received_ts_utc=T0,
        ingestion_sequence=sequence,
        ingestion_sequence_scope=api.ingestion_sequence_scope(scope),
        source_temporal_kind="receipt_only",
    )
    return api.RawObservationOccurrenceV1(**(values | changes))


def fresh_observation(path, identity):
    return fresh_record(path, "observation", identity)


def fresh_record(path, kind, identity, version=1):
    """Child gets only the selected file and lookup identity, never expected content."""
    code = """
import base64, pickle, sys
from nvda_desk.raw_signal_occurrence_truth import api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
o = api.create_owner(durability_port=create_sqlite_persistence(sys.argv[1]))
kind, identity = sys.argv[2:4]
if kind == "observation":
    r = o.reads.get_raw_observation_occurrence(api.observation_occurrence_id(identity))
elif kind == "policy":
    r = o.reads.get_capture_scope_policy(api.scope_policy_id(identity), int(sys.argv[4]))
elif kind == "capture":
    r = o.reads.get_scheduled_capture_occurrence(api.capture_occurrence_id(identity))
elif kind == "assessment":
    r = o.reads.get_receipt_presence_assessment(api.assessment_occurrence_id(identity))
elif kind == "chain":
    r = o.reads.list_receipt_presence_assessments(api.capture_occurrence_id(identity))
else:
    raise AssertionError("unknown read kind")
print(base64.b64encode(pickle.dumps(r)).decode("ascii"))
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(path), kind, identity, str(version)],
        env=process_env(),
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    # Trusted child under this proof's control; transport only, no expected-answer logic.
    return pickle.loads(base64.b64decode(result.stdout))


def process_env():
    import os
    from pathlib import Path

    return dict(os.environ, PYTHONPATH=str(Path(__file__).parent))
