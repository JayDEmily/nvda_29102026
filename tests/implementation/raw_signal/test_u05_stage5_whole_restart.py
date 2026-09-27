from __future__ import annotations

import functools
import inspect
from datetime import UTC, datetime
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    admit_observation,
    append_assessment,
    build_owner,
    copy_with,
    observation,
    policy,
    realise_capture,
    register_policy,
    required_symbol,
)

from nvda_desk.raw_signal_occurrence_truth._postgres import create_postgres_persistence

_FIXED_NOW = datetime(2026, 9, 20, 12, 5, tzinfo=UTC)


def _dsn() -> str:
    import os

    value = os.environ.get("NVDA_TEST_POSTGRES_DSN")
    if not value:
        pytest.fail("NVDA_TEST_POSTGRES_DSN is required for Stage-5 real PostgreSQL proof")
    return value


def _fresh_owner(*, eligible: bool = True) -> Any:
    return build_owner(
        durability_port=create_postgres_persistence(_dsn()),
        eligibility_resolver=lambda _observation, _policy: eligible,
        utc_now=lambda: _FIXED_NOW,
    )


@pytest.fixture(autouse=True)
def _clean_stage5_tables() -> None:
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


def _policy_id(value: str) -> Any:
    return required_symbol("scope_policy_id")(value)


def _policy_ref(value: str) -> Any:
    return required_symbol("scope_policy_ref")(value)


def _capture_id(value: str) -> Any:
    return required_symbol("capture_occurrence_id")(value)


def _observation_id(value: str) -> Any:
    return required_symbol("observation_occurrence_id")(value)


def _assessment_id(value: str) -> Any:
    return required_symbol("assessment_occurrence_id")(value)


def _ordinary_object_graph_contains(root: Any, target: Any) -> bool:
    """Traverse the accepted ordinary attribute/slot graph, not function internals."""

    pending = [root]
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if current is target:
            return True
        if inspect.ismethod(current) and current.__self__ is target:
            return True

        marker = id(current)
        if marker in seen:
            continue
        seen.add(marker)

        if isinstance(current, functools.partial):
            pending.append(current.func)
            pending.extend(current.args)
            pending.extend((current.keywords or {}).values())
            continue
        if callable(current):
            # Accepted U02 review explicitly excludes arbitrary function-closure introspection.
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


def test_stage5_ordinary_owner_graph_does_not_expose_postgresql_mutation_capability() -> None:
    port = create_postgres_persistence(_dsn())

    class NameMangledCanary:
        __slots__ = ("__port",)

        def __init__(self, value: Any) -> None:
            self.__port = value

    # Prove this discriminator sees the exact private-slot shape that defeated the earlier helper.
    assert _ordinary_object_graph_contains(NameMangledCanary(port), port)

    owner = build_owner(
        durability_port=port,
        eligibility_resolver=lambda _observation, _policy: True,
        utc_now=lambda: _FIXED_NOW,
    )
    assert not _ordinary_object_graph_contains(owner, port)
    for facet in (owner, owner.commands, owner.reads):
        assert not hasattr(facet, "transaction")


