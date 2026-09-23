from __future__ import annotations

from datetime import UTC, datetime, timedelta
from operator import attrgetter
from typing import Any

import pytest
from tests.product.raw_signal._support import (
    build_owner,
    copy_with,
    policy,
    policy_ref,
    realise_capture,
    register_policy,
    typed_identity,
)


def test_public_facets_do_not_expose_mutable_owner_semantic_state() -> None:
    owner = build_owner()
    original = register_policy(owner)

    for facet in (owner.commands, owner.reads):
        assert not hasattr(facet, "_state")

        pending = [facet]
        seen: set[int] = set()
        while pending:
            current = pending.pop()
            marker = id(current)
            if marker in seen:
                continue
            seen.add(marker)

            if callable(current):
                continue
            assert not isinstance(current, (dict, list, set))

            namespace = getattr(current, "__dict__", None)
            if isinstance(namespace, dict):
                pending.extend(namespace.values())

            for cls in type(current).__mro__:
                slots = getattr(cls, "__slots__", ())
                if isinstance(slots, str):
                    slots = (slots,)
                for slot in slots:
                    if slot in {"__dict__", "__weakref__"}:
                        continue
                    resolved = slot
                    if slot.startswith("__") and not slot.endswith("__"):
                        resolved = f"_{cls.__name__.lstrip('_')}{slot}"
                    missing = object()
                    child = getattr(current, resolved, missing)
                    if child is not missing:
                        pending.append(child)

    reread = owner.reads.get_capture_scope_policy(
        original.scope_policy_id, original.scope_policy_version
    )
    assert reread == original


def test_reviewer023_direct_state_bypass_is_closed() -> None:
    owner = build_owner()
    original = register_policy(owner)

    overlapping = policy(
        scope_policy_version=2,
        activation_ts_utc=datetime(2026, 9, 20, 12, 1, tzinfo=UTC),
        deactivation_ts_utc=None,
    )
    with pytest.raises((TypeError, ValueError)):
        register_policy(owner, overlapping)

    state_getter = attrgetter("_state")
    with pytest.raises(AttributeError):
        state_getter(owner.commands)
    with pytest.raises(AttributeError):
        state_getter(owner.reads)

    assert owner.reads.get_capture_scope_policy(
        original.scope_policy_id, original.scope_policy_version
    ) == original
    assert owner.reads.get_capture_scope_policy(
        overlapping.scope_policy_id, overlapping.scope_policy_version
    ) is None


def test_exact_half_minute_slots_are_owed_inside_active_policy() -> None:
    owner = build_owner()
    register_policy(owner)
    first = realise_capture(owner, slot_start_utc=datetime(2026, 9, 20, 12, 0, tzinfo=UTC))
    second = realise_capture(
        owner,
        slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        capture_occurrence_id="capture-002",
    )
    assert first.slot_end_utc - first.slot_start_utc == timedelta(seconds=30)
    assert second.slot_end_utc - second.slot_start_utc == timedelta(seconds=30)
    assert first.slot_start_utc.second == 0
    assert second.slot_start_utc.second == 30
    assert str(first.scope_policy_ref) == str(second.scope_policy_ref) == "scope-policy-001@1"


@pytest.mark.parametrize(
    "slot",
    [
        datetime(2026, 9, 20, 11, 59, 30, tzinfo=UTC),
        datetime(2026, 9, 20, 12, 2, 0, tzinfo=UTC),
        datetime(2026, 9, 20, 12, 0, 15, tzinfo=UTC),
    ],
)
def test_before_activation_at_deactivation_and_unaligned_slots_fail(slot: datetime) -> None:
    owner = build_owner()
    register_policy(owner)
    with pytest.raises((TypeError, ValueError)):
        realise_capture(owner, slot_start_utc=slot)


@pytest.mark.parametrize(
    "slot",
    [
        datetime(2026, 9, 20, 12, 0, 0, 1, tzinfo=UTC),
        datetime(2026, 9, 20, 12, 0, 29, 999999, tzinfo=UTC),
        datetime(2026, 9, 20, 12, 0, 30, 1, tzinfo=UTC),
        datetime(2026, 9, 20, 12, 1, 59, 999999, tzinfo=UTC),
    ],
)
def test_capture_slot_grid_rejects_one_microsecond_off_exact_boundaries(slot: datetime) -> None:
    owner = build_owner()
    register_policy(owner)
    with pytest.raises((TypeError, ValueError)):
        realise_capture(owner, slot_start_utc=slot)


