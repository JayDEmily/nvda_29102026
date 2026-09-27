from __future__ import annotations

import functools
import gc
import os
from datetime import UTC, datetime
from typing import Any

import pytest
from tests.product.raw_signal._support import observation, policy, policy_ref

import nvda_desk.composition as composition
from nvda_desk.raw_signal_occurrence_truth import api
from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence


def _dsn() -> str:
    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for U06 Stage-3 PostgreSQL proof")
    return value


@pytest.fixture(autouse=True)
def _clean_semantic_store() -> None:
    psycopg = pytest.importorskip("psycopg")
    assert psycopg.__version__ == "3.3.4"
    create_postgres_persistence(_dsn())
    with psycopg.connect(_dsn()) as connection:
        connection.execute(
            "TRUNCATE rsot_capture_receipt_presence_assessment_v1, "
            "rsot_raw_observation_occurrence_v1, "
            "rsot_scheduled_capture_occurrence_v1, "
            "rsot_capture_scope_policy_v1 CASCADE"
        )
        connection.commit()


def _durable_counts() -> tuple[int, int, int, int]:
    psycopg = pytest.importorskip("psycopg")
    with psycopg.connect(_dsn()) as connection:
        return tuple(
            connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            for table in (
                "rsot_capture_scope_policy_v1",
                "rsot_scheduled_capture_occurrence_v1",
                "rsot_raw_observation_occurrence_v1",
                "rsot_capture_receipt_presence_assessment_v1",
            )
        )


class _EligibilityAuthority:
    def __init__(self) -> None:
        self.calls: list[tuple[Any, Any]] = []

    def __call__(self, raw_observation: Any, effective_policy: Any) -> bool:
        self.calls.append((raw_observation, effective_policy))
        return True


def _ordinary_graph_has_transaction_capability(root: Any) -> bool:
    pending = [root]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        marker = id(current)
        if marker in seen:
            continue
        seen.add(marker)

        if hasattr(current, "transaction"):
            return True
        if isinstance(current, functools.partial):
            pending.append(current.func)
            pending.extend(current.args)
            pending.extend((current.keywords or {}).values())
            continue
        if callable(current):
            continue
        if isinstance(current, dict):
            pending.extend(current.keys())
            pending.extend(current.values())
            continue
        if isinstance(current, (list, tuple, set, frozenset)):
            pending.extend(current)
            continue

        namespace = getattr(current, "__dict__", None)
        if isinstance(namespace, dict):
            pending.extend(namespace.values())

        for owner_type in type(current).__mro__:
            declared = vars(owner_type).get("__slots__", ())
            slot_names = (declared,) if isinstance(declared, str) else declared
            for slot in slot_names:
                if slot in {"__dict__", "__weakref__"}:
                    continue
                resolved = slot
                if slot.startswith("__") and not slot.endswith("__"):
                    resolved = f"_{owner_type.__name__.lstrip('_')}{slot}"
                missing = object()
                child = getattr(current, resolved, missing)
                if child is not missing:
                    pending.append(child)
    return False


def _sequence_inputs() -> dict[str, Any]:
    return {
        "capture_scope_policy": policy(
            scope_policy_id="u06-stage3-policy",
            eligibility_policy_ref="u06-stage3-eligibility-v1",
        ),
        "scope_policy_ref": policy_ref("u06-stage3-policy", 1),
        "slot_start_utc": datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        "capture_occurrence_id": api.capture_occurrence_id("u06-stage3-capture"),
        "raw_observation": observation(
            observation_occurrence_id="u06-stage3-observation",
            delivery_artifact_ref="u06-stage3-delivery",
            ingestion_sequence_scope="u06-stage3-ingestion",
            ingestion_sequence=1,
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, 123456, tzinfo=UTC),
        ),
        "assessment_occurrence_id": api.assessment_occurrence_id("u06-stage3-assessment"),
        "assessment_evidence_as_of_ts_utc": datetime(
            2026, 9, 20, 12, 0, 10, 777777, tzinfo=UTC
        ),
        "supersedes_assessment_ref": None,
    }


def test_production_factory_composes_real_postgresql_m00_sequence_end_to_end() -> None:
    eligibility = _EligibilityAuthority()
    inputs = _sequence_inputs()
    app = composition.create_application(
        postgres_dsn=_dsn(),
        raw_signal_eligibility_resolver=eligibility,
    )

    result = app.run_raw_signal_proof_sequence(**inputs)

    assert result.policy == inputs["capture_scope_policy"]
    assert result.capture.capture_occurrence_id == inputs["capture_occurrence_id"]
    assert result.capture.scope_policy_ref == inputs["scope_policy_ref"]
    assert result.observation == inputs["raw_observation"]
    assert result.relation is not None
    assert (
        result.relation.observation_occurrence_ref
        == result.observation.observation_occurrence_id
    )
    assert result.relation.capture_occurrence_ref == result.capture.capture_occurrence_id
    assert result.relation.scope_policy_ref == result.capture.scope_policy_ref
    assert result.assessment.capture_occurrence_ref == result.capture.capture_occurrence_id
    assert result.assessment.outcome == "one_or_more_received"
    assert result.readback == result.observation
    assert eligibility.calls
    assert all(call[0] == result.observation for call in eligibility.calls)
    assert all(call[1] == result.policy for call in eligibility.calls)
    assert _durable_counts() == (1, 1, 1, 1)

    # A fresh production application must resolve the same durable identities and keep row counts
    # stable on exact retry; this cannot be satisfied by process-local owner state alone.
    restarted_eligibility = _EligibilityAuthority()
    restarted = composition.create_application(
        postgres_dsn=_dsn(),
        raw_signal_eligibility_resolver=restarted_eligibility,
    )
    retry = restarted.run_raw_signal_proof_sequence(**inputs)
    assert retry == result
    assert _durable_counts() == (1, 1, 1, 1)

    # A00 does not expose the PostgreSQL transaction capability through its ordinary object graph.
    assert not _ordinary_graph_has_transaction_capability(app)
    assert not _ordinary_graph_has_transaction_capability(restarted)

    del app
    del restarted
    gc.collect()
    assert _durable_counts() == (1, 1, 1, 1)