def test_stage5_whole_u05_restart_composes_all_restart_sensitive_semantics() -> None:
    policy_value = policy(
        scope_policy_id="stage5-policy",
        activation_ts_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        deactivation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        eligibility_policy_ref="stage5-eligibility-v1",
    )
    stored_policy = register_policy(_fresh_owner(), policy_value)

    # Fresh process-local state must recover policy identity, content and the complete policy set
    # needed for overlap decisions.
    restarted = _fresh_owner()
    assert restarted.reads.get_capture_scope_policy(_policy_id("stage5-policy"), 1) == stored_policy
    assert register_policy(restarted, policy_value) == stored_policy
    with pytest.raises(ValueError, match="must not overlap"):
        register_policy(
            _fresh_owner(),
            policy(
                scope_policy_id="stage5-overlap",
                activation_ts_utc=datetime(2026, 9, 20, 12, 1, tzinfo=UTC),
                deactivation_ts_utc=datetime(2026, 9, 20, 12, 3, tzinfo=UTC),
            ),
        )

    capture = realise_capture(
        _fresh_owner(),
        scope_policy_ref="stage5-policy@1",
        capture_occurrence_id="stage5-capture",
        slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
    )
    assert (
        realise_capture(
            _fresh_owner(),
            scope_policy_ref="stage5-policy@1",
            capture_occurrence_id="stage5-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )
        == capture
    )
    with pytest.raises(ValueError, match="different capture identity"):
        realise_capture(
            _fresh_owner(),
            scope_policy_ref="stage5-policy@1",
            capture_occurrence_id="stage5-other-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        )
    with pytest.raises(ValueError, match="different owed slot"):
        realise_capture(
            _fresh_owner(),
            scope_policy_ref="stage5-policy@1",
            capture_occurrence_id="stage5-capture",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        )

    # Establish the pre-observation U04 state, discard the owner, and preserve that exact assessment
    # when evidence is admitted later.
    zero = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage5-assessment-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 2, tzinfo=UTC),
    )
    assert zero.outcome == "zero_received"

    observed = observation(
        observation_occurrence_id="stage5-observation-a10",
        delivery_artifact_ref="stage5-delivery",
        source_provider="stage5-provider",
        native_identifier="stage5-native-id",
        native_record={"exact_int": 1, "exact_float": 1.0, "null": None},
        received_ts_utc=datetime(2026, 9, 20, 12, 0, 5, tzinfo=UTC),
        ingestion_sequence=10,
        ingestion_sequence_scope="stage5-scope-a",
    )
    stored_observation = admit_observation(_fresh_owner(), observed)
    assert admit_observation(_fresh_owner(), observed) == stored_observation
    with pytest.raises(ValueError, match="different content"):
        admit_observation(
            _fresh_owner(),
            copy_with(observed, native_record={"exact_int": 1.0, "exact_float": 1.0, "null": None}),
        )

    # Durable ingestion sequence ordering remains exact-scope local after repeated owner loss.
    admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage5-observation-b1",
            ingestion_sequence=1,
            ingestion_sequence_scope="stage5-scope-b",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 6, tzinfo=UTC),
        ),
    )
    with pytest.raises(ValueError, match="must not decrease"):
        admit_observation(
            _fresh_owner(),
            observation(
                observation_occurrence_id="stage5-observation-a9",
                ingestion_sequence=9,
                ingestion_sequence_scope="stage5-scope-a",
                received_ts_utc=datetime(2026, 9, 20, 12, 0, 7, tzinfo=UTC),
            ),
        )
    admitted_higher = admit_observation(
        _fresh_owner(),
        observation(
            observation_occurrence_id="stage5-observation-a11",
            ingestion_sequence=11,
            ingestion_sequence_scope="stage5-scope-a",
            received_ts_utc=datetime(2026, 9, 20, 12, 0, 8, tzinfo=UTC),
        ),
    )
    assert admitted_higher.ingestion_sequence == 11

    # Relation materialisation is optional. A fresh owner re-derives it directly from durable facts.
    relation = _fresh_owner().commands.derive_capture_receipt_evidence_relation(
        observation_occurrence_ref=stored_observation.observation_occurrence_id,
        capture_occurrence_ref=capture.capture_occurrence_id,
        scope_policy_ref=capture.scope_policy_ref,
    )
    assert relation is not None
    assert relation.observation_occurrence_ref == stored_observation.observation_occurrence_id
    assert relation.capture_occurrence_ref == capture.capture_occurrence_id
    assert relation.scope_policy_ref == capture.scope_policy_ref

    # Same assessment ID remains the original zero despite later evidence. A new assessment derives
    # one-or-more from durable evidence and supersedes only the immediate durable predecessor.
    retried_zero = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage5-assessment-zero",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 2, tzinfo=UTC),
    )
    assert retried_zero == zero

    one = append_assessment(
        _fresh_owner(),
        assessment_occurrence_id="stage5-assessment-one",
        capture_occurrence_ref=capture.capture_occurrence_id,
        evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 10, tzinfo=UTC),
        supersedes_assessment_ref=zero.assessment_occurrence_id,
    )
    assert one.outcome == "one_or_more_received"
    assert one.supersedes_assessment_ref == zero.assessment_occurrence_id

    with pytest.raises(ValueError, match="immediately prior"):
        append_assessment(
            _fresh_owner(),
            assessment_occurrence_id="stage5-assessment-stale",
            capture_occurrence_ref=capture.capture_occurrence_id,
            evidence_as_of_ts_utc=datetime(2026, 9, 20, 12, 0, 12, tzinfo=UTC),
            supersedes_assessment_ref=zero.assessment_occurrence_id,
        )

    # Existing owed-slot reconciliation returns the durable current chain head without creating a
    # second capture or a fabricated unknown. A missing owed slot is captured first, then separately
    # assessed unknown_not_established as required by the non-cross-kind-atomic U05 contract.
    existing = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("stage5-policy@1"),
        [datetime(2026, 9, 20, 12, 0, tzinfo=UTC)],
        [_capture_id("stage5-capture")],
        [_assessment_id("stage5-unused-reconcile-assessment")],
    )
    assert tuple(existing) == (one,)

    missing = _fresh_owner().commands.reconcile_owed_slots(
        _policy_ref("stage5-policy@1"),
        [datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC)],
        [_capture_id("stage5-reconciled-capture")],
        [_assessment_id("stage5-reconciled-assessment")],
    )
    assert len(missing) == 1
    assert missing[0].outcome == "unknown_not_established"
    assert missing[0].supersedes_assessment_ref is None
    assert missing[0].evidence_as_of_ts_utc == _FIXED_NOW

    # One last completely fresh owner must recover every original semantic family with exact lineage
    # and schedule context intact and no caller-managed semantic hydration.
    reader = _fresh_owner()
    assert reader.reads.get_capture_scope_policy(_policy_id("stage5-policy"), 1) == stored_policy
    assert reader.reads.get_scheduled_capture_occurrence(_capture_id("stage5-capture")) == capture
    assert (
        reader.reads.get_raw_observation_occurrence(_observation_id("stage5-observation-a10"))
        == stored_observation
    )
    assert reader.reads.get_receipt_presence_assessment(
        _assessment_id("stage5-assessment-zero")
    ) == zero
    assert reader.reads.get_receipt_presence_assessment(
        _assessment_id("stage5-assessment-one")
    ) == one
    assert tuple(reader.reads.list_receipt_presence_assessments(_capture_id("stage5-capture"))) == (
        zero,
        one,
    )

    reconciled_capture = reader.reads.get_scheduled_capture_occurrence(
        _capture_id("stage5-reconciled-capture")
    )
    assert reconciled_capture is not None
    assert reconciled_capture.scope_policy_ref == _policy_ref("stage5-policy@1")
    assert reconciled_capture.slot_start_utc == datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC)
    assert reader.reads.get_receipt_presence_assessment(
        _assessment_id("stage5-reconciled-assessment")
    ) == missing[0]
    assert reader.reads.get_receipt_presence_assessment(
        _assessment_id("stage5-unused-reconcile-assessment")
    ) is None