def test_scheduler_wake_time_cannot_become_schedule_truth() -> None:
    owner = build_owner()
    register_policy(owner)
    with pytest.raises((TypeError, ValueError)):
        realise_capture(
            owner,
            scheduler_wake_ts_utc=datetime(2026, 9, 20, 12, 0, 7, tzinfo=UTC),
        )


def test_same_slot_retry_reuses_existing_capture_identity() -> None:
    owner = build_owner()
    register_policy(owner)
    first = realise_capture(owner, capture_occurrence_id="capture-001")
    second = realise_capture(owner, capture_occurrence_id="capture-001")
    assert second.capture_occurrence_id == first.capture_occurrence_id
    assert second == first


def test_stable_policy_slot_key_cannot_admit_second_capture_identity() -> None:
    owner = build_owner()
    register_policy(owner)
    first = realise_capture(owner, capture_occurrence_id="capture-001")
    try:
        second = realise_capture(owner, capture_occurrence_id="capture-second-id")
    except (TypeError, ValueError):
        return
    assert second.capture_occurrence_id == first.capture_occurrence_id


def test_conflicting_reuse_of_capture_identity_fails_closed() -> None:
    owner = build_owner()
    register_policy(owner)
    realise_capture(owner, capture_occurrence_id="capture-001")
    with pytest.raises((TypeError, ValueError)):
        realise_capture(
            owner,
            capture_occurrence_id="capture-001",
            slot_start_utc=datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        )


def test_missing_policy_authority_cannot_create_owed_slot() -> None:
    owner = build_owner()
    with pytest.raises((TypeError, ValueError, KeyError)):
        realise_capture(owner)


def test_policy_version_boundary_is_non_overlapping_and_does_not_rewrite_history() -> None:
    owner = build_owner()
    register_policy(owner)
    earlier = realise_capture(owner, capture_occurrence_id="capture-v1")
    register_policy(
        owner,
        policy(
            scope_policy_version=2,
            activation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
            deactivation_ts_utc=None,
        ),
    )
    assert owner.reads.get_scheduled_capture_occurrence(earlier.capture_occurrence_id) == earlier
    assert str(earlier.scope_policy_ref) == "scope-policy-001@1"


def test_overlapping_policy_versions_fail_closed() -> None:
    owner = build_owner()
    register_policy(owner)
    with pytest.raises((TypeError, ValueError)):
        register_policy(
            owner,
            policy(
                scope_policy_version=2,
                activation_ts_utc=datetime(2026, 9, 20, 12, 1, tzinfo=UTC),
                deactivation_ts_utc=None,
            ),
        )


def _policy_conflict(field: str) -> Any:
    changes: dict[str, Any] = {
        "activation_ts_utc": datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
        "deactivation_ts_utc": datetime(2026, 9, 20, 12, 1, 30, tzinfo=UTC),
        "eligibility_policy_ref": typed_identity(
            "CaptureScopePolicyV1", "eligibility_policy_ref", "eligibility-policy:changed:v1"
        ),
    }
    return copy_with(policy(), **{field: changes[field]})


@pytest.mark.parametrize(
    "field", ["activation_ts_utc", "deactivation_ts_utc", "eligibility_policy_ref"]
)
def test_same_policy_identity_and_version_cannot_be_reregistered_with_changed_content(
    field: str,
) -> None:
    owner = build_owner()
    original = register_policy(owner, policy())
    with pytest.raises((TypeError, ValueError)):
        register_policy(owner, _policy_conflict(field))
    reread = owner.reads.get_capture_scope_policy(
        original.scope_policy_id, original.scope_policy_version
    )
    assert reread == original


def test_identical_policy_reregistration_is_idempotent_or_rejected_without_mutation() -> None:
    owner = build_owner()
    original_value = policy()
    original = register_policy(owner, original_value)
    try:
        retry = register_policy(owner, original_value)
    except (TypeError, ValueError):
        retry = None
    if retry is not None:
        assert retry == original
    reread = owner.reads.get_capture_scope_policy(
        original.scope_policy_id, original.scope_policy_version
    )
    assert reread == original


def test_absent_deactivation_is_preserved_as_absence() -> None:
    owner = build_owner()
    value = policy(deactivation_ts_utc=None)
    stored = register_policy(owner, value)
    assert stored.deactivation_ts_utc is None
    assert not getattr(stored, "perpetual_service", False)


