from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from tests.product.raw_signal._support import build_owner, policy, realise_capture, register_policy


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
    assert first.scope_policy_ref == second.scope_policy_ref == "scope-policy-001@1"


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
    assert owner.reads.get_scheduled_capture_occurrence("capture-v1") == earlier
    assert earlier.scope_policy_ref == "scope-policy-001@1"


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


def test_absent_deactivation_is_preserved_as_absence() -> None:
    owner = build_owner()
    value = policy(deactivation_ts_utc=None)
    stored = register_policy(owner, value)
    assert stored.deactivation_ts_utc is None
    assert not getattr(stored, "perpetual_service", False)
