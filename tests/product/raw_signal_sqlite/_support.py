"""Literal fixtures and process plumbing; expected answers live in the proof families."""

import importlib
import importlib.util
import json
import subprocess
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from struct import pack

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


def representation(value):
    """Independent native representation oracle, deliberately not the production codec."""
    if isinstance(value, Mapping):
        return ["mapping", [[key, representation(value[key])] for key in sorted(value)]]
    if type(value) is Decimal:
        t = value.as_tuple()
        return ["decimal", t.sign, list(t.digits), str(t.exponent)]
    if type(value) is float:
        return ["float", pack("!d", value).hex()]
    if type(value) is bytes:
        return ["bytes", value.hex()]
    if type(value) in (tuple, list):
        return [type(value).__name__, [representation(item) for item in value]]
    return [type(value).__name__, str(value)]


def fresh_observation(path, identity):
    """Child gets only the selected file and lookup identity, never expected content."""
    code = """
import json, sys
from nvda_desk.raw_signal_occurrence_truth import api
from nvda_desk.raw_signal_occurrence_truth._sqlite import create_sqlite_persistence
from _support import representation
o = api.create_owner(durability_port=create_sqlite_persistence(sys.argv[1]))
r = o.reads.get_raw_observation_occurrence(api.observation_occurrence_id(sys.argv[2]))
print(json.dumps(None if r is None else {
    "native": representation(r.native_record), "provider": r.source_provider.value,
    "delivery": r.delivery_artifact_ref.value, "kind": r.source_temporal_kind,
    "source_timestamp_raw": r.source_timestamp_raw, "sequence": str(r.ingestion_sequence),
    "scope": r.ingestion_sequence_scope.value, "receipt": r.received_ts_utc.isoformat(),
    "epoch": None if r.received_epoch_ns is None else str(r.received_epoch_ns),
    "revision": r.revision_vintage_native, "timezone": r.source_timezone_native,
}))
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(path), identity],
        env=process_env(),
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def process_env():
    import os
    from pathlib import Path

    return dict(os.environ, PYTHONPATH=str(Path(__file__).parent))