@pytest.mark.parametrize(
    ("activation", "deactivation"),
    [
        (
            datetime(2026, 9, 20, 12, 0, 15, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        ),
        (
            datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 2, 15, tzinfo=UTC),
        ),
        (
            datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        ),
        (
            datetime(2026, 9, 20, 12, 0, 30, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 0, tzinfo=UTC),
        ),
    ],
)
def test_policy_validity_timestamps_are_aligned_and_strictly_ordered(
    activation: datetime, deactivation: datetime
) -> None:
    owner = build_owner()
    with pytest.raises((TypeError, ValueError)):
        register_policy(
            owner,
            policy(
                activation_ts_utc=activation,
                deactivation_ts_utc=deactivation,
            ),
        )


@pytest.mark.parametrize(
    ("activation", "deactivation"),
    [
        (
            datetime(2026, 9, 20, 12, 0, 0, 1, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 2, 0, tzinfo=UTC),
        ),
        (
            datetime(2026, 9, 20, 12, 0, 0, tzinfo=UTC),
            datetime(2026, 9, 20, 12, 2, 0, 1, tzinfo=UTC),
        ),
    ],
)
def test_policy_grid_rejects_one_microsecond_off_activation_or_deactivation(
    activation: datetime, deactivation: datetime
) -> None:
    owner = build_owner()
    with pytest.raises((TypeError, ValueError)):
        register_policy(
            owner,
            policy(activation_ts_utc=activation, deactivation_ts_utc=deactivation),
        )


def test_v2_owns_first_slot_at_activation_boundary_and_v1_stops_before_it() -> None:
    owner = build_owner()
    register_policy(owner, policy())
    v1_last = realise_capture(
        owner,
        scope_policy_ref=policy_ref("scope-policy-001", 1),
        capture_occurrence_id="capture-v1-last",
        slot_start_utc=datetime(2026, 9, 20, 12, 1, 30, tzinfo=UTC),
    )
    register_policy(
        owner,
        policy(
            scope_policy_version=2,
            activation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
            deactivation_ts_utc=None,
        ),
    )
    v2_first = realise_capture(
        owner,
        scope_policy_ref=policy_ref("scope-policy-001", 2),
        capture_occurrence_id="capture-v2-first",
        slot_start_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
    )
    assert str(v1_last.scope_policy_ref) == "scope-policy-001@1"
    assert str(v2_first.scope_policy_ref) == "scope-policy-001@2"
    with pytest.raises((TypeError, ValueError)):
        realise_capture(
            owner,
            scope_policy_ref=policy_ref("scope-policy-001", 1),
            capture_occurrence_id="capture-v1-illegal-boundary",
            slot_start_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
        )
    with pytest.raises((TypeError, ValueError)):
        realise_capture(
            owner,
            scope_policy_ref=policy_ref("scope-policy-001", 2),
            capture_occurrence_id="capture-v2-too-early",
            slot_start_utc=datetime(2026, 9, 20, 12, 1, 30, tzinfo=UTC),
        )


def test_distinct_policy_identity_cannot_overlap_existing_active_policy() -> None:
    owner = build_owner()
    register_policy(owner, policy())
    with pytest.raises((TypeError, ValueError)):
        register_policy(
            owner,
            policy(
                scope_policy_id="scope-policy-002",
                scope_policy_version=1,
                activation_ts_utc=datetime(2026, 9, 20, 12, 1, tzinfo=UTC),
                deactivation_ts_utc=datetime(2026, 9, 20, 12, 3, tzinfo=UTC),
                eligibility_policy_ref="eligibility-policy:fixture-002:v1",
            ),
        )


def test_distinct_policy_identity_may_follow_without_active_interval_overlap() -> None:
    owner = build_owner()
    register_policy(owner, policy())
    successor = register_policy(
        owner,
        policy(
            scope_policy_id="scope-policy-002",
            scope_policy_version=1,
            activation_ts_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
            deactivation_ts_utc=None,
            eligibility_policy_ref="eligibility-policy:fixture-002:v1",
        ),
    )
    assert str(successor.scope_policy_id) == "scope-policy-002"
    capture = realise_capture(
        owner,
        scope_policy_ref=policy_ref("scope-policy-002", 1),
        capture_occurrence_id="capture-policy-002-first",
        slot_start_utc=datetime(2026, 9, 20, 12, 2, tzinfo=UTC),
    )
    assert str(capture.scope_policy_ref) == "scope-policy-002@1"
